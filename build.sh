#!/bin/bash

[ -f ~/.env/abjad/bin/activate ] && . ~/.env/abjad/bin/activate

mkdir -p ./build

for py_file in jazz*.py
do
	echo "Generating pattern "$py_file
	python $py_file
done

python progression001.py -c
python progression001.py -f
