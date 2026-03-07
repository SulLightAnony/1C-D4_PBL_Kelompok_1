# theme.py

MODERN_DARK_THEME = """
QMainWindow, QDialog, QWidget {
    background-color: #1e1e2e;
    color: #cdd6f4;
    font-family: 'Segoe UI', Arial, sans-serif;
}

QGroupBox {
    border: 1px solid #45475a;
    border-radius: 6px;
    margin-top: 1ex;
    padding-top: 15px;
    font-weight: bold;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 5px;
    color: #89b4fa;
}

QLineEdit, QSpinBox, QDateEdit, QTextEdit {
    background-color: #181825;
    border: 1px solid #313244;
    border-radius: 4px;
    padding: 6px;
    color: #cdd6f4;
    selection-background-color: #89b4fa;
    selection-color: #11111b;
}

QLineEdit:focus, QSpinBox:focus, QDateEdit:focus, QTextEdit:focus {
    border: 1px solid #89b4fa;
}

QPushButton {
    background-color: #89b4fa;
    color: #11111b;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #b4befe;
}

QPushButton:pressed {
    background-color: #74c7ec;
}

QPushButton:disabled {
    background-color: #313244;
    color: #585b70;
}

QTableWidget {
    background-color: #181825;
    alternate-background-color: #1e1e2e;
    color: #cdd6f4;
    gridline-color: #313244;
    border: 1px solid #313244;
    border-radius: 4px;
}

QHeaderView::section {
    background-color: #313244;
    color: #cdd6f4;
    padding: 6px;
    border: none;
    border-right: 1px solid #1e1e2e;
    border-bottom: 1px solid #1e1e2e;
    font-weight: bold;
}

QProgressBar {
    border: 1px solid #313244;
    border-radius: 4px;
    text-align: center;
    color: white;
    font-weight: bold;
    background-color: #181825;
}

QProgressBar::chunk {
    background-color: #a6e3a1;
    border-radius: 3px;
}
"""

MODERN_LIGHT_THEME = """
QMainWindow, QDialog, QWidget {
    background-color: #f8f9fa;
    color: #212529;
    font-family: 'Segoe UI', Arial, sans-serif;
}

QGroupBox {
    border: 1px solid #dee2e6;
    border-radius: 6px;
    margin-top: 1ex;
    padding-top: 15px;
    font-weight: bold;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 5px;
    color: #0d6efd;
}

QLineEdit, QSpinBox, QDateEdit, QTextEdit {
    background-color: #ffffff;
    border: 1px solid #ced4da;
    border-radius: 4px;
    padding: 6px;
    color: #212529;
    selection-background-color: #0d6efd;
    selection-color: #ffffff;
}

QLineEdit:focus, QSpinBox:focus, QDateEdit:focus, QTextEdit:focus {
    border: 1px solid #0d6efd;
}

QPushButton {
    background-color: #0d6efd;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #0b5ed7;
}

QPushButton:pressed {
    background-color: #0a58ca;
}

QPushButton:disabled {
    background-color: #e9ecef;
    color: #6c757d;
}

QTableWidget {
    background-color: #ffffff;
    alternate-background-color: #f8f9fa;
    color: #212529;
    gridline-color: #dee2e6;
    border: 1px solid #ced4da;
    border-radius: 4px;
}

QHeaderView::section {
    background-color: #e9ecef;
    color: #212529;
    padding: 6px;
    border: none;
    border-right: 1px solid #ced4da;
    border-bottom: 1px solid #ced4da;
    font-weight: bold;
}

QProgressBar {
    border: 1px solid #ced4da;
    border-radius: 4px;
    text-align: center;
    color: #212529;
    font-weight: bold;
    background-color: #e9ecef;
}

QProgressBar::chunk {
    background-color: #198754;
    border-radius: 3px;
}
"""