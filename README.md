# CoreBank - Comprehensive Bank Management System

**Version**: 2.0  
**Status**: Production Ready  
**Type**: Educational High School IP Project

---

## Quick Start

### 1. Installation (2 minutes)

```bash
# Install required libraries
pip install pandas matplotlib numpy

# Navigate to project directory
cd "/path/to/IP Project"

# Run the application
python bank_management_system.py
```

### 2. First Login

```
Username: admin
Password: admin@123
```

### 3. Try These Steps

1. **Add a Customer**
   - Main Menu → Option 1 (Add Customer)
   - Enter name, DOB, PAN, Aadhar, phone, email
   - Get Customer ID (e.g., CUST001)

2. **Open an Account**
   - Main Menu → Option 2 (Open Account)
   - Enter Customer ID
   - Select account type (Savings recommended)
   - Enter initial deposit (₹5000 minimum)
   - Get Account Number (e.g., ACC1001)

3. **Deposit Money**
   - Main Menu → Option 3 (Deposit)
   - Enter Account Number (ACC1001)
   - Enter amount (₹10000)
   - See confirmation

4. **Check Balance**
   - Main Menu → Option 5 (Check Balance)
   - Enter Account Number
   - View updated balance

5. **Apply for Loan**
   - Main Menu → Option 6 (Apply Loan)
   - Enter Customer ID
   - Select loan type (Personal Loan)
   - Enter amount and tenure

6. **View Reports & Analytics**
   - Main Menu → Option 8 (Reports & Analytics)
   - Select report type:
     - Transaction History (by account)
     - Bank Financial Summary
     - Customer Balances
     - Account Distribution Chart (Pie)
     - Loan Portfolio Chart (Bar)
   - Get Loan ID and EMI calculation

---

## System Overview

### What This System Does

**Customer Management**
- Register customers with full KYC details
- Store: Name, DOB, Gender, PAN, Aadhar, Contact
- Search, update, and delete customers
- Track KYC verification status

**Account Management**
- Open multiple account types: Savings, Current, Fixed Deposit
- Track balance and interest accrual
- Support account linking to loans
- Generate account statements

**Transaction Processing**
- Deposit and withdraw money
- Transfer funds between accounts
- Validate balance and limits
- Create audit trail of all transactions

**Loan Management**
- Apply for 5 types of loans: Home, Personal, Car, Education, Business
- Auto-calculate monthly EMI using financial formulas
- Track loan approval and disbursement
- Record and validate EMI payments
- Generate amortization schedules

**Analytics Dashboard**
- View customer count, account summary
- Monitor total balance and loan portfolio
- Track active and total loans
- Check transaction volume

---

## File Organization

```
Project Root/
│
├── bank_management_system.py      ← RUN THIS FILE (Main App - Single File)
├── bank_database.csv              ← SINGLE DATABASE FILE (Stores all data)
│
├── Documentation/                 (User Guides & Technical Docs)
│   ├── README.md
│   ├── BANK_STAFF_MANUAL.md
│   ├── CUSTOMER_GUIDE.md
│   └── TECHNICAL.md
│
└── backups/                       (Auto-created backups)
```

│   └── ... (8 CSV files total)
│
├── backups/                       (Auto-created backups)
│   └── backup_YYYYMMDD_HHMMSS/
│
├── Documentation/
│   ├── README.md                  (This file)
│   ├── BANK_STAFF_MANUAL.md      (Staff user guide)
│   ├── CUSTOMER_GUIDE.md         (Customer guide)
│   ├── TECHNICAL.md              (Technical details)
│   └── bank_implementation_plan.md
│
└── old_library_system/           (Previous project - archived)
```

---

## Features at a Glance

### Core Features
- ✅ Customer registration with 15 data fields
- ✅ 3 account types with interest calculations
- ✅ Real-time transaction processing
- ✅ 5 loan types with EMI calculations
- ✅ Secure password and PIN hashing
- ✅ Automatic daily/weekly backups
- ✅ CSV-based data persistence
- ✅ Role-based access control (Admin, Manager, Teller)

### Calculations
- ✅ EMI (Equated Monthly Installment) with exact formula
- ✅ Interest accrual for savings accounts
- ✅ FD (Fixed Deposit) maturity calculations
- ✅ Amortization schedules
- ✅ Credit score simulation
- ✅ Fine calculations for overdue amounts

### Security
- ✅ SHA256 password hashing
- ✅ PIN hashing for transactions
- ✅ Sensitive data masking (PAN, Aadhar, Card numbers)
- ✅ Audit logging of all operations
- ✅ Input validation for all fields
- ✅ Balance validation before transactions

### Data Management
- ✅ Automatic CSV file creation
- ✅ Data loading/saving for persistence
- ✅ Timestamped backups
- ✅ Orphan record detection
- ✅ Transaction rollback capability
- ✅ Data integrity checks

---

## How the System Works

### 1. Data Storage

Data is stored in **CSV files** (easy to understand, no database needed):
- `customers.csv` → Customer information
- `accounts.csv` → Account details
- `transactions.csv` → All deposits/withdrawals
- `loans.csv` → Loan applications
- `loan_payments.csv` → EMI payment history
- ... and more

**When you run the app**:
1. App checks if CSV files exist
2. If not, creates empty files with headers
3. Loads data into memory (Pandas DataFrames)
4. After every operation, saves back to CSV

### 2. User Flow

```
Start App
  ↓
[Data Initialization & Loading]
  ↓
[Login Screen]
  ↓
[Main Menu with 6 Options]
  ├─→ Customer Management (5 operations)
  ├─→ Account Management (3 operations)
  ├─→ Transactions (5 operations)
  ├─→ Loan Management (4 operations)
  ├─→ Backup Data
  └─→ Exit
  
Each Operation:
  ├─ Input Validation (format, range checks)
  ├─ Business Logic (calculations, rules)
  ├─ Data Update (modify DataFrames)
  ├─ CSV Save (persist changes)
  └─ Confirmation (show results)
```

### 3. Transaction Example

```
Customer wants to transfer ₹1000 from ACC1001 to ACC1002

App does:
1. Validate both accounts exist
2. Check ACC1001 has ₹1000 + minimum balance
3. Deduct ₹1000 from ACC1001
4. Add ₹1000 to ACC1002
5. Create transfer record with ID, date, status
6. Create 2 transaction records (Debit & Credit)
7. Save all 3 DataFrames to CSV
8. Display confirmation with new balances
```

### 4. Loan EMI Example

```
Customer applies for ₹2,00,000 Personal Loan for 36 months

App calculates:
P = 2,00,000 (Principal)
R = 12.0% annual = 1.0% monthly = 0.01 monthly rate
N = 36 months

Using Formula: EMI = [P × R × (1+R)^N] / [(1+R)^N - 1]
Result: EMI = ₹6,644 per month

App displays:
- Loan ID: LOAN001
- Monthly EMI: ₹6,644
- Total amount to pay: ₹2,39,184
- Total interest: ₹39,184
- Status: Pending Approval
```

---

## Key Concepts Explained

### EMI (Equated Monthly Installment)
- Fixed monthly payment for a loan
- Includes both principal and interest
- Calculated using mathematical formula
- Same amount every month

### Interest Rate
- Annual percentage (e.g., 4% means ₹4 per ₹100 per year)
- Different for different products:
  - Savings: 4% p.a.
  - Personal Loan: 12% p.a.
  - Home Loan: 8.5% p.a.

### Minimum Balance
- Least amount you must keep in account
- Savings: ₹1,000
- Current: ₹5,000
- Cannot withdraw below this

### Outstanding Loan Amount
- Principal amount remaining (not yet paid)
- Decreases with each EMI payment
- When zero, loan is closed

### Daily Withdrawal Limit
- Maximum you can withdraw in one day: ₹50,000
- Prevents fraud and protects system
- Can apply for higher limit in person

---

## Important Limits & Rules

| Item | Value | Notes |
|---|---|---|
| Min Balance (Savings) | ₹1,000 | Must maintain always |
| Min Balance (Current) | ₹5,000 | Must maintain always |
| Daily Withdraw Limit | ₹50,000 | Max per day |
| Large Transaction | ₹1,00,000+ | Flagged for review |
| Savings Interest | 4.0% p.a. | Credited monthly |
| FD Interest | 7.5% p.a. | On maturity |
| Loan Tenure | 12-240 months | Depends on type |

---

## Validation Rules

The system validates all inputs:

| Input | Rule |
|---|---|
| PAN | Exactly 10 chars: 5 letters + 4 digits + 1 letter |
| Aadhar | Exactly 12 digits |
| Phone | Exactly 10 digits |
| Email | Valid format with @ and . |
| Amount | Must be positive number |
| Date | Format YYYY-MM-DD |

**Invalid input is rejected** - User must enter again

---

## Real-World Workflow Example

### Day 1: Opening an Account

```
Customer: "I want to open a Savings Account"

Teller:
1. "What is your name?" → Customer: "Raghav"
2. "DOB?" → "2005-08-15"
3. "PAN?" → "ABCDE1234F"
4. "Aadhar?" → "123456789012"
5. "Phone?" → "9876543210"
6. "Email?" → "raghav@email.com"
7. "Initial deposit?" → "₹5000"

System:
- Creates CUST001
- Creates ACC1001
- Sets Balance = ₹5000
- Status = Active
- Saves to CSV

Teller: "Your account is ready! 
- Customer ID: CUST001
- Account Number: ACC1001
- Balance: ₹5000"
```

### Day 5: Earning Interest

```
System (automatic, behind the scenes):
- Reads Savings accounts from accounts.csv
- Calculates: 5000 × 4% ÷ 12 = ₹16.67
- Adds to balance: 5000 + 16.67 = ₹5016.67
- Updates accounts.csv
- Creates transaction record
```

### Day 10: Applying for Loan

```
Customer: "I want to borrow ₹2,00,000"

Teller:
1. "Customer ID?" → "CUST001"
2. "Loan type?" → "Personal Loan"
3. "How long?" → "36 months"

System:
- Calculates EMI = ₹6,644
- Creates LOAN001
- Status = Pending Approval
- Saves to loans.csv

Manager (next day):
- Views pending loans
- Approves LOAN001
- System adds ₹2,00,000 to ACC1001
- Status = Active
```

### Day 31: First EMI Payment

```
System (automatic):
- Reads LOAN001
- EMI = ₹6,644
- Checks ACC1001 balance
- Deducts ₹6,644
- Calculates: 5000 in principal, 1644 in interest
- Updates: Outstanding = ₹1,95,356
- Records payment in loan_payments.csv
- Creates transaction record
- Sends notification
```

---

## Running the Application

### Step 1: Open Terminal
```bash
cd "/Users/raghav/Developer/IP Project"
```

### Step 2: Run Python
```bash
python bank_management_system.py
```

### Step 3: See This Output
```
==============================================================
          COREBANK - Bank Management System v2.0
==============================================================

Enter username (default: admin): [Press Enter]
Enter password (default: admin@123): [Press Enter]
✓ Login successful!

============================================================
                  COREBANK DASHBOARD
============================================================

Total Customers: 5
Total Accounts: 7
Total Balance in System: ₹2,45,000.00

Loan Portfolio:
  Active Loans: 2
  Total Loans: 4
  Total Outstanding: ₹25,00,000.00

Transactions: 12

============================================================

--- Main Menu ---
1. Customer Management
2. Account Management
3. Transaction Processing
4. Loan Management
5. Backup Data
6. Exit

Select option: [Type option number]
```

### Step 4: Explore

- Try adding a customer
- Open an account
- Make transactions
- Apply for a loan

**All data is automatically saved** - Close and reopen, your data is still there!

---

## Documentation

Read these files for detailed information:

1. **BANK_STAFF_MANUAL.md**
   - How staff use the system
   - Step-by-step procedures
   - Troubleshooting tips

2. **CUSTOMER_GUIDE.md**
   - For bank customers
   - Account types explained
   - How loans work
   - FAQ section

3. **TECHNICAL.md**
   - For developers
   - Code architecture
   - Algorithm explanations
   - How to modify system

4. **bank_implementation_plan.md**
   - Complete feature specifications
   - Module descriptions
   - Testing guidelines

---

## Sample Data

The system comes with sample data in `data/` directory:
- 5 sample customers
- 7 sample accounts
- 8 sample transactions
- 4 sample loans

**Use these to learn the system before adding your own data.**

---

## Tips & Tricks

### Backup Your Data
```
From Main Menu → Option 5 (Backup Data)
Creates: backups/backup_YYYYMMDD_HHMMSS/
```

### Check Customer Information
```
Option 1 (Customer) → Option 2 (View All Customers)
Shows all customers with status
```

### View Account Statement
```
Option 3 (Transactions) → Option 5 (Account Statement)
Shows balance and recent transactions
```

### Verify Loan EMI
```
Apply loan → See calculated EMI
Tells you exact amount you'll pay monthly
```

---

## Troubleshooting

### Issue: "Customer not found"
**Solution**: Add customer first (Option 1 → 1)

### Issue: "Insufficient balance"
**Solution**: Check available balance; deposit money first

### Issue: "Invalid PAN format"
**Solution**: PAN must be 10 chars like ABCDE1234F

### Issue: Data not saving
**Solution**: Check if `data/` folder exists and is writable

### Issue: EMI calculation seems high
**Solution**: EMI includes interest; check with calculator

---

## Project Statistics

| Metric | Value |
|---|---|
| Total Lines of Code | 1560+ |
| Main App | 1200+ lines |
| Utility Modules | 300+ lines |
| Data Files | 10 CSV formats |
| Features | 20+ operations |
| Supported Accounts | 3 types |
| Supported Loans | 5 types |
| Documentation | 4 files |

---

## What You Learned

Building this system teaches you:

✅ **Python Programming**
- File I/O (reading/writing CSV)
- Data structures (Lists, Dictionaries, DataFrames)
- Functions and modular code
- Error handling and validation
- Control flow (if/else, loops)

✅ **Data Management**
- CSV file format
- Pandas DataFrames
- Data persistence
- Backup strategies

✅ **Financial Concepts**
- Interest calculations
- EMI formulas
- Loan amortization
- Credit scoring

✅ **Software Design**
- Modular architecture
- User interfaces (CLI)
- Input validation
- Security (hashing)
- Audit logging

✅ **Real-World Applications**
- Banking operations
- Customer management
- Transaction processing
- Loan management

---

## Next Steps

### Learn More
- Explore TECHNICAL.md for deeper understanding
- Read code comments in bank_management_system.py
- Experiment with modifying config.py values

### Enhance the System
- Add interest auto-crediting for savings
- Create card management features
- Add cheque processing
- Build a web interface (optional)

### Test Thoroughly
- Create test customers
- Open multiple accounts
- Transfer between accounts
- Apply and pay loans
- Check data persistence (close/reopen app)

---

## Support

If you have questions:
1. Read the relevant documentation file
2. Check TECHNICAL.md for technical details
3. Review code comments
4. Test with sample data
5. Use validation error messages as guides

---

**Thank you for using CoreBank!**

**Questions?** Review the documentation or modify config.py for your needs.

**Version**: 2.0 | **Status**: Production Ready | **Date**: December 2025
