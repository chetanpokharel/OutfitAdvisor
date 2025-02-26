# utils.py
import csv
import os

# Define the base directory path as specified
BASE_DIR = r"C:\Users\chetan pokharel\Desktop\shop\shop"  # Raw string to handle backslashes correctly

def load_product_details(file_name):
    product_details = {}
    # Concatenate the base directory with the file name
    file_path = os.path.join(BASE_DIR, file_name)  # This will create the full path to styles.csv

    # Open the CSV file
    try:
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)  # Read the CSV as a dictionary
            for row in reader:
                image_filename = row['id'] + '.jpg'  # Assuming 'id' column exists
                product_details[image_filename] = {
                    'id': row['id'],
                    'name': row['productDisplayName'],
                    'category': row['masterCategory'],
                    'subCategory': row['subCategory'],
                    'articleType': row['articleType'],
                    'baseColour': row['baseColour'],
                    'season': row['season'],
                    'year': row['year'],
                    'usage': row['usage']
                }
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    
    return product_details
