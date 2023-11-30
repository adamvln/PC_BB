import pandas as pd

def merge_excel_csv(base_excel_path, new_csv_path, output_file_path, filter_value='Oost'):
    # Load the existing base Excel file into a DataFrame
    base_df = pd.read_excel(base_excel_path)
    
    # Load the new CSV file into a DataFrame
    new_df = pd.read_csv(new_csv_path, delimiter=';', encoding='latin1', header=0) 
    
    # Filter rows where the first column matches the filter_value (e.g., 'Oost')
    filtered_new_df = new_df[new_df.iloc[:, 0] == filter_value]
    
    # Select only the columns of interest from the filtered DataFrame
    # Update the indices to match the CSV structure if necessary
    columns_of_interest = ['Grond X', 'Grond Y', 'Grond Z', 'Top X', 'Top Y', 'Top Z', 'Hoogte', 'Hoek', 'Identifier']
    selected_new_df = filtered_new_df[columns_of_interest]
    
    # Generate new ID numbers for the new rows
    last_id = base_df['Id'].max() if not base_df['Id'].empty else 0
    new_ids = range(last_id + 1, last_id + 1 + len(selected_new_df))
    selected_new_df.insert(0, 'Id', new_ids)
    
    # Append the selected new data to the base DataFrame
    merged_df = pd.concat([base_df, selected_new_df], ignore_index=True)
    
    # Save the merged DataFrame to a new Excel file
    merged_df.to_excel(output_file_path, index=False)

# Usage
base_excel_path = 'dataset/sheets/coordinates_poles.xlsx'  # The base Excel file
new_csv_path = 'Oost_matches.csv'          # The new CSV file with additional matches
output_file_path = 'dataset/sheets/fused_coordinates_poles.xlsx'  # The output file after merging

# # Call the function
# merge_excel_csv(base_excel_path, new_csv_path, output_file_path)

# def clean_coordinates_data(file_path):
#     # Load the Excel file into a DataFrame
#     df = pd.read_excel(file_path)

#     # Drop rows where any of the required coordinates are missing
#     required_columns = ['Grond X', 'Grond Y', 'Grond Z', 'Top X', 'Top Y', 'Top Z']
#     df_cleaned = df.dropna(subset=required_columns)

#     # Save the cleaned DataFrame back to the Excel file
#     df_cleaned.to_excel(file_path, index=False)

# # Replace 'path_to_your_file' with the actual path to the 'fused_coordinates_poles.xlsx' file on your machine
# clean_coordinates_data('fused_coordinates_poles.xlsx')

# import pandas as pd

# def convert_coordinates_to_numbers(file_path):
#     # Load the Excel file into a DataFrame
#     df = pd.read_excel(file_path)

#     # Columns to convert to numeric
#     columns_to_convert = ['Grond X', 'Grond Y', 'Grond Z', 'Top X', 'Top Y', 'Top Z']

#     # Convert the specified columns to numeric
#     df[columns_to_convert] = df[columns_to_convert].apply(pd.to_numeric, errors='coerce')

#     # Save the DataFrame back to the Excel file
#     df.to_excel(file_path, index=False)

# # Replace 'path_to_your_file' with the actual path to the cleaned Excel file
# convert_coordinates_to_numbers('dataset/sheets/fused_coordinates_poles.xlsx')
