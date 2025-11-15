# 📋 CAMBIOS LÓGICOS DEL MÓDULO - Corrección de Cálculo de IVA en Compras REBU

**Fecha**: 15 de noviembre de 2025  
**Impacto**: CRÍTICO - Redefine la lógica de cálculo en todo el módulo  
**Estado**: PLANIFICACIÓN DE CAMBIOS

---

## 🔴 RESUMEN EJECUTIVO

La corrección de tipos de IVA en compras (0% para particulares, 10% para artistas) **requiere cambios fundamentales en la lógica del módulo**:

1. **Modelo de datos**: Los campos de cálculo deben ser sensibles al tipo de IVA de compra
2. **Cálculo de costos**: El IVA no deducible se suma al coste real de compra
3. **Cálculo de margen**: El margen se calcula sobre el coste REAL (incluye IVA no deducible)
4. **Fórmula de BI**: La base imponible de venta depende del margen real, que varía según origen
5. **Fiscalización**: La forma en que se registra el IVA cambia según tipo de compra

---

## 📊 MATRIZ DE CAMBIOS NECESARIOS

### Nivel 1: Configuración de Impuestos (✅ COMPLETADO)

**Estado**: Ya implementado en CSV  
**Cambios realizados**:
- ✅ 3 posiciones fiscales: `fp_rebu_particular` (0%), `fp_rebu_artist` (10%), `fp_rebu_sale` (21%)
- ✅ 3 impuestos: `account_tax_template_p_rebu_particular` (0%), `account_tax_template_p_rebu_artist` (10%)
- ✅ Impuesto venta: `account_tax_template_s_rebu0` (21%)

**Impacto en BD**:
```sql
-- Al importar las posiciones fiscales:
-- Proveedor A (particular) → fp_rebu_particular → IVA 0%
-- Proveedor B (artista) → fp_rebu_artist → IVA 10%
-- Cliente → fp_rebu_sale → IVA 21% en ventas
```

---

### Nivel 2: Estructura de Datos en Facturas de Compra

**Archivo afectado**: `models/account_chart_template.py` (EXTENSIÓN NECESARIA)

#### 2.1 Campos Nuevos en `account.invoice.line`

```python
# NUEVOS CAMPOS PARA GESTIONAR TIPO DE COMPRA
class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'
    
    # === INFORMACIÓN DE COMPRA ===
    rebu_supplier_type = fields.Selection([
        ('particular', 'Compra a Particular (0% IVA)'),
        ('artist', 'Compra a Artista Original (10% IVA)'),
        ('other', 'Otra compra (régimen normal)'),
    ], string="Tipo de Proveedor REBU",
       help="Clasificación del tipo de compra para aplicar IVA correcto")
    
    # === INFORMACIÓN DE COSTOS ===
    rebu_purchase_price_base = fields.Float(
        "Precio de compra (sin IVA)",
        help="Base imponible de la compra",
    )
    
    rebu_purchase_price_with_tax = fields.Float(
        "Precio de compra (REAL con IVA)",
        compute="_compute_purchase_price_with_tax",
        store=True,
        help="Coste real desembolsado (base + IVA)",
    )
    
    rebu_purchase_vat_amount = fields.Float(
        "IVA en compra",
        compute="_compute_purchase_vat_amount",
        store=True,
        help="IVA pagado (0% o 10% según tipo)",
    )
    
    # === INFORMACIÓN DE VENTAS ===
    rebu_sale_price_net = fields.Float(
        "Precio venta (sin IVA)",
        help="Precio de venta sin incluir IVA",
    )
    
    # === CÁLCULO DE MARGEN ===
    rebu_margin_gross = fields.Float(
        "Margen bruto",
        compute="_compute_margin_gross",
        store=True,
        help="PVP - Coste REAL (venta - compra con IVA no deducible)",
    )
    
    # === BASE IMPONIBLE REBU ===
    rebu_taxable_base = fields.Float(
        "Base Imponible REBU",
        compute="_compute_rebu_taxable_base",
        store=True,
        help="BI según fórmula AEAT: (Margen × 100) ÷ 121",
    )
    
    rebu_tax_calculation = fields.Float(
        "IVA a pagar (venta)",
        compute="_compute_rebu_tax_calculation",
        store=True,
        help="IVA 21% calculado sobre BI REBU",
    )
```

#### 2.2 Métodos de Cálculo Interdependientes

```python
# === PASO 1: CALCULAR COSTOS DE COMPRA ===
@api.depends('rebu_supplier_type', 'rebu_purchase_price_base')
def _compute_purchase_vat_amount(self):
    """Calcular IVA según tipo de proveedor"""
    for line in self:
        if line.is_rebu_good:
            if line.rebu_supplier_type == 'particular':
                # Compra a particular: 0% IVA
                line.rebu_purchase_vat_amount = 0.0
            elif line.rebu_supplier_type == 'artist':
                # Compra a artista: 10% IVA (NO DEDUCIBLE)
                line.rebu_purchase_vat_amount = line.rebu_purchase_price_base * 0.10
            else:
                # Otras compras: 0
                line.rebu_purchase_vat_amount = 0.0
        else:
            line.rebu_purchase_vat_amount = 0.0

@api.depends('rebu_purchase_price_base', 'rebu_purchase_vat_amount')
def _compute_purchase_price_with_tax(self):
    """Coste real = Base + IVA (el IVA no deducible se suma al coste)"""
    for line in self:
        if line.is_rebu_good:
            line.rebu_purchase_price_with_tax = \
                line.rebu_purchase_price_base + line.rebu_purchase_vat_amount
        else:
            line.rebu_purchase_price_with_tax = 0.0

# === PASO 2: CALCULAR MARGEN ===
@api.depends('rebu_sale_price_net', 'rebu_purchase_price_with_tax')
def _compute_margin_gross(self):
    """Margen = PVP - Coste REAL (incluye IVA no deducible)"""
    for line in self:
        if line.is_rebu_good and line.rebu_sale_price_net > 0:
            line.rebu_margin_gross = \
                line.rebu_sale_price_net - line.rebu_purchase_price_with_tax
        else:
            line.rebu_margin_gross = 0.0

# === PASO 3: CALCULAR BASE IMPONIBLE ===
@api.depends('rebu_margin_gross')
def _compute_rebu_taxable_base(self):
    """Fórmula AEAT: BI = (Margen × 100) ÷ 121"""
    for line in self:
        if line.is_rebu_good and line.rebu_margin_gross > 0:
            # Divisor: 100 + tasa_iva (para 21% es 121)
            line.rebu_taxable_base = (line.rebu_margin_gross * 100) / 121
        else:
            line.rebu_taxable_base = 0.0

# === PASO 4: CALCULAR IVA A PAGAR ===
@api.depends('rebu_taxable_base')
def _compute_rebu_tax_calculation(self):
    """IVA venta = BI × 21%"""
    for line in self:
        if line.is_rebu_good and line.rebu_taxable_base > 0:
            line.rebu_tax_calculation = line.rebu_taxable_base * 0.21
        else:
            line.rebu_tax_calculation = 0.0
```

**Flujo de cálculo**:
```
rebu_supplier_type + rebu_purchase_price_base
    ↓
_compute_purchase_vat_amount()
    ↓
_compute_purchase_price_with_tax()  [Coste real con IVA]
    ↓
rebu_sale_price_net
    ↓
_compute_margin_gross()  [PVP - Coste real]
    ↓
_compute_rebu_taxable_base()  [Margen ÷ 1,21]
    ↓
_compute_rebu_tax_calculation()  [BI × 21%]
```

---

## 🎯 CAMBIOS POR ESCENARIO

### Escenario A: Compra a Particular (0% IVA)

**Entrada**:
```
rebu_supplier_type = 'particular'
rebu_purchase_price_base = 1.000€
rebu_sale_price_net = 1.500€
```

**Cálculos automáticos**:
```
rebu_purchase_vat_amount = 1.000€ × 0% = 0€ ✓
rebu_purchase_price_with_tax = 1.000€ + 0€ = 1.000€ ✓
rebu_margin_gross = 1.500€ - 1.000€ = 500€ ✓
rebu_taxable_base = (500€ × 100) ÷ 121 = 413,22€ ✓
rebu_tax_calculation = 413,22€ × 0,21 = 86,78€ ✓
```

**Línea de factura de venta**:
```
Línea: Cuadro artístico
  - Descripción: [producto]
  - Cantidad: 1
  - Precio unitario: 413,22€  [BI REBU, no 1.500€]
  - Impuesto: 21% = 86,78€
  - Subtotal: 413,22€
  - IVA: 86,78€
  - Total: 500€
```

---

### Escenario B: Compra a Artista Original (10% IVA no deducible)

**Entrada**:
```
rebu_supplier_type = 'artist'
rebu_purchase_price_base = 1.000€
rebu_sale_price_net = 1.500€
```

**Cálculos automáticos**:
```
rebu_purchase_vat_amount = 1.000€ × 10% = 100€ ✓
rebu_purchase_price_with_tax = 1.000€ + 100€ = 1.100€ ✓
rebu_margin_gross = 1.500€ - 1.100€ = 400€ ✓
rebu_taxable_base = (400€ × 100) ÷ 121 = 330,58€ ✓
rebu_tax_calculation = 330,58€ × 0,21 = 69,42€ ✓
```

**Línea de factura de venta**:
```
Línea: Obra original
  - Descripción: [producto artista]
  - Cantidad: 1
  - Precio unitario: 330,58€  [BI REBU]
  - Impuesto: 21% = 69,42€
  - Subtotal: 330,58€
  - IVA: 69,42€
  - Total: 400€
```

---

## 🔧 CAMBIOS EN VISTAS Y FORMULARIOS

### Vista de Línea de Factura (account.invoice.line)

**Grupo 1: Información de Compra** (Solo lectura en vista, editable en wizard)
```xml
<group string="Información de Compra">
    <field name="rebu_supplier_type" widget="radio"/>
    <field name="rebu_purchase_price_base"/>
    <field name="rebu_purchase_vat_amount" readonly="1"/>
    <field name="rebu_purchase_price_with_tax" readonly="1"/>
</group>
```

**Grupo 2: Información de Venta** (Editable)
```xml
<group string="Información de Venta">
    <field name="rebu_sale_price_net"/>
</group>
```

**Grupo 3: Cálculos REBU** (Solo lectura, computados)
```xml
<group string="Cálculos REBU">
    <field name="rebu_margin_gross" readonly="1"/>
    <field name="rebu_taxable_base" readonly="1"/>
    <field name="rebu_tax_calculation" readonly="1"/>
</group>
```

### Wizard de Creación de Factura de Venta

**Pasos**:
1. Seleccionar cliente
2. Para cada producto REBU:
   - Indicar tipo de compra (particular/artista)
   - Indicar precio compra (sin IVA)
   - Indicar precio venta (neto)
   - Sistema calcula automáticamente BI y IVA

---

## 📦 CAMBIOS EN REPORTES

### Reporte de Factura de Venta REBU

**Sección de Líneas**:
```
Descripción        | Cantidad | Precio Unit. | Subtotal | IVA | Total
                   |          | (BI REBU)    |          |     |
---------------------------------------------------------------------------
Cuadro artístico   |    1     | 413,22€      | 413,22€  | 86,78€ | 500€
```

**Pie de Factura - Desglose REBU**:
```
Subtotal (BI REBU): 413,22€
IVA 21%: 86,78€
TOTAL: 500€

Nota: Régimen Especial de Bienes Usados - Artísticos
Base imponible calculada según fórmula AEAT: (Margen × 100) ÷ 121
```

---

## ⚙️ CAMBIOS EN INTEGRACIONES

### 1. Integración con `account.invoice.line`

**Método de validación**:
```python
def _validate_rebu_data(self):
    """Validar que los datos REBU son coherentes"""
    for line in self:
        if line.is_rebu_good:
            if not line.rebu_supplier_type:
                raise ValidationError(
                    "Debe indicar tipo de proveedor (Particular/Artista)"
                )
            if line.rebu_sale_price_net <= 0:
                raise ValidationError(
                    "Precio de venta debe ser mayor a 0"
                )
            if line.rebu_purchase_price_base <= 0:
                raise ValidationError(
                    "Precio de compra debe ser mayor a 0"
                )
            if line.rebu_margin_gross <= 0:
                raise ValidationError(
                    "Margen debe ser positivo (venta > compra real)"
                )
```

### 2. Integración con Impuestos en Factura

**Método en `account.move`**:
```python
def _compute_rebu_tax_line(self):
    """Alinear impuestos computados con líneas de impuesto"""
    for move in self:
        if move.is_rebu_invoice:
            for line in move.invoice_line_ids.filtered('is_rebu_good'):
                # Crear/actualizar línea de impuesto según rebu_tax_calculation
                tax_data = {
                    'account_id': line.get_rebu_tax_account(),
                    'amount': line.rebu_tax_calculation,
                    'tax_tag_ids': line.get_rebu_tax_tags(),
                }
                # Aplicar cambios a línea de impuesto existente
```

---

## 📝 RESUMEN DE CAMBIOS REQUERIDOS

| Componente | Cambio | Prioridad | Estado |
|------------|--------|-----------|--------|
| CSV impuestos | ✅ 3 posiciones fiscales | 🔴 CRÍTICO | ✅ COMPLETADO |
| CSV impuestos | ✅ 3 tipos de impuesto | 🔴 CRÍTICO | ✅ COMPLETADO |
| `account.invoice.line` | 7 campos nuevos | 🔴 CRÍTICO | ⏳ PENDIENTE |
| Métodos de cálculo | 5 métodos computados | 🔴 CRÍTICO | ⏳ PENDIENTE |
| Vistas XML | Actualizar formulario | 🟠 ALTO | ⏳ PENDIENTE |
| Wizard | Agregar paso de entrada | 🟠 ALTO | ⏳ PENDIENTE |
| Reportes | Actualizar desglose | 🟠 ALTO | ⏳ PENDIENTE |
| Validaciones | 4 validaciones nuevas | 🟠 ALTO | ⏳ PENDIENTE |
| Tests | Actualizar 27 tests | 🟠 ALTO | ⏳ PENDIENTE |

---

## 🚀 PLAN DE IMPLEMENTACIÓN

### Fase 2.1: Base de Datos (Semana 1)
- [ ] Crear migraciones para nuevos campos
- [ ] Agregar índices en `rebu_supplier_type`
- [ ] Documentar cambios en diccionario de datos

### Fase 2.2: Lógica de Negocio (Semana 2)
- [ ] Implementar 5 métodos computados
- [ ] Agregar 4 validaciones
- [ ] Crear tests unitarios (15 tests)

### Fase 2.3: Interfaz de Usuario (Semana 2-3)
- [ ] Actualizar vistas de formulario
- [ ] Crear wizard de entrada
- [ ] Agregar campos a búsqueda avanzada

### Fase 2.4: Reportes (Semana 3)
- [ ] Actualizar reporte de factura
- [ ] Agregar desglose REBU
- [ ] Crear reporte de validación

### Fase 2.5: Testing (Semana 4)
- [ ] Actualizar 27 tests existentes
- [ ] Agregar 12 tests nuevos
- [ ] Test de integración end-to-end

---

## 📌 DEPENDENCIAS Y RIESGOS

**Dependencias**:
- ✅ CSV ya está en lugar (no bloqueante)
- ⏳ Migración de datos existentes (si las hay)
- ⏳ Validación con asesor fiscal

**Riesgos**:
- 🔴 Si se cambia fórmula nuevamente, afecta todos los cálculos
- 🔴 Integridad referencial si hay facturas ya creadas
- 🟠 Performance si hay muchas líneas REBU

---

## ✅ PRÓXIMOS PASOS

1. **Validar este plan** con el usuario/asesor fiscal
2. **Crear rama de desarrollo** para Fase 2
3. **Implementar campos** en modelos
4. **Desarrollar métodos** de cálculo
5. **Crear tests** antes de implementar
6. **Integrar** con vistas y wizards

---

**Documento preparado por**: GitHub Copilot  
**Última actualización**: 15 de noviembre de 2025  
**Estado**: LISTO PARA REVISION
