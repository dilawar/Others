

import numpy as np
import os

import cv2



for f in os.listdir('.'):
         if f.endswith('.png'):
            image = cv2.imread(f,1)
            
            print( 'Processing image file %s' % image )




            # define the list of boundaries
            boundaries = [([0,0,0],[50,50,50])]


            # loop over the boundaries

            for (lower, upper)in boundaries:
                # create NumPy arrays from the boundaries
                lower = np.array(lower, dtype = "uint8")
                upper = np.array(upper, dtype = "uint8")
                
                
            # find the colors within the specified boundaries and apply the mask
                
                mask = cv2.inRange(image, lower, upper)
                
                output = cv2.bitwise_and(image, image, mask = mask)
                
                
                        
            
            
          
            
                outfile = 'gaps/%s_out.png' % f
                cv2.imwrite( outfile, np.hstack( [ output]) )
                print( '\tOutput written to %s' % outfile )
                
