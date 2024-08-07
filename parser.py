import pandas as pd
import os

# BU 31-12-2023 , 22
# BS 31-12-2022 , 22 , 21

def parse_sheet_excel(file_pointer):
    # reading the excel file to extract bank_name
    df = pd.read_excel(file_pointer)
    bank_name = df.columns[0]

    # header set to 5 to skip first rows containing bank name, date and other data
    df = pd.read_excel(file_pointer, header=5)

    # drop arbitrary row containing column numbers
    df = df.drop(df.index[0])
    # reset index
    df = df.reset_index(drop=True)

    # multiply all values in third column by 1000
    df.iloc[:,2] = df.iloc[:,2] * 1000

    return bank_name,df