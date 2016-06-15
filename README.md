# TouchUI

The TouchUI was initially started as part of the [ftcommunity-TXT
project](https://github.com/ftCommunity/ftcommunity-TXT).  It has now
become a stand-alone GUI project aiming to create a simple yet useful
user interface for small touch screen enabled devices like the
Raspberry Pi using a display module add-on.

![Launcher](https://raw.githubusercontent.com/harbaum/TouchUI/master/screenshots/launcher.png)
           
TouchUI is based on Python, Qt and PyQt. It runs on any device
supporting these incl. the Raspberry Pi and the Fischertechnik TXT.
It's designed for resultions from 240x320 to 480x320 / 320x480
and is meant to be used with a touchscreen. 

## PC Demo

The TouchUI can run an a PC inside a window. The launcher
([touchui/launcher.py](https://github.com/harbaum/TouchUI/blob/master/touchui/launcher.py))
can just be started. If apps are being used the enironment variable
PYTHONPATH needs to be set to the directory where
[TouchStyle.py](https://github.com/harbaum/TouchUI/blob/master/touchui/TouchStyle.py)
is located.
