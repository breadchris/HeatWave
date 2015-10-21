#!/bin/bash
echo [*] Getting pin
wget --content-disposition http://software.intel.com/sites/landingpage/pintool/downloads/pin-2.14-71313-gcc.4.4.7-linux.tar.gz
echo [+] Done getting pin

tar -xvf pin-2.14-71313-gcc.4.4.7-linux.tar.gz
rm pin-2.14-71313-gcc.4.4.7-linux.tar.gz
cd pin-2.14-71313-gcc.4.4.7-linux/source/tools

echo [*] Making pin tools
#make
echo [*] Done making pin tools

git clone https://github.com/blankwall/Python_Pin.git
cd Python_Pin/

echo [*] Making pin python
make
echo [+] Done making pin python

cd ..
mv Python_Pin/ ../../..
cd ..
cp -r tools ../..
cd ../..

sudo cp pin-2.14-71313-gcc.4.4.7-linux/intel64/bin/pinbin /usr/local/bin/pin
cp -r Python_Pin/obj-intel64 .
cp -r Python_Pin/examples .

rm -rf Python_Pin
rm -rf pin-2.14-71313-gcc.4.4.7-linux
