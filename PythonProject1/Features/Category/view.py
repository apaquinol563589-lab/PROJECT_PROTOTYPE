from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox
)

class CategoryView(QWidget):

    def __init__(self, service):
        super().__init__()

        self.service = service
        self.setWindowTitle("Category Management")
        self.resize(650, 450)

        self.build_ui()
        self.refresh()

    def build_ui(self):
        layout = QVBoxLayout()

        title = QLabel("CATEGORY MANAGEMENT")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

        # Input
        input_layout = QHBoxLayout()

        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("Enter category name")

        add_button = QPushButton("Add Category")
        add_button.clicked.connect(self.add_category)

        input_layout.addWidget(self.category_input)
        input_layout.addWidget(add_button)
        layout.addLayout(input_layout)

        # Table
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Category", "Items"])
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        layout.addWidget(self.table)

        # Buttons
        buttons = QHBoxLayout()

        delete_button = QPushButton("Delete Category")
        refresh_button = QPushButton("Refresh")
        close_button = QPushButton("Close")

        delete_button.clicked.connect(self.delete_category)
        refresh_button.clicked.connect(self.refresh)
        close_button.clicked.connect(self.close)

        buttons.addWidget(delete_button)
        buttons.addWidget(refresh_button)
        buttons.addWidget(close_button)

        layout.addLayout(buttons)
        self.setLayout(layout)

    def add_category(self):
        try:
            self.service.add_category(
                self.category_input.text()
            )

            self.category_input.clear()
            self.refresh()

        except ValueError as error:
            QMessageBox.warning(self, "Invalid Category", str(error))

    def delete_category(self):
        row = self.table.currentRow()

        if row < 0:
            QMessageBox.warning(
                self,
                "No Selection",
                "Please select a category first."
            )
            return

        name = self.table.item(row, 0).text()

        try:
            self.service.delete_category(name)
            self.refresh()

        except ValueError as error:
            QMessageBox.warning(self, "Cannot Delete", str(error))

    def refresh(self):
        try:
            categories = self.service.get_categories()
            self.table.setRowCount(0)

            for category in categories:
                row = self.table.rowCount()
                self.table.insertRow(row)

                self.table.setItem(
                    row, 0, QTableWidgetItem(category.name)
                )

                count = self.service.get_item_count(category.name)

                self.table.setItem(
                    row, 1, QTableWidgetItem(str(count))
                )

        except Exception as error:
            QMessageBox.critical(
                self,
                "Category Error",
                f"An error occurred:\n{error}"
            )