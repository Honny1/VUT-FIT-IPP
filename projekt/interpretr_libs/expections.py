
class UnexpectedXMLStructureError(Exception):
    exit_code = 32


class NotExistFrameError(Exception):
    exit_code = 55


class MissingValueError(Exception):
    exit_code = 56


class SemanticError(Exception):
    exit_code = 52


class BadDataType(Exception):
    exit_code = 53


class BadStringOperation(Exception):
    exit_code = 58


class BadOperandValue(Exception):
    exit_code = 57


class UndefinedVar(Exception):
    exit_code = 54


class StatsMissingFile(Exception):
    exit_code = 10


class TooMuchJumps(Exception):
    exit_code = 99
