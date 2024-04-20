import tkinter as tk
from tkinter.filedialog import askopenfile

import customtkinter

from python.utils.data_comparation import *


class TwoFilePage(customtkinter.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.file_texts = ["", ""]  # Variable for two files text
        self.files_text = []  # Variable to store multiple file text

        self.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)

        label = customtkinter.CTkLabel(self, text_color=("black", "white"), text="CHOOSE TWO FILES",
                                       font=customtkinter.CTkFont(size=20, weight="bold"))
        label.grid(row=0, column=0, columnspan=5, padx=20, pady=(20, 20), sticky="ew")

        self.button_1_text = tk.StringVar()
        self.button_1_text.set("CHOOSE FILE 1")
        button_1 = customtkinter.CTkButton(self, text_color=("black", "white"), textvariable=self.button_1_text,
                                           command=self.open_file1)
        button_1.grid(row=1, column=1, padx=20, pady=20, sticky="ew")

        self.button_2_text = tk.StringVar()
        self.button_2_text.set("CHOOSE FILE 2")
        button_2 = customtkinter.CTkButton(self, text_color=("black", "white"), textvariable=self.button_2_text,
                                           command=self.open_file2)
        button_2.grid(row=1, column=3, padx=20, pady=20, sticky="ew")

        button_3 = customtkinter.CTkButton(self, text_color=("black", "white"), text="CHECK PLAGIARISM",
                                           command=self.two_file_compare_result)
        button_3.grid(row=2, column=2, padx=20, pady=20, sticky="ew")

        self.textbox = customtkinter.CTkTextbox(self)
        self.textbox.grid(row=3, column=0, columnspan=5, rowspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")


    def open_file1(self):
        self.button_1_text.set("Loading..")
        file1 = askopenfile(mode='r', title="Choose a File", filetypes=[
            ("All files", "*"),
            ("text file", "*.txt"),
            ("java File", "*.java"),
            ("python file", "*.py"),
            ("C file", "*.c"),
            ("C++ file", "*.cpp")
        ])
        if file1:
            self.button_1_text.set(os.path.basename(file1.name))
            self.file_texts[0] = file1.read()
        else:
            self.button_1_text.set("Choose File 1")


    def open_file2(self):
        self.button_2_text.set("Loading..")
        file2 = askopenfile(mode='r', title="Choose a File", filetypes=[
            ("All files", "*"),
            ("text file", "*.txt"),
            ("java File", "*.java"),
            ("python file", "*.py"),
            ("C file", "*.c"),
            ("C++ file", "*.cpp")
        ])
        if file2:
            self.button_2_text.set(os.path.basename(file2.name))
            self.file_texts[1] = file2.read()
        else:
            self.button_2_text.set("Choose File 2")


    def two_file_compare_result(self):
        self.textbox.delete("1.0", "end")
        similarity = jaccard_similarity(self.file_texts[0], self.file_texts[1])
        self.textbox.insert("1.0", "Similarity Percentage is : " + str(similarity))
        self.textbox.insert("1.0", "\n\nDuplicate Sentences Are:\n")
