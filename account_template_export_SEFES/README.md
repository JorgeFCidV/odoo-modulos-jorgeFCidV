Account Template Export (.xlsm) - MIS integration
==================================================
Este módulo permite rellenar una plantilla .xlsm (hoja "Cuentas", nombres en columna A desde fila 14)
con los importes obtenidos desde una instancia MIS (mis_builder). Mantiene macros al usar openpyxl con keep_vba=True.

Instalación:
- Colocar la carpeta en addons.
- Instalar dependencia Python: pip install openpyxl
- Actualizar apps y activar el módulo.
- Subir tu plantilla en "Plantillas" (opcional) o copiarla a static/template.xlsm

Uso:
- Contabilidad > Informes > Informes Personalizados > Exportar plantilla .xlsm (MIS)
- Seleccionar rango y la instancia MIS deseada (por ejemplo "Balance PYMEs (PGCE2008)")
- Generar y descargar
