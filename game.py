from tkinter import *
import tkinter as tk
import tkinter.messagebox as mb
import pygame as py
import sqlite3
import random
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

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS scores(
        id INTEGER PRIMARY KEY,
        player TEXT,
        score INTEGER,
        date TEXT)
        """)

        self.db.commit()

    def add_score(self, player, score):

        date = datetime.now().strftime("%Y-%m-%d %H:%M")

        self.cursor.execute(
            "INSERT INTO scores(player,score,date) VALUES(?,?,?)",
            (player, score, date)
        )

        self.db.commit()

    def get_scores(self):

        self.cursor.execute(
            "SELECT player,score,date FROM scores ORDER BY score DESC LIMIT 10"
        )

        return self.cursor.fetchall()

#Idol Selection
class characterSelection:

    def __init__(self, parent, selected_character):

        selected_character.set("")   # FIX

        self.win = tk.Toplevel(parent)
        self.win.geometry("1000x700")
        self.win.grab_set()

        self.bg = PhotoImage(file="Background-Select.png")

        self.canvas = Canvas(self.win, width=1000, height=700)
        self.canvas.pack()

        self.canvas.create_image(0, 0, image=self.bg, anchor="nw")

        self.selected_character = selected_character

        self.characters = ["Gelo", "Akira", "Mikki", "Nate", "JL"]

        self.imgs = []

        title = Title(self.canvas, text="Choose Idol")
        self.canvas.create_window(500, 80, window=title)

        frame = Frame(self.canvas, bg="#f2776a")
        self.canvas.create_window(500, 350, window=frame)

        for name in self.characters:

            f = Frame(frame, bg="#f2776a")
            f.pack(side=LEFT, padx=10)

            img = PhotoImage(file=f"{name}.png")
            img = img.zoom(3, 3)

            self.imgs.append(img)

            Label(f, image=img, bg="#f2776a").pack()

            tk.Radiobutton(
                f,
                text=name,
                variable=self.selected_character,
                value=name,
                indicatoron=False,
                bg="#f2776a",
                font=("Comic Sans MS", 16)
            ).pack()

        btn = Button(
            self.canvas,
            text="Confirm",
            command=self.confirm
        )

        self.canvas.create_window(500, 600, window=btn)

    def confirm(self):

        char = self.selected_character.get()

        if not char:
            mb.showwarning("Error", "Select idol")
            return

        self.win.destroy()

        playGame(char, db)


class playGame:

    def __init__(self, char, db):

        py.init()

        self.screen = py.display.set_mode((800, 600))

        self.clock = py.time.Clock()

        self.db = db

        self.score = 0
        self.lives = 3

        self.x = 350

        self.items = []
        

        self.bg = py.image.load("Dressing Room.png")
        self.bg = py.transform.scale(self.bg, (800, 600))

        self.life = py.image.load("bgyo-con.png")
        self.life = py.transform.scale(self.life, (40, 40))

        img = py.image.load(f"{char}.png")
        self.player = py.transform.scale(img, (100, 120))


        
        self.clothes_images = []
        for i in range(1, 11):  # Correctly loops from cloth1 to cloth10
            try:
                # Load the image
                cloth = py.image.load(f"cloth{i}.png").convert_alpha()
                
                # Scale them up (e.g., 80x80 or 100x100 instead of 50x50)
                # Adjust these numbers based on the desired visual size
                cloth = py.transform.scale(cloth, (150, 150)) 
                
                self.clothes_images.append(cloth)
            except py.error: # Pygame specific error handling
                print(f"Warning: cloth{i}.png not found")
        
        # Fallback if no images were loaded at all
        if not self.clothes_images:
            fallback = py.Surface((80, 80))
            fallback.fill((255, 0, 0))
            self.clothes_images.append(fallback)
 
        
        # Fallback if no images loaded
        if not self.clothes_images:
            fallback = py.Surface((50, 50))
            fallback.fill((255, 0, 0))
            self.clothes_images.append(fallback)

        self.run()

    def run(self):

        font = py.font.SysFont("Comic Sans MS", 25)

        while self.lives > 0:

            self.screen.blit(self.bg, (0, 0))

            for e in py.event.get():
                if e.type == py.QUIT:
                    self.lives = 0

            keys = py.key.get_pressed()

            if keys[py.K_LEFT]and self.x > 0:
                self.x -= 10

            if keys[py.K_RIGHT] and self.x < 700:
                self.x += 10

            if random.randint(1, 30) == 1:
                # FIX: Store both position AND random clothing image
                self.items.append([
                    random.randint(50, 750),  # x position
                    -50,                       # y position
                    random.choice(self.clothes_images)  # random clothing image
                ])

            for item in self.items[:]:

                item[1] += 4.5 # Fall down

                player_rect = py.Rect(self.x, 450, 100, 120)
                item_rect = py.Rect(item[0], item[1], 125, 125)

                if player_rect.colliderect(item_rect):
                    self.score += 10
                    self.items.remove(item)

                elif item[1] > 600:
                    self.lives -= 1
                    self.items.remove(item)

            self.screen.blit(self.player, (self.x, 450))

            # FIX: Draw the clothing image (item[2] is the image)
            for item in self.items:
                self.screen.blit(item[2], (item[0], item[1]))

            txt = font.render(
                f"Score: {self.score}",
                True,
                (0,0,0)
            )

            self.screen.blit(txt, (20, 20))

            for i in range(self.lives):
                self.screen.blit(
                    self.life,
                    (20 + i * 45, 60)
                )

            py.display.flip()
            self.clock.tick(60)

        py.display.quit()

        name = sd.askstring(
            "Game Over",
            "Enter name"
        )

        if not name:
            name = "Guest"

        self.db.add_score(name, self.score)

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
        
        self.scores_frame = Frame(self.bg_canvas, background="#f2776a")
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

        self.is_muted = False
        
        self.mute_btn = tk.Checkbutton(
            self.bg_canvas,
            text="Mute Music",
            variable = self.is_muted,
            command=self.toggle_music,
            font = ("Comic Sans Ms", 28, "bold"),
            background= "#f2776a",
            foreground= "white",
            activebackground="#f2776a"
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
            py.mixer.music.set_volume(0)
            self.is_muted = True
        else:
            py.mixer.music.set_volume(self.volume_slider.get() / 100)
            self.is_muted = False

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
    top.withdraw()
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
