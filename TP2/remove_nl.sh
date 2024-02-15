#!/usr/bin/bash

if [[ $# -ne 1 ]]; then
		echo "Usage : ./remove_nl.sh dir-name"
	exit
fi

dir=$1

if [ ! -d "$dir" ]; then
		echo "On attend un dossier."
	exit
fi

for text in "$dir"/*.txt; do
	tr '\n' ' ' < "$text" > "tmp.txt" && mv "tmp.txt" "$text"
	echo >> "$text"
done
