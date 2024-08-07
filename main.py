from parser import *
from webscraper import *

# BU 31-12-2023 , 22
# BS 31-12-2022 , 22 , 21

# this url contains a table of bank names, along with links to their corresponding excel files
# NOTE: we need to check if this is a permanent url or if they change it every year/quarter
table_url = 'https://nbs.rs/static/nbs_site/gen/cirilica/50/vl_strukt/50b5.htm'

#privremeno hard-coded
sheets_folder = 'sheets/'

links_dictionary = get_excel_urls(table_url)
    
#test download_file function
for name,link in links_dictionary.items():
    download_file(link, sheets_folder)


assert os.path.exists(sheets_folder), "sheets_folder does not exist"
sheet_files = os.listdir(sheets_folder)


bank_data = dict()

for sheet_path in sheet_files:
    with open(sheets_folder+sheet_path, 'rb') as file_pointer:
        bank_name, parsed_df = parse_sheet_excel(file_pointer)
        bank_data[bank_name] = parsed_df

print(bank_data)