class Token(object):
    def __init__(self, token_type, lexeme, literal, line):
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
        return

    def __str__(self):
        return "{token_type:} {lexeme:} {literal:}".format(**self.__dict__)

    
        
    
