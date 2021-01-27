#!/bin/sh

# This script download all programs requires to run the Fourier Shell Occupancy algorithm

# The first step is to download Xmipp-lite and compile it (Xmipp lite is a xmipp version without CUDA, python, just resolution related algorithms)

echo "Cloning xmipp-lite repository..."
git clone https://github.com/Vilax/xmipp.git

echo " "
echo " "
echo "Compiling xmipp ..."
echo " "

cd xmipp
chmod +x xmipp
./xmipp get_devel_sources vi_bflr
./xmipp config 
./xmipp check_config
./xmipp get_dependencies
./xmipp compile
mkdir build
./xmipp install build/


cd ..

echo " "
echo " "
echo "Creating a virtual enviroment..."

ifvenv=$(pip list | grep virtualenv)
if [ "$ifvenv" != "*virtualenv*" ];
then
pip install virtualenv
fi

python3 -m venv env
. env/bin/activate
pip install --upgrade pip
pip install pyqt5
pip install matplotlib

# Editing paths
INITFILE="config.ini"
rm ${INITFILE}
XMIPP_PATH="/xmipp/build"

echo "[EXTERNAL_PROGRAMS]" >> $INITFILE
echo "XMIPP_PATH = ${PWD}${XMIPP_PATH}" >> $INITFILE


EXECUTABLEFILE="FSO"
echo "cd $(pwd)" >> $EXECUTABLEFILE
echo "$(pwd)/bfactor.py" >> $EXECUTABLEFILE
chmod +x ${EXECUTABLEFILE}









