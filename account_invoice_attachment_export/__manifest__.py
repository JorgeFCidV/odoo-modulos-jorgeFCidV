{
    'name': 'Exportación de adjuntos de facturas',
    'version': '17.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Exporta los documentos adjuntos de facturas de proveedor en un ZIP',
    'author': 'Jorge Fernández-Cid',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'views/export_attachment_wizard_views.xml',
        'views/menu.xml',
        'views/res_partner_view.xml',
    ],
    'license': 'AGPL-3',
    'application': False,
}
