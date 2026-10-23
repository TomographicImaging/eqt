from qtpy.QtWidgets import QScrollArea


class NoBorderScrollArea(QScrollArea):
    def __init__(self, widget, parent=None):
        """Creates an instance of a QScrollArea and sets its border to none.
        Sets its widget to resizable."""
        super().__init__(parent)
        self.setStyleSheet("QScrollArea { border: none; }")
        self.setWidgetResizable(True)
        self.setWidget(widget)
