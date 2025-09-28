from lexer_ import Lexer
from parser_ import Parser
from interpreter_ import Interpreter

import math

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
        
        if abs(result) > 1e15:
            raise Exception("Result too large (approaching infinity)")
        
        if math.isinf(result):
            raise Exception("Result infinite")
        elif math.isnan(result):
            raise Exception("Result undefined")
        
        if result is not None:
            print(result)
    except Exception as e:
        print(e)
