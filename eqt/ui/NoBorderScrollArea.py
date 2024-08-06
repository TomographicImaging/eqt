from PySide2.QtWidgets import QPushButton, QScrollArea, QWidget
import qdarkstyle, re

class NoBorderScrollArea(QScrollArea):
    """Note: move this class to eqt."""

    def __init__(self, widget, parent=None):
        """Creates an instance of a QScrollArea and sets its border to none. 
        Sets its widget to resizable."""
        super().__init__(parent)
        self.setStyleSheet("QScrollArea { border: none; }")
        self.setWidgetResizable(True)
        self.setWidget(widget)
        self.apply_qdarkstyle_to_buttons(widget)
        
    def apply_qdarkstyle_to_buttons(self, widget):
        """Applies the qdarkstyle to all the buttons in the widget explicitly. 
        This ensures that the style is consistent with the rest of the app."""
        if isinstance(widget, QPushButton):
            
            button_style = self._extract_qdarkstyle_button_style()
            widget.setStyleSheet(button_style)
        for child in widget.findChildren(QWidget):
            self.apply_qdarkstyle_to_buttons(child)

    def _extract_qdarkstyle_button_style(self):
        """Returns the QPushButton styles from qdarkstyle, including the different button styles."""
        style = qdarkstyle.load_stylesheet(qt_api='pyside2')
        pattern = re.compile(r"(QPushButton\s*{[^}]*}|QPushButton\s*:[^}]*{[^}]*})", re.DOTALL)
        matches = pattern.findall(style)
        if matches:
            return ''.join(matches)
        return ""