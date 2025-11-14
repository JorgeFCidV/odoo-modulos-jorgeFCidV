# Descripción

## REBU - Régimen Especial de Bienes Usados (Bienes Artísticos)

Este módulo de localización española para Odoo 17 implementa el **Régimen Especial de Bienes Usados (REBU)** 
específicamente orientado a **bienes artísticos**.

## ¿A quién va dirigido?

El régimen REBU para bienes artísticos es aplicable a:

- **Galerías de arte**
- **Marchantes de arte**
- **Comerciantes de bienes artísticos**
- Empresas dedicadas a la **compra-venta de arte**

## ¿Qué es el REBU?

El REBU es un **régimen voluntario** de IVA que aplica a las entregas de:

- **Objetos de arte:** Cuadros, pinturas, dibujos, grabados, esculturas, etc.
- **Bienes usados:** Bienes muebles de segunda mano
- **Antigüedades:** Bienes con más de 100 años
- **Objetos de colección:** Filatelia, numismática, etc.

Fuente: [AEAT - Régimen Especial de Bienes Usados](https://sede.agenciatributaria.gob.es/Sede/iva/regimenes-tributacion-iva/regimen-especial-bienes-usados.html)

## Características fiscales del REBU

### Base Imponible Especial

En el REBU, el **IVA se calcula sobre el margen bruto**, no sobre el importe total:

```
Margen de beneficio = Precio venta (IVA incluido) - Precio compra (IVA incluido)

Base Imponible = (Margen de beneficio × 100) ÷ (100 + tipo impositivo)
```

### IVA Soportado No Deducible

- El **IVA en las compras de bienes para reventa NO es deducible**
- Sí son deducibles otros gastos operativos (electricidad, teléfono, alquileres, etc.)

### Tipo Impositivo

- El régimen REBU aplica el **tipo impositivo correspondiente al bien**
- Para bienes artísticos generalmente es del **21%**
- Otros tipos (4%, 10%) aplican según características del bien

## Impuestos incluidos en el módulo

El módulo proporciona:

- **IVA Repercutido incluido REBU 21%**: Impuesto a aplicar en la venta de bienes artísticos
- **IVA Soportado no deducible REBU 21%**: Impuesto a aplicar en la compra de bienes artísticos

## Posiciones fiscales

- **REBU - Bienes Usados Artísticos**: Posición fiscal que convierte automáticamente los impuestos estándar al régimen REBU

## Consideraciones importantes

- ⚠️ **Régimen voluntario**: La empresa puede optar por este régimen o el régimen general
- ⚠️ **Solo bienes específicos**: No todos los artículos aplican (ej: oro de inversión excluido)
- ⚠️ **Cálculo especial**: Requiere gestión del margen bruto, no del total
- ⚠️ **Obligaciones especiales**: Revisa obligaciones de facturación en la AEAT

## Disclaimer

Este módulo proporciona la estructura contable para el REBU. Se recomienda validar con un **asesor fiscal** 
que la configuración es correcta para tu caso específico, ya que hay variaciones según el tipo de arte y 
procedencia de los bienes.
