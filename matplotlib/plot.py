import matplotlib.pyplot as plt
import numpy as np
#%matplotlib inline

#  generate an array of evenly spaced numbers over a specified range.
x = np.linspace(0, 10, 100)
print("x=\n", x)

# generate sin of those values
y = np.sin(x)
print("y=\n",y)

# Create a plot
plt.plot(x, y, label="Sine Wave")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.title("Simple Sine Wave Plot")
plt.legend()
plt.show()