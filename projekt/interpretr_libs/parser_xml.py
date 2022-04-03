import re
from lxml import etree
from interpretr_libs.expections import UnexpectedXMLStructureError

from interpretr_libs.instruction_args import (
        ArgDataType, ArgType, ArgFrame, Label, Symbol, TypeArg, Var
    )
from interpretr_libs.instruction_map import OPCODE_TO_INSTRUCTION


class ParserXML():
    def __init__(self, data):
        self.root = etree.XML(data)

    def get_code(self):
        out = dict()
        if self.root.tag != "program":
            raise UnexpectedXMLStructureError("Missing root tag! Expect: program")
        lang = self.root.attrib.get("language")
        if lang is not None and lang != "IPPcode22":
            raise UnexpectedXMLStructureError("Missing or bad language! Expect: IPPcode22")

        for instruction in self.root:
            if instruction.tag != "instruction":
                raise UnexpectedXMLStructureError(f"Unexpected tag \"{instruction.tag}\"!")

            try:
                order = int(instruction.attrib.get("order"))
                if order <= 0:
                    raise ValueError
            except (ValueError, TypeError):
                raise UnexpectedXMLStructureError("Bad order value!")

            if order in out.keys():
                raise UnexpectedXMLStructureError("Duplicite order!")

            out[order] = self._get_instruction(instruction)

        return {i: value for i, value in enumerate(dict(sorted(out.items())).values())}

    def _get_instruction(self, instruction):
        opcode = instruction.attrib.get("opcode")
        if opcode is not None:
            opcode = opcode.upper()
        if OPCODE_TO_INSTRUCTION.get(opcode, None) is None:
            raise UnexpectedXMLStructureError(f"Unknown instructions \"{opcode}\"")
        args = self._get_args(instruction)
        instruction = OPCODE_TO_INSTRUCTION[opcode](opcode, args)

        if len(instruction.args) != len(instruction.expected_args):
            raise UnexpectedXMLStructureError("Bad number of operands!")
        for arg, e_arg in zip(instruction.args, instruction.expected_args):
            if e_arg == ArgType.SYMBOL:
                if arg.type != e_arg and arg.type != ArgType.VAR:
                    raise UnexpectedXMLStructureError(
                        f"Unexpected type of operand! Expect: {e_arg} Get: {arg.type}"
                    )
            else:
                if arg.type != e_arg:
                    raise UnexpectedXMLStructureError(
                        f"Unexpected type of operand! Expect: {e_arg} Get: {arg.type}"
                        )
        return instruction

    def _get_args(self, instruction):
        arg1 = instruction.findall("arg1")
        arg2 = instruction.findall("arg2")
        arg3 = instruction.findall("arg3")

        if len(arg1) > 1 and len(arg2) > 1 and len(arg3) > 1:
            raise UnexpectedXMLStructureError("Too much args!")

        out = []
        if len(arg1) == 1:
            out.append(self._get_arg(arg1[0]))
        if len(arg2) == 1:
            if len(out) != 1:
                raise UnexpectedXMLStructureError("Missing arg1!")
            out.append(self._get_arg(arg2[0]))
        if len(arg3) == 1:
            if len(out) != 2:
                raise UnexpectedXMLStructureError("Missing arg1 or arg2!")
            out.append(self._get_arg(arg3[0]))
        return out

    def _get_arg(self, arg):
        if list(arg):
            raise UnexpectedXMLStructureError("Unexpected element in arg tag!")

        arg_type = arg.attrib.get("type")
        arg_value = "" if arg.text is None else arg.text

        if arg_type == ArgType.LABEL:
            if re.match(r"^[a-zA-Z_\-$&%\*\!\?][\w_\-$&%\*\!\?]*$", arg_value) is None:
                raise UnexpectedXMLStructureError("Bad Label format!")
            return Label(arg_value)

        if arg_type == ArgType.TYPE:
            if arg_value == ArgDataType.INT:
                return TypeArg(ArgDataType.INT)
            if arg_value == ArgDataType.BOOL:
                return TypeArg(ArgDataType.BOOL)
            if arg_value == ArgDataType.STR:
                return TypeArg(ArgDataType.STR)
            raise UnexpectedXMLStructureError

        if arg_type == ArgDataType.NIL:
            if arg_value != ArgDataType.NIL:
                raise UnexpectedXMLStructureError("Bad Nil value!")
            return Symbol(ArgDataType.NIL, None)

        if arg_type == ArgDataType.BOOL:
            if arg_value == "true":
                return Symbol(ArgDataType.BOOL, True)
            if arg_value == "false":
                return Symbol(ArgDataType.BOOL, False)

        if arg_type == ArgDataType.INT:
            try:
                return Symbol(ArgDataType.INT, int(arg_value))
            except ValueError:
                raise UnexpectedXMLStructureError("Bad int format!")

        if arg_type == ArgDataType.STR:
            if "#" in arg_value:
                raise UnexpectedXMLStructureError("String cant contain \"#\"!")
            return Symbol(ArgDataType.STR, self.clean_string(arg_value))

        if arg_type == ArgType.VAR:
            frame, value = arg_value.split("@")
            if frame != ArgFrame.GF and frame != ArgFrame.LF and frame != ArgFrame.TF:
                raise UnexpectedXMLStructureError("Bad frame format!")
            if re.match(r"^[a-zA-Z_\-$&%\*\!\?][\w_\-$&%\*\!\?]*$", value) is None:
                raise UnexpectedXMLStructureError("Bad var value!")
            return Var(value, frame)

        raise UnexpectedXMLStructureError(f"Bad arg! Type: {arg_type} Value: {arg_value}")

    @staticmethod
    def clean_string(string):
        str_parts = string.split("\\")
        out = str_parts.pop(0)
        for part in str_parts:
            if not re.match(r"^\d{3}", part[:3]):
                raise UnexpectedXMLStructureError("Invalid escape seqencion!")
            out += chr(int(part[:3]))
            out += part[3:]
        return out
