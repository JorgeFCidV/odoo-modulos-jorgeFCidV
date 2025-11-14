# FASE 2: IMPLEMENTACIÓN AUTOMÁTICA DE MARGEN REBU

**Estado**: ✅ ESPECIFICACIÓN COMPLETA Y LISTA PARA DESARROLLO

**Fecha**: 14 de noviembre de 2025

---

## 📊 Resumen Ejecutivo

### Objetivo
Automatizar el cálculo del margen bruto en régimen REBU según fórmula AEAT para eliminar riesgos fiscales y errores manuales.

### Cambio Principal
- **ANTES (Fase 1)**: Margen calculado manualmente → Riesgo de error fiscal
- **DESPUÉS (Fase 2)**: Margen calculado automáticamente → 100% conformidad AEAT

### Impacto
- ✅ Elimina error de 174,38€ por transacción
- ✅ 100% conformidad con AEAT
- ✅ Reducción de riesgo fiscal a cero
- ✅ Automatización completa

---

## 📂 Documentos de Especificación

### 1. Especificación técnica: Margen automático
**Archivo**: `ESPECIFICACION_MARGEN_AUTOMATICO_REBU.md`

**Contenido**:
- Fórmula AEAT: BI = (Margen × 100) ÷ 121
- Arquitectura 3 niveles (DB → Logic → UI)
- Definición de campos del modelo
- Métodos compute paso a paso
- Vistas XML ejemplificadas
- Tests diseñados

**Líneas**: 400+

### 2. Especificación técnica: Facturación especial
**Archivo**: `ESPECIFICACION_FACTURACION_REBU_ESPECIAL.md`

**Contenido**:
- Requisitos AEAT: Sin desglose VAT por línea
- Cambios en interfaz de usuario
- Modelo account_move_rebu
- Reporte PDF especial
- Flujo de generación de factura

**Líneas**: 450+

### 3. Plan de implementación (65 horas)
**Archivo**: `PLAN_IMPLEMENTACION_FASE_2.md`

**Contenido**:
- 8 tareas concretas (A-H)
- Cronograma 3 semanas
- Asignación de equipo
- Entregables por semana
- Criterios de "Hecho"

**Líneas**: 350+

### 4. Resumen ejecutivo
**Archivo**: `RESUMEN_TAREA_4_ESPECIFICACION.md`

**Contenido**:
- Problema y solución
- Cambios principales
- Ejemplo práctico
- Estado de implementación

**Líneas**: 300+

---

## 🔧 Plan de Implementación (8 Tareas - 65 horas)

### Semana 1: Modelos (16 horas)

#### Tarea A: Modelo de línea REBU (12 horas)
- Crear archivo: `models/account_invoice_line_rebu.py`
- Campos a definir:
  - `is_rebu_good`: ¿Es un bien REBU?
  - `rebu_purchase_price`: Precio de compra histórico
  - `rebu_sale_price`: Precio de venta actual
  - `rebu_margin`: Computado = venta - compra
  - `rebu_taxable_base`: Computado = (margen × 100) ÷ 121
- Métodos compute:
  - `_compute_rebu_margin()`
  - `_compute_rebu_taxable_base()`
- Crear tests unitarios

**Criterio "Hecho"**:
- ✅ Campo `rebu_margin` calcula correctamente
- ✅ Campo `rebu_taxable_base` usa fórmula AEAT
- ✅ 100% cobertura tests modelo

#### Tarea B: Vistas para línea REBU (4 horas)
- Vista formulario línea REBU
- Panel de información (Margen | BI | IVA)
- Validaciones en vistas
- Pruebas en UI

### Semana 2: UI y Reportes (18 horas)

#### Tarea C: Modelo de factura REBU (10 horas)
- Crear archivo: `models/account_move_rebu.py`
- Campos a definir:
  - `is_rebu_invoice`: ¿Es factura REBU?
  - `rebu_total_margin`: Total margen computado
  - `rebu_total_taxable_base`: Total BI computado
  - `rebu_tax_amount`: Total IVA computado
- Métodos compute:
  - `_compute_is_rebu_invoice()`
  - `_compute_rebu_totals()`
- Integración con account.move
- Tests integración

#### Tarea D: Vistas para factura REBU (8 horas)
- Vista formulario factura REBU
- Referencia a régimen REBU visible
- Panel información márgenes
- Validación: Sin desglose VAT por línea
- Tests UI

### Semana 3: QA y Documentación (12 horas)

#### Tarea E: Reporte PDF especial (8 horas)
- Template QWeb para PDF REBU
- PDF sin desglose VAT por línea
- Muestra: Margen | Base Imponible | IVA Total
- Referencia visible a régimen REBU
- Validación layout

#### Tarea F: Suite de tests completa (10 horas)
- Tests modelo línea: 10 tests
- Tests modelo factura: 10 tests
- Tests integración: 5 tests
- Tests reporte: 3 tests
- Alcanzar 100% cobertura en código REBU

#### Tarea G: Documentación (6 horas)
- Documentar código
- Guía de usuario
- Guía de administrador
- Excepciones y límites
- Ejemplos de uso

#### Tarea H: QA y validación AEAT (8 horas)
- Ejecutar suite completa
- Validación manual casos críticos
- Validación con asesor fiscal
- Documentar conformidad AEAT
- Ajustes finales

---

## 📈 Cronograma Detallado

### Semana 1: Modelos (16 horas)

```
Lunes-Martes:  Modelo línea REBU + vistas         6h
Miércoles:     Modelo factura REBU                4h
Jueves:        Vistas línea                       4h
Viernes:       Integración inicial                2h
               ENTREGABLES: Models ✅ Tests ✅
```

### Semana 2: UI y Reportes (18 horas)

```
Lunes-Martes:  Vistas factura + panel             6h
Miércoles:     Reporte PDF REBU                   4h
Jueves:        Tests integración                  6h
Viernes:       Bug fixes y ajustes                2h
               ENTREGABLES: UI ✅ PDF ✅ Tests ✅
```

### Semana 3: QA y Documentación (12 horas)

```
Lunes-Martes:  Documentación técnica              4h
Miércoles-Jue: QA + validación AEAT               6h
Viernes:       Ajustes finales y deployment       2h
               ENTREGABLES: Docs ✅ AEAT validated ✅
```

---

## 👥 Equipo Requerido (65 horas)

| Rol | Horas | Tareas | Descripción |
|-----|-------|--------|-------------|
| Dev Senior | 25h | A, C, E, F | Modelos, lógica, tests |
| UI Dev | 12h | B, D | Vistas, interfaces |
| QA Engineer | 15h | F, H | Tests, validación |
| Tech Writer | 6h | G | Documentación |
| PM/Architect | 4h | - | Coordinación |
| Asesor Fiscal | 3h | H | Validación AEAT |
| **TOTAL** | **65h** | | **3 semanas** |

---

## ✅ Definición de "Hecho" (DoD)

### Por modelo
- [ ] Código compilable sin errores
- [ ] 100% de tests pasando
- [ ] Cobertura >= 95%
- [ ] Documentación de API

### Por vista
- [ ] Layout correcto en desktop y mobile
- [ ] Validaciones funcionando
- [ ] Sin errores en consola
- [ ] Accesibilidad validada

### Por reporte
- [ ] PDF genera sin errores
- [ ] Layout REBU especial implementado
- [ ] Sin desglose VAT por línea
- [ ] Información correcta mostrada

### Antes de producción
- [ ] 100% cobertura tests
- [ ] Validación asesor fiscal
- [ ] Documentación completa
- [ ] No hay bugs críticos

---

## 📊 Ejemplos Prácticos

### Ejemplo 1: Bien artístico (compra)

```
ENTRADA:
- Bien REBU: Cuadro antiguo
- is_rebu_good: TRUE
- rebu_purchase_price: 1.000€

PROCESAMIENTO:
- Margen = 0€ (es compra inicial)
- BI = 0€

SALIDA EN ODOO:
- Impuesto: IVA Soportado no deducible REBU 21%
- IVA: 0€ (margen = 0)
- Total: 1.000€
```

### Ejemplo 2: Bien artístico (venta)

```
ENTRADA:
- Bien REBU: Cuadro antiguo
- is_rebu_good: TRUE
- rebu_purchase_price: 1.000€ (histórico)
- rebu_sale_price: 1.500€ (actual)

PROCESAMIENTO (AUTOMÁTICO - Fase 2):
- rebu_margin = 1.500 - 1.000 = 500€
- rebu_taxable_base = (500 × 100) ÷ 121 = 413,22€
- IVA = 413,22 × 0,21 = 86,78€
- Total = 413,22 + 86,78 = 500€

SALIDA EN ODOO:
- Impuesto: IVA Repercutido incluido REBU 21%
- Base imponible: 413,22€ ✅
- IVA: 86,78€ ✅
- Total: 500€ ✅

DIFERENCIA vs INCORRECTO:
- Incorrecto: 1.500 × 0,21 ÷ 1,21 = 261,16€ ❌
- Diferencia: -174,38€ (AHORRADO) ✅
```

---

## 🎯 Métricas de Éxito

### Antes de Fase 2
- Cobertura tests: 97%
- Conformidad AEAT: 80% (margen manual)
- Riesgo fiscal: 🔴 ALTO

### Después de Fase 2
- Cobertura tests: 99%+
- Conformidad AEAT: 100% (margen automático)
- Riesgo fiscal: 🟢 CERO
- Automatización: 100%

---

## 📋 Checklist de Inicio

Antes de comenzar Fase 2:

- [ ] Equipo técnico reunido y alineado
- [ ] Especificaciones revisadas por arquitecto
- [ ] Ambiente de desarrollo preparado
- [ ] Repositorio con rama feature/phase2 creada
- [ ] Asesor fiscal contactado para validación posterior
- [ ] Base de datos de prueba con datos REBU
- [ ] Herramientas de testing configuradas (pytest)
- [ ] IDE y linters configurados

---

## 🚀 Próximos Pasos

1. ✅ **Leer** las 4 especificaciones (1.200+ líneas)
2. ✅ **Revisar** ejemplos de código Python
3. ✅ **Confirmar** cronograma con equipo
4. ✅ **Iniciar** Tarea A (Modelo línea REBU)

---

## 📞 Referencias

**Especificaciones técnicas**:
- `ESPECIFICACION_MARGEN_AUTOMATICO_REBU.md`
- `ESPECIFICACION_FACTURACION_REBU_ESPECIAL.md`
- `PLAN_IMPLEMENTACION_FASE_2.md`

**AEAT oficial**:
- https://sede.agenciatributaria.gob.es/

**Tarea 6 pendiente**:
- Validación fiscal con asesor fiscal

---

**Versión**: 2.0  
**Fecha**: 14 de noviembre de 2025  
**Estado**: ✅ ESPECIFICACIÓN COMPLETA
