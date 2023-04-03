wget https://libsdl.org/projects/SDL_image/release/SDL2_image-2.0.5.tar.gz
tar -zxvf SDL2_image-2.0.5.tar.gz
pushd SDL2_image-2.0.5
./configure
make -j$(nproc)
sudo make install
popd

wget https://libsdl.org/projects/SDL_mixer/release/SDL2_mixer-2.0.4.tar.gz
tar -zxvf SDL2_mixer-2.0.4.tar.gz
pushd SDL2_mixer-2.0.4
./configure
make -j$(nproc)
sudo make install
popd

wget https://libsdl.org/projects/SDL_ttf/release/SDL2_ttf-2.0.15.tar.gz
tar -zxvf SDL2_ttf-2.0.15.tar.gz
pushd SDL2_ttf-2.0.15
./configure
make -j$(nproc)
sudo make install
popd

rm -r SDL2*

