class Config(object):
    thresh_low = 25
    thresh_high = 150
    blocksize = 16
    resolution = (640, 480)
    framerate = 30
    iso = 400
    brightness = 50 #0-100
    contrast = 0 #-100 - 100
    hflip = False
    vflip = True
    awb_mode = 'auto' # 'off', 'auto', 'sunlight', 'cloudy', 'shade', 'tungsten', 'fluorescent', 'incandescent', 'flash', 'horizon'
    resize_scale = 1. # how big to resize, [0, 1]