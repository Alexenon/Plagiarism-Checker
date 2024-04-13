#######################################--GRAPHICAL USER INTERFACE--#######################################

import tkinter as tk
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfile, askopenfiles, asksaveasfile, asksaveasfilename
from openpyxl import Workbook
from PIL import Image
import customtkinter

from main import *

# Setting Color Theme
customtkinter.set_appearance_mode("Dark")      # Modes: "Dark"(standard), "System", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

# Create App Object
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Plagiarism Checker")
        self.geometry(f"{1100}x{580}")
        self.minsize(1100, 580)

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=10)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, padx=(20, 10), pady=(20, 20), sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Welcome to \nPlagiarism Checker",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text_color=("black", "white"),
                                                        text="HOMEPAGE", command=self.homepage)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text_color=("black", "white"),
                                                        text="COMPARE TWO FILES", command=self.two_file_page)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text_color=("black", "white"),
                                                        text="MULTIPLE COMPARE", command=self.multiple_file_page)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text_color=("black", "white"),
                                                            text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, text_color=("black", "white"),
                                                                        values=["Light", "Dark", "System"],
                                                                        command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text_color=("black", "white"), text="UI Scaling:",anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, text_color=("black", "white"),
                                                               values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # Set Default values
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.homepage()

    # Appearance Modes (Light Dark System)
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    # Scaling Menu(80% 90% 100% 110% 120%)
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    # Homepage Definition
    def homepage(self):
        frame = customtkinter.CTkFrame(self, corner_radius=10)
        frame.grid_columnconfigure((0), weight=1)
        frame.grid_rowconfigure((0), weight=1)
        frame.grid(row=0, column=1, padx=(10, 20), pady=(20, 20), rowspan=4, columnspan=3, sticky="nsew")
        banner = customtkinter.CTkImage(light_image=Image.open("light_bg.png"), dark_image=Image.open("dark_bg.png"),
                                        size=(900, 540))
        banner_label = customtkinter.CTkLabel(frame, text="", image=banner)
        banner_label.grid(row=0, column=0, padx=20, pady=(20, 20), sticky="nsew")

    # Two File Comparison Page
    def two_file_page(self):
        frame = customtkinter.CTkFrame(self, corner_radius=10)
        frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        frame.grid(row=0, column=1, padx=(10, 20), pady=(20, 20), rowspan=4, columnspan=3, sticky="nsew")
        label = customtkinter.CTkLabel(frame, text_color=("black", "white"), text="CHOOSE TWO FILES",
                                      font=customtkinter.CTkFont(size=20, weight="bold"))
        label.grid(row=0, column=0, columnspan=5, padx=20, pady=(20, 20), sticky="ew")

        button_1_text = tk.StringVar()
        button_1_text.set("CHOOSE FILE 1")
        button_1 = customtkinter.CTkButton(frame, text_color=("black", "white"), textvariable=button_1_text,
                                           command=lambda: open_file1(button_1_text))
        button_1.grid(row=1, column=1, padx=20, pady=20, sticky="ew")

        button_2_text = tk.StringVar()
        button_2_text.set("CHOOSE FILE 2")
        button_2 = customtkinter.CTkButton(frame, text_color=("black", "white"), textvariable=button_2_text,
                                           command=lambda: open_file2(button_2_text))
        button_2.grid(row=1, column=3, padx=20, pady=20, sticky="ew")

        button_3 = customtkinter.CTkButton(frame, text_color=("black", "white"), text="CHECK PLAGIARISM",
                                           command=lambda: two_file_compare_result(textbox))
        button_3.grid(row=2, column=2, padx=20, pady=20, sticky="ew")

        textbox = customtkinter.CTkTextbox(frame)
        textbox.grid(row=3, column=0, columnspan=5, rowspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

    # Multiple File Compare Page
    def multiple_file_page(self):
        frame = customtkinter.CTkFrame(self, width=500, corner_radius=10)
        frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        frame.grid(row=0, column=1, padx=(10, 20), pady=(20, 20), rowspan=4, columnspan=3, sticky="nsew")

        frame2 = customtkinter.CTkFrame(frame)
        frame2.grid_columnconfigure((0), weight=3)
        frame2.grid_columnconfigure((1, 2), weight=1)
        frame2.grid_columnconfigure((3), weight=2)
        frame2.grid_columnconfigure((4), weight=5)
        frame2.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)
        frame2.grid(row=1, column=0, columnspan=5, rowspan=3, padx=20, pady=20, sticky="nsew")

        button_text = tk.StringVar()
        button_text.set("CHOOSE FILES")
        button_1 = customtkinter.CTkButton(frame, text_color=("black", "white"), textvariable=button_text,
                                           command=lambda: open_files(button_text))
        button_1.grid(row=0, column=1, padx=20, pady=20, sticky="ew")

        button_2 = customtkinter.CTkButton(frame, text_color=("black", "white"), text="Check Plagiarism",
                                           command=lambda: multiple_comp_table(frame2))
        button_2.grid(row=0, column=3, padx=20, pady=20, sticky="ew")

        button_3 = customtkinter.CTkButton(frame, text_color=("black", "white"), text="Save Report",
                                           command=lambda: save_report())
        button_3.grid(row=4, column=3, padx=20, pady=20, sticky="ew")

        button_4 = customtkinter.CTkButton(frame, text_color=("black", "white"), text="View Complete Report",
                                           command=lambda: detailed_report())
        button_4.grid(row=4, column=1, padx=20, pady=20, sticky="ew")

def detailed_report():
    report = tk.Toplevel()
    report.title("Detailed Report")
    report.geometry("1100x580")

    columns = ('No', 'File1', 'File2', 'Similarity')

    tree = tk.ttk.Treeview(report, columns=columns, show='headings')

    # define headings
    tree.heading('No', text='Sr No')
    tree.heading('File1', text='File 1 Name')
    tree.heading('File2', text='File 2 Name')
    tree.heading('Similarity', text='Similarity Percentage')

    global data_list

    # add data to the treeview
    for data in data_list:
        tree.insert('', tk.END, values=data)

    tree.pack(expand=True, fill='both')

    report.mainloop()
