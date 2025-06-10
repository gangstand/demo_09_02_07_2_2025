from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
)
from PyQt5.QtGui import QFont
from app.application.service import ProductTypeService


class AddProductTypeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Новый тип продукции")
        self.setFont(QFont("Comic Sans MS", 10))
        self.svc = ProductTypeService()
        self._setup_ui()

    def _setup_ui(self):
        layout = QFormLayout(self)

        self.name_edit = QLineEdit()
        layout.addRow("Название типа:", self.name_edit)

        self.coef_edit = QLineEdit()
        self.coef_edit.setPlaceholderText("например, 1.2")
        layout.addRow("Коэффициент:", self.coef_edit)

        btn_box = QHBoxLayout()
        save_btn = QPushButton("Сохранить")
        cancel_btn = QPushButton("Отмена")
        for btn in (save_btn, cancel_btn):
            btn.setStyleSheet("background-color: #546F94; color: white; padding:4px;")
            btn_box.addWidget(btn)
        save_btn.clicked.connect(self.on_save)
        cancel_btn.clicked.connect(self.reject)
        layout.addRow(btn_box)

    def on_save(self):
        name = self.name_edit.text().strip()
        coef_str = self.coef_edit.text().strip()

        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название типа продукции.")
            return
        try:
            coef = float(coef_str.replace(",", "."))
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Коэффициент должен быть числом.")
            return
        if coef <= 0:
            QMessageBox.warning(self, "Ошибка", "Коэффициент должен быть положительным.")
            return

        try:
            pt = self.svc.create(name=name, coefficient=coef)
            self.new_id = pt.id
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка создания", str(e))
