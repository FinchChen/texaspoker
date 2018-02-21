import numpy as np

num=1000000
lst = np.random.randint(num / 100000, size=num)

print dict(zip(*np.unique(lst, return_counts=True)))
