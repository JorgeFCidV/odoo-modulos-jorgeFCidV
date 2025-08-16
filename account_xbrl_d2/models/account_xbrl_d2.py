from odoo import models, fields
import base64
from lxml import etree

class AccountXBRLExporter(models.Model):
    _name = "account.xbrl.exporter"
    _description = "XBRL Exporter for D2"

    name = fields.Char(default="Export XBRL D2")
    file_data = fields.Binary("XBRL File", readonly=True)
    file_name = fields.Char("Filename", readonly=True)

    def generate_xbrl(self, fiscal_year):
        balance_lines = self.env["account.balance.report"]._get_lines(fiscal_year)
        pyg_lines = self.env["account.profit.loss.report"]._get_lines(fiscal_year)

        nsmap = {"xbrli": "http://www.xbrl.org/2003/instance"}
        root = etree.Element("{http://www.xbrl.org/2003/instance}xbrl", nsmap=nsmap)

        for line in balance_lines:
            concept_name = self._map_account_to_xbrl_concept(line.get("code"))
            value = line.get("balance")
            if concept_name:
                elem = etree.SubElement(root, concept_name)
                elem.text = str(value)

        file_content = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="UTF-8")
        file_name = f"xbrl_d2_{fiscal_year.name}.xml"
        self.write({
            "file_data": base64.b64encode(file_content),
            "file_name": file_name
        })
        return file_name

    def _map_account_to_xbrl_concept(self, account_code):
        mapping = {
            "100": "ActivoNoCorriente",
            "200": "PatrimonioNeto"
        }
        return mapping.get(account_code)
