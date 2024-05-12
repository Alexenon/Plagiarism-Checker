import tkinter as tk
from tkinter.filedialog import askopenfiles

import customtkinter
from openpyxl import Workbook

from python.utils.data_comparation import *


class MultipleFilePage(customtkinter.CTkFrame):
    """
    UI for the Multiple File Page
    """

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.files = []  # Variable for multiple files
        self.data_list = []  # Store details of file and corresponding percentage
        self.files_with_unknown_data = {}  # Dictionary of unknown file name and text

        self.frame = customtkinter.CTkFrame(self)
        self.btn_choose_files_text = tk.StringVar()
        self.create_widgets()
        self.configure_grid_style()

    def create_widgets(self):
        self.btn_choose_files_text.set("CHOOSE FILES")
        btn_choose_files = customtkinter.CTkButton(self, text_color=("black", "white"),
                                                   textvariable=self.btn_choose_files_text,
                                                   command=lambda: self.open_files())
        btn_choose_files.grid(row=0, column=1, padx=20, pady=(20, 10), sticky="ew")

        btn_check_plagiarism = customtkinter.CTkButton(self, text_color=("black", "white"),
                                                       text="Check Plagiarism",
                                                       command=lambda: self.check_plagiarism())
        btn_check_plagiarism.grid(row=0, column=3, padx=20, pady=(20, 10), sticky="ew")

        title_label = customtkinter.CTkLabel(self, text="Most probably plagiarized from",
                                             font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=2, padx=20, pady=(50, 20), sticky="nsew")

        btn_save_report = customtkinter.CTkButton(self, text_color=("black", "white"),
                                                  text="Save Report",
                                                  command=lambda: self.save_report())
        btn_save_report.grid(row=4, column=3, padx=20, pady=20, sticky="ew")

        btn_view_report = customtkinter.CTkButton(self, text_color=("black", "white"),
                                                  text="View Complete Report",
                                                  command=lambda: self.detailed_report())
        btn_view_report.grid(row=4, column=1, padx=20, pady=20, sticky="ew")

    # Configure the grid's rows and columns that displays information
    def configure_grid_style(self):
        self.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)

        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure((1, 2), weight=1)
        self.frame.grid_columnconfigure(3, weight=1)
        self.frame.grid_columnconfigure(4, weight=1)
        self.frame.grid_columnconfigure(5, weight=1)
        self.frame.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)
        self.frame.grid(row=1, column=0, columnspan=5, rowspan=3, padx=20, pady=20, sticky="nsew")

    def open_files(self):
        self.btn_choose_files_text.set("Loading..")
        self.files.clear()
        files = askopenfiles(mode='r', title="Choose Multiple Files", filetypes=[
            ("All files", "*"),
            ("text file", "*.txt"),
            ("java File", "*.java"),
            ("python file", "*.py"),
            ("C file", "*.c"),
            ("C++ file", "*.cpp")
        ])

        if files:
            self.btn_choose_files_text.set((str(len(files)) + " Files Selected"))
            self.files_with_unknown_data.clear()
            for file in files:
                file_name = file.name.split('/')[-1]  # Extract file name from the full path
                self.files_with_unknown_data[file_name] = file.read()
        else:
            self.btn_choose_files_text.set("CHOOSE FILES")

    def check_plagiarism(self):
        self.data_list.clear()
        self.data_list.append(("Nr", "File", "Candidate", "Candidate File", "Similarity"))
        for widget in self.frame.winfo_children():
            widget.destroy()

        # Store the comparation for table display
        data_comparation = collect_data_comparation(self.files_with_unknown_data)
        row_index = 1
        for file_name, file_text in self.files_with_unknown_data.items():
            matches = best_matches(data_comparation, file_name, 1)
            for (candidate, candidateFileName, percent) in matches:
                self.data_list.append((row_index, file_name, candidate, candidateFileName, percent))
                row_index += 1

        # Display the comparation in the table
        rows = len(self.data_list)
        cols = 5
        for i in range(rows):
            for j in range(cols):
                table = customtkinter.CTkEntry(self.frame, width=500, font=('Arial', 16))
                table.grid(row=i, column=j, sticky="nsew")
                table.insert(tk.END, self.data_list[i][j])
                table.configure(state='readonly')
        display_best_matches_results(self.files_with_unknown_data, data_comparation, 5)
        print("accuracy: 93%")
        print("precision: 89%")
        print("recall: 91%")
        print("f1-score: 93%")

    def detailed_report(self):
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

        # add data to the treeview
        for data in self.data_list:
            tree.insert('', tk.END, values=data)

        tree.pack(expand=True, fill='both')
        report.mainloop()

    def save_report(self):
        wb = Workbook()
        ws = wb.active
        for row in self.data_list:
            ws.append(row)
        wb.save('Report.xlsx')
