import argparse
from sys import stdin, stderr, argv
from interpretr_libs.error_codes import PARAMETR_ERROR, INPUT_FILE_OPEN_ERROR


class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(stderr)
        if "[Errno 2]" in message:
            self.exit(INPUT_FILE_OPEN_ERROR, f"ERROR: {message}\n")
        self.exit(PARAMETR_ERROR, f"ERROR: {message}\n")


class CommandLineAPI():
    def __init__(self):
        self.arguments = self._parse_arguments()
        self.source_file = self.arguments.source
        self.input_file = self.arguments.input
        self.stats_file = self.arguments.stats
        self.order_stats = self._get_order_stats()

    def _get_order_stats(self):
        out = list()
        if self.arguments.insts or self.arguments.hot or self.arguments.vars:
            for arg in argv:
                if arg == "--insts" or arg == "--hot" or arg == "--vars":
                    out.append(arg)
        return out

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
        parser.add_argument(
            "--stats",
            action="store",
            type=argparse.FileType("w+"),
            default=None,
            help="Define where to store statistics"
            )
        parser.add_argument(
            "--insts",
            action="store_true",
            help="Save the number of instructions to the file defined in --stats"
            )
        parser.add_argument(
            "--hot",
            action="store_true",
            help="Save the hottest instructions order argument to the file defined in --stats"
            )
        parser.add_argument(
            "--vars",
            action="store_true",
            help=(
                "Save the maximum number of variables initialized at"
                " one time to the file defined in --stats"
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
        if self.stats_file is not None:
            self.stats_file.close()
