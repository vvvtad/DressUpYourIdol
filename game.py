from tkinter import *
import tkinter as tk
import tkinter.messagebox as mb
import pygame as py
import sqlite3
from datetime import datetime

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

class NameEntry:
    def __init__(self, parent, callback):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Enter Player Name")
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)
        self.callback = callback
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (300 // 2)
        self.dialog.geometry(f'+{x}+{y}')
        
        label = Label(self.dialog, text="Enter Your Name: ", font=("Comic Sans MS", 16))
        label.pack(pady=20)
        
        self.entry = Entry(self.dialog, font=("Comic Sans MS", 14))
        self.entry.pack(pady=10)
        self.entry.focus()
        
        btn = Button(self.dialog, text="Continue ", command=self.submit_name,
                    font=("Comic Sans MS", 12), bg="#f2a445", fg="#fff")
        btn.pack(pady=20)
        
        self.dialog.bind('<Return>', lambda event: self.submit_name())

    def submit_name(self):
        name = self.entry.get().strip()
        if name:
            self.callback(name)
            self.dialog.destroy()
        else:
             mb.showwarning("Input Error ", "Please enter a valid name. ")

class LeaderboardPanel:
    def __init__(self, parent, canvas, menu_items, bg_image, db_instance):
        self.parent = parent
        self.canvas = canvas
        self.menu_items = menu_items
        self.bg_image = bg_image
        self.db = db_instance
        self.frame = Frame(parent)
        self.bg_canvas = Canvas(self.frame, width=700, height=700, highlightthickness=0)
        self.bg_canvas.pack(fill="both", expand=True)
        self.bg_canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        self.bg_canvas.image = self.bg_image
        
        title = Label(
            self.bg_canvas,
            text="🏆 LEADERBOARD 🏆 ",
            font=("Comic Sans MS", 28, "bold"),
            bg="#fff4e6",
            fg="#222222"
        )
        
        header_frame = Frame(self.bg_canvas, bg="#f2a445")
        self.bg_canvas.create_window(350, 150, window=header_frame, width=500)
        
        Label(header_frame, text="Rank ", width=5, bg="#f2a445", font=("Arial", 12, "bold")).pack(side=LEFT)
        Label(header_frame, text="Player ", width=20, bg="#f2a445", font=("Arial", 12, "bold")).pack(side=LEFT)
        Label(header_frame, text="Score ", width=10, bg="#f2a445", font=("Arial", 12, "bold")).pack(side=LEFT)
        Label(header_frame, text="Date ", width=15, bg="#f2a445", font=("Arial", 12, "bold")).pack(side=LEFT)
        
        self.scores_frame = Frame(self.bg_canvas, bg="#fff4e6")
        self.bg_canvas.create_window(350, 350, window=self.scores_frame, width=500)
        
        self.score_widgets = []
        
        back_btn = tk.Button(
            self.bg_canvas,
            text="← Back to Menu ",
            font=("Comic Sans MS", 14),
            command=self.hide,
            bg="#f44a28",
            fg="white"
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
                Label(self.scores_frame, text="No scores yet! ", 
                     font=("Comic Sans MS", 14), bg="#fff4e6").pack(pady=20)
            else:
                for i, (player, score, date) in enumerate(scores, 1):
                    row_frame = Frame(self.scores_frame, bg="#fff4e6" if i % 2 == 0 else "white")
                    row_frame.pack(fill="x", pady=2)
                    
                    Label(row_frame, text=f"{i}. ", width=5, bg=row_frame.cget("bg"), 
                         font=("Arial", 11)).pack(side=LEFT)
                    Label(row_frame, text=player, width=20, bg=row_frame.cget("bg"), 
                         font=("Arial", 11)).pack(side=LEFT)
                    Label(row_frame, text=str(score), width=10, bg=row_frame.cget("bg"), 
                         font=("Arial", 11, "bold")).pack(side=LEFT)
                    Label(row_frame, text=date, width=15, bg=row_frame.cget("bg"), 
                         font=("Arial", 9)).pack(side=LEFT)
                    
                    self.score_widgets.append(row_frame)

class Settings:
    def __init__(self, parent, canvas, menu_items, bg_image):
        self.parent = parent
        self.canvas = canvas
        self.menu_items = menu_items
        self.bg_image = bg_image
        self.frame = Frame(parent)
        self.bg_canvas = Canvas(self.frame, width=700, height=700, highlightthickness=0)
        self.bg_canvas.pack(fill="both", expand=True)
        self.bg_canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        self.bg_canvas.image = self.bg_image
        
        title = Label(
            self.bg_canvas,
            text="Settings ",
            font=("Comic Sans MS", 28, "bold"),
            bg="#fff4e6",
            fg="#222222"
        )
        
        vol_label = Label(
            self.bg_canvas,
            text="Music Volume ",
            font=("Comic Sans MS", 16),
            bg="#fff4e6",
            fg="#222222"
        )
        
        self.volume_slider = Scale(
            self.bg_canvas,
            from_=0,
            to=100,
            orient="horizontal",
            command=self.change_volume,
            bg="#fff4e6",
            font=("Comic Sans MS", 12),
            length=250,
            highlightthickness=0
        )
        self.volume_slider.set(50)
        
        self.mute_btn = tk.Button(
            self.bg_canvas,
            text="Mute Music ",
            font=("Comic Sans MS", 14),
            command=self.toggle_music
        )
        
        close_btn = tk.Button(
            self.bg_canvas,
            text="Close Settings ",
            font=("Comic Sans MS", 14),
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

class Button(tk.Button):
    def __init__(self, top=None, **kwargs):
        super().__init__(top, **kwargs)
        self.config(
            highlightthickness=0,
            padx=10,
            pady=5,
            font=("Comic Sans MS", 15),
            foreground="#f44a28",
            background="#f2a445"
        )
        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)

    def on_hover(self, event):
        self.config(foreground="#f2a445", background="#f44a28")

    def on_leave(self, event):
        self.config(foreground="#f44a28", background="#f2a445")

# Main Application
top = tk.Tk()
top.title("Dress Up Your Idol!")
top.geometry("700x700")
top.resizable(False, False)

db = DataBase()

try:
    menu = PhotoImage(file="Menu.png")
except:
    menu = PhotoImage(width=700, height=700)

c = Canvas(top, width=700, height=700, highlightthickness=0)
c.create_image(0, 0, image=menu, anchor='nw')
c.pack(fill="both", expand=True)

player_name_var = tk.StringVar(value="Guest")

# --- Logic for Name Entry and Leaderboard Flow ---

def show_leaderboard():
    leaderboard_panel.show()

def on_name_submitted(name):
    """Callback when name is entered. Sets name and opens leaderboard."""
    player_name_var.set(name)
    show_leaderboard()

def start_game_flow():
    """Triggered on startup to ask for name."""
    NameEntry(top, on_name_submitted)

def start_game_action():
    """Placeholder for starting the actual game."""
    print(f"Player {player_name_var.get()} is starting the game...")
    mb.showinfo("Game Start", f"Welcome {player_name_var.get()}! Game logic would start here.")

# Buttons
playbutton = Button(top, text="Play", command=start_game_action)
scorebutton = Button(top, text="Score", command=show_leaderboard)
settingsbutton = Button(top, text="Settings")
exitbutton = Button(top, text="Exit", command=top.destroy)

# Positioning Buttons (Play added at the top)
playwindow = c.create_window(320, 340, anchor="nw", window=playbutton)
scorewindow = c.create_window(310, 400, anchor="nw", window=scorebutton)
settingswindow = c.create_window(300, 460, anchor="nw", window=settingsbutton)
exitwindow = c.create_window(320, 520, anchor="nw", window=exitbutton)

# Include playwindow in menu_items so it hides when panels open
menu_items = [playwindow, scorewindow, settingswindow, exitwindow]

# Panels
settings_panel = Settings(top, c, menu_items, menu)
settingsbutton.config(command=settings_panel.show)

# Create leaderboard panel
leaderboard_panel = LeaderboardPanel(top, c, menu_items, menu, db)

# Audio Initialization
try:
    py.mixer.init()
    py.mixer.music.load("BGYO - When I'm With You.wav")
    py.mixer.music.set_volume(0.5)
    py.mixer.music.play(-1)
except:
    print("Audio file not found or mixer error.")

# Start name entry after 100ms (allows window to render first)
top.after(100, start_game_flow)

top.mainloop()