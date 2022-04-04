
class ArgType:
    VAR = "var"
    SYMBOL = "symb"
    LABEL = "label"
    TYPE = "type"


class ArgDataType:
    NIL = "nil"
    INT = "int"
    BOOL = "bool"
    STR = "string"


class ArgFrame:
    GF = "GF"
    TF = "TF"
    LF = "LF"


class ArgIndexes:
    ARG1 = 0
    ARG2 = 1
    ARG3 = 2


class Argument:
    def __init__(self, type, value):
        self.type = type
        self.value = value


class Var(Argument):
    def __init__(self, value, frame):
        super().__init__(ArgType.VAR, value)
        self.frame = frame

    def __repr__(self):
        return f"VAR: {self.frame}, {self.value}"


class TypeArg(Argument):
    def __init__(self, value):
        super().__init__(ArgType.TYPE, value)

    def __repr__(self):
        return f"TYPE: {self.value}"


class Label(Argument):
    def __init__(self, value):
        super().__init__(ArgType.LABEL, value)

    def __repr__(self):
        return f"LABEL: {self.value}"


class Symbol(Argument):
    def __init__(self, data_type, value):
        super().__init__(ArgType.SYMBOL, value)
        self.data_type = data_type

    def __eq__(self, _o):
        return self.value == _o.value and self.data_type == _o.data_type

    def __lt__(self, _o):
        return self.value < _o.value

    def __gt__(self, _o):
        return self.value > _o.value

    def __repr__(self):
        return f"SYMBOL: {self.data_type}, {self.value}"
