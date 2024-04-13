#######################################--PLAGIARISM CHECKER--##############################################

#######################################--IMPORTING LIBRARIES--############################################

import tkinter as tk
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfile, askopenfiles, asksaveasfile, asksaveasfilename
from openpyxl import Workbook
import os
import customtkinter

from PIL import Image
from data_comparation import *
# from gui import App



#######################################--DECLARING GLOBAL VARIABLES--#####################################

# Variables for two files text
file_text = ["", ""]

# Variable for multiple files
files = []

# Variable to store multiple file text
files_text = []

# Variable to store duplicate sentences
duplicates = []

# Variable to store details of file and corresponding percentage
data_list = []

#######################################--GRAPHICAL USER INTERFACE--#######################################

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
        banner = customtkinter.CTkImage(light_image=Image.open("light_bg.png"), dark_image=Image.open("dark_bg.png"), size=(900, 540))
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
        frame2.grid_columnconfigure((0), weight=1)
        frame2.grid_columnconfigure((1, 2), weight=1)
        frame2.grid_columnconfigure((3), weight=1)
        frame2.grid_columnconfigure((4), weight=1)
        frame2.grid_columnconfigure((5), weight=1)
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

##############################################--FUNCTIONS--###############################################

def plagiarism_percentage(text1, text2):
    sentences1 = text1.split("\n")
    sentences2 = text2.split("\n")
    count = 0
    for x in sentences1:
        for y in sentences2:
            if x == y and x != "":
                count += len(x)
                break
    similarity = count * 100 / (len(text1) - len(sentences1))
    return int(limit(similarity))


def duplicate_sentences(text1, text2):
    global duplicates
    duplicates.clear()
    for x in text1.split("\n"):
        x = x.strip()
    for x in text2.split("\n"):
        x = x.strip()
    for x in text1.split("\n"):
        for y in text2.split("\n"):
            if x == y:
                duplicates.append(x)
                break


def open_file1(button_text):
    button_text.set("Loading..")
    file1 = askopenfile(mode='r', title="Choose a File", filetypes=[
        ("All files", "*"),
        ("text file", "*.txt"),
        ("java File", "*.java"),
        ("python file", "*.py"),
        ("C file", "*.c"),
        ("C++ file", "*.cpp")
    ])
    if file1:
        button_text.set(os.path.basename(file1.name))
        global file_text
        file_text[0] = file1.read()
    else:
        button_text.set("Choose File 1")


def open_file2(button_text):
    button_text.set("Loading..")
    file2 = askopenfile(mode='r', title="Choose a File", filetypes=[
        ("All files", "*"),
        ("text file", "*.txt"),
        ("java File", "*.java"),
        ("python file", "*.py"),
        ("C file", "*.c"),
        ("C++ file", "*.cpp")
    ])
    if file2:
        button_text.set(os.path.basename(file2.name))
        global file_text
        file_text[1] = file2.read()
    else:
        button_text.set("Choose File 2")


def two_file_compare_result(textbox):
    textbox.delete("1.0", "end")
    global file_text
    global duplicates
    similarity = plagiarism_percentage(file_text[0], file_text[1])
    duplicate_sentences(file_text[0], file_text[1])
    for x in range(len(duplicates) - 1, 0, -1):
        if duplicates[x] != "":
            textbox.insert("1.0", duplicates[x] + "\n")
    textbox.insert("1.0", "\n\nDuplicate Sentences Are:\n")
    textbox.insert("1.0", "Similarity Percentage is : " + str(similarity))


def multiple_compare_result(textbox):
    textbox.delete("1.0", "end")
    global files
    global files_text
    for x in files_text:
        a = files_text.index(x)
        for y in files_text:
            b = files_text.index(y)
            similarity = plagiarism_percentage(x, y)
            file_name1 = os.path.basename(files[a].name)
            file_name2 = os.path.basename(files[b].name)
            textbox.insert("1.0", file_name1 + "\t and \t" + file_name2 + "\t  -  \t" + str(similarity) + "\n")


def save_report():
    global data_list
    wb = Workbook()
    ws = wb.active
    for row in data_list:
        ws.append(row)
    wb.save('Report.xlsx')


def limit(k):
    if k > 100:
        return 100
    else:
        return k



files_with_uknown_data = {}

def open_files(button_text):
    button_text.set("Loading..")
    global files
    files.clear()
    files = askopenfiles(mode='r', title="Choose Multiple Files", filetypes=[
        ("All files", "*"),
        ("text file", "*.txt"),
        ("java File", "*.java"),
        ("python file", "*.py"),
        ("C file", "*.c"),
        ("C++ file", "*.cpp")
    ])
    
    if files:
        button_text.set((str(len(files)) + " Files Selected"))
        files_with_uknown_data.clear()
        for file in files:
            file_name = file.name.split('/')[-1]  # Extract file name from the full path
            files_with_uknown_data[file_name] = file.read()
    else:
        button_text.set("CHOOSE FILES")




def multiple_comp_table(frame):
    data_list.clear()
    data_list.append(("Nr", "File", "Candidate", "Candidate File", "Similarity"))
    for widget in frame.winfo_children():
        widget.destroy()
        
    data_comparation = collect_data_comparation(files_with_uknown_data)

    for file_name, file_text in files_with_uknown_data.items():
        matches = best_matches(data_comparation, file_name, 1)
        for i, (candidate, candidateFileName, percent) in enumerate(matches, start=1):
            data_list.append((i, file_name, candidate, candidateFileName, percent))

    rows = len(data_list)
    cols = 5
    for i in range(rows):
        for j in range(cols):
            table = customtkinter.CTkEntry(frame, width=500, font=('Arial', 16))
            table.grid(row=i, column=j, sticky="nsew")
            table.insert(tk.END, data_list[i][j])
    display_best_matches_results(files_with_uknown_data, data_comparation, 5)
            
            
            
if __name__ == "__main__":
    app = App()
    app.mainloop()
