from odoo import models, fields
from odoo.exceptions import UserError
import base64
import io
import zipfile
import mimetypes

class ExportAttachmentWizard(models.TransientModel):
    _name = 'export.attachment.wizard'
    _description = 'Exportar adjuntos de facturas'

    partner_id = fields.Many2one('res.partner', string='Proveedor', required=True, domain=[('supplier_rank', '>', 0)])
    date_from = fields.Date('Desde', required=True)
    date_to = fields.Date('Hasta', required=True)
    datas_file = fields.Binary('Archivo ZIP')
    datas_fname = fields.Char('Nombre del archivo')

    def action_export(self):
        domain = [
            ('partner_id', '=', self.partner_id.id),
            ('date', '>=', self.date_from),
            ('date', '<=', self.date_to),
            ('move_type', 'in', ['in_invoice', 'in_refund']),
        ]
        invoices = self.env['account.move'].search(domain)
        attachments = self.env['ir.attachment'].search([
            ('res_model', '=', 'account.move'),
            ('res_id', 'in', invoices.ids),
            ('type', '=', 'binary'),
        ])

        if not attachments:
            raise UserError("No se encontraron adjuntos para exportar.")

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zipf:
            for att in attachments:
                if not att.datas:
                    continue
                invoice = self.env['account.move'].browse(att.res_id)
                invoice_name = invoice.name or 'SinNombre'  # Nº de factura
                provider_name = invoice.partner_id.name or 'Proveedor'
                invoice_ref = invoice.ref or 'SinReferencia'
                invoice_date = invoice.date and invoice.date.strftime('%Y-%m-%d') or 'SinFecha'

                safe_invoice = invoice_name.replace('/', '_').replace(' ', '_')
                safe_provider = provider_name.replace('/', '_').replace(' ', '_')
                safe_ref = invoice_ref.replace('/', '_').replace(' ', '_')

                extension = att.mimetype and mimetypes.guess_extension(att.mimetype) or '.bin'
                filename = f"{safe_invoice}_{safe_provider}_{safe_ref}_{invoice_date}{extension}"

                file_data = base64.b64decode(att.datas)
                zipf.writestr(filename, file_data)

        zip_data = base64.b64encode(zip_buffer.getvalue())
        self.write({
            'datas_file': zip_data,
            'datas_fname': 'adjuntos_facturas.zip'
        })

        return {
            "type": "ir.actions.act_url",
            "url": f"/web/content/?model={self._name}&id={self.id}&field=datas_file&filename_field=datas_fname&download=true",
            "target": "new",
        }
