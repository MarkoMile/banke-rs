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

#temporarily hard-coded
sheets_folder = 'sheets/'

def download_data(sheets_folder='sheets/', table_url='https://nbs.rs/static/nbs_site/gen/cirilica/50/vl_strukt/50b5.htm'):
    links_dictionary = get_excel_urls(table_url)
        
    #test download_file function
    for name,link in links_dictionary.items():
        download_file(link, sheets_folder)

# def show_loading_frame(master = None):
#     # Add a temporary loading label until data is parsed and aggregated
#     loading_label = ctk.CTkLabel(master, text="Učitavanje podataka...", font=("Arial", 24))
#     loading_label.grid(row=1, column=0, pady=10, sticky="n")

#     # Configure the master to expand and fill the available space
#     master.grid_rowconfigure(0, weight=1)
#     master.grid_rowconfigure(1, weight=1)
#     master.grid_columnconfigure(0, weight=1)

#     show_frame(master)

def load_main_dashboard_data(agg_frame = None):
    # DATA THAT WILL BE DISPLAYED ON MAIN DASHBOARD
    UKUPNO_AKTIVA_2023 = agg_frame.dataframe[agg_frame.dataframe['Godina'] == 2023]['UKUPNO AKTIVA'].sum()
    UKUPNO_AKTIVA_2022 = agg_frame.dataframe[agg_frame.dataframe['Godina'] == 2022]['UKUPNO AKTIVA'].sum()
    RAST_AKTIVE = round((UKUPNO_AKTIVA_2023 / UKUPNO_AKTIVA_2022-1)*100,2)
    UKUPAN_DEPOZIT_2023 = agg_frame.dataframe[agg_frame.dataframe['Godina'] == 2023]['Depoziti i ostale finansijske obaveze prema drugim komitentima'].sum()
    UKUPAN_DEPOZIT_2022 = agg_frame.dataframe[agg_frame.dataframe['Godina'] == 2022]['Depoziti i ostale finansijske obaveze prema drugim komitentima'].sum()
    RAST_DEPOZITA = round((UKUPAN_DEPOZIT_2023 / UKUPAN_DEPOZIT_2022-1)*100,2)
    UKUPAN_KREDIT_2023 = agg_frame.dataframe[agg_frame.dataframe['Godina'] == 2023]['Krediti i potraživanja od komitenata'].sum()
    UKUPAN_KREDIT_2022 = agg_frame.dataframe[agg_frame.dataframe['Godina'] == 2022]['Krediti i potraživanja od komitenata'].sum()
    RAST_KREDITA = round((UKUPAN_KREDIT_2023 / UKUPAN_KREDIT_2022-1)*100,2)

    # dataframe that contains display data
    display_data = pd.DataFrame({
        'UKUPNO_AKTIVA_2023': [UKUPNO_AKTIVA_2023],
        'RAST_AKTIVE': [RAST_AKTIVE],
        'UKUPAN_DEPOZIT_2023': [UKUPAN_DEPOZIT_2023],
        'RAST_DEPOZITA': [RAST_DEPOZITA],
        'UKUPAN_KREDIT_2023': [UKUPAN_KREDIT_2023],
        'RAST_KREDITA': [RAST_KREDITA]
    })

    # Filter godina 2023 and show only column 'Udeo na tržištu'
    data_treemap = agg_frame.dataframe[agg_frame.dataframe['Godina']==2023][['Banka','Udeo na tržištu']].reset_index(drop=True)
    data_treemap['Ticker'] = data_treemap['Banka'].map(tickers)
    
    return data_treemap,display_data

def creat_agg_frame(sheet_path='dataframe.xlsx',bank_data=None):
    # If sheet_path is provided (and exists), filter the data for that sheet, else create new Agg_frame
    agg_frame = Agg_frame(None if not(sheet_path and os.path.exists(sheet_path)) else sheet_path)
    agg_frame.aggregate_bilans(bank_data)

    agg_frame.add_indicators()
    # agg_frame.show_correlations()
    agg_frame.hierarchical_clustering()
    agg_frame.kmeans()
    agg_frame.perform_pca_and_cluster()
    agg_frame.dataframe.loc[:, 'Ticker'] = agg_frame.dataframe['Banka'].map(tickers)
    #take cluster from rows with Godina==2023 and add it to the rows with Godina==2022 if the cell banka is the same
    agg_frame.dataframe.loc[agg_frame.dataframe['Godina'] == 2022, 'cluster'] = agg_frame.dataframe.loc[agg_frame.dataframe['Godina'] == 2022, 'Banka'].map(agg_frame.dataframe.loc[agg_frame.dataframe['Godina'] == 2023].set_index('Banka')['cluster'])


    # print(agg_frame.dataframe)
    return agg_frame

#callback should be show_main_dashboard
def load_sheets(sheets_folder='sheets/',sheet_path='dataframe.xlsx',download=False,load=False,save=True):

    # Download data if folder doesn't exist or if the folder is empty [or if download is set to True]
    if download or (not os.path.exists(sheets_folder) or not os.listdir(sheets_folder)):
        download_data(sheets_folder, table_url)

    if not load:
        # Parse the excel files and aggregate the data
        bank_data = parse_sheet_excel(sheets_folder)

        agg_frame = creat_agg_frame(sheet_path,bank_data)
        if save:
            agg_frame.output_file(sheet_path)
    else:
        if os.path.exists(sheet_path):
            try:
                agg_frame = Agg_frame(sheet_path)
                agg_frame.load_file(sheet_path)
            except:
                raise ValueError("Sheet path not provided correctly or file not found")
                exit(1)
        else:
            print("Sheet path not provided correctly or file not found")
            print("Defaulting to download and save mode...")
            download_data(sheets_folder, table_url)
            # Parse the excel files and aggregate the data
            bank_data = parse_sheet_excel(sheets_folder)

            agg_frame = creat_agg_frame(sheet_path,bank_data)
            agg_frame.output_file(sheet_path)

    return agg_frame
    # if callback:
    #     data_treemap, display_data = load_main_dashboard_data(agg_frame)
    #     callback(data_treemap,display_data)
    #     return agg_frame
    # else:
    #     raise ValueError("Callback function not provided")

# Function to create Seaborn chart
# DEPRECATED: USE change_grouped_barplot INSTEAD
# def create_grouped_barplot(data, banks, marketvalue, year, title):
#     fig, ax = plt.subplots()
#     sns.barplot(data=data, x=banks, y=marketvalue,hue=year, ax=ax)
#     ax.set_title(title)
#     ax.legend()
#     return fig

# Function to change Seaborn chart,
# bank_canvas.draw() MUST be called after this function
def change_grouped_barplot(canvas,ax,data, banks, marketvalue, year, title):
    ax.clear()
    ax = sns.barplot(data=data, x=banks, y=marketvalue,hue=year, ax=ax)
    ax.set_title(title)
    ax.legend()
    canvas.draw()

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

# Function to switch frames
def show_frame(frame):
    frame.tkraise()

# Function to handle click events in treemap
def on_click(event,bank_canvas=None,bank_market_chart_ax=None,agg_frame=None):
    if event:
        # event.annotation.remove()
        pass
    if event.artist:
        label = event.artist.patches[event.index].name
        #get bank cluster value for this label
        bank_cluster = agg_frame.dataframe.loc[(agg_frame.dataframe["Banka"] == label, "cluster")].values[0]
        df = agg_frame.dataframe.loc[(agg_frame.dataframe['cluster'] == bank_cluster)]

        #create dataframe to be used for data
        print(f"Clicked on: {label}")
        show_frame(bank_frame)

        if bank_canvas and bank_market_chart_ax and agg_frame:
            change_grouped_barplot(bank_canvas,bank_market_chart_ax,df, "Ticker","UKUPNO AKTIVA","Godina", f"Grafikon {int(bank_cluster)}. klastera")
        else:
            print("Error: bank_canvas, bank_market_chart_ax or agg_frame not provided")
            return


# callback function to change color when hovering in treemap
def on_hover(event):
    if event.artist:
        for patch in event.artist.patches:
            patch.set_alpha(0.6)
        event.artist.patches[event.index].set_alpha(0.5)

def show_market_chart(data = None, master = None,on_click_callback=lambda event, bank_canvas,bank_market_chart_ax,agg_frame, : on_click(event,bank_canvas,bank_market_chart_ax,agg_frame),on_hover_callback=lambda event: on_hover(event)):
    # Add content to 'chart' frame
    market_chart = create_treemap(data)
    canvas = FigureCanvasTkAgg(market_chart, master=master)
    canvas.draw()
    canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

    # Add click functionality to the treemap elements
    cursor = mplcursors.cursor(market_chart, hover=False)
    cursor.connect("add", on_click_callback)
    # add hover functionality to the treemap elements
    hover_cursor = mplcursors.cursor(market_chart, hover=True)
    hover_cursor.connect("add", on_hover_callback)

    # i want to make the annotation invisible
    cursor.annotation_kwargs = {'alpha':0}
    hover_cursor.annotation_kwargs = {'alpha':0}

    return canvas

def show_market_data(data = None,master = None):

    BOX_LABELS = ['UKUPNO AKTIVA 2023', 'RAST AKTIVE', 'UKUPAN DEPOZIT 2023', 'RAST DEPOZITA', 'UKUPAN KREDIT 2023', 'RAST KREDITA']
    BOX_DATA = [data.at[0,'UKUPNO_AKTIVA_2023'], data.at[0,'RAST_AKTIVE'], data.at[0,'UKUPAN_DEPOZIT_2023'], data.at[0,'RAST_DEPOZITA'], data.at[0,'UKUPAN_KREDIT_2023'], data.at[0,'RAST_KREDITA']]

    # Add 6 boxes with labels and data to 'data' frame
    for i, (label_text, data_value) in enumerate(zip(BOX_LABELS, BOX_DATA)):
        row, col = divmod(i, 2)
        box_frame = ctk.CTkFrame(master)
        box_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        label = ctk.CTkLabel(box_frame, text=label_text, font=("Arial", 24))
        label.pack(pady=5)
        
        data_content = ctk.CTkLabel(box_frame, text=f"{data_value}{'%' if i % 2 else ''}", font=("Arial", 30))
        data_content.pack(pady=5)

    # Configure the master to expand and fill the available space
    for i in range(3):
        master.grid_rowconfigure(i, weight=1,uniform='Silent_Creme')
    for j in range(2):
        master.grid_columnconfigure(j, weight=1,uniform='Silent_Creme')

def show_main_dashboard(master = None, treemap_data = None, market_data = None, bank_canvas=None,bank_market_chart_ax=None,agg_frame=None):
    # Add Title to 'entire market' frame
    entire_market_title = ctk.CTkLabel(master, text="Celo tržište", font=("Arial", 24))
    entire_market_title.grid(row=0, column=0, columnspan=2, pady=10, sticky="n")

    # Create sub-frames for chart and numerical data
    main_chart_frame = ctk.CTkFrame(master)
    main_data_frame = ctk.CTkFrame(master)

    main_chart_frame.grid(row=1, column=0, sticky="nsew")
    main_data_frame.grid(row=1, column=1, sticky="nsew")

    # Configure the master to expand and fill the available space
    master.grid_rowconfigure(1, weight=1)
    master.grid_columnconfigure(0, weight=10,uniform='Silent_Creme')
    master.grid_columnconfigure(1, weight=9,uniform='Silent_Creme')

    # Show the treemap
    show_market_chart(data=treemap_data, master=main_chart_frame,on_click_callback=lambda event: on_click(event,bank_canvas,bank_market_chart_ax,agg_frame))

    # Show the numerical data
    show_market_data(data=market_data, master=main_data_frame)

    show_frame(master)
    

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#NOTE: SHOULDN'T BE CREATING DICTIONARIES, INSTEAD INDEXING DATAFRAMES DIRECTLY
# def create_full_dataframes(label,agg_frame):
#     #docstring template
#     """
#     Function to create full dataframes for each bank that contains all the data for that bank
#     """
#     # get cluster of the bank by reading the dataframe in 2023
#     bank_clusters[label] = agg_frame.dataframe.loc[
#         (agg_frame.dataframe['Godina'] == 2023) & (agg_frame.dataframe['Banka'] == label), 'cluster'
#     ].values[0]

#     bank_clustered_dataframes[label] = agg_frame.dataframe.loc[
#         agg_frame.dataframe['cluster'] == bank_clusters[label]
#     ].copy()
#     bank_clustered_dataframes[label].loc[:, 'Ticker'] = bank_clustered_dataframes[label]['Banka'].map(tickers)

#     # create new dataframe from agg_frame containing all banks that are in bank_clustered_dataframes[label]['Banka']
#     bank_full_dataframes[label] = agg_frame.dataframe[agg_frame.dataframe['Banka'].isin(bank_clustered_dataframes[label]['Banka'])].copy()
#     bank_full_dataframes[label].loc[:, 'Ticker'] = bank_full_dataframes[label]['Banka'].map(tickers)
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # #create rank for each bank
    # agg_frame.dataframe[agg_frame.dataframe['Godina'] == 2023].loc[:, 'rang'] = agg_frame.dataframe[agg_frame.dataframe['Godina'] == 2023]['UKUPNO AKTIVA'].rank(ascending=False)
    #NOTE: DEPRECATED
#     bank_dataframes[label] = agg_frame.dataframe[agg_frame.dataframe['Godina'] == 2023].copy()
#     # rank this bank by UKUPNO AKTIVA
#     bank_dataframes[label].loc[:, 'rang'] = bank_dataframes[label]['UKUPNO AKTIVA'].rank(ascending=False)

    # BOX_DATA = [bank_dataframes[label][bank_dataframes[label]['Banka'] == label]['rang'].values[0],bank_dataframes[label][bank_dataframes[label]['Banka'] == label]['UKUPNO AKTIVA'].values[0],round(bank_dataframes[label][bank_dataframes[label]['Banka'] == label]['Neto kamatna marža'].values[0],2),round(bank_dataframes[label][bank_dataframes[label]['Banka'] == label]['Povrat na sopstveni kapital'].values[0],2),round(bank_dataframes[label][bank_dataframes[label]['Banka'] == label]['Koeficijent likvidnosti'].values[0],2),round(bank_dataframes[label][bank_dataframes[label]['Banka'] == label]['Stopa obezvređenja'].values[0],2)]
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


# function to change the data in the chart based on radio button click
# def on_radio_click(event, value, label):
#     global bank_market_charts
#     global bank_full_dataframes
#     global bank_clusters
#     global bank_canvases
#     global bank_chart_frames
#     if label in bank_canvases and bank_canvases[label].get_tk_widget().winfo_exists():
#         bank_canvases[label].get_tk_widget().pack_forget()
#     # on radio click, do different things based on value
#     if (value==0):
#         #change the data in the chart to show UKUPNO AKTIVA
#         print("change the data in the chart to show UKUPNO AKTIVA")
#         bank_market_charts[label].clear()
#         bank_market_charts[label] = create_grouped_barplot(bank_full_dataframes[label], "Ticker","UKUPNO AKTIVA","Godina", f"Grafikon {int(bank_clusters[label])}. klastera")
#     elif (value==1):
#         #change the data in the chart to show NETO KAMATNA MARŽA
#         print("change the data in the chart to show NETO KAMATNA MARŽA")
#         bank_market_charts[label].clear()
#         bank_market_charts[label] = create_grouped_barplot(bank_full_dataframes[label], "Ticker","Neto kamatna marža","Godina", f"Grafikon {int(bank_clusters[label])}. klastera")
#     elif (value==2):
#         #change the data in the chart to show POVRAT NA SOPSTVENI KAPITAL
#         print("change the data in the chart to show POVRAT NA SOPSTVENI KAPITAL")
#         bank_market_charts[label].clear()
#         bank_market_charts[label] = create_grouped_barplot(bank_full_dataframes[label], "Ticker","Povrat na sopstveni kapital","Godina", f"Grafikon {int(bank_clusters[label])}. klastera")
#     elif (value==3):
#         #change the data in the chart to show Koeficijent likvidnosti
#         print("change the data in the chart to show Koeficijent likvidnosti")
#         bank_market_charts[label].clear()
#         bank_market_charts[label] = create_grouped_barplot(bank_full_dataframes[label], "Ticker","Koeficijent likvidnosti","Godina", f"Grafikon {int(bank_clusters[label])}. klastera")
#     elif (value==4):
#         #change the data in the chart to show Stopa obezvređenja
#         print("change the data in the chart to show Stopa obezvređenja")
#         bank_market_charts[label].clear()
#         bank_market_charts[label] = create_grouped_barplot(bank_full_dataframes[label], "Ticker","Stopa obezvređenja","Godina", f"Grafikon {int(bank_clusters[label])}. klastera")
#     elif (value==5):
#         #change the data in the chart to show Odnos kredita prema depozitima
#         print("change the data in the chart to show Odnos kredita prema depozitima")
#         bank_market_charts[label].clear()
#         bank_market_charts[label] = create_grouped_barplot(bank_full_dataframes[label], "Ticker","Odnos kredita prema depozitima","Godina", f"Grafikon {int(bank_clusters[label])}. klastera")
#     bank_canvases[label] = FigureCanvasTkAgg(bank_market_charts[label], master=bank_chart_frames[label])
#     bank_canvases[label].draw()
#     bank_canvases[label].get_tk_widget().pack(side="top", fill="both", expand=True)

def create_bank_frame(master,agg_frame=None):
    bank_frame = ctk.CTkFrame(master)
    bank_frame.grid(row=0, column=0, sticky="nsew")

    # Add Title to bank frame
    bank_title = ctk.CTkLabel(bank_frame, text="<Banka-Placeholder>", font=("Arial", 24))
    bank_title.grid(row=0, column=0, columnspan=3, pady=10, sticky="n")

    # Add a button to row 0
    bank_button = ctk.CTkButton(bank_frame, text="Return to dashboard", command=lambda: show_frame(entire_market_frame))
    bank_button.grid(row=0, column=2, padx=10, pady=10, sticky="e")

    # Create sub-frames for chart and numerical data
    bank_choice_frame = ctk.CTkFrame(bank_frame)
    bank_chart_frame = ctk.CTkFrame(bank_frame)
    bank_data_frame = ctk.CTkFrame(bank_frame)

    bank_choice_frame.grid(row=1, column=0, sticky="nsew")
    #vertically center bank_choice_frame
    bank_choice_frame.grid_rowconfigure(0, weight=1)
    bank_chart_frame.grid(row=1, column=1, sticky="nsew")
    bank_data_frame.grid(row=1, column=2, sticky="nsew")

    # Configure the bank_frame to expand and fill the available space
    bank_frame.grid_rowconfigure(1, weight=1)
    bank_frame.grid_columnconfigure(0, weight=1,uniform='Silent_Creme')
    bank_frame.grid_columnconfigure(1, weight=9,uniform='Silent_Creme')
    bank_frame.grid_columnconfigure(2, weight=9,uniform='Silent_Creme')
    #NOTE: CONTINUE HERE WITH THE REST OF THE CODE UNDER...
    # create base figure for bank_canvas
    bank_frame.bank_market_chart_fig, bank_frame.bank_market_chart_ax = plt.subplots()
    bank_frame.bank_canvas = FigureCanvasTkAgg(bank_frame.bank_market_chart_fig,master=bank_chart_frame)
    bank_frame.bank_canvas.get_tk_widget().pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)
    
    BOX_LABELS = ['RANG PO AKTIVI','UKUPNA AKTIVA', 'NETO KAMATNA MARŽA','POVRAĆAJ NA SOPSTVENI KAPITAL', 'KOEFICIJENT LIKVIDNOSTI', 'STOPA OBEZVREĐENJA']


    # Add 6 boxes with labels and data to 'data' frame
    for i in range(3):
        for j in range(2):
            bank_box_frame = ctk.CTkFrame(bank_data_frame)
            bank_box_frame.grid(row=i, column=j, padx=10, pady=10, sticky="nsew")
            
            box_text = ctk.CTkLabel(bank_box_frame, text=BOX_LABELS[i*2 + j], font=("Arial", 24))
            box_text.pack(pady=5)
            
            data_content = ctk.CTkLabel(bank_box_frame, text="placeholder_text", font=("Arial", 30))
            #NOTE: USE THIS FOR CHANGE_BANK_DATA
            # data_content = ctk.CTkLabel(bank_box_frame, text=str(BOX_DATA[i*2 + j]) + ('%' if (i*2 + j) >=2 else ''), font=("Arial", 30))
            data_content.pack(pady=5)

    # Configure the bank_data_frames[label] to expand and fill the available space
    for i in range(3):
        bank_data_frame.grid_rowconfigure(i, weight=1,uniform='Silent_Creme')
    for j in range(2):
        bank_data_frame.grid_columnconfigure(j, weight=1,uniform='Silent_Creme')

    # Add 6 vertical radio buttons to 'bank_choice' frame that are connected to each other
    bank_choice = ctk.IntVar()
    for i in range(6):
        bank_choice_button = ctk.CTkRadioButton(bank_choice_frame, text=f"", variable=bank_choice, value=i)
        bank_choice_button.grid(row=i, column=0, padx=10, pady=10, sticky="w")
        #NOTE: USE THIS FOR CHANGE_BANK_DATA
        #add on_click event to radio buttons
        # bank_choice_button.bind("<Button-1>", lambda event, value=i, label=label: on_radio_click(event, value, label))

    # center all the radio buttons vertically
    for i in range(6):
        bank_choice_frame.grid_rowconfigure(i, weight=1,uniform='Silent_Creme')

    return bank_frame

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
loading_frame = ctk.CTkFrame(container)
entire_market_frame = ctk.CTkFrame(container)
bank_frame = create_bank_frame(container)

loading_frame.grid(row=0, column=0, sticky="nsew")
entire_market_frame.grid(row=0, column=0, sticky="nsew")
    

# NOTE:DEPRECATED
# Schedule load_sheets to run after the main loop starts
# show_loading_frame(master=loading_frame)

agg_frame = load_sheets(
    sheets_folder,
    save=False,
    sheet_path='dataframe.xlsx',
    download=False,
    load=True
)

# # #NOTE: PUT THIS OUTSIDE OF  THE CALLBACK
# bank_clustered_dataframe = agg_frame.dataframe.loc[agg_frame.dataframe['cluster'] == bank_cluster].copy()

data_treemap, display_data = load_main_dashboard_data(agg_frame)
show_main_dashboard(
        master=entire_market_frame,
        treemap_data=data_treemap,
        market_data=display_data,
        bank_canvas=bank_frame.bank_canvas,
        bank_market_chart_ax=bank_frame.bank_market_chart_ax,
        agg_frame=agg_frame
    )

#bank_frame.canvas...

#NOTE:
# try using threads to load the data and be able to update the app in parallel


app.mainloop()

