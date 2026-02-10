import pandas as pd

# Replace 'your_file.csv' with the actual name of your file
df = pd.read_csv(r'C:\Users\mitta\Desktop\old\hosp\labevents.csv\labevents.csv')

# Filter the DataFrame for the specific hadm_id
filtered_rows = df[df['hadm_id'] == 22841357]

# Display the result
print(filtered_rows)