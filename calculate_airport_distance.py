import googlemaps
import pandas as pd
from dotenv import load_dotenv
import os

# Load the Google Maps API key from the .env file
load_dotenv()
gmaps_key = os.getenv("GOOGLE_MAPS_API_KEY")

# Initialize the Google Maps client
gmaps = googlemaps.Client(key=gmaps_key)

# Load the spreadsheet
df = pd.read_excel('schools.xlsx')  # or pd.read_csv('spreadsheet.csv')

# Get the 'Address' column
addresses = df['Address']

# List of airports
airports = ['Heathrow Airport', 'Gatwick Airport', 'Stansted Airport', 'Manchester Airport', 'Bristol Airport', 'Edinburgh Airport', 'Birmingham Airport']

# Initialize a dictionary to store the distances
distances = {airport: [] for airport in airports}

# Iterate over the airports
for airport in airports:

    distances[airport] = []

    # Iterate over the addresses
    for address in addresses:
        # Get the distance to the current airport
        distance_result = gmaps.distance_matrix(address, airport)
        # Extract the distance in km
        distance_text = distance_result['rows'][0]['elements'][0]['distance']['text']
        # Remove " km" and convert to float
        distance = float(distance_text.replace(' km', ''))
        # Append the distance to the list for the current airport
        distances[airport].append(distance)
        print(f'Distance to {airport} calculated for {address}.')

    # Save the distances in a new column in the DataFrame
    df[f'Distance to {airport}'] = distances[airport]

    print(f'Distances to {airport} calculated.')

# Write the DataFrame back to the spreadsheet
df.to_excel('schools.xlsx', index=False)  # or df.to_csv('spreadsheet.csv', index=False)

print('Distances calculated and saved to the spreadsheet.')