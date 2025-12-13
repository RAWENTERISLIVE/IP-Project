# Librarian Daily Workflow

This document outlines the standard operating procedures for the School Library Management System.

## Daily Routine

### 1. Start of Day
1.  **Launch the System**: Open your terminal/command prompt and run the application:
    ```bash
    python library_management_system.py
    ```
2.  **Check Overdue Books**: Go to **Option 4 (Reports & Analytics) -> 3 (Overdue Books Report)** to see a list of students who need to return books.

### 2. During School Hours

#### Issuing Books
When a student comes to borrow a book:
1.  Select **Option 3 (Issue/Return Book) -> 1 (Issue Book)**.
2.  Ask for the **Book ID** (found on the book) and the student's **Member ID**.
3.  The system will automatically check availability and assign a due date (7 days from today).
4.  Confirm the issue success message.

#### Returning Books
When a student returns a book:
1.  Select **Option 3 -> 2 (Return Book)**.
2.  Enter the **Book ID** and **Member ID**.
3.  **Collect Fines**: If the book is overdue, the system will calculate the fine (₹2/day). Collect the amount from the student before completing the return.

#### Managing Inventory
-   **New Arrivals**: Use **Option 1 -> 1 (Add Book)** to enter details of new books purchased.
-   **Updates**: Use **Option 1 -> 4 (Update Book Details)** if you need to correct a title or add more quantity.
-   **Lost/Damaged Books**: Use **Option 1 -> 5 (Delete Book)** to remove books that are no longer in circulation.

#### Managing Members
-   **New Admissions**: Use **Option 2 -> 1 (Add Member)** to register new students or staff.
-   **Updates**: Use **Option 2 -> 4 (Update Member Details)** to change contact info or class.

### 3. End of Day
1.  **View Reports**: Select **Option 4 (Reports & Analytics)** to see:
    -   Which books are most popular (Bar Chart).
    -   The distribution of books by category (Pie Chart).
    -   Monthly transaction statistics.
2.  **Data Backup**: Select **Option 5 (Backup Data)**. This will create a timestamped copy of your data files in the `backups` folder.
3.  **Exit**: Select **Option 6** to close the application safely.

## Troubleshooting
-   **"Book ID already exists"**: You are trying to add a book with an ID that is already in the database. Use a unique ID.
-   **"Member not found"**: Ensure the student is registered. If not, go to Member Management and add them first.
-   **"Book not available"**: All copies of this book are currently issued out.
