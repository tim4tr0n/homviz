#!/bin/sh
# Automatically downloads, extracts, and puts all files under one folder
# (to make it easier for Python to track the files) 


if [ -d "catalog/" ]; then rm -r catalog/; fi
wget http://gutenberg.readingroo.ms/cache/generated/feeds/rdf-files.tar.bz2
tar -xjf rdf-files.tar.bz2
rm rdf-files.tar.bz2
mv cache/ catalog/
cd catalog/
find . -mindepth 2 -type f -print -exec mv --backup=numbered {} . \;
rm -r epub/
