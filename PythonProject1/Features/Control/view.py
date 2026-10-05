from PyQt6.QtWidgets import (
    QFormLayout,
    QLineEdit,
    QComboBox,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QMessageBox,
)


class ControlPanelView(QWidget):

    def __init__(self, controller, management_view):
        super().__init__()

        self.controller = controller
        self.management_view = management_view

        self.build_ui()
        self.refresh_categories()

    def build_ui(self):
        layout = QVBoxLayout(self)

        form = QFormLayout()

        self.name_input = QLineEdit()
        self.quantity_input = QLineEdit()
        self.price_input = QLineEdit()
        self.category_input = QComboBox()

        form.addRow("Name:", self.name_input)
        form.addRow("Quantity:", self.quantity_input)
        form.addRow("Price:", self.price_input)
        form.addRow("Category:", self.category_input)

        layout.addLayout(form)

        buttons = QHBoxLayout()

        add_button = QPushButton("Add")
        update_button = QPushButton("Update")
        delete_button = QPushButton("Delete")
        clear_button = QPushButton("Clear")

        add_button.clicked.connect(self.add_item)
        update_button.clicked.connect(self.update_item)
        delete_button.clicked.connect(self.delete_item)
        clear_button.clicked.connect(self.clear)

        buttons.addWidget(add_button)
        buttons.addWidget(update_button)
        buttons.addWidget(delete_button)
        buttons.addWidget(clear_button)

        layout.addLayout(buttons)

    def add_item(self):
        success = self.controller.add_item(
            self.name_input.text(),
            self.quantity_input.text(),
            self.price_input.text(),
            self.category_input.currentText()
        )

        if success:
            self.clear()

    def update_item(self):
        row = self.management_view.table.currentRow()

        if row < 0:
            QMessageBox.warning(
                self,
                "Error",
                "Select an item to update."
            )
            return

        item_id = int(
            self.management_view.table.item(row, 0).text()
        )

        success = self.controller.update_item(
            item_id,
            self.name_input.text(),
            self.quantity_input.text(),
            self.price_input.text(),
            self.category_input.currentText()
        )

        if success:
            self.clear()

    def delete_item(self):
        row = self.management_view.table.currentRow()

        if row < 0:
            QMessageBox.warning(
                self,
                "Error",
                "Select an item to delete."
            )
            return

        item_id = int(
            self.management_view.table.item(row, 0).text()
        )

        success = self.controller.delete_item(item_id)

        if success:
            self.clear()

    def load_selected_item(self):
        row = self.management_view.table.currentRow()

        if row < 0:
            return

        self.name_input.setText(
            self.management_view.table.item(row, 1).text()
        )

        self.quantity_input.setText(
            self.management_view.table.item(row, 3).text()
        )

        self.price_input.setText(
            self.management_view.table.item(row, 4)
            .text()
            .replace("₱", "")
            .replace(",", "")
        )

        self.category_input.setCurrentText(
            self.management_view.table.item(row, 2).text()
        )

    def refresh_categories(self):
        self.category_input.clear()

        categories = self.controller.get_categories()

        self.category_input.addItems([
            category.name
            for category in categories
        ])

    def clear(self):
        self.name_input.clear()
        self.quantity_input.clear()
        self.price_input.clear()
        self.management_view.table.clearSelection()