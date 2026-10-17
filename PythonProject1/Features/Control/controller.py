from PyQt6.QtWidgets import QMessageBox


class ControlPanelController:

    def __init__(
        self,
        service,
        management_view,
        category_view=None
    ):
        self.service = service
        self.management_view = management_view
        self.category_view = category_view

    def add_item(
        self,
        name,
        quantity,
        price,
        category
    ):
        try:
            self.service.add_item(
                name,
                quantity,
                price,
                category
            )

            self.management_view.refresh()

            if self.category_view:
                self.category_view.refresh()

            return True

        except (ValueError, TypeError) as error:
            QMessageBox.warning(
                self.management_view,
                "Error",
                str(error)
            )
            return False

    def update_item(
        self,
        item_id,
        name,
        quantity,
        price,
        category
    ):
        try:
            self.service.update_item(
                item_id,
                name,
                quantity,
                price,
                category
            )

            self.management_view.refresh()

            if self.category_view:
                self.category_view.refresh()

            return True

        except (ValueError, TypeError) as error:
            QMessageBox.warning(
                self.management_view,
                "Error",
                str(error)
            )
            return False

    def delete_item(self, item_id):
        try:
            self.service.delete_item(item_id)

            self.management_view.refresh()

            if self.category_view:
                self.category_view.refresh()

            return True

        except (ValueError, TypeError) as error:
            QMessageBox.warning(
                self.management_view,
                "Error",
                str(error)
            )
            return False

    def get_items(self):
        return self.service.get_items()

    def get_categories(self):
        return self.service.get_categories()