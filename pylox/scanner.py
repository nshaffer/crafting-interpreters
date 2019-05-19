import lox
from token import Token
from token_types import *


KEYWORDS = {
    "and":    AND,
    "class":  CLASS,
    "else":   ELSE,
    "false":  FALSE,
    "for":    FOR,
    "fun":    FUN,
    "if":     IF,
    "nil":    NIL,
    "or":     OR,
    "print":  PRINT,
    "return": RETURN,
    "super":  SUPER,
    "this":   THIS,
    "true":   TRUE,
    "var":    VAR,
    "while":  WHILE
}


def is_digit(c):
    return '0' <= c <= '9'

    
def is_alpha(c):
    return ('a' <= c <= 'z') or ('A' <= c <= 'Z') or (c == '_')

    
def is_alphanumeric(c):
    return is_alpha(c) or is_digit(c)


class Scanner(object):
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0 
        self.line = 1
        return

    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        
        self.tokens.append(Token(EOF, "", None, self.line))
        return self.tokens

    def match(self, expected):
        if self.is_at_end() or self.source[self.current] != expected:
            return False
        else:
            self.current += 1
            return True

    def peek(self):
        if self.is_at_end():
            return '\0'
        else:
            return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        else:
            return self.source[self.current + 1]

    def scan_token(self):
        c = self.advance()
        # Single characters
        if   c == '(': self.add_token(LEFT_PAREN)
        elif c == ')': self.add_token(RIGHT_PAREN),
        elif c == '{': self.add_token(LEFT_BRACE),
        elif c == '}': self.add_token(RIGHT_BRACE),
        elif c == ',': self.add_token(COMMA),
        elif c == '.': self.add_token(DOT),
        elif c == '-': self.add_token(MINUS),
        elif c == '+': self.add_token(PLUS),
        elif c == ';': self.add_token(SEMICOLON),
        elif c == '*': self.add_token(STAR)
        # Disambiguate two-character relational ops (e.g., '!=' from '!')
        elif c == '!': self.add_token(BANG_EQUAL if self.match('=') else BANG)
        elif c == '=': self.add_token(EQUAL_EQUAL if self.match('=') else EQUAL)
        elif c == '<': self.add_token(LESS_EQUAL if self.match('=') else LESS)
        elif c == '>': self.add_token(GREATER_EQUAL if self.match('=') else GREATER)
        # Disambiguate comments from single slash
        elif c == '/':
            if self.match('/'): # # can safely skip to the next line
                while self.peek() != '\n' and not self.is_at_end():
                    self.advance()
            else:
                self.add_token(SLASH)
        # Whitespace (insignificant)
        elif c == ' ': pass
        elif c == '\r': pass
        elif c == '\t': pass
        elif c == '\n': self.line += 1
        # String literals
        elif c == '"': self.string()
        # Numeric literals
        elif is_digit(c): self.number()
        # Identifiers
        elif is_alpha(c): self.identifier()
        # Parse error
        else: lox.error(self.line, "Unexpected character")
        return

    def identifier(self):
        while is_alphanumeric(self.peek()):
            self.advance()
        text = self.source[self.start:self.current]

        # If it's not a reserved word, it's an identifier
        token_type = KEYWORDS.get(text, IDENTIFIER)

        self.add_token(token_type)
        return

    def number(self):
        # Integer part
        while is_digit(self.peek()):
            self.advance()

        # Fractional part
        if self.peek() == '.' and is_digit(self.peek_next()):
            self.advance()
            while is_digit(self.peek()):
                self.advance()

        value = float(self.source[self.start:self.current])
        self.add_token(NUMBER, value)
        return

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':  # Lox allows multi-line strings
                self.line += 1
            self.advance()

        if self.is_at_end():
            lox.error(self.line, "Unterminated string.")

        self.advance() # Consume closing quote
        value = self.source[self.start+1:self.current-1] # Trim off quotes
        self.add_token(STRING, value)
        return

    def is_at_end(self):
        return self.current >= len(self.source)

    def advance(self):
        self.current += 1
        return self.source[self.current-1]

    def add_token(self, token_type, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))
        return
            
