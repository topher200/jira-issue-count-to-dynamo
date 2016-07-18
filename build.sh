#!/bin/bash

ROOT_DIRNAME="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ZIP_FILENAME="package.zip"

# remove old package file
rm $ROOT_DIRNAME/$ZIP_FILENAME

# add virtualenv packages
cd ~/.virtualenvs/asserts/lib/python2.7/site-packages
zip -r9 $ROOT_DIRNAME/$ZIP_FILENAME * &> /dev/null

# add our script
cd $ROOT_DIRNAME
zip -g $ZIP_FILENAME run.py &> /dev/null
