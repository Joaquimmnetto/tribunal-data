
pydir=../src/python/utils

pyexec='python'
unamestr=`uname`
if [[ "$unamestr" == 'Linux' ]]; then
   pyexec='python3'
fi

${pyexec} ${pydir}/$@
