from interpretr_libs.instructions import (
    Instruction, InstructionADD, InstructionSUB,
    InstructionMUL, InstructionIDIV, InstructionLT,
    InstructionGT, InstructionEQ, InstructionAND,
    InstructionOR, InstructionNOT, InstructionINT2CHAR,
    InstructionSTRING2INT, InstructionJUMPIFEQ,
    InstructionJUMPIFNEQ
)
from interpretr_libs.instruction_args import ArgDataType, Symbol, ArgType
from interpretr_libs.expections import BadDataType, MissingValueError, BadStringOperation


class InstructionCLEARS(Instruction):

    def exec(self, engine):
        engine.stack_data = list()


class InstructionADDS(InstructionADD):
    expected_args = []

    def _get_symbol_operands(self, engine):
        return self._get_symbol_operands_from_stack(engine)

    def _save_symbol(self, engine, symbol, arg_index=None):
        self._save_symbol_stack(engine, symbol)


class InstructionSUBS(InstructionSUB):
    expected_args = []

    def _get_symbol_operands(self, engine):
        return self._get_symbol_operands_from_stack(engine)

    def _save_symbol(self, engine, symbol, arg_index=None):
        self._save_symbol_stack(engine, symbol)


class InstructionMULS(InstructionMUL):
    expected_args = []

    def _get_symbol_operands(self, engine):
        return self._get_symbol_operands_from_stack(engine)

    def _save_symbol(self, engine, symbol, arg_index=None):
        self._save_symbol_stack(engine, symbol)


class InstructionIDIVS(InstructionIDIV):
    expected_args = []

    def _get_symbol_operands(self, engine):
        return self._get_symbol_operands_from_stack(engine)

    def _save_symbol(self, engine, symbol, arg_index=None):
        self._save_symbol_stack(engine, symbol)


class InstructionLTS(InstructionLT):
    expected_args = []

    def _get_symbol_operands(self, engine):
        return self._get_symbol_operands_from_stack(engine)

    def _save_symbol(self, engine, symbol, arg_index=None):
        self._save_symbol_stack(engine, symbol)


class InstructionGTS(InstructionGT):
    expected_args = []

    def _get_symbol_operands(self, engine):
        return self._get_symbol_operands_from_stack(engine)

    def _save_symbol(self, engine, symbol, arg_index=None):
        self._save_symbol_stack(engine, symbol)


class InstructionEQS(InstructionEQ):
    expected_args = []

    def _get_symbol_operands(self, engine):
        return self._get_symbol_operands_from_stack(engine)

    def _save_symbol(self, engine, symbol, arg_index=None):
        self._save_symbol_stack(engine, symbol)


class InstructionANDS(InstructionAND):
    expected_args = []

    def _get_symbol_operands(self, engine):
        return self._get_symbol_operands_from_stack(engine)

    def _save_symbol(self, engine, symbol, arg_index=None):
        self._save_symbol_stack(engine, symbol)


class InstructionORS(InstructionOR):
    expected_args = []

    def _get_symbol_operands(self, engine):
        return self._get_symbol_operands_from_stack(engine)

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
            raise BadDataType("LOGICAL INSTRUCTION: Support just BOOL!")
        self._save_symbol_stack(engine, Symbol(ArgDataType.BOOL, not symbol.value))


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

    def _get_symbol_operands(self, engine):
        return self._get_symbol_operands_from_stack(engine)

    def _save_symbol(self, engine, symbol, arg_index=None):
        self._save_symbol_stack(engine, symbol)


class InstructionJUMPIFEQS(InstructionJUMPIFEQ):
    expected_args = [ArgType.LABEL]

    def _get_symbol_operands(self, engine):
        return self._get_symbol_operands_from_stack(engine)


class InstructionJUMPIFNEQS(InstructionJUMPIFNEQ):
    expected_args = [ArgType.LABEL]

    def _get_symbol_operands(self, engine):
        return self._get_symbol_operands_from_stack(engine)
