# Instrucciones para Agentes de IA - Módulo Account Template Export SEFES

## Arquitectura y Componentes Principales

Este es un módulo de Odoo 17 que permite exportar datos financieros desde informes MIS Builder a plantillas Excel (.xlsm) manteniendo las macros VBA.

### Componentes Clave:
- `models/template_model.py`: Define `account.excel.template` para almacenar plantillas Excel
- `models/export_wizard.py`: Contiene `account.template.export.wizard` que maneja la lógica de exportación
- `static/template.xlsm`: Plantilla Excel predeterminada

## Flujo de Datos
1. Usuario selecciona una instancia MIS y opcionalmente una plantilla personalizada
2. El sistema extrae datos del informe MIS usando `_get_mis_values()`
3. Los valores se escriben en la hoja "Cuentas" de la plantilla Excel, columna C desde la fila 14
4. Se preservan las macros VBA usando `openpyxl` con `keep_vba=True`

## Convenciones Importantes
- Las plantillas Excel DEBEN tener una hoja llamada "Cuentas"
- Los nombres de cuentas se leen de la columna A desde la fila 14
- Los valores se escriben en la columna C
- Se normalizan los nombres de cuentas a minúsculas para la comparación

## Dependencias Críticas
```python
'depends': ['account', 'mis_builder', 'report_xlsx']
```
- Python: `openpyxl` (requerido para manipular archivos .xlsm)

## Puntos de Integración
- MIS Builder: Integración principal a través de `mis.report.instance`
- Se adapta a la API de Odoo 17 usando `_get_report_data()` o `_compute_report_data()`

## Patrones de Desarrollo
- Manejo de errores explícito con mensajes de usuario claros
- Soporte para plantillas personalizadas o predeterminada en `static/`
- Valores no encontrados se establecen a 0.0 en lugar de N/D
- Redondeo a 2 decimales para todos los valores exportados

## Comandos y Flujos de Desarrollo
1. Instalación:
   ```bash
   pip install openpyxl
   ```
2. Ubicación de archivos de prueba:
   - Plantilla ejemplo: `static/2101_OC_Plantilla_Visualizador.xlsm`
   - Plantilla base: `static/template.xlsm`

## Referencias de Archivos Clave
- Vista principal: `views/account_template_export_views.xml`
- Seguridad: `security/ir.model.access.csv`