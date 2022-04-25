from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from analyzer import Analyzer
from tkinter import ttk
import seaborn as sns
import tkinter as tk
import matplotlib
import time


matplotlib.use("TkAgg")


class AnalyzerUI(tk.Tk):
    def __init__(self, analyzer: Analyzer):
        super().__init__()
        self.analyzer = analyzer
        self.init_components()
        
    def init_components(self):
        self.title("Video Game Sales Analyzer")
        self.build_labelframe()
        self.build_comboboxs()
        self.build_buttons()
        self.figure = Figure(figsize=(7, 5))
        self.axes = self.figure.add_subplot()
        self.figure_canvas = FigureCanvasTkAgg(self.figure, self)
        self.figure_canvas.get_tk_widget().grid(row=0, column=2)

    def build_labelframe(self):
        self.labelframe = ttk.LabelFrame(self, labelanchor="w")
        self.labelframe.grid(row=0, column=0)

    def build_comboboxs(self):
        self.year_cbb_var = tk.StringVar(value="Select Year")
        self.year_cbb_var.trace("w", lambda *args: self.filter())
        self.year_cbb = ttk.Combobox(
            self.labelframe,
            textvariable=self.year_cbb_var, 
            values=list(range(2000, 2011)), 
            state="readonly"
            )
        self.publisher_cbb_var = tk.StringVar(value="Select Publisher")
        self.publisher_cbb_var.trace("w", lambda *args: self.filter())
        self.publisher_cbb = ttk.Combobox(
            self.labelframe,
            textvariable=self.publisher_cbb_var, 
            values=list(self.analyzer.VDG_df["Publisher"].unique()), 
            state="readonly"
            )
        self.country_cbb_var = tk.StringVar(value="Select Country")
        self.country_cbb_var.trace("w", lambda *args: self.filter())
        self.country_cbb = ttk.Combobox(
            self.labelframe,
            textvariable=self.country_cbb_var, 
            values=list([
                        "NA_Sales", 
                        "EU_Sales", 
                        "JP_Sales", 
                        "Other_Sales"
                        ]),
            state="readonly"
            )
        self.year_cbb.grid(row=1, column=0)
        self.publisher_cbb.grid(row=2, column=0)    
        self.country_cbb.grid(row=3, column=0)

    def build_buttons(self):
        self.pro_bar = ttk.Progressbar(
            self.labelframe,
            orient="horizontal",
            mode="determinate",
            length=142
            )
        self.pro_bar.grid(row=4, column=0)
        self.reset_all_button = tk.Button(
            self.labelframe, 
            text="Reset All",
            command=self.reset_all_filter
            )
        self.reset_year_button = tk.Button(
            self.labelframe, 
            text="Reset", 
            command=self.reset_year_filter
            )
        self.reset_publisher_button = tk.Button(
            self.labelframe, 
            text="Reset", 
            command=self.reset_publisher_filter
            )
        self.reset_country_button = tk.Button(
            self.labelframe, 
            text="Reset", 
            command=self.reset_country_filter
            )    
        self.show_button = tk.Button(
            self.labelframe, 
            text="Show", 
            command=self.show_graph
            )
        self.reset_all_button.grid(row=5, column=0, sticky="w")
        self.reset_year_button.grid(row=1, column=1)
        self.reset_publisher_button.grid(row=2, column=1)
        self.reset_country_button.grid(row=3, column=1)
        self.show_button.grid(row=5, column=1)

    def filter(self):
        country_list = list([
                            "NA_Sales", 
                            "EU_Sales", 
                            "JP_Sales", 
                            "Other_Sales"
                            ])
        year = int(self.year_cbb_var.get())
        publisher = str(self.publisher_cbb_var.get())
        country = str(self.country_cbb_var.get())

        self.axes.clear()
        df_by_year = self.analyzer.by_year(year)
        sns.barplot(
            x=df_by_year["Name"] + " (" + df_by_year["Platform"] + ")", 
            y=df_by_year["Global_Sales"],
            ax=self.axes
            )
        self.axes.set_title(f"Top 50 Games Global Sales {year}")
        self.axes.set_xlabel("Name (Platform)")
        self.axes.set_ylabel("Sales (Million Units)")
        self.axes.tick_params(axis="x", rotation=90, labelsize=8)

        if self.publisher_cbb_var.get() in self.analyzer.VDG_df["Publisher"].unique():
            for bar in self.axes.patches:
                bar.set_color("white")
            df_by_publisher = self.analyzer.by_publisher(year, publisher)
            sns.barplot(
                x=df_by_publisher["Name"] + " (" + df_by_publisher["Platform"] + ")", 
                y=df_by_publisher["Global_Sales"], 
                ax=self.axes
                )
            self.axes.set_title(f"Top 10 {publisher} Games Global Sales {year}")

        if self.country_cbb_var.get() in country_list:
            self.axes.clear()
            sns.barplot(
                x=df_by_year["Name"] + " (" + df_by_year["Platform"] + ")", 
                y=df_by_year[country],
                ax=self.axes
                )
            self.axes.set_title(f"Top 50 Games {country} {year}")

        if self.country_cbb_var.get() in country_list and self.publisher_cbb_var.get() in self.analyzer.VDG_df["Publisher"].unique():
            for bar in self.axes.patches:
                bar.set_color("white")
            df_by_publisher = self.analyzer.by_publisher(year, publisher)
            sns.barplot(
                x=df_by_publisher["Name"] + " (" + df_by_publisher["Platform"] + ")", 
                y=df_by_publisher[country], 
                ax=self.axes
                )
            self.axes.set_title(f"Top {publisher} Games {country} {year}")

    def reset_all_filter(self):
        self.axes.clear()
        self.figure.canvas.draw()
        self.year_cbb.set("Select Year")
        self.publisher_cbb.set("Select Publisher")
        self.country_cbb.set("Select Country")
        self.pro_bar["value"] -= self.pro_bar["value"]

    def reset_year_filter(self):
        self.axes.clear()
        self.figure.canvas.draw()
        self.year_cbb.set("Select Year")
        self.pro_bar["value"] -= self.pro_bar["value"]

    def reset_publisher_filter(self):
        self.axes.clear()
        self.figure.canvas.draw()
        self.publisher_cbb.set("Select Publisher")
        self.pro_bar["value"] -= self.pro_bar["value"]

    def reset_country_filter(self):
        self.axes.clear()
        self.figure.canvas.draw()
        self.country_cbb.set("Select Country")
        self.pro_bar["value"] -= self.pro_bar["value"]

    def show_graph(self):
        while self.pro_bar["value"] != 100:
            self.update_idletasks() 
            self.pro_bar["value"] += 5
            time.sleep(0.1)
        self.figure.canvas.draw()
        self.pro_bar["value"] -= self.pro_bar["value"]

    def run(self):
        # start the app
        self.mainloop()
