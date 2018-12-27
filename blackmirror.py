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
    camera.resolution = Config.camres
    camera.framerate = 30
    rawCapture = PiRGBArray(camera, size=Config.camres)
     
    # allow the camera to warmup
    time.sleep(0.1)

    # camera does not have alpha channel, but framebuffer ignores alpha
    alpha = np.zeros((fb.minsize, fb.minsize, 1), dtype='B')

    offsety = int(fb.ysize/2) - int(Config.camres[0]/2)
    offsetx = int(fb.xsize/2) - int(Config.camres[1]/2)

    location = None
    skin = None
    im = None
    try:
        blocksize = 16
        slices = generateArraySlices(Config.camres[0], Config.camres[1], Config.blocksize)
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            now = time.time()

            # make mutable
            #im = np.copy(frame.array)
            # process
            # skin detection 100 < R - G < 500
            # possible alternative https://softexpert.wordpress.com/2007/10/17/skin-color-detection/
            # skincal(
            #     im, 
            #     slices, 
            #     Config.thresh_low, 
            #     Config.thresh_high
            # )

            im = frame.array
            im = skincal_(im, 
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