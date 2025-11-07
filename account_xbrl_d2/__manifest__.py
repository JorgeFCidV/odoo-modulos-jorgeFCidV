{
    "name": "Account XBRL Export for D2",
    "version": "17.0.2.0.0",
    "author": "Tu Empresa, OCA",
    "website": "https://github.com/tuempresa/account_xbrl_d2",
    "category": "Accounting/Localizations",
    "license": "AGPL-3",
    "summary": "Exporta cuentas anuales en formato XBRL para el D2 del Registro Mercantil",
    "depends": [
        "l10n_es_account_balance_report",
        "account"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/export_xbrl_wizard_views.xml",
        "views/menu_views.xml"
    ],
    "installable": True,
    "application": False
}