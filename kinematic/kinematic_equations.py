from sample_pandas_data import df
import matplotlib.pyplot as plt

print(df.to_csv())

def variation(num, den):
    assert len(num) == len(den)
    var = [0] * len(num)
    for i in range(len(num)-1):
        delta_num = num[i+1] - num[i]
        delta_den = den[i+1] - den[i]
        var[i+1] = delta_num / delta_den
    return var

def velocity(positions, time):
    return variation(positions, time)

def acceleration(velocity, time):
    return variation(velocity, time)

t = df["t"].to_numpy()
y = df["y"].to_numpy()

v = velocity(y, t)
a = acceleration(v, t)

print(t)
print(y)
print(v)
print(a)

plt.plot(t, y)
plt.plot(t, v)
plt.plot(t, a)
plt.show()

def landmark_to_kinematic(landmark_df):
    """TODO"""