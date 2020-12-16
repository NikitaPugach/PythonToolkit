class Grammar(object):
    def __init__(self):
        self.E = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-', '*', '/', '(', ')']
        self.N = ["FORMULA", "SIGN", "NUMBER", "DIGIT"]
        self.S = self.N[0]
        self.rules = {self.S: [self.S, self.N[1], self.S], }


class ToolKit(object):
    def __init__(self):
        self.grammar = Grammar()

    def remove_unproductive_non_terminal(self):
        alive = []
        # Нахождение первого элемента, который войдет в alive
        for rules_for_symbols in self.grammar.rules:
            right_part = self.grammar.rules[rules_for_symbols]
            is_terminal = True
            for rule in right_part:
                for symbol in rule:
                    is_terminal = symbol in self.grammar.E    # Проверка все ли символы в правой части терминалы
                    if not is_terminal:
                        break
                if is_terminal:  # если да, то добавляем левую часть в alive
                    alive.append(rules_for_symbols)
                    break

        # Основной алгоритм
        expansion = True

        while expansion:
            alive_size = len(alive)
            for rules_for_symbols in self.grammar.rules:
                right_part = self.grammar.rules[rules_for_symbols]
                for rule in right_part:
                    is_terminal_or_from_alive = True
                    for symbol in rule:
                        is_terminal_or_from_alive = symbol in self.grammar.E or symbol in alive  # Проверка все ли
                        if not is_terminal_or_from_alive:             # символы в правой части терминалы либо из alive
                            break
                    if is_terminal_or_from_alive:  # если да, то добавляем левую часть в alive
                        alive.append(rules_for_symbols)
            if alive_size == len(alive):   # Проверка расширилось ли alive
                expansion = False

        return alive
