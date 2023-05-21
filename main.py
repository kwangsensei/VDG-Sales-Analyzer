"""
This Main module is responsible for running the application.
"""
from window_gui import WindowGUI


class Main:
    """Run the application."""
    app = WindowGUI()
    app.mainloop()
