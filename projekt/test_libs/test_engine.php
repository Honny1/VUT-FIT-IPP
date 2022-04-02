<?php
require_once "error_codes.php";
require_once "test_class.php";

class TestEngine {
    public $arg_parser;
    public $tests;
    private $dom_tree;
    private $body;

    public function __construct($arg_parser) {
        $this->arg_parser = $arg_parser;
        $this->tests = array();
        $this->dom_tree = new DOMDocument('1.0');
        $this->dom_tree->loadHTML(file_get_contents(dirname(__FILE__) . DIRECTORY_SEPARATOR . "base.html"));
        $this->body = $this->dom_tree->getElementsByTagName('body');
        $this->body = $this->body[0];
    }

    public function load_tests(){
        $test_files = get_test_files($this->arg_parser->recursive, $this->arg_parser->directory);
        foreach ($test_files as $file) {
            if(str_ends_with($file, ".src")) {
                $test_path =substr($file, 0, -4);
                if (!in_array($test_path . ".in", $test_files)) 
                    touch($test_path . ".in");
                if (!in_array($test_path . ".out", $test_files)) 
                    touch($test_path . ".out");
                if (!in_array($test_path . ".rc", $test_files)) 
                    file_put_contents($test_path . ".rc", "0");
                
                if ($this->arg_parser->parse_only):
                    array_push($this->tests, new TestOnlyParse($test_path, $this->arg_parser));        
                elseif ($this->arg_parser->int_only):
                    array_push($this->tests, new TestOnlyInt($test_path, $this->arg_parser));
                else:
                    array_push($this->tests, new Test($test_path, $this->arg_parser));
                endif;
            }
        }
    }

    public function exec_tests(){
        foreach ($this->tests as $test){
            try {
                $test->exec_test();
            } catch (Exception $e) {
                $test->result = "ERROR";
                $test->error_msg = $e->getMessage();
            }
        }   
    }

    private function generate_info(){
        $sum = 0;
        $failed = 0;
        $pass = 0;
        foreach ($this->tests as $test){
            if($test->result == "FAIL")
                $failed++;
            if($test->result == "PASS")
                $pass++;
            $sum++;
        }
        $ul = $this->dom_tree->createElement("ul");
        
        $li = $this->dom_tree->createElement("li", "The tests were performed: ". date("d-m-y h:i:sa"));
        $ul->appendChild($li);

        $li = $this->dom_tree->createElement("li", "Number of tests: ". $sum);
        $ul->appendChild($li);
        
        $li = $this->dom_tree->createElement("li", "Number of passed tests: " . $pass);
        $ul->appendChild($li);
        
        $li = $this->dom_tree->createElement("li", "Number of failed tests: " . $failed);
        $ul->appendChild($li);
        
        $rec = "OFF";
        if($this->arg_parser->recursive) $rec = "ON";
        $li = $this->dom_tree->createElement("li", "Recursive: " . $rec);
        $ul->appendChild($li);

        $default = "PARSE and INTERPRETR";
        if($this->arg_parser->parse_only) $default = "PARSE";
        if($this->arg_parser->int_only) $default = "INTERPRETR";
        
        $li = $this->dom_tree->createElement("li", "Test mode: " . $default);
        $ul->appendChild($li);

        
        $h2 = $this->dom_tree->createElement("h2", "Tests INFO:");
        $this->body->appendChild($h2);
        
        $this->body->appendChild($ul);

        $h2 = $this->dom_tree->createElement("h2", "Tests Results:");
        $this->body->appendChild($h2);
        
        
    }

    public function generate_report(){
        $this->generate_info();
        foreach ($this->tests as $test){
            $test->add_to_html($this->dom_tree, $this->body);
            if(!$this->arg_parser->noclean) $test->clean();
        }
        echo $this->dom_tree->saveHTML();
    }
}

function get_test_files($recursive, $dir, &$test_files = array()){
    $files = scandir($dir);
    foreach ($files as $value) {
        $full_path = realpath($dir . DIRECTORY_SEPARATOR . $value);
        if (is_dir($full_path)){ 
            if ($recursive && $value != "." && $value != "..")
                get_test_files($recursive, $full_path, $test_files);
        } else {
            $test_files[] = $full_path;
        } 
    }
    return $test_files;
}
?>
