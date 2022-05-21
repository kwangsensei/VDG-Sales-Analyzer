from analyzer import Analyzer
from analyzer_ui import AnalyzerUI

if __name__ == "__main__":
    """Run the program."""
    analyzer = Analyzer()
    ui = AnalyzerUI(analyzer)
    ui.run()
    