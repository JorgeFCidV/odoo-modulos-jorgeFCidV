# 📋 Tarea Adicional: Facturación Especial en Régimen REBU

**Fecha**: 14 de noviembre de 2025  
**Estado**: ESPECIFICACIÓN DE DISEÑO  
**Versión**: 1.0

---

## 📖 Resumen Ejecutivo

Según AEAT y regulaciones de facturación, las facturas en régimen REBU deben cumplir requisitos especiales:

1. ❌ **NO deben desglosar IVA** en líneas
2. ✅ **Deben incluir referencia explícita** al régimen especial REBU
3. ✅ **Deben documentar base imponible** (margen)

**Objetivo**: Crear lógica para aplicar automáticamente estas reglas al generar facturas REBU.

---

## ⚖️ Requisitos AEAT para Facturación REBU

### Fuente Oficial

**AEAT - Obligaciones de Facturación REBU:**
```
https://sede.agenciatributaria.gob.es/Sede/iva/regimenes-tributacion-iva/
regimen-especial-bienes-usados/obligaciones-facturacion.html
```

---

## 🔴 Problema Actual

### Factura Estándar Odoo (❌ No es válida para REBU)

```
FACTURA DE VENTA - RÉGIMEN GENERAL
════════════════════════════════════════════════════════════

Concepto                      Cantidad  Precio Unit.  Total sin IVA
─────────────────────────────────────────────────────────────────
Cuadro "La Noche Estrellada"     1        1.200€       1.200€

SUBTOTAL:                                              1.200€
IVA 21% (desglosado):                                    252€  ← ❌ NO
────────────────────────────────────────────────────────────────
TOTAL:                                                 1.452€
```

### Factura Requerida para REBU (✅ Válida según AEAT)

```
FACTURA DE VENTA - RÉGIMEN ESPECIAL DE BIENES USADOS
════════════════════════════════════════════════════════════

Concepto                      Cantidad  Precio Unit.  Total
─────────────────────────────────────────────────────────────
Cuadro "La Noche Estrellada"     1        1.200€     1.200€

─ RÉGIMEN ESPECIAL REBU ─────────────────────────────────
Margen bruto:                                     484€
Base imponible (AEAT):                            400€
IVA 21%:                                           84€

Operación acogida al Régimen Especial de Bienes Usados
════════════════════════════════════════════════════════════
TOTAL:                                           1.284€

* Factura especial sin desglose de IVA por línea
* IVA calculado sobre base imponible (margen)
```

---

## ✅ Cambios Requeridos

### 1. Campos en Factura

**Nueva tabla**: `account.move` (REBU fields)

```python
is_rebu_invoice = fields.Boolean(
    string="Es factura REBU",
    help="Indica si la factura aplica régimen especial REBU",
)

rebu_total_margin = fields.Float(
    string="Margen total REBU",
    compute="_compute_rebu_totals",
    help="Suma de márgenes de todas las líneas REBU",
)

rebu_total_taxable_base = fields.Float(
    string="Base imponible total REBU",
    compute="_compute_rebu_totals",
    help="Suma de bases imponibles según AEAT",
)

rebu_tax_amount = fields.Float(
    string="IVA según base REBU",
    compute="_compute_rebu_totals",
    help="IVA calculado sobre base imponible REBU",
)
```

### 2. Lógica de Detección Automática

```python
@api.onchange("fiscal_position_id", "invoice_line_ids")
def _onchange_detect_rebu(self):
    """
    Detectar automáticamente si es factura REBU.
    
    Regla: Si posición fiscal es REBU, es factura REBU.
    """
    if self.fiscal_position_id:
        self.is_rebu_invoice = "REBU" in self.fiscal_position_id.name.upper()
```

### 3. Cálculos Agregados

```python
@api.depends("invoice_line_ids", "is_rebu_invoice")
def _compute_rebu_totals(self):
    """Calcular totales REBU para toda la factura"""
    for invoice in self:
        if invoice.is_rebu_invoice:
            total_margin = sum(
                line.rebu_margin 
                for line in invoice.invoice_line_ids 
                if line.is_rebu_good
            )
            total_base = sum(
                line.rebu_taxable_base 
                for line in invoice.invoice_line_ids 
                if line.is_rebu_good
            )
            invoice.rebu_total_margin = total_margin
            invoice.rebu_total_taxable_base = total_base
            invoice.rebu_tax_amount = total_base * 0.21
        else:
            invoice.rebu_total_margin = 0.0
            invoice.rebu_total_taxable_base = 0.0
            invoice.rebu_tax_amount = 0.0
```

---

## 🎨 Diseño de Factura en Odoo

### Factura de Venta REBU - Formulario

```
┌──────────────────────────────────────────────────────────────────┐
│ FACTURA DE VENTA                                                 │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ Cliente: La Pinacoteca de Arte Moderno                          │
│ Fecha: 14/11/2025                                               │
│                                                                  │
│ ☑ Régimen Especial REBU                                        │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│ LÍNEAS DE FACTURA                                                │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ Concepto              Cantidad  Precio Unit.  Subtotal          │
│ ───────────────────────────────────────────────────────────────│
│ Cuadro "Noche Est."      1      1.200€       1.200€            │
│                                                                  │
│ [Más líneas...]                                                 │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│ RESUMEN FINANCIERO                                               │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ Subtotal sin IVA:                              1.200€           │
│                                                                  │
│ ┌─ RÉGIMEN ESPECIAL REBU ──────────────────────────────────┐  │
│ │ Margen bruto total:                           484€       │  │
│ │ Base imponible (según AEAT):                  400€       │  │
│ │ IVA 21%:                                       84€       │  │
│ └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│ TOTAL:                                         1.284€           │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│ NOTAS                                                            │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ * Esta factura está acogida al Régimen Especial de Bienes     │
│   Usados (REBU) según normativa AEAT.                          │
│ * La base imponible se calcula sobre el margen bruto de la    │
│   operación.                                                   │
│ * El IVA no se desglos en línea sino como cantidad global.    │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 📋 Impresión de Factura (PDF)

### Formato PDF REBU

```
FACTURA
═══════════════════════════════════════════════════════════════════

De:   Galería de Arte Moderno
      Calle Principal 123, 28001 Madrid
      CIF: A12345678

Para: La Pinacoteca
      Avenida del Arte 456, 28002 Madrid

Factura: 2025-001      Fecha: 14/11/2025      Vencimiento: 14/12/2025

───────────────────────────────────────────────────────────────────

RÉGIMEN ESPECIAL DE BIENES USADOS (REBU) - AEAT

───────────────────────────────────────────────────────────────────

Descripción del bien                  Precio de compra    Precio de venta
─────────────────────────────────────────────────────────────────────
Cuadro "La Noche Estrellada"         968,00€             1.452,00€
Escultura "David"                    1.240,00€           1.800,00€

SUBTOTAL OPERACIONES REBU                                   3.252,00€

CÁLCULO DEL IVA SEGÚN AEAT (MARGEN BRUTO):

Margen bruto total (Venta - Compra):                           484,00€
Base imponible = (Margen × 100) ÷ 121:                        400,00€
IVA 21%:                                                       84,00€

───────────────────────────────────────────────────────────────────

TOTAL A PAGAR:                                               3.336,00€

───────────────────────────────────────────────────────────────────

NOTAS IMPORTANTES:

* Esta factura está acogida al Régimen Especial de Bienes Usados
  (REBU) según las disposiciones de la Agencia Tributaria Española.

* La base imponible del IVA se calcula sobre el margen bruto de la
  operación (diferencia entre precio de venta y precio de compra),
  no sobre el precio de venta total.

* El IVA no se desglose por línea sino como cantidad global según
  fórmula AEAT: BI = (Margen × 100) ÷ (100 + 21) = (Margen × 100) ÷ 121

* Para más información sobre este régimen, consulte:
  https://sede.agenciatributaria.gob.es/

```

---

## 🔧 Implementación Técnica

### 1. Nuevo Modelo: `models/account_move_rebu.py`

```python
# Copyright 2025 Jorge Fernández
# License AGPL-3.0 or later

from odoo import api, fields, models


class AccountMoveRebu(models.Model):
    """
    Extensión de factura para soporte REBU.
    Gestiona facturación especial en régimen REBU.
    """

    _inherit = "account.move"

    # Campos REBU
    is_rebu_invoice = fields.Boolean(
        string="Es factura REBU",
        compute="_compute_is_rebu_invoice",
        help="Indica si la factura aplica régimen especial REBU",
    )

    rebu_total_margin = fields.Monetary(
        string="Margen total REBU",
        compute="_compute_rebu_totals",
        currency_field="company_currency_id",
        help="Suma de márgenes de todas las líneas REBU",
    )

    rebu_total_taxable_base = fields.Monetary(
        string="Base imponible total REBU",
        compute="_compute_rebu_totals",
        currency_field="company_currency_id",
        help="Suma de bases imponibles según AEAT",
    )

    rebu_tax_amount = fields.Monetary(
        string="IVA según base REBU",
        compute="_compute_rebu_totals",
        currency_field="company_currency_id",
        help="IVA calculado sobre base imponible REBU",
    )

    @api.depends("fiscal_position_id")
    def _compute_is_rebu_invoice(self):
        """Detectar automáticamente si es factura REBU"""
        for invoice in self:
            if invoice.fiscal_position_id:
                invoice.is_rebu_invoice = (
                    "REBU" in invoice.fiscal_position_id.name.upper()
                )
            else:
                invoice.is_rebu_invoice = False

    @api.depends("invoice_line_ids", "is_rebu_invoice")
    def _compute_rebu_totals(self):
        """Calcular totales REBU para toda la factura"""
        for invoice in self:
            if invoice.is_rebu_invoice and invoice.move_type in (
                "out_invoice",
                "in_invoice",
            ):
                total_margin = sum(
                    line.rebu_margin
                    for line in invoice.invoice_line_ids
                    if line.is_rebu_good
                )
                total_base = sum(
                    line.rebu_taxable_base
                    for line in invoice.invoice_line_ids
                    if line.is_rebu_good
                )
                invoice.rebu_total_margin = total_margin
                invoice.rebu_total_taxable_base = total_base
                invoice.rebu_tax_amount = total_base * 0.21
            else:
                invoice.rebu_total_margin = 0.0
                invoice.rebu_total_taxable_base = 0.0
                invoice.rebu_tax_amount = 0.0
```

### 2. Actualizar `models/__init__.py`

```python
from . import account_chart_template
from . import account_invoice_line_rebu
from . import account_move_rebu  # ← NUEVO
```

---

## 🖨️ Plantilla de Reporte (Fase 2)

**Archivo**: `reports/account_invoice_rebu_report.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <!-- Reporte de factura REBU -->
        <record id="account_invoice_rebu_report" model="ir.actions.report">
            <field name="name">Factura REBU</field>
            <field name="model">account.move</field>
            <field name="report_type">qweb-pdf</field>
            <field name="report_name">l10n_es_rebu.account_invoice_rebu_report</field>
            <field name="print_report_name">'Factura REBU %s' % object.name</field>
        </record>

        <!-- Template PDF -->
        <template id="account_invoice_rebu_report_template">
            <!-- Sección REBU especial en PDF -->
            <t t-if="o.is_rebu_invoice">
                <div class="alert alert-info">
                    <h4>RÉGIMEN ESPECIAL DE BIENES USADOS (REBU)</h4>
                    <p>Esta factura está acogida al Régimen Especial de Bienes Usados según normativa AEAT.</p>
                </div>
                <table class="table table-sm">
                    <tr>
                        <th>Margen bruto total</th>
                        <td><t t-esc="o.rebu_total_margin"/></td>
                    </tr>
                    <tr>
                        <th>Base imponible (AEAT)</th>
                        <td><t t-esc="o.rebu_total_taxable_base"/></td>
                    </tr>
                    <tr>
                        <th>IVA 21%</th>
                        <td><t t-esc="o.rebu_tax_amount"/></td>
                    </tr>
                </table>
            </t>
        </template>
    </data>
</odoo>
```

---

## 📄 Cambios en Plantilla Impresión

### Ocultar desglose de IVA por línea en REBU

```xml
<!-- En vista estándar de factura, agregar -->
<t t-if="not o.is_rebu_invoice">
    <!-- Mostrar IVA desglosado por línea -->
    <column>Impuestos</column>
</t>

<t t-if="o.is_rebu_invoice">
    <!-- NO mostrar IVA desglosado, mostrarlo al final -->
    <!-- Ver sección "CÁLCULO DEL IVA SEGÚN AEAT" -->
</t>
```

---

## 🔄 Flujo de Generación de Factura REBU

```
1. CREAR FACTURA
   │
   ├─ Seleccionar cliente REBU
   ├─ Seleccionar posición fiscal REBU
   └─ Sistema detecta: is_rebu_invoice = True ✓
   
2. AGREGAR LÍNEAS
   │
   ├─ Línea 1: Bien artístico
   │  ├─ is_rebu_good = True ✓
   │  ├─ rebu_purchase_price = 968€
   │  └─ rebu_sale_price = 1.452€
   │
   └─ Línea N: Bien artístico
      ├─ is_rebu_good = True ✓
      ├─ rebu_purchase_price = ...
      └─ rebu_sale_price = ...

3. CÁLCULOS AUTOMÁTICOS
   │
   ├─ Margen por línea = venta - compra
   ├─ BI por línea = (margen × 100) ÷ 121
   ├─ Margen total = suma márgenes
   ├─ BI total = suma bases
   └─ IVA total = BI total × 0.21

4. GENERAR FACTURA
   │
   ├─ Mostrar líneas (SIN desglose IVA)
   ├─ Mostrar sección REBU
   │  ├─ Margen bruto
   │  ├─ Base imponible
   │  └─ IVA total
   └─ Mostrar nota sobre régimen REBU

5. IMPRIMIR/EXPORTAR
   │
   └─ PDF con formato especial REBU
```

---

## 📊 Comparativa: Factura Normal vs REBU

### Factura Normal (IVA Desglosado)

```
Línea 1: Producto A           100€
         IVA 21%:              21€
         ────────────────────────
         Subtotal:           121€

Línea 2: Producto B           200€
         IVA 21%:              42€
         ────────────────────────
         Subtotal:           242€

────────────────────────────────────
TOTAL:                        363€
```

### Factura REBU (SIN Desglose IVA)

```
Línea 1: Bien Artístico      1.200€
Línea 2: Bien Artístico      1.500€

────────────────────────────────────
Subtotal:                    2.700€

RÉGIMEN ESPECIAL REBU:
  Margen bruto:               700€
  Base imponible:             578€
  IVA 21%:                    121€

────────────────────────────────────
TOTAL:                      2.821€
```

---

## ✅ Checklist de Requisitos AEAT

- [ ] Factura indica "Régimen Especial REBU"
- [ ] NO desglose IVA por línea
- [ ] Muestra margen bruto
- [ ] Muestra base imponible (fórmula AEAT)
- [ ] Muestra IVA como cantidad global
- [ ] Incluye nota sobre régimen
- [ ] Referencia a AEAT en factura
- [ ] Precio compra documentado
- [ ] Precio venta documentado
- [ ] Cálculos auditable

---

## 🎯 Fases de Implementación

### Fase 2a (Tarea 4)
- ✅ Especificación (este documento)
- ⏳ Crear modelo `account_move_rebu.py`
- ⏳ Crear vistas XML

### Fase 2b (Tarea adicional)
- ⏳ Crear reporte PDF especial
- ⏳ Integrar con sistema de impresión
- ⏳ Crear tests

### Fase 3
- ⏳ Automatización de notas
- ⏳ Exportación XML factura
- ⏳ Integración SAT (si aplica)

---

## 📞 Referencias AEAT

- **Obligaciones Facturación REBU**: https://sede.agenciatributaria.gob.es/Sede/iva/regimenes-tributacion-iva/regimen-especial-bienes-usados/obligaciones-facturacion.html
- **Documentación REBU**: `VALIDACION_AEAT.md`
- **Recomendaciones**: `RECOMENDACIONES_AEAT.md`

---

**Documento**: ESPECIFICACION_FACTURACION_REBU_ESPECIAL.md  
**Estado**: 📋 ESPECIFICACIÓN (Tarea Adicional)  
**Próximo Paso**: Implementar en Fase 2b
