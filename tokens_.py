class Token():
    def __init__(self, type, value) -> None:
        self.type = type
        self.value = value
    
    def __repr__(self) -> str:
        return f"{self.type}({self.value})"


class INTEGER(Token):
    def __init__(self, value) -> None:
        super().__init__("INTEGER", value)

class FLOAT(Token):
    def __init__(self, value) -> None:
        super().__init__("FLOAT", value)

class PLUS(Token):
    def __init__(self, value) -> None:
        super().__init__("PLUS", value)

class MINUS(Token):
    def __init__(self, value) -> None:
        super().__init__("MINUS", value)

class MUL(Token):
    def __init__(self, value) -> None:
        super().__init__("MUL", value)

class POW(Token):
    def __init__(self, value) -> None:
        super().__init__("POW", value)

class DIV(Token):
    def __init__(self, value) -> None:
        super().__init__("DIV", value)

class INTDIV(Token):
    def __init__(self, value) -> None:
        super().__init__("INTDIV", value)

class MOD(Token):
    def __init__(self, value) -> None:
        super().__init__("MOD", value)

class LPAREN(Token):
    def __init__(self, value) -> None:
        super().__init__("LPAREN", value)

class RPAREN(Token):
    def __init__(self, value) -> None:
        super().__init__("RPAREN", value)

class ID(Token):
    def __init__(self, value) -> None:
        super().__init__("ID", value)

class ASSIGN(Token):
    def __init__(self, value) -> None:
        super().__init__("ASSIGN", value)

class SEMI(Token):
    def __init__(self, value) -> None:
        super().__init__("SEMI", value)

class EOF(Token):
    def __init__(self, value) -> None:
        super().__init__("EOF", value)