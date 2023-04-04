
cd $RELIVE_SRC_FOLDER
if [ -d "mididings" ]; then
	rm -rf "mididings"
fi

git clone https://github.com/ponderworthy/mididings
cd mididings

python3 setup.py build
sudo python3 setup.py install

rm -rf "$RELIVE_SRC_FOLDER/mididings"
