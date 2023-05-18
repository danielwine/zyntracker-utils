#!/bin/bash

# Dependencies for audio related tools

sudo apt install libjack-jackd2-dev
sudo apt install jalv lilv-utils

arch=$(uname -i)

if [ "$arch" == 'armv*' ];
then
sudo apt install lv2-dev
fi

pip install JACK-Client==0.5.4
pip install Kivy==2.1.0
pip install oscpy==0.6.0
