import numpy as np

def variation(num, den):
    assert len(num) == len(den)
    var = np.zeros(len(num))
    for i in range(len(num)-1):
        delta_num = num[i+1] - num[i]
        delta_den = den[i+1] - den[i]
        if delta_den == 0:
            continue
        var[i+1] = delta_num / delta_den
    return var

def velocity(positions, time):
    return variation(positions, time)

def acceleration(velocity, time):
    accel = variation(velocity, time)
    accel[0:1] = 0
    return accel