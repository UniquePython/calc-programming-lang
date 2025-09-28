import tokens_
import ast_


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
    
    def eat(self, token_type):
        if isinstance(self.current_token, token_type):
            self.current_token = self.lexer.get_next_token()
        else:
            raise Exception(f"Unexpected token {self.current_token}, expected {token_type}")
    
    def peek(self):
        """Return the next token without consuming current"""
        saved_pos = self.lexer.pos
        saved_char = self.lexer.current_char
        token = self.lexer.get_next_token()
        # restore lexer state
        self.lexer.pos = saved_pos
        self.lexer.current_char = saved_char
        return token
    
    def assignment(self):
        if isinstance(self.current_token, tokens_.ID):
            var_token = self.current_token
            # Temporarily advance to check next token
            saved_pos = self.lexer.pos
            saved_char = self.lexer.current_char
            self.eat(tokens_.ID)
            if self.current_token.type == "ASSIGN":
                op = self.current_token
                self.eat(tokens_.ASSIGN)
                right = self.expr()
                return ast_.Assign(ast_.Var(var_token), op, right)
            else:
                # restore lexer state if no assignment
                self.lexer.pos = saved_pos - 1  # -1 because eat() advanced
                self.lexer.current_char = saved_char
                self.current_token = var_token
        return self.expr()

    def factor(self):
        """factor : (PLUS | MINUS) factor | INTEGER | FLOAT | LPAREN expr RPAREN | ID"""
        token = self.current_token

        if token.type == "PLUS":
            self.eat(tokens_.PLUS)
            node = self.factor()
            return ast_.BinOp(left=ast_.Num(tokens_.INTEGER(0)), op=token, right=node)

        elif token.type == "MINUS":
            self.eat(tokens_.MINUS)
            node = self.factor()
            return ast_.BinOp(left=ast_.Num(tokens_.INTEGER(0)), op=token, right=node)

        elif token.type == "INTEGER":
            self.eat(tokens_.INTEGER)
            return ast_.Num(token)

        elif token.type == "FLOAT":
            self.eat(tokens_.FLOAT)
            return ast_.Num(token)

        elif token.type == "LPAREN":
            self.eat(tokens_.LPAREN)
            node = self.expr()
            self.eat(tokens_.RPAREN)
            return node

        elif token.type == "ID":
            next_token = self.peek()
            if next_token.type == "LPAREN":
                func_name = token
                self.eat(tokens_.ID)
                self.eat(tokens_.LPAREN)

                args = []
                if self.current_token.type != "RPAREN":
                    args.append(self.expr())
                    while self.current_token.type == "COMMA":
                        self.eat(tokens_.COMMA)
                        args.append(self.expr())

                self.eat(tokens_.RPAREN)
                return ast_.FuncCall(func_name, args)
            else:
                self.eat(tokens_.ID)
                return ast_.Var(token)

        else:
            raise Exception(f"Unexpected token in factor: {token}")


    def power(self):
        """power : factor (POW power)?  (right-associative)"""
        node = self.factor()
        
        while self.current_token.type == "POW":
            token = self.current_token
            self.eat(tokens_.POW)
            node = ast_.BinOp(left=node, op=token, right=self.power())
        
        return node


    def term(self):
        """term : power ((MUL | DIV | INTDIV | MOD) power)*"""
        node = self.power()
        
        while self.current_token.type in ("MUL", "DIV", "INTDIV", "MOD"):
            token = self.current_token
            if isinstance(token, tokens_.MUL):
                self.eat(tokens_.MUL)
            elif isinstance(token, tokens_.DIV):
                self.eat(tokens_.DIV)
            elif isinstance(token, tokens_.INTDIV):
                self.eat(tokens_.INTDIV)
            elif isinstance(token, tokens_.MOD):
                self.eat(tokens_.MOD)
            node = ast_.BinOp(left=node, op=token, right=self.power())
        
        return node


    def expr(self):
        """expr : term ((PLUS | MINUS) term)*"""
        node = self.term()
        
        while self.current_token.type in ("PLUS", "MINUS"):
            token = self.current_token
            if isinstance(token, tokens_.PLUS):
                self.eat(tokens_.PLUS)
            elif isinstance(token, tokens_.MINUS):
                self.eat(tokens_.MINUS)
            node = ast_.BinOp(left=node, op=token, right=self.term())
        
        return node

    def statement(self):
        """Single statement: assignment or expression"""
        if self.current_token.type == "ID":
            next_token = self.peek()
            if next_token.type == "ASSIGN":
                left = ast_.Var(self.current_token)
                self.eat(tokens_.ID)
                op = self.current_token
                self.eat(tokens_.ASSIGN)
                right = self.expr()
                return ast_.Assign(left, op, right)
        # Otherwise, just an expression
        return self.expr()


    def statement_list(self):
        """Handle multiple statements separated by semicolons"""
        node = ast_.Compound()
        node.children.append(self.statement())
        
        while self.current_token and self.current_token.type == "SEMI":
            self.eat(tokens_.SEMI)
            node.children.append(self.statement())
        
        return node

    def parse(self):
        return self.statement_list()
