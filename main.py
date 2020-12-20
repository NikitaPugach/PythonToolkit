class Grammar(object):
    def __init__(self):
        self.E = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-', '*', '/', '(', ')']
        self.N = ["FORMULA", "SIGN", "NUMBER", "DIGIT", "ALT", "DELETE"]
        self.S = self.N[0]
        self.rules = {self.S: [[self.S, self.N[1], self.S, self.N[4]], self.E[7]], self.N[2]: [self.N[1]], self.N[1]: self.E[0],
                      self.N[4]: None, self.N[5]: self.N[4], self.N[3]: [self.N[4], self.N[5]]}

    def show(self):
        print("Non-terminals: ", end="")
        print(self.N)
        print("Terminals", end="")
        print(self.E)
        print("Start Symbol:", end="")
        print(self.S)
        print("Rules", end="")
        print(self.rules)


def find_index(elem, array):
    for i in range(len(array)):
        if array[i] == elem:
            return i
    return -1


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
                        is_terminal = symbol in self.grammar.E  # Проверка все ли символы в правой части терминалы
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
                            if not is_terminal_or_from_alive:  # символы в правой части терминалы либо из alive
                                break

                    if is_terminal_or_from_alive:  # если да, то добавляем левую часть в alive
                        if not rules_for_symbols in alive:
                            alive.append(rules_for_symbols)

                else:
                    is_terminal_or_from_alive = right_part in self.grammar.E or right_part in alive
                    if is_terminal_or_from_alive:
                        if not rules_for_symbols in alive:
                            alive.append(rules_for_symbols)

            if alive_size == len(alive):  # Проверка расширилось ли alive
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

        expansion = True

        while expansion:
            vanishing_size = len(vanishing)

            for rules_for_symbol in self.grammar.rules:
                right_part = self.grammar.rules[rules_for_symbol]

                is_vanishing = False
                if isinstance(right_part, list):
                    for symbol in right_part:
                        if isinstance(symbol, list):
                            for s in symbol:
                                if s in vanishing:
                                    is_vanishing = True
                                else:
                                    is_vanishing = False
                                    break
                        else:
                            if symbol in vanishing:
                                is_vanishing = True
                            else:
                                is_vanishing = False
                                break
                    if is_vanishing is True:
                        if not rules_for_symbol in vanishing:
                            vanishing.append(rules_for_symbol)
                else:
                    if right_part in vanishing:
                        if not rules_for_symbol in vanishing:
                            vanishing.append(rules_for_symbol)

            if vanishing_size == len(vanishing):
                expansion = False

        return vanishing

    def remove_all_rules_with_vanishing_symbols(self):
        self.grammar.N = list(set(self.grammar.N) - set(self.find_vanishing_symbols()))

        [self.grammar.rules.pop(key) for key in self.find_vanishing_symbols()]

        change = True

        while change:
            change = False
            for rules_for_symbols in self.grammar.rules:
                right_part = self.grammar.rules[rules_for_symbols]

                if isinstance(right_part, list):
                    for symbol in right_part:
                        if isinstance(symbol, list):
                            for s in symbol:
                                if not s in self.grammar.N:
                                    if not s in self.grammar.E:
                                        change = True
                                        right_part.remove(symbol)
                        else:
                            if not symbol in self.grammar.N:
                                if not symbol in self.grammar.E:
                                    change = True
                                    self.grammar.rules.pop(symbol)
                else:
                    if not right_part in self.grammar.N:
                        if not right_part in self.grammar.E:
                            change = True
                            self.grammar.rules.pop(right_part)

    def create_graph(self):
        self.remove_all_rules_with_vanishing_symbols()

        array = [0] * len(self.grammar.N)
        for row in range(len(self.grammar.N)):
            array[row] = [0] * len(self.grammar.N)

        for rules_for_symbol in self.grammar.rules:
            right_part = self.grammar.rules[rules_for_symbol]

            if isinstance(right_part, list):
                for symbol in right_part:
                    if isinstance(symbol, list):
                        for s in symbol:
                            if s in self.grammar.N:
                                row = find_index(rules_for_symbol, self.grammar.N)
                                column = find_index(s, self.grammar.N)
                                array[row][column] = 1
                    else:
                        if symbol in self.grammar.N:
                            row = find_index(rules_for_symbol, self.grammar.N)
                            column = find_index(symbol, self.grammar.N)
                            array[row][column] = 1
                            print(self.grammar.N[row], end=" -> ")
                            print(self.grammar.N[column])

            else:
                if right_part in self.grammar.N:
                    row = find_index(rules_for_symbol, self.grammar.N)
                    column = find_index(right_part, self.grammar.N)
                    array[row][column] = 1

        return array

    def left_recursion_diagnosing(self):
        left_recursion_finder = LeftRecursionFinder(self)
        return left_recursion_finder.left_recursion_diagnosing()

    def getting_greybach_normal_form(self):
        V = self.find_vanishing_symbols()

        rules = self.grammar.rules

        # Первым шагом удаляем все правила вида: А -> є
        for rules_for_symbols in rules:
            right_part = rules[rules_for_symbols]

            if isinstance(right_part, list):
                for symbol in right_part:
                    if isinstance(symbol, list):
                        for s in symbol:
                            if s is None:
                                symbol.pop(symbol)
                    else:
                        if symbol is None:
                            right_part.pop(symbol)
            else:
                if right_part is None:
                    rules.pop(right_part)


        # Далее удалим все правила вида А -> а1V1 ... akVka(k+1)
        # И вставим вместо них новые
        deleted_rules = {}

        for rules_for_symbols in rules:
            right_part = rules[rules_for_symbols]

            if isinstance(right_part, list):
                for symbol in right_part:
                    if isinstance(symbol, list):
                        has_vanishing = False
                        for s in symbol:
                            if s in V:
                                has_vanishing = True
                        if has_vanishing:
                            right_part.pop(symbol)
                            deleted_rules[rules_for_symbols] = symbol

                            new_rules = self.create_new_rules_for_graibach(rules_for_symbols, symbol, V)
                            for r in new_rules:
                                right_part.append(r)
                    else:
                        if symbol in V:
                            right_part.pop(symbol)
                            deleted_rules[rules_for_symbols] = symbol
            else:
                if right_part in V:
                    rules.pop(right_part)
                    deleted_rules[rules_for_symbols] = right_part


    def create_new_rules_for_graibach(self, key, value, V):
        new_value_list = []
        i = 0
        # Далее создадим правила на базе удаленных:
        for symbol in value:
            if symbol in V:
                new_value = value
                new_value_list.append(new_value.copy())
                new_value[i] = None
                new_value_list.append(new_value.copy())
            i = i + 1
        return new_value_list



class LeftRecursionFinder(object):
    def __init__(self, toolkit):
        self.toolkit = toolkit
        self.graph = toolkit.create_graph()
        self.current_stack = []
        self.recursion_elements = []

    def left_recursion_diagnosing(self):
        for i in range(self.graph):
            for j in range(self.graph[i]):
                if self.graph[i][j] is 1:
                    self.current_stack.append(self.toolkit.grammar.N[i])
                    self.recursion(j)
                if len(self.current_stack) > len(set(self.current_stack)):
                    self.recursion_elements.append(self.current_stack[0])
        return self.recursion_elements

    def recursion(self, elem):
        array = self.graph[elem]

        for i in range(len(array)):
            if array[i] is 1:
                self.current_stack.append(self.toolkit.grammar.N[elem])
                self.recursion(i)


# Project in development

toolkit1 = ToolKit(Grammar())

print(toolkit1.left_recursion_diagnosing())
