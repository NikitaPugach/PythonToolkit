class Grammar(object):
    def __init__(self):
        self.E = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-', '*', '/', '(', ')']
        self.N = ["FORMULA", "SIGN", "NUMBER", "DIGIT"]
        self.S = self.N[0]
        self.rules = {self.S: [[self.S, self.N[1], self.S], self.E[7]], self.N[2]: [self.N[1]], self.N[1]: self.E[0], self.N[3]: None}

    def show(self):
        print("Non-terminals: ", end="")
        print(self.N)
        print("Terminals", end="")
        print(self.E)
        print("Start Symbol:", end="")
        print(self.S)
        print("Rules", end="")
        print(self.rules)


class ToolKit(object):
    def __init__(self, grammar):
        self.grammar = grammar

    def find_unproductive_non_terminal(self):
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

    def find_unattainable_non_terminal(self):
        reachable = [self.grammar.S]

        expansion = True
        while expansion:
            reachable_size = len(reachable)

            for rules_for_symbols in self.grammar.rules:
                if rules_for_symbols in reachable:
                    right_part = self.grammar.rules[rules_for_symbols]
                    if isinstance(right_part, list):
                        for symbol in right_part:
                            if isinstance(symbol, list):
                                for s in symbol:
                                    if s in self.grammar.N:
                                        if not s in reachable:
                                            reachable.append(s)
                            else:
                                if symbol in self.grammar.N:
                                    if not symbol in reachable:
                                        reachable.append(symbol)
                    else:
                        if right_part in self.grammar.N:
                            if not right_part in reachable:
                                reachable.append(right_part)

            if len(reachable) == reachable_size:
                expansion = False

        return reachable

    def remove_all_rules_with_unproductive_non_terminal(self):
        alive = self.find_unproductive_non_terminal()

        to_delete = list(set(self.grammar.rules.keys()) - set(alive))

        # Удаляем все правила, в которых в левой части стоят недосягаемые нетерминалы
        [self.grammar.rules.pop(key) for key in to_delete]

        self.grammar.N = alive

        for rules_for_symbols in self.grammar.rules:
            right_part = self.grammar.rules[rules_for_symbols]

            if isinstance(right_part, list):
                for symbol in right_part:
                    if isinstance(symbol, list):
                        for s in symbol:
                            if not s in self.grammar.N:
                                if not s in self.grammar.E:
                                    self.grammar.rules.pop(s)
                    else:
                        if not symbol in self.grammar.N:
                            if not symbol in self.grammar.E:
                                self.grammar.rules.pop(symbol)
            else:
                if not right_part in self.grammar.N:
                    if not right_part in self.grammar.E:
                        self.grammar.rules.pop(right_part)

    def remove_all_rules_with_unattainable_non_terminal(self):
        reachable = self.find_unattainable_non_terminal()

        to_delete = list(set(self.grammar.rules.keys()) - set(reachable))

        # Удаляем все правила, в которых в левой части стоят недосягаемые нетерминалы
        [self.grammar.rules.pop(key) for key in to_delete]

        self.grammar.N = reachable

        for rules_for_symbols in self.grammar.rules:
            right_part = self.grammar.rules[rules_for_symbols]

            if isinstance(right_part, list):
                for symbol in right_part:
                    if isinstance(symbol, list):
                        for s in symbol:
                            if not s in self.grammar.N:
                                if not s in self.grammar.E:
                                    self.grammar.rules.pop(s)
                    else:
                        if not symbol in self.grammar.N:
                            if not symbol in self.grammar.E:
                                self.grammar.rules.pop(symbol)
            else:
                if not right_part in self.grammar.N:
                    if not right_part in self.grammar.E:
                        self.grammar.rules.pop(right_part)

    def remove_excess_non_terminals(self):
        self.remove_all_rules_with_unattainable_non_terminal()
        self.remove_all_rules_with_unproductive_non_terminal()

    def find_vanishing_symbols(self):
        vanishing = []

        for rules_for_symbol in self.grammar.rules:
            if self.grammar.rules[rules_for_symbol] is None:
                vanishing.append(rules_for_symbol)

        for rules_for_symbol in self.grammar.rules:
            right_part = self.grammar.rules[rules_for_symbol]

            if isinstance(right_part, list):
                for symbol in right_part:
                    if isinstance(symbol, list):
                        for s in symbol:
                            if s in vanishing:
                                if not rules_for_symbol in vanishing:
                                    vanishing.append(rules_for_symbol)
                    else:
                        if symbol in vanishing:
                            if not rules_for_symbol in vanishing:
                                vanishing.append(rules_for_symbol)
            else:
                if right_part in vanishing:
                    if not rules_for_symbol in vanishing:
                        vanishing.append(rules_for_symbol)

# Project in development

toolkit = ToolKit(Grammar())

toolkit.remove_excess_non_terminals()

print(toolkit.grammar.show())
