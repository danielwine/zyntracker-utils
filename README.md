
# ReLive

ReLive is a minimalistic and experimental Python application under development for sequencing and performing synthesizer-based music using Zynaddsubfx, LinuxSampler and the zynseq c++ library made by the Zynthian project / Brian Walton.

At the moment it has only a few basic functions and consists of only a few structural scripts and a command line interface. The idea is that the graphical user interface will be based on the Kivy UI framework.

## Software dependencies

Check out the install scripts in the 'bin' folder.
Target platforms are:

arm7l    for Raspberry Pi with Raspberry Pi OS Lite Buster
x86_64   for x86/64 with Ubuntu 22.04 LTS

## Python dependencies

JACK-Client
Kivy
oscpy

## Usage

python -m relive.cli
python -m relive.gui
python -m relive.diagnose
