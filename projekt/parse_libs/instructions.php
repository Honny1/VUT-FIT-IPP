<?php
require_once "error_codes.php";

define("INSTRUCTIONS", array("CREATEFRAME", "PUSHFRAME", "POPFRAME", "RETURN", "BREAK"));
define("INSTRUCTIONS_ONE_ARG", array("DEFVAR", "CALL", "PUSHS", "POPS", "WRITE", "LABEL", "JUMP", "DPRINT", "EXIT"));
define("INSTRUCTIONS_TWO_ARGS", array("MOVE", "INT2CHAR", "READ", "STRLEN", "TYPE", "NOT"));
define("INSTRUCTIONS_THREE_ARGS", array("ADD", "SUB", "MUL", "IDIV", "LT", "GT", "EQ", "AND", "OR", "STRI2INT", "CONCAT", "GETCHAR", "SETCHAR", "JUMPIFEQ", "JUMPIFNEQ"));

abstract class AbstractInstruction {
    public $operation_code;
    static public $num = 0;
    public $row;
    
    private $regex_int = "/^int@[+-]?[0-9]+$/";
    private $regex_str = "/^string@([^\\\\\r\n\t\f\v ]|\\\\\d\d\d)*$/";
    private $regex_bool = "/^bool@(true|false)$/";
    private $regex_nil = "/^nil@nil$/";

    private $regex_var = "/^(LF|GF|TF)@[a-zA-Z_\-$&%\*\!\?][\w_\-$&%\*\!\?]*$/";

    private $regex_types = "/^(int|string|bool)$/";

    private $regex_label = "/^[a-zA-Z_\-$&%\*\!\?][\w_\-$&%\*\!\?]*$/";

    abstract public function validate_instruction();
    abstract public function as_xml($dom_tree, $xml_root);

    abstract public function update_stats($stats);

    protected function validate_var($arg) {
        if (preg_match($this->regex_var, $arg)) return;
        fwrite(STDERR, "ERROR: Bad var! ROW: " . $this->row . "\n");
        exit(LEX_SYN_ERROR);
    }

    protected function validate_symb($arg) {
        if (preg_match($this->regex_int, $arg) ||
            preg_match($this->regex_str, $arg) ||
            preg_match($this->regex_bool, $arg) ||
            preg_match($this->regex_nil, $arg) ||
            preg_match($this->regex_var, $arg)
        ) return;
        fwrite(STDERR, "ERROR: Bad constant! ROW: " . $this->row . "\n");
        exit(LEX_SYN_ERROR);
    }

    protected function validate_type($arg) {
        if (preg_match($this->regex_types, $arg)) return;
        fwrite(STDERR, "ERROR: Bad type! ROW: " . $this->row . "\n");
        exit(LEX_SYN_ERROR);
    }

    protected function validate_label($arg) {
        if (preg_match($this->regex_label, $arg)) return;
        fwrite(STDERR, "ERROR: Bad label! ROW: " . $this->row . "\n");
        exit(LEX_SYN_ERROR);
    }

    public function get_arg_type($arg) {
        if (preg_match($this->regex_int, $arg)) return "int";
        if (preg_match($this->regex_bool, $arg)) return "bool";
        if (preg_match($this->regex_str, $arg)) return "string";
        if (preg_match($this->regex_nil, $arg)) return "nil";
        if (preg_match($this->regex_types, $arg)) return "type";
        if (preg_match($this->regex_var, $arg)) return "var";
        if (preg_match($this->regex_label, $arg)) return "label";
        return "";
    }

    public function get_arg_value($arg) {
        $prefix = "";
        $data = "";
        if (preg_match($this->regex_var, $arg)){
            $prefix = strstr($arg, '@', true);
            $data = htmlspecialchars(strstr($arg, '@'));
        }elseif(str_contains($arg, '@')){
            $data = strstr($arg, '@');
            $data = substr($data, 1);
            $data = htmlspecialchars($data);
        }else{
            $data = htmlspecialchars($arg);
        }
        return $prefix . $data;
    }
}


class Instruction extends AbstractInstruction {

    public function __construct($row, $operation_code) {
        static::$num++;
        $this->row = $row;
        $this->operation_code = $operation_code;
    }

    public function validate_instruction() {
        if (!in_array($this->operation_code, INSTRUCTIONS)) {
            fwrite(STDERR, "ERROR: Unexpected operation code! ROW:" . $this->row . "\n");
            exit(OPERATION_CODE_ERROR);
        }
    }

    public function update_stats($stats) {
        $stats->add_loc();
        if ($this->operation_code == "RETURN")
            $stats->add_return_jump();
    }

    public function as_xml($dom_tree, $xml_root) {
        $instruction = $dom_tree->createElement("instruction");
        $xml_root->appendChild($instruction);
        $instruction->setAttribute("order", $this::$num);
        $instruction->setAttribute("opcode", $this->operation_code);
    }
}

class InstructionOneArg extends AbstractInstruction {
    public $arg1;

    public function __construct($row, $operation_code, $arg1) {
        static::$num++;
        $this->row = $row;
        $this->operation_code = $operation_code;
        $this->arg1 = $arg1;
    }

    public function update_stats($stats) {
        $stats->add_loc();
        if ($this->operation_code == "LABEL")
            $stats->add_label($this->arg1);
        if ($this->operation_code == "JUMP" || $this->operation_code == "CALL")
            $stats->add_jump($this->arg1);
    }

    public function validate_instruction() {
        switch ($this->operation_code) {
            case 'DEFVAR':
                $this->validate_var($this->arg1);
                break;
            case 'CALL':
                $this->validate_label($this->arg1);
                break;
            case 'PUSHS':
                $this->validate_symb($this->arg1);
                break;
            case 'POPS':
                $this->validate_var($this->arg1);
                break;
            case 'WRITE':
                $this->validate_symb($this->arg1);
                break;
            case 'LABEL':
                $this->validate_label($this->arg1);
                break;
            case 'JUMP':
                $this->validate_label($this->arg1);
                break;
            case 'EXIT':
                $this->validate_symb($this->arg1);
                break;
            case 'DPRINT':
                $this->validate_symb($this->arg1);
                break;
            default:
                echo $this->operation_code;
                echo "\n";
                fwrite(STDERR, "ERROR: Unexpected operation code! ROW:" . $this->row . "\n");
                exit(OPERATION_CODE_ERROR);
                break;
        }
    }

    public function as_xml($dom_tree, $xml_root) {
        $instruction = $dom_tree->createElement("instruction");
        $xml_root->appendChild($instruction);
        $instruction->setAttribute("order", $this::$num);
        $instruction->setAttribute("opcode", $this->operation_code);

        $arg1 = $dom_tree->createElement("arg1", $this->get_arg_value($this->arg1));
        $instruction->appendChild($arg1);
        $arg1->setAttribute("type", $this->get_arg_type($this->arg1));
        
    }
}

class InstructionTwoArgs extends AbstractInstruction {
    public $arg1;
    public $arg2;

    public function __construct($row, $operation_code, $arg1, $arg2) {
        static::$num++;
        $this->row = $row;
        $this->operation_code = $operation_code;
        $this->arg1 = $arg1;
        $this->arg2 = $arg2;
    }

    public function update_stats($stats) {
        $stats->add_loc();
    }

    public function validate_instruction() {
        switch ($this->operation_code) {
            case 'MOVE':
                $this->validate_var($this->arg1);
                $this->validate_symb($this->arg2);
                break;
            case 'INT2CHAR':
                $this->validate_var($this->arg1);
                $this->validate_symb($this->arg2);
                break;
            case 'READ':
                $this->validate_var($this->arg1);
                $this->validate_type($this->arg2);
                break;
            case 'STRLEN':
                $this->validate_var($this->arg1);
                $this->validate_symb($this->arg2);
                break;
            case 'TYPE':
                $this->validate_var($this->arg1);
                $this->validate_symb($this->arg2);
                break;
            case 'NOT':
                $this->validate_var($this->arg1);
                $this->validate_symb($this->arg2);
                break;
            default:
                fwrite(STDERR, "ERROR: Unexpected operation code! ROW:" . $this->row . "\n");
                exit(OPERATION_CODE_ERROR);
                break;
        }
    }

    public function as_xml($dom_tree, $xml_root) {
        $instruction = $dom_tree->createElement("instruction");
        $xml_root->appendChild($instruction);
        $instruction->setAttribute("order", $this::$num);
        $instruction->setAttribute("opcode", $this->operation_code);

        $arg1 = $dom_tree->createElement("arg1", $this->get_arg_value($this->arg1));
        $instruction->appendChild($arg1);
        $arg1->setAttribute("type", $this->get_arg_type($this->arg1));

        $arg2 = $dom_tree->createElement("arg2", $this->get_arg_value($this->arg2));
        $instruction->appendChild($arg2);
        $arg2->setAttribute("type", $this->get_arg_type($this->arg2));
    }
}

class InstructionThreeArgs extends AbstractInstruction {
    public $arg1;
    public $arg2;
    public $arg3;

    public function __construct($row, $operation_code, $arg1, $arg2, $arg3) {
        static::$num++;
        $this->row = $row;
        $this->operation_code = $operation_code;
        $this->arg1 = $arg1;
        $this->arg2 = $arg2;
        $this->arg3 = $arg3;
    }

    public function update_stats($stats) {
        $stats->add_loc();
        if ($this->operation_code == "JUMPIFEQ")
            $stats->add_jump($this->arg1);
        if ($this->operation_code == "JUMPIFNEQ")
            $stats->add_jump($this->arg1);
    }

    public function validate_instruction() {
        switch ($this->operation_code) {
            case 'ADD':
            case 'SUB':
            case 'MUL':
            case 'IDIV':
            case 'LT':
            case 'GT':
            case 'EQ':
            case 'AND':
            case 'OR':
            case 'STRI2INT':
            case 'CONCAT':
            case 'GETCHAR':
            case 'SETCHAR':
                $this->validate_var($this->arg1);
                $this->validate_symb($this->arg2);
                $this->validate_symb($this->arg3);
                break;
            case 'JUMPIFEQ':
            case 'JUMPIFNEQ':
                $this->validate_label($this->arg1);
                $this->validate_symb($this->arg2);
                $this->validate_symb($this->arg3);
                break;
            default:
                fwrite(STDERR, "ERROR: Unexpected operation code! ROW:" . $this->row . "\n");
                exit(OPERATION_CODE_ERROR);
                break;
        }
    }

    public function as_xml($dom_tree, $xml_root) {
        $instruction = $dom_tree->createElement("instruction");
        $xml_root->appendChild($instruction);
        $instruction->setAttribute("order", $this::$num);
        $instruction->setAttribute("opcode", $this->operation_code);

        $arg1 = $dom_tree->createElement("arg1", $this->get_arg_value($this->arg1));
        $instruction->appendChild($arg1);
        $arg1->setAttribute("type", $this->get_arg_type($this->arg1));

        $arg2 = $dom_tree->createElement("arg2", $this->get_arg_value($this->arg2));
        $instruction->appendChild($arg2);
        $arg2->setAttribute("type", $this->get_arg_type($this->arg2));
    
        $arg3 = $dom_tree->createElement("arg3", $this->get_arg_value($this->arg3));
        $instruction->appendChild($arg3);
        $arg3->setAttribute("type", $this->get_arg_type($this->arg3));    
    }
}
