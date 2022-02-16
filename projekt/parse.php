<?php
ini_set('display_errors', 'stderr');

require_once "./parser_libs/arg_parse.php";
require_once "./parser_libs/code_parser.php";

$arg_parser = new ArgParser($argc, $argv);
$arg_parser->parse();

$code_parser = new CodeParser();
$code_parser->parse();
echo "end";
?>
