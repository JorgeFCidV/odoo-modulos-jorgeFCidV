# Configuración

## Instalación del módulo

1. Copiar el módulo `l10n_es_rebu` en la carpeta `addons` de tu instancia de Odoo
2. Actualizar la lista de módulos disponibles
3. Buscar e instalar el módulo "REBU - Régimen Especial de Bienes Usados (Bienes Artísticos)"

## Aplicar cambios al plan contable

Una vez instalado el módulo, es necesario actualizar la localización fiscal de tu compañía para que se apliquen los nuevos impuestos y posiciones fiscales:

### Paso 1: Acceder a la configuración de localización fiscal
- Ir a **Contabilidad** > **Configuración** > **Localización fiscal**
- O acceder a través de **Configuración** > **Facturación/Contabilidad** > **Localización fiscal**

### Paso 2: Recargar la localización
- Hacer clic en el botón **"Recargar"** 
- Esto aplicará los nuevos impuestos y posiciones fiscales a tu plan contable

### Paso 3: Verificar la instalación
- Ir a **Contabilidad** > **Configuración** > **Impuestos**
- Verificar que existan los siguientes impuestos:
  - IVA Soportado no deducible REBU 21%
  - IVA Repercutido incluido REBU 21%

- Ir a **Contabilidad** > **Configuración** > **Posiciones fiscales**
- Verificar que exista:
  - REBU - Bienes Usados Artísticos

## Notas importantes

- El módulo añade los impuestos y posiciones fiscales a las plantillas de planes contables estándar
- Los cambios se aplicarán a nuevos planes contables que se creen con estas plantillas
- Para aplicar los cambios a un plan contable existente, es necesario ejecutar el botón "Recargar"
