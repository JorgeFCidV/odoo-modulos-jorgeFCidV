from odoo import models, fields

class AccountExcelTemplate(models.Model):
    _name = 'account.excel.template'
    _description = 'Plantilla Excel para exportación contable'

    name = fields.Char(string="Nombre", required=True)
    file = fields.Binary(string="Archivo .xlsm", required=True)
    filename = fields.Char(string="Nombre del archivo")
