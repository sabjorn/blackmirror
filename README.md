# Black Mirror
## About
Project in collaboration with Marlene Jess where a live video feed is dispalted on a screen, augmented to pixelate anything which matches human skin.

Uses direct Linux framebuffer manipulation with Python.

## Installation
For installing on Raspbian, run:

```
sudo su
export GITBRANCH=master
wget -O - https://raw.githubusercontent.com/sabjorn/blackmirror/${GITBRANCH}/install.sh | bash
```

## Components
* Raspberry Pi 3
    * Python
* [PI Camera](https://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/)

## Notes
### Screen Blanking
To prevent screen from sleeping, must add:
Based on [this](https://www.raspberrypi.org/documentation/configuration/screensaver.md)

```
consoleblank=0
```
to
`/boot/cmdline.txt`
