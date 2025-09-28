from lexer_ import Lexer
from parser_ import Parser
from interpreter_ import Interpreter

interpreter = Interpreter(None)

print("Welcome to your calculator! Type 'exit' to quit.")

while True:
    try:
        text = input("> ")
        if text.strip().lower() == "exit":
            break
        if not text.strip():
            continue

        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter.parser = parser
        result = interpreter.visit(parser.parse())
        if result is not None:
            print(result)
    except Exception as e:
        print(e)
