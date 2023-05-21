"""
This analyzer control module is responsible for facade pattern
of analyzer module.
"""
from analyzer import Analyzer


class AnalyzerControl():
    """Definr facade pattern to control workflow between analyzer and window UI."""
    def __init__(self):
        self.__analyzer = Analyzer()

    @property
    def analyzer(self):
        return self.__analyzer

    def get_df(self):
        """Get the default use data frame from the logic layer."""
        return self.analyzer.default_df()

    def get_all_years(self):
        """Get all years in year column from the logic layer."""
        return self.analyzer.all_years()

    def get_record_by_year(self, selected_year):
        """
        Get selected year in the combobox and return data frame 
        by selected year from the logic layer.
        """
        return self.analyzer.record_by_year(selected_year)

    def get_all_publishers(self):
        """Get top 20 publishers from the logic layer."""
        return self.analyzer.all_publishers()

    def get_record_by_publisher(self, selected_publisher):
        """
        Get selected publisher in the combobox and return data frame 
        by selected publisher from the logic layer.
        """
        return self.analyzer.record_by_publisher(selected_publisher)

    def get_record_by_zone(self, selected_zone):
        """
        Get selected zone in the combobox and return frame
        by selected zone from the logic layer.
        """
        return self.analyzer.record_by_zone(selected_zone)
