import glob
import matplotlib.pyplot as plt
from pvlib import iotools

# Find all .epw files in the current folder
epw_files = glob.glob("*.epw")

if not epw_files:
    print("No .epw files found! Please check if the files are in the correct folder.")
else:
    print(f"Total {len(epw_files)} file(s) found. Starting processing...\n")

# Loop through each file and read the data
for file_path in epw_files:
    print(f"--- Reading file: {file_path} ---")
    
    # Parse the epw file using pvlib
    data, metadata = iotools.read_epw(file_path)
    
    # Safely extract city and country from metadata dictionary
    city = metadata.get('city', 'Unknown City')
    country = metadata.get('country', 'Unknown Country')
    print(f"Location: {city}, {country}")
    
    # Display the first 5 rows of specific columns
    print("\nFirst few rows of data:")
    print(data[['temp_air', 'relative_humidity', 'wind_speed']].head())
    print("\n" + "="*50 + "\n")
    
    # Sample plot: Visualize air temperature for the first week (168 hours)
    plt.figure(figsize=(10, 4))
    data['temp_air'].iloc[:168].plot(label=f"{city}, {country}")
    plt.title("Air Temperature Comparison (First Week)")
    plt.xlabel("Time")
    plt.ylabel("Temperature (°C)")
    plt.legend()

# Display the generated plots
plt.show()