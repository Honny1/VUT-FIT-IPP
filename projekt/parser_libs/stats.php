<?php
require_once "error_codes.php";

class Stats {
    public $loc;
    public $comments;
    public $labels;
    public $jumps;

    private $jumps_and_labels;
    private $bad_or_fw_jumps;
    public $fwjumps;
    public $backjumps;
    public $badjumps;

    function __construct() {
        $this->loc = 0;
        $this->comments = 0;
        $this->labels = 0;
        $this->jumps = 0;

        $this->jumps_and_labels = array();
        $this->bad_or_fw_jumps = array();
        $this->fwjumps = 0;
        $this->backjumps = 0;
        $this->badjumps = 0;
    }

    function add_loc(){
        $this->loc++;
    }

    function add_comments(){
        $this->comments++;
    }

    function add_label($label){
        if(in_array("L_".$label, $this->jumps_and_labels)){
            $this->labels++;
            array_push($this->jumps_and_labels, "L_".$label);
        }
    }

    function add_jump($jump){
        $this->jumps++;
        array_push($this->jumps_and_labels, "J_".$jump);
        if(in_array("L_".$jump, $this->jumps_and_labels)){
            $this->backjumps++;
        } else {
            array_push($this->bad_or_fw_jumps, $jump);   
        }
    }

    function count_bad_or_fw_jumps(){
        foreach ($this->bad_or_fw_jumps as $jump) {
            if(in_array("L_".$jump, $this->jumps_and_labels)){
                $this->fwjumps++;            
            } else {
                $this->badjumps++;
            } 
        }
    }
    
    function save_stats($where_and_what){
        foreach ($where_and_what as $file_name => $stats) {
            $file = fopen($file_name, "w") or exit(OUTPUT_FILE_OPEN_ERROR);
            $data = "";
            foreach ($stats as $value) {
                switch ($value) {
                    case "--comments":
                        $data .= $this->comments . "\n" ;
                        break;
                    case "--loc":
                        $data .= $this->loc . "\n" ;
                        break;
                    case "--labels":
                        $data .= $this->labels . "\n" ;
                        break;
                    case "--jumps":
                        $data .= $this->jumps . "\n" ;
                        break;
                    case "--fwjumps":
                        $data .= $this->fwjumps . "\n" ;
                        break;
                    case "--backjumps":
                        $data .= $this->backjumps . "\n" ;
                        break;
                    case "--badjumps":
                        $data .= $this->badjumps . "\n" ;
                        break;
                    default:
                        fwrite(STDERR,"ERROR: Internal error!\n");
                        exit(INTERNAL_ERROR);
                        break;
                }
            }
            fwrite($file, $data);
            fclose($file);
        }
    }
}

?>