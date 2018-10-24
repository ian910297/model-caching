#!/usr/bin/env python3
""" Example copy from https://www.w3cschool.cn/doc_numpy_1_12/numpy_1_12-generated-numpy-random-randomstate-zipf.html#id1 """
import numpy as np
import matplotlib.pyplot as plt
from scipy import special

""" Generate zipf distribution(zeta distribution) """
""" parameter """
a = 2.
s = np.random.zipf(a, 1000)


""" Display """
""" Draw a histogram """
""" 'normed' kwargs is depreacted, and has been replace by the 'density' """
""" Display value less than 50 """
""" plt.hist([data array], [bins], kargs... ) """
""" bins means integer or sequence or string, optimal """
"""  """
#count, bins, ignored = plt.hist(s[s<50], [10, 20, 30, 40, 50], density=True)
count, bins, ignored = plt.hist(s[s<50], 50, density=True)
print(count, bins, ignored)

""" Draw a curve """
""" Generate a array contains number 1 to number 50 """
x = np.arange(1., 50.)

""" The probability density for the zipf distribution """
y = x**(-a) / special.zetac(a)
plt.plot(x, y/max(y), linewidth=2, color='r')

plt.show()