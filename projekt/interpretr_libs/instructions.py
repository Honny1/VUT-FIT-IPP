from sys import exit as sys_exit, stderr
from interpretr_libs.expections import (
    BadDataType, BadOperandValue,
    BadStringOperation, MissingValueError, UnexpectedXMLStructureError)
from interpretr_libs.instruction_args import ArgDataType, ArgType, Symbol, ArgIndexes
from interpretr_libs.expections import NotExistFrameError, SemanticError, TooMuchJumps


class Instruction:
    expected_args = []

    def __init__(self, opcode, args, order):
        self.opcode = opcode
        self.args = args
        self.order = order
        if len(args) != len(self.expected_args):
            raise UnexpectedXMLStructureError(
                f"Unexpected number of operands! Instruction order: {self.order}"
            )

    def exec(self, engine):
        raise NotImplementedError

    def __repr__(self):
        return f"{self.opcode}: {self.args}"

    def _get_symbol_operands(self, engine):
        symbol1 = engine.get_symbol_value(self.args[ArgIndexes.ARG2])
        symbol2 = engine.get_symbol_value(self.args[ArgIndexes.ARG3])
        return (symbol1, symbol2)

    def _get_symbol_operands_from_stack(self, engine):
        if not engine.stack_data:
            raise MissingValueError(
                f"STACK MATH OPERATION: empty stack! Instruction order: {self.order}"
                )
        symbol2 = engine.stack_data.pop()
        if not engine.stack_data:
            raise MissingValueError(
                f"STACK MATH OPERATION: empty stack! Instruction order: {self.order}"
            )
        symbol1 = engine.stack_data.pop()
        return (symbol1, symbol2)

    def _save_symbol(self, engine, symbol, arg_index=ArgIndexes.ARG1):
        engine.set_var(self.args[arg_index], symbol)

    def _save_symbol_stack(self, engine, symbol):
        engine.stack_data.append(symbol)


class InstructionMOVE(Instruction):
    expected_args = [ArgType.VAR, ArgType.SYMBOL]

    def exec(self, engine):
        symbol_value = engine.get_symbol_value(self.args[ArgIndexes.ARG2])
        engine.set_var(self.args[ArgIndexes.ARG1], symbol_value)


class InstructionCREATEFRAME(Instruction):

    def exec(self, engine):
        engine.TF = dict()


class InstructionPUSHFRAME(Instruction):

    def exec(self, engine):
        if engine.TF is None:
            raise NotExistFrameError(f"PUSHFRAME: frame not exist! Instruction order: {self.order}")
        engine.stack_LF.append(engine.TF)
        engine.TF = None


class InstructionPOPFRAME(Instruction):

    def exec(self, engine):
        if not engine.stack_LF:
            raise NotExistFrameError(
                f"POPFRAME: empty frame stack! Instruction order: {self.order}"
            )
        engine.TF = engine.stack_LF.pop()


class InstructionDEFVAR(Instruction):
    expected_args = [ArgType.VAR]

    def exec(self, engine):
        var = self.args[ArgIndexes.ARG1]
        if engine.is_var_exist(var):
            raise SemanticError(f"DEFVAR: Variable exist! Instruction order: {self.order}")
        engine.create_var(var, None)


class InstructionPUSHS(Instruction):
    expected_args = [ArgType.SYMBOL]

    def exec(self, engine):
        symbol = engine.get_symbol_value(self.args[ArgIndexes.ARG1])
        engine.stack_data.append(symbol)


class InstructionPOPS(Instruction):
    expected_args = [ArgType.VAR]

    def exec(self, engine):
        if not engine.stack_data:
            raise MissingValueError(f"POPS: empty stack! Instruction order: {self.order}")
        engine.set_var(self.args[ArgIndexes.ARG1], engine.stack_data.pop())


class InstructionADD(Instruction):
    expected_args = [ArgType.VAR, ArgType.SYMBOL, ArgType.SYMBOL]

    def exec(self, engine):
        symbol1, symbol2 = self._get_symbol_operands(engine)

        self._save_symbol(engine, symbol1 + symbol2)


class InstructionSUB(Instruction):
    expected_args = [ArgType.VAR, ArgType.SYMBOL, ArgType.SYMBOL]

    def exec(self, engine):
        symbol1, symbol2 = self._get_symbol_operands(engine)

        self._save_symbol(engine, symbol1 - symbol2)


class InstructionMUL(Instruction):
    expected_args = [ArgType.VAR, ArgType.SYMBOL, ArgType.SYMBOL]

    def exec(self, engine):
        symbol1, symbol2 = self._get_symbol_operands(engine)

        self._save_symbol(engine, symbol1 * symbol2)


class InstructionIDIV(Instruction):
    expected_args = [ArgType.VAR, ArgType.SYMBOL, ArgType.SYMBOL]

    def exec(self, engine):
        symbol1, symbol2 = self._get_symbol_operands(engine)

        self._save_symbol(engine, symbol1 // symbol2)


class InstructionLT(Instruction):
    expected_args = [ArgType.VAR, ArgType.SYMBOL, ArgType.SYMBOL]

    def exec(self, engine):
        symbol1, symbol2 = self._get_symbol_operands(engine)

        self._save_symbol(engine, Symbol(ArgDataType.BOOL, symbol1 < symbol2))


class InstructionGT(Instruction):
    expected_args = [ArgType.VAR, ArgType.SYMBOL, ArgType.SYMBOL]

    def exec(self, engine):
        symbol1, symbol2 = self._get_symbol_operands(engine)

        self._save_symbol(engine, Symbol(ArgDataType.BOOL, symbol1 > symbol2))


class InstructionEQ(Instruction):
    expected_args = [ArgType.VAR, ArgType.SYMBOL, ArgType.SYMBOL]

    def exec(self, engine):
        symbol1, symbol2 = self._get_symbol_operands(engine)

        self._save_symbol(engine, Symbol(ArgDataType.BOOL, symbol1 == symbol2))


class InstructionAND(Instruction):
    expected_args = [ArgType.VAR, ArgType.SYMBOL, ArgType.SYMBOL]

    def exec(self, engine):
        symbol1, symbol2 = self._get_symbol_operands(engine)
        symbol1.is_bool(symbol2)
        self._save_symbol(engine, Symbol(ArgDataType.BOOL, symbol1.value and symbol2.value))


class InstructionOR(Instruction):
    expected_args = [ArgType.VAR, ArgType.SYMBOL, ArgType.SYMBOL]

    def exec(self, engine):
        symbol1, symbol2 = self._get_symbol_operands(engine)
        symbol1.is_bool(symbol2)
        self._save_symbol(engine, Symbol(ArgDataType.BOOL, symbol1.value or symbol2.value))


class InstructionNOT(Instruction):
    expected_args = [ArgType.VAR, ArgType.SYMBOL]

    def exec(self, engine):
        symbol = engine.get_symbol_value(self.args[ArgIndexes.ARG2])
        if symbol.data_type != ArgDataType.BOOL:
            raise BadDataType("LOGICAL INSTRUCTION: Support just BOOL!")
        self._save_symbol(engine, Symbol(ArgDataType.BOOL, not symbol.value))


class InstructionINT2CHAR(Instruction):
    expected_args = [ArgType.VAR, ArgType.SYMBOL]

    def exec(self, engine):
        symbol = engine.get_symbol_value(self.args[ArgIndexes.ARG2])
        if symbol.data_type != ArgDataType.INT:
            raise BadDataType(f"INT2CHAR: Support just INT! Instruction order: {self.order}")
        try:
            self._save_symbol(engine, Symbol(ArgDataType.STR, chr(symbol.value)))
        except (TypeError, ValueError):
            raise BadStringOperation((
                f"INT2CHAR: Bad int to char corversion: {symbol.value},"
                f" Instruction order: {self.order}"
            ))


class InstructionSTRING2INT(Instruction):
    expected_args = [ArgType.VAR, ArgType.SYMBOL, ArgType.SYMBOL]

    def exec(self, engine):
        symbol1, symbol2 = self._get_symbol_operands(engine)

        if symbol1.data_type != ArgDataType.STR or symbol2.data_type != ArgDataType.INT:
            raise BadDataType(f"STRING2INT: Bad type of operands! Instruction order: {self.order}")

        if symbol2.value < 0:
            raise BadStringOperation(
                f"STRING2INT: Index out of the range! Instruction order: {self.order}"
            )
        try:
            self._save_symbol(engine, Symbol(ArgDataType.INT, ord(symbol1.value[symbol2.value])))
        except IndexError:
            raise BadStringOperation(
                f"STRING2INT: Index out of the range! Instruction order: {self.order}"
            )
        except (TypeError, ValueError):
            raise BadStringOperation((
                f"Bad int to char corversion: {symbol1.value[symbol2.value]}, "
                f"Instruction order: {self.order}"
            ))


class InstructionREAD(Instruction):
    expected_args = [ArgType.VAR, ArgType.TYPE]

    def exec(self, engine):
        data = None
        try:
            if engine.user_input == "<stdin>":
                data = input()
            if not isinstance(engine.user_input, str):
                data = engine.user_input.readline()
        except Exception:
            data = None
        type_ = self.args[ArgIndexes.ARG2]

        if data is None or data == "":
            self._save_symbol(engine, Symbol(ArgDataType.NIL, None))
            return
        if type_.value == ArgDataType.BOOL:
            str_to_bool = {"true": True, "false": False}
            data = data.rstrip().lower()
            if data not in str_to_bool:
                self._save_symbol(engine, Symbol(ArgDataType.BOOL, str_to_bool["false"]))
            else:
                self._save_symbol(engine, Symbol(ArgDataType.BOOL, str_to_bool[data]))
            return
        if type_.value == ArgDataType.STR:
            self._save_symbol(engine, Symbol(ArgDataType.STR, data.rstrip()))
            return
        if type_.value == ArgDataType.INT:
            try:
                int_val = int(data.rstrip())
                self._save_symbol(engine, Symbol(ArgDataType.INT, int_val))
            except ValueError:
                self._save_symbol(engine, Symbol(ArgDataType.NIL, None))
            return


class InstructionWRITE(Instruction):
    expected_args = [ArgType.SYMBOL]

    def exec(self, engine):
        symbol = engine.get_symbol_value(self.args[ArgIndexes.ARG1])

        if symbol.data_type == ArgDataType.NIL:
            print("", end="")
            return
        if symbol.data_type == ArgDataType.BOOL:
            print(str(symbol.value).lower(), end="")
            return
        print(symbol.value, end="")


class InstructionCONCAT(Instruction):
    expected_args = [ArgType.VAR, ArgType.SYMBOL, ArgType.SYMBOL]

    def exec(self, engine):
        symbol1, symbol2 = self._get_symbol_operands(engine)

        if symbol1.data_type != ArgDataType.STR or symbol2.data_type != ArgDataType.STR:
            raise BadDataType((
                f"CONCAT: Bad type of operands! Just string are supported."
                f" Instruction order: {self.order}"
            ))
        self._save_symbol(engine, Symbol(ArgDataType.STR, f"{symbol1.value}{symbol2.value}"))


class InstructionSTRLEN(Instruction):
    expected_args = [ArgType.VAR, ArgType.SYMBOL]

    def exec(self, engine):
        symbol = engine.get_symbol_value(self.args[ArgIndexes.ARG2])

        if symbol.data_type != ArgDataType.STR:
            raise BadDataType((
                f"STRLEN: Bad type of operands! Just string is supported. "
                f"Instruction order: {self.order}"
            ))
        self._save_symbol(engine, Symbol(ArgDataType.INT, len(symbol.value)))


class InstructionGETCHAR(Instruction):
    expected_args = [ArgType.VAR, ArgType.SYMBOL, ArgType.SYMBOL]

    def exec(self, engine):
        symbol1, symbol2 = self._get_symbol_operands(engine)

        if symbol2.data_type != ArgDataType.INT or symbol1.data_type != ArgDataType.STR:
            raise BadDataType(f"GETCHAR: Bad type of operands! Instruction order: {self.order}")
        if symbol2.value < 0:
            raise BadStringOperation(
                f"GETCHAR: Index out of the range! Instruction order: {self.order}"
            )
        try:
            self._save_symbol(engine, Symbol(ArgDataType.STR, symbol1.value[symbol2.value]))
        except IndexError:
            raise BadStringOperation(
                f"GETCHAR: Index out of the range! Instruction order: {self.order}"
            )


class InstructionSETCHAR(Instruction):
    expected_args = [ArgType.VAR, ArgType.SYMBOL, ArgType.SYMBOL]

    def exec(self, engine):
        var = engine.get_var(self.args[ArgIndexes.ARG1])
        symbol1, symbol2 = self._get_symbol_operands(engine)

        if var is None:
            raise MissingValueError(f"SETCHAR: Undefined value! Instruction order: {self.order}")

        type_of_symbol1 = symbol1.data_type != ArgDataType.INT
        type_of_symbol2 = symbol2.data_type != ArgDataType.STR
        type_of_var = var.data_type != ArgDataType.STR

        if type_of_symbol1 or type_of_symbol2 or type_of_var:
            raise BadDataType(f"SETCHAR: Bad type of operands! Instruction order: {self.order}")

        if symbol1.value < 0 or symbol1.value > len(var.value)-1:
            raise BadStringOperation(
                f"SETCHAR: Index out of the range! Instruction order: {self.order}"
            )
        try:
            result = var.value[:symbol1.value] + symbol2.value[0] + var.value[symbol1.value + 1:]
            self._save_symbol(engine, Symbol(ArgDataType.STR, result))
        except IndexError:
            raise BadStringOperation("SETCHAR: Index out of the range!")


class InstructionTYPE(Instruction):
    expected_args = [ArgType.VAR, ArgType.SYMBOL]

    def exec(self, engine):
        symbol = engine.get_symbol_value(self.args[ArgIndexes.ARG2], True)
        if symbol is None:
            self._save_symbol(engine, Symbol(ArgDataType.STR, ""))
            return
        self._save_symbol(engine, Symbol(ArgDataType.STR, symbol.data_type))


class InstructionLABEL(Instruction):
    expected_args = [ArgType.LABEL]

    def exec(self, engine):
        return


class InstructionJUMP(Instruction):
    expected_args = [ArgType.LABEL]

    def _check_if_label_exist(self, label, engine):
        if label not in engine.labels.keys():
            raise SemanticError(f"Undefined Label: {label} Instruction order: {self.order}")

    def exec(self, engine):
        if engine.MAX_NUMBER_OF_JUMPS == engine.number_of_jumps:
            raise TooMuchJumps("ERROR: Maximum number of jumps exceeded")
        label = self.args[ArgIndexes.ARG1].value
        self._check_if_label_exist(label, engine)
        engine.instruction_pointer = engine.labels[label]
        engine.number_of_jumps += 1


class InstructionCALL(InstructionJUMP):

    def exec(self, engine):
        engine.push_instruction_pointer_to_call_stack()
        super().exec(engine)


class InstructionJUMPIFEQ(InstructionJUMP):
    expected_args = [ArgType.LABEL, ArgType.SYMBOL, ArgType.SYMBOL]

    def exec(self, engine):
        label = self.args[ArgIndexes.ARG1].value
        self._check_if_label_exist(label, engine)
        symbol1, symbol2 = self._get_symbol_operands(engine)
        if symbol1 == symbol2:
            super().exec(engine)


class InstructionJUMPIFNEQ(InstructionJUMP):
    expected_args = [ArgType.LABEL, ArgType.SYMBOL, ArgType.SYMBOL]

    def exec(self, engine):
        label = self.args[ArgIndexes.ARG1].value
        self._check_if_label_exist(label, engine)
        symbol1, symbol2 = self._get_symbol_operands(engine)
        if symbol1 != symbol2:
            super().exec(engine)


class InstructionEXIT(Instruction):
    expected_args = [ArgType.SYMBOL]

    def exec(self, engine):
        symbol = engine.get_symbol_value(self.args[ArgIndexes.ARG1])
        if symbol.data_type != ArgDataType.INT:
            raise BadDataType(f"EXIT: Bad operand type! Instruction order: {self.order}")
        if int(symbol.value) < 0 or int(symbol.value) > 49:
            raise BadOperandValue(f"EXIT: Bad operand value! Instruction order: {self.order}")
        sys_exit(symbol.value)


class InstructionDPRINT(Instruction):
    expected_args = [ArgType.SYMBOL]

    def exec(self, engine):
        symbol = engine.get_symbol_value(self.args[ArgIndexes.ARG1])
        print(symbol.value, file=stderr)


class InstructionBREAK(Instruction):

    def exec(self, engine):
        engine.print_info()


class InstructionRETURN(Instruction):

    def exec(self, engine):
        engine.pop_instruction_pointer_from_call_stack()
