from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QAbstractItemView
)
from PyQt5.QtGui import QIcon, QFont

from app.application.service import MaterialService
from app.presentation.ui.calculation import CalculationWindow
from app.presentation.ui.edit_material import EditMaterialDialog
from app.presentation.ui.suppliers import SuppliersWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Склад материалов — Мозаика")
        self.setWindowIcon(QIcon("./app/resources/icon.png"))
        self.resize(1440, 1000)
        self.setMinimumSize(1000, 800)
        self._setup_ui()
        self._load_data()

    def _setup_ui(self):
        self.setFont(QFont("Comic Sans MS", 10))
        central = QWidget()
        central.setStyleSheet("background-color: #FFFFFF;")
        self.setCentralWidget(central)

        vbox = QVBoxLayout(central)

        self.table = QTableWidget(0, 9)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setHorizontalHeaderLabels([
            "Наименование материала", "Тип материала", "Единица измерения", "Количество в упаковке",
            "Количество на складе", "Минимальное количество", "Цена единицы материала", "Минимальная партия, руб.",
            "Поставщики"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        vbox.addWidget(self.table)

        hbox = QHBoxLayout()
        btn_style = """
            background-color: #546F94; color: white; padding: 6px; border-radius: 4px;
        """
        buttons = [
            ("Добавить", self.on_add),
            ("Редактировать", self.on_edit),
            ("Поставщики", self.on_suppliers),
            ("Расчет продукции", self.on_calculation)
        ]
        for text, handler in buttons:
            btn = QPushButton(text)
            btn.setStyleSheet(btn_style)
            btn.clicked.connect(handler)
            hbox.addWidget(btn)
        vbox.addLayout(hbox)

    def _load_data(self):
        self.table.setRowCount(0)
        try:
            materials = MaterialService().get_all()
            for m in materials:
                row = self.table.rowCount()
                self.table.insertRow(row)
                vals = [
                    m.name,
                    m.material_type.name,
                    m.unit.name,
                    str(m.pack_size),
                    str(m.quantity),
                    str(m.min_quantity),
                    f"{m.price:.2f}",
                    f"{MaterialService.calc_min_batch_cost(m):.2f}",
                    ", ".join(s.name for s in m.suppliers)
                ]
                for col, val in enumerate(vals):
                    self.table.setItem(row, col, QTableWidgetItem(val))
        except Exception as e:
            QMessageBox.critical(self, "Ошибка загрузки", str(e))

    def _selected_material(self):
        idx = self.table.currentRow()
        if idx < 0:
            QMessageBox.warning(self, "Выбор материала", "Сначала выберите строку.")
            return None
        name = self.table.item(idx, 0).text()
        return MaterialService().get_by_name(name)

    def on_add(self):
        dlg = EditMaterialDialog(parent=self)
        if dlg.exec_():
            self._load_data()

    def on_edit(self):
        material = self._selected_material()
        if material:
            dlg = EditMaterialDialog(material=material, parent=self)
            if dlg.exec_():
                self._load_data()

    def on_suppliers(self):
        material = self._selected_material()
        if material:
            dlg = SuppliersWindow(material_id=material.id, parent=self)
            dlg.exec_()
            self._load_data()

    def on_calculation(self):
        dlg = CalculationWindow(parent=self)
        dlg.exec_()
