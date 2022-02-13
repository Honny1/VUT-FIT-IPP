#!/usr/bin/env bash

set -e -o pipefail

vas_vystup=$1
referencni=$2

java -jar ./jexamxml/jexamxml.jar $vas_vystup $referencni delta.xml ./options
