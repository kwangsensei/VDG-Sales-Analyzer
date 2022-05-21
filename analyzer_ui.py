import seaborn as sns
import tkinter as tk
import matplotlib
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from analyzer import Analyzer
from tkinter import ttk


matplotlib.use("TkAgg")


class AnalyzerUI(tk.Tk):
    def __init__(self, analyzer: Analyzer):
        """Initialize of the AnalyzerUI Class."""
        super().__init__()
        self.analyzer = analyzer
        self.init_components()
        self.state = self.plot_graph
        
    def init_components(self):
        """Initialize components of UI."""
        self.title("Video Game Sales Analyzer")
        self.build_labelframe()
        self.build_comboboxs()
        self.build_buttons()
        self.build_progress_bar()
        self.figure = Figure(figsize=(7, 5))
        self.axes = self.figure.add_subplot()
        self.figure_canvas = FigureCanvasTkAgg(self.figure, self)
        self.figure_canvas.get_tk_widget().grid(row=0, column=2)

    def build_labelframe(self):
        """Create LabelFrame."""
        self.labelframe = ttk.LabelFrame(self, labelanchor="w")
        self.labelframe.grid(row=0, column=0, sticky="n")

    def build_comboboxs(self):
        """Create Comboboxs."""
        self.year_cbb_var = tk.StringVar(value="Select Year")
        self.year_cbb_var.trace("w", lambda *args: self.plot_graph())
        self.year_cbb = ttk.Combobox(
            self.labelframe,
            textvariable=self.year_cbb_var, 
            values=list(range(2000, 2011)), 
            state="readonly"
            )
        self.publisher_cbb_var = tk.StringVar(value="Select Publisher")
        self.publisher_cbb_var.trace("w", lambda *args: self.plot_graph())
        self.publisher_cbb = ttk.Combobox(
            self.labelframe,
            textvariable=self.publisher_cbb_var, 
            values=list(self.analyzer.VDG_df["Publisher"].unique()), 
            state="readonly"
            )
        self.country_cbb_var = tk.StringVar(value="Global_Sales")
        self.country_cbb_var.trace("w", lambda *args: self.plot_graph())
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
        """Create Buttons."""
        self.reset_all_button = ttk.Button(
            self.labelframe, 
            text="Reset All"
            )
        self.reset_all_button.bind("<Button-1>", self.reset_all_filter)    
        self.reset_year_button = ttk.Button(
            self.labelframe, 
            text="Reset"
            )
        self.reset_year_button.bind("<Button-1>", self.reset_year_filter) 
        self.reset_publisher_button = ttk.Button(
            self.labelframe, 
            text="Reset"
            )
        self.reset_publisher_button.bind("<Button-1>", self.reset_publisher_filter)
        self.reset_country_button = ttk.Button(
            self.labelframe,
            text="Reset"
            )
        self.reset_country_button.bind("<Button-1>", self.reset_country_filter)
        self.show_button = ttk.Button(
            self.labelframe, 
            text="Show"
            )
        self.show_button.bind("<Button-1>", self.show_graph)

        self.reset_all_button.grid(row=5, column=0, sticky="w")
        self.reset_year_button.grid(row=1, column=1)
        self.reset_publisher_button.grid(row=2, column=1)
        self.reset_country_button.grid(row=3, column=1)
        self.show_button.grid(row=5, column=1)

    def build_progress_bar(self):
        """Create Progress Bar."""
        self.pro_bar = ttk.Progressbar(
            self.labelframe,
            orient="horizontal",
            mode="determinate",
            length=142
            )
        self.pro_bar.grid(row=4, column=0)

    def reset_all_filter(self, event):
        """
        Clear all comboboxs.
        Observer Pattern.
        """
        self.axes.clear()
        self.figure.canvas.draw()
        notice = event.widget["text"]
        print(f"{notice} All button pressed")
        self.year_cbb.set("Select Year")
        self.publisher_cbb.set("Select Publisher")
        self.country_cbb.set("Global_Sales")
        self.pro_bar["value"] -= self.pro_bar["value"]

    def reset_year_filter(self, event):
        """
        Clear year comboboxs.
        Observer Pattern.
        """
        self.axes.clear()
        self.figure.canvas.draw()
        notice = event.widget["text"]
        print(f"{notice} year button pressed")
        self.year_cbb.set("Select Year")
        self.pro_bar["value"] -= self.pro_bar["value"]

    def reset_publisher_filter(self, event):
        """
        Clear publisher comboboxs.
        Observer Pattern.
        """
        self.axes.clear()
        self.figure.canvas.draw()
        notice = event.widget["text"]
        print(f"{notice} publisher button pressed")
        self.publisher_cbb.set("Select Publisher")
        self.pro_bar["value"] -= self.pro_bar["value"]

    def reset_country_filter(self, event):
        """
        Clear country comboboxs.
        Observer Pattern.
        """
        self.axes.clear()
        self.figure.canvas.draw()
        notice = event.widget["text"]
        print(f"{notice} country button pressed")
        self.country_cbb.set("Global_Sales")
        self.pro_bar["value"] -= self.pro_bar["value"]

    def plot_graph(self):
        """
        Get value(s) from the comboboxs and accessing the dataframe.
        Plotting graph from dataframe that filtered by value(s) from combobox.
        """
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
        self.axes.tick_params(axis="x", rotation=90, labelsize=5)
        if self.publisher_cbb_var.get() in self.analyzer.VDG_df["Publisher"].unique():
            try:
                for bar in self.axes.patches:
                    bar.set_color("white")
                df_by_publisher = self.analyzer.by_publisher(year, publisher)
                sns.barplot(
                    x=df_by_publisher["Name"] + " (" + df_by_publisher["Platform"] + ")", 
                    y=df_by_publisher["Global_Sales"], 
                    ax=self.axes
                    )
                self.axes.set_title(f"Top 10 {publisher} Games Global Sales {year}")
            except:
                if len(df_by_publisher) == 0:
                    print(f"No games were published by {publisher} in {year}.")
        if self.country_cbb_var.get() in country_list:
            self.axes.clear()
            sns.barplot(
                x=df_by_year["Name"] + " (" + df_by_year["Platform"] + ")", 
                y=df_by_year[country],
                ax=self.axes
                )
            self.axes.set_title(f"Top 50 Games {country} {year}")
        if self.country_cbb_var.get() in country_list and self.publisher_cbb_var.get() in self.analyzer.VDG_df["Publisher"].unique():
            try:
                for bar in self.axes.patches:
                    bar.set_color("white")
                df_by_publisher = self.analyzer.by_publisher(year, publisher)
                sns.barplot(
                    x=df_by_publisher["Name"] + " (" + df_by_publisher["Platform"] + ")", 
                    y=df_by_publisher[country], 
                    ax=self.axes
                    )
                self.axes.set_title(f"Top 10 {publisher} Games {country} {year}")
            except:
                if len(df_by_publisher) == 0:
                    print(f"No games were published by {publisher} in {year}.")

    def show_graph(self, event):
        """
        Show the graph to the user.
        Observer Pattern.
        """
        while self.pro_bar["value"] != 100:
            self.update_idletasks() 
            self.pro_bar["value"] += 5
            time.sleep(0.1)
        self.figure.canvas.draw()
        self.pro_bar["value"] -= self.pro_bar["value"]

    def state_pattern(self, cbb_state, event):
        """State Pattern."""
        if cbb_state == self.year_cbb:
            self.state = self.plot_graph
        if cbb_state == self.year_cbb and self.publisher_cbb:
            self.state = self.plot_graph
        if cbb_state == self.year_cbb and self.country_cbb:
            self.state = self.plot_graph
        if cbb_state == self.year_cbb and self.publisher_cbb and self.country_cbb:
            self.state = self.plot_graph
        self.state()

    def run(self):
        """Start the app."""
        self.mainloop()
