import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import squarify
import mplcursors
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# program
from excel_parser import *
from webscraper import *
from data_anal import *

tickers = {
    '3 BANKA a.d. Novi Sad': '3BAN',
    'ALTA BANKA A.D. BEOGRAD': 'ALT',
    'API Bank akcionarsko društvo Beograd': 'API',
    'Addiko Bank AD Beograd': 'ADIK',
    'Adriatic Bank akcionarsko društvo Beograd': 'ADR',
    'Agroindustrijsko komercijalna banka AIK banka akcionarsko društvo, Beograd': 'AIK',
    'Banca Intesa A.D.- Beograd': 'BIT',
    'Bank of China Srbija akcionarsko društvo Beograd - Novi Beograd': 'BOCS',
    'Banka Poštanska štedionica A.D.- Beograd': 'POS',
    'Erste Bank A.D.- Novi Sad': 'ERST',
    'Eurobank Direktna akcionarsko društvo Beograd': 'EURO',
    'Halkbank Akcionarsko društvo Beograd': 'HALK',
    'MIRABANK AKCIONARSKO DRUSTVO BEOGRAD': 'MIRA',
    'Mobi banka A.D. - Beograd': 'MOBI',
    'NLB Komercijalna banka AD Beograd': 'NLB',
    'OTP Banka Srbija a.d. Novi Sad': 'OTP',
    'ProCredit Bank A.D.- Beograd': 'PRO',
    'Raiffeisen Banka A.D.- Beograd': 'RAIF',
    'Srpska banka A.D.- Beograd': 'SRPS',
    'Unicredit Bank Srbija A.D.- Beograd': 'UNI',
}

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

agg_frame = Agg_frame('test_sheet.xlsx')
agg_frame.aggregate_bilans(bank_data)
agg_frame.add_indicators()
agg_frame.show_correlations()
agg_frame.hierarchical_clustering()
agg_frame.kmeans()
agg_frame.perform_pca_and_cluster()
# agg_frame.print_dataframe()
# agg_frame.output_file('test_sheet.xlsx')

UKUPNO_AKTIVA_2023 = agg_frame.dataframe[agg_frame.dataframe['Godina'] == 2023]['UKUPNO AKTIVA'].sum()
UKUPNO_AKTIVA_2022 = agg_frame.dataframe[agg_frame.dataframe['Godina'] == 2022]['UKUPNO AKTIVA'].sum()
RAST_AKTIVE = round((UKUPNO_AKTIVA_2023 / UKUPNO_AKTIVA_2022-1)*100,2)
UKUPAN_DEPOZIT_2023 = agg_frame.dataframe[agg_frame.dataframe['Godina'] == 2023]['Depoziti i ostale finansijske obaveze prema drugim komitentima'].sum()
UKUPAN_DEPOZIT_2022 = agg_frame.dataframe[agg_frame.dataframe['Godina'] == 2022]['Depoziti i ostale finansijske obaveze prema drugim komitentima'].sum()
RAST_DEPOZITA = round((UKUPAN_DEPOZIT_2023 / UKUPAN_DEPOZIT_2022-1)*100,2)
UKUPAN_KREDIT_2023 = agg_frame.dataframe[agg_frame.dataframe['Godina'] == 2023]['Krediti i potraživanja od komitenata'].sum()
UKUPAN_KREDIT_2022 = agg_frame.dataframe[agg_frame.dataframe['Godina'] == 2022]['Krediti i potraživanja od komitenata'].sum()
RAST_KREDITA = round((UKUPAN_KREDIT_2023 / UKUPAN_KREDIT_2022-1)*100,2)

# Filter godina 2023 and show only column 'Udeo na tržištu'
data_treemap = agg_frame.dataframe[agg_frame.dataframe['Godina']==2023][['Banka','Udeo na tržištu']].reset_index(drop=True)
data_treemap['Ticker'] = data_treemap['Banka'].map(tickers)
# Function to create Seaborn chart
def create_grouped_barplot(data, banks, marketvalue, year, title):
    fig, ax = plt.subplots()
    sns.barplot(data=data, x=banks, y=marketvalue,hue=year, ax=ax)
    ax.set_title(title)
    ax.legend()
    return fig

def create_line_chart(data, x, y, title):
    fig, ax = plt.subplots()
    sns.lineplot(data=data, x=x, y=y, ax=ax)
    ax.set_title(title)
    return fig

def create_treemap(data):
    fig, ax = plt.subplots()
    colors = sns.color_palette("husl", n_colors=len(data))
    sns.set_style(style="whitegrid") # set seaborn plot style
    sizes= data["Udeo na tržištu"].values# proportions of the categories
    label_percent=data["Ticker"]+' '+round(data["Udeo na tržištu"],2).astype(str) + '%' # labels for categories
    squarify.plot(sizes=sizes, label=label_percent, alpha=0.6,color=colors,ax=ax)
    # Ensure each element of the plot is labeled
    for i, rect in enumerate(ax.patches):
        rect.name = data["Banka"][i]
    ax.set_title('Udeo na tržištu u 2023. godini')
    plt.axis('off')
    return fig

# Function to handle click events
def on_click(event):
    if event:
        # event.annotation.remove()
        pass
    if event.artist:
        print(f"Clicked on: {event.artist.patches[event.index].name}")
        show_frame(selected_bank_frames[event.artist.patches[event.index].name])


def on_hover(event):
    if event.artist:
        for patch in event.artist.patches:
            patch.set_alpha(0.6)
        event.artist.patches[event.index].set_alpha(0.5)

def on_radio_click(event, value, label):
    global bank_market_charts
    global bank_full_dataframes
    global bank_clusters
    global bank_canvases
    global bank_chart_frames
    if label in bank_canvases and bank_canvases[label].get_tk_widget().winfo_exists():
        bank_canvases[label].get_tk_widget().pack_forget()
    # on radio click, do different things based on value
    if (value==0):
        #change the data in the chart to show UKUPNO AKTIVA
        print("change the data in the chart to show UKUPNO AKTIVA")
        bank_market_charts[label].clear()
        bank_market_charts[label] = create_grouped_barplot(bank_full_dataframes[label], "Ticker","UKUPNO AKTIVA","Godina", f"{bank_clusters[label]} cluster comparison")
    elif (value==1):
        #change the data in the chart to show NETO KAMATNA MARŽA
        print("change the data in the chart to show NETO KAMATNA MARŽA")
        bank_market_charts[label].clear()
        bank_market_charts[label] = create_grouped_barplot(bank_full_dataframes[label], "Ticker","Neto kamatna marža","Godina", f"{bank_clusters[label]} cluster comparison")
    elif (value==2):
        #change the data in the chart to show POVRAT NA SOPSTVENI KAPITAL
        print("change the data in the chart to show POVRAT NA SOPSTVENI KAPITAL")
        bank_market_charts[label].clear()
        bank_market_charts[label] = create_grouped_barplot(bank_full_dataframes[label], "Ticker","Povrat na sopstveni kapital","Godina", f"{bank_clusters[label]} cluster comparison")
    elif (value==3):
        #change the data in the chart to show Koeficijent likvidnosti
        print("change the data in the chart to show Koeficijent likvidnosti")
        bank_market_charts[label].clear()
        bank_market_charts[label] = create_grouped_barplot(bank_full_dataframes[label], "Ticker","Koeficijent likvidnosti","Godina", f"{bank_clusters[label]} cluster comparison")
    elif (value==4):
        #change the data in the chart to show Stopa obezvređenja
        print("change the data in the chart to show Stopa obezvređenja")
        bank_market_charts[label].clear()
        bank_market_charts[label] = create_grouped_barplot(bank_full_dataframes[label], "Ticker","Stopa obezvređenja","Godina", f"{bank_clusters[label]} cluster comparison")
    elif (value==5):
        #change the data in the chart to show Odnos kredita prema depozitima
        print("change the data in the chart to show Odnos kredita prema depozitima")
        bank_market_charts[label].clear()
        bank_market_charts[label] = create_grouped_barplot(bank_full_dataframes[label], "Ticker","Odnos kredita prema depozitima","Godina", f"{bank_clusters[label]} cluster comparison")
    bank_canvases[label] = FigureCanvasTkAgg(bank_market_charts[label], master=bank_chart_frames[label])
    bank_canvases[label].draw()
    bank_canvases[label].get_tk_widget().pack(side="top", fill="both", expand=True)

# Function to switch frames
def show_frame(frame):
    frame.tkraise()

# Initialize seaborn
sns.set_theme(style="whitegrid")

# Initialize the main app
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1280x720")
app.title("BANKE.RS")


# Create a container frame to hold the pages
container = ctk.CTkFrame(app)
container.pack(fill="both", expand=True)

# Configure the container to expand and fill the available space
container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

# Create frames for each page
entire_market_frame = ctk.CTkFrame(container)
selected_bank_frames = {}
for label in data_treemap['Banka']:
    selected_bank_frames[label] = ctk.CTkFrame(container)

entire_market_frame.grid(row=0, column=0, sticky="nsew")
for frame in (selected_bank_frames.values()):
    frame.grid(row=0, column=0, sticky="nsew")

####################################################
################ ENTIRE MARKET FRAME ###############
####################################################

# Add Title to 'entire market' frame
entire_market_title = ctk.CTkLabel(entire_market_frame, text="Entire Market", font=("Arial", 24))
entire_market_title.grid(row=0, column=0, columnspan=2, pady=10, sticky="n")

# Create sub-frames for chart and numerical data
chart_frame = ctk.CTkFrame(entire_market_frame)
data_frame = ctk.CTkFrame(entire_market_frame)

chart_frame.grid(row=1, column=0, sticky="nsew")
data_frame.grid(row=1, column=1, sticky="nsew")

# Configure the entire_market_frame to expand and fill the available space
entire_market_frame.grid_rowconfigure(1, weight=1)
entire_market_frame.grid_columnconfigure(0, weight=10,uniform='Silent_Creme')
entire_market_frame.grid_columnconfigure(1, weight=9,uniform='Silent_Creme')

# Add content to 'chart' frame
market_chart = create_treemap(data_treemap)
canvas = FigureCanvasTkAgg(market_chart, master=chart_frame)
canvas.draw()
canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

# Add click functionality to the treemap elements
cursor = mplcursors.cursor(market_chart, hover=False)
cursor.connect("add", on_click)
# add hover functionality to the treemap elements
hover_cursor = mplcursors.cursor(market_chart, hover=True)
hover_cursor.connect("add", on_hover)

# i want to make the annotation invisible
cursor.annotation_kwargs = {'alpha':0}
hover_cursor.annotation_kwargs = {'alpha':0}

# # Add content to 'data' frame (example numerical data)
# numerical_data_label = ctk.CTkLabel(data_frame, text="Numerical Data", font=("Arial", 18))
# numerical_data_label.grid(pady=10)

BOX_LABELS = ['UKUPNO AKTIVA 2023', 'RAST AKTIVE', 'UKUPAN DEPOZIT 2023', 'RAST DEPOZITA', 'UKUPAN KREDIT 2023', 'RAST KREDITA']
BOX_DATA = [UKUPNO_AKTIVA_2023, RAST_AKTIVE, UKUPAN_DEPOZIT_2023, RAST_DEPOZITA, UKUPAN_KREDIT_2023, RAST_KREDITA]

# Add 6 boxes with labels and data to 'data' frame
for i in range(3):
    for j in range(2):
        box_frame = ctk.CTkFrame(data_frame)
        box_frame.grid(row=i, column=j, padx=10, pady=10, sticky="nsew")
        
        label = ctk.CTkLabel(box_frame, text=BOX_LABELS[i*2 + j], font=("Arial", 24))
        label.pack(pady=5)
        
        data_content = ctk.CTkLabel(box_frame, text= str(BOX_DATA[i*2 + j]) + ('%' if ((i*2 + j)%2) else '') , font=("Arial", 30))
        data_content.pack(pady=5)

# Configure the data_frame to expand and fill the available space
for i in range(3):
    data_frame.grid_rowconfigure(i, weight=1,uniform='Silent_Creme')
for j in range(2):
    data_frame.grid_columnconfigure(j, weight=1,uniform='Silent_Creme')

    
####################################################
################ SELECTED BANK FRAME ###############
####################################################

# Add Title to bank frames
bank_titles = {}
for label,bank_frame in selected_bank_frames.items():
    bank_titles[label] = ctk.CTkLabel(bank_frame, text=label+' bank', font=("Arial", 24))
    bank_titles[label].grid(row=0, column=0, columnspan=3, pady=10, sticky="n")

    # Add a button to row 0
    bank_button = ctk.CTkButton(bank_frame, text="Return to dashboard", command=lambda: show_frame(entire_market_frame))
    bank_button.grid(row=0, column=2, padx=10, pady=10, sticky="e")

# Create sub-frames for chart and numerical data
bank_choice_frames = {}
bank_chart_frames = {}
bank_data_frames = {}
bank_box_frames = {}
# make bank_market_charts global
bank_market_charts = {}
bank_choices = {}
bank_choice_buttons= {}
bank_clustered_dataframes = {}
bank_clusters = {}
bank_dataframes = {}
bank_full_dataframes = {}
bank_canvases = {}

for label,bank_frame in selected_bank_frames.items():
    bank_choice_frames[label] = ctk.CTkFrame(bank_frame)
    bank_chart_frames[label] = ctk.CTkFrame(bank_frame)
    bank_data_frames[label] = ctk.CTkFrame(bank_frame)

    bank_choice_frames[label].grid(row=1, column=0, sticky="nsew")
    bank_chart_frames[label].grid(row=1, column=1, sticky="nsew")
    bank_data_frames[label].grid(row=1, column=2, sticky="nsew")

    # Configure the bank_frame to expand and fill the available space
    bank_frame.grid_rowconfigure(1, weight=1)
    bank_frame.grid_columnconfigure(0, weight=1,uniform='Silent_Creme')
    bank_frame.grid_columnconfigure(1, weight=9,uniform='Silent_Creme')
    bank_frame.grid_columnconfigure(2, weight=9,uniform='Silent_Creme')

    # get cluster of the bank by reading the dataframe in 2023
    bank_clusters[label] = agg_frame.dataframe[agg_frame.dataframe['Godina'] == 2023][agg_frame.dataframe['Banka'] == label]['cluster'].values[0]
    bank_clustered_dataframes[label] = agg_frame.dataframe[agg_frame.dataframe['cluster'] == bank_clusters[label]]
    bank_clustered_dataframes[label]['Ticker'] = bank_clustered_dataframes[label]['Banka'].map(tickers)

    #create new dataframe from agg_frame containing all banks that are in bank_clustered_dataframes[label]['Banka']
    bank_full_dataframes[label] = agg_frame.dataframe[agg_frame.dataframe['Banka'].isin(bank_clustered_dataframes[label]['Banka'])]
    bank_full_dataframes[label]['Ticker'] = bank_full_dataframes[label]['Banka'].map(tickers)

    # NOTE: comment this out when debugging for better performance
    # Add content to 'chart' frame
    bank_market_charts[label] = create_grouped_barplot(bank_full_dataframes[label], "Ticker","UKUPNO AKTIVA","Godina", f"{bank_clusters[label]} cluster comparison")
    bank_canvases[label] = FigureCanvasTkAgg(bank_market_charts[label], master=bank_chart_frames[label])
    bank_canvases[label].draw()
    bank_canvases[label].get_tk_widget().pack(side="top", fill="both", expand=True)

    bank_dataframes[label] = agg_frame.dataframe[agg_frame.dataframe['Godina'] == 2023]
    # rank this bank by UKUPNO AKTIVA
    bank_dataframes[label]['rang'] = bank_dataframes[label]['UKUPNO AKTIVA'].rank(ascending=False)

    BOX_LABELS = ['RANG PO AKTIVI','UKUPNA AKTIVA', 'NETO KAMATNA MARŽA','POVRAĆAJ NA SOPSTVENI KAPITAL', 'KOEFICIJENT LIKVIDNOSTI', 'STOPA OBEZVREĐENJA']
    BOX_DATA = [bank_dataframes[label][bank_dataframes[label]['Banka'] == label]['rang'].values[0],bank_dataframes[label][bank_dataframes[label]['Banka'] == label]['UKUPNO AKTIVA'].values[0],round(bank_dataframes[label][bank_dataframes[label]['Banka'] == label]['Neto kamatna marža'].values[0]*100,2),round(bank_dataframes[label][bank_dataframes[label]['Banka'] == label]['Povrat na sopstveni kapital'].values[0],2),round(bank_dataframes[label][bank_dataframes[label]['Banka'] == label]['Koeficijent likvidnosti'].values[0],2),round(bank_dataframes[label][bank_dataframes[label]['Banka'] == label]['Stopa obezvređenja'].values[0],2)]

    # Add 6 boxes with labels and data to 'data' frame
    for i in range(3):
        for j in range(2):
            bank_box_frames[label] = ctk.CTkFrame(bank_data_frames[label])
            bank_box_frames[label].grid(row=i, column=j, padx=10, pady=10, sticky="nsew")
            
            box_text = ctk.CTkLabel(bank_box_frames[label], text=BOX_LABELS[i*2 + j], font=("Arial", 24))
            box_text.pack(pady=5)
            
            data_content = ctk.CTkLabel(bank_box_frames[label], text=str(BOX_DATA[i*2 + j]) + ('%' if (i*2 + j) >=2 else ''), font=("Arial", 30))
            data_content.pack(pady=5)

    # Configure the bank_data_frames[label] to expand and fill the available space
    for i in range(3):
        bank_data_frames[label].grid_rowconfigure(i, weight=1,uniform='Silent_Creme')
    for j in range(2):
        bank_data_frames[label].grid_columnconfigure(j, weight=1,uniform='Silent_Creme')
    
    # Add 6 vertical radio buttons to 'bank_choice' frame that are connected to each other
    bank_choices[label] = ctk.IntVar()
    for i in range(6):
        bank_choice_buttons[label] = ctk.CTkRadioButton(bank_choice_frames[label], text=f"Choice {i+1}", variable=bank_choices[label], value=i)
        bank_choice_buttons[label].grid(row=i, column=0, padx=10, pady=10, sticky="w")
        #add on_click event to radio buttons
        bank_choice_buttons[label].bind("<Button-1>", lambda event, value=i, label=label: on_radio_click(event, value, label))
    # center the radio buttons vertically
    bank_choice_frames[label].grid_rowconfigure(6, weight=1)

# Add content to 'selected bank' frame
# bank_chart = create_line_chart(data, 'Year', 'BankValue', 'Bank Value Over Years')
# canvas = FigureCanvasTkAgg(bank_chart, master=selected_bank_frame)
# canvas.draw()
# canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

####################################################
################ NAVIGATION MENU ###################
####################################################

# # Navigation menu
# nav_frame = ctk.CTkFrame(app)
# nav_frame.pack(side="left",pady=25,padx=25, fill="y")

# entire_market_button = ctk.CTkButton(nav_frame, text="Entire Market", command=lambda: show_frame(entire_market_frame))
# entire_market_button.pack(pady=10)

# selected_bank_button = ctk.CTkButton(nav_frame, text="Selected Bank", command=lambda: show_frame(selected_bank_frame))
# selected_bank_button.pack(pady=10)

# Show the initial frame
show_frame(entire_market_frame)

app.mainloop()