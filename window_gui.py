"""
This Window UI module is responsible for display
the graph and user interface.
"""
import tkinter as tk
import seaborn as sns
import matplotlib as plt
from tkinter import ttk
from analyzer_control import AnalyzerControl
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Set the backend to TkAgg
plt.use("TkAgg")


class WindowGUI(tk.Tk):
    """Define layout of UI and create its components."""
    def __init__(self):
        super().__init__()
        # Facade pattern control
        self.control = AnalyzerControl()

        # Set window title
        self.title("Video Game Sales Data Analyzer")

        # Create Year Combobox
        self.year_combobox()

        # Create Publisher Combobox
        self.publisher_combobox()

        # Create Zone Combobox
        self.zone_combobox()

        # Create Button for ploting graph
        self.plot_graph_button()

        # Create Progress Bar
        self.progress_bar()

        # Create a matplotlib figure
        self.figure = Figure(figsize=(8, 6))

        # Add a subplot to the figure
        self.ax = self.figure.add_subplot(2, 1, 1)

        # Create a Tkinter canvas that can display the figure
        self.figure_canvas = FigureCanvasTkAgg(self.figure, self)
        self.figure_canvas.get_tk_widget().grid(row=0, column=0, sticky="NSWE")

    def plot_graph_button(self):
        """Create button for visualizing various of graph."""
        # Create a LabelFrame for the Button
        graph_butt_frame = tk.LabelFrame(self, text="Plot", padx=10, pady=10)

        # Create Button
        graph_button = ttk.Button(
            graph_butt_frame, 
            text="Graph",
        )

        # Bind the plot_graph() to Button
        graph_button.bind("<Button-1>", self.plot_graph)
        graph_button.pack()

        # Add the LabelFrame and Button to the top right corner of the window
        graph_butt_frame.grid(row=0, column=1, padx=10, pady=0, sticky="S")

    def year_combobox(self):
        """Create Year Combobox of the applications."""
        # Create a LabelFrame for the ComboBox
        year_combo_frame = tk.LabelFrame(self, text="Year", padx=10, pady=10)

        # Add default value to the Combobox
        all_years_values = self.control.get_all_years()
        all_years_values.insert(0, "Select Year")

        # Create the ComboBox
        self.year_var = tk.StringVar(value=all_years_values[0])
        self.year_var.trace("w", lambda *args: self.bar_by_year())
        year_combo = ttk.Combobox(
            year_combo_frame,
            textvariable=self.year_var,
            values=all_years_values,
            state="readonly",
        )
        year_combo.pack()

        # Add the LabelFrame and ComboBox to the top left corner of the window
        year_combo_frame.grid(row=0, column=1, padx=10, pady=10, sticky="N")

    def publisher_combobox(self):
        """Create Publisher Combobox for the application."""
        # Create a LabelFrame for the ComboBox
        publisher_combo_frame = tk.LabelFrame(self, text="Publisher", padx=10, pady=10)

        # Add default value to the Combobox
        all_publishers_values = self.control.get_all_publishers()
        all_publishers_values.insert(0, "Select Publisher")

        # Create the ComboBox
        self.publisher_var = tk.StringVar(value=all_publishers_values[0])
        self.publisher_var.trace("w", lambda *args: self.line_by_publisher())
        publisher_combo = ttk.Combobox(
            publisher_combo_frame,
            textvariable=self.publisher_var,
            values=all_publishers_values,
            state="readonly",
        )
        publisher_combo.pack()

        # Add the LabelFrame and ComboBox to the top of the window
        publisher_combo_frame.grid(row=0, column=1, padx=10, pady=80, sticky="N")

    def zone_combobox(self):
        """Create Release Zone Combobox for the application."""
        # Create a LabelFrame for the ComboBox
        zone_combo_frame = tk.LabelFrame(self, text="Zone", padx=10, pady=10)

        # Add default value to the Combobox
        all_zones_values = [
            "Select Zone",
            "Global Sales",
            "NA Sales",
            "EU Sales",
            "JP Sales",
            "Other Sales",
        ]

        # Create the ComboBox
        self.zone_var = tk.StringVar(value=all_zones_values[0])
        self.zone_var.trace("w", lambda *args: self.scatter_by_zone())
        zone_combo = ttk.Combobox(
            zone_combo_frame,
            textvariable=self.zone_var,
            values=all_zones_values,
            state="readonly",
        )
        zone_combo.pack()

        # Add the LabelFrame and ComboBox to the top left corner of the window
        zone_combo_frame.grid(row=0, column=1, padx=10, pady=150, sticky="N")

    def progress_bar(self):
        """Create Progress Bar for the application."""
        # Create a LabelFrame for the ComboBox
        prog_bar_frame = tk.LabelFrame(self, padx=0, pady=0)

        self.prog_bar = ttk.Progressbar(
            prog_bar_frame,
            orient="horizontal",
            length=800,
            mode="determinate",
        )
        self.prog_bar.pack()

        prog_bar_frame.grid(row=1, column=0, padx=0, pady=0, sticky="SW")

    def hist_by_year(self):
        """Create distribution graph of games released in different years."""
        # Plot seaborn histogram graph
        sns.histplot(
            data=self.control.get_df(),
            x="Year",
            # Set interval bins to be all years in data frame.
            bins=self.control.get_all_years(),
            ax=self.ax,
        )

        # Graph components
        self.ax.set_title("Distribution of Global Sales")
        self.ax.set_xlabel("Year")
        self.ax.set_ylabel("Number of Games Released")

        self.ax.tick_params(axis="x", rotation=360, labelsize=10)

    def bar_by_year(self):
        """Create the graph of data frame filter by selected year."""
        # Get selected value from combobox
        selected_year = self.year_var.get()

        # Get the data frame from control module filter by selected year
        df_by_selected_year = self.control.get_record_by_year(int(selected_year))

        # Plot seaborn bar graph
        sns.barplot(
            data=df_by_selected_year,
            x=df_by_selected_year["Name"] + " (" + df_by_selected_year["Platform"] + ")",
            y="Global_Sales",
            ax=self.ax,
        )

        # Graph components
        # # If row is 1
        if df_by_selected_year.shape[0] == 1:
            self.ax.set_title(f"Top Game sales in {selected_year}")
        else:
            self.ax.set_title(
                f"Top {df_by_selected_year.shape[0]} Games sales in {selected_year}"
            )
        self.ax.set_xlabel("Games (Platform)")
        self.ax.set_ylabel("Global Sales (Million Units)")

        # If rows are more than 15, ratate x axis 80
        if df_by_selected_year.shape[0] <= 15:
            self.ax.tick_params(axis="x", rotation=80, labelsize=8)
        # Otherwise, 90
        else:
            self.ax.tick_params(axis="x", rotation=90, labelsize=8)

    def line_by_publisher(self):
        """Create line graph of data frame filter by selected publisher."""
        # Get selected value from combobox
        selected_publisher = self.publisher_var.get()

        # Get the data frame from control module filter by selected publisher
        df_by_selected_publisher = self.control.get_record_by_publisher(str(selected_publisher))

        # Plot seaborn line graph
        sns.lineplot(
            x="Year",
            y="Global_Sales",
            data=df_by_selected_publisher,
            ax=self.ax,
        )

        # Graph components
        self.ax.set_title(f"Trend of Global Sales for {selected_publisher}")
        self.ax.set_xlabel("Year")
        self.ax.set_ylabel("Global Sales (Millions)")

        self.ax.tick_params(axis="x", rotation=360, labelsize=10)

    def scatter_by_zone(self):
        """Create scatter graph of data frame filter by selected zone."""
        # Get selected value from combobox
        selected_zone = self.zone_var.get()
        add_underscore = selected_zone.replace(" ", "_")

        # Get the data frame from control module filter by selected zone
        df_by_selected_zone = self.control.get_record_by_zone(str(selected_zone))

        # Plot seaborn scatter graph
        sns.scatterplot(
            x="Year",
            y=add_underscore,
            data=df_by_selected_zone,
            ax=self.ax,
        )

        # Graph components
        self.ax.set_title(f"{selected_zone} vs Year")
        self.ax.set_xlabel("Year")
        self.ax.set_ylabel(f"{selected_zone} (Million Units)")

        self.ax.tick_params(axis="x", rotation=360, labelsize=10)

    def plot_graph(self, event):
        """Drawing various of graph to the canvas. Update Progess Bar when ploting graph."""
        self.ax.clear()

        # If none of all comboboxes have been chosen
        if self.year_var.get() == "Select Year" and self.publisher_var.get() == "Select Publisher" and self.zone_var.get() == "Select Zone":
            self.hist_by_year()
        # If only Zone is selected
        elif self.year_var.get() == "Select Year" and self.publisher_var.get() == "Select Publisher":
            self.scatter_by_zone()
        # If only Publisher is selected
        elif self.year_var.get() == "Select Year" and self.zone_var.get() == "Select Zone":
            self.line_by_publisher()
        # If only Year is selected
        elif self.publisher_var.get() == "Select Publisher" and self.zone_var.get() == "Select Zone":
            self.bar_by_year()

        # Update Progress Bar
        for i in range(0, 101):
            self.prog_bar["value"] = i
            self.prog_bar.update()

            # Pause for a moment to allow the GUI to update
            self.after(1)
        
        # Place the graph
        self.figure.canvas.draw()
        # Reset Progress Bar
        self.prog_bar["value"] -= self.prog_bar["value"]
