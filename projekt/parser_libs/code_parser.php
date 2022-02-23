<?php
require_once "instructions.php";
require_once "stats.php";
define("HEADER", ".ippcode22");


class CodeParser {
    private $header;
    private $row;
    private $dom_tree;
    private $xml_root;
    public $stats;

    function __construct() {
        $this->header = false;
        $this->row = 0;
        $this->stats = new Stats();

        $this->dom_tree = new DOMDocument('1.0', 'UTF-8');
        $this->dom_tree->formatOutput = true;
        $this->xml_root = $this->dom_tree->createElement("program");
        $this->xml_root->setAttribute("language", "IPPcode22");
        $this->dom_tree->appendChild($this->xml_root);
    }

    function check_instruction_parts($instruction_parts, $expected_num){
        if(count($instruction_parts) != $expected_num){
            fwrite(STDERR,"ERROR: Unexpected number of operands! ROW:".$this->row."\n");
            exit(LEX_SYN_ERROR);
        }
    }

    function parse_instruction($line){
        $instruction = null;
        $instruction_parts = preg_split("/\s+/", $line);
        $operation_code = strtoupper($instruction_parts[0]);
        if(in_array($operation_code, INSTRUCTIONS)){
            $this->check_instruction_parts($instruction_parts, 1);
            $instruction = new Instruction($this->row, $operation_code);
        } elseif(in_array($operation_code, INSTRUCTIONS_ONE_ARG)){
            $this->check_instruction_parts($instruction_parts, 2);
            $instruction = new InstructionOneArg($this->row, $operation_code, $instruction_parts[1]);
        } elseif(in_array($operation_code, INSTRUCTIONS_TWO_ARGS)){
            $this->check_instruction_parts($instruction_parts, 3);
            $instruction = new InstructionTwoArgs($this->row, $operation_code, $instruction_parts[1], $instruction_parts[2]);
        } elseif(in_array($operation_code, INSTRUCTIONS_THREE_ARGS)){
            $this->check_instruction_parts($instruction_parts, 4);
            $instruction = new InstructionThreeArgs($this->row, $operation_code, $instruction_parts[1], $instruction_parts[2], $instruction_parts[3]);
        }else{
            fwrite(STDERR,"ERROR: Unexpected operation code! ROW:".$this->row."\n");
            exit(OPERATION_CODE_ERROR);
        }
        $instruction->validate_instruction();
        $instruction->update_stats($this->stats);
        $instruction->as_xml($this->dom_tree, $this->xml_root);
    }

    function remove_comment($line){
        if (str_contains($line, '#')){
            $this->stats->add_comments();
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

    function generate_xml(){
        echo $this->dom_tree->saveXML();
    }
    function end_of_file(){
        $this->generate_xml();
        $this->stats->count_bad_or_fw_jumps();
    }

    function parse() {
        $line = fgets(STDIN);
        $this->row++;

        if(!$line) { // Konec souboru nebo prázdný soubor
            $this->is_missing_header(); 
            $this->end_of_file();
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
            $this->parse();
            return;
        } 
        $this->is_missing_header();
        $this->parse_instruction($line);
        $this->parse();
    }
}
