# Cambios Realizados - Transformación de REAV a REBU

## 📁 Estructura del módulo

### Cambios de nombres
- ✅ Carpeta: `l10n_es_reav` → `l10n_es_rebu`
- ✅ Identificadores internos: `reav` → `rebu`
- ✅ Identificadores de impuestos: `account_tax_template_p_reav0` → `account_tax_template_p_rebu0`
- ✅ Identificadores de grupos de impuestos: `tax_group_reav` → `tax_group_rebu`
- ✅ Identificadores de posición fiscal: `fp_reav` → `fp_rebu`

## 📝 Archivos modificados

### 1. `__manifest__.py`
**Cambios:**
- Nombre: "REAV - Régimen Especial Agencias de Viajes" → "REBU - Régimen Especial de Bienes Usados (Bienes Artísticos)"
- Autor: Bilbonet → Jorge Fernández
- Mantenedor: Bilbonet → JorgeFCidV
- Website: GitHub OCA → GitHub Personal

### 2. `data/template/account.tax.group-es_common.csv`
**Cambios:**
- ID: `tax_group_reav` → `tax_group_rebu`
- Nombre: REAV → REBU (todos los idiomas)

### 3. `data/template/account.tax-es_common.csv`
**Cambios principales:**
- **IVA de compra (no deducible):**
  - ID: `account_tax_template_p_reav0` → `account_tax_template_p_rebu0`
  - Nombre: "VAT REAV non-deductible" → "VAT REBU non-deductible 21%"
  - Cantidad: 0.00% → 21.0%
  - Grupo de impuestos: `tax_group_reav` → `tax_group_rebu`

- **IVA de venta (incluido):**
  - ID: `account_tax_template_s_reav0` → `account_tax_template_s_rebu0`
  - Nombre: "VAT REAV included" → "VAT REBU included 21%"
  - Cantidad: 0.00% → 21.0%
  - Grupo de impuestos: `tax_group_reav` → `tax_group_rebu`

### 4. `data/template/account.fiscal.position-es_common.csv`
**Cambios:**
- ID: `fp_reav` → `fp_rebu`
- Nombre: "REAV - Travel agencies" → "REBU - Used Artistic Goods"
- Español: "REAV - Agencias de viajes" → "REBU - Bienes Usados Artísticos"
- Catalán: "REAV - Agències de viatges" → "REBU - Béns Usats Artístics"
- Todos los mapeos de impuestos actualizados a los nuevos IDs

### 5. `README.rst`
**Cambios:**
- Título y descripción completamente actualizada
- Referencias a REBU en lugar de REAV
- Información sobre bienes artísticos
- Enlaces actualizados

### 6. `readme/DESCRIPTION.md`
**Cambios:**
- Descripción orientada a bienes artísticos
- Target: Galerías de arte, marchantes, comerciantes de arte
- Características fiscales específicas de REBU

### 7. `readme/CONFIGURE.md`
**Creado nuevo con:**
- Instrucciones de instalación
- Pasos para recargar la localización fiscal
- Verificación de instalación

### 8. `readme/USAGE.md`
**Creado nuevo con:**
- Cómo asignar impuestos a productos
- Cómo asignar posición fiscal a contactos
- Impacto en facturas de venta y compra
- Consideraciones especiales

### 9. `readme/CONTRIBUTORS.md`
**Actualizado con:**
- Jorge Fernández como autor principal
- Referencia a contribuyentes originales de REAV

## 🔧 Impuestos aplicables

| Concepto | Nombre | Porcentaje | Tipo |
|----------|--------|-----------|------|
| Compras | IVA Soportado no deducible REBU 21% | 21% | No deducible |
| Ventas | IVA Repercutido incluido REBU 21% | 21% | Incluido |

## 🎯 Destino del módulo

- **Entidad**: Galerías de arte, marchantes, comerciantes de bienes artísticos
- **Régimen fiscal**: REBU (Régimen Especial de Bienes Usados)
- **Base imponible**: Margen bruto (diferencia entre precio de venta y compra)
- **Tipo IVA**: 21%

## ✅ Verificación final

Todos los archivos han sido actualizado satisfactoriamente:
- [x] Estructura de carpetas renombrada
- [x] Metadatos del módulo actualizados
- [x] Impuestos configurados al 21%
- [x] Posiciones fiscales creadas
- [x] Documentación completada
- [x] Identificadores internos actualizados

## 📞 Próximos pasos

Para completar la adaptación:

1. **Revisar especificaciones de AEAT**: Proporciona la documentación oficial de AEAT para validar que todos los requisitos están cumplidos

2. **Pruebas en entorno de desarrollo**: Verifica que el módulo se instala correctamente y que los impuestos funcionan como se espera

3. **Validación fiscal**: Consulta con un asesor fiscal para asegurar que el régimen se ha implementado correctamente

4. **Ajustes si es necesario**: En función de la documentación de AEAT, se pueden realizar ajustes adicionales
