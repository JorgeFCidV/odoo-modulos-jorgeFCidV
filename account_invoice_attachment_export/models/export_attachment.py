from odoo import models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    def action_open_attachment_export_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Exportar adjuntos de facturas',
            'res_model': 'export.attachment.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_partner_id': self.id},
        }
