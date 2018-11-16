#!  /usr/bin/ksh

export  TEST_DIRECTORY=test
export  CURRENT_DIRECTORY=$( pwd )
export  PYTHONPATH="$( pwd )/src"

cd ${TEST_DIRECTORY}
python3 -m unittest discover
cd "${CURRENT_DIRECTORY}"
