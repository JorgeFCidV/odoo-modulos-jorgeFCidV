# Uso del módulo REBU

## Asignación de impuestos a productos

Una vez actualizado el plan contable (impuestos y posiciones fiscales), podremos asignar los impuestos REBU a los productos de nuestra empresa:

### Pasos para asignar impuestos a un producto:

1. **Acceder a la ficha del producto**
   - Ir a **Ventas** > **Productos** o **Compras** > **Productos**
   - Crear un nuevo producto o editar uno existente

2. **Asignar impuesto de venta (cliente)**
   - En la pestaña **Información General** o **Facturación**
   - En el campo **"Impuestos de cliente"** o **"Impuestos de venta"**
   - Asignar: **IVA Repercutido incluido REBU 21%**

3. **Asignar impuesto de compra (proveedor)**
   - En el campo **"Impuestos de proveedor"** o **"Impuestos de compra"**
   - Asignar: **IVA Soportado no deducible REBU 21%**

4. **Guardar los cambios**

## Asignación de posición fiscal a contactos

También podemos asignar la posición fiscal a los proveedores y clientes para cambiar automáticamente los impuestos en las facturas:

### Pasos para asignar posición fiscal a un contacto:

1. **Acceder a la ficha del contacto**
   - Ir a **Ventas** > **Clientes** o **Compras** > **Proveedores**
   - Crear un nuevo contacto o editar uno existente

2. **Asignar la posición fiscal**
   - En la pestaña **Facturación**
   - En el campo **"Posición fiscal"**
   - Asignar: **REBU - Bienes Usados Artísticos**

3. **Guardar los cambios**

## Funcionamiento en facturas

### Cálculo en facturas de venta

En el REBU, el IVA se calcula especialmente sobre el margen bruto:

```
Margen de beneficio = Precio venta (IVA incluido) - Precio compra (IVA incluido)
Base Imponible = (Margen × 100) ÷ (100 + tipo impositivo)
IVA a repercutir = Base Imponible × (tipo impositivo / 100)
```

**Ejemplo:**
- Precio de compra (con IVA): 1.000 €
- Precio de venta (con IVA): 1.500 €
- Margen de beneficio: 500 €
- Con IVA 21%: Base = (500 × 100) ÷ 121 = 413,22 €
- IVA: 413,22 × 0,21 = 86,78 €

### Facturas de venta
Cuando creas una factura de venta para un cliente con posición fiscal REBU:
- El impuesto aplicado será automáticamente **IVA Repercutido incluido REBU 21%**
- Este impuesto se calcula sobre el margen bruto de la operación

### Facturas de compra
Cuando creas una factura de compra de un proveedor:
- El impuesto aplicado será automáticamente **IVA Soportado no deducible REBU 21%**
- Este impuesto **no es deducible** en el régimen REBU (solo para los bienes revendidos)
- Otros gastos operativos (suministros, servicios, etc.) sí permiten deducción

## ⚠️ Consideraciones especiales

### Régimen voluntario
- El REBU es **opcional** - la empresa puede optar por el régimen general en cualquier momento
- Sin declaración expresa, se entiende que se aplica el régimen general

### Bienes aplicables
- El régimen REBU es exclusivo para empresas de compra-venta de bienes específicos
- Para bienes artísticos (tu caso), aplica correctamente
- Revisa la lista oficial de la AEAT si comercializas otros tipos de bienes

### Cálculo del margen
- El IVA se calcula sobre el **margen** (diferencia entre venta y compra), no sobre el importe total
- Esto supone una ventaja fiscal si el margen es pequeño

### Deducción de otros gastos
- Aunque el IVA de compra de bienes revendidos no se deduce
- **SÍ se deducen**: IVA en servicios, suministros, alquiler, teléfono, etc.

### Obligaciones de facturación
- Revisa las obligaciones especiales de facturación en REBU en la [AEAT](https://sede.agenciatributaria.gob.es/Sede/iva/regimenes-tributacion-iva/regimen-especial-bienes-usados/obligaciones-facturacion.html)
- Debe constar claramente en facturas que se aplica el régimen REBU

### Consultar con asesor fiscal
- Es **recomendable** revisar la documentación de la AEAT para comprender completamente el régimen
- **Consulta con un asesor fiscal** para asegurar la correcta aplicación del régimen en tu empresa
- Cada situación puede tener variaciones según procedencia, tipo de arte, etc.

## Troubleshooting

### Los impuestos no se aplican correctamente
1. Verifica que has instalado el módulo correctamente
2. Comprueba que has recargado la localización fiscal
3. Asegúrate de que asignaste la posición fiscal al contacto

### Necesito más tipos de IVA
Si comercializas con otros bienes (libros, antiguedades, etc.) que usan otros tipos de IVA, puedes:
1. Crear impuestos adicionales REBU con otros porcentajes
2. Usar posiciones fiscales adicionales
3. Contactar con soporte

