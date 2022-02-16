<?php
define("HEADER", ".ippcode22");


class CodeParser {
    public $instructions;
    private $header;

    function __construct() {
        $this->instructions = array();
        $this->header = false;
    }

    function parse_instruction($line){
        echo "$line\n";
    }

    function remove_comment($line){
        if (str_contains($line, '#')){
            $line = strstr($line, '#', true);
            return $this->trim_line($line);
        }
        return $line;
    }

    function trim_line($line){
        $line = trim($line);
        return $line;
    }
    
    function is_missing_header(){
        if(!$this->header){
            fwrite(STDERR,"ERROR: Missing header!\n");
            exit(HEADER_ERROR);
        }
    }

    function parse() {
        $line = fgets(STDIN);
        if(!$line) { // Konec souboru nebo prázdný soubor
            $this->is_missing_header(); 
            return;
        }
        
        $line = $this->trim_line($line);
        $line = $this->remove_comment($line);

        if ($line == null){ 
            $this->parse();
            return;
        }

        if(!$this->header && strcasecmp(HEADER, $line) == 0){
            $this->header = true;
        } 
        $this->is_missing_header();
        $this->parse_instruction($line);
        $this->parse();
    }
}
