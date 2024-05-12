import tkinter as tk
import customtkinter as ctk
from tksheet import Sheet
from estimator import Estimator

info = """Aby wprowadzić dane zaznacz komórkę z odpowienim levelem oraz poziomem ulepszenia,
następnie kliknij odpowiedni przycisk na klawiaturze
    1 - ulepszanie pomyślne
    2 - ulepszanie niepomyślne
Po prawej wyświeli się estymowany proecnt szansy na ulepszenia dla danego poziomu
W górnym panelu jest możliwość wybrania dodatkowego procentu podczas ulepszania (0%, 10%, 15%)"""

class UI:
    def __init__(self, estimator: Estimator):
        self.estimator = estimator

        root = ctk.CTk()
        self.root = root

        root.geometry("1280x720")
        root.title("Forge percent")
        root._set_appearance_mode("dark")

        self.percent = tk.IntVar()
        self.__create_top_panel(root)
        self.__create_sheet(root)

        root.bind("<KeyRelease>", self.__key_pressed)

    def run(self):
        self.root.mainloop()

    def __show_info(self):
        top = tk.Toplevel(self.root, width=1000, height=200)
        self.root.eval(f'tk::PlaceWindow {str(top)} center')
        ctk.CTkLabel(top, text=info, justify="left", text_color="black").place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def __create_sheet(self, root):
        sheet = Sheet(root, empty_horizontal=0,
                headers=['+1', '+2', '+3', '+4', '+5', '+6', '+7', '+8', '+9', '+1%', '+2%', '+3%', '+4%', '+5%', '+6%', '+7%', '+8%', '+9%'])
        sheet.pack(fill=tk.BOTH, expand=True)
        sheet.enable_bindings("single_select")

        data = []
        for row in range(120):
            data.append(['+1', '+2', '+3', '+4', '+5', '+6', '+7',
                        '+8', '+9'] + self.estimator.estimated[row])

        sheet.set_sheet_data(data)
        sheet.set_options(auto_resize_columns=50)

        self.sheet = sheet

    def __key_pressed(self, event):
        if event.keysym not in ['1', '2']:
            return
        if not len(self.sheet.get_selected_cells()):
            return

        selected_sheet = self.sheet.get_selected_cells().pop()
        row = selected_sheet[0]
        col = selected_sheet[1]
        if col > 8:
            return

        self.estimator.update(row, col, self.percent.get(), event.keysym == '1')
        self.sheet[row, col + 9].data = self.estimator.estimated[row][col]

    def __create_top_panel(self, root):
        # Create a frame for the top panel
        top_panel = ctk.CTkFrame(root)
        top_panel.pack(side=tk.TOP, fill=tk.X)

        # Add a label to the top panel
        check = ctk.CTkRadioButton(top_panel, text="0%", value=0, variable=self.percent)
        check.select()
        check.pack(side="left", padx=10, pady=10)
        check = ctk.CTkRadioButton(top_panel, text="10%", value=10, variable=self.percent)
        check.pack(side="left", padx=10, pady=10)
        check = ctk.CTkRadioButton(top_panel, text="15%", value=15, variable=self.percent)
        check.pack(side="left", padx=10, pady=10)

        info_button = ctk.CTkButton(top_panel, command=self.__show_info, text="Info")
        info_button.pack(side="right")
    