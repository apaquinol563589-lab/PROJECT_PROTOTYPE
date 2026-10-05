import sys

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
)

from Database.database import Database

from Features.Management.repository import ManagementRepository
from Features.Management.service import ManagementService
from Features.Management.view import ManagementView

from Features.Category.repository import CategoryRepository
from Features.Category.service import CategoryService
from Features.Category.view import CategoryView

from Features.Calculate.repository import CalculateRepository
from Features.Calculate.service import CalculateService
from Features.Calculate.view import CalculateView

from Features.Control.controller import ControlPanelController
from Features.Control.view import ControlPanelView


class MainView(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Inventory Management System")
        self.resize(450, 350)

        self.setup_services()
        self.setup_views()
        self.build_ui()

    def setup_services(self):
        self.database = Database()

        self.management_repository = ManagementRepository(
            self.database
        )

        self.category_repository = CategoryRepository(
            self.database
        )

        self.management_service = ManagementService(
            self.management_repository,
            self.category_repository
        )

        self.category_service = CategoryService(
            self.category_repository,
            self.management_repository
        )

        self.calculate_repository = CalculateRepository(
            self.management_repository
        )

        self.calculate_service = CalculateService(
            self.calculate_repository
        )

    def setup_views(self):
        self.management_view = ManagementView(
            self.management_service
        )

        self.control_controller = ControlPanelController(
            self.management_service,
            self.management_view
        )

        self.control_panel = ControlPanelView(
            self.control_controller,
            self.management_view
        )

        self.management_view.set_control_panel(
            self.control_panel
        )

        self.category_view = CategoryView(
            self.category_service
        )

        self.calculate_view = CalculateView(
            self.calculate_service
        )

    def build_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel(
            "INVENTORY MANAGEMENT SYSTEM"
        )

        title.setStyleSheet(
            "font-size: 20px; font-weight: bold;"
        )

        layout.addWidget(title)

        management_button = QPushButton(
            "Inventory Management"
        )

        category_button = QPushButton(
            "Category Manager"
        )

        calculate_button = QPushButton(
            "Calculations"
        )

        exit_button = QPushButton(
            "Exit"
        )

        management_button.clicked.connect(
            self.management_view.show
        )

        category_button.clicked.connect(
            self.category_view.show
        )

        calculate_button.clicked.connect(
            self.calculate_view.show
        )

        exit_button.clicked.connect(
            self.close
        )

        layout.addWidget(management_button)
        layout.addWidget(category_button)
        layout.addWidget(calculate_button)
        layout.addWidget(exit_button)


app = QApplication(sys.argv)

window = MainView()
window.show()

sys.exit(app.exec())