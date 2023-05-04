
cd $ZT_SRC_FOLDER
if [ -d "mididings" ]; then
	rm -rf "mididings"
fi

git clone https://github.com/ponderworthy/mididings
cd mididings

python3 -m build
sudo pip install dist/mididings-*.whl

rm -rf "$ZT_SRC_FOLDER/mididings"
