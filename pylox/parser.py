import lox
import expressions
from token_types import *


class Parser(object):
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        try:
            return self.expression()
        except ParseError as e:
            return None
        
    def match(self, *token_types):
        """
        Consume the current token if its type matches any of a given list.
        """
        for token_type in token_types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def check(self, token_type):
        """
        Check if the current token's type matches a given one.
        """
        if (self.is_at_end()):
            return False
        else:
            return token_type == self.peek().token_type

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self):
        return self.peek().token_type == EOF

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]
        
    def expression(self):
        """
        expression : equality
        """
        return self.equality()

    def equality(self):
        """
        equality : comparison ( ( "!=" | "==" ) comparison )*
        """
        expr = self.comparison()

        while self.match(BANG_EQUAL, EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = expressions.Binary(expr, operator, right)

        return expr

    def comparison(self):
        """
        comparison : addition ( ( ">" | ">=" | "<" | "<=" ) addition )*
        """
        expr = self.addition()

        while self.match(GREATER, GREATER_EQUAL, LESS, LESS_EQUAL):
            operator = self.previous()
            right = self.additon()
            expr = expressions.Binary(expr, operator, right)

        return expr

    def addition(self):
        """
        addition : multiplication ( ( "-" | "+" ) multiplication )*
        """
        expr = self.multiplication()

        while self.match(MINUS, PLUS):
            operator = self.previous()
            right = self.multiplication()
            expr = expressions.Binary(expr, operator, right)

        return expr

    def multiplication(self):
        """
        multiplication : unary ( ( "/" | "*" ) unary )*
        """
        expr = self.unary()

        while self.match(SLASH, STAR):
            operator = self.previous()
            right = self.unary()
            expr = expressions.Binary(expr, operator, right)

        return expr
        
    def unary(self):
        """
        unary : ( "!" | "-" ) unary
              | primary
        """
        if self.match(BANG, MINUS):
            operator = self.previous()
            right = self.unary()
            expr = expressions.Unary(operator, right)
        else:
            expr = self.primary()

        return expr

    def primary(self):
        """
        primary : NUMBER 
                | STRING 
                | "false" 
                | "true" 
                | "nil"
                | "(" expression ")"
        """
        if self.match(NUMBER, STRING):
            return expressions.Literal(self.previous().literal)
        elif self.match(FALSE):
            return expressions.Literal(False)
        elif self.match(TRUE):
            return expressions.Literal(True)
        elif self.match(NIL):
            return expressions.Literal(None)
        elif self.match(LEFT_PAREN):
            expr = self.expression()
            self.consume(RIGHT_PAREN, "Expect ')' after expression.")
            return expressions.Grouping(expr)
        else:
            raise self.error(self.peek(), "Expect expression.")

    def consume(self, token_type, message):
        if self.check(token_type):
            return self.advance()
        else:
            raise self.error(self.peek(), message)
        return

    def error(self, token_type, message):
        lox.error(token_type, message)
        return ParseError()

    def synchronize(self):
        self.advance()

        while not self.is_at_end():
            if self.previous().token_type == SEMICOLON:
                return
            elif self.peek().token_type in (CLASS, FUN, VAR, FOR, IF, WHILE, PRINT, RETURN):
                return
            else:
                self.advance()
        return

    
            
                
    


            
class ParseError(Exception):
    pass
