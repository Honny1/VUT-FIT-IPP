from sys import exit as sys_exit, stderr
from interpretr_libs.expections import (
    BadDataType, BadOperandValue,
    BadStringOperation, MissingValueError, UnexpectedXMLStructureError)
from interpretr_libs.instruction_args import ArgDataType, ArgType, Symbol, ArgIndexes
from interpretr_libs.expections import NotExistFrameError, SemanticError


class Instruction:
    expected_args = []

    def __init__(self, opcode, args):
        self.opcode = opcode
        self.args = args
        if len(args) != len(self.expected_args):
            raise UnexpectedXMLStructureError("Unexpected number of operands!")

    def exec(self, engine):
        raise NotImplementedError

    def __repr__(self):
        return f"{self.opcode}: {self.args}"

    def _get_operands_for_math_instruction(self, engine):
        symbol1 = engine.get_symbol_value(self.args[ArgIndexes.ARG2])
        symbol2 = engine.get_symbol_value(self.args[ArgIndexes.ARG3])

        if symbol1.data_type != ArgDataType.INT or symbol2.data_type != ArgDataType.INT:
            raise BadDataType("MATH INSTRUCTION: Support just INT!")
        return (symbol1, symbol2)

    def _get_operands_for_math_stack_instruction(self, engine):
        if not engine.stack_data:
            raise MissingValueError("STACK MATH OPERATION: empty stack!")
        symbol2 = engine.stack_data.pop()
        if not engine.stack_data:
            raise MissingValueError("STACK MATH OPERATION: empty stack!")
        symbol1 = engine.stack_data.pop()

        if symbol1.data_type != ArgDataType.INT or symbol2.data_type != ArgDataType.INT:
            raise BadDataType("MATH INSTRUCTION: Support just INT!")
        return (symbol1, symbol2)

    def _get_operands_for_compare_instruction(self, engine, enable_nil=False):
        symbol1 = engine.get_symbol_value(self.args[ArgIndexes.ARG2])
        symbol2 = engine.get_symbol_value(self.args[ArgIndexes.ARG3])

        supporeted_types = (ArgDataType.INT, ArgDataType.BOOL, ArgDataType.STR)
        if enable_nil:
            supporeted_types = (ArgDataType.INT, ArgDataType.BOOL, ArgDataType.STR, ArgDataType.NIL)
        if symbol1.data_type not in supporeted_types or symbol2.data_type not in supporeted_types:
            raise BadDataType("COMPARE INSTRUCTION: Support just INT, BOOL, STRING!")
        is_one_nil = symbol1.data_type == ArgDataType.NIL or symbol2.data_type == ArgDataType.NIL
        if symbol1.data_type != symbol2.data_type and not is_one_nil:
            raise BadDataType("COMPARE INSTRUCTION: Cant compare different types")

        return (symbol1, symbol2)

    def _get_operands_for_compare_stack_instruction(self, engine, enable_nil=False):
        if not engine.stack_data:
            raise MissingValueError("STACK COMPARE OPERATION: empty stack!")
        symbol2 = engine.stack_data.pop()
        if not engine.stack_data:
            raise MissingValueError("STACK COMPARE OPERATION: empty stack!")
        symbol1 = engine.stack_data.pop()

        supporeted_types = (ArgDataType.INT, ArgDataType.BOOL, ArgDataType.STR)
        if enable_nil:
            supporeted_types = (ArgDataType.INT, ArgDataType.BOOL, ArgDataType.STR, ArgDataType.NIL)

        if symbol1.data_type not in supporeted_types or symbol2.data_type not in supporeted_types:
            raise BadDataType("COMPARE INSTRUCTION: Support just INT, BOOL, STRING!")
        is_one_nil = symbol1.data_type == ArgDataType.NIL or symbol2.data_type == ArgDataType.NIL
        if symbol1.data_type != symbol2.data_type and not is_one_nil:
            raise BadDataType("COMPARE INSTRUCTION: Cant compare different types")

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
            raise NotExistFrameError("PUSHFRAME: frame not exist!")
        engine.stack_LF.append(engine.TF)
        engine.TF = None


class InstructionPOPFRAME(Instruction):

    def exec(self, engine):
        if not engine.stack_LF:
            raise NotExistFrameError("POPFRAME: empty frame stack!")
        engine.TF = engine.stack_LF.pop()


class InstructionDEFVAR(Instruction):
    expected_args = [ArgType.VAR]

    def exec(self, engine):
        var = self.args[ArgIndexes.ARG1]
        if engine.is_var_exist(var):
            raise SemanticError("DEFVAR: Variable exist")
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
            raise MissingValueError("POPS: empty stack!")
        engine.set_var(self.args[ArgIndexes.ARG1], engine.stack_data.pop())


class InstructionADD(Instruction):
    expected_args = [ArgType.VAR, ArgType.SYMBOL, ArgType.SYMBOL]

    def exec(self, engine):
        symbol1, symbol2 = self._get_operands_for_math_instruction(engine)

        result = symbol1.value + symbol2.value
        self._save_symbol(engine, Symbol(ArgDataType.INT, result))


class InstructionSUB(Instruction):
    expected_args = [ArgType.VAR, ArgType.SYMBOL, ArgType.SYMBOL]

    def exec(self, engine):
        symbol1, symbol2 = self._get_operands_for_math_instruction(engine)

        result = symbol1.value - symbol2.value
        self._save_symbol(engine, Symbol(ArgDataType.INT, result))


class InstructionMUL(Instruction):
    expected_args = [ArgType.VAR, ArgType.SYMBOL, ArgType.SYMBOL]

    def exec(self, engine):
        symbol1, symbol2 = self._get_operands_for_math_instruction(engine)

        result = symbol1.value * symbol2.value
        self._save_symbol(engine, Symbol(ArgDataType.INT, result))


class InstructionIDIV(Instruction):
    expected_args = [ArgType.VAR, ArgType.SYMBOL, ArgType.SYMBOL]

    def exec(self, engine):
        symbol1, symbol2 = self._get_operands_for_math_instruction(engine)
        if symbol2.value == 0:
            raise BadOperandValue("IDIV: Division ZERO!")
        result = symbol1.value // symbol2.value
        self._save_symbol(engine, Symbol(ArgDataType.INT, result))


class InstructionLT(Instruction):
    expected_args = [ArgType.VAR, ArgType.SYMBOL, ArgType.SYMBOL]

    def exec(self, engine):
        symbol1, symbol2 = self._get_operands_for_compare_instruction(engine)

        result = symbol1.value < symbol2.value
        self._save_symbol(engine, Symbol(ArgDataType.BOOL, result))


class InstructionGT(Instruction):
    expected_args = [ArgType.VAR, ArgType.SYMBOL, ArgType.SYMBOL]

    def exec(self, engine):
        symbol1, symbol2 = self._get_operands_for_compare_instruction(engine)

        result = symbol1.value > symbol2.value
        self._save_symbol(engine, Symbol(ArgDataType.BOOL, result))


class InstructionEQ(Instruction):
    expected_args = [ArgType.VAR, ArgType.SYMBOL, ArgType.SYMBOL]

    def exec(self, engine):
        symbol1, symbol2 = self._get_operands_for_compare_instruction(engine, True)

        result = symbol1 == symbol2
        self._save_symbol(engine, Symbol(ArgDataType.BOOL, result))


class InstructionAND(Instruction):
    expected_args = [ArgType.VAR, ArgType.SYMBOL, ArgType.SYMBOL]

    def exec(self, engine):
        symbol1, symbol2 = self._get_operands_for_compare_instruction(engine)
        if symbol1.data_type != ArgDataType.BOOL or symbol2.data_type != ArgDataType.BOOL:
            raise BadDataType("AND: Support just BOOL!")

        result = symbol1.value and symbol2.value
        self._save_symbol(engine, Symbol(ArgDataType.BOOL, result))


class InstructionOR(Instruction):
    expected_args = [ArgType.VAR, ArgType.SYMBOL, ArgType.SYMBOL]

    def exec(self, engine):
        symbol1, symbol2 = self._get_operands_for_compare_instruction(engine)
        if symbol1.data_type != ArgDataType.BOOL or symbol2.data_type != ArgDataType.BOOL:
            raise BadDataType("OR: Support just BOOL!")

        result = symbol1.value or symbol2.value
        self._save_symbol(engine, Symbol(ArgDataType.BOOL, result))


class InstructionNOT(Instruction):
    expected_args = [ArgType.VAR, ArgType.SYMBOL]

    def exec(self, engine):
        symbol = engine.get_symbol_value(self.args[ArgIndexes.ARG2])
        if symbol.data_type != ArgDataType.BOOL:
            raise BadDataType("NOT: Support just BOOL!")

        result = not symbol.value
        self._save_symbol(engine, Symbol(ArgDataType.BOOL, result))


class InstructionINT2CHAR(Instruction):
    expected_args = [ArgType.VAR, ArgType.SYMBOL]

    def exec(self, engine):
        symbol = engine.get_symbol_value(self.args[ArgIndexes.ARG2])
        if symbol.data_type != ArgDataType.INT:
            raise BadDataType("INT2CHAR: Support just INT!")
        try:
            self._save_symbol(engine, Symbol(ArgDataType.STR, chr(symbol.value)))
        except Exception:
            raise BadStringOperation(f"INT2CHAR: Bad int to char corversion: {symbol.value}")


class InstructionSTRING2INT(Instruction):
    expected_args = [ArgType.VAR, ArgType.SYMBOL, ArgType.SYMBOL]

    def exec(self, engine):
        symbol1 = engine.get_symbol_value(self.args[ArgIndexes.ARG2])
        symbol2 = engine.get_symbol_value(self.args[ArgIndexes.ARG3])

        if symbol1.data_type != ArgDataType.STR or symbol2.data_type != ArgDataType.INT:
            raise BadDataType("STRING2INT: Bad type of operands!")

        try:
            self._save_symbol(engine, Symbol(ArgDataType.INT, ord(symbol1.value[symbol2.value])))
        except IndexError:
            raise BadStringOperation("STRING2INT: Index out of the range!")
        except Exception:
            raise BadStringOperation(f"Bad int to char corversion: {symbol1.value[symbol2.value]}")


class InstructionREAD(Instruction):
    expected_args = [ArgType.VAR, ArgType.TYPE]

    def exec(self, engine):
        data = None
        try:
            if engine.user_input == "<stdin>":
                data = input().rstrip()
            if not isinstance(engine.user_input, str):
                data = engine.user_input.readline().rstrip()
        except Exception:
            data = None
        type_ = self.args[ArgIndexes.ARG2]

        if data is None:
            self._save_symbol(engine, Symbol(ArgDataType.NIL, None))
            return
        if type_.value == ArgDataType.BOOL:
            str_to_bool = {"true": True, "false": False, True: True, False: False}
            if data not in str_to_bool:
                self._save_symbol(engine, Symbol(ArgDataType.NIL, None))
            else:
                self._save_symbol(engine, Symbol(ArgDataType.BOOL, str_to_bool[data]))
            return
        if type_.value == ArgDataType.STR:
            self._save_symbol(engine, Symbol(ArgDataType.STR, data))
            return
        if type_.value == ArgDataType.INT:
            try:
                int_val = int(data)
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
        symbol1 = engine.get_symbol_value(self.args[ArgIndexes.ARG2])
        symbol2 = engine.get_symbol_value(self.args[ArgIndexes.ARG3])

        if symbol1.data_type != ArgDataType.STR or symbol2.data_type != ArgDataType.STR:
            raise BadDataType("CONCAT: Bad type of operands! Just string are supported.")
        self._save_symbol(engine, Symbol(ArgDataType.STR, f"{symbol1.value}{symbol2.value}"))


class InstructionSTRLEN(Instruction):
    expected_args = [ArgType.VAR, ArgType.SYMBOL]

    def exec(self, engine):
        symbol = engine.get_symbol_value(self.args[ArgIndexes.ARG2])

        if symbol.data_type != ArgDataType.STR:
            raise BadDataType("STRLEN: Bad type of operands! Just string is supported.")
        self._save_symbol(engine, Symbol(ArgDataType.INT, len(symbol.value)))


class InstructionGETCHAR(Instruction):
    expected_args = [ArgType.VAR, ArgType.SYMBOL, ArgType.SYMBOL]

    def exec(self, engine):
        symbol1 = engine.get_symbol_value(self.args[ArgIndexes.ARG2])
        symbol2 = engine.get_symbol_value(self.args[ArgIndexes.ARG3])

        if symbol1.data_type != ArgDataType.INT or symbol2.data_type != ArgDataType.STR:
            raise BadDataType("GETCHAR: Bad type of operands!")

        try:
            self._save_symbol(engine, Symbol(ArgDataType.STR, symbol2.value[symbol1.value]))
        except IndexError:
            raise BadStringOperation("GETCHAR: Index out of the range!")


class InstructionSETCHAR(Instruction):
    expected_args = [ArgType.VAR, ArgType.SYMBOL, ArgType.SYMBOL]

    def exec(self, engine):
        var = engine.get_var(self.args[ArgIndexes.ARG1])
        symbol1 = engine.get_symbol_value(self.args[ArgIndexes.ARG2])
        symbol2 = engine.get_symbol_value(self.args[ArgIndexes.ARG3])

        if var is None:
            raise MissingValueError("SETCHAR: Undefined value!")

        type_of_symbol1 = symbol1.data_type != ArgDataType.INT
        type_of_symbol2 = symbol2.data_type != ArgDataType.STR
        type_of_var = var.data_type == ArgDataType.STR

        if type_of_symbol1 or type_of_symbol2 or type_of_var:
            raise BadDataType("SETCHAR: Bad type of operands!")

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

    def exec(self, engine):
        label = self.args[ArgIndexes.ARG1].value
        if label not in engine.labels.keys():
            raise SemanticError(f"Undefined Label: {label}")
        engine.instruction_pointer = engine.labels[label]


class InstructionCALL(InstructionJUMP):

    def exec(self, engine):
        engine.push_instruction_pointer_to_call_stack()
        super().exec(engine)


class InstructionJUMPIFEQ(InstructionJUMP):
    expected_args = [ArgType.LABEL, ArgType.SYMBOL, ArgType.SYMBOL]

    def exec(self, engine):
        symbol1 = engine.get_symbol_value(self.args[ArgIndexes.ARG2])
        symbol2 = engine.get_symbol_value(self.args[ArgIndexes.ARG3])
        is_nil = symbol1.data_type == ArgDataType.NIL or symbol2.data_type == ArgDataType.NIL
        if symbol1.data_type == symbol2.data_type or is_nil:
            if symbol1 == symbol2:
                super().exec(engine)
                return
            return
        raise BadDataType("JUMPIFEQ: Bad operands type!")


class InstructionJUMPIFNEQ(InstructionJUMP):
    expected_args = [ArgType.LABEL, ArgType.SYMBOL, ArgType.SYMBOL]

    def exec(self, engine):
        symbol1 = engine.get_symbol_value(self.args[ArgIndexes.ARG2])
        symbol2 = engine.get_symbol_value(self.args[ArgIndexes.ARG3])
        is_nil = symbol1.data_type == ArgDataType.NIL or symbol2.data_type == ArgDataType.NIL
        if symbol1.data_type == symbol2.data_type or is_nil:
            if symbol1 != symbol2:
                super().exec(engine)
                return
            return
        raise BadDataType("JUMPIFNEQ: Bad operands type!")


class InstructionEXIT(Instruction):
    expected_args = [ArgType.SYMBOL]

    def exec(self, engine):
        symbol = engine.get_symbol_value(self.args[ArgIndexes.ARG1])
        if symbol.data_type != ArgDataType.INT:
            raise BadDataType("EXIT: Bad operand type!")
        if symbol.value < 0 and symbol.value > 49:
            raise BadOperandValue("EXIT: Bad operand value!")
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
