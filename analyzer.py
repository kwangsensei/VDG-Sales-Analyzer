import pandas as pd

class Analyzer:
    def __init__(self) -> None:
        self.VDG_df = pd.read_csv("vgsales.csv")
        self.VDG_df.dropna(how="any", inplace = True)
        self.VDG_df["Year"] = self.VDG_df["Year"].astype(int)

    def by_year(self, year):
        return self.VDG_df[self.VDG_df["Year"] == year].iloc[0:50, :]

    def by_publisher(self, year, publisher):
        return self.by_year(year)[self.by_year(year)["Publisher"] == publisher]
