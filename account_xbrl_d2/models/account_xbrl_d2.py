import os
import base64
import json
from lxml import etree
from odoo import models, fields

class AccountXBRLExporter(models.Model):
    _name = "account.xbrl.exporter"
    _description = "XBRL Exporter for D2"

    name = fields.Char(default="Export XBRL D2")
    file_data = fields.Binary("XBRL File", readonly=True)
    file_name = fields.Char("Filename", readonly=True)

    def _load_mapping(self, taxonomy_type):
        module_path = os.path.dirname(os.path.dirname(__file__))  # raíz del módulo
        file_path = os.path.join(module_path, "data", f"xbrl_mapping_pgc_{taxonomy_type}.json")
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def generate_xbrl(self, fiscal_year, taxonomy_type="abreviado"):
        mapping = self._load_mapping(taxonomy_type)
        nsmap = mapping.get("namespaces", {})
        root = etree.Element("{http://www.xbrl.org/2003/instance}xbrl", nsmap=nsmap)

        # Aquí deberías mapear los saldos de balance y PyG contra el JSON
        # De momento solo generamos un archivo vacío válido
        comment = etree.Comment(f"Exportación XBRL {taxonomy_type} para {fiscal_year.name}")
        root.append(comment)

        file_content = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="UTF-8")
        file_name = f"xbrl_d2_{taxonomy_type}_{fiscal_year.name}.xml"
        self.write({
            "file_data": base64.b64encode(file_content),
            "file_name": file_name
        })
        return file_name
