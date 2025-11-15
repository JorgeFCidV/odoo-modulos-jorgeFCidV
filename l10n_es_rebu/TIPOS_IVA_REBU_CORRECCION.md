# CORRECCIÓN: TIPOS DE IVA EN COMPRAS REBU

**Fecha**: 15 de noviembre de 2025  
**Status**: Análisis de cambios necesarios  
**Impacto**: Recalibración de estructura de impuestos

---

## 📋 Problema Identificado

La configuración actual del módulo REBU asume **un único tipo de IVA (21%) para compras**, pero la realidad fiscal en España muestra **dos casos distintos** dependiendo del origen de la compra:

### Casos Reales de Compra REBU

#### Caso 1: Compra a Particular (**0% IVA**)
- **Descripción**: Adquirir obra de arte de un particular (persona física no sujeta a IVA)
- **IVA**: 0% (no hay IVA en la compra)
- **Por qué**: La persona particular no factura IVA
- **Ejemplo**: Compra cuadro a jubilado coleccionista privado

#### Caso 2: Compra a Artista Directo (**10% IVA no deducible**)
- **Descripción**: Adquirir obra original directamente del artista
- **IVA**: 10% no deducible
- **Por qué**: Artista produce la obra (aplica IVA 10% reducido) pero en régimen REBU este IVA no es deducible
- **Ejemplo**: Compra obra original a pintor profesional

#### Caso 3: Venta al Cliente (**21% IVA**)
- **Descripción**: Vender obra de arte a cliente (galería, coleccionista, inversor)
- **IVA**: 21% repercutido incluido
- **Aplicación**: En todas las ventas bajo régimen REBU
- **Ejemplo**: Venta cuadro a galería, coleccionista o inversor

---

## 🔧 Cambios Necesarios

### En Archivos de Datos

#### 1. account.tax-es_common.csv
**Cambios**:
- ❌ Eliminar: `account_tax_template_p_rebu0` (21% - que ya existe)
- ✅ Crear: `account_tax_template_p_rebu0_particular` (0% - sin IVA)
- ✅ Crear: `account_tax_template_p_rebu0_artista` (10% - IVA no deducible)
- ✅ Mantener: `account_tax_template_s_rebu0` (21% - venta, SIN cambios)

#### 2. account.fiscal.position-es_common.csv
**Cambios**:
- Actualizar mapeos para asociar el impuesto correcto según:
  - Contacto proveedor = Particular → Usar 0%
  - Contacto proveedor = Artista → Usar 10%
  - Todos los clientes → Usar 21% en venta

#### 3. __manifest__.py
**Cambios**:
- ⚠️ CRÍTICO: El campo `data: []` está vacío (ya identificado como Error 1)
- Debe incluir rutas de CSV para que se importen los impuestos

#### 4. README.rst
**Cambios**:
- Actualizar sección "Usage" con los dos tipos de IVA en compra
- Añadir explicación de cuándo usar cada uno
- Ejemplos de configuración por tipo de proveedor

---

## 📊 Comparativa Antes vs Después

### ANTES (Actual - Incorrecto)
```
COMPRA:  21% IVA no deducible (solo una opción)
VENTA:   21% IVA repercutido (correcto)
```

### DESPUÉS (Correcto)
```
COMPRA A PARTICULAR:  0% IVA (sin IVA en la compra)
COMPRA A ARTISTA:     10% IVA no deducible
VENTA:                21% IVA repercutido (sin cambios)
```

---

## 💰 Impacto Financiero de la Corrección

### Ejemplo: Compra a Particular vs Artista

**ANTES (Incorrecto)**:
```
Compra obra a particular por 1.000€
IVA calculado (21%): 210€ ❌ (no debería haber IVA)
Total pagado: 1.210€ ❌ INCORRECTO
```

**DESPUÉS (Correcto - Compra a Particular)**:
```
Compra obra a particular por 1.000€
IVA: 0€ (el particular no factura IVA)
Total pagado: 1.000€ ✅ CORRECTO
AHORRO: 210€
```

**DESPUÉS (Correcto - Compra a Artista)**:
```
Compra obra a artista por 1.000€ (precio base)
IVA (10% no deducible): 100€
Total pagado: 1.100€
Margen después (sin deducir IVA): Se aplica a base imponible
```

---

## 🔄 Configuración por Tipo de Proveedor

### Para Proveedores Particulares
1. Ir a contacto proveedor
2. Campo "Posición fiscal": **REBU - Particular (0%)**
3. Las compras usarán 0% IVA

### Para Proveedores Artistas
1. Ir a contacto proveedor
2. Campo "Posición fiscal": **REBU - Artista Original (10% no deducible)**
3. Las compras usarán 10% IVA no deducible

### Para Todos los Clientes
1. Ir a contacto cliente
2. Campo "Posición fiscal": **REBU - Bienes Usados Artísticos**
3. Las ventas usarán 21% IVA repercutido (SIN CAMBIOS)

---

## 🎯 Archivos a Actualizar

### 1. DATOS (Crítico)
- [ ] `data/template/account.tax-es_common.csv`
  - Crear: Impuesto 0% particular
  - Crear: Impuesto 10% artista
  - Verificar: Impuesto 21% venta existente

- [ ] `data/template/account.fiscal.position-es_common.csv`
  - Crear: Posición fiscal para particular (0%)
  - Crear: Posición fiscal para artista (10%)
  - Mantener: Posición fiscal venta (21%)

### 2. DOCUMENTACIÓN (Alto)
- [ ] `README.rst` - Actualizar sección Usage
- [ ] `RECOMENDACIONES_AEAT.md` - Añadir nuevos casos
- [ ] `VALIDACION_AEAT.md` - Documentar los dos casos

### 3. ESPECIFICACIÓN (Medio)
- [ ] `ESPECIFICACION_MARGEN_AUTOMATICO_REBU.md` - Ejemplos con 0% y 10%
- [ ] `ESPECIFICACION_FACTURACION_REBU_ESPECIAL.md` - Actualizar casos
- [ ] `PLAN_IMPLEMENTACION_FASE_2.md` - Considerar múltiples tipos IVA

### 4. CONFIGURACIÓN (Medio)
- [ ] `__manifest__.py` - Corregir campo `data: []` vacío (Error 1 previo)

---

## 📝 Definición de Posiciones Fiscales

Necesitaremos 3 posiciones fiscales (actualizado):

### 1. REBU - Particular (0% - Compra)
```
Nombre: REBU - Particular
Descripción: Compra a particular sin IVA
De país: España
A país: España
Aplicación: Compra
Mapeo impuestos: IVA 0% → 0% No Deducible REBU
```

### 2. REBU - Artista Original (10% - Compra)
```
Nombre: REBU - Artista Original
Descripción: Compra a artista con IVA 10% no deducible
De país: España
A país: España
Aplicación: Compra
Mapeo impuestos: IVA 10% → 10% No Deducible REBU
```

### 3. REBU - Bienes Usados Artísticos (21% - Venta) [EXISTENTE]
```
Nombre: REBU - Bienes Usados Artísticos
Descripción: Venta con IVA 21% repercutido incluido
De país: España
A país: España
Aplicación: Venta
Mapeo impuestos: IVA 21% → 21% Repercutido REBU
```

---

## ✅ Checklist de Implementación

### Fase 1: Datos
- [ ] Crear impuesto 0% no deducible REBU (particular)
- [ ] Crear impuesto 10% no deducible REBU (artista)
- [ ] Crear posición fiscal para particular
- [ ] Crear posición fiscal para artista
- [ ] Verificar CSV syntax correcto
- [ ] Testar carga de impuestos en Odoo

### Fase 2: Documentación
- [ ] Actualizar README.rst
- [ ] Actualizar VALIDACION_AEAT.md
- [ ] Actualizar RECOMENDACIONES_AEAT.md
- [ ] Crear documento TIPOS_IVA_REBU.md (este archivo)
- [ ] Actualizar ejemplos en especificaciones

### Fase 3: Validación
- [ ] Testar cada tipo de impuesto
- [ ] Validar cálculo margen con 0%, 10%, 21%
- [ ] Verificar campos de posición fiscal
- [ ] Confirmar con asesor fiscal

### Fase 4: Pruebas (Fase 2)
- [ ] Actualizar tests para validar 3 tipos IVA
- [ ] Añadir casos de prueba: 0%, 10%, 21%
- [ ] Verificar matrices de trazabilidad AEAT

---

## 🚀 Orden de Ejecución Recomendado

1. **Hoy**: Crear este documento de análisis
2. **Hoy**: Actualizar CSV de impuestos (crear 0% y 10%)
3. **Hoy**: Actualizar README.rst con nuevos casos
4. **Mañana**: Actualizar posiciones fiscales CSV
5. **Mañana**: Actualizar documentación AEAT
6. **Mañana**: Corregir Error 1 (__manifest__.py)
7. **Esta semana**: Testar en Odoo
8. **Esta semana**: Validar con asesor fiscal

---

## 📚 Referencias Externas

### AEAT Oficial
- Régimen REBU: https://sede.agenciatributaria.gob.es/
- Búsqueda: "Régimen Especial de Bienes Usados" + "IVA"
- Consultar específicamente sobre:
  - Compra a particular (0% típicamente)
  - Compra a artista original (10% no deducible típicamente)

---

**Preparado por**: GitHub Copilot  
**Fecha**: 15 de noviembre de 2025  
**Status**: 🔴 PENDIENTE DE IMPLEMENTACIÓN  
**Impacto**: Crítico - Afecta a toda la estructura de impuestos
