from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox
)

class CalculateView(QWidget):

    def __init__(self, service):
        super().__init__()

        self.service = service
        self.setWindowTitle("Inventory Calculations")
        self.resize(750, 500)
        self.build_ui()
        self.refresh()

    def build_ui(self):

        main_layout = QVBoxLayout()
        title = QLabel("INVENTORY CALCULATIONS")
        title.setStyleSheet(
            "font-size: 20px; font-weight: bold;"
        )

        main_layout.addWidget(title)

        self.table = QTableWidget()

        self.table.setColumnCount(4)

        self.table.setHorizontalHeaderLabels([
            "Category",
            "Quantity",
            "Price",
            "Total Value"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        main_layout.addWidget(self.table)

        summary_layout = QHBoxLayout()

        self.item_count_label = QLabel(
            "Items: 0"
        )

        self.quantity_label = QLabel(
            "Quantity: 0"
        )

        self.value_label = QLabel(
            "Total Value: ₱0.00"
        )

        summary_layout.addWidget(
            self.item_count_label
        )

        summary_layout.addWidget(
            self.quantity_label
        )

        summary_layout.addWidget(
            self.value_label
        )

        main_layout.addLayout(summary_layout)

        button_layout = QHBoxLayout()

        self.refresh_button = QPushButton(
            "Refresh"
        )

        self.close_button = QPushButton(
            "Close"
        )

        self.refresh_button.clicked.connect(
            self.refresh
        )

        self.close_button.clicked.connect(
            self.close
        )

        button_layout.addWidget(
            self.refresh_button
        )

        button_layout.addWidget(
            self.close_button
        )

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def refresh(self):

        try:
            calculations = self.service.get_item_calculations()
            summary = self.service.get_summary()

            self.table.setRowCount(0)

            for calculation in calculations:

                row = self.table.rowCount()

                self.table.insertRow(row)

                self.table.setItem(
                    row,
                    0,
                    QTableWidgetItem(calculation.name)
                )

                self.table.setItem(
                    row,
                    1,
                    QTableWidgetItem(
                        str(calculation.quantity)
                    )
                )

                self.table.setItem(
                    row,
                    2,
                    QTableWidgetItem(
                        f"₱{calculation.price:,.2f}"
                    )
                )

                self.table.setItem(
                    row,
                    3,
                    QTableWidgetItem(
                        f"₱{calculation.total_value:,.2f}"
                    )
                )

            self.item_count_label.setText(
                f"Items: {summary.item_count}"
            )

            self.quantity_label.setText(
                f"Quantity: {summary.total_quantity}"
            )

            self.value_label.setText(
                f"Total Value: ₱{summary.total_value:,.2f}"
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Calculation Error",
                f"An error occurred:\n{error}"
            )