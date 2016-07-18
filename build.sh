#!/bin/bash

ROOT_DIRNAME="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ZIP_FILENAME="package.zip"
VIRTUALENV_DIR="$HOME/.virtualenvs/asserts/lib/python2.7/site-packages"

echo "removing old package file"
rm $ROOT_DIRNAME/$ZIP_FILENAME

echo "adding virtualenv packages"
cd $VIRTUALENV_DIR
zip -r9 $ROOT_DIRNAME/$ZIP_FILENAME * &> /dev/null

echo "adding our script"
cd $ROOT_DIRNAME
zip -g $ZIP_FILENAME run.py &> /dev/null

echo "adding our credentials file"
zip -g $ZIP_FILENAME .env &> /dev/null
