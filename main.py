from excel_parser import *
from webscraper import *
from data_anal import *

# BU 31-12-2023 , 22
# BS 31-12-2022 , 22 , 21

# this url contains a table of bank names, along with links to their corresponding excel files
# NOTE: we need to check if this is a permanent url or if they change it every year/quarter
table_url = 'https://nbs.rs/static/nbs_site/gen/cirilica/50/vl_strukt/50b5.htm'

#privremeno hard-coded
sheets_folder = 'sheets/'

# links_dictionary = get_excel_urls(table_url)
    
#test download_file function
# for name,link in links_dictionary.items():
#     download_file(link, sheets_folder)

bank_data = parse_sheet_excel(sheets_folder)

# print(bank_data['Unicredit Bank Srbija A.D.- Beograd'])

agg_frame = Agg_frame('test_sheet.xlsx')
agg_frame.aggregate_bilans(bank_data)
agg_frame.add_indicators()
# agg_frame.show_correlations()
agg_frame.hierarchical_clustering()
# agg_frame.kmeans()
# agg_frame.perform_pca_and_cluster()
# agg_frame.print_dataframe()
agg_frame.output_file('test_sheet.xlsx')