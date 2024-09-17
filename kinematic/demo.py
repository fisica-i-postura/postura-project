import pandas as pd
from joints_to_kinematics_data import JointsToKinematicsData
from joint_kinematics import JointKinematics
import matplotlib.pyplot as plt

"""TODO: extract to main file when integrating changes"""

PATH = './resources/joints_per_second.csv'
df = pd.read_csv(PATH)
joints_data = JointsToKinematicsData(df)
print(joints_data.__str__())

joint_kinematics: JointKinematics = joints_data.get_joint(11)

def plot(domain, rough_image, smooth_image):
    plt.figure()
    plt.plot(domain, rough_image, "-")
    plt.plot(domain, smooth_image, "--")
    plt.show()

plot(joint_kinematics.t, joint_kinematics.x_position, joint_kinematics.x_position_smooth)
plot(joint_kinematics.t, joint_kinematics.y_position, joint_kinematics.y_position_smooth)
plot(joint_kinematics.t, joint_kinematics.x_velocity, joint_kinematics.x_velocity_smooth)
plot(joint_kinematics.t, joint_kinematics.y_velocity, joint_kinematics.y_velocity_smooth)