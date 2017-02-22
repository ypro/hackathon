# hackathon

# On Raspberry:
# setup git
sudo apt-get install git
git config --global user.email "you@example.com"
git config --global user.name "Your Name"

# clone repo
git clone https://github.com/fyhn/hackathon.git

# Install bluetooth
Follow instructions here
http://stackoverflow.com/questions/41351514/leadvertisingmanager1-missing-from-dbus-objectmanager-getmanagedobjects/41398903#41398903

# Connect to bluetooth device
sudo bluetoothctl
scan on
<look for your device>
connect <address>
exit

# Test bluetooth


# Setup python and tornado
sudo apt-get install python-pip
sudo pip install tornado


# On micro:bit
Add to "vid start":
bluetooth button service
bluetooth led service
bluetooth uart service
