import argparse
from sys import stdin, stderr
from interpretr_libs.error_codes import PARAMETR_ERROR


class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(stderr)
        self.exit(PARAMETR_ERROR, f"ERROR: {message}\n")


class CommandLineAPI():
    def __init__(self):
        self.arguments = self._parse_arguments()
        self.source_file = self.arguments.source
        self.input_file = self.arguments.input

    def _parse_arguments(self):
        parser = ArgumentParser(
            prog="interpretr",
            formatter_class=argparse.RawTextHelpFormatter,
            description="Interpretr of IPPcode22",
            add_help=False,
        )
        self._prepare_arguments(parser)

        arguments = parser.parse_args()
        if arguments.source.name == "<stdin>" and arguments.input.name == "<stdin>":
            parser.error("Missing parameter --source or --input. At least one must be listed.")
        return arguments

    @staticmethod
    def _prepare_arguments(parser):
        parser.add_argument(
            '-h',
            '--help',
            action='help',
            default=argparse.SUPPRESS,
            help='Show this help message and exit.')
        parser.add_argument(
            "--source",
            action="store",
            type=argparse.FileType("r"),
            default=stdin,
            help=(
                 "File with IPPcode22. Default is standard input."
                 " The --source or --input parameters must specify at least one of them."
                 )
                )
        parser.add_argument(
            "--input",
            action="store",
            type=argparse.FileType("r"),
            default=stdin,
            help=(
                 "File with user input. Default is standard input."
                 " The --source or --input parameters must specify at least one of them."
                 )
                )

    def load_source(self):
        return self.source_file.read().encode()

    def load_input(self):
        if self.arguments.input.name == "<stdin>":
            return self.arguments.input.name
        return self.input_file

    def close_files(self):
        self.source_file.close()
        self.input_file.close()
