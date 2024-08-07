import pandas as pd
import os

# BU 31-12-2023 , 22
# BS 31-12-2022 , 22 , 21

def parse_sheet_excel(sheets_folder='sheets/'):
    assert os.path.exists(sheets_folder), "sheets_folder does not exist"
    sheet_files = os.listdir(sheets_folder)


    bank_data = dict()

    for sheet_path in sheet_files:
        with open(sheets_folder+sheet_path, 'rb') as file_pointer:
            sheetname = 'BS'+' '+'31.12.'+'2023'    #placeholder sheetname for getting bank name
            df = pd.read_excel(file_pointer,sheet_name=sheetname)
            bank_name = str(df.columns[0])

            for tip_bilansa in ['BS','BU']:
                for godina in range(2021,2024):
                    sheetname = tip_bilansa+' '+'31.12.'+str(godina)
                    # reading the excel file to extract bank_name
                    df = pd.read_excel(file_pointer,sheet_name=sheetname)

                    # header set to 5 to skip first rows containing bank name, date and other data
                    df = pd.read_excel(file_pointer, header=5,sheet_name=sheetname)

                    # drop arbitrary row containing column numbers
                    df = df.drop(df.index[0])
                    # reset index
                    df = df.reset_index(drop=True)

                    # multiply all values in third column by 1000
                    df.iloc[:,2] = df.iloc[:,2] * 1000

                    # Initialize nested dictionaries if they don't exist
                    if bank_name not in bank_data:
                        bank_data[bank_name] = {}
                    if godina not in bank_data[bank_name]:
                        bank_data[bank_name][godina] = {}

                    # Assign the dataframe to the nested dictionary
                    bank_data[bank_name][godina][tip_bilansa] = df

    return bank_data