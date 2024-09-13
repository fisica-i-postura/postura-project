import pandas as pd

# Defining the sequences
x = [1, 2, 3, 4, 5, 6, 7, 8, 9]
y = [1, 4, 9, 16, 25, 16, 9, 4, 1]
t = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Creating the dataframe
df = pd.DataFrame({
    't': t,
    'x': x,
    'y': y
})

print(df.to_csv())

print(df["t"])