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

from Features.Control.controller import ControlPanelController
from Features.Control.view import ControlPanelView

from Features.Stack.repository import StackRepository
from Features.Stack.service import StackService
from Features.Stack.view import StackView


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

        # Stack is maintained separately in memory
        self.stack_repository = StackRepository()

        self.stack_service = StackService(
            self.stack_repository
        )

    def setup_views(self):
        self.management_view = ManagementView(
            self.management_service
        )

        self.category_view = CategoryView(
            self.category_service
        )

        self.control_controller = ControlPanelController(
            self.management_service,
            self.management_view,
            self.category_view
        )

        self.control_panel = ControlPanelView(
            self.control_controller,
            self.management_view
        )

        self.management_view.set_control_panel(
            self.control_panel
        )

        self.category_view.set_control_panel(
            self.control_panel
        )

        # Replacement for Inventory Calculations
        self.stack_view = StackView(
            self.management_service,
            self.stack_service
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

        stack_button = QPushButton(
            "Stack Management"
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

        stack_button.clicked.connect(
            self.open_stack_view
        )

        exit_button.clicked.connect(
            self.close
        )

        layout.addWidget(management_button)
        layout.addWidget(category_button)
        layout.addWidget(stack_button)
        layout.addWidget(exit_button)

    def open_stack_view(self):
        # Reload inventory items when opening Stack Management
        self.stack_view.refresh_inventory()
        self.stack_view.refresh_stack()
        self.stack_view.show()


app = QApplication(sys.argv)

window = MainView()
window.show()

sys.exit(app.exec())
