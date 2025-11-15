# Validación según AEAT - REBU

## Información Oficial de la AEAT

Fuente: https://sede.agenciatributaria.gob.es/Sede/iva/regimenes-tributacion-iva/regimen-especial-bienes-usados.html

### ¿En qué consiste el REBU?

Es un **régimen voluntario** aplicable a las entregas de determinados bienes efectuadas por los **revendedores** 
cuando intervengan en nombre propio, donde la base imponible se determina de forma especial.

### Bienes que aplican REBU

El REBU se aplica a:

1. **Bienes Usados**
   - Bienes muebles utilizados por un tercero
   - Susceptibles de reutilización
   - Adquiridos para reventa
   - NO incluye: bienes renovados/transformados por el vendedor, materiales de recuperación, envases, embalajes, oro, platino, piedras preciosas

2. **Objetos de arte** ⭐ (TU CASO)
   - Cuadros, pinturas, dibujos, grabados, estampas, litografías
   - Esculturas, estatuas, vaciados de esculturas
   - Tapicerías, textiles, murales, cerámica, esmaltes sobre cobre
   - Fotografías (con requisitos específicos del art. 136 LIVA)

3. **Antigüedades**
   - Bienes muebles con más de 100 años de antigüedad
   - No sean objetos de arte o de colección

4. **Objetos de colección**
   - Artículos de filatelia
   - Colecciones de zoología, botánica, mineralogía, anatomía
   - Interés histórico, arqueológico, paleontológico, etnográfico, numismático

**EXCLUSIÓN IMPORTANTE:** No aplica a oro de inversión

---

## Tipos de IVA en Compras REBU

### 📌 IMPORTANTE (Actualizado 15 Nov 2025)

No existe un único tipo de IVA para compras REBU. Depende del **origen de la compra**:

### Compra 1: Adquisición a Particular (**0% IVA**)

**Características**:
- Compra de obra de arte a **persona física** (no sujeto pasivo del IVA)
- El particular NO emite factura con IVA
- Ejemplo: Compra cuadro a coleccionista jubilado

**IVA**:
- 0% (no existe IVA en la transacción)
- No deducible (porque no existe IVA a deducir)

**Configuración Odoo**:
- Posición fiscal: "REBU - Compra a Particular (0%)"
- Impuesto: "IVA Soportado no deducible REBU 0%"

### Compra 2: Adquisición Directa a Artista Original (**10% IVA NO DEDUCIBLE**)

**Características**:
- Compra de obra **original del artista** (persona física o profesional)
- Artista emite factura con **IVA 10% reducido**
- Este IVA 10% **NO es deducible** bajo régimen REBU
- Ejemplo: Compra cuadro original a pintor profesional

**IVA**:
- 10% (IVA reducido para creadores)
- 0% deducible (no deducible en REBU)

**Configuración Odoo**:
- Posición fiscal: "REBU - Compra a Artista Original (10%)"
- Impuesto: "IVA Soportado no deducible REBU 10%"

### Venta: Entregas a Cliente (**21% IVA REPERCUTIDO**)

**Características**:
- Venta a **cliente final** (galería, coleccionista, inversor)
- Se aplica IVA 21% repercutido incluido
- Aplica a **TODAS las ventas** bajo régimen REBU
- Ejemplo: Venta a galería o coleccionista

**IVA**:
- 21% repercutido incluido
- Deducible: Sí (se aplica sobre margen)

**Configuración Odoo**:
- Posición fiscal: "REBU - Bienes Usados Artísticos (Venta 21%)"
- Impuesto: "IVA Repercutido incluido REBU 21%"

---

## Funcionamiento del REBU

### Sistema 1: Operación por operación (TU CASO - RECOMENDADO)

**Base Imponible = Margen de beneficio (sin IVA)**

```
Margen de beneficio = Precio venta (IVA incluido) - Precio compra (IVA incluido)

Base Imponible = (Margen de beneficio × 100) ÷ (100 + tipo impositivo)
```

**Impuestos:**
- ✅ Repercute IVA en las ventas aplicando el **tipo impositivo correspondiente al bien** sobre el margen
- ❌ **IVA soportado en las compras NO es deducible** (excepto otros gastos como teléfono, alquileres, etc.)

### Sistema 2: Margen de beneficio global

Se aplica previa opción, periódicamente, con regularización anual de existencias.
No aplica a bienes artísticos en general, solo a:
- Sellos, efectos timbrados, billetes, monedas
- Discos, cintas magnéticas, soportes
- Libros, revistas, publicaciones
- Bienes autorizados por AEAT

---

## ⚠️ CONSIDERACIONES IMPORTANTES

### Tipo de IVA
- **El régimen REBU NO ESPECIFICA UN ÚNICO TIPO DE IVA**
- **Aplica el tipo impositivo correspondiente al bien** (4%, 10%, 21%, etc.)
- En tu caso (bienes artísticos), generalmente es **21%**

### IVA no deducible
- El IVA soportado en las compras de bienes para reventa **NO se deduce**
- Solo se deducen otros gastos operativos (electricidad, teléfono, alquileres, etc.)

### Base imponible
- Se calcula sobre el **margen bruto** (diferencia entre venta y compra)
- No sobre el importe total

### Régimen voluntario
- Es **opcional** - el vendedor puede renunciar
- Sin comunicación expresa, pueden aplicar régimen general (IVA total deducible)

---

## Validación del módulo actual

### ✅ CORRECTO
- [x] Impuesto del 21% (válido para bienes artísticos)
- [x] IVA no deducible en compras
- [x] IVA incluido en ventas
- [x] Orientado a bienes artísticos

### 📝 OBSERVACIONES
- La documentación AEAT no especifica un único tipo de IVA para REBU
- El régimen permite aplicar el tipo impositivo del bien
- Para bienes artísticos (tu caso), el 21% es correcto

### 💡 SUGERENCIAS DE MEJORA
1. Añadir información sobre que es un régimen voluntario
2. Mencionar que IVA no deducible aplica solo al IVA de compras de bienes revendidos
3. Documentar que otros gastos SÍ permiten deducción
4. Añadir ejemplos de cálculo del margen

---

## Próximos pasos

1. ✅ Validar con tu asesor fiscal que el 21% es correcto para tu tipo específico de arte
2. ✅ Documentar el procedimiento de cálculo del margen en Odoo
3. ✅ Considerar si necesitas múltiples tipos de IVA (4%, 10%, 21%)
4. ✅ Validar obligaciones de facturación especiales en REBU
