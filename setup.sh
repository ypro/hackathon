sudo apt-get update
sudo apt-get upgrade

sudo apt-get install -y libusb-dev libdbus-1-dev libglib2.0-dev libudev-dev libical-dev libreadline-dev

BLUEZ_REV=5.44
wget http://www.kernel.org/pub/linux/bluetooth/bluez-${BLUEZ_REV}.tar.xz
tar -xvf bluez-${BLUEZ_REV}.tar.xz
cd bluez-${BLUEZ_REV}
./configure
make
sudo make install

sudo systemctl daemon-reload
sudo systemctl restart bluetooth

sudo apt-get install python-dev libdbus-1-dev libdbus-glib-1-dev
sudo apt-get install python-pip
sudo apt-get install --reinstall python-gi

sudo python2.7 -m pip install dbus-python
sudo python2.7 -m pip install tornado
