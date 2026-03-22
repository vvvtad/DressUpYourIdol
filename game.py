from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image

class Button(tk.Button): #Costumization of Menu Buttons
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.config(
            highlightthickness=0,  # Remove highlight
            padx=10,  # Add horizontal padding
            pady=5,  # Add vertical padding
            font=("Comic Sans MS", 15),  # Set font
            foreground="#f44a28",  # Text color
            background="#f2a445",  # Background color
        )
        # Bind events
        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)

    def on_hover(self, event):
        self.config(foreground="#f2a445", background="#f44a28")  # Change color on hover
    def on_leave(self, event):
        self.config(foreground="#f44a28", background="#f2a445")  # Restore original color


top = tk.Tk()
top.title("Dress Up Your Idol!")
top.geometry("700x700")
menu = PhotoImage(file="Menu.png")
c = Canvas(top, width=700, height=700)
c.create_image(0, 0, image=menu, anchor='nw')
c.pack(fill = "both", expand = True)

#Menu Buttons
playbutton = Button(top, text="Play")
scorebutton = Button(top, text="Score")
settingsbutton = Button(top, text="Settings")
exitbutton = Button(top, text="Exit")

#Placing the buttons on the menu
playwindow = c.create_window( 320, 380, anchor = "nw", window = playbutton)
scorewindow = c.create_window( 310, 440, anchor = "nw", window = scorebutton)
settingswindow = c.create_window( 300, 500, anchor = "nw", window = settingsbutton)
exitwindow = c.create_window( 320, 560, anchor = "nw", window = exitbutton)
c.pack(side="bottom")

top.mainloop()