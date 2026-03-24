from tkinter import *
import tkinter as tk
import tkinter.messagebox as mb
import sqlite3
from datetime import datetime

#Font Styles
class Button(tk.Button):
    def __init__(self, top=None, **kwargs):
        super().__init__(top, **kwargs)
        self.config(
            highlightthickness=0,
            padx=10,
            pady=5,
            font=("Comic Sans MS", 15),
            foreground="white",
            background="#f2a445"
        )
        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)

    def on_hover(self, event):
        self.config(background="#f44a28")

    def on_leave(self, event):
        self.config(background="#f2a445")

class Title(tk.Label):
    def __init__(self, top=None, **kwargs):
        super().__init__(top, **kwargs)
        self.config(
            font=("Comic Sans MS", 28, "bold"),
            foreground="white",
            background="#f2776a"
        )

class Label(tk.Label):
    def __init__(self, top=None, **kwargs):
        super().__init__(top, **kwargs)
        self.config(
            font=("Comic Sans MS", 15),
            foreground="white",
            background="#f2776a"
        )

#Database
class DataBase:
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

    def add_score(self, player, score):
        date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute(
            "INSERT INTO scores (player, score, date) VALUES (?, ?, ?)",
            (player, score, date_now)
        )
        self.db.commit()

    def get_scores(self):
        self.cursor.execute(
            "SELECT player, score, date FROM scores ORDER BY score DESC LIMIT 10"
        )
        return self.cursor.fetchall()

#Idol Selection
class characterSelection:
    def __init__(self, parent, selected_character):
        self.characterselect = tk.Toplevel(parent)
        self.characterselect.title("Dress Up Your Idol!")
        self.characterselect.geometry("1000x700")

        self.bg = PhotoImage(file="Background-Select.png")

        self.idolbg = Canvas(self.characterselect, width=1000, height=700)
        self.idolbg.create_image(0, 0, image=self.bg, anchor='nw')
        self.idolbg.pack(fill="both", expand=True)

        self.selected_character = selected_character
        self.characters = ["Gelo", "Akira", "Mikki", "Nate", "JL"]
        self.img_refs = []
        
        title = Title(self.idolbg, text = "Choose Your Bias")
        self.idolbg.create_window(500, 95, window=title)

        confirm = Button(self.idolbg, text="Confirm", command=self.selectCharacter)
        self.idolbg.create_window(500, 600, window=confirm)

        selection_container = Frame(self.idolbg, highlightthickness=0, bg="#f2776a")
        self.idolbg.create_window(500, 350, window=selection_container)

        for i, char_name in enumerate(self.characters):
            char_container = Frame(selection_container, bg="#f2776a")
            char_container.pack(side=LEFT, expand=True, padx=10)

            # Zooming the image to make it significantly larger
            # .zoom(3, 3) makes it 3x original size. Adjust if needed.
            full_img = PhotoImage(file=f"{char_name}.png")
            display_img = full_img.zoom(3, 3) 
                
            self.img_refs.append(display_img)
            img_label = Label(char_container, image=display_img)

            img_label.pack(pady=15)

            tk.Radiobutton(
                char_container, text=char_name, variable=self.selected_character,
                value=char_name, font=("Comic Sans MS", 20, "bold"),
                bg="#f2776a", 
                activebackground="#f2776a",
            ).pack()

    def selectCharacter(self):
        try:
            character = self.selected_character.get()
            playGame(self.characterselect.master, character)
        except ValueError:
            mb.showwarning("Selection Error", "No characters selected")


class playGame:
    def __init__(self, parent, character):
        self.character = character
        self.frame = Frame(parent)

#Gets Player Name after the game ends
class getName:
    def __init__(self, callback):
        self.title("Dress Up Your Idol!")
        self.geometry("400x200")
        self.resizable(True, True)
        self.configure(background="#f44a28")

        self.callback = callback

        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.winfo_screenheight() // 2) - (300 // 2)
        self.geometry(f'+{x}+{y}')
        
        label = tk.Label(self, text="Enter Your Name: ", font=("Comic Sans MS", 15), foreground= "white", background = "#f44a28")
        label.pack()
        
        self.entry = Entry(self, font=("Comic Sans MS", 15))
        self.entry.pack()
        self.entry.focus()
        
        btn = Button(self, text="Continue ", command=self.submit_name)
        btn.pack(pady=20)
        
        self.bind('<Return>', lambda a: self.submit_name())

    def submit_name(self):
        name = self.entry.get().strip()
        if name:
            self.callback(name)
            self.destroy()
        else:
             mb.showwarning("Input Error ", "Please enter a valid name. ")

#Displays Leaderboard
class LeaderboardPanel:
    def __init__(self, parent, canvas, menu_items, db_instance):
        self.parent = parent
        self.canvas = canvas
        self.menu_items = menu_items
        self.db = db_instance
        self.bg_image = PhotoImage(file = r"Background.png")
        self.frame = Frame(parent)
        self.bg_canvas = Canvas(self.frame, width=700, height=700, highlightthickness=0)
        self.bg_canvas.pack(fill="both", expand=True)
        self.bg_canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        
        title = Title(
            self.bg_canvas,
            text="LEADERBOARD"
        )
        
        header_frame = Frame(self.bg_canvas)
        self.bg_canvas.create_window(350, 150, window=header_frame, width=500)
        
        Label(header_frame, text="Rank", width = 5).pack(side=LEFT)
        Label(header_frame, text="Player", width = 20).pack(side=LEFT)
        Label(header_frame, text="Score", width = 10).pack(side=LEFT)
        Label(header_frame, text="Date", width = 15).pack(side=LEFT)
        
        self.scores_frame = Frame(self.bg_canvas)
        self.bg_canvas.create_window(350, 350, window=self.scores_frame, width=500)
        
        self.score_widgets = []
        
        back_btn = Button(
            self.bg_canvas,
            text="Back to Menu",
            command=self.hide,
        )
        
        self.bg_canvas.create_window(350, 80, window=title)
        self.bg_canvas.create_window(350, 620, window=back_btn)
        
        self.refresh_scores()

    def show(self):
        self.refresh_scores()
        self.frame.place(x=0, y=0, relwidth=1, relheight=1)
        for item in self.menu_items:
            self.canvas.itemconfigure(item, state="hidden")

    def hide(self):
        self.frame.place_forget()
        for item in self.menu_items:
            self.canvas.itemconfigure(item, state="normal")

    def refresh_scores(self):
        for widget in self.score_widgets:
            widget.destroy()
        self.score_widgets = []
        
        if self.db:
            scores = self.db.get_scores()
            if not scores:
                Label(self.scores_frame, text="No scores yet!").pack(pady=20)
            else:
                for i, (player, score, date) in enumerate(scores, 1):
                    row_frame = Frame(self.scores_frame)
                    row_frame.pack(pady=2)
                    
                    Label(row_frame, text=f"{i}. ", width=5).pack(side=LEFT)
                    Label(row_frame, text=player, width=20).pack(side=LEFT)
                    Label(row_frame, text=str(score), width=10).pack(side=LEFT)
                    Label(row_frame, text=date, width=15).pack(side=LEFT)
                    
                    self.score_widgets.append(row_frame)

class Settings:
    def __init__(self, parent, canvas, menu_items):
        self.parent = parent
        self.canvas = canvas
        self.menu_items = menu_items
        self.bg_image = PhotoImage(file = r"Background.png")
        self.frame = Frame(parent)
        self.bg_canvas = Canvas(self.frame, width=700, height=700, highlightthickness=0)
        self.bg_canvas.pack(expand=True)
        self.bg_canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        
        title = Title(
            self.bg_canvas, text="Settings")
        
        vol_label = Title(
            self.bg_canvas, text="Music Volume")
        
        self.volume_slider = Scale(
            self.bg_canvas,
            from_=0,
            to=100,
            orient="horizontal",
            command=self.change_volume,
            bg="#f2a445",
            length=250,
            highlightthickness=0
        )
        self.volume_slider.set(50)
        
        self.mute_btn = Button(
            self.bg_canvas,
            text="Mute Music",
            command=self.toggle_music
        )
        
        close_btn = Button(
            self.bg_canvas,
            text="Close Settings",
            command=self.hide
        )
        
        self.bg_canvas.create_window(350, 140, window=title)
        self.bg_canvas.create_window(350, 230, window=vol_label)
        self.bg_canvas.create_window(350, 280, window=self.volume_slider)
        self.bg_canvas.create_window(350, 350, window=self.mute_btn)
        self.bg_canvas.create_window(350, 420, window=close_btn)
         
        self.is_muted = False

    def show(self):
        self.frame.place(x=0, y=0, relwidth=1, relheight=1)
        for item in self.menu_items:
            self.canvas.itemconfigure(item, state="hidden")

    def hide(self):
        self.frame.place_forget()
        for item in self.menu_items:
            self.canvas.itemconfigure(item, state="normal")

    def change_volume(self, value):
        py.mixer.music.set_volume(int(value) / 100)

    def toggle_music(self):
        if self.is_muted:
            py.mixer.music.set_volume(self.volume_slider.get() / 100)
            self.mute_btn.config(text="Mute Music ")
            self.is_muted = False
        else:
            py.mixer.music.set_volume(0)
            self.mute_btn.config(text="Unmute Music ")
            self.is_muted = True

# Main Application
top = tk.Tk()
top.title("Dress Up Your Idol!")
top.geometry("700x700")
top.resizable(True, True)

db = DataBase()

menu = PhotoImage(file="Menu.png")

c = Canvas(top, width=700, height=700, highlightthickness=0)
c.create_image(0, 0, image=menu, anchor='nw')
c.pack(fill="both", expand=True)

player_name_var = tk.StringVar(value="Guest")
selected_character = tk.StringVar(value="")

# ---Functions for events---
def show_settings():
    settings_panel.show()

def show_leaderboard():
    leaderboard_panel.show()

def on_name_submitted(name):
    """Callback when name is entered. Sets name and opens leaderboard."""
    player_name_var.set(name)
    show_leaderboard()

def start_game_flow():
    """Triggered on startup to ask for name."""
    characterSelection(top, selected_character)


# Buttons
playbutton = Button(top, text="Play", command = start_game_flow)
scorebutton = Button(top, text="Score", command=show_leaderboard)
settingsbutton = Button(top, text="Settings", command=show_settings)
exitbutton = Button(top, text="Exit", command=top.destroy)

# Positioning Buttons
playwindow = c.create_window(320, 340, anchor="nw", window=playbutton)
scorewindow = c.create_window(310, 400, anchor="nw", window=scorebutton)
settingswindow = c.create_window(300, 460, anchor="nw", window=settingsbutton)
exitwindow = c.create_window(320, 520, anchor="nw", window=exitbutton)

# Include playwindow in menu_items so it hides when panels open
menu_items = [playwindow, scorewindow, settingswindow, exitwindow]

# Panels
settings_panel = Settings(top, c, menu_items)
leaderboard_panel = LeaderboardPanel(top, c, menu_items, db)

# Audio Initialization
try:
    py.mixer.init()
    py.mixer.music.load("BGYO - When I'm With You.wav")
    py.mixer.music.set_volume(0.5)
    py.mixer.music.play(-1)
except:
    print("Audio file not found or mixer error.")

top.mainloop()
