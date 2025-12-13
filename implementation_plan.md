# School Library Management System - Implementation Plan

A comprehensive library management system for high school IP project using Python, pandas, matplotlib, and numpy with CSV-based / Mysql data storage.

## Proposed Changes

### Core Application

#### [NEW] [library_management_system.py](file:///Users/raghav/Developer/IP%20Project/library_management_system.py)

Single Python file containing:
- **Menu-driven interface** for librarian operations
- **Book Management Module**:
  - Add new books (Book ID, Title, Author, Publisher, ISBN, Quantity, Category)
  - Delete books
  - Update book details
  - Search books (by title, author, ISBN, category)
  - View all books
- **Member Management Module**:
  - Add new members (Member ID, Name, Class, Contact, Email)
  - Delete members
  - Update member details
  - Search members
  - View all members
- **Issue/Return Module**:
  - Issue books to members (with due date tracking)
  - Return books
  - View issued books
  - Check availability
  - Auto fine calculation for overdue books
- **Reports & Analytics Module**:
  - Most issued books (bar chart using matplotlib)
  - Category-wise distribution (pie chart)
  - Overdue books report
  - Member-wise issue history
  - Monthly statistics
- **Data Management**:
  - Auto-save to CSV files using pandas
  - Load data on startup
  - Data validation and error handling
  - Backup functionality

### Data Files

#### [NEW] [books.csv](file:///Users/raghav/Developer/IP%20Project/books.csv)
CSV file storing book records with columns: BookID, Title, Author, Publisher, ISBN, Quantity, Available, Category

#### [NEW] [members.csv](file:///Users/raghav/Developer/IP%20Project/members.csv)
CSV file storing member records with columns: MemberID, Name, Class, Contact, Email, JoinDate

#### [NEW] [transactions.csv](file:///Users/raghav/Developer/IP%20Project/transactions.csv)
CSV file storing issue/return records with columns: TransactionID, BookID, MemberID, IssueDate, DueDate, ReturnDate, Fine

---

### Documentation

#### [NEW] [LIBRARIAN_MANUAL.md](file:///Users/raghav/Developer/IP%20Project/LIBRARIAN_MANUAL.md)
Comprehensive user manual for librarian including:
- System overview
- How to run the application
- Step-by-step guide for each feature
- Troubleshooting tips
- Sample workflows

#### [NEW] [WORKFLOW.md](file:///Users/raghav/Developer/IP%20Project/WORKFLOW.md)
Daily workflow guide for librarian operations

## Technical Specifications

**Python Libraries Used**:
- `pandas`: Data manipulation and CSV operations
- `matplotlib`: Visualization and charts
- `numpy`: Numerical operations and date calculations
- `datetime`: Date handling for due dates and fines
- `os`: File operations

**Data Storage Strategy**:
- Primary: CSV files (easy to understand for high school level)
- Pandas DataFrames for in-memory operations
- Auto-save after each operation
- Option to export reports

**Fine Calculation**:
- ₹2 per day for overdue books
- Calculated automatically on return

## Verification Plan

### Automated Tests
```bash
# Run the application
cd /Users/raghav/Developer/IP\ Project
python library_management_system.py
```

### Manual Verification
- Test all menu options
- Verify data persistence across sessions
- Check visualization outputs
- Validate fine calculations
- Ensure error handling works properly
