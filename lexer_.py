import tokens_


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None
    
    def advance(self):
        """Move to the next character"""
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
    
    def skip_whitespace(self):
        """Skips whitespaces"""
        while self.current_char and self.current_char.isspace():
            self.advance()
    
    def number(self):
        """Read an integer or float"""
        result = ""
        has_dot = False

        while self.current_char and (self.current_char.isdigit() or self.current_char == "."):
            if self.current_char == ".":
                if has_dot:  # second dot not allowed
                    raise Exception("Invalid number format")
                has_dot = True
            result += self.current_char
            self.advance()
        
        if has_dot:
            return tokens_.FLOAT(float(result))
        else:
            return tokens_.INTEGER(int(result))
    
    
    def get_next_token(self):
        """Lexical analyzer (scanner)"""
        while self.current_char:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit() or self.current_char == ".":
                return self.number()

            if self.current_char == '+':
                self.advance()
                return tokens_.PLUS("+")

            if self.current_char == '-':
                self.advance()
                return tokens_.MINUS("-")

            if self.current_char == '*':
                self.advance()
                return tokens_.MUL("*")

            if self.current_char == '^':
                self.advance()
                return tokens_.POW("^")

            if self.current_char == '/':
                self.advance()
                
                if self.current_char == '/':
                    self.advance()
                    return tokens_.INTDIV("//")
                return tokens_.DIV("/")

            if self.current_char == '%':
                self.advance()
                return tokens_.MOD("%")

            if self.current_char == '/':
                self.advance()
                return tokens_.DIV("/")

            if self.current_char == '(':
                self.advance()
                return tokens_.LPAREN("(")

            if self.current_char == ')':
                self.advance()
                return tokens_.RPAREN(")")

            raise Exception(f"Invalid character: {self.current_char}")
        
        return tokens_.EOF(None)