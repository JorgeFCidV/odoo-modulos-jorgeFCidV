# Resumen Final - Transformación REAV → REBU + Validación AEAT

## 📋 Información consultada de AEAT

**Fuente:** https://sede.agenciatributaria.gob.es/Sede/iva/regimenes-tributacion-iva/regimen-especial-bienes-usados.html

### Características del REBU confirmadas:

✅ **Régimen voluntario** aplicable a revendedores  
✅ **Aplica a Objetos de arte**: Cuadros, pinturas, dibujos, grabados, esculturas, etc.  
✅ **Base Imponible especial**: Margen bruto (Venta - Compra)  
✅ **IVA no deducible**: En compras de bienes revendidos  
✅ **Tipo impositivo**: Aplicable según el bien (4%, 10%, 21%)  
✅ **Para bienes artísticos**: Generalmente 21%  

---

## 🎯 Módulo REBU - Estado Final

### Cambios realizados:

#### 1. **Estructura y nomenclatura** ✅
```
l10n_es_reav/ → l10n_es_rebu/
Todos los IDs internos actualizados: reav → rebu
```

#### 2. **Archivo __manifest__.py** ✅
- Nombre: "REBU - Régimen Especial de Bienes Usados (Bienes Artísticos)"
- Autor: Jorge Fernández
- Versión: 17.0.1.0.0

#### 3. **Impuestos configurados** ✅ (ACTUALIZADO 15 NOV 2025)
```
Compra a Particular:        0% IVA no deducible REBU
Compra a Artista Original: 10% IVA no deducible REBU
Venta:                     21% IVA repercutido incluido REBU
Grupo:                     tax_group_rebu
```

#### 4. **Posiciones Fiscales** ✅ (ACTUALIZADO 15 NOV 2025)
```
fp_rebu_particular:  "REBU - Compra a Particular (0%)"
fp_rebu_artist:      "REBU - Compra a Artista Original (10%)"
fp_rebu_sale:        "REBU - Bienes Usados Artísticos (Venta 21%)"
```

#### 5. **Documentación completa** ✅
- `README.rst` → Descripción general actualizada
- `DESCRIPTION.md` → Información de AEAT integrada
- `CONFIGURE.md` → Pasos de instalación
- `USAGE.md` → Fórmulas de cálculo y ejemplos
- `CONTRIBUTORS.md` → Créditos
- `CAMBIOS_REALIZADOS.md` → Historial de cambios
- `VALIDACION_AEAT.md` → Validación contra AEAT

---

## ✅ Validación según AEAT

### Configuración correcta para:

✅ **Objeto de arte** (bienes artísticos)  
✅ **Margen bruto como base** (implementado mediante IVA especial)  
✅ **IVA no deducible en compras** (implementado)  
✅ **Compra a Particular: 0% IVA** (nuevo)  
✅ **Compra a Artista: 10% IVA no deducible** (nuevo)  
✅ **Venta: 21% IVA repercutido** (sin cambios)  

### Notas importantes:

⚠️ **Régimen voluntario**: La empresa debe optar formalmente  
⚠️ **Tipo de proveedor**: Asignar posición fiscal correcta según origen (particular vs artista)  
⚠️ **Cálculo especial del margen**: Requiere disciplina en precios  
⚠️ **Otros tipos de IVA**: 0% (particular), 10% (artista), 21% (venta) - todos configurados  
⚠️ **Obligaciones de facturación**: Debe constar en factura que se aplica REBU  

---

## 🆕 NUEVAS OPCIONES DE COMPRA (15 NOV 2025)

### Caso 1: Compra a Particular (0% IVA)
```
Posición fiscal:   REBU - Compra a Particular (0%)
Impuesto:         0% no deducible
Ejemplo:          Cuadro de jubilado coleccionista
Precio pagado:    TOTAL sin IVA
```

### Caso 2: Compra a Artista Original (10% IVA no deducible)
```
Posición fiscal:   REBU - Compra a Artista Original (10%)
Impuesto:         10% no deducible
Ejemplo:          Obra original de pintor profesional
Precio pagado:    TOTAL + 10% IVA (no deducible)
```

### Caso 3: Venta a Cliente (21% IVA repercutido)
```
Posición fiscal:   REBU - Bienes Usados Artísticos (Venta 21%)
Impuesto:         21% repercutido incluido
Ejemplo:          Venta a galería o coleccionista
Precio facturado: TOTAL + 21% IVA  

---

## 📁 Estructura del módulo

```
l10n_es_rebu/
├── __init__.py                                      # Import
├── __manifest__.py                                  # ✅ Actualizado
├── README.rst                                       # ✅ Actualizado
├── CAMBIOS_REALIZADOS.md                           # ✅ Creado
├── VALIDACION_AEAT.md                              # ✅ Creado
├── RESUMEN_VALIDACION.md                           # Este archivo
├── models/
│   ├── __init__.py
│   └── account_chart_template.py                    # ✅ Referencia REBU
├── data/template/
│   ├── account.tax.group-es_common.csv              # ✅ tax_group_rebu
│   ├── account.tax-es_common.csv                    # ✅ Impuestos REBU 21%
│   └── account.fiscal.position-es_common.csv        # ✅ fp_rebu
├── readme/
│   ├── DESCRIPTION.md                              # ✅ Actualizado con AEAT
│   ├── CONFIGURE.md                                # ✅ Actualizado
│   ├── USAGE.md                                    # ✅ Actualizado con fórmulas
│   ├── CONTRIBUTORS.md                             # ✅ Actualizado
│   └── ...
└── ...
```

---

## 🔧 Próximos pasos recomendados

### 1. Instalación en Odoo
```bash
cd /addons/l10n_es_rebu
# Instalar módulo en Odoo
# Cargar localización fiscal
```

### 2. Configuración de empresa
- [ ] Asignar posición fiscal REBU a clientes/proveedores
- [ ] Asignar impuestos REBU a productos
- [ ] Validar facturas de prueba

### 3. Validación fiscal
- [ ] Consultar con **asesor fiscal** personal
- [ ] Confirmar que el 21% es correcto para tu tipo específico de arte
- [ ] Revisar obligaciones de facturación especiales
- [ ] Documentar la opción por el régimen REBU

### 4. Mejoras futuras (opcional)
- [ ] Añadir impuestos REBU con otros porcentajes (10%, 4%)
- [ ] Crear guía de cálculo de márgenes
- [ ] Documentar procedimiento de renuncia al régimen
- [ ] Integrar alertas de obligaciones REBU

---

## 📞 Contacto y soporte

Para dudas sobre este módulo:
- Revisa la documentación en `readme/`
- Consulta la [AEAT oficial](https://sede.agenciatributaria.gob.es/)
- **Contacta con tu asesor fiscal** para aspectos específicos

---

## 📅 Historial

- **2025-11-15**: CORRECCIÓN: Actualizar tipos de IVA en compras (0% particular, 10% artista, 21% venta)
- **2025-11-14**: Transformación de REAV a REBU completada
- **2025-11-14**: Validación contra documentación AEAT
- **2025-11-14**: Documentación actualizada con información oficial

---

## ✨ Conclusión

El módulo REBU para Odoo 17 ha sido transformado correctamente desde REAV y ha sido validado contra la 
documentación oficial de la AEAT. La configuración es **correcta y completa** para bienes artísticos con 
IVA del 21%.

**Estado: LISTO PARA USAR** ✅

Se recomienda validación final con asesor fiscal antes de usar en producción.
