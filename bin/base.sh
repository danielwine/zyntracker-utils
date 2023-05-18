#!/bin/bash

# Base dependencies (for running the bridge)

sudo apt install cmake -y
./lib/zynseq/build.sh

pip install pysftp==0.2.9 watchdog==3.0.0
