#!/usr/bin/env python3
"""
Patient Data Cleaner

This script standardizes and filters patient records according to specific rules:

Data Cleaning Rules:
1. Names: Capitalize each word (e.g., "john smith" -> "John Smith")
2. Ages: Convert to integers, set invalid ages to 0
3. Filter: Remove patients under 18 years old
4. Remove any duplicate records

Input JSON format:
    [
        {
            "name": "john smith",
            "age": "32",
            "gender": "male",
            "diagnosis": "hypertension"
        },
        ...
    ]

Output:
- Cleaned list of patient dictionaries
- Each patient should have:
  * Properly capitalized name
  * Integer age (≥ 18)
  * Original gender and diagnosis preserved
- No duplicate records
- Prints cleaned records to console

Example:
    Input: {"name": "john smith", "age": "32", "gender": "male", "diagnosis": "flu"}
    Output: {"name": "John Smith", "age": 32, "gender": "male", "diagnosis": "flu"}

Usage:
    python patient_data_cleaner.py
"""

import json
import os
import pandas as pd # added
import sys # added

def load_patient_data(filepath):
    """
    Load patient data from a JSON file.
    
    Args:
        filepath (str): Path to the JSON file
        
    Returns:
        list: List of patient dictionaries
    """
    # BUG: No error handling for file not found
    # FIX: added a try/except statement to detect if the file can be read
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f'Error: {e}')
        sys.exit(1)
    else:
        with open(filepath, 'r') as file:
            return json.load(file)

def clean_patient_data(patients):
    """
    Clean patient data by:
    - Capitalizing names
    - Converting ages to integers
    - Filtering out patients under 18
    - Removing duplicates
    
    Args:
        patients (list): List of patient dictionaries
        
    Returns:
        list: Cleaned list of patient dictionaries
    """
    # convert to pd.dataframe
    patients = pd.DataFrame(patients)

    # Moved age fillna and drop_duplicates step outside of loop because they can be done in one step as a series
    # BUG: Wrong method name (fill_na vs fillna)
    # FIX: Corrected method name
    # Also converted to integers to prevent future bugs in function
    patients['age'] = patients['age'].fillna(0).astype(int)
    
    # BUG: Wrong method name (drop_duplcates vs drop_duplicates)
    # FIX: Corrected method name
    patients = patients.drop_duplicates()

    for ii in patients.index: # added .index to facilitate looping
        # BUG: Typo in key 'nage' instead of 'name'
        # FIX: Corrected typo, and editted code to properly index names
        patients.loc[ii,'name'] = patients.loc[ii,'name'].title()
        
    # BUG: Wrong comparison operator (= vs ==)
    # BUG: Logic error - keeps patients under 18 instead of filtering them out
    # FIX: Replaced .append method with Pandas method to select only patients with age >= 18
    cleaned_patients = patients[patients['age']>=18].reset_index(drop=True)
    
    # BUG: Missing return statement for empty list
    # FIX: return statement will return an empty list when cleaned_patients is empty
    # otherwise returns cleaned_patients as list of dictionaries
    if cleaned_patients.empty==False:
        return cleaned_patients.to_dict('records')
    else:
        return []

def main():
    """Main function to run the script."""
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the path to the data file
    data_path = os.path.join(script_dir, 'data', 'raw', 'patients.json')
    
    # BUG: No error handling for load_patient_data failure
    # FIX: function will exit script upon load failure
    patients = load_patient_data(data_path)
    
    # Clean the patient data
    cleaned_patients = clean_patient_data(patients)
    
    # BUG: No check if cleaned_patients is None
    # FIX: added if statement to check if cleaned_patients is empty
    if cleaned_patients == None:
        print('No cleaned data')
    else:
        # Print the cleaned patient data
        print("Cleaned Patient Data:")
        # changed loop to .index and .iloc method for Pandas dataframe
        for ii in cleaned_patients:
            # BUG: Using 'name' key but we changed it to 'nage'
            # FIX: No longer an issue due to earlier correction
            print(f"Name: {ii['name']}, Age: {ii['age']}, Diagnosis: {ii['diagnosis']}")
    
    # Return the cleaned data (useful for testing)
    return cleaned_patients

if __name__ == "__main__":
    main()