from interpretr_libs.command_line_api import CommandLineAPI
from interpretr_libs.interpretr_engine import Engine
from interpretr_libs.parser_xml import ParserXML
from interpretr_libs.stats import Stats
from lxml.etree import XMLSyntaxError
from interpretr_libs.error_codes import EXIT_OK, INTERNAL_ERROR, XML_ERROR
from sys import exit as sys_exit
from sys import stderr
from interpretr_libs.expections import (
    UnexpectedXMLStructureError, NotExistFrameError, MissingValueError,
    SemanticError, BadDataType, BadStringOperation, BadOperandValue, UndefinedVar,
    StatsMissingFile
)

EXPECTED_INTERPRETATION_ERRORS = (
    NotExistFrameError, MissingValueError, SemanticError,
    BadDataType, BadStringOperation, BadOperandValue, UndefinedVar
)


def main():
    exit_code = EXIT_OK
    api = CommandLineAPI()
    xml = api.load_source()
    instructions = dict()
    stats = None
    try:
        stats = Stats(api.stats_file, api.order_stats)
    except StatsMissingFile as error:
        print(f"ERROR: {error}", file=stderr)
        exit_code = error.exit_code
        sys_exit(exit_code)
    try:
        parser = ParserXML(xml)
        instructions = parser.get_code()
    except XMLSyntaxError:
        exit_code = XML_ERROR
        sys_exit(exit_code)
    except UnexpectedXMLStructureError as error:
        print(f"ERROR: {error}", file=stderr)
        exit_code = error.exit_code
        sys_exit(exit_code)
    try:
        engine = Engine(instructions, api.load_input(), stats)
        engine.exec()
    except EXPECTED_INTERPRETATION_ERRORS as error:
        print(f"ERROR: {error}", file=stderr)
        exit_code = error.exit_code
        sys_exit(exit_code)

    stats.save_stats()
    api.close_files()
    sys_exit(exit_code)


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(f"ERROR: {error}", file=stderr)
        exit_code = INTERNAL_ERROR
        sys_exit(exit_code)
