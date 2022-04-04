#!/usr/bin/env bash

php test.php --directory internal_tests/tests/both --recursive --jexampath internal_tests/jexamxml > test.html; 
firefox test.html &

php test.php --directory internal_tests/tests/int-only --recursive --int-only > test-int-only.html; 
firefox test-int-only.html &

php test.php --directory internal_tests/tests/parse-only --recursive --parse-only --jexampath internal_tests/jexamxml > test-parse-only.html; 
firefox test-parse-only.html &
