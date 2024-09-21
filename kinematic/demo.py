import pandas as pd
from joints_to_kinematics_data import JointsToKinematicsData

"""TODO: extract to main file when integrating changes"""

PATH = '../resources/joints_per_second.csv'
df = pd.read_csv(PATH)
print(JointsToKinematicsData(df).__str__())