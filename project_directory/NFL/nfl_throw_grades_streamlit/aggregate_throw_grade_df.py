import os
import pandas as pd
from numbers_parser import Document

# Set the root directory (adjust if it's not in your current working directory)
root_dir = 'throw_grade_data/2024'  # e.g., '/path/to/24' for an absolute path

# List to hold all DataFrames from all files
all_dataframes = []

# Loop through subdirectories 1 to 22
for subdir_num in range(1, 23):
    subdir_path = os.path.join(root_dir, str(subdir_num))
    
    # Check if the subdirectory exists
    if os.path.isdir(subdir_path):
        # Loop through files in the subdirectory
        for filename in os.listdir(subdir_path):
            if filename.endswith('.numbers'):
                file_path = os.path.join(subdir_path, filename)
                print(f"Processing file: {file_path}")
                
                # Load the .numbers file
                try:
                    doc = Document(file_path)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
                    continue
                
                # Loop through all sheets in the document
                for sheet in doc.sheets:
                    # Loop through all tables in the sheet
                    for table in sheet.tables:
                        # Extract data as a list of lists (values only)
                        data = table.rows(values_only=True)
                        
                        # Convert to DataFrame, using first row as headers (skip if no headers)
                        if data and len(data) > 1:  # Ensure there's data and at least one row beyond headers
                            df = pd.DataFrame(data[1:], columns=data[0])
                            # Optionally, add metadata columns to track source
                            df['source_file'] = filename
                            df['sheet_name'] = sheet.name
                            df['table_name'] = table.name
                            all_dataframes.append(df)
                        else:
                            print(f"Skipping empty or header-only table in {file_path}, sheet: {sheet.name}, table: {table.name}")

# Combine all DataFrames into a single DataFrame
if all_dataframes:
    try:
        combined_df = pd.concat(all_dataframes, ignore_index=True)
        print("Combined DataFrame shape:", combined_df.shape)
        print(combined_df.head())
        
        # Optional: Save to CSV
        combined_df.to_csv('combined_output.csv', index=False)
        print("Saved combined DataFrame to 'combined_output.csv'")
    except ValueError as e:
        print(f"Error concatenating DataFrames: {e}")
        print("Check if all tables have compatible column structures.")
else:
    print("No .numbers files found or no data extracted.")


