# ZynTracker utils

ZynTracker utils are a collection of small Python modules in order to facilitate (remote) sequencing for the Zynthian open synth platform.

It supports phrase extraction from renoise files (xrns, xrni) and zynthian snapshot (zss) imports and exports.

It serves as a bridge between my Renoise projects and the Zynthian platform.
A standalone editor with graphical user interface _might_ be based on the Kivy UI framework.

## Renoise bridge

### Compile zynseq library on your linux system

`./lib/zynseq/build.sh`

### Install Python dependencies (based on the use case)

`pip install -r requirements.txt`

## Using the file converter / bridge

If no arguments are given, it will constantly monitor the changes in the standard project folder (preconfigured in config.py):

`python -m app.bridge`

Example to manually convert and upload a project
(imports phrases from test.xrns and uploads a ZSS to zynthian):

`python -m app.bridge test.xrns --upload 002`

## Interactive CLI / standalone editor (very experimental, only partially implemented)

### Software dependencies (mainly LinuxSampler)

There are install scripts (in /bin folder) for the following platforms:

arm7l for Raspberry Pi with Raspberry Pi OS Lite Buster
x86_64 for x86/64 with Ubuntu 22.04 LTS

### Starting the CLI / Kivy GUI

`python -m app.gui`
`python -m app.cli`
`python -m app.cli --simple`
