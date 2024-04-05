import pandas as pd

# Load the Excel file into a DataFrame
df = pd.read_excel('schools.xlsx')

# List of airports
airports = ['Heathrow Airport', 'Gatwick Airport', 'Stansted Airport', 'Manchester Airport', 'Bristol Airport', 'Edinburgh Airport', 'Birmingham Airport']

# Convert distance columns to numeric values (removing " miles" from the end)
for airport in airports:
    df[f'Distance to {airport}'] = df[f'Distance to {airport}'].str.replace(' km', '').str.replace(',', '').astype(float)

# Filter the DataFrame
df = df[df.apply(lambda row: any(row[f'Distance to {airport}'] <= 50 for airport in airports), axis=1)]

# Remove semicolons from the "Number of pupils" column
df['Number of pupils'] = df['Number of pupils'].str.replace(';', '').astype(int)

# Write the filtered DataFrame back to the spreadsheet
df.to_excel('filtered_schools.xlsx', index=False)

print('Schools close to airports filtered and saved to new spreadsheet.')