# pyrtm
A Python app to serve as a character sheet for the PnP RPG Rogue Trader

## Dependencies
In order to run pyrtm, you need the following dependencies:

* [Python 3](https://www.python.org/downloads/)
* [kivy](https://kivy.org/#download)

With those, you should be able to run pyrtm on any desktop machine.

Currently only building of .apk files for Android is supported. If you want to
do so, you'd also need:

* [buildozer](https://github.com/kivy/buildozer)

## Install
If you run pyrtm on a desktop machine, you don't have to install anything other
than the above mentioned dependencies. Just run `./main.py` and you should be
good to go.

To install it on a mobil device, first build the binaries with `make`. You can
find the build files in `bin`. Then copy the file to your device and install it
as you would normally do with a downloaded app file.
