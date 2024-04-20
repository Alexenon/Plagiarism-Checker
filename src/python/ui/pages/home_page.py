import os
import tkinter as tk
import customtkinter
from PIL import Image


class HomePage(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.create_widgets()
        customtkinter.set_appearance_mode("Dark")
        # self.configure(bg="darkgrey")

    def create_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        banner = customtkinter.CTkImage(light_image=Image.open(os.path.join("src", "resources", "light_bg.png")),
                                        dark_image=Image.open(os.path.join("src", "resources", "dark_bg.png")),
                                        size=(900, 540))
        banner_label = customtkinter.CTkLabel(self, text="", image=banner)
        banner_label.grid(row=0, column=0, padx=20, pady=(20, 20), sticky="nsew")