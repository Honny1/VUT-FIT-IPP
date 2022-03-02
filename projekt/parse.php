<?php
ini_set('display_errors', 'stderr');

require_once "parse_libs/error_codes.php";
require_once "parse_libs/arg_parse.php";
require_once "parse_libs/code_parser.php";

$arg_parser = new ArgParser($argc, $argv);
$stats_args = $arg_parser->parse();
$code_parser = new CodeParser();
$code_parser->parse();
$code_parser->stats->save_stats($stats_args);
exit(EXIT_OK);
?>
