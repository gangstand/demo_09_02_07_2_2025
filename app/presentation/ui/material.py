from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox,
    QPushButton, QHBoxLayout, QMessageBox
)
from PyQt5.QtGui import QFont

from app.application.service import (
    MaterialService,
    MaterialTypeService,
    UnitService,
)
from app.presentation.ui.material_type import AddMaterialTypeDialog
from app.presentation.ui.unit import AddUnitDialog


class EditMaterialDialog(QDialog):
    def __init__(self, material=None, parent=None):
        super().__init__(parent)
        self.material = material
        self.setWindowTitle("Добавить материал" if material is None else "Редактировать материал")
        self.setFont(QFont("Comic Sans MS", 10))

        self.svc = MaterialService()
        self.mt_svc = MaterialTypeService()
        self.unit_svc = UnitService()

        self._setup_ui()
        self._load_refs()
        if material:
            self._fill_fields(material)

    def _setup_ui(self):
        layout = QFormLayout(self)

        self.name = QLineEdit()
        layout.addRow("Наименование материала:", self.name)

        h_type = QHBoxLayout()
        self.type_cb = QComboBox()
        btn_type = QPushButton("+")
        btn_type.setFixedWidth(24)
        h_type.addWidget(self.type_cb)
        h_type.addWidget(btn_type)
        layout.addRow("Тип материала:", h_type)
        btn_type.clicked.connect(self._on_add_type)

        h_unit = QHBoxLayout()
        self.unit_cb = QComboBox()
        btn_unit = QPushButton("+")
        btn_unit.setFixedWidth(24)
        h_unit.addWidget(self.unit_cb)
        h_unit.addWidget(btn_unit)
        layout.addRow("Единица измерения:", h_unit)
        btn_unit.clicked.connect(self._on_add_unit)

        self.pack_size = QSpinBox()
        self.pack_size.setRange(1, 1_000_000)
        layout.addRow("Количество в упаковке:", self.pack_size)

        self.min_qty = QSpinBox()
        self.min_qty.setRange(0, 1_000_000)
        layout.addRow("Минимальное количество:", self.min_qty)

        self.quantity = QSpinBox()
        self.quantity.setRange(0, 1_000_000)
        layout.addRow("Количество на складе:", self.quantity)

        self.price = QDoubleSpinBox()
        self.price.setDecimals(2)
        self.price.setRange(0.00, 1_000_000.00)
        layout.addRow("Цена единицы материала:", self.price)

        btn_box = QHBoxLayout()
        save_btn = QPushButton("Сохранить")
        cancel_btn = QPushButton("Отмена")
        for b in (save_btn, cancel_btn):
            b.setStyleSheet("background-color: #546F94; color: white; padding:4px;")
            btn_box.addWidget(b)
        save_btn.clicked.connect(self._on_save)
        cancel_btn.clicked.connect(self.reject)
        layout.addRow(btn_box)

    def _load_refs(self):
        self.types = self.mt_svc.get_all()
        self.type_cb.clear()
        for t in self.types:
            self.type_cb.addItem(t.name, t.id)
        self.units = self.unit_svc.get_all()
        self.unit_cb.clear()
        for u in self.units:
            self.unit_cb.addItem(u.name, u.id)

    def _fill_fields(self, m):
        self.name.setText(m.name)
        idx = next((i for i, t in enumerate(self.types) if t.id == m.material_type_id), 0)
        self.type_cb.setCurrentIndex(idx)
        idx = next((i for i, u in enumerate(self.units) if u.id == m.unit_id), 0)
        self.unit_cb.setCurrentIndex(idx)
        self.pack_size.setValue(m.pack_size)
        self.min_qty.setValue(m.min_quantity)
        self.quantity.setValue(m.quantity)
        self.price.setValue(float(m.price))

    def _on_add_type(self):
        dlg = AddMaterialTypeDialog(self)
        if dlg.exec_():
            new_id = dlg.new_id
            self._load_refs()
            idx = self.type_cb.findData(new_id)
            if idx >= 0:
                self.type_cb.setCurrentIndex(idx)

    def _on_add_unit(self):
        dlg = AddUnitDialog(self)
        if dlg.exec_():
            new_id = dlg.new_id
            self._load_refs()
            idx = self.unit_cb.findData(new_id)
            if idx >= 0:
                self.unit_cb.setCurrentIndex(idx)

    def _on_save(self):
        data = {
            "name": self.name.text().strip(),
            "material_type_id": self.type_cb.currentData(),
            "unit_id": self.unit_cb.currentData(),
            "pack_size": self.pack_size.value(),
            "min_quantity": self.min_qty.value(),
            "quantity": self.quantity.value(),
            "price": self.price.value(),
        }
        try:
            if self.material:
                self.svc.update(self.material.id, **data)
            else:
                self.svc.create(**data)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка сохранения", str(e))
