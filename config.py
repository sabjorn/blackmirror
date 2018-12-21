import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    thresh_low = 15
    thresh_high = 150
    blocksize = 16
    camres = (512,512)