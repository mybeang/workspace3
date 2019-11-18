from test_global_var.conf import GlobalVars
from unittest import TestCase


class ThisTest(TestCase):
    def test_001(self):
        self.assertEqual(GlobalVars.a, 1)
        self.assertEqual(GlobalVars.b, 2)
        self.assertEqual(GlobalVars.c, 3)
