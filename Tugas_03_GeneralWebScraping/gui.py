import csv
from datetime import datetime
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QProgressBar, QLabel, QDateEdit, QFileDialog, QSpinBox, QMessageBox, QGroupBox, QHeaderView, QDialog, QTextEdit, QSizePolicy
from PyQt5.QtCore import QDate, Qt, QUrl, QTimer
from PyQt5.QtGui import QDesktopServices
from scraper import ScraperThread
from theme import MODERN_DARK_THEME, MODERN_LIGHT_THEME

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("General News Scraper")
        self.resize(1000, 650)
        self.scraped_data = []
        self.is_dark_theme = True
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        
        layout_top = QHBoxLayout()
        self.lbl_project = QLabel("Project by Kelompok C1")
        self.lbl_project.setStyleSheet("font-weight: bold; color: white;")
        layout_top.addWidget(self.lbl_project)
        
        layout_top.addStretch()
        self.btn_theme = QPushButton("Ganti Tema Terang")
        self.btn_theme.clicked.connect(self.toggle_theme)
        layout_top.addWidget(self.btn_theme)
        
        group_input = QGroupBox("Konfigurasi Scraping")
        layout_input = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Masukkan URL Berita Akar (contoh: detik.com)")
        self.limit_input = QSpinBox()
        self.limit_input.setRange(1, 100)
        self.limit_input.setValue(10)
        layout_input.addWidget(QLabel("URL:"))
        layout_input.addWidget(self.url_input, stretch=3)
        layout_input.addWidget(QLabel("Limit:"))
        layout_input.addWidget(self.limit_input, stretch=1)
        group_input.setLayout(layout_input)
        
        group_filter = QGroupBox("Filter Rentang Tanggal")
        layout_filter = QHBoxLayout()
        self.start_date = QDateEdit(QDate.currentDate().addDays(-7))
        self.start_date.setCalendarPopup(True)
        self.end_date = QDateEdit(QDate.currentDate())
        self.end_date.setCalendarPopup(True)
        layout_filter.addWidget(QLabel("Dari:"))
        layout_filter.addWidget(self.start_date)
        layout_filter.addWidget(QLabel("Sampai:"))
        layout_filter.addWidget(self.end_date)
        group_filter.setLayout(layout_filter)
        
        group_action = QGroupBox("Aksi")
        layout_action = QVBoxLayout()
        
        self.btn_start = QPushButton("Mulai Scraping")
        self.btn_start.setObjectName("btn_start")
        self.btn_start.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.btn_start.clicked.connect(self.start_scraping)
        
        btn_layout = QHBoxLayout()
        self.btn_stop = QPushButton("Batal")
        self.btn_stop.setObjectName("btn_stop")
        self.btn_stop.setEnabled(False)
        self.btn_stop.clicked.connect(self.stop_scraping)
        
        self.btn_export_csv = QPushButton("Export CSV")
        self.btn_export_csv.setEnabled(False)
        self.btn_export_csv.clicked.connect(self.export_csv)
        
        self.btn_export_excel = QPushButton("Export Excel")
        self.btn_export_excel.setObjectName("btn_export_excel")
        self.btn_export_excel.setEnabled(False)
        self.btn_export_excel.clicked.connect(self.export_excel)
        
        btn_layout.addWidget(self.btn_stop)
        btn_layout.addWidget(self.btn_export_csv)
        btn_layout.addWidget(self.btn_export_excel)
        
        self.progress_bar = QProgressBar()
        
        layout_action.addWidget(self.btn_start)
        layout_action.addLayout(btn_layout)
        layout_action.addWidget(self.progress_bar)
        group_action.setLayout(layout_action)
        
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Judul", "Tanggal", "Aksi"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.verticalHeader().setDefaultSectionSize(60)
        
        main_layout.addLayout(layout_top)
        main_layout.addWidget(group_input)
        main_layout.addWidget(group_filter)
        main_layout.addWidget(group_action)
        main_layout.addWidget(self.table)
        
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        if self.is_dark_theme:
            self.setStyleSheet(MODERN_DARK_THEME)
            self.btn_theme.setText("Ganti Tema Terang")
            self.lbl_project.setStyleSheet("font-weight: bold; color: white;")
        else:
            self.setStyleSheet(MODERN_LIGHT_THEME)
            self.btn_theme.setText("Ganti Tema Gelap")
            self.lbl_project.setStyleSheet("font-weight: bold; color: black;")

    def start_scraping(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Peringatan", "Silakan masukkan URL tujuan.")
            return
            
        if not url.startswith("http"):
            url = "https://" + url
        
        self.init_start_dialog()
        
        self.table.setRowCount(0)
        self.scraped_data.clear()
        
        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.btn_export_csv.setEnabled(False)
        self.btn_export_excel.setEnabled(False)
        
        self.progress_bar.setFormat("%p%")
        
        dt_start = datetime.combine(self.start_date.date().toPyDate(), datetime.min.time())
        dt_end = datetime.combine(self.end_date.date().toPyDate(), datetime.max.time())
        
        self.thread = ScraperThread(url, self.limit_input.value(), dt_start, dt_end)
        self.thread.data_received.connect(self.add_to_table)
        self.thread.progress_update.connect(self.update_progress)
        self.thread.finished_scraping.connect(self.on_finished)
        self.thread.error_occurred.connect(self.on_error)
        self.thread.start()

    def init_start_dialog(self):
        self.start_dialog = QDialog(self)
        self.start_dialog.setWindowTitle("Proses Dimulai")
        self.start_dialog.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Sedang memulai proses..."))
        self.start_dialog.setLayout(layout)
        self.start_dialog.show()

    def update_progress(self, val):
        if val > 0 and hasattr(self, 'start_dialog') and self.start_dialog.isVisible():
            self.start_dialog.close()
        self.progress_bar.setValue(val)

    def stop_scraping(self):
        if hasattr(self, 'thread') and self.thread.isRunning():
            self.thread.stop()
            self.progress_bar.setFormat("Dibatalkan")
            self.on_finished("Proses dihentikan secara manual.")

    def add_to_table(self, data):
        self.scraped_data.append(data)
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(data['title']))
        self.table.setItem(row, 1, QTableWidgetItem(data['date']))
        widget_aksi = QWidget()
        layout_aksi = QHBoxLayout()
        layout_aksi.setContentsMargins(5, 5, 5, 5)
        btn_lihat = QPushButton("Lihat Konten")
        btn_buka = QPushButton("Buka URL")
        btn_lihat.setStyleSheet("font-size: 8pt; padding: 4px; border-radius: 3px;")
        btn_buka.setStyleSheet("font-size: 8pt; padding: 4px; border-radius: 3px;")
        btn_lihat.clicked.connect(lambda checked, c=data['content']: self.show_content_popup(c))
        btn_buka.clicked.connect(lambda checked, u=data['url']: QDesktopServices.openUrl(QUrl(u)))
        layout_aksi.addWidget(btn_lihat)
        layout_aksi.addWidget(btn_buka)
        widget_aksi.setLayout(layout_aksi)
        self.table.setCellWidget(row, 2, widget_aksi)

    def show_content_popup(self, content):
        dialog = QDialog(self)
        dialog.setWindowTitle("Isi Konten Berita")
        dialog.setFixedSize(700, 500)
        layout = QVBoxLayout()
        text_edit = QTextEdit()
        text_edit.setPlainText(content)
        text_edit.setReadOnly(True)
        btn_tutup = QPushButton("Tutup")
        btn_tutup.clicked.connect(dialog.accept)
        layout.addWidget(text_edit)
        layout.addWidget(btn_tutup)
        dialog.setLayout(layout)
        dialog.exec_()

    def reset_progress(self):
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("%p%")

    def on_finished(self, msg):
        if hasattr(self, 'start_dialog') and self.start_dialog.isVisible():
            self.start_dialog.close()
            
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)
        
        has_data = len(self.scraped_data) > 0
        self.btn_export_csv.setEnabled(has_data)
        self.btn_export_excel.setEnabled(has_data)
        
        if self.progress_bar.value() == 100:
            self.progress_bar.setFormat("Selesai")
            QTimer.singleShot(10000, self.reset_progress)
        QMessageBox.information(self, "Informasi", msg)

    def on_error(self, msg):
        self.on_finished("Error")
        QMessageBox.critical(self, "Terjadi Kesalahan", str(msg))

    def export_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Simpan Dataset CSV", "dataset.csv", "CSV Files (*.csv)")
        if path:
            with open(path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=["title", "date", "content", "url"])
                writer.writeheader()
                writer.writerows(self.scraped_data)
            QMessageBox.information(self, "Sukses", "Data berhasil diexport ke CSV!")

    def export_excel(self):
        path, _ = QFileDialog.getSaveFileName(self, "Simpan Dataset Excel", "dataset.xlsx", "Excel Files (*.xlsx)")
        if path:
            try:
                import openpyxl
                wb = openpyxl.Workbook()
                ws = wb.active
                ws.title = "Hasil Scraping"
                headers = ["Judul Berita", "Tanggal", "Konten Berita", "URL Source"]
                ws.append(headers)
                for col_num, header in enumerate(headers, 1):
                    cell = ws.cell(row=1, column=col_num)
                    cell.font = openpyxl.styles.Font(bold=True)
                for row_data in self.scraped_data:
                    ws.append([row_data['title'], row_data['date'], row_data['content'], row_data['url']])
                wb.save(path)
                QMessageBox.information(self, "Sukses", "Data berhasil diexport ke Excel!")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))