#######################################--PLAGIARISM CHECKER--##############################################

#######################################--IMPORTING LIBRARIES--############################################

import tkinter as tk
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfile, askopenfiles, asksaveasfile, asksaveasfilename
from openpyxl import Workbook
import os
import customtkinter

from data_comparation import *
from gui import App



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


def open_files(button_text):
    button_text.set("Loading..")
    global files
    global files_text
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
        files_text.clear()
        for x in files:
            files_text.append(x.read())
    else:
        button_text.set("CHOOSE FILES")


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


def multiple_comp_table(frame):
    global files
    global files_text
    k = 1
    data_list.clear()
    data_list.append(("No", "File 1", "File 2", "Similarity"))
    for widget in frame.winfo_children():
        widget.destroy()
    for x in files_text:
        a = files_text.index(x)
        for y in files_text:
            b = files_text.index(y)
            similarity = plagiarism_percentage(x, y)
            file_name1 = os.path.basename(files[a].name)
            file_name2 = os.path.basename(files[b].name)
            data_list.append((k, file_name1, file_name2, similarity))
            k += 1

    columns = min(len(data_list), 10)
    for i in range(columns):
        for j in range(4):
            e = customtkinter.CTkEntry(frame, width=500, font=('Arial', 16))
            e.grid(row=i, column=j, sticky="nsew")
            e.insert(tk.END, data_list[i][j])


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

if __name__ == "__main__":
    app = App()
    app.mainloop()

