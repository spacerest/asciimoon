#https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_histograms/py_histogram_begins/py_histogram_begins.html

import cv2
import numpy as np
import matplotlib.pyplot as plt


img = np.full((500, 500, 3), 255, dtype = np.uint8) 
plt.hist(img.ravel(),256,[0,256])
plt.show()
