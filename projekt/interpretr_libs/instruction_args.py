from interpretr_libs.expections import BadDataType, BadOperandValue


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

    def _is_comparable(self, _o, enable_null_compare=False):
        supporeted_types = (ArgDataType.INT, ArgDataType.BOOL, ArgDataType.STR)
        if enable_null_compare:
            supporeted_types = (ArgDataType.INT, ArgDataType.BOOL, ArgDataType.STR, ArgDataType.NIL)
        if self.data_type not in supporeted_types or _o.data_type not in supporeted_types:
            raise BadDataType("COMPARE INSTRUCTION: Support just INT, BOOL, STRING or NIL for EQ!")
        is_one_nil = self.data_type == ArgDataType.NIL or _o.data_type == ArgDataType.NIL
        if self.data_type != _o.data_type and not is_one_nil:
            raise BadDataType("COMPARE INSTRUCTION: Cant compare different types!")
        return True

    def is_bool(self, _o):
        if self.data_type == ArgDataType.BOOL and _o.data_type == ArgDataType.BOOL:
            return True
        raise BadDataType("LOGICAL INSTRUCTION: Support just BOOL!")

    def _is_int(self, _o):
        if self.data_type == ArgDataType.INT and _o.data_type == ArgDataType.INT:
            return True
        raise BadDataType("MATH INSTRUCTION: Support just INT!")

    def __eq__(self, _o):
        self._is_comparable(_o, True)
        return self.value == _o.value

    def __ne__(self, _o):
        self._is_comparable(_o, True)
        return self.value != _o.value

    def __lt__(self, _o):
        self._is_comparable(_o)
        return self.value < _o.value

    def __gt__(self, _o):
        self._is_comparable(_o)
        return self.value > _o.value

    def __add__(self, _o):
        self._is_int(_o)
        return Symbol(ArgDataType.INT, self.value + _o.value)

    def __sub__(self, _o):
        self._is_int(_o)
        return Symbol(ArgDataType.INT, self.value - _o.value)

    def __mul__(self, _o):
        self._is_int(_o)
        return Symbol(ArgDataType.INT, self.value * _o.value)

    def __floordiv__(self, _o):
        self._is_int(_o)
        if _o.value == 0:
            raise BadOperandValue("IDIV: Division ZERO!")
        return Symbol(ArgDataType.INT, self.value // _o.value)

    def __repr__(self):
        return f"SYMBOL: {self.data_type}, {self.value}"
