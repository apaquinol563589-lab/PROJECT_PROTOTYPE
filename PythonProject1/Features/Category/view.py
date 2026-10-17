from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
)


class CategoryView(QWidget):

    def __init__(self, service):
        super().__init__()

        self.service = service

        # Reference to the inventory control panel
        self.control_panel = None

        self.setWindowTitle("Category Manager")
        self.resize(500, 450)

        self.build_ui()
        self.refresh()

    def build_ui(self):
        layout = QVBoxLayout()

        title = QLabel("CATEGORY MANAGER")
        title.setStyleSheet(
            "font-size: 20px; font-weight: bold;"
        )

        layout.addWidget(title)

        self.input = QLineEdit()
        self.input.setPlaceholderText(
            "Enter category name..."
        )

        layout.addWidget(self.input)

        buttons = QHBoxLayout()

        add_button = QPushButton("Add")
        delete_button = QPushButton("Delete")
        refresh_button = QPushButton("Refresh")

        add_button.clicked.connect(
            self.add_category
        )

        delete_button.clicked.connect(
            self.delete_category
        )

        refresh_button.clicked.connect(
            self.refresh
        )

        buttons.addWidget(add_button)
        buttons.addWidget(delete_button)
        buttons.addWidget(refresh_button)

        layout.addLayout(buttons)

        self.table = QTableWidget(0, 2)

        self.table.setHorizontalHeaderLabels([
            "Category",
            "Items"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        layout.addWidget(self.table)

        self.setLayout(layout)

    # Connect the Category Manager to the inventory controls
    def set_control_panel(self, control_panel):
        self.control_panel = control_panel

        # Refresh the dropdown immediately after connecting
        self.control_panel.refresh_categories()

    def add_category(self):
        try:
            self.service.add_category(
                self.input.text()
            )

            self.input.clear()

            # Refresh the category table and dropdown
            self.refresh()

        except ValueError as error:
            QMessageBox.warning(
                self,
                "Error",
                str(error)
            )

    def delete_category(self):
        row = self.table.currentRow()

        if row < 0:
            QMessageBox.warning(
                self,
                "Error",
                "Select a category."
            )
            return

        name = self.table.item(row, 0).text()

        try:
            self.service.delete_category(name)

            # Refresh the category table and dropdown
            self.refresh()

        except ValueError as error:
            QMessageBox.warning(
                self,
                "Error",
                str(error)
            )

    def refresh(self):
        self.table.setRowCount(0)

        categories = self.service.get_categories()

        for category in categories:
            row = self.table.rowCount()

            self.table.insertRow(row)

            self.table.setItem(
                row,
                0,
                QTableWidgetItem(category.name)
            )

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(
                    str(
                        self.service.get_item_count(
                            category.name
                        )
                    )
                )
            )

        # Automatically update the inventory category dropdown
        if self.control_panel is not None:
            self.control_panel.refresh_categories()