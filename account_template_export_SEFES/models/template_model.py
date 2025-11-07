from odoo import models, fields  # pyright: ignore[reportMissingImports]

class AccountExcelTemplate(models.Model):
    _name = "account.excel.template"
    _description = "Plantilla Excel para informes contables (.xlsm)"

    name = fields.Char(required=True)
    file = fields.Binary(string="Fichero .xlsm", required=True)
    filename = fields.Char(string="Filename")
    company_id = fields.Many2one('res.company', string="Compañía")
    note = fields.Text()
