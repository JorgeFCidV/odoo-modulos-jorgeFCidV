# 📋 Tarea 4: Cálculo de Margen Automático en REBU

**Fecha**: 14 de noviembre de 2025  
**Estado**: ESPECIFICACIÓN DE DISEÑO  
**Versión**: 1.0

---

## 📖 Resumen Ejecutivo

Actualmente, el módulo REBU calcula impuestos sobre el 100% del precio, cuando según AEAT debe calcular solo sobre el **margen bruto** (diferencia compra-venta).

**Objetivo**: Automatizar el cálculo de margen en Odoo siguiendo la fórmula AEAT.

---

## ⚠️ Problema Actual

### Cálculo Incorrecto (Fase 1)

```
Compra: 1.000€ (con IVA)
Venta: 1.500€ (con IVA)

Odoo ACTUAL (❌ INCORRECTO):
  IVA venta = 1.500€ × 21% ÷ 1,21 = 261,16€

Según AEAT (✅ CORRECTO):
  Margen = 1.500 - 1.000 = 500€
  BI = (500 × 100) ÷ 121 = 413,22€
  IVA = 413,22 × 0,21 = 86,78€

DIFERENCIA: 261,16 - 86,78 = 174,38€ de IVA excesivo
```

---

## 🎯 Objetivo (Fase 2)

Crear un **modelo personalizado** en Odoo que:

1. ✅ Capture el **precio de compra** de cada artículo
2. ✅ Capture el **precio de venta** de cada artículo
3. ✅ Calcule el **margen bruto** automáticamente
4. ✅ Aplique la **fórmula AEAT** de base imponible
5. ✅ Registre el impuesto correcto en la factura

---

## 📐 Especificación Técnica

### 1. Fórmula AEAT (Base Imponible)

```
BI = (Margen × 100) ÷ (100 + tasa_iva)

Donde:
Margen = Precio_venta - Precio_compra

Para 21% IVA:
BI = (Margen × 100) ÷ 121
```

### 2. Ejemplo Concreto

```
Operación: Compra y reventa de cuadro artístico

COMPRA:
  Precio sin IVA: 800€
  IVA 21%: 168€
  Precio con IVA: 968€

VENTA:
  Precio sin IVA: 1.200€
  IVA 21%: 252€
  Precio con IVA: 1.452€

CÁLCULO MARGEN (AEAT):
  Margen = 1.452€ - 968€ = 484€
  Base Imponible = (484 × 100) ÷ 121 = 400€
  IVA a repercutir = 400€ × 0,21 = 84€
```

---

## 🏗️ Arquitectura de Implementación

### Nivel 1: Base de Datos

**Nuevos campos en `account.invoice.line`:**

```python
# Campos para REBU
rebu_purchase_price = fields.Float(
    "Precio de compra (con IVA)",
    help="Precio de adquisición del bien incluyendo IVA",
)

rebu_sale_price = fields.Float(
    "Precio de venta (con IVA)",
    help="Precio de venta del bien incluyendo IVA",
)

rebu_margin = fields.Float(
    "Margen bruto",
    compute="_compute_rebu_margin",
    help="Diferencia entre venta y compra",
)

rebu_taxable_base = fields.Float(
    "Base imponible REBU",
    compute="_compute_rebu_taxable_base",
    help="Base imponible según fórmula AEAT",
)

is_rebu_good = fields.Boolean(
    "Es bien REBU",
    help="Marca si es bien artístico bajo régimen REBU",
)
```

### Nivel 2: Métodos de Cálculo

**En `account.invoice.line`:**

```python
@api.depends("rebu_purchase_price", "rebu_sale_price")
def _compute_rebu_margin(self):
    """Calcular margen bruto: Venta - Compra"""
    for line in self:
        if line.is_rebu_good and line.rebu_purchase_price and line.rebu_sale_price:
            line.rebu_margin = line.rebu_sale_price - line.rebu_purchase_price
        else:
            line.rebu_margin = 0.0

@api.depends("rebu_margin")
def _compute_rebu_taxable_base(self):
    """Calcular base imponible según AEAT: BI = (Margen × 100) ÷ 121"""
    for line in self:
        if line.is_rebu_good and line.rebu_margin > 0:
            # Fórmula AEAT para 21%
            line.rebu_taxable_base = (line.rebu_margin * 100) / 121
        else:
            line.rebu_taxable_base = 0.0
```

### Nivel 3: Integración con Impuestos

**En `account.invoice`:**

```python
def _compute_taxes_rebu(self):
    """Recalcular impuestos usando base imponible REBU si aplica"""
    for invoice in self:
        if invoice.has_rebu_lines:
            for line in invoice.invoice_line_ids:
                if line.is_rebu_good and line.rebu_taxable_base > 0:
                    # Calcular IVA sobre base REBU
                    tax_amount = line.rebu_taxable_base * 0.21
                    # Aplicar en taxes_id
```

---

## 📋 Diseño de Interfaz de Usuario

### Formulario de Línea de Factura (Compra)

```
┌─────────────────────────────────────────────────────────┐
│ Línea de Factura - Bien Artístico REBU                  │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ Producto: _________________ [Seleccionar]              │
│                                                          │
│ Cantidad: 1     Precio unitario: _________ €           │
│                                                          │
│ ☑ Es bien REBU                                         │
│                                                          │
│ Precio de compra (con IVA): 968€                       │
│ Subtotal: 968€                                          │
│ IVA (21% no deducible): 168€                           │
│ Total con IVA: 968€                                     │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Formulario de Línea de Factura (Venta)

```
┌─────────────────────────────────────────────────────────┐
│ Línea de Factura - Bien Artístico REBU                  │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ Producto: Cuadro "La Noche Estrellada"                 │
│                                                          │
│ Cantidad: 1     Precio unitario: 1.200€                │
│                                                          │
│ ☑ Es bien REBU                                         │
│                                                          │
│ ┌─ INFORMACIÓN REBU ────────────────────────────┐      │
│ │ Precio de compra (con IVA): 968€             │      │
│ │ Precio de venta (con IVA): 1.452€            │      │
│ │ Margen bruto: 484€                           │      │
│ │ Base imponible (AEAT): 400€                  │      │
│ │ IVA a repercutir (21%): 84€                  │      │
│ └─────────────────────────────────────────────────┘      │
│                                                          │
│ Subtotal: 1.200€                                        │
│ IVA (21% incluido REBU): 84€                            │
│ Total: 1.284€                                           │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 💾 Modificaciones de Archivos

### 1. Nuevo modelo: `models/account_invoice_line_rebu.py`

```python
# Copyright 2025 Jorge Fernández
# License AGPL-3.0 or later

from odoo import api, fields, models


class AccountInvoiceLineRebu(models.Model):
    """
    Extensión de línea de factura para soporte REBU.
    Calcula margen bruto y base imponible según AEAT.
    """

    _inherit = "account.move.line"

    # Campos REBU
    is_rebu_good = fields.Boolean(
        string="Es bien REBU",
        default=False,
        help="Marca si es bien artístico bajo régimen REBU",
    )

    rebu_purchase_price = fields.Float(
        string="Precio de compra (con IVA)",
        help="Precio de adquisición del bien incluyendo IVA",
    )

    rebu_sale_price = fields.Float(
        string="Precio de venta (con IVA)",
        help="Precio de venta del bien incluyendo IVA",
    )

    rebu_margin = fields.Float(
        string="Margen bruto",
        compute="_compute_rebu_margin",
        store=True,
        help="Diferencia entre venta y compra",
    )

    rebu_taxable_base = fields.Float(
        string="Base imponible REBU",
        compute="_compute_rebu_taxable_base",
        store=True,
        help="Base imponible según fórmula AEAT: BI = (Margen × 100) ÷ 121",
    )

    @api.depends("rebu_purchase_price", "rebu_sale_price", "is_rebu_good")
    def _compute_rebu_margin(self):
        """Calcular margen bruto: Venta - Compra"""
        for line in self:
            if line.is_rebu_good and line.rebu_purchase_price and line.rebu_sale_price:
                line.rebu_margin = line.rebu_sale_price - line.rebu_purchase_price
            else:
                line.rebu_margin = 0.0

    @api.depends("rebu_margin", "is_rebu_good")
    def _compute_rebu_taxable_base(self):
        """
        Calcular base imponible según AEAT.
        
        Fórmula AEAT para 21% IVA:
        BI = (Margen × 100) ÷ 121
        
        Referencia:
        https://sede.agenciatributaria.gob.es/Sede/iva/regimenes-tributacion-iva/
        regimen-especial-bienes-usados/funcionamiento-rebu.html
        """
        for line in self:
            if line.is_rebu_good and line.rebu_margin > 0:
                # Fórmula AEAT para 21%
                line.rebu_taxable_base = (line.rebu_margin * 100) / 121
            else:
                line.rebu_taxable_base = 0.0

    @api.onchange("rebu_purchase_price", "rebu_sale_price")
    def _onchange_rebu_prices(self):
        """Recalcular automáticamente cuando cambian precios"""
        self._compute_rebu_margin()
        self._compute_rebu_taxable_base()
```

### 2. Actualizar `models/__init__.py`

```python
# Copyright 2025 Jorge Fernández
# License AGPL-3.0 or later

from . import account_chart_template
from . import account_invoice_line_rebu  # ← NUEVO
```

### 3. Actualizar `__manifest__.py`

```python
{
    "name": "REBU - Régimen Especial de Bienes Usados (Bienes Artísticos)",
    "version": "17.0.1.0.0",
    "category": "Localization/Account Charts",
    "website": "https://github.com/JorgeFCidV/odoo-modulos-jorgeFCidV",
    "author": "Jorge Fernández",
    "maintainers": ["JorgeFCidV"],
    "license": "AGPL-3",
    "depends": ["l10n_es"],
    "data": [
        "data/template/account.tax.group-es_common.csv",
        "data/template/account.tax-es_common.csv",
        "data/template/account.fiscal.position-es_common.csv",
        # Vistas para REBU (crear en Fase 2)
        # "views/account_move_line_rebu_views.xml",
    ],
}
```

---

## 🎨 Vistas XML (Fase 2)

**Archivo**: `views/account_move_line_rebu_views.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <!-- Formulario de factura - Agregar campos REBU -->
        <record id="view_move_form_rebu" model="ir.ui.view">
            <field name="name">account.move.form.rebu</field>
            <field name="model">account.move</field>
            <field name="inherit_id" ref="account.view_move_form"/>
            <field name="arch" type="xml">
                <xpath expr="//field[@name='line_ids']" position="after">
                    <!-- Mostrar campos REBU si es posición fiscal REBU -->
                </xpath>
            </field>
        </record>

        <!-- Formulario de línea - Agregar grupo REBU -->
        <record id="view_move_line_form_rebu" model="ir.ui.view">
            <field name="name">account.move.line.form.rebu</field>
            <field name="model">account.move.line</field>
            <field name="inherit_id" ref="account.view_move_line_form"/>
            <field name="arch" type="xml">
                <xpath expr="//field[@name='price_unit']" position="after">
                    <field name="is_rebu_good" widget="boolean"/>
                    <field name="rebu_purchase_price" attrs="{'invisible': [('is_rebu_good', '=', False)]}"/>
                    <field name="rebu_sale_price" attrs="{'invisible': [('is_rebu_good', '=', False)]}"/>
                    <field name="rebu_margin" attrs="{'invisible': [('is_rebu_good', '=', False)]}"/>
                    <field name="rebu_taxable_base" attrs="{'invisible': [('is_rebu_good', '=', False)]}"/>
                </xpath>
            </field>
        </record>
    </data>
</odoo>
```

---

## 🧪 Pruebas Unitarias (Fase 2)

**Archivo**: `tests/test_rebu_margin_calculation.py`

```python
class TestREBUMarginAutomatic(TransactionCase):
    """Tests para cálculo automático de margen REBU"""

    def test_margin_calculation_positive(self):
        """Test: Margen positivo calcula BI correctamente"""
        line = self.env["account.move.line"].create({
            "is_rebu_good": True,
            "rebu_purchase_price": 968.0,
            "rebu_sale_price": 1452.0,
        })
        
        # Margen debe ser 484
        self.assertEqual(line.rebu_margin, 484.0)
        
        # BI debe ser (484 × 100) ÷ 121 = 400
        self.assertAlmostEqual(line.rebu_taxable_base, 400.0, places=2)

    def test_margin_calculation_zero_margin(self):
        """Test: Sin margen BI = 0"""
        line = self.env["account.move.line"].create({
            "is_rebu_good": True,
            "rebu_purchase_price": 1000.0,
            "rebu_sale_price": 1000.0,
        })
        
        self.assertEqual(line.rebu_margin, 0.0)
        self.assertEqual(line.rebu_taxable_base, 0.0)

    def test_no_calculation_if_not_rebu(self):
        """Test: No calcula si no es REBU"""
        line = self.env["account.move.line"].create({
            "is_rebu_good": False,
            "rebu_purchase_price": 968.0,
            "rebu_sale_price": 1452.0,
        })
        
        self.assertEqual(line.rebu_margin, 0.0)
        self.assertEqual(line.rebu_taxable_base, 0.0)
```

---

## 📊 Flujo de Datos

```
COMPRA:
┌─────────────────────────────────────────────────┐
│ Crear factura de compra REBU                    │
│                                                 │
│ Línea: Cuadro artístico                         │
│ - Precio sin IVA: 800€                          │
│ - IVA 21% (no deducible): 168€                 │
│ - Precio con IVA: 968€ ← guardar en linea      │
│                                                 │
│ Odoo registra: rebu_purchase_price = 968€      │
└─────────────────────────────────────────────────┘
                        │
                        ↓
VENTA:
┌─────────────────────────────────────────────────┐
│ Crear factura de venta REBU                     │
│                                                 │
│ Línea: Cuadro artístico                         │
│ - Producto: [buscar bien anterior]              │
│ - Cantidad: 1                                   │
│ - Precio unitario: 1.200€ (sin IVA)            │
│                                                 │
│ El módulo autocompleta:                         │
│ - rebu_purchase_price = 968€ (desde histórico) │
│ - rebu_sale_price = 1.452€ (1.200 + 21% IVA)  │
│                                                 │
│ Cálculos automáticos:                           │
│ - Margen = 1.452 - 968 = 484€                  │
│ - BI = (484 × 100) ÷ 121 = 400€               │
│ - IVA = 400 × 0,21 = 84€ ← se aplica este     │
└─────────────────────────────────────────────────┘
```

---

## ⚙️ Configuración de Producto (Recomendación)

**Crear tipo de producto para REBU:**

```python
# En categoría de producto
class ProductCategory(models.Model):
    _inherit = "product.category"
    
    is_rebu_category = fields.Boolean(
        "Es categoría REBU",
        help="Marcas automáticamente bienes como REBU",
    )

# En producto
class Product(models.Model):
    _inherit = "product.product"
    
    is_rebu_good = fields.Boolean(
        "Es bien REBU",
        related="categ_id.is_rebu_category",
        help="Heredado de categoría",
    )
```

---

## 📝 Documentación de Usuario

### Guía: Crear Factura REBU con Margen

1. **Crear línea de factura**
   - Seleccionar producto (bien artístico REBU)
   - Marcar ☑ "Es bien REBU"
   - Ingresa precio de compra anterior (con IVA)
   - Ingresa precio de venta (sin IVA)

2. **Sistema automáticamente calcula:**
   - Margen bruto
   - Base imponible (AEAT)
   - IVA correcto

3. **Resultado:**
   - Factura muestra IVA correcto
   - Margen documentado
   - AEAT compliant ✓

---

## 🔄 Integración con Campos Existentes

La implementación se integra con campos estándar de Odoo:

```
account.move.line (estándar):
├─ price_unit              (precio sin IVA de línea)
├─ price_subtotal          (subtotal sin IVA)
├─ price_total             (total con IVA)
└─ tax_ids                 (impuestos aplicados)

account.move.line (REBU - nuevos):
├─ is_rebu_good            (marca como REBU)
├─ rebu_purchase_price     (precio histórico compra)
├─ rebu_sale_price         (precio actual venta)
├─ rebu_margin             (computado: venta - compra)
└─ rebu_taxable_base       (computado: BI AEAT)
```

---

## 🎯 Beneficios de la Automatización

### Antes (Manual - Fase 1)

```
❌ Contador calcula manualmente
❌ Riesgo de errores humanos
❌ No hay auditoría de márgenes
❌ Incumplimiento potencial AEAT
```

### Después (Automático - Fase 2)

```
✅ Odoo calcula automáticamente
✅ Sin posibilidad de errores
✅ Auditoría completa de márgenes
✅ 100% conforme AEAT
```

---

## 📋 Checklist de Implementación

### Desarrollo
- [ ] Crear modelo `AccountInvoiceLinesRebu`
- [ ] Implementar métodos de cálculo
- [ ] Crear vistas XML
- [ ] Integrar con impuestos REBU
- [ ] Crear campos en base de datos (migrations)

### Testing
- [ ] Tests unitarios (margen cálculo)
- [ ] Tests integración (factura completa)
- [ ] Validación AEAT fórmula
- [ ] Pruebas manuales en Odoo

### Documentación
- [ ] Guía de usuario
- [ ] Documentación técnica
- [ ] Ejemplos prácticos
- [ ] Troubleshooting

### Validación
- [ ] QA interno
- [ ] Asesor fiscal (validar fórmula)
- [ ] Testing en producción

---

## 🚀 Fases de Implementación

### Fase 2a (Actual)
- ✅ Especificación de diseño (este documento)
- ⏳ Crear modelo
- ⏳ Crear vistas
- ⏳ Crear tests

### Fase 2b (Siguiente)
- ⏳ Integración con facturación
- ⏳ Reportes de márgenes
- ⏳ Auditoría de cálculos

### Fase 3 (Futuro)
- ⏳ Automatización de precios de compra
- ⏳ Sincronización con proveedores
- ⏳ Predicción de márgenes

---

## 📞 Referencias

- **AEAT REBU**: https://sede.agenciatributaria.gob.es/Sede/iva/regimenes-tributacion-iva/regimen-especial-bienes-usados.html
- **Fórmula AEAT**: https://sede.agenciatributaria.gob.es/.../funcionamiento-rebu.html
- **Documentación**: `RECOMENDACIONES_AEAT.md`

---

**Documento**: ESPECIFICACION_MARGEN_AUTOMATICO_REBU.md  
**Estado**: 📋 ESPECIFICACIÓN (Fase 2)  
**Próximo Paso**: Implementar modelo
