# Checklist de Implementación - Módulo REBU

Guía paso a paso para instalar y validar el módulo REBU en Odoo 17.

---

## 📋 CHECKLIST COMPLETO

### ✅ Fase 1: Preparación (Antes de instalar)

#### Lectura de documentación
- [ ] Leer [INDICE_DOCUMENTACION.md](INDICE_DOCUMENTACION.md)
- [ ] Leer [VALIDACION_AEAT.md](VALIDACION_AEAT.md)
- [ ] Leer [RECOMENDACIONES_AEAT.md](RECOMENDACIONES_AEAT.md) (CRÍTICO)
- [ ] Entender punto 1: "El REBU es VOLUNTARIO"
- [ ] Entender punto 3: "Base Imponible = MARGEN BRUTO"

#### Validación fiscal
- [ ] Contactar con asesor fiscal
- [ ] Confirmar que aplica REBU para tu caso
- [ ] Confirmar que 21% es el IVA correcto
- [ ] Documentar procedimiento de optación por REBU ante AEAT

#### Preparación técnica
- [ ] Tener acceso a Odoo 17
- [ ] Backup de base de datos creado
- [ ] Ambiente de pruebas disponible
- [ ] Usuario con permisos de administrador

---

### ✅ Fase 2: Instalación del módulo

#### Copiar archivos
- [ ] Copiar carpeta `l10n_es_rebu` a `/addons/` de Odoo
- [ ] Verificar permisos de carpeta (755)
- [ ] Verificar permisos de archivos (644)

#### Instalar en Odoo
- [ ] Entrar en Odoo como administrador
- [ ] Ir a **Aplicaciones** → **Actualizar lista de módulos**
- [ ] Buscar "REBU" o "Régimen Especial de Bienes Usados"
- [ ] Hacer clic en **Instalar**
- [ ] Esperar a que termine la instalación

#### Verificar instalación
- [ ] Ir a **Contabilidad** → **Configuración** → **Impuestos**
- [ ] Verificar impuestos existentes:
  - [ ] "IVA Soportado no deducible REBU 21%" (compra)
  - [ ] "IVA Repercutido incluido REBU 21%" (venta)
- [ ] Ir a **Contabilidad** → **Configuración** → **Posiciones fiscales**
- [ ] Verificar posición: "REBU - Bienes Usados Artísticos"

---

### ✅ Fase 3: Configuración de localización fiscal

#### Recargar localización
- [ ] Ir a **Contabilidad** → **Configuración** → **Localización fiscal**
- [ ] Hacer clic en **Recargar**
- [ ] Esperar a que termine
- [ ] Verificar que no hay errores

#### Validar cambios
- [ ] Ir a **Contabilidad** → **Configuración** → **Impuestos**
- [ ] Verificar impuestos REBU están activos
- [ ] Hacer clic en impuesto REBU
- [ ] Verificar:
  - [ ] Porcentaje: 21%
  - [ ] Tipo: Compra (no deducible) o Venta (incluido)
  - [ ] Grupo de impuestos: "REBU"

---

### ✅ Fase 4: Configuración de empresa

#### Datos de empresa
- [ ] Ir a **Configuración** → **Empresas**
- [ ] Editar tu empresa
- [ ] Ir a pestaña **Facturación**
- [ ] En "Localización fiscal": seleccionar localización española
- [ ] Guardar

#### Registro del régimen (IMPORTANTE)
- [ ] 📝 Documentar en Odoo la opción por REBU
- [ ] 📧 Enviar comunicación a AEAT (opción por régimen REBU)
- [ ] 📋 Guardar copia de comunicación en expediente fiscal

---

### ✅ Fase 5: Configuración de contactos

#### Clientes
- [ ] Crear/editar cliente típico de REBU
- [ ] Ir a pestaña **Facturación**
- [ ] En "Posición fiscal": seleccionar "REBU - Bienes Usados Artísticos"
- [ ] Guardar

#### Proveedores
- [ ] Crear/editar proveedor típico de REBU
- [ ] Ir a pestaña **Facturación**
- [ ] En "Posición fiscal": seleccionar "REBU - Bienes Usados Artísticos"
- [ ] Guardar

---

### ✅ Fase 6: Configuración de productos

#### Crear categoría de productos
- [ ] Ir a **Inventario** → **Configuración** → **Categorías de producto**
- [ ] Crear nueva categoría: "Bienes Artísticos REBU"
- [ ] Guardar

#### Configurar impuestos en productos
- [ ] Para productos REBU (bienes artísticos):
  - [ ] Ir a **Ventas** → **Productos**
  - [ ] Crear/editar producto
  - [ ] Pestaña **Información General**
  - [ ] **Impuestos de cliente**: "IVA Repercutido incluido REBU 21%"
  - [ ] **Impuestos de proveedor**: "IVA Soportado no deducible REBU 21%"
  - [ ] Guardar

---

### ✅ Fase 7: Pruebas iniciales

#### Crear factura de compra
- [ ] Ir a **Compras** → **Nuevas facturas**
- [ ] Seleccionar proveedor con REBU configurado
- [ ] Crear línea con producto REBU
- [ ] Verificar que impuesto es "IVA Soportado no deducible REBU 21%"
- [ ] Verificar que es **NO deducible** (0% en deducible)
- [ ] Guardar como borrador

#### Crear factura de venta
- [ ] Ir a **Ventas** → **Nuevas facturas**
- [ ] Seleccionar cliente con REBU configurado
- [ ] Crear línea con producto REBU
- [ ] Verificar que impuesto es "IVA Repercutido incluido REBU 21%"
- [ ] Guardar como borrador

#### Validar cálculos
- [ ] En factura de venta, verificar:
  - [ ] Línea con precio (sin IVA)
  - [ ] Impuesto calculado al 21%
  - [ ] Total = Subtotal + Impuesto

---

### ✅ Fase 8: Pruebas de margen (CRÍTICO)

#### Test de margen bruto
- [ ] Crear factura de compra:
  - [ ] Precio: 1.000 € (sin IVA)
  - [ ] IVA 21%: 210 €
  - [ ] Total: 1.210 € (con IVA)

- [ ] Crear factura de venta del MISMO artículo:
  - [ ] Precio: 1.500 € (sin IVA)
  - [ ] IVA 21%: 315 €
  - [ ] Total: 1.815 € (con IVA)

#### Validar cálculo del margen
- [ ] Margen = Precio venta (con IVA) - Precio compra (con IVA)
- [ ] Margen = 1.815 - 1.210 = 605 €
- [ ] ✅ CORRECTO: El cálculo es manual en Odoo
  - (No está automatizado en Fase 1)

#### Documentación
- [ ] Anotar ejemplo en documento fiscal
- [ ] Guardar para referencia de auditoría

---

### ✅ Fase 9: Validación de reportes

#### Reporte de facturas
- [ ] Ir a **Contabilidad** → **Reportes** → **Facturas**
- [ ] Filtrar por impuesto "REBU"
- [ ] Verificar que aparecen facturas correctas

#### Reporte de impuestos
- [ ] Ir a **Contabilidad** → **Reportes** → **Resumen de impuestos**
- [ ] Verificar:
  - [ ] IVA no deducible aparece como NO deducible
  - [ ] IVA repercutido aparece como deuda

#### Reporte de movimientos
- [ ] Ir a **Contabilidad** → **Contabilidad** → **Movimientos**
- [ ] Filtrar por impuesto REBU
- [ ] Verificar que movimientos están correctos

---

### ✅ Fase 10: Validación fiscal final

#### Documentación requerida
- [ ] [ ] Copia de optación por REBU ante AEAT
- [ ] [ ] Procedimiento de cálculo documentado
- [ ] [ ] Ejemplos de facturas con REBU
- [ ] [ ] Ejemplos de márgenes calculados
- [ ] [ ] Segregación IVA deducible / no deducible

#### Asesoramiento final
- [ ] [ ] Contactar asesor fiscal con ejemplos
- [ ] [ ] Revisar facturas creadas en Odoo
- [ ] [ ] Validar que cálculos son correctos
- [ ] [ ] Obtener visto bueno para producción

#### Checklist de conformidad
- [ ] [ ] Régimen REBU documentado
- [ ] [ ] Base imponible = margen bruto (entendido)
- [ ] [ ] IVA no deducible en compras (configurado)
- [ ] [ ] IVA repercutido en ventas (configurado)
- [ ] [ ] Obligaciones de facturación (cumplidas)
- [ ] [ ] Registros contables (mantenidos)

---

## 🎯 Después de instalar

### Operación diaria
1. Crear facturas normalmente (sistema automático)
2. Verificar impuestos correctos (REBU)
3. Calcular márgenes (manual o con auxiliar)
4. Documentar operaciones para auditoría
5. Mantener segregación IVA deducible/no deducible

### Reportes periódicos
- Mensual: Resumen de facturas REBU
- Trimestral: Validación de márgenes
- Anual: Auditoría fiscal completa

### Mantenimiento
- Revisar obligaciones de facturación (AEAT)
- Actualizar documentación si hay cambios normativos
- Comunicar cambios de régimen si es necesario

---

## ⚠️ Problemas comunes y soluciones

### "No aparecen impuestos REBU"
1. ✅ Verificar que módulo está instalado
2. ✅ Recargar localización fiscal
3. ✅ Limpiar caché de navegador
4. ✅ Contactar soporte técnico

### "El impuesto no está marcado como no deducible"
1. ✅ Ir a impuesto
2. ✅ Verificar tipo: "Compra" y "No deducible"
3. ✅ Guardar cambios
4. ✅ Recargar localización

### "Las posiciones fiscales no se aplican"
1. ✅ Verificar contacto tiene posición fiscal asignada
2. ✅ Crear factura nueva (no editar borrador antiguo)
3. ✅ Verificar que cliente/proveedor tiene fiscal correcto
4. ✅ Recargar página de contacto

### "No veo diferencia en márgenes"
- ⚠️ NOTA: Fase 1 no calcula márgenes automáticamente
- Se deben calcular manualmente o con módulo adicional
- Consultar documentación: [RECOMENDACIONES_AEAT.md](RECOMENDACIONES_AEAT.md) Fase 2

---

## 📞 Contacto y soporte

- Documentación: [INDICE_DOCUMENTACION.md](INDICE_DOCUMENTACION.md)
- AEAT oficial: https://sede.agenciatributaria.gob.es/
- Asesor fiscal: [Tu asesor/gestoría]
- Soporte técnico Odoo: [Tu proveedor técnico]

---

## ✅ Fin del checklist

Una vez completados todos los pasos, tu módulo REBU está:
- ✅ Instalado
- ✅ Configurado
- ✅ Probado
- ✅ Validado
- ✅ Listo para producción

**Recuerda**: Contacta con tu asesor fiscal para validación final antes de usar con datos reales.

---

**Última actualización**: 14 de noviembre de 2025  
**Versión**: 1.0

