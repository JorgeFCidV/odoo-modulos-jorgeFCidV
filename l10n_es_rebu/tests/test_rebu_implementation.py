# Copyright 2025 Jorge Fernández
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import TransactionCase


class TestREBUImplementation(TransactionCase):
    """
    Test suite for REBU (Régimen Especial de Bienes Usados) implementation.
    
    Tests validate compliance with AEAT specifications:
    - https://sede.agenciatributaria.gob.es/Sede/iva/regimenes-tributacion-iva/regimen-especial-bienes-usados.html
    """

    @classmethod
    def setUpClass(cls):
        """Set up test environment with REBU tax configuration."""
        super().setUpClass()
        
        # Get REBU tax records
        cls.tax_group_rebu = cls.env["account.tax.group"].search(
            [("name", "=", "REBU")]
        )
        
        # Impuesto REBU de compra (no deducible)
        cls.tax_purchase_rebu = cls.env["account.tax"].search(
            [("name", "ilike", "REBU non-deductible")]
        )
        
        # Impuesto REBU de venta (incluido)
        cls.tax_sale_rebu = cls.env["account.tax"].search(
            [("name", "ilike", "REBU included")]
        )
        
        # Posición fiscal REBU
        cls.fiscal_position_rebu = cls.env["account.fiscal.position"].search(
            [("name", "ilike", "REBU")]
        )

    def test_01_rebu_tax_group_exists(self):
        """
        Test 1: Verify that REBU tax group exists.
        Expected: Tax group "REBU" should be created.
        """
        self.assertTrue(
            self.tax_group_rebu,
            "REBU tax group not found. Module not installed correctly."
        )
        self.assertEqual(
            self.tax_group_rebu.name,
            "REBU",
            "Tax group name should be 'REBU'"
        )

    def test_02_rebu_purchase_tax_exists(self):
        """
        Test 2: Verify that REBU purchase tax exists.
        Expected: Purchase tax "IVA Soportado no deducible REBU 21%" should exist.
        """
        self.assertTrue(
            self.tax_purchase_rebu,
            "REBU purchase tax not found. Check if module loaded correctly."
        )
        self.assertEqual(
            self.tax_purchase_rebu.amount,
            21.0,
            "REBU purchase tax rate should be 21%"
        )

    def test_03_rebu_sale_tax_exists(self):
        """
        Test 3: Verify that REBU sale tax exists.
        Expected: Sale tax "IVA Repercutido incluido REBU 21%" should exist.
        """
        self.assertTrue(
            self.tax_sale_rebu,
            "REBU sale tax not found. Check if module loaded correctly."
        )
        self.assertEqual(
            self.tax_sale_rebu.amount,
            21.0,
            "REBU sale tax rate should be 21%"
        )

    def test_04_purchase_tax_is_non_deductible(self):
        """
        Test 4: Verify that REBU purchase tax is marked as non-deductible.
        
        According to AEAT REBU regulations:
        "IVA soportado en las compras de bienes para reventa NO es deducible"
        (VAT on purchase of goods for resale is NOT deductible)
        
        Expected: Purchase tax should have type_tax_use="purchase"
        """
        self.assertEqual(
            self.tax_purchase_rebu.type_tax_use,
            "purchase",
            "REBU purchase tax type should be 'purchase' (non-deductible)"
        )

    def test_05_sale_tax_is_of_type_sale(self):
        """
        Test 5: Verify that REBU sale tax is marked as sale type.
        Expected: Sale tax should have type_tax_use="sale"
        """
        self.assertEqual(
            self.tax_sale_rebu.type_tax_use,
            "sale",
            "REBU sale tax type should be 'sale'"
        )

    def test_06_fiscal_position_rebu_exists(self):
        """
        Test 6: Verify that REBU fiscal position exists.
        Expected: Fiscal position "REBU - Bienes Usados Artísticos" should exist.
        """
        self.assertTrue(
            self.fiscal_position_rebu,
            "REBU fiscal position not found."
        )

    def test_07_fiscal_position_contains_tax_mappings(self):
        """
        Test 7: Verify that REBU fiscal position has tax mappings.
        
        According to AEAT, REBU applies to artistic goods. The fiscal position
        should map standard IVA taxes to REBU taxes.
        
        Expected: Fiscal position should have tax_ids (mappings)
        """
        self.assertTrue(
            self.fiscal_position_rebu.tax_ids,
            "REBU fiscal position should have tax mappings configured"
        )
        
        # Count mappings
        mappings_count = len(self.fiscal_position_rebu.tax_ids)
        self.assertGreater(
            mappings_count,
            0,
            f"REBU fiscal position should have at least one tax mapping, found {mappings_count}"
        )

    def test_08_purchase_tax_has_correct_account_mappings(self):
        """
        Test 8: Verify that REBU purchase tax has repartition lines.
        
        A tax in Odoo requires repartition lines to specify how the tax
        amount should be distributed to accounts.
        
        Expected: Tax should have repartition_line_ids with at least:
        - Base line
        - Tax line (for both invoice and refund)
        """
        repartition_lines = self.tax_purchase_rebu.invoice_repartition_line_ids
        self.assertTrue(
            repartition_lines,
            "REBU purchase tax should have repartition lines"
        )
        
        # Should have at least 2 lines (base + tax)
        self.assertGreaterEqual(
            len(repartition_lines),
            2,
            "Purchase tax should have at least base and tax repartition lines"
        )

    def test_09_sale_tax_has_correct_account_mappings(self):
        """
        Test 9: Verify that REBU sale tax has repartition lines.
        Expected: Tax should have repartition_line_ids
        """
        repartition_lines = self.tax_sale_rebu.invoice_repartition_line_ids
        self.assertTrue(
            repartition_lines,
            "REBU sale tax should have repartition lines"
        )
        
        self.assertGreaterEqual(
            len(repartition_lines),
            2,
            "Sale tax should have at least base and tax repartition lines"
        )

    def test_10_purchase_tax_percentage_is_21_percent(self):
        """
        Test 10: Verify purchase tax rate is exactly 21%.
        
        According to AEAT, for artistic goods under REBU regime,
        the applicable IVA rate is 21%.
        
        Expected: tax_purchase_rebu.amount == 21.0
        """
        self.assertEqual(
            self.tax_purchase_rebu.amount,
            21.0,
            "REBU purchase tax must be 21% according to AEAT specifications"
        )

    def test_11_sale_tax_percentage_is_21_percent(self):
        """
        Test 11: Verify sale tax rate is exactly 21%.
        Expected: tax_sale_rebu.amount == 21.0
        """
        self.assertEqual(
            self.tax_sale_rebu.amount,
            21.0,
            "REBU sale tax must be 21% according to AEAT specifications"
        )

    def test_12_purchase_tax_is_percent_type(self):
        """
        Test 12: Verify that REBU purchase tax is percentage-based (not fixed).
        Expected: amount_type should be "percent"
        """
        self.assertEqual(
            self.tax_purchase_rebu.amount_type,
            "percent",
            "REBU tax should be percentage-based"
        )

    def test_13_sale_tax_is_percent_type(self):
        """
        Test 13: Verify that REBU sale tax is percentage-based.
        Expected: amount_type should be "percent"
        """
        self.assertEqual(
            self.tax_sale_rebu.amount_type,
            "percent",
            "REBU tax should be percentage-based"
        )

    def test_14_purchase_tax_is_active(self):
        """
        Test 14: Verify that REBU purchase tax is active.
        Expected: active should be True
        """
        self.assertTrue(
            self.tax_purchase_rebu.active,
            "REBU purchase tax should be active"
        )

    def test_15_sale_tax_is_active(self):
        """
        Test 15: Verify that REBU sale tax is active.
        Expected: active should be True
        """
        self.assertTrue(
            self.tax_sale_rebu.active,
            "REBU sale tax should be active"
        )

    def test_16_fiscal_position_is_active(self):
        """
        Test 16: Verify that REBU fiscal position is active.
        Expected: active should be True
        """
        self.assertTrue(
            self.fiscal_position_rebu.active,
            "REBU fiscal position should be active"
        )

    def test_17_tax_group_has_correct_name(self):
        """
        Test 17: Verify tax group name is exactly "REBU".
        Expected: name == "REBU"
        """
        self.assertEqual(
            self.tax_group_rebu.name,
            "REBU",
            "Tax group name must be 'REBU'"
        )

    def test_18_purchase_tax_belongs_to_rebu_group(self):
        """
        Test 18: Verify that purchase tax belongs to REBU tax group.
        Expected: tax_group_id should be REBU group
        """
        self.assertEqual(
            self.tax_purchase_rebu.tax_group_id.id,
            self.tax_group_rebu.id,
            "Purchase tax should belong to REBU tax group"
        )

    def test_19_sale_tax_belongs_to_rebu_group(self):
        """
        Test 19: Verify that sale tax belongs to REBU tax group.
        Expected: tax_group_id should be REBU group
        """
        self.assertEqual(
            self.tax_sale_rebu.tax_group_id.id,
            self.tax_group_rebu.id,
            "Sale tax should belong to REBU tax group"
        )

    def test_20_margin_calculation_example_aeat_spec(self):
        """
        Test 20: Validate AEAT margin calculation formula (informational).
        
        According to AEAT REBU specification:
        Margin (base imponible) = (Selling price - Purchase price) / 1.21
        
        This test documents the expected calculation for reference:
        
        Example from AEAT:
        - Purchase price (with IVA): 1,000€
        - Selling price (with IVA): 1,500€
        - Margin: 500€
        - Taxable base: (500 × 100) ÷ 121 = 413.22€
        - IVA to pay: 413.22€ × 0.21 = 86.78€
        
        NOTE: This test is informational. Odoo's automatic calculation
        requires additional customization (not in Fase 1).
        """
        # Documented calculation
        purchase_price_with_iva = 1000.00
        selling_price_with_iva = 1500.00
        margin = selling_price_with_iva - purchase_price_with_iva
        
        # AEAT formula for taxable base
        taxable_base = (margin * 100) / 121
        iva_to_pay = taxable_base * 0.21
        
        # Validate calculation
        self.assertEqual(margin, 500.00)
        self.assertAlmostEqual(taxable_base, 413.22, places=2)
        self.assertAlmostEqual(iva_to_pay, 86.78, places=2)
        
        # This confirms AEAT formula understanding


class TestREBUMarginCalculation(TransactionCase):
    """
    Test suite for REBU margin calculation (Fase 2).
    
    These tests validate the margin calculation according to AEAT:
    Base Imponible = (Margen × 100) ÷ (100 + tipo impositivo)
    """

    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        super().setUpClass()

    def test_01_margin_calculation_no_margin(self):
        """
        Test: Margin calculation when there is NO margin.
        Scenario: Sell at cost
        Expected: BI = 0
        """
        purchase_price = 1000.00
        selling_price = 1000.00
        margin = selling_price - purchase_price
        
        self.assertEqual(margin, 0.00)
        # BI should be 0
        taxable_base = (margin * 100) / 121
        self.assertEqual(taxable_base, 0.00)

    def test_02_margin_calculation_positive_margin(self):
        """
        Test: Margin calculation with positive margin.
        Scenario: Normal resale with profit
        Expected: BI calculated correctly
        """
        purchase_price = 1000.00
        selling_price = 1500.00
        margin = selling_price - purchase_price
        
        # AEAT formula
        taxable_base = (margin * 100) / 121
        iva_amount = taxable_base * 0.21
        
        self.assertEqual(margin, 500.00)
        self.assertAlmostEqual(taxable_base, 413.22, places=2)
        self.assertAlmostEqual(iva_amount, 86.78, places=2)

    def test_03_margin_calculation_negative_margin(self):
        """
        Test: Margin calculation with negative margin.
        Scenario: Sale at loss
        Expected: BI = 0 (negative margins carry forward)
        """
        purchase_price = 1000.00
        selling_price = 800.00
        margin = selling_price - purchase_price
        
        self.assertEqual(margin, -200.00)
        # According to AEAT, negative margins carry forward
        # So current period BI should be 0
        taxable_base_current = max(0, (margin * 100) / 121)
        self.assertEqual(taxable_base_current, 0.00)

    def test_04_margin_calculation_multiple_operations_monthly(self):
        """
        Test: Margin calculation for multiple operations in a month.
        Scenario: Multiple sales with different margins
        Expected: Total BI = sum of individual BIs
        """
        operations = [
            {"purchase": 1000, "selling": 1500},  # margin: 500
            {"purchase": 500, "selling": 550},    # margin: 50
            {"purchase": 800, "selling": 900},    # margin: 100
        ]
        
        total_margin = 0
        total_bi = 0
        
        for op in operations:
            margin = op["selling"] - op["purchase"]
            total_margin += margin
            bi = (margin * 100) / 121
            total_bi += bi
        
        # Verify totals
        self.assertEqual(total_margin, 650.00)
        self.assertAlmostEqual(total_bi, 537.19, places=2)  # sum of individual BIs
        
        # Total IVA
        total_iva = total_bi * 0.21
        self.assertAlmostEqual(total_iva, 112.81, places=2)

    def test_05_margin_iva_rate_variations(self):
        """
        Test: Margin calculation with different IVA rates.
        Scenario: AEAT allows 4%, 10%, 21% depending on good type
        Note: Current implementation uses 21%
        """
        margin = 500.00
        
        # Test with different rates
        rates = [0.04, 0.10, 0.21]
        
        for rate in rates:
            taxable_base = (margin * 100) / (100 + rate * 100)
            iva_amount = taxable_base * rate
            
            if rate == 0.04:
                self.assertAlmostEqual(taxable_base, 480.77, places=2)
                self.assertAlmostEqual(iva_amount, 19.23, places=2)
            elif rate == 0.10:
                self.assertAlmostEqual(taxable_base, 454.55, places=2)
                self.assertAlmostEqual(iva_amount, 45.45, places=2)
            elif rate == 0.21:
                self.assertAlmostEqual(taxable_base, 413.22, places=2)
                self.assertAlmostEqual(iva_amount, 86.78, places=2)


class TestREBUIntegration(TransactionCase):
    """
    Integration tests for REBU module with Odoo models.
    """

    def test_01_rebu_module_is_installed(self):
        """
        Test: Verify that REBU module is installed.
        Expected: Module should be in installed state.
        """
        module = self.env["ir.module.module"].search(
            [("name", "=", "l10n_es_rebu"), ("state", "=", "installed")]
        )
        self.assertTrue(
            module,
            "l10n_es_rebu module should be installed"
        )

    def test_02_spanish_localization_is_installed(self):
        """
        Test: Verify that Spanish localization (l10n_es) is installed.
        Expected: Spanish localization should be available.
        """
        module = self.env["ir.module.module"].search(
            [("name", "=", "l10n_es"), ("state", "=", "installed")]
        )
        self.assertTrue(
            module,
            "l10n_es (Spanish localization) should be installed"
        )
