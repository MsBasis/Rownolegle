import numpy as np
# two dimensional arrays
m1 = np.random.randint(10, size=(10, 10))
m2 = np.random.randint(10, size=(10, 10))
m3 = np.dot(m1,m2) 
print(m3)