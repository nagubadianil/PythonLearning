import numpy as np

a_in = np.array([1, 2, 3])
a = np.array(a_in, copy=False)
print(a)
a[0] = 0
print(a)
print(a_in)

a = np.array([1.3738729019013636723763], dtype=np.float16)[0]
print("float16:", a)

a = np.array([1.3738729019013636723763], dtype=np.float32)[0]
print("float32:", a)

a = np.array([1.3738729019013636723763], dtype=np.float64)[0]
print("float64:", a)

a = np.array([0.0, 2.0, 3.0, 4.0, 5.0])
# Get elements at position 0 and 2
print(a[[0, 2]])
# [0., 3.]
# Change the first two elements
a[[0, 1]] = [0, 3.0]
print(a)
# [0., 3., 3., 4., 5.]

a = np.array([1.0, 2.0])
a = np.append(a, [4.0, 5.0])
print(a)

a = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
# Insert one element at position 3
a = np.insert(a, 3, values=3.5)
# a is now [1. , 2. , 3. , 3.5, 4. , 5. ]
# Insert a list of elements at position 3
a = np.insert(a, 3, values=[100, 200])
# a is now [1. , 2. , 3. , 3.5, 100, 200, 4. , 5. ]
# Insert multiple elements at multiple positions
a = np.insert(a, [3, 5], values=[4.5, 5.5])
# a is nop [1. , 2. , 3. , 4.5, 4. , 5. , 5.5]

# Sorting- return copy
a = np.array([1.0, 3.0, 2.0, 4.0, 5.0])
b = np.sort(a)

# In place sorting
a = np.array([1.0, 3.0, 2.0, 4.0, 5.0])
a.sort()