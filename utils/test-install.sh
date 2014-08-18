#! /bin/bash

#
# A simple & quick script to test that a local development source distribution
# can be successfully installed in a fresh virtual environment via pip.
#


REPO_DIR="$HOME/programming/django-rest-framework-httpsignature"
VIRTUALENV_DIR="${REPO_DIR}/env"
DEST_DIR="$HOME/tmp/t"

set -e
set -x

# Build the source distribution
cd ${REPO_DIR}
source ${VIRTUALENV_DIR}/bin/activate
rm -rf dist/
python setup.py build sdist

# Move to the distination directory, create the test environment and instal.
mkdir ${DEST_DIR}
cd ${DEST_DIR}
virtualenv .
source bin/activate

pip install -U pip
pip install ${REPO_DIR}/dist/*

# The installation was successful. Destroy the test environment.
cd ${REPO_DIR}
rm -fr ${DEST_DIR}
