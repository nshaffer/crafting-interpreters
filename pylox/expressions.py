class Expr(object):
    def visit_binary(self, expr):
        raise RuntimeError('Method not implemented.')

    def visit_grouping(self, expr):
        raise RuntimeError('Method not implemented.')

    def visit_literal(self, expr):
        raise RuntimeError('Method not implemented.')

    def visit_unary(self, expr):
        raise RuntimeError('Method not implemented.')

    def accept(self, visitor):
        raise RuntimeError('Method not implemented.')


class Binary(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binary(self)


class Grouping(Expr):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_grouping(self)


class Literal(Expr):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal(self)


class Unary(Expr):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_unary(self)


