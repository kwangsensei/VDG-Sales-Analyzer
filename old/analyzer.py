import pandas as pd


class Analyzer:
    def __init__(self) -> None:
        """Initialize Analyzer Class."""
        # Read CSV file and create dataframe.
        self.df = pd.read_csv("vgsales.csv")
        # Copy the original DataFrame
        self.VDG_df = self.df.copy()
        # Delete NaN type value.
        self.VDG_df.dropna(how="any", inplace = True)
        # Set year to integer.
        self.VDG_df["Year"] = self.VDG_df["Year"].astype(int)

    def by_year(self, year):
        """
        Return dataframe by selected year.
        Cut off below 50th.
        """
        return self.VDG_df[self.VDG_df["Year"] == year].iloc[0:50]

    def by_publisher(self, year, publisher):
        """Return dataframe by selected year and punlisher."""
        return self.by_year(year)[self.by_year(year)["Publisher"] == publisher]
