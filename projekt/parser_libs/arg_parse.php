<?php
require_once "error_codes.php";

class ArgParser {
    public $argc;
    public $argv;
    public $short_parameters;
    public $long_parameters;
    public $args;

    function __construct($argc, $argv) {
        $this->argc = $argc;
        $this->argv = $argv;
        $this->short_parameters = "";
        $this->long_parameters  = array("help");
        $this->args = array("parse.php", "--help");
    }

    function help() {
        $message = "Usage: %s [--help]\n\n";
        $message .= "Parser of IPPcode22 code.\n";
        $message .= "\tExpects IPPcode22 on standard input -> Returns the XML representation of IPPcode22 on standard output.\n\n";
        $message .= "Optional arguments:\n";
        $message .="\t--help\t\tShow this help message and exit.\n";
        
        echo sprintf($message, $this->argv[0]);
    }

    function parse() {
        $options = getopt($this->short_parameters, $this->long_parameters);
        $bad_args = array_diff($this->argv, $this->args);
        if (array_key_exists("help", $options)){
            $this->help();
            exit(EXIT_OK);
        }
        if (!empty($bad_args)){
            fwrite(STDERR,"ERROR: Bad parameter!\n");
            $this->help();
            exit(PARAMETR_ERROR);
        }
    }
}
?>