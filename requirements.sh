
sudo apt install libjack-jackd2-dev
sudo apt install jalv lilv-utils

arch=$(uname -i)

if [ "$arch" == 'armv*' ];
then
sudo apt install lv2-dev
fi
