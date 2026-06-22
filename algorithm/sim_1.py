import numpy as np
import matplotlib.pyplot as plt

tSim = 10.0
fS = 10e3
nPts = round(tSim * fS)

# Time vector
t = np.arange(nPts) / fS

# Distance
d = 1 - np.cos(2 * np.pi * 1.1 * t) + 10 * t

# Speed (derivative of d)
v = 2 * np.pi * 1.1 * np.sin(2 * np.pi * 1.1 * t) + 10

# Plot
plt.plot(t, d, label='distance')
plt.plot(t, v, label='speed')
plt.xlabel('time')
plt.ylabel('distance')
plt.legend()
plt.title('reference speed profile')
plt.grid(True)
plt.show()