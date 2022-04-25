"""File to launch the clock application."""
from analyzer import Analyzer
from analyzer_ui import AnalyzerUI

if __name__ == "__main__":
    analyzer = Analyzer()
    ui = AnalyzerUI(analyzer)
    ui.run()
    