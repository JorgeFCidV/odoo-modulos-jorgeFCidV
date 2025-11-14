# 🧪 Pruebas de Validación REBU

Suite de pruebas unitarias para validar la implementación del módulo REBU en Odoo 17.

---

## 📂 Estructura de Pruebas

```
tests/
├── __init__.py                           # Inicializador de pruebas
└── test_rebu_implementation.py           # Suite principal de pruebas
    ├── TestREBUImplementation            # 20 pruebas de configuración
    ├── TestREBUMarginCalculation         # 5 pruebas de margen
    └── TestREBUIntegration               # 2 pruebas de integración
                                          # TOTAL: 27 pruebas
```

---

## 🚀 Inicio Rápido

### Opción 1: Usar el script incluido

```bash
# Darle permisos de ejecución
chmod +x run_tests.sh

# Ver opciones
./run_tests.sh

# Ejecutar todas las pruebas
./run_tests.sh 4
```

### Opción 2: Usar pytest directamente

```bash
# Instalar pytest (si no lo tienes)
pip install pytest pytest-cov

# Ejecutar todas las pruebas
pytest tests/test_rebu_implementation.py -v

# Con cobertura
pytest tests/test_rebu_implementation.py --cov=. --cov-report=html
```

### Opción 3: Dentro de Odoo

```bash
# Terminal en servidor Odoo
odoo-bin -d mydb -i l10n_es_rebu --test-enable --log-level=test

# O con tag específico
odoo-bin -d mydb --test-tags=l10n_es_rebu
```

---

## 📊 Suites de Prueba

### Suite 1: TestREBUImplementation (20 tests)

Valida la configuración correcta de REBU según AEAT.

```bash
# Ejecutar solo esta suite
pytest tests/test_rebu_implementation.py::TestREBUImplementation -v
```

**Pruebas incluidas:**

| # | Test | Validación |
|---|------|-----------|
| 1-3 | Existencia de recursos | REBU group, tax purchase, tax sale |
| 4-5 | Tipos de impuesto | No deducible (purchase), sale |
| 6-7 | Posición fiscal | Existe, tiene mapeos |
| 8-9 | Líneas de repartición | Purchase y sale tienen líneas |
| 10-11 | Porcentaje 21% | Purchase 21%, Sale 21% |
| 12-13 | Tipo porcentual | Ambos son "percent" |
| 14-16 | Estado activo | Purchase, Sale, Fiscal position |
| 17-19 | Pertenencia a grupo | Todos pertenecen a REBU |
| 20 | Fórmula AEAT | Documentación de margen |

---

### Suite 2: TestREBUMarginCalculation (5 tests)

Valida los cálculos matemáticos de margen según AEAT.

```bash
# Ejecutar solo esta suite
pytest tests/test_rebu_implementation.py::TestREBUMarginCalculation -v
```

**Pruebas incluidas:**

| # | Test | Escenario |
|---|------|----------|
| 1 | Sin margen | Venta al costo |
| 2 | Margen positivo | Ganancia normal |
| 3 | Margen negativo | Venta con pérdida |
| 4 | Múltiples operaciones | Resumen mensual |
| 5 | Variaciones de tipo IVA | 4%, 10%, 21% |

---

### Suite 3: TestREBUIntegration (2 tests)

Valida la integración del módulo con Odoo.

```bash
# Ejecutar solo esta suite
pytest tests/test_rebu_implementation.py::TestREBUIntegration -v
```

**Pruebas incluidas:**

| # | Test | Validación |
|---|------|-----------|
| 1 | Módulo instalado | l10n_es_rebu en estado "installed" |
| 2 | Localización española | l10n_es disponible |

---

## 📈 Ejemplos de Ejecución

### Todas las pruebas

```bash
pytest tests/test_rebu_implementation.py -v
```

**Salida esperada:**

```
test_01_rebu_tax_group_exists PASSED
test_02_rebu_purchase_tax_exists PASSED
test_03_rebu_sale_tax_exists PASSED
...
=================== 27 passed in 2.45s ===================
```

---

### Solo pruebas críticas

```bash
pytest tests/test_rebu_implementation.py -v -m critical
```

---

### Con cobertura de código

```bash
pytest tests/test_rebu_implementation.py --cov=. --cov-report=html
# Abre: htmlcov/index.html
```

---

### Pruebas específicas

```bash
# Solo Test 1
pytest tests/test_rebu_implementation.py::TestREBUImplementation::test_01_rebu_tax_group_exists -v

# Solo suite de margen
pytest tests/test_rebu_implementation.py::TestREBUMarginCalculation -v
```

---

## ✅ Criterios de Éxito

### Todas las pruebas deben pasar (27/27)

```
✅ 20 tests en TestREBUImplementation
✅ 5 tests en TestREBUMarginCalculation
✅ 2 tests en TestREBUIntegration
```

### Cobertura mínima: 80%

```
Líneas cubiertas: > 80%
Ramas cubiertas: > 70%
```

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'pytest'"

```bash
pip install pytest pytest-cov
```

### "No tests found"

```bash
# Verificar estructura
ls -la tests/
# Debe haber __init__.py y test_*.py
```

### "REBU tax group not found"

El módulo no está instalado en Odoo.

**Soluciones:**
1. Instalar módulo desde Odoo: Aplicaciones → Buscar REBU → Instalar
2. Recargar localización fiscal
3. Reiniciar Odoo

### "assertion 'purchase_tax.amount == 21.0' failed"

El impuesto no tiene tasa 21%.

**Soluciones:**
1. Verificar `account.tax-es_common.csv`
2. Confirmar que amount="21.0"
3. Recargar localización fiscal

---

## 📊 Reporte de Pruebas

### Generar reporte HTML

```bash
pytest tests/test_rebu_implementation.py --cov=. --cov-report=html
# Abre htmlcov/index.html en navegador
```

### Generar reporte JSON

```bash
pytest tests/test_rebu_implementation.py --json-report --json-report-file=report.json
```

---

## 🔄 Fase 2: Pruebas Adicionales Recomendadas

Para la siguiente fase, se recomienda añadir:

```python
# 1. Tests de Factura Completa
class TestREBUInvoice:
    def test_purchase_invoice_with_rebu()
    def test_sales_invoice_with_rebu()
    def test_margin_calculation_on_invoice()

# 2. Tests de Margen Automático
class TestREBUMarginAutomatic:
    def test_margin_calculation_real_time()
    def test_margin_stored_in_invoice()

# 3. Tests de Reportes
class TestREBUReports:
    def test_margin_report()
    def test_deductible_vat_report()

# 4. Tests de Seguridad
class TestREBUSecurity:
    def test_only_rebu_goods()
    def test_user_permissions()
```

---

## 📝 Documentación Relacionada

- **PRUEBAS_VALIDACION_REBU.md** - Documentación completa de pruebas
- **VALIDACION_AEAT.md** - Especificaciones de AEAT
- **RECOMENDACIONES_AEAT.md** - Recomendaciones de implementación
- **INFORME_EVALUACION_IMPLEMENTACION.md** - Evaluación completa

---

## 📞 Soporte

Si necesitas ayuda con las pruebas:

1. Revisar `PRUEBAS_VALIDACION_REBU.md`
2. Verificar logs en `/var/log/odoo/`
3. Consultar documentación de pytest: https://docs.pytest.org

---

**Última actualización**: 14 de noviembre de 2025  
**Versión**: 1.0  
**Licencia**: AGPL-3.0 or later
