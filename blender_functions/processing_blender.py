# import bpy
import pandas as pd
import re 
import os 
import bpy

def create_blend_file(dae_file):
    """
    Creates a new Blender .blend file with no objects and returns the path to it.

    :param dae_file: The name of the DAE file (e.g., 'Collada-RD-122500_485500.dae').
    :return: The path to the generated .blend file.
    """
    # Extract x1 and x2 from the DAE file name
    x1, x2 = extract_numbers_from_string(dae_file)

    # Create a new scene
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    # Save the blend file with the specified name
    blend_file_name = f"dataset/blend_files/blend_{x1}_{x2}.blend"
    blend_file_path = os.path.abspath(blend_file_name)
    bpy.ops.wm.save_as_mainfile(filepath=blend_file_path)

    return blend_file_path

def import_object(dae_file, blend_file):
    # Open the specified .blend file
    bpy.ops.wm.open_mainfile(filepath=blend_file)

    # Clear existing objects (optional)
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Import the .dae file
    bpy.ops.wm.collada_import(filepath=dae_file)

    print("Imported:", dae_file)

    # Save the changes to the .blend file
    bpy.ops.wm.save_mainfile()

def add_lights(df, blend_file_path):
    """
    Opens a specific .blend file, adds point lights and a sun light to the scene based on the provided
    DataFrame, and saves the file.

    :param df: DataFrame containing 'Grond X' and 'Grond Y' columns for point light positions.
    :param blend_file_path: The file path of the .blend file to operate on.
    """
    # Open the specified .blend file
    bpy.ops.wm.open_mainfile(filepath=blend_file_path)

    # Loop through the DataFrame rows and add point lights
    for index, row in df.iterrows():
        # Create a new point light datablock
        light_data = bpy.data.lights.new(name=f"PointLight_{index}", type='POINT')

        # Set the point light power (energy) to 1000 watts
        light_data.energy = 1000

        # Create a new object with the point light data
        light_object = bpy.data.objects.new(name=f"PointLight_{index}", object_data=light_data)

        # Set point light location
        light_object.location = (row['Grond X'], row['Grond Y'], 6)  # Z coordinate is 6

        # Link point light object to the current collection
        bpy.context.collection.objects.link(light_object)

    # Add a sun light
    sun_data = bpy.data.lights.new(name="SunLight", type='SUN')
    sun_data.energy = 0.100  # Strength of the sun light
    sun_object = bpy.data.objects.new(name="SunLight", object_data=sun_data)
    sun_object.location = (50, 50, 50)  # Sun light coordinates
    bpy.context.collection.objects.link(sun_object)

    # Save the .blend file after adding the lights
    bpy.ops.wm.save_mainfile()

def extract_coordinate_pairs(df, x1, x2):
    """
    Extracts all pairs of coordinates where Ground X is between X1 and X1 + 100,
    and Ground Y is between X2 and X2 + 100.

    :param df: Pandas DataFrame containing the coordinate data.
    :param x1: The starting value for Ground X range.
    :param x2: The starting value for Ground Y range.
    :return: A DataFrame with the filtered coordinate pairs.
    """
    # Filter the dataframe based on the conditions
    filtered_df = df[
        (df['Grond X'] >= x1) & (df['Grond X'] <= x1 + 100) &
        (df['Grond Y'] >= x2) & (df['Grond Y'] <= x2 + 100)
    ]
    
    # Subtract x1 from 'Grond X' and x2 from 'Grond Y'
    filtered_df['Grond X'] = filtered_df['Grond X'] - x1
    filtered_df['Grond Y'] = filtered_df['Grond Y'] - x2

    # Return only the 'Ground X' and 'Ground Y' columns
    return filtered_df[['Grond X', 'Grond Y']]

def extract_numbers_from_string(s):
    """
    Extract two numbers from a string.
    
    :param s: The string containing the numbers.
    :return: A tuple containing the two numbers (x1, x2).
    """
    # Find all numbers in the string
    numbers = re.findall(r'\d+', s)
    
    # Convert extracted strings to integers and return as a tuple
    return tuple(map(int, numbers[:2])) if len(numbers) >= 2 else None


def preprocessing_dae(dae_file_path):
    """
    Preprocesses a DAE file by changing the encoding declaration from UTF-16 to UTF-8.

    :param dae_file_path: The path to the DAE file.
    """
    # Read the content of the DAE file
    with open(dae_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Replace the encoding declaration with UTF-8
    content = content.replace('encoding="utf-16"', 'encoding="utf-8"')

    # Write the modified content back to the DAE file
    with open(dae_file_path, 'w', encoding='utf-8') as file:
        file.write(content)

if __name__ == "__main__":
    folder_path = 'dataset/dae'  # Replace with the path to your folder

    # Iterate over the files in the folder
    for filename in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, filename)):
            dae_file = os.path.join(folder_path, filename)  
            preprocessing_dae(dae_file)
            x1, x2 = extract_numbers_from_string(dae_file)
            blend_file = create_blend_file(dae_file)
            import_object(dae_file, blend_file)

            xlsx_file = 'dataset/sheets/fused_coordinates_poles.xlsx'
            df = pd.read_excel(xlsx_file)
            filtered_df = extract_coordinate_pairs(df, x1, x2)

            add_lights(filtered_df, blend_file)

