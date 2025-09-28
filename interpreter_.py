import ast_
import tokens_

import math


class Interpreter:
    def __init__(self, parser):
        self.parser = parser
        self.GLOBAL_SCOPE = {
            "pi": math.pi,
            "e": math.e,
            "tau": math.tau,
            "phi": (1 + math.sqrt(5)) / 2,
        }
        self.FUNC_TABLE = {
            "sqrt": math.sqrt,
            "cbrt": math.cbrt,
            "ceil": math.ceil,
            "floor": math.floor,
            "deg": math.degrees,
            "rad": math.radians,
            "exp": math.exp,
            "abs": math.fabs,
            "fact": math.factorial,
            "gamma": math.gamma,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "cot": lambda x: 1/math.tan(x),
            "sec": lambda x: 1/math.cos(x),
            "csc": lambda x: 1/math.sin(x),
            "sinh": math.sinh,
            "cosh": math.cosh,
            "tanh": math.tanh,
            "coth": lambda x: 1/math.tanh(x),
            "sech": lambda x: 1/math.cosh(x),
            "csch": lambda x: 1/math.sinh(x),
            "asin": math.asin,
            "acos": math.acos,
            "asec": lambda x: math.acos(1/x),
            "acsc": lambda x: math.asin(1/x),
            "asinh": math.asinh,
            "acosh": math.acosh,
            "asech": lambda x: math.acosh(1/x),
            "acsch": lambda x: math.asinh(1/x),
            "ln": math.log,
            "log": math.log10,
        }

    
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
        elif isinstance(node, ast_.FuncCall):
            return self.visit_FuncCall(node)
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
        if node.left.value in ["pi", "e", "phi", "tau"]:
            raise Exception(f"Cannot assign to constant '{node.left.value}'")
        var_name = node.left.value
        value = self.visit(node.right)
        self.GLOBAL_SCOPE[var_name] = value
        return value
    
    def visit_Compound(self, node):
        result = None
        for child in node.children:
            result = self.visit(child)  # last statement result
        return result   

    def visit_FuncCall(self, node):
        func_name = node.func_name.value
        if func_name not in self.FUNC_TABLE:
            raise Exception(f"Function '{func_name}' not defined")
        arg_val = self.visit(node.arg)
        return self.FUNC_TABLE[func_name](arg_val)
    
    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)
