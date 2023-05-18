# ZynTracker utils

ZynTracker utils are a collection of small Python modules in order to facilitate (remote) sequencing for the Zynthian open synth platform.

It supports phrase extraction from renoise files (xrns, xrni) and zynthian snapshot (zss) imports and exports.

It serves as a bridge between my Renoise projects and the Zynthian platform.
A standalone editor with graphical user interface _might_ be based on the Kivy UI framework.

## Renoise bridge

### Installation

Run the install script

` ./install.sh `

It compiles the zynseq library and installs basic python dependencies.
Change the configuration according to your needs (app/config.py).

### Usage

If no arguments are given, it will constantly monitor the changes in the standard project folder (preconfigured in config.py):

`python -m app.bridge`

Example to manually convert and upload a project
(imports phrases from test.xrns and uploads a ZSS to zynthian):

`python -m app.bridge test.xrns --upload 002`

## Interactive CLI / standalone editor (very experimental, only partially implemented)

### Software dependencies

Install basic dependencies with

` ./bin/audio.sh `

Install LinuxSampler
(there are further install scripts (in /bin folder) for different platforms)

### Starting the CLI / Kivy GUI

`python -m app.gui`
`python -m app.cli`
`python -m app.cli --simple`
