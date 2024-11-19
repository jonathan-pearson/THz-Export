import os
import csv
import pandas as pd
import numpy as np

# This program will perform all the tasks needed to turn .t2t files 
# from the THz machine into a .csv file for a pandas dataframe
# For more information see the vizualize_data.ipynb file
# Just write folder_path as the path to the folder containing the data

class dataset():
    def __init__(self, folder_path):
        self.data = []
        self.files = []
        # Call the methods below
        self.get_filepaths(folder_path)
        self.t2t_to_df()

    # This method will find all .t2t files in any subfolder of the folder_path.
    # Files containing the string "error" will be ignored.
    def get_filepaths(self, folder_path):
        # Checks subfolders of a path
        for root, dirs, files in os.walk(folder_path):
            # Ignores files containing the string "error"
            if "error" in root:
                continue
            for file in files:
                # Find .t2t files
                if file.endswith(".t2t"):
                    # Print and append the file path to the files list
                    print("Located ", os.path.join(root, file).replace("\\", "\\\\"))
                    self.files.append(os.path.join(root, file).replace("\\", "\\\\"))

    # This method will process the .t2t files and convert them to .csv files.
    def t2t_to_df(self):
        for file_path in self.files:
            with open(file_path, "r") as file:
                content = file.read()
                lines = content.strip().split("\n")
                #print(lines[0], file_path)
                # Remove the first few lines which are not data
                del lines[0:4]
                # Split each string by commas to create a list of lists
                list_of_lists = [s.split(',') for s in lines]
                # Convert the list of lists into a NumPy array
                numpy_array = np.array(list_of_lists, dtype=np.float32)
                # Create a dataframe from the NumPy array
                df = pd.DataFrame(numpy_array)

                # Extract Sample and Scan from the file path
                # Expected input looks like : 
                # folder_path\\sXX-X\\sXX-X\\_TC2340ms_resX100um_resY100um.t2t
                # or
                # folder_path\\sXX_X\\_TC2340ms_resX100um_resY100um.t2t
                
                # Made robust for inconsistent naming conventions
                path = file_path.split("\\")[-3]

                if "-" in path:
                    scan = path.split("-")[1]
                    sample = path.split("-")[0]
                elif "_" in path:
                    scan = path.split("_")[1]
                    sample = path.split("_")[0]
                sample = sample[1:]

                #print(scan)
                #print(sample)

                # Add the columns to the dataframe
                df.insert(0, 'Sample', sample)
                df.insert(1, 'Scan', scan)
                df.insert(2, 'Location', range(1, len(df) + 1))
                df.insert(3, 'AC', 0)

                # Rename the columns after 'AC' to 'X', 'Y', 'Z', and then start counting from 1
                df.columns = list(df.columns[:4]) + ['X', 'Y', 'Z'] + list(range(1, len(df.columns) - 6))

                # Append the dataframe to the data list
                self.data.append(df)
        #Concatenate all the dataframes together and turn the data list into one dataframe (this makes a really big dataframe)
        self.data = pd.concat(self.data, ignore_index = True)
    
    #This member function will save the dataframe to a csv file when called
    def df_to_csv(self):
        self.data.to_csv("output.csv", index=False)          

def main():
    # Define the folder path (we can put a GUI here later)
    folder_path = "Sample_Data"
    # Create an instance of the dataset class
    data = dataset(folder_path)
    # Save the dataframe to a csv file
    data.df_to_csv()
    print("Data saved to output.csv")
    input("Press Enter to exit...")

main()