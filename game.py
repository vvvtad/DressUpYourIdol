from tkinter import *
import tkinter as tk
import pygame as py
import sqlite3 

class DataBase: #Class for handling database operations and connections 
    def __init__(self):
        self.db = sqlite3.connect("scores.db")
        self.cursor = self.db.cursor()
        self.setup_database()

    def setup_database(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS scores(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player TEXT,
            score INTEGER,
            date TEXT
        )
        """)

        self.db.commit()
        def get_scores(self):
            self.cursor.execute(
            "SELECT player, score, date FROM scores ORDER BY score DESC LIMIT 10"
        )
        return self.cursor.fetchall()

class playGame(Toplevel): #New Window for Play Button
    def __init__(self, top=None):
        super().__init__(top)
        self.title("Dress Up Your Idol! - Play")
        self.geometry("700x700")

        # Game variables from your snippet
        self.player_name = "Guest" # You can add an Entry widget to get this
        self.score = 0
        self.lives = 3

        label1 = Label(self, text=f"Welcome {self.player_name}!", font=("Comic Sans MS", 20))
        label1.pack(pady=20)

class Button(tk.Button): #Costumization of Menu Buttons
    def __init__(self, top=None, **kwargs):
        super().__init__(top, **kwargs)
        self.config(
            highlightthickness=0,  # Remove highlight
            padx=10,  # Add horizontal padding
            pady=5,  # Add vertical padding
            font=("Comic Sans MS", 15),  # Set font
            foreground="#f44a28",  # Text color
            background="#f2a445"  # Background color
        )
        # Bind events
        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)

    def on_hover(self, event):
        self.config(foreground="#f2a445", background="#f44a28")  # Change color on hover
    def on_leave(self, event):
        self.config(foreground="#f44a28", background="#f2a445")  # Restore original color


#Main Window
top = tk.Tk()
top.title("Dress Up Your Idol!")
top.geometry("700x700")
menu = PhotoImage(file="Menu.png") #Get Menu Interface from file to be stored at menu variable
c = Canvas(top, width=700, height=700)
c.create_image(0, 0, image=menu, anchor='nw')
c.pack(fill = "both", expand = True)

#Menu Buttons
playbutton = Button(top, text="Play")
playbutton.bind("<Button-1>", lambda a: playGame(top))  #Action to start game when play button is clicked
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
