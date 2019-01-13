import numpy as np

def skincal(im, low, high, blocksize=16, format="bgr"):
    # makes an [x,y] accessor of blocksize x blocksize blocks
    blocks = im.reshape(
        im.shape[0]//blocksize, 
        blocksize, 
        im.shape[1]//blocksize, 
        blocksize, 3).swapaxes(1, 2)

    blocks2 = blocks.reshape(
        im.shape[0]*im.shape[1]//(blocksize**2), 
        blocksize, 
        1,
        blocksize, 3).swapaxes(1, 2)

    # test for skin
    g = 1
    if(format == "bgr"): r = 2
    if (format == "rgb"): r = 0

    rg = blocks2[:,:,:,:,r] - blocks2[:,:,:,:,g] 
    inx = np.greater(rg, low) & np.less(rg, high)

    # find blocksize indexes where skin exists
    average_indexes = np.any(np.any(np.any(inx, axis=1), axis=1), axis=1)
    average_indexes = np.where(average_indexes)[0]

    # is this faster?
    for averages in average_indexes:
        blocks2[averages, :, :, :, 0] = np.average(blocks2[averages, :, :, :, 0])
        blocks2[averages, :, :, :, 1] = np.average(blocks2[averages, :, :, :, 1])
        blocks2[averages, :, :, :, 2] = np.average(blocks2[averages, :, :, :, 2])

    # converty back, 
    # double `reshape` above destroys pointer, otherwise this would be unncessary
    outim = blocks2.swapaxes(2,1).reshape(blocks.shape)
    outim = outim.swapaxes(2,1).reshape(im.shape)
    return outim

"""
The functions below are for reference.
'skincal' (above) uses the same steps BUT
these functions operate on copies, not refrences :(
"""
def toXY(im, blocksize):
    """ Convert to array of [x, y, blocksize, blocksize, 3]
        i.e. a coordinate system that allows for an X/Y indexing
        with blocks.

        NOTE: the returned array is a view (pointer) of the original
        'im' array, so manipulation of the returned array will
        affect the original array
    """
    blocks = img.reshape(
        img.shape[0]//blocksize, 
        blocksize, 
        img.shape[1]//blocksize, 
        blocksize, 3).swapaxes(1, 2)
    return blocks

def toBlocks(im, blocksize):
    """ Converts to array of [x*y, blocksize, blocksize, 3]
        which allows for a single inices to move through blocks of
        the input image

        NOTE: Unfortunatelly, for some reason, the double
        reshape makes the return array NOT a POINTER to the 
        original data.

        SO, the fromBlocks() function returns the original image 
    """
    blocks = im.reshape(
        im.shape[0]//blocksize, 
        blocksize, 
        im.shape[1]//blocksize, 
        blocksize, 3).swapaxes(1, 2)


    blocks = blocks.reshape(
        im.shape[0]*im.shape[1]//(blocksize**2), 
        blocksize, 
        1,
        blocksize, 3).swapaxes(1, 2)

    return blocks

def fromBlocks(blocks, im):
    outimg = blocks.swapaxes(2,1).reshape(blocks.shape)
    outimg = outimg.swapaxes(2,1).reshape(im.shape)
    return outimg


if __name__ == '__main__':
    """
        Getting close to a solution for this
    """
    from PIL import Image

    img = np.copy(np.asarray(Image.open("/Users/sabjorn/Dropbox/Camera Uploads/2016-11-09 12.37.45.jpg"))[512:2048, 512:2048, :])

    blocksize = 32
    # makes an [x,y] accessor of blocksize x blocksize blocks
    blocks = img.reshape(
        img.shape[0]//blocksize, 
        blocksize, 
        img.shape[1]//blocksize, 
        blocksize, 3).swapaxes(1, 2)

    blocks2 = blocks.reshape(
        img.shape[0]*img.shape[1]//(blocksize**2), 
        blocksize, 
        1,
        blocksize, 3).swapaxes(1, 2)

    blocks2[img.shape[0]//blocksize*2, :,:,:,:] = 0

    low = 150
    high = 25

    rg = blocks2[:,:,:,:,0] - blocks2[:,:,:,:,1] 
    inx = np.greater(rg, 25) & np.less(rg, 200)

    average_indexes = np.any(np.any(np.any(inx, axis=1), axis=1), axis=1)
    average_indexes = np.where(average_indexes)[0]

    # is this faster?
    for averages in average_indexes:
        blocks2[averages, :, :, :, 0] = np.average(blocks2[averages, :, :, :, 0])
        blocks2[averages, :, :, :, 1] = np.average(blocks2[averages, :, :, :, 1])
        blocks2[averages, :, :, :, 2] = np.average(blocks2[averages, :, :, :, 2])

    outimg = blocks2.swapaxes(2,1).reshape(blocks.shape)
    outimg = outimg.swapaxes(2,1).reshape(img.shape)

    (Image.fromarray(outimg)).show()