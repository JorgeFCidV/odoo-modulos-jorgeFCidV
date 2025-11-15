# 🐍 IMPLEMENTACIÓN CÓDIGO PYTHON - Corrección de Cálculo de IVA

**Fecha**: 15 de noviembre de 2025  
**Archivo destino**: `models/account_invoice_extension.py` (NUEVO)  
**Estado**: ESPECIFICACIÓN TÉCNICA

---

## 📋 RESUMEN

Se requiere crear un nuevo módulo de extensión que hereda de `account.invoice.line` para agregar:

1. **7 campos nuevos** para capturar y calcular datos REBU
2. **5 métodos computados** con dependencias para cálculos automáticos
3. **2 métodos de validación** para integridad de datos
4. **Integración** con impuestos en líneas de factura

---

## 📝 CÓDIGO COMPLETO

```python
# -*- coding: utf-8 -*-
"""
models/account_invoice_extension.py

Extensión de account.invoice.line para soportar cálculo de margen
según Régimen Especial de Bienes Usados (REBU) - AEAT

Fórmula: BI = (Margen × 100) ÷ (100 + tasa_iva)
Donde: Margen = Precio_venta - Precio_compra_REAL (incluye IVA no deducible)
"""

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AccountInvoiceLine(models.Model):
    """Extensión de líneas de factura para REBU"""
    _inherit = 'account.invoice.line'

    # =========================================================================
    # SECCIÓN 1: CAMPOS DE INFORMACIÓN
    # =========================================================================

    # --- Clasificación de Compra ---
    rebu_supplier_type = fields.Selection([
        ('particular', 'Compra a Particular (0% IVA)'),
        ('artist', 'Compra a Artista Original (10% IVA)'),
        ('other', 'Otra compra (régimen normal)'),
    ],
        string="Tipo de Proveedor REBU",
        help="Clasificación del tipo de compra para aplicar IVA correcto"
    )

    # --- Información de Costos (ENTRADA) ---
    rebu_purchase_price_base = fields.Float(
        "Precio de compra (sin IVA)",
        default=0.0,
        help="Base imponible de la compra sin incluir IVA"
    )

    rebu_sale_price_net = fields.Float(
        "Precio venta (sin IVA)",
        default=0.0,
        help="Precio de venta sin incluir IVA (precio unitario neto)"
    )

    # --- Información de Costos (COMPUTADOS) ---
    rebu_purchase_vat_amount = fields.Float(
        "IVA en compra",
        compute="_compute_purchase_vat_amount",
        store=True,
        readonly=True,
        help="IVA pagado en compra (0% o 10% según tipo de proveedor)"
    )

    rebu_purchase_price_with_tax = fields.Float(
        "Coste real con IVA",
        compute="_compute_purchase_price_with_tax",
        store=True,
        readonly=True,
        help="Coste desembolsado = Base + IVA (el IVA no deducible se suma)"
    )

    # --- Cálculo de Margen ---
    rebu_margin_gross = fields.Float(
        "Margen bruto",
        compute="_compute_margin_gross",
        store=True,
        readonly=True,
        help="Diferencia = Precio_venta - Coste_REAL (incluye IVA no deducible)"
    )

    # --- Base Imponible REBU ---
    rebu_taxable_base = fields.Float(
        "Base Imponible REBU",
        compute="_compute_rebu_taxable_base",
        store=True,
        readonly=True,
        help="Base imponible según fórmula AEAT: (Margen × 100) ÷ 121"
    )

    rebu_tax_calculation = fields.Float(
        "IVA a pagar (venta)",
        compute="_compute_rebu_tax_calculation",
        store=True,
        readonly=True,
        help="IVA 21% sobre base imponible REBU"
    )

    # --- Indicador ---
    is_rebu_good = fields.Boolean(
        "Es bien REBU",
        default=False,
        help="Marcar si es bien artístico bajo régimen REBU"
    )

    # =========================================================================
    # SECCIÓN 2: MÉTODOS COMPUTADOS (ORDEN CRÍTICO)
    # =========================================================================

    @api.depends('rebu_supplier_type', 'rebu_purchase_price_base', 'is_rebu_good')
    def _compute_purchase_vat_amount(self):
        """
        PASO 1: Calcular IVA en compra según tipo de proveedor
        
        Reglas:
        - Particular (0%): IVA = 0€
        - Artista (10%): IVA = Base × 10%
        - Otro: IVA = 0€
        
        El IVA no deducible se suma al coste (no es deducible en REBU)
        """
        for line in self:
            if not line.is_rebu_good:
                line.rebu_purchase_vat_amount = 0.0
                continue

            if line.rebu_supplier_type == 'particular':
                # Compra a particular: 0% IVA
                line.rebu_purchase_vat_amount = 0.0

            elif line.rebu_supplier_type == 'artist':
                # Compra a artista: 10% IVA (NO DEDUCIBLE)
                if line.rebu_purchase_price_base > 0:
                    line.rebu_purchase_vat_amount = \
                        line.rebu_purchase_price_base * 0.10
                else:
                    line.rebu_purchase_vat_amount = 0.0

            else:
                # Otras compras
                line.rebu_purchase_vat_amount = 0.0

    @api.depends('rebu_purchase_price_base', 'rebu_purchase_vat_amount', 'is_rebu_good')
    def _compute_purchase_price_with_tax(self):
        """
        PASO 2: Calcular coste real con IVA
        
        Fórmula: Coste_Real = Precio_Base + IVA
        
        El IVA no deducible se suma porque es un costo no recuperable
        en el régimen REBU.
        
        Ejemplo:
        - Compra a particular: 1.000€ + 0€ = 1.000€
        - Compra a artista: 1.000€ + 100€ = 1.100€
        """
        for line in self:
            if not line.is_rebu_good:
                line.rebu_purchase_price_with_tax = 0.0
                continue

            line.rebu_purchase_price_with_tax = \
                line.rebu_purchase_price_base + line.rebu_purchase_vat_amount

    @api.depends('rebu_sale_price_net', 'rebu_purchase_price_with_tax', 'is_rebu_good')
    def _compute_margin_gross(self):
        """
        PASO 3: Calcular margen bruto (gross margin)
        
        Fórmula: Margen = Precio_Venta - Coste_REAL
        
        CRÍTICO: Se calcula sobre el COSTE REAL (que incluye IVA no deducible)
        
        Ejemplo Particular:
        - Venta: 1.500€
        - Coste: 1.000€
        - Margen: 500€
        
        Ejemplo Artista:
        - Venta: 1.500€
        - Coste: 1.100€ (1.000€ + 100€ IVA no deducible)
        - Margen: 400€
        
        El margen del artista es menor porque el IVA no deducible se suma.
        """
        for line in self:
            if not line.is_rebu_good:
                line.rebu_margin_gross = 0.0
                continue

            if line.rebu_sale_price_net > 0 and line.rebu_purchase_price_with_tax > 0:
                margin = line.rebu_sale_price_net - line.rebu_purchase_price_with_tax
                # El margen puede ser negativo (pérdida)
                line.rebu_margin_gross = margin
            else:
                line.rebu_margin_gross = 0.0

    @api.depends('rebu_margin_gross', 'is_rebu_good')
    def _compute_rebu_taxable_base(self):
        """
        PASO 4: Calcular Base Imponible según fórmula AEAT
        
        Fórmula: BI = (Margen × 100) ÷ (100 + tasa_iva)
        
        Para IVA 21%:
        BI = (Margen × 100) ÷ 121
        
        Esto asegura que: BI + (BI × 21%) = Margen
        
        Ejemplo Particular (Margen 500€):
        BI = (500 × 100) ÷ 121 = 50.000 ÷ 121 = 413,22€
        IVA = 413,22€ × 0,21 = 86,78€
        Total = 413,22€ + 86,78€ = 500€ ✓
        
        Ejemplo Artista (Margen 400€):
        BI = (400 × 100) ÷ 121 = 40.000 ÷ 121 = 330,58€
        IVA = 330,58€ × 0,21 = 69,42€
        Total = 330,58€ + 69,42€ = 400€ ✓
        """
        for line in self:
            if not line.is_rebu_good:
                line.rebu_taxable_base = 0.0
                continue

            if line.rebu_margin_gross > 0:
                # Divisor: 100 + tasa_iva (para 21% es 121)
                # Fórmula: BI = (Margen × 100) ÷ 121
                divisor = 121  # 100 + 21 (para IVA 21%)
                line.rebu_taxable_base = (line.rebu_margin_gross * 100) / divisor
            else:
                line.rebu_taxable_base = 0.0

    @api.depends('rebu_taxable_base', 'is_rebu_good')
    def _compute_rebu_tax_calculation(self):
        """
        PASO 5: Calcular IVA a pagar en venta
        
        Fórmula: IVA = BI × 21%
        
        Este es el IVA que se factura al cliente (repercutido).
        
        Ejemplo:
        - BI = 413,22€
        - IVA = 413,22€ × 0,21 = 86,78€
        """
        for line in self:
            if not line.is_rebu_good:
                line.rebu_tax_calculation = 0.0
                continue

            if line.rebu_taxable_base > 0:
                line.rebu_tax_calculation = line.rebu_taxable_base * 0.21
            else:
                line.rebu_tax_calculation = 0.0

    # =========================================================================
    # SECCIÓN 3: MÉTODOS DE VALIDACIÓN
    # =========================================================================

    @api.constrains('is_rebu_good', 'rebu_supplier_type', 
                    'rebu_purchase_price_base', 'rebu_sale_price_net',
                    'rebu_margin_gross')
    def _validate_rebu_data(self):
        """
        Validar integridad de datos REBU
        
        Reglas:
        1. Si is_rebu_good=True, debe haber tipo de proveedor
        2. Precio de compra > 0
        3. Precio de venta > 0
        4. Margen > 0 (no puede ser operación con pérdida en REBU)
        5. Precio venta > Precio compra real
        """
        for line in self:
            if not line.is_rebu_good:
                continue

            # Regla 1: Tipo de proveedor requerido
            if not line.rebu_supplier_type or line.rebu_supplier_type == 'other':
                raise ValidationError(
                    f"Línea '{line.product_id.name}': "
                    "Debe indicar tipo de proveedor (Particular o Artista)"
                )

            # Regla 2: Precio de compra > 0
            if line.rebu_purchase_price_base <= 0:
                raise ValidationError(
                    f"Línea '{line.product_id.name}': "
                    "Precio de compra debe ser mayor a 0€"
                )

            # Regla 3: Precio de venta > 0
            if line.rebu_sale_price_net <= 0:
                raise ValidationError(
                    f"Línea '{line.product_id.name}': "
                    "Precio de venta debe ser mayor a 0€"
                )

            # Regla 4: Margen positivo
            if line.rebu_margin_gross <= 0:
                raise ValidationError(
                    f"Línea '{line.product_id.name}': "
                    "Margen debe ser positivo (precio venta > coste real). "
                    f"Venta: {line.rebu_sale_price_net}€, "
                    f"Coste: {line.rebu_purchase_price_with_tax}€"
                )

    def _validate_rebu_fiscal_consistency(self):
        """
        Validación adicional de consistencia fiscal
        
        Se ejecuta antes de validar la factura.
        """
        rebu_lines = self.filtered('is_rebu_good')
        
        if not rebu_lines:
            return  # Nada que validar
        
        # Obtener factura padre
        move = self.move_id
        
        if not move:
            return
        
        # Validar que sea factura de venta
        if move.move_type not in ['out_invoice', 'out_refund']:
            raise ValidationError(
                "Las líneas REBU solo pueden usarse en facturas de venta"
            )
        
        # Validar que cliente tenga posición fiscal REBU
        if move.partner_id.property_account_position_id:
            fiscal_pos = move.partner_id.property_account_position_id.code
            if not fiscal_pos or 'rebu' not in fiscal_pos.lower():
                raise ValidationError(
                    f"Cliente '{move.partner_id.name}' no tiene "
                    "posición fiscal REBU configurada"
                )

    # =========================================================================
    # SECCIÓN 4: MÉTODOS AUXILIARES
    # =========================================================================

    def get_rebu_summary(self):
        """
        Obtener resumen de cálculos REBU para una línea
        
        Retorna: dict con todos los valores REBU
        """
        self.ensure_one()
        
        return {
            'supplier_type': self.rebu_supplier_type,
            'purchase_price_base': self.rebu_purchase_price_base,
            'purchase_vat': self.rebu_purchase_vat_amount,
            'purchase_total': self.rebu_purchase_price_with_tax,
            'sale_price': self.rebu_sale_price_net,
            'margin': self.rebu_margin_gross,
            'taxable_base': self.rebu_taxable_base,
            'tax_21pct': self.rebu_tax_calculation,
            'total_invoiced': self.rebu_taxable_base + self.rebu_tax_calculation,
        }

    def log_rebu_calculation(self):
        """
        Log de cálculos REBU para debugging
        """
        self.ensure_one()
        
        if not self.is_rebu_good:
            return
        
        msg = f"""
        === CÁLCULO REBU: {self.product_id.name} ===
        
        ENTRADA:
          Tipo: {self.get_rebu_supplier_type_display()}
          Precio compra (sin IVA): {self.rebu_purchase_price_base}€
          Precio venta (sin IVA): {self.rebu_sale_price_net}€
        
        CÁLCULOS:
          IVA compra: {self.rebu_purchase_vat_amount}€
          Coste real: {self.rebu_purchase_price_with_tax}€
          Margen bruto: {self.rebu_margin_gross}€
          Base Imponible: {self.rebu_taxable_base}€
          IVA venta 21%: {self.rebu_tax_calculation}€
          Total facturado: {self.rebu_taxable_base + self.rebu_tax_calculation}€
        
        VERIFICACIÓN:
          BI + IVA = {self.rebu_taxable_base} + {self.rebu_tax_calculation} = {self.rebu_taxable_base + self.rebu_tax_calculation}€
          Debe = Margen: {self.rebu_margin_gross}€
          Coincide: {abs((self.rebu_taxable_base + self.rebu_tax_calculation) - self.rebu_margin_gross) < 0.01}
        """
        
        print(msg)
        return msg

    # =========================================================================
    # SECCIÓN 5: SOBREESCRITURAS DE MÉTODOS EXISTENTES
    # =========================================================================

    def _compute_price_unit(self):
        """
        Sobrescribir cálculo de precio unitario
        
        Si es bien REBU, usar Base Imponible como precio unitario
        (no el precio de venta completo)
        """
        super()._compute_price_unit()
        
        for line in self:
            if line.is_rebu_good and line.rebu_taxable_base > 0:
                # Para REBU, el precio unitario en la factura es la BI
                line.price_unit = line.rebu_taxable_base

    def _compute_tax_id(self):
        """
        Sobrescribir selección de impuestos
        
        Para REBU, asegurar que se usa el impuesto de venta correcto (21%)
        """
        super()._compute_tax_id()
        
        for line in self:
            if line.is_rebu_good:
                # Buscar impuesto REBU de venta 21%
                tax = self.env['account.tax'].search([
                    ('name', 'ilike', 'REBU%venta%21%'),
                    ('type_tax_use', '=', 'sale'),
                    ('amount', '=', 21.0),
                ], limit=1)
                
                if tax:
                    line.tax_ids = [(6, 0, [tax.id])]

```

---

## 📊 FLUJO DE CÁLCULO VISUAL

```
┌─────────────────────────────────────────────────────────────┐
│ ENTRADA DE DATOS (Usuario introduce)                        │
├─────────────────────────────────────────────────────────────┤
│ is_rebu_good = True                                         │
│ rebu_supplier_type = 'artist'                               │
│ rebu_purchase_price_base = 1.000€                           │
│ rebu_sale_price_net = 1.500€                                │
└─────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│ PASO 1: Calcular IVA en compra                              │
├─────────────────────────────────────────────────────────────┤
│ rebu_purchase_vat_amount = 1.000€ × 10% = 100€             │
│ (depende: rebu_supplier_type, rebu_purchase_price_base)     │
└─────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│ PASO 2: Calcular coste real con IVA                         │
├─────────────────────────────────────────────────────────────┤
│ rebu_purchase_price_with_tax = 1.000€ + 100€ = 1.100€      │
│ (depende: rebu_purchase_price_base, rebu_purchase_vat)      │
└─────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│ PASO 3: Calcular margen bruto                               │
├─────────────────────────────────────────────────────────────┤
│ rebu_margin_gross = 1.500€ - 1.100€ = 400€                 │
│ (depende: rebu_sale_price_net, rebu_purchase_price_with_tax)│
└─────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│ PASO 4: Calcular Base Imponible AEAT                        │
├─────────────────────────────────────────────────────────────┤
│ rebu_taxable_base = (400€ × 100) ÷ 121 = 330,58€           │
│ (depende: rebu_margin_gross)                                │
└─────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│ PASO 5: Calcular IVA a pagar                                │
├─────────────────────────────────────────────────────────────┤
│ rebu_tax_calculation = 330,58€ × 21% = 69,42€              │
│ (depende: rebu_taxable_base)                                │
└─────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│ SALIDA: Línea de factura generada                           │
├─────────────────────────────────────────────────────────────┤
│ price_unit = 330,58€ (BI REBU, no 1.500€)                  │
│ tax_ids = [IVA 21% REBU]                                    │
│ quantity = 1                                                │
│ subtotal = 330,58€                                          │
│ tax_amount = 69,42€                                         │
│ total = 400€                                                │
│                                                             │
│ VERIFICACIÓN: BI + IVA = 330,58 + 69,42 = 400€ = Margen ✓  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔗 INTEGRACIÓN CON OTROS MODELOS

### 1. Integración con `account.move`

```python
class AccountMove(models.Model):
    _inherit = 'account.move'
    
    is_rebu_invoice = fields.Boolean(
        compute="_compute_is_rebu_invoice",
        help="True si contiene al menos una línea REBU"
    )
    
    @api.depends('invoice_line_ids.is_rebu_good')
    def _compute_is_rebu_invoice(self):
        for move in self:
            move.is_rebu_invoice = any(
                line.is_rebu_good for line in move.invoice_line_ids
            )
```

### 2. Integración con `product.product`

```python
class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    is_rebu_product = fields.Boolean(
        "Es producto REBU",
        help="Marcar si este bien es artístico para régimen REBU"
    )
```

### 3. Integración con `res.partner`

```python
class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    rebu_supplier_type = fields.Selection([
        ('particular', 'Proveedor Particular'),
        ('artist', 'Proveedor Artista'),
        ('other', 'Otro'),
    ],
        "Tipo en REBU",
        help="Clasificación para régimen REBU"
    )
```

---

## ✅ CHECKLIST DE IMPLEMENTACIÓN

- [ ] Crear archivo `models/account_invoice_extension.py`
- [ ] Agregar 7 campos nuevos
- [ ] Implementar 5 métodos computados
- [ ] Implementar 2 métodos de validación
- [ ] Agregar 4 métodos auxiliares
- [ ] Integrar con `account.move`
- [ ] Integrar con `product.product`
- [ ] Integrar con `res.partner`
- [ ] Crear vistas XML (formularios)
- [ ] Crear wizard de entrada
- [ ] Actualizar reporte de factura
- [ ] Crear tests (mínimo 20 tests)
- [ ] Documentar en README
- [ ] Validar con asesor fiscal

---

**Documento preparado por**: GitHub Copilot  
**Última actualización**: 15 de noviembre de 2025  
**Estado**: LISTO PARA IMPLEMENTACIÓN
