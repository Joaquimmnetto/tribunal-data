
pydir=../src/python

pyexec='python'
unamestr=`uname`
if [[ "$unamestr" == 'Linux' ]]; then
   pyexec='python3'
fi

PYTHONPATH=${pydir} ${pyexec} -m $@
