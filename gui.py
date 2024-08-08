import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import squarify
import mplcursors
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Sample data
data = pd.DataFrame({
    'Banks': ['A', 'B', 'C', 'D','A', 'B', 'C', 'D'],
    'Year': [2021, 2022, 2021, 2022,2022, 2021, 2022, 2021],
    'MarketValue': [1000, 1500, 2000,3000, 500, 1000, 1500, 2000],
})

data_treemap = pd.DataFrame({
    'labels': ['A', 'B', 'C', 'D','E','F','G','H','I','J'],
    #random array of percentages (adding up to 100)
    'values': list(np.random.dirichlet(np.ones(10),size=1).transpose()*100)
})

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
    sizes= data["values"].values# proportions of the categories
    label_percent=data["labels"]+' '+data["values"].astype(str) + '%' # labels for categories
    squarify.plot(sizes=sizes, label=label_percent, alpha=0.6,color=colors,ax=ax)
    # Ensure each element of the plot is labeled
    for i, rect in enumerate(ax.patches):
        rect.name = data["labels"][i]
    ax.set_title('Treemap with Squarify')
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
for label in data_treemap['labels']:
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

# Add 6 boxes with labels and data to 'data' frame
for i in range(3):
    for j in range(2):
        box_frame = ctk.CTkFrame(data_frame)
        box_frame.grid(row=i, column=j, padx=10, pady=10, sticky="nsew")
        
        label = ctk.CTkLabel(box_frame, text=f"Label {i*2 + j + 1}", font=("Arial", 14))
        label.pack(pady=5)
        
        data_content = ctk.CTkLabel(box_frame, text=f"Data {i*2 + j + 1}", font=("Arial", 12))
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
bank_market_charts = {}
bank_choices = {}
bank_choice_buttons= {}
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

    # NOTE: comment this out when debugging for better performance
    # Add content to 'chart' frame
    bank_market_charts[label] = create_grouped_barplot(data, "Banks","MarketValue","Year", f"{label} Bank Market Value")
    canvas = FigureCanvasTkAgg(bank_market_charts[label], master=bank_chart_frames[label])
    canvas.draw()
    canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

    # Add 6 boxes with labels and data to 'data' frame
    for i in range(3):
        for j in range(2):
            bank_box_frames[label] = ctk.CTkFrame(bank_data_frames[label])
            bank_box_frames[label].grid(row=i, column=j, padx=10, pady=10, sticky="nsew")
            
            box_text = ctk.CTkLabel(bank_box_frames[label], text=f"Label {i*2 + j + 1}", font=("Arial", 14))
            box_text.pack(pady=5)
            
            data_content = ctk.CTkLabel(bank_box_frames[label], text=f"Data {i*2 + j + 1}", font=("Arial", 12))
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