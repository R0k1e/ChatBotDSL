class NotExistError(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Error: " + self.name + " does not exist"


class FuncNotExistError(NotExistError):
    def __str__(self):
        return "Error: Function " + self.name + " does not exist"


class VarNotExistError(NotExistError):
    def __str__(self):
        return "Error: Variable " + self.name + " does not exist"


class DupError(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Error: " + self.name + " already exist, it cannot be defined again"


class FuncDupError(DupError):
    def __str__(self):
        return "Error: Function " + self.name + " already exist, it cannot be defined again"


class SyntaxError(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Error: " + self.name + " is not a valid syntax"
    
class ExpressionError(Exception):
    def __init__(self, left, right, op):
        self.left = left
        self.right = right
        self.op = op
    
    def __str__(self) -> str:
        return "Error: " + self.left + " " + self.op + " " + self.right + " is not a valid expression"
