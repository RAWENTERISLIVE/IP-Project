# Librarian User Manual
## School Library Management System

Welcome to the School Library Management System! This software is designed to help you manage books, members, and daily transactions efficiently.

---

## 1. Getting Started

### Prerequisites
Ensure you have Python installed on your computer along with the required libraries.
To install the required libraries, run:
```bash
pip install pandas matplotlib numpy
```

### Launching the Application
1.  Open your terminal or command prompt.
2.  Navigate to the project folder.
3.  Run the command:
    ```bash
    python library_management_system.py
    ```

---

## 2. Main Menu Overview
The main menu is your central hub. It offers the following options:
1.  **Book Management**: Add, view, search, update, or delete books.
2.  **Member Management**: Register, view, search, update, or delete members.
3.  **Issue/Return Book**: Lend books, accept returns, view issued books, and check availability.
4.  **Reports & Analytics**: View visual charts and detailed reports.
5.  **Backup Data**: Create a secure backup of your data.
6.  **Exit**: Close the program.

---

## 3. Feature Guide

### Book Management
-   **Add Book**: Enter details like Title, Author, ISBN, etc. *Note: Book ID must be unique.*
-   **Search Book**: Find a book by Title, Author, ISBN, or Category.
-   **Update Book**: Modify details of an existing book (e.g., add more quantity).
-   **Delete Book**: Remove a book record permanently using its Book ID.

### Member Management
-   **Add Member**: Register a new user. You will need a unique Member ID, Name, Class, etc.
-   **Search Member**: Find a student by Name or ID.
-   **Update Member**: Change a member's contact details or class.
-   **Delete Member**: Remove a member from the system.

### Issue & Return
-   **Issuing**: The system automatically sets a **7-day** borrowing period. It also checks if the book is currently in stock.
-   **Returning**: The system checks the due date against the current date.
    -   **Fine Calculation**: If returned late, a fine of **₹2.00 per day** is calculated.
-   **View Issued Books**: See a list of all books currently with students.
-   **Check Availability**: Quickly check if a specific book is on the shelf.

### Analytics
-   **Most Issued Books**: Displays a bar chart showing the top 5 most popular books.
-   **Category Distribution**: Displays a pie chart showing the proportion of books in each category.
-   **Overdue Books**: Generates a list of all books that are past their due date.
-   **Member History**: Shows the borrowing history for a specific student.
-   **Monthly Statistics**: Visualizes the number of transactions per month.

### Data Backup
-   Select **Backup Data** to create a timestamped copy of all your CSV files in a `backups` folder. This ensures you never lose data.

---

## 4. Data Storage
All data is stored in CSV files in the same folder as the application:
-   `books.csv`: Inventory of all books.
-   `members.csv`: List of registered members.
-   `transactions.csv`: History of all issues and returns.

**Note**: Do not manually edit these CSV files while the program is running to avoid data corruption.

## 5. Support
If you encounter any errors (e.g., "File not found"), try restarting the application. The system is designed to auto-create missing data files on startup.
