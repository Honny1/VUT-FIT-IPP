<?php
define("PY", "python3.8");
define("PHP", "php");

abstract class AbstractTest {
    static public $num = 0;
    public $arg_parser;
    public $path;
    public $src;
    public $in;
    public $out;
    public $rc;
    public $expect_rc;
    public $std_out;
    public $std_err;
    
    public $result;
    public $returned_rc;
    public $error_msg;

    public function __construct($path, $arg_parser) {
        $this->result = "FAIL";
        $this->arg_parser = $arg_parser;

        $this->path = $path;
        $this->src = $path . ".src";
        $this->in = $path . ".in";
        $this->out = $path . ".out";
        $this->rc = $path . ".rc";
        $this->expect_rc = intval(trim(file_get_contents($this->rc)));
        $this->std_out = $path . ".TMP_std_out";
        $this->std_err = $path . ".TMP_std_err";
        $this->std_out_diff = $path . ".TMP_std_out_diff";
        $this->std_out_int = $path . ".TMP_std_out_int";
        $this->error_msg = "";
        
    }
    
    abstract public function exec_test();
    
    protected function test_parse() {
        $command_pattern = PHP . ' "%s" < "%s" > "%s" 2> "%s"';
        $parse_command = sprintf($command_pattern, $this->arg_parser->parser_script, $this->src, $this->std_out, $this->std_err);
        exec($parse_command, $output, $this->returned_rc);
        if($this->returned_rc == $this->expect_rc)
            $this->result = "PASS";
    }

    protected function diff_parse_out() {
        if($this->returned_rc != 0) return;
        $command_pattern = "java -jar \"%s/jexamxml.jar\" \"%s\" \"%s\" xml_diff.xml \"%s/options\"";
        $jexamxml_command = sprintf($command_pattern, $this->arg_parser->jexampath, $this->std_out, $this->out, $this->arg_parser->jexampath, $this->std_err);
        $output = null;
        $jexamxml_rc = null;
        exec($jexamxml_command, $output, $jexamxml_rc);
        unlink("xml_diff.xml");
        if($this->returned_rc != 0)
            $this->result = "FAIL";
    }

    protected function test_int($code_in) {
        $out = $code_in == $this->std_out ? $this->std_out_int: $this->std_out;
        $command_pattern = PY . " \"%s\" --input=\"%s\" --source=\"%s\" > \"%s\" 2> \"%s\"";
        $interpretr_command = sprintf($command_pattern, $this->arg_parser->int_script, $this->in, $code_in, $out, $this->std_err);
        $output = null;
        exec($interpretr_command, $output, $this->returned_rc);
        if($this->returned_rc == $this->expect_rc)
            $this->result = "PASS";
    }

    protected function diff_int_out() {
        if($this->returned_rc != 0) return;
        $in = file_exists($this->std_out_int)? $this->std_out_int: $this->std_out;
        $command_pattern = "diff -u \"%s\" \"%s\" > \"%s\" 2> \"%s\"";
        $diff_command = sprintf($command_pattern, $in, $this->out, $this->std_out_diff, $this->std_err);
        $output = null;
        exec($diff_command, $output, $this->returned_rc);
        if($this->returned_rc != 0)
            $this->result = "FAIL";
    }

    public function clean() {
        if (file_exists($this->std_out)) unlink($this->std_out);
        if (file_exists($this->std_err)) unlink($this->std_err);
        if (file_exists($this->std_out_diff)) unlink($this->std_out_diff);
        if (file_exists($this->std_out_int)) unlink($this->std_out_int);
    }

    public function add_to_html($dom_tree, $html_root) {
        $details = $dom_tree->createElement("details");
        $domAttribute = $dom_tree->createAttribute('open');
        if($this->result == "FAIL") $details->appendChild($domAttribute);
        
        $domAttribute = $dom_tree->createAttribute('class');
        $domAttribute->value = $this->result == "FAIL" ? "fail": "pass";
        
        static::$num++;
        $test_path_info = pathinfo($this->path);
        $summary = $dom_tree->createElement("summary", $this::$num . ". Test name: " . $test_path_info['basename']);
        $summary->appendChild($domAttribute);
        
        $ul = $dom_tree->createElement("ul");

        $li = $dom_tree->createElement("li", "Result: ". $this->result);
        $ul->appendChild($li);
        
        $li = $dom_tree->createElement("li", "Directory: ". $test_path_info['dirname']);
        $ul->appendChild($li);


        $summary->appendChild($ul);

        $details->appendChild($summary);

        if($this->result == "ERROR") {
            $err_msg = $dom_tree->createElement("p", $this->error_msg);
            $details->appendChild($err_msg);
            return;
        }
        
        $details_expected_er = $dom_tree->createElement("details");
        
        $domAttribute = $dom_tree->createAttribute('open');
        if($this->result == "FAIL") $details_expected_er->appendChild($domAttribute);

        $summary_expected_er = $dom_tree->createElement("summary", "Expected error code:");
        $details_expected_er->appendChild($summary_expected_er);
        $pre_expected_er = $dom_tree->createElement("pre", $this->expect_rc);
        $details_expected_er->appendChild($pre_expected_er);
        
        $details->appendChild($details_expected_er);


        $details_received_er = $dom_tree->createElement("details");
        $domAttribute = $dom_tree->createAttribute('open');
        if($this->result == "FAIL") $details_received_er->appendChild($domAttribute);

        $summary_received_er = $dom_tree->createElement("summary", "Received error code:");
        $details_received_er->appendChild($summary_received_er);
        $pre_received_er = $dom_tree->createElement("pre", $this->returned_rc);
        $details_received_er->appendChild($pre_received_er);

        $details->appendChild($details_received_er);


        $details_std_er = $dom_tree->createElement("details");
        $domAttribute = $dom_tree->createAttribute('open');
        if($this->result == "FAIL") $details_std_er->appendChild($domAttribute);

        $summary_std_er = $dom_tree->createElement("summary", "Received std error:");
        $details_std_er->appendChild($summary_std_er);
        $pre_std_er = $dom_tree->createElement("pre", file_get_contents($this->std_err));
        $details_std_er->appendChild($pre_std_er);

        $details->appendChild($details_std_er);


        $details_expected_out = $dom_tree->createElement("details");
        $domAttribute = $dom_tree->createAttribute('open');
        if($this->result == "FAIL") $details_expected_out->appendChild($domAttribute);

        $summary_expected_out = $dom_tree->createElement("summary", "Expected output:");
        $details_expected_out->appendChild($summary_expected_out);
        $pre_expected_out = $dom_tree->createElement("pre", file_get_contents($this->out));
        $details_expected_out->appendChild($pre_expected_out);

        $details->appendChild($details_expected_out);


        $details_received_out = $dom_tree->createElement("details");
        $domAttribute = $dom_tree->createAttribute('open');
        if($this->result == "FAIL") $details_received_out->appendChild($domAttribute);

        $summary_received_out = $dom_tree->createElement("summary", "Received output:");
        $details_received_out->appendChild($summary_received_out);
        $pre_received_out = $dom_tree->createElement("pre", file_get_contents($this->std_out));
        $details_received_out->appendChild($pre_received_out);
        
        $details->appendChild($details_received_out);

        if(file_exists($this->std_out_diff)) {
            $details_received_out = $dom_tree->createElement("details");
            $domAttribute = $dom_tree->createAttribute('open');
            if($this->result == "FAIL") $details_received_out->appendChild($domAttribute);

            $summary_received_out = $dom_tree->createElement("summary", "Received diff:");
            $details_received_out->appendChild($summary_received_out);
            $pre_received_out = $dom_tree->createElement("pre", file_get_contents($this->std_out_diff));
            $details_received_out->appendChild($pre_received_out);

            $details->appendChild($details_received_out);
        }

        $details_in_data = $dom_tree->createElement("details");
        $domAttribute = $dom_tree->createAttribute('open');
        if($this->result == "FAIL") $details_in_data->appendChild($domAttribute);

        $summary_in_data = $dom_tree->createElement("summary", "Input data:");
        $details_in_data->appendChild($summary_in_data);
        
        $details_in_data_code = $dom_tree->createElement("details");
        $domAttribute = $dom_tree->createAttribute('open');
        if($this->result == "FAIL") $details_in_data_code->appendChild($domAttribute);

        $summary_in_data_code = $dom_tree->createElement("summary", "Input code:");
        $details_in_data_code->appendChild($summary_in_data_code);
        $pre_in_data_code = $dom_tree->createElement("pre", file_get_contents($this->src));
        $details_in_data_code->appendChild($pre_in_data_code);
        
        $details_in_data->appendChild($details_in_data_code);

        $details_in_data_user = $dom_tree->createElement("details");
        $domAttribute = $dom_tree->createAttribute('open');
        if($this->result == "FAIL") $details_in_data_user->appendChild($domAttribute);

        $summary_in_data_user = $dom_tree->createElement("summary", "Input user:");
        $details_in_data_user->appendChild($summary_in_data_user);
        $pre_in_data_user = $dom_tree->createElement("pre", file_get_contents($this->in));
        $details_in_data_user->appendChild($pre_in_data_user);
        
        $details_in_data->appendChild($details_in_data_user);

        $details->appendChild($details_in_data);
        
        $html_root->appendChild($details);
    }
    
}

class Test extends AbstractTest {

    public function exec_test() {
        $this->test_parse();
        if($this->result != "FAIL") $this->diff_parse_out();
        if($this->result != "FAIL") $this->test_int($this->std_out);
        if($this->result != "FAIL") $this->diff_int_out();
    }

}

class TestOnlyParse extends AbstractTest {

    public function exec_test() {
        $this->test_parse();
        if($this->result != "FAIL") $this->diff_parse_out();
    }

}

class TestOnlyInt extends AbstractTest {

    public function exec_test() {
        $this->test_int($this->src);
        if($this->result != "FAIL") $this->diff_int_out();
    }

}
?>