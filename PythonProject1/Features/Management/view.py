from PyQt6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QTableWidget,
    QHeaderView,
    QTableWidgetItem,
    QLabel,
)


class ManagementView(QWidget):

    def __init__(self, service):
        super().__init__()

        self.service = service
        self.control_panel = None

        self.setWindowTitle("Inventory Management")
        self.resize(850, 650)

        self.build_ui()
        self.refresh()

    def build_ui(self):

        layout = QVBoxLayout(self)

        title = QLabel("INVENTORY MANAGEMENT")

        title.setStyleSheet(
            "font-size: 20px; font-weight: bold;"
        )

        layout.addWidget(title)

        self.table = QTableWidget(0, 6)

        self.table.setHorizontalHeaderLabels([
            "ID",
            "Name",
            "Category",
            "Quantity",
            "Price",
            "Total"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        layout.addWidget(self.table)

    def set_control_panel(self, control_panel):

        self.control_panel = control_panel

        # Add ONE control panel to the window
        self.layout().insertWidget(
            1,
            control_panel
        )

        # Load the selected item's information
        self.table.itemSelectionChanged.connect(
            self.control_panel.load_selected_item
        )

    def refresh(self):
        items = self.service.get_items()

        self.table.setRowCount(len(items))

        for row, item in enumerate(items):
            values = [
                str(item.id),
                item.name,
                item.category,
                str(item.quantity),
                f"₱{item.price:,.2f}",
                f"₱{item.quantity * item.price:,.2f}"
            ]

            for column, value in enumerate(values):
                self.table.setItem(
                    row,
                    column,
                    QTableWidgetItem(value)
                )