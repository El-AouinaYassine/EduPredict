import matplotlib.pyplot as plt
import pandas as pd
df = pd.read_csv('processed_student_data.csv')
x = df['Sexe']

# Show the plot
plt.plot(x)
plt.show()