from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QMessageBox, QAbstractItemView,
    QComboBox, QFormLayout, QSpinBox, QDateEdit
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QDate

from app.application.service import SupplierService, MaterialSupplierService
from app.presentation.ui.supplier import AddSupplierDialog


class SuppliersWindow(QDialog):
    def __init__(self, material_id, parent=None):
        super().__init__(parent)
        self.material_id = material_id
        self.sup_svc = SupplierService()
        self.ms_svc = MaterialSupplierService()
        self.resize(600, 600)
        self.setMinimumSize(600, 600)
        self._setup_ui()
        self._load_data()

    def _setup_ui(self):
        self.setWindowTitle("Поставщики материала")
        self.setFont(QFont("Comic Sans MS", 10))
        vbox = QVBoxLayout(self)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Поставщик", "Рейтинг", "Дата начала"])
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.horizontalHeader().setStretchLastSection(True)
        vbox.addWidget(self.table)

        hbox = QHBoxLayout()
        btn_style = "background-color: #546F94; color: white; padding:4px;"

        add_btn = QPushButton("Добавить")
        add_btn.setStyleSheet(btn_style)
        add_btn.clicked.connect(self.on_attach)
        hbox.addWidget(add_btn)

        remove_btn = QPushButton("Удалить")
        remove_btn.setStyleSheet(btn_style)
        remove_btn.clicked.connect(self.on_remove)
        hbox.addWidget(remove_btn)

        back_btn = QPushButton("Назад")
        back_btn.setStyleSheet(btn_style)
        back_btn.clicked.connect(self.accept)
        hbox.addWidget(back_btn)

        vbox.addLayout(hbox)

    def _load_data(self):
        self.table.setRowCount(0)
        entries = self.sup_svc.get_by_material(self.material_id)
        for entry in entries:
            supplier = entry['supplier']
            rating = entry['rating']
            start_date = entry['start_date']
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(supplier.name))
            self.table.setItem(row, 1, QTableWidgetItem(f"{rating:.1f}"))
            self.table.setItem(row, 2, QTableWidgetItem(start_date.strftime("%Y-%m-%d")))

    def on_attach(self):
        dlg = QDialog(self)
        dlg.resize(600, 600)
        dlg.setMinimumSize(600, 600)
        dlg.setWindowTitle("Выбрать поставщика")
        dlg.setFont(QFont("Comic Sans MS", 10))
        form = QFormLayout(dlg)

        h_sup = QHBoxLayout()
        combo = QComboBox()
        all_sup = self.sup_svc.get_all()
        for s in all_sup:
            combo.addItem(s.name, s.id)
        btn_new = QPushButton("+")
        btn_new.setFixedWidth(24)
        h_sup.addWidget(combo)
        h_sup.addWidget(btn_new)
        form.addRow("Поставщик:", h_sup)

        def add_new_supplier():
            new_dlg = AddSupplierDialog(self)
            if new_dlg.exec_():
                new_id = new_dlg.new_id
                combo.clear()
                updated = self.sup_svc.get_all()
                for sup in updated:
                    combo.addItem(sup.name, sup.id)
                idx = combo.findData(new_id)
                combo.setCurrentIndex(idx)

        btn_new.clicked.connect(add_new_supplier)

        rating_sb = QSpinBox()
        rating_sb.setRange(0, 100)
        form.addRow("Рейтинг:", rating_sb)
        date_edit = QDateEdit()
        date_edit.setCalendarPopup(True)
        date_edit.setDate(QDate.currentDate())
        form.addRow("Дата начала:", date_edit)

        btn_box = QHBoxLayout()
        ok = QPushButton("OK")
        cancel = QPushButton("Отмена")
        ok.clicked.connect(dlg.accept)
        cancel.clicked.connect(dlg.reject)
        btn_box.addWidget(ok)
        btn_box.addWidget(cancel)
        form.addRow(btn_box)

        if dlg.exec_():
            sup_id = combo.currentData()
            rating = rating_sb.value()
            start_date = date_edit.date().toPyDate()
            self.ms_svc.attach(self.material_id, sup_id, rating, start_date)
            self._load_data()

    def on_remove(self):
        idx = self.table.currentRow()
        if idx < 0:
            QMessageBox.warning(self, "Удаление", "Сначала выберите запись.")
            return
        sup_name = self.table.item(idx, 0).text()
        sup = next((s for s in self.sup_svc.get_all() if s.name == sup_name), None)
        if sup:
            self.ms_svc.detach(self.material_id, sup.id)
            self._load_data()
        else:
            QMessageBox.critical(self, "Ошибка", "Поставщик не найден.")
