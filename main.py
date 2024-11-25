import os
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton, QFileDialog, QTextEdit, QWidget
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class RemoveReadOnlyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Снятие атрибута 'Только чтение'")
        self.setGeometry(100, 100, 600, 400)
        self.initUI()

    def initUI(self):
        # Основной виджет
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Основной layout
        layout = QVBoxLayout()

        # Заголовок
        self.title_label = QLabel("Снятие атрибута 'Только чтение'")
        self.title_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)

        # Кнопка выбора папки
        self.select_folder_btn = QPushButton("Выбрать папку")
        self.select_folder_btn.clicked.connect(self.select_folder)

        # Текстовое поле для отображения логов
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)

        # Кнопка запуска обработки
        self.run_btn = QPushButton("Снять атрибуты")
        self.run_btn.clicked.connect(self.run_process)
        self.run_btn.setEnabled(False)

        # Добавление элементов в layout
        layout.addWidget(self.title_label)
        layout.addWidget(self.select_folder_btn)
        layout.addWidget(self.log_output)
        layout.addWidget(self.run_btn)

        self.central_widget.setLayout(layout)

        # Применение стилей через CSS
        self.setStyleSheet("""
            QLabel {
                color: #333;
                margin: 10px 0;
            }
            QPushButton {
                background-color: #0078D7;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #005A9E;
            }
            QTextEdit {
                background-color: #f9f9f9;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 10px;
                font-family: Consolas, monospace;
            }
        """)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку")
        if folder:
            self.folder_path = folder
            self.log_output.append(f"Выбрана папка: {folder}")
            self.run_btn.setEnabled(True)

    def run_process(self):
        if hasattr(self, 'folder_path'):
            self.log_output.append("Начинается обработка...\n")
            self.remove_read_only_attribute(self.folder_path)
            self.log_output.append("Обработка завершена.")

    def remove_read_only_attribute(self, directory):
        for root, dirs, files in os.walk(directory):
            # Обработка папок
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                try:
                    os.chmod(dir_path, os.stat(dir_path).st_mode | 0o222)
                    self.log_output.append(f"Снят атрибут 'Только чтение' с папки: {dir_path}")
                except Exception as e:
                    self.log_output.append(f"Ошибка при обработке папки {dir_path}: {e}")

            # Обработка файлов
            for file_name in files:
                file_path = os.path.join(root, file_name)
                try:
                    os.chmod(file_path, os.stat(file_path).st_mode | 0o222)
                    self.log_output.append(f"Снят атрибут 'Только чтение' с файла: {file_path}")
                except Exception as e:
                    self.log_output.append(f"Ошибка при обработке файла {file_path}: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RemoveReadOnlyApp()
    window.show()
    sys.exit(app.exec_())
