from odoo import models, fields, api, _  # pyright: ignore[reportMissingImports]
from odoo.exceptions import UserError, ValidationError  # pyright: ignore[reportMissingImports]
import base64
import io
import openpyxl  # pyright: ignore[reportMissingModuleSource]
import json
import logging

_logger = logging.getLogger(__name__)

class AccountTemplateExportWizard(models.TransientModel):
    _name = "account.template.export.wizard"
    _description = "Exportar plantilla Excel rellenada con informes MIS"

    company_id = fields.Many2one('res.company', string="Compañía", required=True, default=lambda self: self.env.company)
    mis_instance_id = fields.Many2one('mis.report.instance', string="Instancia MIS", required=True)
    template_id = fields.Many2one('account.excel.template', string="Plantilla (.xlsm)")
    generated_file = fields.Binary(string="Fichero generado", readonly=True)
    generated_filename = fields.Char(string="Nombre fichero", readonly=True)

    def _load_template_bytes(self):
        template_data = None
        if self.template_id and self.template_id.file:
            template_data = base64.b64decode(self.template_id.file)
        else:
            import os
            module_path = os.path.dirname(__file__)
            static_path = os.path.join(module_path, '..', 'static', 'template.xlsm')
            static_path = os.path.normpath(static_path)
            if os.path.exists(static_path):
                with open(static_path, 'rb') as f:
                    template_data = f.read()
        if not template_data:
            raise UserError(_("No se encontró la plantilla XLSM."))
        return template_data

    def _get_mis_values(self):
        """Obtiene los valores del informe MIS (compatible con Odoo 17)."""
        self.ensure_one()
        mis = self.mis_instance_id
        if not mis:
            raise UserError(_("Selecciona una instancia MIS."))

        try:
            # Obtener el periodo actual de la instancia MIS
            period = mis.period_ids and mis.period_ids[0] or False
            if not period:
                raise UserError(_("La instancia MIS no tiene periodos definidos."))

            # Calcular el informe para el periodo
            matrix = mis._compute_matrix()
            if not matrix:
                raise UserError(_("No se pudo calcular la matriz de resultados del informe MIS."))

            # Procesar los resultados
            values = {}
            for row in matrix.iter_rows():
                # El nombre puede estar en label o en description
                name = str(row.kpi.description or row.kpi.name or "").strip().lower()
                if name:
                    # Obtener el valor del primer periodo (o el especificado)
                    cell = row.cells[period.id]
                    if cell and hasattr(cell, 'val'):
                        try:
                            val = float(cell.val or 0.0)
                        except (ValueError, TypeError):
                            val = 0.0
                        values[name] = val

            if not values:
                raise UserError(_("No se encontraron valores en el informe MIS."))

            return values

        except Exception as e:
            _logger.error("Error al obtener valores MIS: %s", str(e))
            raise UserError(_("Error al calcular el MIS: %s") % str(e))

    def action_generate(self):
        self.ensure_one()
        mis_values = self._get_mis_values()
        if not mis_values:
            raise UserError(_("No se encontraron valores en la instancia MIS seleccionada."))

        template_data = self._load_template_bytes()
        wb = openpyxl.load_workbook(io.BytesIO(template_data), keep_vba=True)
        if 'Cuentas' not in wb.sheetnames:
            raise UserError(_("La plantilla debe tener una hoja llamada 'Cuentas'."))
        ws = wb['Cuentas']

        row = 14
        while True:
            cell_value = ws[f"A{row}"].value
            if not cell_value:
                break
            name = str(cell_value).strip().lower()
            val = mis_values.get(name, 0.0)  # usar 0 en lugar de N/D
            ws[f"C{row}"] = round(val, 2)
            row += 1

        out = io.BytesIO()
        wb.save(out)
        out.seek(0)
        file_data = out.read()
        
        # Guardar el archivo generado
        self.write({
            'generated_file': base64.b64encode(file_data),
            'generated_filename': f"{self.company_id.name.replace(' ', '_')}_MIS_{fields.Date.today()}.xlsm"
        })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.template.export.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
            'context': self._context,
        }
