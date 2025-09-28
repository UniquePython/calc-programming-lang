class AST:
    pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left  # Var node
        self.op = op      # should be '=' token
        self.right = right

class Compound(AST):
    """Represents multiple statements"""
    def __init__(self):
        self.children = []
