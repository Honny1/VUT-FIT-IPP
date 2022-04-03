from interpretr_libs.instructions import (
    InstructionCREATEFRAME, InstructionPUSHFRAME, InstructionPOPFRAME,
    InstructionRETURN, InstructionBREAK, InstructionDEFVAR,
    InstructionCALL, InstructionPUSHS, InstructionPOPS,
    InstructionWRITE, InstructionLABEL, InstructionJUMP,
    InstructionDPRINT, InstructionEXIT, InstructionMOVE,
    InstructionINT2CHAR, InstructionREAD, InstructionSTRLEN,
    InstructionTYPE, InstructionNOT, InstructionADD,
    InstructionSUB, InstructionMUL, InstructionIDIV,
    InstructionLT, InstructionGT, InstructionEQ,
    InstructionAND, InstructionOR, InstructionSTRING2INT,
    InstructionCONCAT, InstructionGETCHAR, InstructionSETCHAR,
    InstructionJUMPIFEQ, InstructionJUMPIFNEQ,
)

OPCODE_TO_INSTRUCTION = {
    "CREATEFRAME": InstructionCREATEFRAME,
    "PUSHFRAME": InstructionPUSHFRAME,
    "POPFRAME": InstructionPOPFRAME,
    "RETURN": InstructionRETURN,
    "BREAK": InstructionBREAK,
    "DEFVAR": InstructionDEFVAR,
    "CALL": InstructionCALL,
    "PUSHS": InstructionPUSHS,
    "POPS": InstructionPOPS,
    "WRITE": InstructionWRITE,
    "LABEL": InstructionLABEL,
    "JUMP": InstructionJUMP,
    "DPRINT": InstructionDPRINT,
    "EXIT": InstructionEXIT,
    "MOVE": InstructionMOVE,
    "INT2CHAR": InstructionINT2CHAR,
    "READ": InstructionREAD,
    "STRLEN": InstructionSTRLEN,
    "TYPE": InstructionTYPE,
    "NOT": InstructionNOT,
    "ADD": InstructionADD,
    "SUB": InstructionSUB,
    "MUL": InstructionMUL,
    "IDIV": InstructionIDIV,
    "LT": InstructionLT,
    "GT": InstructionGT,
    "EQ": InstructionEQ,
    "AND": InstructionAND,
    "OR": InstructionOR,
    "STRI2INT": InstructionSTRING2INT,
    "CONCAT": InstructionCONCAT,
    "GETCHAR": InstructionGETCHAR,
    "SETCHAR": InstructionSETCHAR,
    "JUMPIFEQ": InstructionJUMPIFEQ,
    "JUMPIFNEQ": InstructionJUMPIFNEQ,
}