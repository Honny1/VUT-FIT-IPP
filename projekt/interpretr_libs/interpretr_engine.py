from sys import stderr
from interpretr_libs.instructions import InstructionLABEL
from interpretr_libs.expections import SemanticError, UndefinedVar
from interpretr_libs.expections import MissingValueError
from interpretr_libs.instruction_args import ArgFrame, Var
from interpretr_libs.expections import NotExistFrameError


class Engine:
    def __init__(self, instructions, user_input, stats=None):
        self.instructions = instructions
        self.user_input = user_input
        self.stats = stats

        self.instruction_pointer = 0
        self.GF = dict()
        self.TF = None
        self.stack_LF = list()
        self.stack_call = list()
        self.stack_data = list()

        self.labels = self.get_labels()

    def get_labels(self):
        labels = dict()
        for i_num, instruction in self.instructions.items():
            if type(instruction) is InstructionLABEL:
                if instruction.args[0].value in labels.keys():
                    raise SemanticError(f"Redefine label! Instruction order: {instruction.order}")
                labels[instruction.args[0].value] = i_num
        return labels

    def push_instruction_pointer_to_call_stack(self):
        self.stack_call.append(self.instruction_pointer)

    def pop_instruction_pointer_from_call_stack(self):
        if not self.stack_call:
            raise MissingValueError((
                f"Call stack is empty! Instruction order:"
                f" {self.instructions[self.instruction_pointer].order}"
            ))
        self.instruction_pointer = self.stack_call.pop()

    def exec(self):
        while self.instruction_pointer < len(self.instructions):
            instruction = self.instructions[self.instruction_pointer]
            instruction.exec(self)
            if self.stats is not None:
                self.stats.update_stats(self, instruction)
            self.instruction_pointer += 1

    def is_var_exist(self, var):
        if var.frame == ArgFrame.GF:
            return var.value in self.GF

        if var.frame == ArgFrame.TF:
            if self.TF is None:
                raise NotExistFrameError((
                    f"TF: Frame not exists! Instruction order:"
                    f" {self.instructions[self.instruction_pointer].order}"
                ))
            return var.value in self.TF

        if var.frame == ArgFrame.LF:
            if not self.stack_LF:
                raise NotExistFrameError((
                    f"LF: Empty Frame stack! Instruction order:"
                    f" {self.instructions[self.instruction_pointer].order}"
                ))
            return var.value in self.stack_LF[-1]
        return False

    def set_var(self, var, value, new_var=False):
        if not new_var and not self.is_var_exist(var):
            raise UndefinedVar((
                f"VAR: {var.value} is undefined! Instruction order:"
                f" {self.instructions[self.instruction_pointer].order}"
            ))
        if var.frame == ArgFrame.GF:
            self.GF[var.value] = value
            return
        if var.frame == ArgFrame.TF:
            self.TF[var.value] = value
            return
        if var.frame == ArgFrame.LF:
            self.stack_LF[-1][var.value] = value
            return

    def create_var(self, var, value):
        self.set_var(var, value, True)

    def get_var(self, var):
        if not self.is_var_exist(var):
            raise UndefinedVar((
                f"VAR: {var.value} is undefined! Instruction order:"
                f" {self.instructions[self.instruction_pointer].order}"
            ))
        if var.frame == ArgFrame.GF:
            return self.GF[var.value]
        if var.frame == ArgFrame.TF:
            return self.TF[var.value]
        if var.frame == ArgFrame.LF:
            return self.stack_LF[-1][var.value]

    def get_symbol_value(self, symbol, none_enable=False):
        out = symbol
        if type(symbol) is Var:
            out = self.get_var(symbol)
        if none_enable:
            return out
        if out is None:
            raise MissingValueError((
                f"Symbol or var is undefined! {out}, Instruction order:"
                f" {self.instructions[self.instruction_pointer].order}"
            ))
        return out

    def print_info(self):
        out = (
            f"Instruction pointer: {self.instruction_pointer}\n"
            f"GF: {self.GF}\n"
            f"LF: {self.stack_LF}\n"
            f"TF: {self.TF}\n"
            f"stack call: {self.stack_call}\n"
            f"stack data: {self.stack_data}\n"
            )
        print(out, file=stderr)
