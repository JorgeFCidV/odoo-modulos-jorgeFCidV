# 🗺️ Plan de Implementación Fase 2 - Cálculo Margen y Facturación REBU

**Fecha**: 14 de noviembre de 2025  
**Versión**: 1.0  
**Estado**: PLAN DETALLADO

---

## 📊 Resumen del Plan

**Objetivo**: Automatizar cálculo de margen y facturación especial REBU

**Duración estimada**: 40-50 horas  
**Prioridad**: 🔴 CRÍTICA  

---

## 🎯 Objetivos de Fase 2

### Objetivo Principal
Implementar cálculo automático de margen bruto según fórmula AEAT y generar facturas con requisitos especiales de régimen REBU.

### Resultados Esperados

1. ✅ **Cálculo correcto de IVA** en facturas REBU
2. ✅ **Documentación de márgenes** en facturas
3. ✅ **Facturación conforme a AEAT** 
4. ✅ **Tests 100% cobertura** margen y facturación
5. ✅ **Zero riesgo fiscal** incumplimiento

---

## 📋 Desglose de Tareas

### TAREA A: Modelo de Línea REBU (12 horas)

**Objetivo**: Crear campos y métodos para cálculo de margen en línea de factura

| Sub-tarea | Descripción | Estimado | Responsable |
|-----------|---|---|---|
| A1 | Crear modelo `account_invoice_line_rebu.py` | 3h | Dev |
| A2 | Implementar campos y métodos | 4h | Dev |
| A3 | Crear migrations (si aplica) | 2h | Dev |
| A4 | Tests unitarios (margen) | 3h | QA |

**Entregables**:
- Modelo con campos: `is_rebu_good`, `rebu_purchase_price`, `rebu_sale_price`, `rebu_margin`, `rebu_taxable_base`
- Métodos compute: `_compute_rebu_margin()`, `_compute_rebu_taxable_base()`
- 5 tests unitarios

**Definición de Hecho**:
- [ ] Modelo crea/actualiza correctamente
- [ ] Campos computados se actualizan automáticamente
- [ ] Tests pasan 100%
- [ ] No hay errores de validación

---

### TAREA B: Vistas Línea REBU (8 horas)

**Objetivo**: Crear interfaz para ingreso de precios REBU en factura

| Sub-tarea | Descripción | Estimado | Responsable |
|-----------|---|---|---|
| B1 | Crear vista XML línea compra | 2h | UI/Dev |
| B2 | Crear vista XML línea venta | 2h | UI/Dev |
| B3 | Agregar campos a vista estándar | 2h | UI/Dev |
| B4 | Tests vista (validación) | 2h | QA |

**Entregables**:
- `views/account_move_line_rebu_views.xml`
- Campos REBU visibles solo si `is_rebu_good=True`
- Validaciones de ingreso

**Definición de Hecho**:
- [ ] Campos REBU visibles en factura
- [ ] Campos ocultos si no es REBU
- [ ] Validación de precios (no negativos)
- [ ] Tests pasan

---

### TAREA C: Modelo de Factura REBU (10 horas)

**Objetivo**: Crear campos agregados y lógica de facturación especial

| Sub-tarea | Descripción | Estimado | Responsable |
|-----------|---|---|---|
| C1 | Crear modelo `account_move_rebu.py` | 3h | Dev |
| C2 | Métodos compute (agregados) | 4h | Dev |
| C3 | Lógica detección REBU | 2h | Dev |
| C4 | Tests integración factura | 1h | QA |

**Entregables**:
- Modelo con campos: `is_rebu_invoice`, `rebu_total_margin`, `rebu_total_taxable_base`, `rebu_tax_amount`
- Método: `_compute_is_rebu_invoice()` (detecta automáticamente)
- Métodos: `_compute_rebu_totals()`

**Definición de Hecho**:
- [ ] Factura detecta régimen REBU automáticamente
- [ ] Totales se calculan correctamente
- [ ] Tests pasan
- [ ] Sin errores al guardar

---

### TAREA D: Vistas Factura REBU (10 horas)

**Objetivo**: Crear interfaz especial para factura REBU

| Sub-tarea | Descripción | Estimado | Responsable |
|-----------|---|---|---|
| D1 | Vista formulario factura REBU | 4h | UI/Dev |
| D2 | Panel informativo margen/BI/IVA | 3h | UI/Dev |
| D3 | Avisos y validaciones | 2h | Dev |
| D4 | Tests vista | 1h | QA |

**Entregables**:
- `views/account_move_rebu_views.xml`
- Panel especial con: Margen | BI | IVA
- Indicador visual "RÉGIMEN REBU"
- Validaciones

**Definición de Hecho**:
- [ ] Vista se muestra correctamente
- [ ] Panel REBU visible
- [ ] Validaciones funcionan
- [ ] Tests pasan

---

### TAREA E: Reporte PDF REBU (8 horas)

**Objetivo**: Crear plantilla especial para impresión de facturas REBU

| Sub-tarea | Descripción | Estimado | Responsable |
|-----------|---|---|---|
| E1 | Crear reporte base | 3h | Dev |
| E2 | Diseño sección REBU | 3h | UI/Dev |
| E3 | Validaciones PDF | 2h | QA |

**Entregables**:
- `reports/account_invoice_rebu_report.xml`
- Template con sección REBU especial
- NO desglose IVA por línea
- Muestra: Margen | BI | IVA

**Definición de Hecho**:
- [ ] PDF se genera correctamente
- [ ] Sección REBU visible
- [ ] Sin desglose IVA
- [ ] Notas incluidas

---

### TAREA F: Tests Completos (10 horas)

**Objetivo**: Cobertura 100% de new tests (margen + factura)

| Sub-tarea | Descripción | Estimado | Responsable |
|-----------|---|---|---|
| F1 | Tests margen cálculo | 3h | QA |
| F2 | Tests factura REBU | 3h | QA |
| F3 | Tests integración end-to-end | 2h | QA |
| F4 | Cobertura y reportes | 2h | QA |

**Entregables**:
- `tests/test_rebu_margin_automatic.py` (nuevos tests)
- `tests/test_rebu_invoice_special.py` (nuevos tests)
- Reporte de cobertura (target: 100%)

**Definición de Hecho**:
- [ ] 20+ tests nuevos
- [ ] 100% cobertura de nuevo código
- [ ] Todos los tests pasan
- [ ] Reporte generado

---

### TAREA G: Documentación (6 horas)

**Objetivo**: Documentar cambios para usuarios y desarrolladores

| Sub-tarea | Descripción | Estimado | Responsable |
|-----------|---|---|---|
| G1 | Guía de usuario | 2h | Doc |
| G2 | Documentación técnica | 2h | Dev/Doc |
| G3 | Ejemplos prácticos | 1h | Doc |
| G4 | Troubleshooting | 1h | QA/Doc |

**Entregables**:
- Guía usuario: "Cómo crear factura REBU"
- Documentación técnica: arquitectura
- Ejemplos: casos de uso reales
- FAQ

**Definición de Hecho**:
- [ ] Documentación completa
- [ ] Ejemplos claros
- [ ] Fácil de seguir
- [ ] Revisada

---

### TAREA H: QA y Validación (8 horas)

**Objetivo**: Validar que implementación cumple con AEAT

| Sub-tarea | Descripción | Estimado | Responsable |
|-----------|---|---|---|
| H1 | Tests manuales en Odoo | 3h | QA |
| H2 | Validación AEAT (fórmula) | 2h | QA + Asesor |
| H3 | Edge cases | 2h | QA |
| H4 | Preparar para asesor fiscal | 1h | PM |

**Entregables**:
- Reporte de tests manuales
- Matriz de validación AEAT
- Documento para asesor fiscal
- Lista de edge cases cubiertos

**Definición de Hecho**:
- [ ] Todos los tests manuales pasan
- [ ] Asesor valida fórmula
- [ ] Edge cases documentados
- [ ] Listo para producción

---

## 🗓️ Cronograma

### Semana 1: Modelos y Base de Datos

```
Lunes-Martes:     TAREA A (Modelo línea)         6h
Miércoles:        TAREA C (Modelo factura)       4h
Jueves:           TAREA B (Vistas línea)         4h
Viernes:          Integración y fixing            2h
────────────────────────────────────────────────────────
Total semana 1:                                  16h
```

### Semana 2: Interfaz y Reportes

```
Lunes-Martes:     TAREA D (Vistas factura)       6h
Miércoles:        TAREA E (Reporte PDF)          4h
Jueves:           TAREA F (Tests)                6h
Viernes:          Bug fixes y ajustes             2h
────────────────────────────────────────────────────────
Total semana 2:                                  18h
```

### Semana 3: Testing y Documentación

```
Lunes-Martes:     TAREA G (Documentación)        4h
Miércoles-Jueves: TAREA H (QA y Validación)      6h
Viernes:          Buffer y ajustes finales       2h
────────────────────────────────────────────────────────
Total semana 3:                                  12h
```

---

## 👥 Equipo Requerido

| Rol | Horas | Responsabilidades |
|-----|-------|------------------|
| **Desarrollador Senior** | 25h | A1, A2, C1, C2, C3, E1 |
| **UI/Front Developer** | 12h | B1, B2, B3, D1, D2, E2 |
| **QA Engineer** | 15h | A4, D4, E3, F1, F2, F3, F4, H1, H3 |
| **Tech Writer/Doc** | 6h | G1, G2, G3, G4 |
| **PM/Architect** | 4h | H2, H4, coordinación |
| **Asesor Fiscal** | 3h | H2, validación |
| **TOTAL** | **65h** | |

---

## 📊 Entregables por Semana

### Semana 1 Entregables

```
✅ Modelo account_invoice_line_rebu.py
✅ Campos y métodos de cálculo
✅ Vistas línea REBU (compra)
✅ Tests unitarios iniciales (5)
✅ Migrations (si aplica)
```

### Semana 2 Entregables

```
✅ Modelo account_move_rebu.py
✅ Vistas formulario factura REBU
✅ Panel informativo (Margen/BI/IVA)
✅ Reporte PDF especial
✅ Tests integración (15 tests)
✅ Bug fixes iniciales
```

### Semana 3 Entregables

```
✅ Documentación usuario
✅ Documentación técnica
✅ Cobertura 100% (reporte)
✅ QA completa
✅ Aprobación asesor fiscal
✅ Listo para producción
```

---

## 🎯 Definición de Hecho (DoD)

Cada tarea debe cumplir:

1. ✅ **Código implementado** y funcional
2. ✅ **Tests escritos** (100% cobertura de lógica nueva)
3. ✅ **Todos los tests pasan**
4. ✅ **Code review completado**
5. ✅ **Documentación actualizada**
6. ✅ **Sin bugs conocidos**
7. ✅ **Validación AEAT confirmada**

---

## 🚨 Riesgos Identificados

| Riesgo | Impacto | Probabilidad | Mitigación |
|--------|---------|---|---|
| Cambios en especificación AEAT | Alto | Bajo | Revisar AEAT oficialmente antes de finalizar |
| Complejidad integración Odoo | Alto | Medio | Hacer POC rápido en semana 1 |
| Retrasos en asesoría fiscal | Medio | Medio | Contactar temprano en proceso |
| Bugs en cálculos | Alto | Bajo | Tests exhaustivos + validación externa |

---

## ✅ Criterios de Éxito

**La Fase 2 es exitosa cuando:**

1. ✅ Todos los tests pasan (100% del código nuevo)
2. ✅ Asesor fiscal valida que fórmula AEAT es correcta
3. ✅ Factura REBU se genera sin desglose IVA
4. ✅ Margen se calcula automáticamente
5. ✅ Documentación completa y clara
6. ✅ Zero bugs críticos
7. ✅ Listo para entorno de producción

---

## 📞 Dependencias Externas

| Dependencia | Proveedor | Status |
|---|---|---|
| Validación AEAT | Asesor Fiscal | ⏳ Por contactar |
| Especificaciones | AEAT | ✅ Obtenidas |
| Infraestructura Odoo | TI | ✅ Disponible |

---

## 🔄 Procesos de Revisión

### Code Review

```
Dev → Code Review → QA → Merge
```

### QA Review

```
Dev Completed → QA Testing → Pass/Fail → Deploy
```

### AEAT Validation

```
Implementation → Prepare docs → Asesor Fiscal → Approved/Changes
```

---

## 📈 Métricas de Seguimiento

```
Semana 1:
├─ Tests pasando: 5/5 (100%)
├─ Code coverage: 80%
└─ Tareas completadas: 3/8 (37%)

Semana 2:
├─ Tests pasando: 20/20 (100%)
├─ Code coverage: 95%
└─ Tareas completadas: 7/8 (87%)

Semana 3:
├─ Tests pasando: 20/20 (100%)
├─ Code coverage: 100%
├─ Asesor fiscal: Validado ✅
└─ Tareas completadas: 8/8 (100%)
```

---

## 🎓 Capacitación Requerida

Para que el equipo sea efectivo:

1. **Desarrolladores**: Conocer modelo REBU, fórmula AEAT
2. **QA**: Entender requisitos fiscales, validación AEAT
3. **Usuarios**: Ver demo de facturación REBU
4. **Asesor**: Revisar diseño e implementación

---

## 📋 Checklist Pre-Inicio

Antes de comenzar Fase 2:

- [ ] Equipo confirmado
- [ ] Especificaciones revisadas
- [ ] Asesor fiscal contactado
- [ ] Ambiente Odoo 17 preparado
- [ ] Repositorio git actualizado
- [ ] Ramas de desarrollo creadas
- [ ] Herramientas de testing configuradas
- [ ] Documentación base generada

---

## 🚀 Post-Implementación

Después de Fase 2:

```
Fase 2 Completa
    ↓
Testing en Staging (1 semana)
    ↓
Asesor Fiscal Valida
    ↓
Deployment Producción (si es requerido)
    ↓
Monitoreo (4 semanas)
    ↓
Cierre Fase 2
```

---

## 📞 Referencias

- **Especificación Margen**: `ESPECIFICACION_MARGEN_AUTOMATICO_REBU.md`
- **Especificación Factura**: `ESPECIFICACION_FACTURACION_REBU_ESPECIAL.md`
- **Validación AEAT**: `VALIDACION_AEAT.md`
- **Pruebas Base**: `PRUEBAS_VALIDACION_REBU.md`

---

**Documento**: PLAN_IMPLEMENTACION_FASE_2.md  
**Estado**: ✅ PLAN COMPLETO  
**Próximo Paso**: Iniciar Tarea A (Modelo línea REBU)
