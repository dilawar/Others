
from PIL import Image
import os

#to loop all the images in the current dir
for f in os.listdir('.'):
         if f.endswith('.png'):
             try:
                i=Image.open(f)
             except Exception as e:
                print( '[WARN] Could not open %s' % f )
                continue
                    
             fn,fext = os.path.splitext(f)
             print('[INFO] Processing %s' % f )
             #i = Image.open(fn)
             
             #to crop the required size; it crops from the middle 
             half_the_width = i.size[0] /2

             half_the_height = i.size[1] /2

             c = i.crop(  
                            (
                                half_the_width - 550,
                                half_the_height - 270,
                                half_the_width + 550,
                                half_the_height + 480,
                                )
                         )
         
             
             c.save('cropped/{}_crop{}'.format(fn,fext))
             #save all the images tot he cropped folder with _crop.same file ext
