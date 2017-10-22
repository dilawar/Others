
import numpy as np
import os

import cv2



for f in os.listdir('.'):
         if f.endswith('.png'):
            image = cv2.imread(f)
            
            print( 'Processing image file %s' % image )
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (3, 3), 0)
            tight = cv2.Canny(blurred, 525, 550)
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
            ctight = cv2.morphologyEx(tight, cv2.MORPH_CLOSE, kernel)
            outfile = 'contour/%s_c.png' % f
            cv2.imwrite( outfile, np.hstack( [ ctight]) )
            
            