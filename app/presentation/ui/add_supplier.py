from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QFont
from app.application.service import SupplierService

class AddSupplierDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Новый поставщик")
        self.setFont(QFont("Comic Sans MS", 10))
        self.svc = SupplierService()

        self._setup_ui()

    def _setup_ui(self):
        layout = QFormLayout(self)

        self.name_edit = QLineEdit()
        layout.addRow("Название поставщика:", self.name_edit)

        self.inn_edit = QLineEdit()
        self.inn_edit.setInputMask("0000000000;_")
        layout.addRow("ИНН (10 цифр):", self.inn_edit)

        btn_box = QHBoxLayout()
        save = QPushButton("Сохранить")
        cancel = QPushButton("Отмена")
        save.clicked.connect(self.on_save)
        cancel.clicked.connect(self.reject)
        for b in (save, cancel):
            b.setStyleSheet("background-color: #546F94; color: white; padding:4px;")
            btn_box.addWidget(b)
        layout.addRow(btn_box)

    def on_save(self):
        name = self.name_edit.text().strip()
        inn = self.inn_edit.text().strip()
        if not name or len(inn) != 10 or "_" in inn:
            QMessageBox.warning(self, "Ошибка", "Введите корректное название и 12-значный ИНН.")
            return
        try:
            s = self.svc.create(name=name, inn=inn)
            self.new_id = s.id
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
