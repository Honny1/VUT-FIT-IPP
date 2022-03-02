<?php
require_once "error_codes.php";

define("ARGS", array("parse.php", "--help", "--comments", "--loc", "--labels", "--jumps", "--fwjumps", "--backjumps", "--badjumps"));
define("LONG_PARAMETERS", array("help", "stats:", "comments", "loc", "labels", "jumps","fwjumps", "backjumps", "badjumps"));
define("SHORT_PARAMETERS", "");
define("STATS", array("--comments", "--loc", "--labels", "--jumps", "--fwjumps", "--backjumps", "--badjumps"));

class ArgParser {
    public $argc;
    public $argv;
    public $options;

    function __construct($argc, $argv) {
        $this->argc = $argc;
        $this->argv = $argv;
        $this->options = array();
    }

    function help() {
        $message = "Usage: %s [--help][--stats=FILE [STAT_FLAG...]]\n\n";
        $message .= "Parser of IPPcode22 code.\n";
        $message .= "\tExpects IPPcode22 on standard input -> Returns the XML representation of IPPcode22 on standard output.\n\n";
        $message .= "Optional arguments:\n";
        $message .="\t--help\t\tShow this help message and exit.\n\n";
        $message .="\t--stats=FILE STAT_FLAG\t\tDefine where to store statistics and what statistic\n\n";
        $message .="\tSTAT_FLAGs:\n";
        $message .="\t\t--loc\t\t\tNumber of instructions\n";
        $message .="\t\t--comments\t\tNumber of comments\n";
        $message .="\t\t--labels\t\tNumber of labels\n";
        $message .="\t\t--jumps\t\t\tNumber of jumps\n";
        $message .="\t\t--fwjumps\t\tNumber of forward jumps\n";
        $message .="\t\t--backjumps\t\tNumber of back jumps\n";
        $message .="\t\t--badjumps\t\tNumber of bad jumps\n";

        echo sprintf($message, $this->argv[0]);
    }

    private function filter_args(){
        $bad_args = array_diff($this->argv, ARGS);
        if(array_key_exists("stats", $this->options) && is_array($this->options["stats"])){
            foreach ($bad_args as $key => $value)
                if(in_array($value, $this->options["stats"])){
                    unset($bad_args[$key]);
                    unset($bad_args[$key-1]);
                }
        } else {
            $bad_args = array_diff($bad_args, $this->options);
            if(array_key_exists("stats", $this->options) && is_array($this->options["stats"]))
                $bad_args = array_diff($bad_args, array("--stats"));
        }
        foreach ($bad_args as $key => $value)
            if(str_starts_with($value, "--stats=") || str_starts_with($value, "--stats"))
                unset($bad_args[$key]);
        if(in_array($this->argv[0], $bad_args))
            if (($key = array_search($this->argv[0], $bad_args)) !== false)
                unset($bad_args[$key]);
        return $bad_args;
    }

    function parse() {
        $this->options = getopt(SHORT_PARAMETERS, LONG_PARAMETERS);
        $bad_args = $this->filter_args();
        if (array_key_exists("help", $this->options)){
            $this->help();
            exit(EXIT_OK);
        }
        if (!empty($bad_args)){
            fwrite(STDERR,"ERROR: Bad parameter!\n");
            $this->help();
            exit(PARAMETR_ERROR);
        }
        return $this->validate_stats_parameters();
    }

    private function validate_stats_parameters(){
        $args_ = array_diff($this->argv, ["parse.php"]);
        $out = array();
        $file = null;
        $expect_stats = false;
        $expect_file = false;
        foreach ($args_ as $value) {
            if($expect_file){
                $file = $value;
                $expect_file = false;
                $expect_stats = true;
                if(array_key_exists($file, $out)){
                    fwrite(STDERR,"ERROR: Bad parameter! FILE must be uncinate per run!\n");
                    $this->help();
                    exit(OUTPUT_FILE_OPEN_ERROR);
                }
                $out[$file] = array();
            }
            if($value == "--stats"){
                $expect_stats = false;
                $expect_file = true;
            }
            if(str_starts_with($value, "--stats=")){
                $file = strstr($value, '=');
                $file = substr($file, 1);
                $expect_stats = true;
                if(array_key_exists($file, $out)){
                    fwrite(STDERR,"ERROR: Bad parameter! FILE must be uncinate per run!\n");
                    $this->help();
                    exit(OUTPUT_FILE_OPEN_ERROR);
                }
                $out[$file] = array();
            }
            if(in_array($value, STATS) && !$expect_stats){
                fwrite(STDERR,"ERROR: Bad parameter! STAT_FLAG require --stats=FILE parameter\n");
                $this->help();
                exit(PARAMETR_ERROR);
            }

            if(in_array($value, STATS) && $expect_stats){
                array_push($out[$file], $value);
            }
        }
        if($expect_file){
            fwrite(STDERR,"ERROR: Bad parameter! --stats missing FILE\n");
            $this->help();
            exit(PARAMETR_ERROR);
        }
        return $out;
    }
}
?>