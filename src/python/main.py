#######################################--PLAGIARISM CHECKER--##############################################

#######################################--IMPORTING LIBRARIES--############################################

import customtkinter
from PIL import Image

from data_comparation import *
from python.pages.multiple_files_page import MultipleFilePage
from python.pages.two_file_page import TwoFilePage

#######################################--GRAPHICAL USER INTERFACE--#######################################

# Setting Color Theme
customtkinter.set_appearance_mode("Dark")  # Modes: "Dark"(standard), "System", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


# Create App Object
# noinspection PyMethodMayBeStatic
class App(customtkinter.CTk):
    """
    The UI for the entire Application
    """

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
                                                        text="COMPARE TWO FILES", command=self.display_two_file_page)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text_color=("black", "white"),
                                                        text="MULTIPLE COMPARE",
                                                        command=self.display_multiple_file_page)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text_color=("black", "white"),
                                                            text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_option_menu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                       text_color=("black", "white"),
                                                                       values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_option_menu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text_color=("black", "white"),
                                                    text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_option_menu = customtkinter.CTkOptionMenu(self.sidebar_frame, text_color=("black", "white"),
                                                               values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_option_menu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # Set Default values
        self.appearance_mode_option_menu.set("Dark")
        self.scaling_option_menu.set("100%")
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
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid(row=0, column=1, padx=(10, 20), pady=(20, 20), rowspan=4, columnspan=3, sticky="nsew")
        banner = customtkinter.CTkImage(light_image=Image.open(os.path.join("src", "resources", "light_bg.png")),
                                        dark_image=Image.open(os.path.join("src", "resources", "dark_bg.png")),
                                        size=(900, 540))
        banner_label = customtkinter.CTkLabel(frame, text="", image=banner)
        banner_label.grid(row=0, column=0, padx=20, pady=(20, 20), sticky="nsew")

    # Two File Comparison Page
    def display_two_file_page(self):
        frame = TwoFilePage(self)
        frame.grid(row=0, column=1, padx=(10, 20), pady=(20, 20), rowspan=4, columnspan=3, sticky="nsew")

    def display_multiple_file_page(self):
        multiple_file_page = MultipleFilePage(self)
        multiple_file_page.grid(row=0, column=1, padx=(10, 20), pady=(20, 20), rowspan=4, columnspan=3, sticky="nsew")


##############################################--FUNCTIONS--###############################################


if __name__ == "__main__":
    app = App()
    app.mainloop()
