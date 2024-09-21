import matplotlib.pyplot as plt
import pandas as pd
from kinematic.joints_to_kinematics_data import JointsToKinematicsData



def plot_joint_data(joint_data, joint_id):
    """
    Plots position, velocity, and acceleration for a given joint.

    Args:
        joint_data: A JointKinematics object.
        joint_id: The ID of the joint.
    """

    plt.figure(figsize=(12, 8))

    # Plot position
    plt.subplot(3, 1, 1)
    plt.plot(joint_data.t, joint_data.x_position, label='Posición X')
    plt.plot(joint_data.t, joint_data.y_position, label='Posición Y')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Posición (m)')
    plt.title(f'Posición de la articulación {joint_id}')
    plt.legend()

    # Plot velocity
    plt.subplot(3, 1, 2)
    plt.plot(joint_data.t, joint_data.x_velocity, label='Velocidad X')
    plt.plot(joint_data.t, joint_data.y_velocity, label='Velocidad Y')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Velocidad (m/s)')
    plt.title(f'Velocidad de la articulación {joint_id}')
    plt.legend()

    # Plot acceleration
    plt.subplot(3, 1, 3)
    plt.plot(joint_data.t, joint_data.x_accel, label='Aceleración X')
    plt.plot(joint_data.t, joint_data.y_accel, label='Aceleración Y')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Aceleración (m/s^2)')
    plt.title(f'Aceleración de la articulación {joint_id}')
    plt.legend()

    plt.tight_layout()
    plt.show()

# Carga tus datos
PATH = './resources/joints_per_second.csv'
df = pd.read_csv(PATH)

# Crea un objeto JointsToKinematicsData
joints_data = JointsToKinematicsData(df)

# Lista de articulaciones de interés
articulaciones = [11, 12, 15, 16, 23, 27, 28]

# Itera sobre cada articulación y grafica los datos
for articulacion in articulaciones:
    joint_data = joints_data.get_joint(articulacion)
    plot_joint_data(joint_data, articulacion)