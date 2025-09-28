import lexer_
import parser_
import interpreter_


# Integer division
lexer = lexer_.Lexer("7 // 2")
parser = parser_.Parser(lexer)
tree = parser.parse()
interpreter = interpreter_.Interpreter(parser)
print(interpreter.visit(tree))  # Output: 3

# Modulo
lexer = lexer_.Lexer("7 % 2")
parser = parser_.Parser(lexer)
tree = parser.parse()
interpreter = interpreter_.Interpreter(parser)
print(interpreter.visit(tree))  # Output: 1

# Combined
lexer = lexer_.Lexer("10 + 7 // 2 % 3")
parser = parser_.Parser(lexer)
tree = parser.parse()
interpreter = interpreter_.Interpreter(parser)
print(interpreter.visit(tree))  # Output: 10

lexer = lexer_.Lexer("2 ^ 3")
parser = parser_.Parser(lexer)
tree = parser.parse()
interpreter = interpreter_.Interpreter(parser)
print(interpreter.visit(tree))  # Output: 8

# Right-associative
lexer = lexer_.Lexer("2 ^ 3 ^ 2")
parser = parser_.Parser(lexer)
tree = parser.parse()
print(interpreter.visit(tree))  # Output: 512 (2^(3^2))

# Combined with other operators
lexer = lexer_.Lexer("2 + 3 ^ 2 * 2")
parser = parser_.Parser(lexer)
tree = parser.parse()
print(interpreter.visit(tree))  # Output: 20 (3^2 = 9 *2 =18 +2)

lexer = lexer_.Lexer("x = 5")
parser = parser_.Parser(lexer)
interpreter = interpreter_.Interpreter(parser)
print(interpreter.visit(parser.parse()))  # Output: 5

lexer = lexer_.Lexer("y = x + 3")
parser = parser_.Parser(lexer)
print(interpreter.visit(parser.parse()))  # Output: 8

lexer = lexer_.Lexer("y * 2")
parser = parser_.Parser(lexer)
print(interpreter.visit(parser.parse()))  # Output: 16
