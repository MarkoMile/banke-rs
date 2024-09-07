#sample program to test figurecanvastkagg
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk

root = tk.Tk()
root.title("Embedding in Tk")

fig = Figure(figsize=(5, 4), dpi=100)
t = np.arange(0, 3, .01)
fig.n = 1
fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t+fig.n))

def change_figure(fig1=fig):
    fig1.clf()
    fig1.subplots(1,1).plot(t, 2 * np.cos(2 * np.pi * t+fig1.n))
    fig1.n = fig1.n+1
    canvas.draw()
    # canvas.get_tk_widget().update()

canvas = FigureCanvasTkAgg(fig,master=root)  # A tk.DrawingArea.
# canvas.draw()
canvas.get_tk_widget().config(background='red')
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

#create a button to change figure

button = tk.Button(master=root, text="Change Figure", command=change_figure)
button.pack()


tk.mainloop()






