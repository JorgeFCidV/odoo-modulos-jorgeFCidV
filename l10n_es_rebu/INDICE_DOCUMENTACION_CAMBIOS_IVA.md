# 📚 ÍNDICE: Corrección de IVA en Compras REBU - 15 Noviembre 2025

**Estado**: ✅ ESPECIFICACIÓN COMPLETADA  
**Fecha**: 15 de noviembre de 2025  
**Alcance**: Corrección fundamental de lógica del módulo REBU

---

## 🎯 INTRODUCCIÓN

A partir de la identificación de que solo existen **dos casos reales de IVA en compras** (0% para particulares y 10% para artistas originales, vs el incorrecto 21% asumido), se ha replanificado **completamente la lógica del módulo REBU**.

Esta corrección afecta:
- ✅ Configuración de impuestos (CSV)
- ✅ Cálculo de costos y márgenes
- ⏳ Implementación de código (FASE 2)
- ⏳ Vistas y wizards (FASE 2)
- ⏳ Tests y validación (FASE 2)

---

## 📁 DOCUMENTOS DISPONIBLES

### 1. **CAMBIOS_15NOV_TIPOS_IVA.md** (400 líneas)
**Propósito**: Documento operativo de cambios realizados  
**Contenido**:
- ✅ Resumen ejecutivo (antes vs después)
- ✅ 7 archivos modificados (CSV + documentación)
- ✅ Configuración en Odoo (pasos por tipo)
- ✅ **Ejemplo práctico corregido** (con fórmula AEAT correcta)
- ✅ Checklist de validación
- ✅ Próximos pasos

**Leer si**: Necesitas entender QUÉ cambió y POR QUÉ  
**Enlace**: `./CAMBIOS_15NOV_TIPOS_IVA.md`

---

### 2. **CAMBIOS_LOGICOS_MODULO_CORRECCION_IVA.md** (350 líneas)
**Propósito**: Especificación técnica de cambios por nivel  
**Contenido**:
- 📊 Matriz de cambios (datos, código, UI, reportes)
- 🛠️ Nivel 1: Configuración de impuestos (✅ completado)
- 💾 Nivel 2: Estructura de datos (7 campos nuevos, ⏳ pendiente)
- 🔧 Nivel 2: Métodos de cálculo (5 métodos, ⏳ pendiente)
- ✅ Nivel 3: Validaciones (2 métodos, ⏳ pendiente)
- 🎨 Cambios en vistas y formularios (⏳ pendiente)
- 🧪 Cambios en tests (⏳ pendiente)
- 🚀 Plan de implementación (65h, 4 semanas, FASE 2)

**Leer si**: Necesitas comprender la arquitectura técnica del cambio  
**Enlace**: `./CAMBIOS_LOGICOS_MODULO_CORRECCION_IVA.md`

---

### 3. **IMPLEMENTACION_PYTHON_CORRECCION_IVA.md** (400 líneas)
**Propósito**: Código Python listo para implementar  
**Contenido**:
- 🐍 Código completo de `models/account_invoice_extension.py`
- 📋 7 campos con descripciones detalladas
- 🔗 5 métodos computados (con decoradores @api.depends)
- ✅ 2 métodos de validación (@api.constrains)
- 🛠️ 4 métodos auxiliares
- 🔄 Flujo de cálculo visual (5 pasos)
- 🔌 Integraciones con otros modelos
- ✅ Checklist de implementación

**Leer si**: Eres desarrollador y necesitas implementar los cambios  
**Enlace**: `./IMPLEMENTACION_PYTHON_CORRECCION_IVA.md`

---

### 4. **RESUMEN_CAMBIOS_LOGICOS_MODULO.md** (300 líneas)
**Propósito**: Resumen ejecutivo de todo lo anterior  
**Contenido**:
- 🎯 Objetivo y flujo actual vs nuevo
- 📊 Matriz de cambios (tabla resumen)
- 🛠️ Componentes clave (campos, métodos, validaciones)
- 📈 Impacto financiero por escenario
- 📁 Documentos generados (este índice)
- 🚀 Próximos pasos (fases 2.1 a 2.4)
- ⚠️ Consideraciones críticas
- ✅ Checklist final

**Leer si**: Quieres una vista general de TODO  
**Enlace**: `./RESUMEN_CAMBIOS_LOGICOS_MODULO.md`

---

### 5. **INDICE_DOCUMENTACION_CAMBIOS_IVA.md** (este archivo)
**Propósito**: Guía de navegación  
**Contenido**:
- 📚 Índice de documentos
- 🎯 Cómo leer los documentos
- 📊 Matriz de decisión
- 🔗 Referencias cruzadas

**Leer si**: Necesitas orientarte en la documentación  
**Enlace**: `./INDICE_DOCUMENTACION_CAMBIOS_IVA.md` (TÚ ESTÁS AQUÍ)

---

## 🎯 MATRIZ DE DECISIÓN: ¿CUÁL LEER?

```
¿Soy...?                          → ¿Necesito...?                      → Leer
────────────────────────────────────────────────────────────────────────────
Usuario REBU                      → Entender cálculos nuevos           → CAMBIOS_15NOV
                                  → Configurar Odoo                    → CAMBIOS_15NOV
                                  → Casos de uso prácticos             → CAMBIOS_15NOV

Analista Funcional                → Especificación técnica             → CAMBIOS_LOGICOS
                                  → Entender impacto en BBDD           → CAMBIOS_LOGICOS
                                  → Plan de implementación             → CAMBIOS_LOGICOS
                                  → Resumen ejecutivo                  → RESUMEN_CAMBIOS

Desarrollador Python              → Código listo para implementar      → IMPLEMENTACION_PYTHON
                                  → Estructura de campos               → IMPLEMENTACION_PYTHON
                                  → Métodos computados                 → IMPLEMENTACION_PYTHON
                                  → Validaciones                       → IMPLEMENTACION_PYTHON

Asesor Fiscal                     → Validar cálculos AEAT              → CAMBIOS_15NOV
                                  → Verificar fórmula BI               → CAMBIOS_15NOV
                                  → Casos de uso                       → CAMBIOS_LOGICOS (2.2)

Jefe de Proyecto                  → Resumen ejecutivo                  → RESUMEN_CAMBIOS
                                  → Plan de implementación             → CAMBIOS_LOGICOS (final)
                                  → Estimación de recursos             → RESUMEN_CAMBIOS

QA / Tester                       → Casos de test                      → ESPECIFICACION_MARGEN...
                                  → Escenarios a probar                → CAMBIOS_LOGICOS (2.2)
                                  → Validaciones                       → IMPLEMENTACION_PYTHON
```

---

## 🔄 FLUJO DE LECTURA RECOMENDADO

### Para Entender Rápidamente (15 minutos)
1. Lee: **RESUMEN_CAMBIOS_LOGICOS_MODULO.md** (solo secciones 1-3)
2. Entiende: Los 3 tipos de IVA y el flujo de cálculo
3. Conclusion: Qué cambió y por qué

### Para Implementar (2-3 horas)
1. Lee: **CAMBIOS_LOGICOS_MODULO_CORRECCION_IVA.md** (completo)
2. Lee: **IMPLEMENTACION_PYTHON_CORRECCION_IVA.md** (completo)
3. Implementa: Código según especificación
4. Valida: Con tests según sección 5 del documento

### Para Validar (1 hora)
1. Lee: **CAMBIOS_15NOV_TIPOS_IVA.md** (ejemplos)
2. Verifica: Cálculos en Odoo
3. Contacta: Asesor fiscal si necesitas validación

### Para Presentar a Stakeholders (30 minutos)
1. Usa: **RESUMEN_CAMBIOS_LOGICOS_MODULO.md**
2. Muestra: Impacto financiero (sección 5)
3. Presenta: Plan de implementación (sección 6)

---

## 📊 CAMBIOS RESUMIDOS

| Aspecto | Antes | Después | Estado |
|---------|-------|---------|--------|
| **Tipos de IVA compra** | 1 (21%) | 3 (0%, 10%, 21%) | ✅ CSV |
| **Posiciones fiscales** | 1 | 3 | ✅ CSV |
| **Cálculo de margen** | Sobre PVP total | Sobre margen bruto | ⏳ Código |
| **Coste de compra real** | Sin IVA no deducible | Con IVA no deducible | ⏳ Código |
| **Fórmula BI** | No aplicable | (Margen ÷ 1,21) | ⏳ Código |
| **Ahorro por transacción** | - | 210€ (particular) o 110€ (artista) | ✅ Calculado |

---

## 🔗 REFERENCIAS ENTRE DOCUMENTOS

```
CAMBIOS_15NOV_TIPOS_IVA.md
├─ Referencias a: CAMBIOS_LOGICOS (para profundizar)
├─ Ejemplos de: Escenarios A y B
└─ Resultado de: Cambios 15 NOV

CAMBIOS_LOGICOS_MODULO_CORRECCION_IVA.md
├─ Extiende: CAMBIOS_15NOV (con especificación técnica)
├─ Usa: Ejemplos de CAMBIOS_15NOV
├─ Referencia: IMPLEMENTACION_PYTHON (sección 2.2)
└─ Plan implementa: 7 campos + 5 métodos

IMPLEMENTACION_PYTHON_CORRECCION_IVA.md
├─ Implementa: CAMBIOS_LOGICOS (Nivel 2)
├─ Codifica: 7 campos especificados
├─ Codifica: 5 métodos computados
├─ Codifica: 2 validaciones
└─ Integra: Con otros modelos

RESUMEN_CAMBIOS_LOGICOS_MODULO.md
├─ Resume: CAMBIOS_15NOV
├─ Resume: CAMBIOS_LOGICOS
├─ Resume: IMPLEMENTACION_PYTHON
└─ Proporciona: Vista ejecutiva completa
```

---

## ⚠️ NOTAS IMPORTANTES

### 1. Estados de Implementación

- **✅ COMPLETADO**: Cambios en CSV + documentación
- **⏳ PENDIENTE**: Implementación de código (FASE 2)
- **🔄 VALIDAR**: Con asesor fiscal antes de producción

### 2. Archivos Modificados

**Ya modificados (15 NOV 2025)**:
- ✅ `data/template/account.tax-es_common.csv` (3 impuestos)
- ✅ `data/template/account.fiscal.position-es_common.csv` (3 posiciones)
- ✅ `README.rst` (sección Usage reescrita)
- ✅ `VALIDACION_AEAT.md` (nueva sección)
- ✅ `RECOMENDACIONES_AEAT.md` (sección 4.1 añadida)
- ✅ `RESUMEN_VALIDACION.md` (actualizado)

**Por crear (FASE 2)**:
- ⏳ `models/account_invoice_extension.py` (NUEVO)
- ⏳ `views/account_invoice_line_rebu.xml` (NUEVO)
- ⏳ `wizards/rebu_invoice_wizard.py` (NUEVO)
- ⏳ Tests actualizado/nuevos

### 3. Dependencias Críticas

- Fórmula AEAT: BI = (Margen × 100) ÷ (100 + tasa IVA)
- Tipos IVA: 0% (particular), 10% (artista), 21% (venta)
- IVA no deducible se suma al coste de compra
- Margen se calcula sobre coste REAL (incluye IVA)

### 4. Validación Requerida

- ✅ Ejemplos matemáticos: Verificados
- ⏳ Asesor fiscal: Por confirmar
- ⏳ AEAT: Aplicabilidad confirmar
- ⏳ Odoo: Test en ambiente

---

## 📈 LÍNEA DE TIEMPO

**Completado**: 15 NOV 2025
- ✅ Corrección CSV
- ✅ Especificación lógica (350 líneas)
- ✅ Especificación código (400 líneas)
- ✅ Documentación completa (1.450+ líneas)

**Planeado - FASE 2 (4 semanas, 65 horas)**:
- Semana 1: Base de datos (campos + índices)
- Semana 2: Lógica (métodos + validaciones + tests)
- Semana 3: UI (vistas + wizards + reportes)
- Semana 4: Testing (suite + validación fiscal)

**Bloqueante**:
- ⏳ Validación asesor fiscal

---

## ✅ CHECKLIST DE REVISIÓN

### Leer documentación:
- [ ] CAMBIOS_15NOV_TIPOS_IVA.md (ejemplos)
- [ ] CAMBIOS_LOGICOS_MODULO_CORRECCION_IVA.md (especificación)
- [ ] IMPLEMENTACION_PYTHON_CORRECCION_IVA.md (código)
- [ ] RESUMEN_CAMBIOS_LOGICOS_MODULO.md (resumen ejecutivo)

### Validar cambios:
- [ ] CSV de impuestos correctamente modificados
- [ ] Ejemplos cálculos matemáticamente correctos
- [ ] Especificación técnica completa
- [ ] Código Python listo para usar

### Aprobar para FASE 2:
- [ ] Usuario de negocio: Confirma cambios de IVA
- [ ] Asesor fiscal: Valida clasificación 0% y 10%
- [ ] Jefe de proyecto: Aprueba plan 65h
- [ ] Desarrollador: Revisa código Python

---

## 🎓 EJEMPLO PRÁCTICO COMPLETO

Ver: **CAMBIOS_15NOV_TIPOS_IVA.md** → Sección "Ejemplo Práctico"

Contiene:
- Escenario 1: Compra a particular (0% IVA)
- Escenario 2: Compra a artista (10% IVA)
- Fórmula AEAT aplicada paso a paso
- Verificación de cálculos
- Impacto financiero

---

## 🔍 BÚSQUEDA RÁPIDA

**¿Dónde encuentro...?**

| Concepto | Documento | Sección |
|----------|-----------|---------|
| Fórmula BI AEAT | CAMBIOS_15NOV | "Estructura de Costos" |
| Campos a crear | IMPLEMENTACION_PYTHON | "Sección 1" |
| Métodos computados | IMPLEMENTACION_PYTHON | "Sección 2" |
| Validaciones | IMPLEMENTACION_PYTHON | "Sección 3" |
| Plan 65h | CAMBIOS_LOGICOS | "Plan de Implementación" |
| Ejemplos paso a paso | CAMBIOS_15NOV | "Ejemplo Práctico" |
| Impacto financiero | RESUMEN_CAMBIOS | "Sección 5" |
| Código completo | IMPLEMENTACION_PYTHON | "Código Completo" |

---

## 📞 SOPORTE

**Preguntas sobre**:

- **Cálculos**: Ver CAMBIOS_15NOV_TIPOS_IVA.md
- **Especificación técnica**: Ver CAMBIOS_LOGICOS_MODULO_CORRECCION_IVA.md
- **Código Python**: Ver IMPLEMENTACION_PYTHON_CORRECCION_IVA.md
- **Resumen/Plan**: Ver RESUMEN_CAMBIOS_LOGICOS_MODULO.md
- **Validación fiscal**: Contactar asesor fiscal

---

## 📊 ESTADÍSTICAS

| Métrica | Valor |
|---------|-------|
| Documentos creados | 5 |
| Líneas de documentación | 1.450+ |
| Campos nuevos diseñados | 7 |
| Métodos computados | 5 |
| Validaciones | 2 |
| Tests diseñados | 39+ |
| Horas de desarrollo estimadas | 65 |
| Semanas de implementación | 4 |
| Ahorro por transacción (particular) | 210€ |
| Ahorro por transacción (artista) | 110€ |

---

## 🎯 CONCLUSIÓN

**Estado actual**: Especificación técnica COMPLETA y lista para Fase 2.

Toda la lógica del módulo REBU ha sido replanificada para soportar los 3 tipos de IVA (0%, 10%, 21%) según origen de compra. Los cálculos, validaciones y flujos están documentados en código Python listo para implementar.

**Próximo paso**: Validación con asesor fiscal → Implementación (65h, 4 semanas)

---

**Documento preparado por**: GitHub Copilot  
**Última actualización**: 15 de noviembre de 2025  
**Estado**: ✅ LISTO PARA REFERENCIA Y FASE 2
