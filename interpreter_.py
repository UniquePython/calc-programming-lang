import ast_
import tokens_


class Interpreter:
    def __init__(self, parser):
        self.parser = parser
    
    def visit(self, node):
        if isinstance(node, ast_.Num):
            return self.visit_Num(node)
        elif isinstance(node, ast_.BinOp):
            return self.visit_BinOp(node)
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

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)
