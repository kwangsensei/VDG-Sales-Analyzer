"""
This analyzer module is responsible for create data frame
analyzing the data and ploting the graph.
"""
import pandas as pd


class Analyzer:
    """Define analyzer for analyzing the data frame and ploting the graph."""
    def __init__(self):
        """Read a original CSV file and create a copy of original data frame."""
        # Read CSV file
        self.__df = pd.read_csv("vgsales.csv")

        # Copy the original data frame
        self.__vdg_df = self.df.copy()

        # Drop rows with missing data and reassign back to the same data frame
        self.__vdg_df = self.__vdg_df.dropna()

        # Set value in year column to integer (from float).
        self.__vdg_df["Year"] = self.__vdg_df["Year"].astype(int)

    @property
    def df(self):
        return self.__df

    @property
    def vdg_df(self):
        return self.__vdg_df
    
    def default_df(self):
        """Return the default use data frame."""
        return self.vdg_df

    def all_years(self):
        """Return sort all years in Year column."""
        return sorted(self.vdg_df["Year"].unique())
    
    def record_by_year(self, selected_year):
        """Return the data frame by selected year in the year combobox."""
        return self.vdg_df[self.vdg_df["Year"] == selected_year][0:50]

    def all_publishers(self):
        """
        Return top 20 publishers that have most release games in Publisher column.
        Sort them by alphabetical order.
        """
        return sorted(self.vdg_df["Publisher"].value_counts().head(20).index.tolist())

    def record_by_publisher(self, selected_publisher):
        """Return the data frame by selected publisher in the publisher combobox."""
        return self.vdg_df[self.vdg_df["Publisher"] == selected_publisher]
    
    def record_by_zone(self, selected_zone):
        """Return the data frame by selected zone in the zone combobox."""
        add_underscore = selected_zone.replace(" ", "_")
        return self.vdg_df.groupby("Year")[add_underscore].sum().reset_index()
