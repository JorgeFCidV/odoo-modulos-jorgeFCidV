# Recomendaciones según AEAT para REBU

Basado en la documentación oficial de la AEAT sobre REBU: 
https://sede.agenciatributaria.gob.es/Sede/iva/regimenes-tributacion-iva/regimen-especial-bienes-usados.html

---

## 1. Opcionalidad del Régimen (IMPORTANTE)

### ⚠️ El REBU es VOLUNTARIO

- La empresa **debe optar expresamente** por el régimen REBU
- Sin optación expresa, se aplica el **régimen general** de IVA
- La optación puede renunciarse pero no antes de finalizar el año siguiente a su inicio

### Acción recomendada:
```
Documento oficial requerido: Comunicación a AEAT de opción por régimen REBU
En Odoo: Crear un campo de "Estado de régimen" (opcional/general/rebu)
```

---

## 2. Bienes que Aplican (REBU + Bienes Artísticos)

### ✅ Incluidos en REBU para bienes artísticos:
- Cuadros y pinturas
- Dibujos, grabados, estampas, litografías
- Esculturas, estatuas, vaciados de esculturas
- Tapicerías, textiles, murales
- Cerámica, esmaltes sobre cobre
- Fotografías originales (art. 136 LIVA)

### ❌ Excluidos:
- Oro de inversión
- Bienes renovados/transformados por el vendedor
- Materiales de recuperación, envases, embalajes

### ⚠️ Casos especiales:
- Réplicas o copias → Revisa si aplica REBU
- Litografías numeradas → Generalmente sí aplican
- Arte digital/moderno → Consultar AEAT

### Acción recomendada:
```
En Odoo:
1. Crear categoría de producto "Bienes Artísticos REBU"
2. Documentar tipo de bien en cada producto
3. Generar reportes de productos REBU vs no-REBU
```

---

## 3. Base Imponible = MARGEN BRUTO (CRÍTICO)

### Fórmula según AEAT:

```
Margen de beneficio = Precio de venta (IVA incluido) - Precio de compra (IVA incluido)

Base Imponible = (Margen de beneficio × 100) ÷ (100 + tipo impositivo)
```

### Ejemplo con 21% IVA:
```
Compra: 1.000 € (IVA incluido)
Venta:  1.500 € (IVA incluido)
Margen: 500 €

BI = (500 × 100) ÷ 121 = 413,22 €
IVA = 413,22 € × 0,21 = 86,78 €
```

### ⚠️ Puntos críticos en Odoo:

1. **Precios con IVA**
   - El módulo debe incluir IVA en precios de compra Y venta
   - Verificar configuración de precios sin IVA vs. con IVA

2. **Cálculo del margen**
   - Margen = Precio venta total - Precio compra total
   - No es margen por unidad, sino por operación completa
   - Margen NEGATIVO = Base = 0, se arrastra al período siguiente

3. **Documentación contable**
   - Registrar precio compra y precio venta claramente
   - Guardar evidencia de márgenes para auditoría

### Acción recomendada:
```
En Odoo:
1. ✅ Módulo REBU actual: Correcto (impuestos sobre 0%)
   - Esto obliga a calcular manualmente el margen

2. Mejora futura: Crear campo en factura para:
   - Precio compra documentado
   - Margen calculado automáticamente
   - BI = Margen × 100 ÷ 121
   - IVA = BI × 0,21

3. Generar reportes de:
   - Márgenes por operación
   - Márgenes acumulados por período
```

---

## 4. IVA Soportado NO Deducible (IMPORTANTE)

### Regla general en REBU:
```
❌ IVA de compra de bienes para reventa → NO deducible
✅ IVA de otros gastos → SÍ deducible
```

### Ejemplos:
```
NO deducible:
- IVA en compra de cuadro a marchante italiano
- IVA en compra de escultura para reventa

SÍ deducible (otros gastos operativos):
- IVA en seguros
- IVA en alquiler del local
- IVA en servicios profesionales
- IVA en suministros
- IVA en teléfono, electricidad
```

### ⚠️ Implementación en Odoo:

El módulo actual **no diferencia** entre IVA de bienes revendidos y otros gastos.

### Acción recomendada:
```
En Odoo:
1. Crear dos líneas de IVA por factura de compra:
   - Línea 1: Bienes para reventa (0% deducible)
   - Línea 2: Otros gastos operativos (21% deducible)

2. Asignar correctamente en facturas:
   - Artículos de arte → Impuesto REBU no deducible
   - Servicios, suministros → Impuesto general deducible

3. Generar reportes de:
   - IVA deducible vs. no deducible
   - Reclasificación de gastos
```

---

## 4.1 Tipos de IVA en Compras REBU (IMPORTANTE - NUEVAS OPCIONES)

### Caso Real 1: Compra a Particular (0% IVA)

**Situación**:
- Adquisición de obra de arte de un **particular** (persona física)
- El particular no es sujeto pasivo del IVA
- No existe factura o factura sin IVA

**Características**:
- IVA: 0% (no hay IVA en la transacción)
- Documentación: Contrato privado, recibí, etc.
- Ejemplo: Comprar cuadro a jubilado coleccionista

**Configuración en Odoo**:
```
Posición fiscal proveedor: "REBU - Compra a Particular (0%)"
Impuesto asignado: "IVA Soportado no deducible REBU 0%"
```

**Ejemplo de cálculo**:
```
Precio compra: 1.000 €
IVA: 0 € (particular sin IVA)
Total a pagar: 1.000 €

Venta posterior: 1.500 €
Margen: 500 €
BI = (500 × 100) ÷ 121 = 413,22 €
IVA venta: 413,22 × 0,21 = 86,78 €
```

### Caso Real 2: Compra Directa a Artista Original (10% IVA NO DEDUCIBLE)

**Situación**:
- Adquisición de obra **original directamente del artista**
- Artista emite factura con IVA reducido del 10%
- IVA 10% **NO es deducible** en régimen REBU

**Características**:
- IVA: 10% (IVA reducido para creadores)
- Deducibilidad: 0% (no deducible en REBU)
- Documentación: Factura del artista con IVA 10%
- Ejemplo: Comprar cuadro original a pintor profesional

**Configuración en Odoo**:
```
Posición fiscal proveedor: "REBU - Compra a Artista Original (10%)"
Impuesto asignado: "IVA Soportado no deducible REBU 10%"
```

**Ejemplo de cálculo**:
```
Precio base compra: 1.000 €
IVA (10% no deducible): 100 €
Total a pagar: 1.100 €

Venta posterior: 1.500 €
Margen: 500 € (diferencia de precios con IVA)
BI = (500 × 100) ÷ 121 = 413,22 €
IVA venta: 413,22 × 0,21 = 86,78 €
```

### Caso Real 3: Venta a Cliente (21% IVA REPERCUTIDO - SIN CAMBIOS)

**Situación**:
- Venta de obra a **cliente final** (galería, coleccionista, inversor)
- Aplica IVA 21% repercutido incluido
- **Esta situación NO cambia**

**Características**:
- IVA: 21% repercutido incluido
- Deducibilidad: 100% deducible (sobre margen)
- Documentación: Factura cliente con IVA 21%
- Ejemplo: Vender cuadro a galería

**Configuración en Odoo**:
```
Posición fiscal cliente: "REBU - Bienes Usados Artísticos (Venta 21%)"
Impuesto asignado: "IVA Repercutido incluido REBU 21%"
```

---

## 5. Obligaciones de Facturación Especiales

### Requisitos AEAT:

Las facturas bajo régimen REBU **DEBEN constar claramente** que se aplica el régimen.

### ⚠️ En Odoo:
```
Acción recomendada:

1. Añadir campo "Aplicar REBU" en factura
   - [ ] Régimen general
   - [x] Régimen especial REBU

2. En pie de factura o referencia:
   "Operación acogida al Régimen Especial de Bienes Usados"

3. Incluir en líneas:
   - Descripción del bien artístico
   - Precio de compra (si se conoce)
   - Precio de venta
   - Margen calculado
```

### Documentación a revisar:
- [Obligaciones de facturación REBU en AEAT](https://sede.agenciatributaria.gob.es/Sede/iva/regimenes-tributacion-iva/regimen-especial-bienes-usados/obligaciones-facturacion.html)

---

## 6. Otras Consideraciones

### Régimen global alternativo
- REBU permite calcular base imponible de forma global (periódica)
- **NO aplica a bienes artísticos**, solo a: sellos, monedas, libros, discos
- Tu configuración (operación por operación) es la correcta

### Regularización de existencias
- Si optas por método global: regularización anual
- Tu método (operación por operación): no requiere

### Cambio de régimen
- Puedes cambiar de régimen dentro del año natural
- Pero si optas por REBU, no puedes renunciar hasta fin del año siguiente

---

## 7. Checklist para Implementar en Odoo

### Fase 1: Configuración Base (✅ ACTUALIZADA 15 NOV 2025)
- [x] Impuesto 0% REBU no deducible para compra a particular
- [x] Impuesto 10% REBU no deducible para compra a artista
- [x] Impuesto 21% REBU incluido en ventas
- [x] Posición fiscal REBU Particular (0%)
- [x] Posición fiscal REBU Artista (10%)
- [x] Posición fiscal REBU Venta (21%)
- [x] Documentación actualizada

### Fase 2: Mejoras Recomendadas
- [ ] Campo "Régimen aplicado" en factura (general/REBU)
- [ ] Campo "Bienes artísticos REBU" en producto
- [ ] Etiqueta en factura "Régimen REBU"
- [ ] Campos para documentar precio compra/venta
- [ ] Cálculo automático de margen

### Fase 3: Reportes y Auditoría
- [ ] Reporte de operaciones bajo REBU
- [ ] Análisis de márgenes por período
- [ ] Segregación IVA deducible vs. no deducible
- [ ] Exportación para auditoría fiscal

### Fase 4: Cumplimiento Legal
- [ ] Documentar optación por REBU en empresa
- [ ] Revisar obligaciones de facturación
- [ ] Crear procedimiento de renuncia (si aplica)
- [ ] Validar con asesor fiscal

---

## 8. Próximas Acciones Críticas

### ANTES de usar en producción:
1. ⚠️ **Consulta con asesor fiscal** personal
2. ⚠️ **Opción formal por REBU** ante AEAT
3. ⚠️ **Validar precios**: ¿incluyen IVA o no?
4. ⚠️ **Revisar obligaciones**: Facturación, registros, etc.

### DURANTE la operación:
1. Documentar cada operación (compra/venta)
2. Mantener evidencia de márgenes
3. Segregar IVA deducible vs. no deducible
4. Generar reportes de auditoría

### ASESORAMIENTO:
- Contactar: Asesor fiscal / Gestoría
- Referencias AEAT: INFORMA (preguntas frecuentes REBU)
- Asistente virtual IVA: https://www2.agenciatributaria.gob.es/wlpl/AVAC-CALC/AsistenteIVA

---

## 9. Disclaimers Importantes

⚠️ **Este módulo proporciona la estructura contable**, pero NO garantiza cumplimiento fiscal.

⚠️ **Cada empresa es diferente**: 
- Procedencia de bienes (UE, importación, etc.)
- Tipo específico de arte
- Actividades complementarias
- Situación particular

⚠️ **Consulta obligatoria**: Contacta con tu **asesor fiscal** ANTES de implementar.

⚠️ **Responsabilidad**: La AEAT puede requerir ajustes según interpretación del régimen.

