from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
)

class StackView(QWidget):

    def __init__(self, management_service, stack_service):
        super().__init__()

        self.management_service = management_service
        self.stack_service = stack_service
        self.items_by_id = {}

        self.setWindowTitle("Stack Management")
        self.resize(750, 500)

        self.build_ui()
        self.refresh_inventory()
        self.refresh_stack()

    def build_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("STACK MANAGEMENT")
        title.setStyleSheet(
            "font-size: 20px; font-weight: bold;"
        )

        layout.addWidget(title)

        description = QLabel(
            "LIFO: Last In, First Out. "
            "The top item is displayed first."
        )

        layout.addWidget(description)

        selection_layout = QHBoxLayout()

        selection_layout.addWidget(
            QLabel("Inventory Item:")
        )

        self.item_combo = QComboBox()

        selection_layout.addWidget(
            self.item_combo
        )

        layout.addLayout(selection_layout)

        button_layout = QHBoxLayout()

        self.push_button = QPushButton("Push")
        self.pop_button = QPushButton("Pop")
        self.peek_button = QPushButton("Peek")
        self.refresh_button = QPushButton(
            "Refresh Inventory"
        )
        self.close_button = QPushButton("Close")

        self.push_button.clicked.connect(
            self.push_item
        )

        self.pop_button.clicked.connect(
            self.pop_item
        )

        self.peek_button.clicked.connect(
            self.peek_item
        )

        self.refresh_button.clicked.connect(
            self.refresh_inventory
        )

        self.close_button.clicked.connect(
            self.close
        )

        button_layout.addWidget(self.push_button)
        button_layout.addWidget(self.pop_button)
        button_layout.addWidget(self.peek_button)
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.close_button)

        layout.addLayout(button_layout)

        self.stack_count_label = QLabel(
            "Stack size: 0"
        )

        layout.addWidget(self.stack_count_label)

        self.table = QTableWidget(0, 5)

        self.table.setHorizontalHeaderLabels([
            "Item ID",
            "Name",
            "Category",
            "Quantity",
            "Price"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        layout.addWidget(self.table)

    def refresh_inventory(self):
        selected_id = self.item_combo.currentData()

        self.item_combo.clear()
        self.items_by_id.clear()

        items = self.management_service.get_items()

        for item in items:
            if item.id is None:
                continue

            self.items_by_id[item.id] = item

            self.item_combo.addItem(
                f"{item.name} (ID: {item.id})",
                item.id
            )

        if not self.items_by_id:
            self.item_combo.addItem(
                "No inventory items available",
                None
            )

        elif selected_id in self.items_by_id:
            index = self.item_combo.findData(selected_id)

            if index >= 0:
                self.item_combo.setCurrentIndex(index)

    def push_item(self):
        item_id = self.item_combo.currentData()

        if item_id is None:
            QMessageBox.warning(
                self,
                "Stack Error",
                "Please select an inventory item."
            )
            return

        item = self.items_by_id.get(item_id)

        if item is None:
            QMessageBox.warning(
                self,
                "Stack Error",
                "Please refresh the inventory list."
            )
            return

        try:
            self.stack_service.push(item)
            self.refresh_stack()

        except ValueError as error:
            QMessageBox.warning(
                self,
                "Stack Error",
                str(error)
            )

    def pop_item(self):
        try:
            removed = self.stack_service.pop()

            self.refresh_stack()

            QMessageBox.information(
                self,
                "Item Popped",
                f"Removed from stack: {removed.name}\n\n"
                "The inventory record was not deleted."
            )

        except ValueError as error:
            QMessageBox.warning(
                self,
                "Stack Error",
                str(error)
            )

    def peek_item(self):
        try:
            item = self.stack_service.peek()

            QMessageBox.information(
                self,
                "Top of Stack",
                f"Name: {item.name}\n"
                f"Item ID: {item.item_id}\n"
                f"Category: {item.category}\n"
                f"Quantity: {item.quantity}\n"
                f"Price: ₱{item.price:,.2f}"
            )

        except ValueError as error:
            QMessageBox.warning(
                self,
                "Stack Error",
                str(error)
            )

    def refresh_stack(self):
        entries = self.stack_service.get_stack()

        self.table.setRowCount(len(entries))

        for row, entry in enumerate(entries):
            values = [
                str(entry.item_id),
                entry.name,
                entry.category,
                str(entry.quantity),
                f"₱{entry.price:,.2f}"
            ]

            for column, value in enumerate(values):
                self.table.setItem(
                    row,
                    column,
                    QTableWidgetItem(value)
                )

        self.stack_count_label.setText(
            f"Stack size: {len(entries)}"
        )
