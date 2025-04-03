import os
import pandas as pd

# Load the CSV file
csv_file = r"C:\\Users\\pc\\Desktop\\faceattendencemodel\\data\\raw\\Data Collection Form (Responses) - Form Responses 1.csv"
df = pd.read_csv(csv_file)  # Use read_csv for CSV files

# Define the image folder path
image_folder = r"C:\\Users\\pc\\Desktop\\faceattendencemodel\\data\\raw\\Upload Image(passport size) (File responses)"

# Loop through each row and rename files
for index, row in df.iterrows():
    old_name = str(row[2]).strip()  # Convert to string and strip spaces (if any)
    new_name = str(row[3]).strip()  # Convert to string and strip spaces

    old_path = os.path.join(image_folder, old_name)
    new_path = os.path.join(image_folder, f"{new_name}.jpg")

    if os.path.exists(old_path):
        os.rename(old_path, new_path)
        print(f"Renamed: {old_name} → {new_name}.jpg")
    else:
        print(f"File not found: {old_name}")

print("Renaming complete!")
