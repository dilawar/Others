
import os



import numpy as np
import Image



#to loop all the images in the current dir
for f in os.listdir('.'):
         if f.endswith('.png'):
            im = Image.open(f)
             #it can split the image name and the ext so you can call required
            fn,fext = os.path.splitext(f)
            data = np.array(im)
            r1, g1, b1 = 0, 0, 0 # Original value
            r2, g2, b2 = 255, 255, 255 
            #Value that we want to replace it with

            red, green, blue = data[:,:,0], data[:,:,1], data[:,:,2]
            mask = (red == r1) & (green == g1) & (blue == b1)
            data[:,:,:3][mask] = [r2, g2, b2]

            im = Image.fromarray(data)
            #im.save('fig1_modified.png')
            im.save('changegray/{}_white{}'.format(fn,fext))
