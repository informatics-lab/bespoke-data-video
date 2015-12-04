import sys
import argparse as ap
import subprocess as sp
import os
import glob

import iris

sys.path.append(".")
import imageproc

def proc_cube(cube):
    for i, frt_cube in enumerate(cube.slices_over("time")):
        print "Processing timestep ", i, "...",
        img_array = imageproc.tileArray(frt_cube.data)
        img_array /= img_array.max()
        img_array *= 255
        print "Writing image"
        with open("data%03d.png" % i, "wb") as img:
            imageproc.writePng(img_array, img, nchannels=3, alpha=False)
    
    print "Writing video"
    sp.call(["avconv", "-y",
            "-r", "1", "-i", "data%03d.png",
            "-r", "1", "-vcodec", os.getenv("CODEC", "libtheora"), "-qscale:v", os.getenv("QUALITY", 2), os.getenv("FILE_OUT", "out.ogv")])
    print "Cleaning up"
    fs = glob.glob("./data???.png")
    for f in fs:
        os.remove(f)
        
if __name__=="__main__":
    varname = os.getenv("VAR_NAME")
    if varname != None:
        cube = iris.load_cube(os.getenv("FILE_IN"), iris.Constraint(varname))
    else:
        cube = iris.load_cube(os.getenv("FILE_IN"))
    proc_cube(cube)
