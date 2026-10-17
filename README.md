# Personal Inventory Management System

A desktop inventory application built with **Python**, **PyQt6**, and **SQLite3**. It allows users to maintain inventory records, organize items by category, and demonstrate the **Stack** data structure using existing inventory items.

## Contents

- [Project Overview](#project-overview)
- [Objectives](#objectives)
- [Features](#features)
- [Technologies](#technologies)
- [Project Structure](#project-structure)
- [Installation and Setup](#installation-and-setup)
- [How to Use](#how-to-use)
- [System Design](#system-design)
- [Object-Oriented Programming](#object-oriented-programming)
- [Database Design](#database-design)
- [Parameterized SQL](#parameterized-sql)
- [Testing Checklist](#testing-checklist)
- [Limitations](#limitations)
- [Screenshots](#screenshots)
- [Author](#author)

## Project Overview

The Inventory Management System provides a graphical way to add, view, update, and delete inventory records. Each item stores a name, quantity, price, and category. The application also supports category management and a Stack Management window for demonstrating **LIFO (Last In, First Out)**.

Inventory items and categories are saved in a local SQLite database. The Stack feature is separate from the inventory database: pushing or popping an item changes only the temporary stack and does not create, update, or delete an inventory record.

## Objectives

- Build a functional desktop inventory management application.
- Support Create, Read, Update, and Delete (CRUD) operations for inventory items.
- Let users create and manage inventory categories.
- Store inventory and category information persistently with SQLite3.
- Demonstrate object-oriented and modular programming in Python.
- Demonstrate the Stack data structure and its LIFO behavior.
- Provide a graphical interface using PyQt6.

## Features

### Inventory Management

The Inventory Management window lets users:

- Add an item with a name, quantity, price, and category.
- View saved inventory records in a table.
- Update a selected item's information.
- Delete a selected inventory record.
- Clear the input fields and current selection.
- View each item's calculated value, shown as **quantity × price**.

**Note:** The Clear button clears the form and selection; it does not delete inventory records.

### Category Management

The Category Manager lets users:

- Add new categories.
- View categories and the number of inventory items assigned to each category.
- Delete categories that are not in use.
- Refresh the category list.

The `General` category is created automatically and cannot be deleted. A category that still contains inventory items cannot be deleted. After categories are added or removed, the category dropdown in Inventory Management is refreshed so the changes can be used without restarting the application.

### Stack Management

Stack Management demonstrates **LIFO (Last In, First Out)** using a Python list.

- **Push:** Add a selected existing inventory item to the top of the stack.
- **Pop:** Remove the most recently pushed entry from the stack.
- **Peek:** View the top entry without removing it.
- **Refresh Inventory:** Reload the available inventory items in the selection dropdown.
- **Close:** Close the Stack Management window.

The stack table displays the most recently pushed entry at the top. The Stack feature stores a snapshot of the selected item's ID, name, quantity, price, and category. **Pop only removes the entry from the stack; it does not delete or change the item in the inventory database.**

The stack is held in memory and resets when the application closes. Inventory and category records remain saved in SQLite.

## Technologies

- **Language:** Python 3.10 or newer
- **GUI framework:** PyQt6
- **Database:** SQLite3 (`sqlite3` standard-library module)
- **Data models:** Python `dataclasses`
- **Development tools:** VS Code or PyCharm

## Project Structure

```text
PythonProject/
├── Database/
│   ├── __init__.py
│   └── database.py
├── Features/
│   ├── Management/
│   │   ├── __init__.py
│   │   ├── model.py
│   │   ├── repository.py
│   │   ├── service.py
│   │   └── view.py
│   ├── Category/
│   │   ├── __init__.py
│   │   ├── model.py
│   │   ├── repository.py
│   │   ├── service.py
│   │   └── view.py
│   ├── Control/
│   │   ├── __init__.py
│   │   ├── controller.py
│   │   └── view.py
│   └── Stack/
│       ├── __init__.py
│       ├── model.py
│       ├── repository.py
│       ├── service.py
│       └── view.py
├── main.py
└── README.md
```

Responsibilities of the main folders and files:

- **`Database/database.py`** — creates the SQLite connection and required tables.
- **`Features/Management/`** — defines inventory items and implements inventory database access, validation, and the inventory table.
- **`Features/Category/`** — defines categories and implements category rules, database access, and the category window.
- **`Features/Control/`** — connects inventory control actions to the service and provides the inventory input form.
- **`Features/Stack/`** — defines stack entries and implements Push, Pop, Peek, and the Stack Management window.
- **`main.py`** — creates the shared database/services, connects the views, and starts the application.

If the previous `Features/Calculate/` folder remains in the project directory, it is legacy code and is no longer launched from the current main menu. The active replacement is `Features/Stack/`.

## Installation and Setup

### Requirements

- Python 3.10 or newer
- PyQt6

SQLite3 is included with Python and normally does not need to be installed separately.

### 1. Install Python

Install Python and make sure it is available from your terminal or command prompt.

### 2. Install PyQt6

Open a terminal in the project root—the folder containing `main.py`—and run:

```bash
pip install PyQt6
```

### 3. Run the application

From that same project root, run:

```bash
python main.py
```

The application creates `Database/inventory.db` and its tables automatically when needed.

## How to Use

### Inventory Management

1. Open **Inventory Management** from the main menu.
2. Enter the item name, quantity, and price.
3. Select a category from the dropdown.
4. Click **Add** to save the item.
5. To change a record, select it in the table, edit the fields, and click **Update**.
6. To remove a record, select it and click **Delete**.
7. Use **Clear** to reset the form and selection without deleting the record.

### Category Manager

1. Open **Category Manager**.
2. Enter a category name and click **Add**.
3. The category appears in the category table and becomes available in the Inventory Management dropdown.
4. To remove a category, select it and click **Delete**. Categories that still contain items and the `General` category are protected from deletion.

### Stack Management

1. Open **Stack Management** from the main menu.
2. Select an item from the inventory dropdown.
3. Click **Push** to place a copy of that item's current details on the stack.
4. Click **Peek** to inspect the top entry without removing it.
5. Click **Pop** to remove the top stack entry.
6. Click **Refresh Inventory** to reload the available inventory items.

For example, if the user pushes Pencil, then Paper, then Notebook, Notebook appears at the top and is the next entry removed by Pop. This is the LIFO principle.

## System Design

The application is organized into components with separate responsibilities.

For inventory CRUD operations, the general flow is:

```text
User
  ↓
View
  ↓
Controller
  ↓
Service (validation and business rules)
  ↓
Repository (SQL operations)
  ↓
SQLite database
```

The Stack feature follows a separate in-memory flow:

```text
Stack Management View
  ├── Management Service → retrieves available inventory items
  └── Stack Service → Stack Repository → Python list
```

The Stack Repository does not write stack operations to SQLite. This keeps Push and Pop separate from permanent inventory changes.

## Object-Oriented Programming

The project uses classes and objects to group related information and behavior.

### Models

- **`Item`** — represents an inventory item with its ID, name, quantity, price, and category.
- **`Category`** — represents a category name.
- **`StackEntry`** — stores a snapshot of an inventory item's ID, name, quantity, price, and category while it is in the stack.

The models use Python `dataclasses` to avoid repetitive code when defining data containers.

### Encapsulation

Related operations are kept inside their classes. For example, repository classes contain database or stack-storage operations, while service classes handle application rules.

### Inheritance

The PyQt6 windows inherit from Qt widget classes. For example, `ManagementView` and `StackView` inherit from `QWidget`.

## Database Design

The SQLite database file is located at:

```text
Database/inventory.db
```

### `items` table

| Column | Type | Description |
|---|---|---|
| `id` | INTEGER | Unique inventory item ID; primary key with auto-increment |
| `name` | TEXT | Item name; required |
| `quantity` | INTEGER | Number of units; required |
| `price` | REAL | Price per unit; required |
| `category` | TEXT | Category assigned to the item; required |

### `categories` table

| Column | Type | Description |
|---|---|---|
| `id` | INTEGER | Unique category ID; primary key with auto-increment |
| `name` | TEXT | Category name; required and unique |

The database setup creates both tables if they do not already exist and ensures that the `General` category is present. Inventory items and categories are persistent. The temporary stack is not stored in these tables.

## Parameterized SQL

The repository classes use parameterized SQL statements with `?` placeholders. For example, adding an item uses a statement similar to:

```python
connection.execute(
    """
    INSERT INTO items (name, quantity, price, category)
    VALUES (?, ?, ?, ?)
    """,
    (item.name, item.quantity, item.price, item.category)
)
```

The values are passed separately from the SQL statement. This avoids building queries by directly concatenating user input and helps protect against SQL injection.

## Testing Checklist

Run these checks on the current version and record the actual results before submitting the project.

| Test | Expected result |
|---|---|
| Add a valid inventory item | The item appears in the inventory table and remains after restarting the application. |
| Add an empty item name | A validation message appears and the item is not saved. |
| Enter a negative quantity or price | A validation message appears and the item is not saved. |
| Update an item | The selected item's details change. |
| Delete an item | The selected inventory record is removed. |
| Add a category | The category appears in Category Manager and the inventory dropdown refreshes without restarting. |
| Add a duplicate category | A validation message appears. |
| Delete `General` or a category that still contains items | Deletion is prevented. |
| Push an inventory item | A new entry appears at the top of the stack. |
| Peek at the stack | The top entry is shown and remains in the stack. |
| Pop from the stack | The top stack entry is removed but the inventory record remains. |
| Pop from an empty stack | A message explains that the stack is empty. |
| Close and reopen the application | Inventory and categories remain; the in-memory stack resets. |

## Limitations

- The application does not currently include user authentication or user accounts.
- Advanced inventory search and filtering are not implemented.
- Printable reports are not currently available.
- Automatic low-stock notifications are not implemented.
- The database is designed for local use, not simultaneous multi-user network access.
- Stack contents are temporary and reset when the application closes.
- Stack entries contain a snapshot of an item's details; they do not automatically update if the inventory record changes later.
- Stack operations demonstrate a data structure and do not increase or decrease the inventory quantity.

## Screenshots

Add screenshots captured from the current version of the application before final submission. Recommended screenshots are:

1. **Main Menu** — shows Inventory Management, Category Manager, Stack Management, and Exit.
2. **Inventory Management** — shows the input form and inventory table.
3. **Category Manager** — shows category names and the number of items in each category.
4. **Stack Management** — shows the inventory dropdown, Push/Pop/Peek controls, and stack contents.

Place image files in a `screenshots/` folder and link them here using relative paths, for example `![Main Menu](screenshots/main-menu.png)`.

## Author

**Name:** Allen James A. Paquinol
**Course Code:** 3581 
**Project:** Personal Inventory Management System
