from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLabel, QComboBox,
    QSpinBox, QDoubleSpinBox, QPushButton, QMessageBox, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from app.application.service import ProductionService, ProductTypeService, MaterialTypeService
from app.presentation.ui.add_product_type import AddProductTypeDialog


class CalculationWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Расчет выхода продукции")
        self.setFont(QFont("Comic Sans MS", 10))

        self.prod_type_svc = ProductTypeService()
        self.mat_type_svc = MaterialTypeService()
        self.prod_svc = ProductionService()

        self._setup_ui()

    def _setup_ui(self):
        vbox = QVBoxLayout(self)
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)

        h_prod = QHBoxLayout()
        self.prod_cb = QComboBox()
        btn_add_pt = QPushButton("+")
        btn_add_pt.setFixedWidth(24)
        h_prod.addWidget(self.prod_cb)
        h_prod.addWidget(btn_add_pt)
        form.addRow("Тип продукции:", h_prod)
        btn_add_pt.clicked.connect(self._on_add_product_type)
        self._load_product_types()

        self.mat_cb = QComboBox()
        for mt in self.mat_type_svc.get_all():
            self.mat_cb.addItem(mt.name, mt.id)
        form.addRow("Тип сырья:", self.mat_cb)

        self.qty_sb = QSpinBox()
        self.qty_sb.setRange(0, 1_000_000)
        form.addRow("Кол-во сырья:", self.qty_sb)

        self.p1_ds = QDoubleSpinBox()
        self.p1_ds.setRange(0.01, 1_000_000.00)
        self.p1_ds.setDecimals(2)
        form.addRow("Параметр p1:", self.p1_ds)

        self.p2_ds = QDoubleSpinBox()
        self.p2_ds.setRange(0.01, 1_000_000.00)
        self.p2_ds.setDecimals(2)
        form.addRow("Параметр p2:", self.p2_ds)

        calc_btn = QPushButton("Рассчитать")
        calc_btn.setStyleSheet("background-color: #546F94; color: white; padding:6px;")
        calc_btn.clicked.connect(self.on_calculate)
        form.addRow(calc_btn)

        self.result_lbl = QLabel("Результат: ")
        self.result_lbl.setAlignment(Qt.AlignCenter)

        vbox.addLayout(form)
        vbox.addWidget(self.result_lbl)

    def _load_product_types(self):
        self.prod_cb.clear()
        for pt in self.prod_type_svc.get_all():
            self.prod_cb.addItem(pt.name, pt.id)

    def _on_add_product_type(self):
        dlg = AddProductTypeDialog(self)
        if dlg.exec_():
            new_id = dlg.new_id
            self._load_product_types()
            idx = self.prod_cb.findData(new_id)
            if idx >= 0:
                self.prod_cb.setCurrentIndex(idx)

    def on_calculate(self):
        pt_id = self.prod_cb.currentData()
        mt_id = self.mat_cb.currentData()
        qty = self.qty_sb.value()
        p1 = self.p1_ds.value()
        p2 = self.p2_ds.value()

        out = self.prod_svc.calculate_output(
            product_type_id=pt_id,
            material_type_id=mt_id,
            qty=qty,
            p1=p1,
            p2=p2
        )

        if out < 0:
            QMessageBox.warning(self, "Ошибка", "Невозможно рассчитать. Проверьте входные данные.")
        else:
            self.result_lbl.setText(f"Результат: {out} шт.")
