class Grammar(object):
    def __init__(self):
        self.E = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-', '*', '/', '(', ')']
        self.N = ["FORMULA", "SIGN", "NUMBER", "DIGIT"]
        self.S = self.N[0]
        self.rules = {self.N[2]: [self.N[1]], self.N[1]: self.E[0], self.S: [[self.S, self.N[1], self.S]]}


class ToolKit(object):
    def __init__(self):
        self.grammar = Grammar()

    def remove_unproductive_non_terminal(self):
        alive = []
        # Нахождение первого элемента, который войдет в alive
        for rules_for_symbols in self.grammar.rules:
            right_part = self.grammar.rules[rules_for_symbols]
            is_terminal = True
            # for rule in right_part:
            if isinstance(right_part, list):
                for symbol in right_part:
                    if isinstance(symbol, list):
                        for s in symbol:
                            is_terminal = s in self.grammar.E  # Проверка все ли символы в правой части терминалы
                            if not is_terminal:
                                break
                        if is_terminal:  # если да, то добавляем левую часть в alive
                            alive.append(rules_for_symbols)
                            break
                    else:
                        is_terminal = symbol in self.grammar.E    # Проверка все ли символы в правой части терминалы
                        if not is_terminal:
                            break
                if is_terminal:  # если да, то добавляем левую часть в alive
                    alive.append(rules_for_symbols)
                    break
            else:
                is_terminal = right_part in self.grammar.E  # Проверка все ли символы в правой части терминалы

                if is_terminal:  # если да, то добавляем левую часть в alive
                    alive.append(rules_for_symbols)
                    break

        # Основной алгоритм
        expansion = True

        while expansion:
            alive_size = len(alive)
            for rules_for_symbols in self.grammar.rules:
                right_part = self.grammar.rules[rules_for_symbols]
                # for rule in right_part:
                is_terminal_or_from_alive = True
                if isinstance(right_part, list):
                    for symbol in right_part:

                        if isinstance(symbol, list):
                            for s in symbol:
                                is_terminal_or_from_alive = s in self.grammar.E or s in alive  # Проверка все лисимволы
                                if not is_terminal_or_from_alive:  # в правой части терминалы либо из alive
                                    break
                            if is_terminal_or_from_alive:  # если да, то добавляем левую часть в alive
                                if not rules_for_symbols in alive:
                                    alive.append(rules_for_symbols)
                        else:
                            is_terminal_or_from_alive = symbol in self.grammar.E or symbol in alive  # Проверка все ли
                            if not is_terminal_or_from_alive:          # символы в правой части терминалы либо из alive
                                break

                    if is_terminal_or_from_alive:  # если да, то добавляем левую часть в alive
                        if not rules_for_symbols in alive:
                            alive.append(rules_for_symbols)

                else:
                    is_terminal_or_from_alive = right_part in self.grammar.E or right_part in alive
                    if is_terminal_or_from_alive:
                        if not rules_for_symbols in alive:
                            alive.append(rules_for_symbols)

            if alive_size == len(alive):   # Проверка расширилось ли alive
                expansion = False

        return alive


toolkit = ToolKit()

print(toolkit.remove_unproductive_non_terminal())
