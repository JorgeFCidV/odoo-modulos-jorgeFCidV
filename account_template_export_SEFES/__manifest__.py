{
    'name': 'Account Template Export (MIS) SEFES',
    'version': '17.0.1.0',
    'summary': 'Exporta plantilla Excel (.xlsm) con datos del informe MIS seleccionado',
    'category': 'Accounting/Reporting',
    'author': 'OCA Fan Adapted by ChatGPT',
    'license': 'AGPL-3',
    'depends': ['account', 'mis_builder', 'report_xlsx'],
    'data': [
        'views/account_template_export_views.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
