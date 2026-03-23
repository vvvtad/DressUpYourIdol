from tkinter import *
import tkinter as tk
import pygame as py
import sqlite3


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

    def get_scores(self):
        self.cursor.execute(
            "SELECT player, score, date FROM scores ORDER BY score DESC LIMIT 10"
        )
        return self.cursor.fetchall()


class playGame(Toplevel):
    def __init__(self, top=None):
        super().__init__(top)
        self.title("Dress Up Your Idol! - Play")
        self.geometry("700x700")

        self.player_name = "Guest"
        self.score = 0
        self.lives = 3

        label1 = Label(self, text=f"Welcome {self.player_name}!", font=("Comic Sans MS", 20))
        label1.pack(pady=20)


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
            text="Settings",
            font=("Comic Sans MS", 28, "bold"),
            bg="#fff4e6",
            fg="#222222"
        )

        vol_label = Label(
            self.bg_canvas,
            text="Music Volume",
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
            text="Mute Music",
            font=("Comic Sans MS", 14),
            command=self.toggle_music
        )

        close_btn = tk.Button(
            self.bg_canvas,
            text="Close Settings",
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
            self.mute_btn.config(text="Mute Music")
            self.is_muted = False
        else:
            py.mixer.music.set_volume(0)
            self.mute_btn.config(text="Unmute Music")
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


top = tk.Tk()
top.title("Dress Up Your Idol!")
top.geometry("700x700")

menu = PhotoImage(file="Menu.png")
c = Canvas(top, width=700, height=700, highlightthickness=0)
c.create_image(0, 0, image=menu, anchor='nw')
c.pack(fill="both", expand=True)

playbutton = Button(top, text="Play")
playbutton.bind("<Button-1>", lambda a: playGame(top))
scorebutton = Button(top, text="Score")
settingsbutton = Button(top, text="Settings")
exitbutton = Button(top, text="Exit", command=top.destroy)

playwindow = c.create_window(320, 380, anchor="nw", window=playbutton)
scorewindow = c.create_window(310, 440, anchor="nw", window=scorebutton)
settingswindow = c.create_window(300, 500, anchor="nw", window=settingsbutton)
exitwindow = c.create_window(320, 560, anchor="nw", window=exitbutton)

menu_items = [playwindow, scorewindow, settingswindow, exitwindow]
settings_panel = Settings(top, c, menu_items, menu)
settingsbutton.config(command=settings_panel.show)

py.mixer.init()
py.mixer.music.load("BGYO - When I'm With You.wav")
py.mixer.music.set_volume(0.5)
py.mixer.music.play(-1)

top.mainloop()