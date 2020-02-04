#!/bin/sh
# An install script for pulling the Project Gutenberg Catalog and installing the necessary Python dependencies

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
rm *.rdf.~1~

# Install Python Dependencies
pip3 install rdflib pywikibot requests wget firebase_admin
