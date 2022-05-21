import pandas as pd

class Analyzer:
    def __init__(self) -> None:
        """Initialize Analyzer Class."""
        self.VDG_df = pd.read_csv("vgsales.csv") # Read CSV file and create dataframe.
        self.VDG_df.dropna(how="any", inplace = True) # Delete NaN type value.
        self.VDG_df["Year"] = self.VDG_df["Year"].astype(int) # Set year to integer.

    def by_year(self, year):
        """
        Return dataframe by selected year.
        Cut off below 50th.
        """
        return self.VDG_df[self.VDG_df["Year"] == year].iloc[0:50, :]

    def by_publisher(self, year, publisher):
        """Return dataframe by selected year and punlisher."""
        return self.by_year(year)[self.by_year(year)["Publisher"] == publisher]
