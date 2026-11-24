from decimal import Decimal
from django.test import TestCase
from apps.core.utils import naira_format


class CoreUtilsTestCase(TestCase):
    def test_naira_format(self):
        self.assertEqual(naira_format(1000), "₦1,000.00")
        self.assertEqual(naira_format(2500.5), "₦2,500.50")
        self.assertEqual(naira_format("1500000"), "₦1,500,000.00")
        self.assertEqual(naira_format(Decimal("0.75")), "₦0.75")
