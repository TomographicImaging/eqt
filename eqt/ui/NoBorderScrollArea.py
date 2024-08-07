import re

import qdarkstyle
from PySide2.QtWidgets import QPushButton, QScrollArea, QWidget


class NoBorderScrollArea(QScrollArea):
    def __init__(self, widget, parent=None):
        """Creates an instance of a QScrollArea and sets its border to none.
        Sets its widget to resizable. Due to a bug in `qdarkstyle`, the PushButtons in the
        widget do not inherit the right style. The init applies `qdarkstyle` to all the buttons
        present in the widget when the object is created. Any button added to the widget after the
        init is invoked will not be styled as expected. In this case, the method
        `apply_qdarkstyle_to_buttons` would need to be invoked by the user after the object is
        instanced."""
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
        """Returns the QPushButton styles from qdarkstyle, including the different
        button styles."""
        style = qdarkstyle.load_stylesheet(qt_api='pyside2')
        pattern = re.compile(r"(QPushButton\s*{[^}]*}|QPushButton\s*:[^}]*{[^}]*})", re.DOTALL)
        matches = pattern.findall(style)
        if matches:
            return ''.join(matches)
        return ""
