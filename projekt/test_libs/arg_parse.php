<?php
require_once "error_codes.php";

define("ARGS", array("test.php", "--help", "--recursive", "--parse-only", "--int-only", "--noclean"));
define("LONG_PARAMETERS", array("help", "directory:", "recursive", "parse-script:", "int-script:", "parse-only", "int-only", "jexampath:", "noclean"));
define("SHORT_PARAMETERS", "");

class ArgParser {
    public $argc;
    public $argv;
    public $options;

    public $directory;
    public $parser_script;
    public $int_script;
    public $jexampath;

    public $parse_only;
    public $int_only;
    public $recursive;
    public $noclean; 

    function __construct($argc, $argv) {
        $this->argc = $argc;
        $this->argv = $argv;
        $this->options = array();
        
        $this->parse_only = false;
        $this->int_only = false;
        $this->recursive = false;
        $this->noclean = false;
        
        $this->directory = realpath(getcwd());
        $this->parser_script = realpath(getcwd() . "/parse.php");
        $this->int_script = realpath(getcwd() . "/interpret.py");
        $this->jexampath = realpath("/pub/courses/ipp/jexamxml");
    }

    function help() {
        $message = "Usage: %s [--help][--directory=FILE][--recursive][--parse-script=FILE][--int-script=FILE][--parse-only][--int-only][--jexampath=FILE][--noclean]\n\n";
        $message .= "Test script of IPPcode22 code parser and interpretr. Generates HTML report on standard output.\n\n";
        $message .= "Optional arguments:\n";
        $message .="\t--help\t\t\t\tShow this help message and exit.\n";
        $message .="\t--directory=PATH\t\tThe path where the tests are searched. [If not specified - current directory]\n";
        $message .="\t--recursive\t\t\tSearch of tests recursively.\n";
        $message .="\t--parse-script=FILE\t\tThe file of parser of IPPCode22\n";
        $message .="\t--int-script=FILE\t\tThe file of interpreter of IPPCode22.\n";
        $message .="\t--parse-only\t\t\tTests only parser. Cannot be combined with: --int-only, --int-script\n";
        $message .="\t--int-only\t\t\tTests only interpretr. Cannot be combined with: --parse-only, --parse-scriptm, --jexampath\n";
        $message .="\t--jexampath=PATH\t\tPath to jexamxml.\n";
        $message .="\t--noclean\t\t\tDisables removing of temporary files.\n";

        echo sprintf($message, $this->argv[0]);
    }

    private function get_invalid_args(){
        $bad_args = array_diff($this->argv, ARGS);

        if(array_key_exists("directory", $this->options) && is_array($this->options["directory"]))
            return $bad_args;
        if(array_key_exists("parse-script", $this->options) && is_array($this->options["parse-script"]))
            return $bad_args;
        if(array_key_exists("int-script", $this->options) && is_array($this->options["int-script"]))
            return $bad_args;
        if(array_key_exists("jexampath", $this->options) && is_array($this->options["jexampath"]))
            return $bad_args;
        
        $bad_args = array_diff($bad_args, $this->options);  
        if(array_key_exists("directory", $this->options))
            $bad_args = array_diff($bad_args, array("--directory"));
        if(array_key_exists("parse-script", $this->options))
            $bad_args = array_diff($bad_args, array("--parse-script"));
        if(array_key_exists("int-script", $this->options) && is_array($this->options["int-script"]))
            $bad_args = array_diff($bad_args, array("--int-script"));
        if(array_key_exists("jexampath", $this->options))
            $bad_args = array_diff($bad_args, array("--jexampath"));

        foreach ($bad_args as $key => $value)
            if (str_starts_with($value, "--directory=") ||
                str_starts_with($value, "--parse-script=") || 
                str_starts_with($value, "--int-script=")||
                str_starts_with($value, "--jexampath=")
            )
                unset($bad_args[$key]);

        if(in_array($this->argv[0], $bad_args))
            if (($key = array_search($this->argv[0], $bad_args)) !== false)
                unset($bad_args[$key]);
        return $bad_args;
    }

    private function update_parameters(){
        if(array_key_exists("directory", $this->options))
            $this->directory = $this->options["directory"];
        if(array_key_exists("recursive", $this->options))
            $this->recursive = true; 
        if(array_key_exists("parse-script", $this->options))
            $this->parser_script = realpath($this->options["parse-script"]);
        if(array_key_exists("int-script", $this->options))
            $this->int_script = realpath($this->options["int-script"]);
        if(array_key_exists("parse-only", $this->options))
            $this->parse_only = true;
        if(array_key_exists("int-only", $this->options))
            $this->int_only = true;
        if(array_key_exists("jexampath", $this->options))
            $this->jexampath = realpath($this->options["jexampath"]);
        if(array_key_exists("noclean", $this->options))
            $this->noclean = true;
    }

    private function check_parameter_combinations(){
        if(array_key_exists("parse-only", $this->options) && array_key_exists("int-script", $this->options)){
            fwrite(STDERR,"ERROR: Bad parameter combination!\n");
            $this->help();
            exit(PARAMETR_ERROR);
        }
        if(array_key_exists("int-only", $this->options) && array_key_exists("parse-script", $this->options) && array_key_exists("jexampath", $this->options)) {
            fwrite(STDERR,"ERROR: Bad parameter combination!\n");
            $this->help();
            exit(PARAMETR_ERROR);
        }
        if(array_key_exists("parse-only", $this->options) && array_key_exists("int-only", $this->options)) {
            fwrite(STDERR,"ERROR: Bad parameter combination!\n");
            $this->help();
            exit(PARAMETR_ERROR);
        }
    }

    private function check_if_exist_files_or_is_available_path(){
        if(!file_exists($this->directory)){
            fwrite(STDERR,"ERROR: Directory does not exist!\n");
            exit(FILE_OR_PATH_ERROR);
        }

        if(!file_exists($this->parser_script)){
            if(!$this->int_only) {
                fwrite(STDERR,"ERROR: Parse script does not exist!\n");
                exit(FILE_OR_PATH_ERROR);
            }
        }

        if(!file_exists($this->jexampath) && $this->parse_only){
            if(!$this->int_only) {
                fwrite(STDERR,"ERROR: Jexamxml directory does not exist!\n");
                exit(FILE_OR_PATH_ERROR);
            }
        }
        
        if(!file_exists($this->int_script)){
            if(!$this->parse_only) {
                fwrite(STDERR,"ERROR: Interpretr script does not exist!\n");
                exit(FILE_OR_PATH_ERROR);
            }
        }
    }

    function parse() {
        $this->options = getopt(SHORT_PARAMETERS, LONG_PARAMETERS);
        $bad_args = $this->get_invalid_args();
        if (array_key_exists("help", $this->options)){
            $this->help();
            exit(EXIT_OK);
        }
        if (!empty($bad_args)){
            fwrite(STDERR,"ERROR: Bad parameter!\n");
            $this->help();
            exit(PARAMETR_ERROR);
        }
        $this->check_parameter_combinations();
        $this->update_parameters();
        $this->check_if_exist_files_or_is_available_path();
    }
}
?>
