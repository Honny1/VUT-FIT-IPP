from interpretr_libs.instructions import (
    Instruction, InstructionADD, InstructionSUB,
    InstructionMUL, InstructionIDIV, InstructionLT,
    InstructionGT, InstructionEQ, InstructionAND,
    InstructionOR, InstructionNOT, InstructionINT2CHAR,
    InstructionSTRING2INT, InstructionJUMP
)
from interpretr_libs.instruction_args import ArgDataType, Symbol, ArgIndexes
from interpretr_libs.expections import BadDataType, MissingValueError, BadStringOperation


class InstructionCLEARS(Instruction):

    def exec(self, engine):
        engine.stack_data = list()


class InstructionADDS(InstructionADD):
    expected_args = []

    def _get_operands_for_math_instruction(self, engine):
        return self._get_operands_for_math_stack_instruction(engine)

    def _save_symbol(self, engine, symbol, arg_index=None):
        self._save_symbol_stack(engine, symbol)


class InstructionSUBS(InstructionSUB):
    expected_args = []

    def _get_operands_for_math_instruction(self, engine):
        return self._get_operands_for_math_stack_instruction(engine)

    def _save_symbol(self, engine, symbol, arg_index=None):
        self._save_symbol_stack(engine, symbol)


class InstructionMULS(InstructionMUL):
    expected_args = []

    def _get_operands_for_math_instruction(self, engine):
        return self._get_operands_for_math_stack_instruction(engine)

    def _save_symbol(self, engine, symbol, arg_index=None):
        self._save_symbol_stack(engine, symbol)


class InstructionIDIVS(InstructionIDIV):
    expected_args = []

    def _get_operands_for_math_instruction(self, engine):
        return self._get_operands_for_math_stack_instruction(engine)

    def _save_symbol(self, engine, symbol, arg_index=None):
        self._save_symbol_stack(engine, symbol)


class InstructionLTS(InstructionLT):
    expected_args = []

    def _get_operands_for_compare_instruction(self, engine, enable_nil=False):
        return self._get_operands_for_compare_stack_instruction(engine, enable_nil)

    def _save_symbol(self, engine, symbol, arg_index=None):
        self._save_symbol_stack(engine, symbol)


class InstructionGTS(InstructionGT):
    expected_args = []

    def _get_operands_for_compare_instruction(self, engine, enable_nil=False):
        return self._get_operands_for_compare_stack_instruction(engine, enable_nil)

    def _save_symbol(self, engine, symbol, arg_index=None):
        self._save_symbol_stack(engine, symbol)


class InstructionEQS(InstructionEQ):
    expected_args = []

    def _get_operands_for_compare_instruction(self, engine, enable_nil=False):
        return self._get_operands_for_compare_stack_instruction(engine, enable_nil)

    def _save_symbol(self, engine, symbol, arg_index=None):
        self._save_symbol_stack(engine, symbol)


class InstructionANDS(InstructionAND):
    expected_args = []

    def _get_operands_for_compare_instruction(self, engine, enable_nil=False):
        return self._get_operands_for_compare_stack_instruction(engine, enable_nil)

    def _save_symbol(self, engine, symbol, arg_index=None):
        self._save_symbol_stack(engine, symbol)


class InstructionORS(InstructionOR):
    expected_args = []

    def _get_operands_for_compare_instruction(self, engine, enable_nil=False):
        return self._get_operands_for_compare_stack_instruction(engine, enable_nil)

    def _save_symbol(self, engine, symbol, arg_index=None):
        self._save_symbol_stack(engine, symbol)


class InstructionNOTS(InstructionNOT):
    expected_args = []

    def exec(self, engine):
        if not engine.stack_data:
            raise MissingValueError(
                f"STACK COMPARE OPERATION: empty stack! Instruction order: {self.order}")
        symbol = engine.stack_data.pop()
        if symbol.data_type != ArgDataType.BOOL:
            raise BadDataType(f"NOTS: Support just BOOL! Instruction order: {self.order}")

        result = not symbol.value
        self._save_symbol_stack(engine, Symbol(ArgDataType.BOOL, result))


class InstructionINT2CHARS(InstructionINT2CHAR):
    expected_args = []

    def exec(self, engine):
        if not engine.stack_data:
            raise MissingValueError(f"INT2CHARS: empty stack! Instruction order: {self.order}")
        symbol = engine.stack_data.pop()
        if symbol.data_type != ArgDataType.INT:
            raise BadDataType(f"INT2CHARS: Support just INT! Instruction order: {self.order}")
        try:
            self._save_symbol_stack(engine, Symbol(ArgDataType.STR, chr(symbol.value)))
        except Exception:
            raise BadStringOperation((
                f"INT2CHARS: Bad int to char corversion: {symbol.value},"
                f" Instruction order: {self.order}"
            ))


class InstructionSTRING2INTS(InstructionSTRING2INT):
    expected_args = []

    def exec(self, engine):
        if not engine.stack_data:
            raise MissingValueError(f"STRI2INTS: empty stack! Instruction order: {self.order}")
        symbol2 = engine.stack_data.pop()

        if not engine.stack_data:
            raise MissingValueError(f"STRI2INTS: empty stack! Instruction order: {self.order}")
        symbol1 = engine.stack_data.pop()

        if symbol1.data_type != ArgDataType.STR or symbol2.data_type != ArgDataType.INT:
            raise BadDataType(f"STRI2INT: Bad type of operands! Instruction order: {self.order}")

        try:
            self._save_symbol_stack(
                engine,
                Symbol(ArgDataType.INT, ord(symbol1.value[symbol2.value]))
            )
        except IndexError:
            raise BadStringOperation(
                f"STRI2INT: Index out of the range! Instruction order: {self.order}"
            )
        except Exception:
            raise BadStringOperation((
                f"Bad int to char corversion: {symbol1.value[symbol2.value]}, "
                f"Instruction order: {self.order}"
            ))


class InstructionJUMPIFEQS(InstructionJUMP):

    def exec(self, engine):
        label = self.args[ArgIndexes.ARG1].value
        self._check_if_label_exist(label, engine)

        if not engine.stack_data:
            raise MissingValueError(f"JUMPIFEQS: empty stack! Instruction order: {self.order}")
        symbol2 = engine.stack_data.pop()

        if not engine.stack_data:
            raise MissingValueError(f"JUMPIFEQS: empty stack! Instruction order: {self.order}")
        symbol1 = engine.stack_data.pop()
        is_nil = symbol1.data_type == ArgDataType.NIL or symbol2.data_type == ArgDataType.NIL
        if symbol1.data_type == symbol2.data_type or is_nil:
            if symbol1 == symbol2:
                super().exec(engine)
                return
            return
        raise BadDataType(f"JUMPIFEQ: Bad operands type! Instruction order: {self.order}")


class InstructionJUMPIFNEQS(InstructionJUMP):

    def exec(self, engine):
        label = self.args[ArgIndexes.ARG1].value
        self._check_if_label_exist(label, engine)

        if not engine.stack_data:
            raise MissingValueError(f"JUMPIFNEQS: empty stack! Instruction order: {self.order}")
        symbol2 = engine.stack_data.pop()

        if not engine.stack_data:
            raise MissingValueError(f"JUMPIFNEQS: empty stack! Instruction order: {self.order}")
        symbol1 = engine.stack_data.pop()

        is_nil = symbol1.data_type == ArgDataType.NIL or symbol2.data_type == ArgDataType.NIL
        if symbol1.data_type == symbol2.data_type or is_nil:
            if symbol1 != symbol2:
                super().exec(engine)
                return
            return
        raise BadDataType(f"JUMPIFNEQ: Bad operands type! Instruction order: {self.order}")
