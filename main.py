import lexer_
import parser_
import interpreter_


lexer = lexer_.Lexer("x = 5; y = x + 3; y * 2")
parser = parser_.Parser(lexer)
interpreter = interpreter_.Interpreter(parser)
print(interpreter.visit(parser.parse()))  # Output: 16
