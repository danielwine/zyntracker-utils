# ZynTracker utils

ZynTracker utils are a collection of small Python modules in order to facilitate (remote) sequencing for the Zynthian open synth platform.

It supports phrase extraction from renoise files (xrns, xrni) and zynthian snapshot (zss) imports and exports.

It serves as a bridge between my Renoise projects and the Zynthian platform.
A standalone editor with graphical user interface *might* be based on the Kivy UI framework.


## Renoise bridge
### Compile zynseq library on your linux system

./lib/zynseq/build.sh

## Using the file converter / bridge

Example to convert and upload a project
(imports phrases from test.xrns and uploads a ZSS to zynthian):

python -m app.bridge test.xrns --upload 002

To run server
(watches for changes in the standard folder preconfigured in config.py):

python -m app.bridge --serve

## Interactive CLI / standalone editor (experimental, only partially implemented)

### Software dependencies (mainly LinuxSampler)

There are install scripts (in /bin folder) for the following platforms:

arm7l for Raspberry Pi with Raspberry Pi OS Lite Buster
x86_64 for x86/64 with Ubuntu 22.04 LTS
### Install Python dependencies

pip install -r requirements.txt

### Starting the CLI / Kivy GUI

python -m app.gui
python -m app.cli
python -m app.cli --simple
