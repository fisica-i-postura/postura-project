import pandas as pd

# Defining the sequences
x = [1, 2, 3, 4, 5, 6, 7, 8, 9]
y = [1, 4, 9, 16, 25, 36, 49, 64, 81]
t = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4]

# Creating the dataframe
df = pd.DataFrame({
    't': t,
    'x': x,
    'y': y
})