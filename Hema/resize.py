from PIL import Image
import os
import sys

size_500 = (500,500)

#to loop all the images in the current dir
infile, outfile = sys.argv[1:3]
i=Image.open( infile )
i.thumbnail(size_500)
i.save( outfile )
