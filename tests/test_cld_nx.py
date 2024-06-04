import unittest
from src import cld_nx

class TestCleanVariableName(unittest.TestCase):
    def setUp(self):
        pass
    def test_clean_variable_name_with_numbers(self):
        self.assertEqual(cld_nx.clean_variable_name("variable&aaa"), "variable and aaa")
        self.assertEqual(cld_nx.clean_variable_name("123variable"), "123variable")
        self.assertEqual(cld_nx.clean_variable_name("var123iable"), "var123iable")

    def test_clean_variable_name_with_underscores(self):
        self.assertEqual(cld_nx.clean_variable_name("variable_name"), "variable_name")
        self.assertEqual(cld_nx.clean_variable_name("_variable_name_"), "_variable_name_")
        self.assertEqual(cld_nx.clean_variable_name("__variable__name__"), "__variable__name__")

    def test_clean_variable_name_with_mixed_cases(self):
        self.assertEqual(cld_nx.clean_variable_name("VariableName"), "variablename")
        self.assertEqual(cld_nx.clean_variable_name("variableNAME"), "variablename")
        self.assertEqual(cld_nx.clean_variable_name("VARIABLEName"), "variablename")

    def test_clean_variable_name_with_multiple_replacements(self):
        self.assertEqual(cld_nx.clean_variable_name("variable&name/with\\chars"), "variable and name or with chars")
        self.assertEqual(cld_nx.clean_variable_name("variable\\name&with/chars"), "variable name and with chars")
        self.assertEqual(cld_nx.clean_variable_name("variable/name\\with&chars"), "variable or name with and chars")
