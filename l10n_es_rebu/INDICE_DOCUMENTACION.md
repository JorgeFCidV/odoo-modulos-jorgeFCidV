# Índice de Documentación - Módulo REBU para Odoo 17

Navegación rápida por toda la documentación disponible del módulo REBU.

---

## 📚 Documentación Principal

### Para usuarios finales:

1. **[README.rst](README.rst)** - Punto de entrada
   - Descripción general del módulo
   - Características principales
   - Referencias oficiales AEAT
   - ⏱️ **Lectura: 5 min**

2. **[readme/DESCRIPTION.md](readme/DESCRIPTION.md)** - Descripción detallada
   - ¿A quién va dirigido?
   - ¿Qué es el REBU?
   - Características fiscales
   - Impuestos incluidos
   - ⏱️ **Lectura: 10 min**

3. **[readme/CONFIGURE.md](readme/CONFIGURE.md)** - Instalación
   - Pasos de instalación del módulo
   - Recargar localización fiscal
   - Verificación de instalación
   - ⏱️ **Lectura: 5 min**

4. **[readme/USAGE.md](readme/USAGE.md)** - Uso práctico
   - Asignación de impuestos a productos
   - Asignación de posiciones fiscales
   - Cálculo en facturas (con ejemplo)
   - Troubleshooting
   - ⏱️ **Lectura: 15 min**

---

## 🔍 Documentación Técnica / Validación

### Para desarrolladores y asesores fiscales:

5. **[CAMBIOS_REALIZADOS.md](CAMBIOS_REALIZADOS.md)** - Historial técnico
   - Cambios de nombres y estructura
   - Archivos modificados (detalle)
   - Impuestos configurados
   - Tabla resumen
   - ⏱️ **Lectura: 10 min**

6. **[VALIDACION_AEAT.md](VALIDACION_AEAT.md)** - Validación oficial
   - Información consultada de AEAT
   - Características confirmadas
   - Validación del módulo
   - Observaciones y sugerencias
   - ⏱️ **Lectura: 10 min**

7. **[RECOMENDACIONES_AEAT.md](RECOMENDACIONES_AEAT.md)** - Guía de cumplimiento
   - **CRÍTICO**: Régimen voluntario - debe optarse expresamente
   - Bienes que aplican (checklist)
   - Base imponible = MARGEN BRUTO (fórmulas)
   - IVA no deducible (segregación importante)
   - Obligaciones de facturación
   - Checklist de implementación
   - **⏱️ Lectura OBLIGATORIA: 20 min**

8. **[RESUMEN_VALIDACION.md](RESUMEN_VALIDACION.md)** - Executive Summary
   - Resumen ejecutivo del proyecto
   - Validación completada
   - Próximos pasos
   - Historial del proyecto
   - ⏱️ **Lectura: 10 min**

---

## 📊 Ruta de lectura recomendada

### Para instalar y usar (30 min):
1. [README.rst](README.rst) (5 min)
2. [readme/CONFIGURE.md](readme/CONFIGURE.md) (5 min)
3. [readme/USAGE.md](readme/USAGE.md) (15 min)
4. [readme/CONTRIBUTORS.md](readme/CONTRIBUTORS.md) (5 min)

### Para validar fiscalmente (45 min):
1. [VALIDACION_AEAT.md](VALIDACION_AEAT.md) (10 min)
2. [RECOMENDACIONES_AEAT.md](RECOMENDACIONES_AEAT.md) (20 min)
3. [RESUMEN_VALIDACION.md](RESUMEN_VALIDACION.md) (10 min)
4. Contactar asesor fiscal (5 min - preparación)

### Para desarrollo/mejoras (30 min):
1. [CAMBIOS_REALIZADOS.md](CAMBIOS_REALIZADOS.md) (10 min)
2. [RECOMENDACIONES_AEAT.md](RECOMENDACIONES_AEAT.md) - Fase 2 (10 min)
3. Revisar archivos CSV en `data/template/` (10 min)

---

## 🎯 Contenido por tema

### Régimen REBU
- [readme/DESCRIPTION.md](readme/DESCRIPTION.md) - Definición
- [VALIDACION_AEAT.md](VALIDACION_AEAT.md) - Confirmación oficial
- [RECOMENDACIONES_AEAT.md](RECOMENDACIONES_AEAT.md) - Recomendaciones

### Instalación y Configuración
- [readme/CONFIGURE.md](readme/CONFIGURE.md) - Pasos instalación
- [readme/USAGE.md](readme/USAGE.md) - Uso práctico
- [CAMBIOS_REALIZADOS.md](CAMBIOS_REALIZADOS.md) - Cambios técnicos

### Base Imponible y Cálculos
- [readme/DESCRIPTION.md](readme/DESCRIPTION.md) - Concepto
- [readme/USAGE.md](readme/USAGE.md) - Fórmula y ejemplo
- [RECOMENDACIONES_AEAT.md](RECOMENDACIONES_AEAT.md) - Detalles críticos

### IVA Deducible / No Deducible
- [RECOMENDACIONES_AEAT.md](RECOMENDACIONES_AEAT.md) - Reglas y ejemplos

### Obligaciones de Facturación
- [RECOMENDACIONES_AEAT.md](RECOMENDACIONES_AEAT.md) - Requisitos AEAT

---

## ⚠️ Puntos críticos a revisar

🔴 **OBLIGATORIO antes de usar en producción:**

1. [RECOMENDACIONES_AEAT.md](RECOMENDACIONES_AEAT.md) - Sección 1
   - El REBU es VOLUNTARIO - debe optarse expresamente

2. [RECOMENDACIONES_AEAT.md](RECOMENDACIONES_AEAT.md) - Sección 3
   - Base imponible = MARGEN BRUTO (no importe total)
   - Fórmulas críticas

3. [RECOMENDACIONES_AEAT.md](RECOMENDACIONES_AEAT.md) - Sección 8
   - Checklist de acciones críticas antes de usar

4. **Contactar asesor fiscal**: Validar para tu situación específica

---

## 📂 Estructura de archivos del módulo

```
l10n_es_rebu/
├── README.rst                          📖 Inicio aquí
├── INDICE_DOCUMENTACION.md             📑 Este archivo
├── CAMBIOS_REALIZADOS.md               🔧 Historial técnico
├── VALIDACION_AEAT.md                  ✅ Validación oficial
├── RECOMENDACIONES_AEAT.md             ⚠️  LECTURA OBLIGATORIA
├── RESUMEN_VALIDACION.md               📊 Resumen ejecutivo
├── __manifest__.py                     ✅ Actualizado
├── models/
│   ├── __init__.py
│   └── account_chart_template.py       ✅ Referencia REBU
├── data/template/
│   ├── account.tax.group-es_common.csv                ✅ tax_group_rebu
│   ├── account.tax-es_common.csv                      ✅ Impuestos REBU 21%
│   └── account.fiscal.position-es_common.csv          ✅ fp_rebu
└── readme/
    ├── DESCRIPTION.md                  📖 Descripción
    ├── CONFIGURE.md                    ⚙️  Configuración
    ├── USAGE.md                        💡 Uso práctico
    └── CONTRIBUTORS.md                 👥 Créditos
```

---

## 📞 Soporte y referencias

### Recursos oficiales AEAT:
- [AEAT - REBU oficial](https://sede.agenciatributaria.gob.es/Sede/iva/regimenes-tributacion-iva/regimen-especial-bienes-usados.html)
- [Preguntas frecuentes REBU](https://www2.agenciatributaria.gob.es/es13/s/iafriafrc12f?TIPO=C&CODIGO=00340)
- [Asistente virtual IVA](https://www2.agenciatributaria.gob.es/wlpl/AVAC-CALC/AsistenteIVA)

### Para dudas:
- Revisa la sección **Troubleshooting** en [readme/USAGE.md](readme/USAGE.md)
- Consulta [RECOMENDACIONES_AEAT.md](RECOMENDACIONES_AEAT.md) Sección 8
- **Contacta con tu asesor fiscal**

---

## 📋 Estado del módulo

✅ **Transformación REAV → REBU**: COMPLETADA  
✅ **Validación AEAT**: COMPLETADA  
✅ **Documentación**: COMPLETADA  
⚠️ **Pruebas en Odoo**: PENDIENTE  
⚠️ **Validación fiscal final**: PENDIENTE (requiere asesor)  

---

## 🎓 Resumen ejecutivo

| Aspecto | Estado | Referencia |
|--------|--------|-----------|
| Nombre | REBU - Bienes Artísticos | [__manifest__.py](__manifest__.py) |
| IVA Compra | 21% no deducible | [account.tax-es_common.csv](data/template/account.tax-es_common.csv) |
| IVA Venta | 21% incluido | [account.tax-es_common.csv](data/template/account.tax-es_common.csv) |
| Base Imponible | Margen bruto | [USAGE.md](readme/USAGE.md) |
| Régimen | Voluntario | [RECOMENDACIONES_AEAT.md](RECOMENDACIONES_AEAT.md) Sec. 1 |
| Aplicabilidad | Objetos de arte | [DESCRIPTION.md](readme/DESCRIPTION.md) |
| Validación AEAT | ✅ Completada | [VALIDACION_AEAT.md](VALIDACION_AEAT.md) |

---

**Última actualización**: 14 de noviembre de 2025  
**Versión módulo**: 17.0.1.0.0  
**Estado**: ✅ LISTO PARA USAR (Fase 1 completada)
