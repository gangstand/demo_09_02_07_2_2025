from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QFont
from app.application.service import MaterialTypeService

class AddMaterialTypeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Новый тип материала")
        self.setFont(QFont("Comic Sans MS", 10))

        self._setup_ui()
        self.svc = MaterialTypeService()

    def _setup_ui(self):
        layout = QFormLayout(self)
        self.name_edit = QLineEdit()
        layout.addRow("Название типа:", self.name_edit)
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
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название типа материала.")
            return
        try:
            mt = self.svc.create(name=name)
            self.new_id = mt.id
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
