import expressions

class AstPrinter(expressions.Expr):
    def print(self, expr):
        return expr.accept(self)

    def visit_binary(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping(self, expr):
        return self.parenthesize("group", expr.expression)

    def visit_literal(self, expr):
        if (expr.value == None):
            return "nil"
        else:
            return str(expr.value)

    def visit_unary(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name, *exprs):
        s = "({0}".format(name)
        for expr in exprs:
            s += " {0}".format(expr.accept(self))
        s += ")"
        return s
        

# if __name__ == "__main__":
#     from expressions import Binary, Grouping, Literal, Unary
#     from token import Token
#     from token_types import *

#     expr = Binary(Unary(Token(MINUS, "-", None, 1),
#                         Literal(123)),
#                   Token(STAR, "*", None, 1),
#                   Grouping(Literal(45.67)))
    
#     print AstPrinter().print(expr)
