
# ZynTracker

ZynTracker is a simple, experimental Python tool under development for sequencing (or even performing) sample-based music using LinuxSampler, JACK and the zynseq c++ library made by the Zynthian project / Brian Walton.

It is intended to run on both desktop linux and raspberry pi os and supports phrase extraction from renoise files (xrns, xrni) and zynthian snapshot (zss) imports and exports.

At the moment it only has an interactive command-line interface for running basic commands such as note editing and file conversion. 
It serves as a bridge between my Renoise projects and the Zynthian platform.
A graphical user interface might be based on the Kivy UI framework.

## Software dependencies

There are install scripts (in /bin folder) for the following targeted platforms:

arm7l    for Raspberry Pi with Raspberry Pi OS Lite Buster
x86_64   for x86/64 with Ubuntu 22.04 LTS

## Python dependencies

JACK-Client
Kivy
oscpy

## Usage

The main entry points to the application are:

python -m app.gui
python -m app.cli
python -m app.cli --simple
