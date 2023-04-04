#!/bin/bash

cd $RELIVE_SRC_FOLDER
if [ -d "alo" ]; then
	rm -rf "alo"
fi
git clone --recursive https://github.com/devcurmudgeon/alo.git
cd alo/source
make -j 3 BASE_OPTS="-O3 -ffast-math -fdata-sections -ffunction-sections"
make install
cp -r /usr/local/lib/lv2/alo.lv2 /usr/lib/lv2
rm -rf "alo"
