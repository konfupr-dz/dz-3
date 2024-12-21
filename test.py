import unittest

from main import ConfigLanguageParser


class TestConfigParser(unittest.TestCase):

    def setUp(self):
        """Метод для инициализации перед каждым тестом"""
        # Пример инициализации с константами
        self.parser = ConfigLanguageParser()
        self.parser.constants = {
            'name': 'Alice',
            'age': 25,
            'result': 20
        }

    def test_parse_string(self):
        """Тест обработки строковых значений"""
        input_text = "'Hello'"
        expected_output = "Hello"
        result = self.parser.evaluate_expression(input_text)
        self.assertEqual(result, expected_output)


    def test_parse_number(self):
        """Тест обработки числовых значений"""
        input_text = "25"
        expected_output = 25
        result = self.parser.evaluate_expression(input_text)
        self.assertEqual(result, expected_output)

    def test_parse_variable(self):
        """Тест обработки переменных"""
        input_text = "|name|"
        expected_output = 'Alice'  # Константа 'name' имеет значение 'Alice'
        result = self.parser.evaluate_expression(input_text)
        self.assertEqual(result, expected_output)

    def test_parse_computation(self):
        """Тест вычисления выражений"""
        input_text = "|age - 5|"
        expected_output = 20  # age = 25, 25 - 5 = 20
        result = self.parser.evaluate_expression(input_text)
        self.assertEqual(result, expected_output)

    def test_invalid_expression(self):
        """Тест на ошибку синтаксиса в выражении"""
        input_text = "|25 + 'Alice'|"
        with self.assertRaises(SyntaxError):
            self.parser.evaluate_expression(input_text)


if __name__ == '__main__':
    unittest.main()
