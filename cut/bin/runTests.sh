#!  /usr/bin/ksh

export  TEST_DIRECTORY=test
export  CURRENT_DIRECTORY=$( pwd )

cd ${TEST_DIRECTORY}
python -m unittest discover
cd "${CURRENT_DIRECTORY}"
