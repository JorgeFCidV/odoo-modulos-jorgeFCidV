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
            _logger.info("Iniciando extracción de datos MIS para instancia: %s", mis.name)
            
            # Obtener el periodo actual de la instancia MIS
            period = mis.period_ids and mis.period_ids[0] or False
            _logger.info("Periodo seleccionado: %s", period.name if period else "Ninguno")
            if not period:
                raise UserError(_("La instancia MIS no tiene periodos definidos."))

            # Calcular el informe para el periodo
            _logger.info("Calculando matriz MIS para periodo %s", period.name)
            
            # Intentar obtener los datos del informe
            matrix = None
            if hasattr(mis, 'compute'):
                matrix = mis.compute()
            elif hasattr(mis, '_compute_matrix'):
                matrix = mis._compute_matrix()
            
            if not matrix:
                raise UserError(_("No se pudo calcular la matriz de resultados del informe MIS."))

            # Procesar los resultados
            values = {}
            rows_processed = 0
            values_found = 0
            
            for row in matrix.iter_rows():
                rows_processed += 1
                # El nombre puede estar en label o en description
                name = str(getattr(row, 'description', '') or getattr(row, 'name', '') or "").strip().lower()
                _logger.debug("Procesando fila KPI: %s", name)
                
                if name:
                    try:
                        # Obtener el valor directamente del row
                        val = 0.0
                        if hasattr(row, 'val'):
                            val = float(row.val or 0.0)
                        elif hasattr(row, 'total'):
                            val = float(row.total or 0.0)
                        elif hasattr(row, 'amount'):
                            val = float(row.amount or 0.0)
                        
                        values[name] = val
                        values_found += 1
                        _logger.debug("Valor extraído para %s: %f", name, val)
                        
                    except (ValueError, TypeError) as e:
                        val = 0.0
                        values[name] = val
                        _logger.warning("Error convirtiendo valor para %s: %s. Usando 0.0", name, str(e))

            _logger.info("Procesamiento completado: %d filas procesadas, %d valores encontrados", 
                        rows_processed, values_found)

            if not values:
                raise UserError(_("No se encontraron valores en el informe MIS."))

            # Log de algunos valores de ejemplo
            sample_values = dict(list(values.items())[:3])
            _logger.info("Muestra de valores obtenidos: %s", sample_values)

            return values

        except Exception as e:
            _logger.error("Error al obtener valores MIS: %s", str(e), exc_info=True)
            raise UserError(_("Error al calcular el MIS: %s") % str(e))

    def action_generate(self):
        self.ensure_one()
        _logger.info("Iniciando generación de plantilla Excel para compañía: %s", self.company_id.name)
        
        # Obtener valores MIS
        _logger.info("Obteniendo valores del informe MIS: %s", self.mis_instance_id.name)
        mis_values = self._get_mis_values()
        if not mis_values:
            raise UserError(_("No se encontraron valores en la instancia MIS seleccionada."))
        _logger.info("Obtenidos %d valores del informe MIS", len(mis_values))

        # Cargar plantilla
        _logger.info("Cargando plantilla Excel")
        template_data = self._load_template_bytes()
        wb = openpyxl.load_workbook(io.BytesIO(template_data), keep_vba=True)
        if 'Cuentas' not in wb.sheetnames:
            raise UserError(_("La plantilla debe tener una hoja llamada 'Cuentas'."))
        ws = wb['Cuentas']
        _logger.info("Plantilla cargada correctamente")

        # Procesar filas
        row = 14
        valores_escritos = 0
        coincidencias = 0
        while True:
            cell_value = ws[f"A{row}"].value
            if not cell_value:
                _logger.info("Fin de datos en fila %d", row)
                break
                
            name = str(cell_value).strip().lower()
            val = mis_values.get(name, 0.0)  # usar 0 en lugar de N/D
            
            if val != 0.0:
                coincidencias += 1
            
            _logger.debug("Fila %d: '%s' = %f", row, name, val)
            ws[f"C{row}"] = round(val, 2)
            valores_escritos += 1
            row += 1
            
        _logger.info("Procesamiento completado: %d filas procesadas, %d coincidencias encontradas",
                    valores_escritos, coincidencias)

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
