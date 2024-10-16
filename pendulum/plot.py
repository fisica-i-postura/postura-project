import matplotlib.pyplot as plt
from pendulum.model import Pendulum


def plot_pendulum(pendulum: Pendulum, plot_path='resources/pendulum.png'):
    plt.plot(pendulum.time, pendulum.angle, label='angle')
    plt.xlabel('Time (s)')
    plt.ylabel('Angle (deg)')
    plt.title('Shoulder-Wrist angle vs. time')
    plt.legend()
    plt.savefig(plot_path)
    plt.show()
