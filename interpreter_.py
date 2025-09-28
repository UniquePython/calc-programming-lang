import ast_
import tokens_


class Interpreter:
    def __init__(self, parser):
        self.parser = parser
        self.GLOBAL_SCOPE = {}
    
    def visit(self, node):
        if isinstance(node, ast_.Num):
            return self.visit_Num(node)
        elif isinstance(node, ast_.BinOp):
            return self.visit_BinOp(node)
        elif isinstance(node, ast_.Var):
            return self.visit_Var(node)
        elif isinstance(node, ast_.Assign):
            return self.visit_Assign(node)
        elif isinstance(node, ast_.Compound):
            return self.visit_Compound(node)
        else:
            raise Exception(f"No visit method for {type(node)}")
    
    def visit_Num(self, node):
        return node.value
    
    def visit_BinOp(self, node):
        if isinstance(node.op, tokens_.PLUS):
            return self.visit(node.left) + self.visit(node.right)
        elif isinstance(node.op, tokens_.MINUS):
            return self.visit(node.left) - self.visit(node.right)
        elif isinstance(node.op, tokens_.MUL):
            return self.visit(node.left) * self.visit(node.right)
        elif isinstance(node.op, tokens_.DIV):
            return self.visit(node.left) / self.visit(node.right)
        elif isinstance(node.op, tokens_.INTDIV):
            return self.visit(node.left) // self.visit(node.right)
        elif isinstance(node.op, tokens_.MOD):
            return self.visit(node.left) % self.visit(node.right)
        elif isinstance(node.op, tokens_.POW):
            return self.visit(node.left) ** self.visit(node.right)
    
    def visit_Var(self, node):
        var_name = node.value
        if var_name in self.GLOBAL_SCOPE:
            return self.GLOBAL_SCOPE[var_name]
        else:
            raise Exception(f"Variable '{var_name}' not defined")

    def visit_Assign(self, node):
        var_name = node.left.value
        value = self.visit(node.right)
        self.GLOBAL_SCOPE[var_name] = value
        return value
    
    def visit_Compound(self, node):
        result = None
        for child in node.children:
            result = self.visit(child)  # last statement result
        return result   

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)
