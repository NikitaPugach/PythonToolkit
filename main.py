class Grammar(object):
    def __init__(self):
        self.E = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-', '*', '/', '(', ')']
        self.N = ["FORMULA", "SIGN", "NUMBER", "DIGIT"]
        self.S = self.N[0]
        self.rules = {self.S: [self.S, self.N[1], self.S]}


class ToolKit(object):
    def __init__(self):
        self.grammar = Grammar()

    def remove_unproductive_non_terminal(self):
        alive = []
        for rule in self.grammar.rules:
            rule.