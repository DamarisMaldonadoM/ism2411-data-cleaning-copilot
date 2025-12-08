#The data cleaning
#The purpose of this script is to clean the raw sales data for analysis
#By putting it in this script to eventually have a new cleaned data file
#Specifically we are renaming in this data set: lowercasing column names, removing leading/trailing spaces, and replacing missing data by filling it with zero

#importing Path from pathlib to handle file paths
#this makes creating the different paths for raw and processed data to transfer the csv files
from pathlib import Path

#imports the pandas library in this script
#is necessary to be able to read and manipulate data
import pandas as pd


#standardizes column names
#This lower cases and replaces spaces with underscores
#makes column names consistent and easier to work with
def fix_column_names(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_', regex=False)
    return df

#Removing leading and trailing spaces from string entries
#prevents duplicates 
#ensures consistency in data entries
def clean_string_columns(df, col_names):
    for col in col_names:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
    return df

#Replacing missing data in price and quantity columns (filling with 0)
#So that it prevents errors in analysis due to missing values
def replace_missing_values(df):
    df["price"] = pd.to_numeric(df["price"], errors='coerce').fillna(0) #fills missing prices with 0 also makes sure its numeric
    df["qty"] = pd.to_numeric(df["qty"], errors='coerce').fillna(0) #fills missing quantities with 0 also makes sure its numeric
    return df

#Removing rows with negative prices or quantities
#Ensures no negative values in price or quantity
#removes invalid data entries that could mess with the analysis
def Remove_negative_values(df):
    df = df[df["price"] >= 0] #removes negative prices
    df = df[df["qty"] >= 0] #removes negative quantities
    return df

#Completed common errors now create a new updated cleaned data file
if __name__ == "__main__":
    # Construct paths relative to repository root
    root = Path(__file__).resolve().parents[1]
    raw_path = root / "data" / "raw" / "sales_data_raw.csv"
    cleaned_path = root / "data" / "processed" / "sales_data_clean.csv"
    
    # Ensure output directory exists
    cleaned_path.parent.mkdir(parents=True, exist_ok=True)
    
#Load sales_data_raw.csv from data/raw/
#makes the script able to read the csv
#helps for the cleaning in order to create a new cleaned data file
    df = pd.read_csv(raw_path)
    
#Calls the cleaning functions back
#makes sure that it actually updates the dataframe
    df = fix_column_names(df)
    df = clean_string_columns(df, ["prodname", "category"])
    df = replace_missing_values(df)
    df = Remove_negative_values(df)
    
#Saves the cleaned data to a new csv file
#Has it moved to data/processed/sales_data_clean.csv
    df.to_csv(cleaned_path, index=False) 
    print("Cleaning complete. First few rows:")
    print(df.head()) #prints first 5 rows
