# Black Mirror
## About
Project in collaboration with Marlene Jess where a live video feed is dispalted on a screen, augmented to pixelate anything which matches a human skin.


## Components
* Raspberry Pi 3
    * Python
    * [OpenCV](https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/)
* [PI Camera](https://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/)

## Notes
Setup information for PI Camera available [here](https://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/)

When compiling OpenCV, the RPI needs the swap space extended (see [this](https://raspberrypi.stackexchange.com/questions/70/how-to-set-up-swap-space)):

```
/etc/dphys-swapfile 
The content is very simple. By default my Raspbian has 100MB of swap:

CONF_SWAPSIZE=100
If you want to change the size, you need to modify the number and restart dphys-swapfile:

/etc/init.d/dphys-swapfile restart
```