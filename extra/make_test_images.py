import cv2
import numpy as np
import matplotlib.pyplot as plt

x = np.zeros((10, 10, 3))
#x[:, :, 0:3] = np.random.uniform(0, 1, (3,))
#plt.imshow(x)
plt.figure() 

y = np.ones((10, 10, 3))
#y[:,:,0:3] = np.random.uniform(0, 1, (3,))
#plt.imshow(y)

plt.figure()
c = np.linspace(0, 1, 10)[:, None, None]
gradient = x + (y - x) * c
plt.imshow(gradient)
plt.show()