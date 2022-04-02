<?php
ini_set('display_errors', 'stderr');

require_once "test_libs/error_codes.php";
require_once "test_libs/arg_parse.php";
require_once "test_libs/test_engine.php";

$arg_parser = new ArgParser($argc, $argv);
$arg_parser->parse();

$test_engine = new TestEngine($arg_parser);
$test_engine->load_tests();
$test_engine->exec_tests();
$test_engine->generate_report();
exit(EXIT_OK);
?>