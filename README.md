# PC_BB: Pole Detection in Point Clouds
Welcome to the PC_BB repository! This project is part of an internship with the City of Amsterdam, with a primary goal of modelling light illumination in a 3D model of Amsterdam!

## Getting Started with Python and Blender API

### Installation of Blender Software
1. **Download Blender**: Visit [Blender's official website](https://www.blender.org/) and download Blender 4.0.

### Configuring Blender in System Path
2. **Set Blender as a PATH variable**:
   - Navigate to the Blender Foundation folder, typically located in "Program Files" or your chosen installation directory.
   - Find the `blender.exe` executable, usually found at a path similar to `C://...//Blender Foundation\Blender 4.0`.
   - Add this path to your system's PATH environment variable for easy access.

### Collada File Preparation
3. **Download Collada Cube**:
   - Visit [3D Amsterdam](https://3d.amsterdam.nl/) and download a Collada cube.
   - Move the downloaded cube into the `dataset/dae` folder in your project directory.

### Installing Pandas in Blender
4. **Integrate Pandas with Blender**:
   - Launch Blender and navigate to the Scripting menu.
   - Run the following script in the Python Console:
     ```python
     import sys
     print(sys.executable)
     ```
   - Open a command prompt or terminal.
   - Use the Blender Python executable path obtained from the previous step to install Pandas:
     ```bash
     "C:\path\to\blender\python.exe" -m ensurepip
     "C:\path\to\blender\python.exe" -m pip install pandas
     "C:\path\to\blender\python.exe" -m pip install openpyxl
     ```

### Running the Processing Script
5. **Execute Processing Script**:
   - Now you can run the `blender_functions/processing_blender.py` script.
   - Open a command prompt and run : 
     ```bash
     blender --background --python blender_functions/processing_blender.py
     ```
   - Ensure all dependencies and paths are correctly set for a smooth execution.

## Acknowledgements
Special thanks to the City of Amsterdam for their support and collaboration in this internship project.
