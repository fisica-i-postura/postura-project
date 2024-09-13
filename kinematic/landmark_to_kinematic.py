from sample_pandas_data import df
from kinematic_equations import velocity, acceleration
import numpy as np
import matplotlib.pyplot as plt

def resultant(x, y):
    return np.sqrt(np.square(x) + np.square(y))

def direction(x, y):
    return np.arctan(x, y)

t = df["t"].to_numpy()
x = df["x"].to_numpy()
y = df["y"].to_numpy()

vx = velocity(x, t)
vy = velocity(y, t)
v = resultant(vx, vy)
v_direction = direction(vx, vy)

ax = acceleration(vx, t)
ay = acceleration(vy, t)
a = resultant(ax, ay)
a_direction = direction(ax, ay)

print(t)
print(x)
print(y)
print(vx)
print(vy)
print(v)
print(ax)
print(ay)
print(a)

plt.plot(t, vx, "red")
plt.plot(t, vy, "yellow")
# plt.plot(t, v, "o")
plt.show()