#!/bin/bash
# Copyright 2025 Jorge Fernández
# License AGPL-3.0 or later
# 
# Script para ejecutar pruebas del módulo REBU
# Uso: ./run_tests.sh [opción]

set -e

# Colores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funciones de output
print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Obtener directorio del script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

print_header "Pruebas de Validación REBU - Módulo Odoo 17"

# Verificar si Odoo está disponible
if ! command -v odoo-bin &> /dev/null; then
    print_error "odoo-bin no encontrado en PATH"
    print_warning "Instala Odoo 17 o añade odoo-bin al PATH"
    exit 1
fi

# Mostrar opciones
if [ $# -eq 0 ]; then
    print_warning "Uso: $0 [opción]"
    echo ""
    echo "Opciones disponibles:"
    echo "  1 - Ejecutar todas las pruebas (TestREBUImplementation)"
    echo "  2 - Ejecutar pruebas de margen (TestREBUMarginCalculation)"
    echo "  3 - Ejecutar pruebas de integración (TestREBUIntegration)"
    echo "  4 - Ejecutar TODAS las pruebas"
    echo "  5 - Ejecutar con cobertura de código"
    echo "  6 - Generar reporte HTML"
    echo ""
    exit 0
fi

OPTION=$1

case $OPTION in
    1)
        print_header "Ejecutando: TestREBUImplementation"
        python -m pytest tests/test_rebu_implementation.py::TestREBUImplementation -v
        ;;
    2)
        print_header "Ejecutando: TestREBUMarginCalculation"
        python -m pytest tests/test_rebu_implementation.py::TestREBUMarginCalculation -v
        ;;
    3)
        print_header "Ejecutando: TestREBUIntegration"
        python -m pytest tests/test_rebu_implementation.py::TestREBUIntegration -v
        ;;
    4)
        print_header "Ejecutando: TODAS LAS PRUEBAS"
        python -m pytest tests/test_rebu_implementation.py -v
        ;;
    5)
        print_header "Ejecutando con cobertura de código"
        python -m pytest tests/test_rebu_implementation.py --cov=. --cov-report=term-missing
        ;;
    6)
        print_header "Generando reporte HTML"
        python -m pytest tests/test_rebu_implementation.py --cov=. --cov-report=html
        print_success "Reporte generado en: htmlcov/index.html"
        ;;
    *)
        print_error "Opción no válida: $OPTION"
        exit 1
        ;;
esac

print_success "Pruebas completadas"
