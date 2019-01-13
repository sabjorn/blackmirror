#!/usr/bin/python3

import sys
import time
import os
import argparse
import logging

import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera

from skincal import *
from config import Config

from numpyfb import NumpyFb
from PIL import Image

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", help='enable/disable debug print')
    
    args = parser.parse_args()

    loglevel = logging.INFO
    if (args.debug is not None):
        loglevel = logging.DEBUG
    logging.basicConfig(level=loglevel, format='%(asctime)s %(message)s')
    logging.info('Started')

    fb = NumpyFb()
    fb.clear()

    # initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    camera.resolution = Config.resolution
    camera.framerate = Config.framerate
    camera.iso = Config.iso
    camera.brightness = Config.brightness
    camera.contrast = Config.contrast
    camera.awb_mode = Config.awb_mode
    camera.hflip = Config.hflip
    camera.vflip = Config.vflip
    rawCapture = PiRGBArray(camera, size=Config.resolution)
     
    # allow the camera to warmup
    time.sleep(0.1)

    # camera does not have alpha channel, but framebuffer ignores alpha
    alpha = np.zeros((fb.minsize, fb.minsize, 1), dtype='B')

    offsety = int(fb.ysize/2) - int(Config.resolution[0]/2)
    offsetx = int(fb.xsize/2) - int(Config.resolution[1]/2)

    location = None
    skin = None
    im = None
    try:
        blocksize = 16
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            now = time.time()

            im = frame.array
            im = skincal(im, 
                Config.thresh_low, 
                Config.thresh_high, 
                blocksize=Config.blocksize)

            # pad with alpha
            im = np.array(Image.fromarray(im).resize((fb.minsize, fb.minsize)))
            im = np.dstack((im, alpha)) # camera has no opacity value
        
            # copy out
            np.copyto(fb.array[:fb.minsize, :fb.minsize, :], im)
            rawCapture.truncate(0)
            later = time.time()
            logging.debug("fps: {}".format(1/(later - now)))
    except KeyboardInterrupt as e:
        fb.clear()
        logging.debug("KeyboardInterrupt, exiting")
        sys.exit(0)
    except Exception as e:
        logging.error(e)
        fb.clear()
        sys.exit(0)