#!/usr/bin/env bash

PARSER="../../../parse.php" 

for i in  $(find . -iname "*.src"); do
	# IN=$(echo $i | sed 's/\(.*\)\.src/\1.in/g')
	OUT=$(echo $i | sed 's/\(.*\)\.src/\1.out/g')
	RC=$(echo $i | sed 's/\(.*\)\.src/\1.rc/g')
	
	ERR_C=$(cat "$RC")
	php "$PARSER" < "$i" > "$i.out" 2>err.txt
	RETURNED=$?
	if [ "$RETURNED" == "0" ]; then
		java -jar ../../jexamxml/jexamxml.jar "$i.out" "$OUT" diffs.xml ../../options
		DIFFOK=$?
		if [ "$DIFFOK" == "0" ]; then
			rm "$i.out"
		else
			echo "$i"
			echo "DIFFERENCE to $OUT"
			cat ./diffs.xml 
		fi
	else
		if [ "$RETURNED" != "$ERR_C" ]; then
			echo "ERROR CODE BAD!"
			echo "$RETURNED"
		fi
	fi
        echo
done;

exit 0
