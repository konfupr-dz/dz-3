import sys
import re
import yaml


class SyntaxError(Exception):
    pass


class ConfigLanguageParser:
    def __init__(self):
        self.constants = {}

    def parse_comment(self, line):
        """Преобразует комментарии."""
        if line.startswith('"'):
            return None

    def parse_constant(self, line):
        """Обрабатывает объявление констант."""
        match = re.match(r'^([_a-zA-Z]+):\s*(.+)$', line)
        if match:
            name, value = match.groups()
            if not re.fullmatch(r'[_a-zA-Z]+', name):
                raise SyntaxError(f"Некорректное имя константы: {name}")
            value = self.evaluate_expression(value.strip())
            self.constants[name] = value
            return {name: value}
        return None

    def parse_expression(self, line):
        """Обрабатывает вычисление константного выражения."""
        match = re.match(r'^\|(.+)\|$', line.strip())
        if match:
            expression = match.group(1)
            return self.evaluate_expression(expression)
        return None

    def evaluate_expression(self, expression):
        """Вычисляет значение выражения."""
        expression = expression.strip("|")
        expression = re.sub(
            r'\b([_a-zA-Z]+)\b',
            lambda m: f"'{self.constants[m.group(1)]}'" if m.group(1) in self.constants and isinstance(
                self.constants[m.group(1)], str)
            else str(self.constants.get(m.group(1), m.group(1))),
            expression
        )
        try:
            if "print(" in expression:
                match = re.search(r'print\((.+?)\)', expression)
                if match:
                    content = eval(match.group(1))
                    print(content)
                    expression = expression.replace(match.group(0), str(content))

            return eval(expression)
        except Exception as e:
            raise SyntaxError(f"Ошибка в вычислении выражения '{expression}': {e}")

    def parse_array(self, line):
        """Преобразует массивы в YAML."""
        match = re.match(r'^\[(.+)\]$', line.strip())
        if match:
            elements = [self.evaluate_expression(elem.strip()) for elem in match.group(1).split(";") if elem.strip()]
            return elements
        return None

    def parse(self, raw_input):
        """Основной метод разбора текста УКЯ."""
        result = {}
        for line in raw_input.splitlines():
            line = line.strip()
            if not line or line.startswith('"'):
                continue

            constant = self.parse_constant(line)
            if constant:
                result.update(constant)
                continue

            array = self.parse_array(line)
            if array is not None:
                result["array"] = array
                continue

            expression = self.parse_expression(line)
            if expression is not None:
                result["result"] = expression
                continue

            raise SyntaxError(f"Неизвестная конструкция: {line}")

        return result


def main():
    input_data = sys.stdin.read()
    parser = ConfigLanguageParser()
    try:
        parsed_data = parser.parse(input_data)
        yaml_output = yaml.dump(parsed_data, allow_unicode=True)
        print(yaml_output)
    except SyntaxError as e:
        print(f"Синтаксическая ошибка: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
