from odoo import models, fields

class ExportXBRLWizard(models.TransientModel):
    _name = "export.xbrl.wizard"
    _description = "Exportar XBRL para D2"

    fiscal_year_id = fields.Many2one("account.fiscal.year", string="Ejercicio", required=True)

    def action_export_xbrl(self):
        exporter = self.env["account.xbrl.exporter"].create({})
        exporter.generate_xbrl(self.fiscal_year_id)
        return {
            "type": "ir.actions.act_url",
            "url": f"/web/content/{exporter.id}/file_data/{exporter.file_name}?download=true",
            "target": "self",
        }
