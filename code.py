import numpy as np
from numpy.linalg import inv
#numpy.random.randint(low, high = None, size = None, dtype = '|')
A = np.random.randint(10, size=(2,2))

for row in A :
  print(row)

E = A.transpose()

for row in E :
  print(row)

ainv = inv(A)

for row in ainv :
  print(row)

import matplotlib.pyplot as plt
import numpy as np

s = np.random.randint(10, size=1000)
t = np.arange(0.0, 10.0, 0.01)
s = np.sin(2*np.pi*t)
c = np.cos(2*np.pi*t)
plt.plot(t, s)
plt.plot(t, c)
plt.show()

from numpy.random import normal,rand
x = np.random.randint(1,101,size = 100)
plt.hist(x,bins=20)
plt.show()
plt.cla()

from numpy.random import normal,rand

a = np.random.randint(0.0,101.0,size = 1000)
b = np.random.randint(0.0,101.0,size = 1000)
plt.scatter(a,b)
plt.show()
