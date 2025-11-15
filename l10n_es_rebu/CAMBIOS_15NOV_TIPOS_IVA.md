# CAMBIOS REALIZADOS - 15 NOV 2025

## 🔧 Corrección de Tipos de IVA en Compras REBU

**Responsable**: Corrección por usuario  
**Fecha**: 15 de noviembre de 2025  
**Impacto**: CRÍTICO - Cambios en estructura de impuestos

---

## 📋 Resumen Ejecutivo

Se ha corregido la configuración de IVA en compras del módulo REBU para reflejar la **realidad fiscal** española:

### ANTES (Incorrecto)
```
Compra: 21% IVA no deducible (un solo tipo)
Venta:  21% IVA repercutido
```

### DESPUÉS (Correcto)
```
Compra a Particular:       0% IVA (sin IVA)
Compra a Artista Original: 10% IVA no deducible
Venta:                     21% IVA repercutido
```

---

## 📂 Archivos Modificados

### 1. data/template/account.tax-es_common.csv
**Cambios**:
- ✅ Reemplazado: `account_tax_template_p_rebu0` (21%) con dos nuevos
- ✅ Creado: `account_tax_template_p_rebu_particular` (0%)
- ✅ Creado: `account_tax_template_p_rebu_artist` (10%)
- ✅ Mantenido: `account_tax_template_s_rebu0` (21% venta - sin cambios)

**IDs nuevos**:
```
account_tax_template_p_rebu_particular    0% - Particular
account_tax_template_p_rebu_artist        10% - Artista
account_tax_template_s_rebu0              21% - Venta (sin cambios)
```

### 2. data/template/account.fiscal.position-es_common.csv
**Cambios**:
- ✅ Creado: `fp_rebu_particular` (mapea a 0%)
- ✅ Creado: `fp_rebu_artist` (mapea a 10%)
- ✅ Creado: `fp_rebu_sale` (mapea a 21% venta)

**Posiciones Fiscales nuevas**:
```
fp_rebu_particular: REBU - Compra a Particular (0%)
fp_rebu_artist:     REBU - Compra a Artista Original (10%)
fp_rebu_sale:       REBU - Bienes Usados Artísticos (Venta 21%)
```

### 3. README.rst
**Cambios**:
- ✅ Sección Usage completamente reescrita
- ✅ Añadido: Tabla de dos casos de compra (0% y 10%)
- ✅ Añadido: Ejemplos de configuración por tipo
- ✅ Añadido: Descripción de casos de aplicación

**Nuevas secciones**:
- "Configuración de Productos"
- "Configuración de Contactos/Proveedores"
- "Casos de Aplicación"

### 4. VALIDACION_AEAT.md
**Cambios**:
- ✅ Añadida sección: "Tipos de IVA en Compras REBU"
- ✅ Documentado: Caso 1 - Compra a Particular (0%)
- ✅ Documentado: Caso 2 - Compra a Artista (10%)
- ✅ Documentado: Caso 3 - Venta a Cliente (21%)
- ✅ Incluidas: Configuraciones Odoo para cada caso

### 5. RECOMENDACIONES_AEAT.md
**Cambios**:
- ✅ Añadida sección: "4.1 Tipos de IVA en Compras REBU"
- ✅ Documentado: Caso 1 - Particular (0%)
- ✅ Documentado: Caso 2 - Artista (10%)
- ✅ Ejemplos de cálculo para cada caso
- ✅ Actualizado: Checklist Fase 1 (refleja cambios)

### 6. RESUMEN_VALIDACION.md
**Cambios**:
- ✅ Actualizado: Sección "Impuestos configurados"
- ✅ Actualizado: Sección "Posiciones Fiscales"
- ✅ Añadida: Sección "NUEVAS OPCIONES DE COMPRA"
- ✅ Actualizado: Checklist de configuración
- ✅ Actualizado: Historial de cambios

### 7. TIPOS_IVA_REBU_CORRECCION.md (NUEVO)
**Contenido**:
- ✅ Análisis detallado del cambio
- ✅ Comparativa antes/después
- ✅ Impacto financiero
- ✅ Configuración por tipo
- ✅ Checklist de implementación
- ✅ Plan de ejecución

---

## 📊 Impacto de Cambios

### Archivo CSV: account.tax-es_common.csv

**Antes**:
```csv
"account_tax_template_p_rebu0","VAT REBU non-deductible 21%",...,"purchase","21.0",...
```

**Después**:
```csv
"account_tax_template_p_rebu_particular","...0% (Particular)",...,"purchase","0.0",...
"account_tax_template_p_rebu_artist","...10% (Artista Original)",...,"purchase","10.0",...
```

### Archivo CSV: account.fiscal.position-es_common.csv

**Antes**:
```csv
"fp_rebu","REBU - Used Artistic Goods",...
(todos los impuestos mapeaban a account_tax_template_p_rebu0 21%)
```

**Después**:
```csv
"fp_rebu_particular","REBU - Purchase from Private Individual",...
(mapea a account_tax_template_p_rebu_particular 0%)

"fp_rebu_artist","REBU - Purchase from Artist",...
(mapea a account_tax_template_p_rebu_artist 10%)

"fp_rebu_sale","REBU - Sales of Used Artistic Goods",...
(mapea a account_tax_template_s_rebu0 21%)
```

---

## 🎓 Configuración en Odoo

### Para Proveedor Particular (0% IVA):
```
1. Ir a contacto de proveedor
2. Campo "Posición fiscal": Seleccionar "REBU - Compra a Particular (0%)"
3. Las facturas de compra usarán 0% IVA
```

### Para Proveedor Artista (10% IVA no deducible):
```
1. Ir a contacto de proveedor
2. Campo "Posición fiscal": Seleccionar "REBU - Compra a Artista Original (10%)"
3. Las facturas de compra usarán 10% IVA no deducible
```

### Para Clientes (21% IVA repercutido):
```
1. Ir a contacto de cliente
2. Campo "Posición fiscal": Seleccionar "REBU - Bienes Usados Artísticos (Venta 21%)"
3. Las facturas de venta usarán 21% IVA repercutido
```

---

## 💰 Ejemplo Práctico - Estructura de Costos REBU

### Escenario 1: Compra a Particular, Venta Posterior

**ANTES (Configuración incorrecta - Aplicaba 21% a todo)**:
```
COMPRA a particular: 1.000€
IVA 21% (incorrecto): 210€
Total desembolso: 1.210€ ❌

VENTA REBU - Cálculo incorrecto:
  Precio venta neto: 1.500€
  IVA 21% sobre 1.500€: 315€
  Total facturado: 1.815€ ❌
```

**DESPUÉS (Configuración correcta)**:
```
COMPRA a particular: 1.000€
IVA 0% (correcto - sin IVA): 0€
Total desembolso: 1.000€ ✅

VENTA REBU - Cálculo correcto según AEAT:
  PVP (Precio venta): 1.500€
  - Costo compra: 1.000€
  = Margen bruto: 500€
  
  Base Imponible = Margen / (1 + tipo IVA)
                 = 500€ / (1 + 0,21)
                 = 500€ / 1,21
                 = 413,22€
  
  IVA 21%: 413,22€ × 0,21 = 86,78€
  Total facturado: 413,22€ + 86,78€ = 500€ ✅
```

### Escenario 2: Compra a Artista Original, Venta Posterior

**ANTES (Configuración incorrecta - Aplicaba 21% a todo)**:
```
COMPRA a artista: 1.000€
IVA 21% (incorrecto): 210€
Total desembolso: 1.210€ ❌

VENTA REBU - Cálculo incorrecto:
  Precio venta neto: 1.500€
  IVA 21% sobre 1.500€: 315€
  Total facturado: 1.815€ ❌
```

**DESPUÉS (Configuración correcta)**:
```
COMPRA a artista: 1.000€
IVA 10% (correcto, no deducible): 100€
Total desembolso (Costo de compra real): 1.100€ ✅

VENTA REBU - Cálculo correcto según AEAT:
  PVP (Precio venta): 1.500€
  - Costo compra REAL (incluye IVA no deducible): 1.100€
  = Margen bruto: 400€
  
  Base Imponible = Margen / (1 + tipo IVA)
                 = 400€ / (1 + 0,21)
                 = 400€ / 1,21
                 = 330,58€
  
  IVA 21%: 330,58€ × 0,21 = 69,42€
  Total facturado: 330,58€ + 69,42€ = 400€ ✅
```

**Diferencia en compra**: Se paga 1.100€ vs 1.210€

---

### Resumen del Impacto Financiero

**Escenario 1: Compra a Particular (0% IVA)**:
| Concepto | Cálculo | Resultado |
|----------|---------|-----------|
| Margen bruto | PVP 1.500€ - Costo 1.000€ | 500€ |
| Base Imponible REBU | 500€ / 1,21 | 413,22€ |
| IVA 21% en venta | 413,22€ × 0,21 | 86,78€ |
| Total facturado | BI + IVA | 500€ |

**Escenario 2: Compra a Artista (10% IVA no deducible)**:
| Concepto | Cálculo | Resultado |
|----------|---------|-----------|
| Margen bruto | PVP 1.500€ - Costo REAL 1.100€ | 400€ |
| Base Imponible REBU | 400€ / 1,21 | 330,58€ |
| IVA 21% en venta | 330,58€ × 0,21 | 69,42€ |
| Total facturado | BI + IVA | 400€ |

**Comparativa de Costos**:

| Escenario | Antes | Después | Ahorro |
|-----------|-------|---------|--------|
| **Compra a Particular** | 1.210€ (1.000€ + 210€ IVA 21%) | 1.000€ (1.000€ + 0€ IVA) | **-210€** |
| **Compra a Artista** | 1.210€ (1.000€ + 210€ IVA 21%) | 1.100€ (1.000€ + 100€ IVA 10%) | **-110€** |
| **Margen Particular** | 500€ | 500€ | Sin cambios |
| **Margen Artista** | 500€ | 400€ | **-100€** (mayor IVA en compra reduce margen) |

---

## ✅ Checklist de Validación

### Archivos Modificados:
- [x] account.tax-es_common.csv - 3 impuestos (0%, 10%, 21%)
- [x] account.fiscal.position-es_common.csv - 3 posiciones fiscales
- [x] README.rst - Sección Usage reescrita
- [x] VALIDACION_AEAT.md - Nueva sección
- [x] RECOMENDACIONES_AEAT.md - Nueva sección
- [x] RESUMEN_VALIDACION.md - Actualizado
- [x] TIPOS_IVA_REBU_CORRECCION.md - Documento nuevo

### Documentación Actualizada:
- [x] Casos de uso documentados
- [x] Ejemplos de configuración
- [x] Impacto financiero explicado
- [x] Posiciones fiscales claras

### Pruebas Pendientes (en Odoo):
- [ ] Crear proveedor particular y asignar 0% IVA
- [ ] Crear proveedor artista y asignar 10% IVA
- [ ] Crear cliente y asignar 21% IVA venta
- [ ] Generar facturas de prueba
- [ ] Validar cálculos de margen

---

## 📝 Notas Importantes

### 1. Compatibilidad
Estos cambios están orientados a la **realidad fiscal española** bajo régimen REBU para bienes artísticos.

### 2. Estructura CSV

### 2. Estructura CSV
Se mantuvo la estructura CSV compatible con Odoo. Los cambios son aditivos (nuevos impuestos) y no rompen compatibilidad con la venta anterior (21% se mantiene).

### 3. Migración de Datos
Si ya tenías datos con IVA 21% en compras, es importante:
1. Reclasificar las compras existentes
2. Revisar facturas previas
3. Considerar ajustes fiscales si es necesario

### 4. Asesor Fiscal
Se recomienda **validar estos cambios con el asesor fiscal** antes de usar en producción, especialmente:
- Clasificación correcta de proveedores (particular vs artista)
- Aplicabilidad a tu caso específico
- Documentación requerida

---

## 🚀 Próximos Pasos

### Inmediato:
1. Revisar archivos modificados
2. Validar estructura CSV
3. Testar en Odoo

### Esta Semana:
4. Contactar asesor fiscal para validar cambios
5. Reclasificar proveedores existentes
6. Ajustar facturas anteriores si es necesario

### Fase 2 (Según plan):
7. Integrar estos cambios en especificaciones de margen automático
8. Actualizar plan de implementación
9. Revisar ejemplos en especificaciones técnicas

---

## 📞 Referencias

**AEAT - Régimen Especial de Bienes Usados**:
https://sede.agenciatributaria.gob.es/Sede/iva/regimenes-tributacion-iva/regimen-especial-bienes-usados.html

**Documentos internos actualizados**:
- TIPOS_IVA_REBU_CORRECCION.md
- RECOMENDACIONES_AEAT.md (sección 4.1)
- VALIDACION_AEAT.md (nueva sección)

---

**Preparado por**: GitHub Copilot + Usuario  
**Fecha**: 15 de noviembre de 2025  
**Status**: ✅ CAMBIOS IMPLEMENTADOS Y DOCUMENTADOS  
**Próxima acción**: Validación en Odoo + Asesor fiscal
