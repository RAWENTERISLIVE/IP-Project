# 🚀 CoreBank v4.0 - Complete Feature Reference

**Last Updated**: December 14, 2025  
**Total Features**: 50+  
**Menu Options**: 18  
**Report Types**: 6  

---

## 📋 Menu Structure (18 Options)

### Customer & Account Management (Options 1-4)
```
1. Add Customer
   └─ Collects: Name, DOB, Gender, PAN, Aadhar
   └─ Generates: Customer ID (CUST001, CUST002, ...)
   └─ Sets Status: Active, KYC Pending

2. View Customers
   └─ Lists all registered customers
   └─ Shows: ID, Name, Email, Phone, Status

3. Open Account
   └─ Account Types: Savings (4%), Current (0%), FD (7.5%)
   └─ Generates: Account Number (ACC1001, ACC1002, ...)
   └─ Requires: Minimum initial deposit

4. Check Balance
   └─ Shows: Current balance, Interest rate, Status
   └─ Shows: Account type and holder name
```

### Transaction Management (Options 5-7)
```
5. Deposit Money
   └─ Input: Account number, Amount
   └─ Updates: Balance, Creates transaction record
   └─ Minimum deposit: ₹100

6. Withdraw Money
   └─ Input: Account number, Amount
   └─ Validates: Minimum balance enforcement
   └─ Daily limit: ₹50,000

7. Fund Transfer ⭐
   └─ Transfer types: Same customer, Different customer
   └─ Daily limit: ₹2,00,000
   └─ Validates: Source/destination accounts exist
   └─ Deducts: Transfer charge (if applicable)
   └─ Creates: Transfer record + Audit log
```

### Loan Management (Option 8 - Submenu)
```
8. Loan Menu
   ├─ 1. Apply for Loan
   │   ├─ Select loan type: Home (8.5%), Personal (12.0%),
   │   │                  Car (9.5%), Education (7.5%),
   │   │                  Business (11.0%)
   │   ├─ Input: Amount, Tenure (months)
   │   ├─ Calculates: Monthly EMI using formula
   │   ├─ Generates: Loan ID (LOAN001, ...)
   │   └─ Status: Active, pending approval
   │
   ├─ 2. Pay Loan EMI
   │   ├─ Input: Loan ID, Payment amount
   │   ├─ Updates: Outstanding amount
   │   ├─ Records: Payment date and amount
   │   └─ Marks: Loan as Closed if fully paid
   │
   ├─ 3. View Loan Details
   │   ├─ Shows: Principal, Rate, EMI, Outstanding
   │   ├─ Shows: Payment history
   │   └─ Shows: Remaining tenure
   │
   ├─ 4. View All Loans
   │   └─ Lists: All loans with status
   │
   └─ 5. Back to Main Menu
```

### Card Management (Option 9 - Submenu)
```
9. Card Management
   ├─ 1. Issue Card
   │   ├─ Card types: Debit, Credit, Premium Credit
   │   ├─ Auto-generates: 16-digit card number
   │   ├─ Auto-generates: 3-digit CVV
   │   ├─ Sets: Activation required
   │   └─ Generates: Card ID (CARD001, ...)
   │
   ├─ 2. View Cards
   │   ├─ Shows: Card number (masked), Card type
   │   ├─ Shows: Expiry, CVV, Status
   │   └─ Shows: Daily limit remaining
   │
   ├─ 3. Activate Card
   │   ├─ Input: Card number
   │   ├─ Sets: Active status
   │   └─ Enables: Transactions
   │
   ├─ 4. Block Card
   │   ├─ Input: Card number
   │   ├─ Sets: Blocked status
   │   └─ Disables: All transactions
   │
   └─ 5. Back to Main Menu
```

### Cheque Processing (Option 10 - Submenu)
```
10. Cheque Processing
    ├─ 1. Issue Cheque
    │   ├─ Auto-generates: Cheque number
    │   ├─ Input: Payee name, Amount
    │   ├─ Validates: Balance ≥ Amount
    │   ├─ Sets: Status = "Issued"
    │   └─ Generates: CHEQUE001, CHEQUE002, ...
    │
    ├─ 2. Clear Cheque
    │   ├─ Input: Cheque number
    │   ├─ Updates: Cheque status to "Cleared"
    │   ├─ Sets: Clearance date
    │   └─ Records: Clearing transaction
    │
    ├─ 3. View Cheques
    │   ├─ Shows: All issued cheques
    │   ├─ Shows: Cheque number, payee, amount, status
    │   └─ Shows: Clearance date (if cleared)
    │
    └─ 5. Back to Main Menu
```

### Advanced Features (Options 11-14) ⭐ NEW
```
11. Account Statement
    ├─ Input: Account number
    ├─ Displays: Account holder, account type
    ├─ Shows: Current balance, interest rate
    ├─ Lists: Last 10 transactions with dates
    ├─ Shows: Balance after each transaction
    └─ Professional formatting with headers

12. Interest Calculator ⭐
    ├─ Input: Account number, months to calculate
    ├─ Calculates: Simple interest
    │   └─ Formula: (Balance × Rate × Months) / (100 × 12)
    ├─ Calculates: Compound interest (quarterly)
    │   └─ Formula: P × (1 + R/(100×4))^(M/3) - P
    ├─ Shows: Final balance for both
    └─ Comparison display

13. Financial Dashboard ⭐
    ├─ Input: Customer ID
    ├─ Displays: Customer overview
    ├─ Shows: Total accounts, total balance
    ├─ Shows: Total loans, total outstanding
    ├─ Shows: Cards issued, transaction count
    ├─ Calculates: Net worth (Assets - Liabilities)
    ├─ Shows: Debt-to-assets ratio
    ├─ Lists: Account breakdown by type
    ├─ Displays: Credit score with rating
    └─ Professional formatted dashboard

14. Compare Loan Offers ⭐
    ├─ Input: Desired amount, tenure
    ├─ Shows: All 5 loan types side-by-side
    ├─ Displays: Interest rate for each
    ├─ Calculates: Monthly EMI for each
    ├─ Calculates: Total amount payable
    ├─ Calculates: Total interest cost
    └─ Helps in informed decision making
```

### Reports & Utilities (Options 15-18)
```
15. Reports & Analytics (Submenu)
    ├─ 1. Transaction History Report
    │   ├─ Input: Account number
    │   └─ Shows: All transactions with dates and amounts
    │
    ├─ 2. Bank Summary Report
    │   ├─ Total customers
    │   ├─ Total accounts & balance
    │   ├─ Total loans & outstanding
    │   ├─ Total cards issued
    │   └─ Average account balance
    │
    ├─ 3. Customer Balances
    │   └─ Lists: All customers with total balance
    │
    ├─ 4. Account Distribution (Pie Chart)
    │   └─ Visual: Distribution of account types
    │
    ├─ 5. Loan Portfolio (Bar Chart)
    │   └─ Visual: Outstanding loan amounts by type
    │
    ├─ 6. Monthly Trends (Line Chart)
    │   └─ Visual: Transaction trends over months
    │
    ├─ 7. Credit Score Display
    │   ├─ Shows: Credit score for each customer
    │   ├─ Shows: Rating (Excellent/Good/Fair/Poor)
    │   └─ Based on: Balance, loans, activity
    │
    ├─ 8. View Audit Log
    │   ├─ Shows: All system operations
    │   ├─ Shows: Timestamp, operation type, details
    │   └─ Last 50 audit entries
    │
    └─ 9. Back to Main Menu

16. Backup Data
    ├─ Creates: Timestamped backup
    ├─ Format: bank_database_YYYYMMDD_HHMMSS.csv
    ├─ Location: backups/ directory
    └─ Message: Confirmation with timestamp

17. Search Customer
    ├─ Input: Customer name or ID
    ├─ Shows: Matching customer(s)
    ├─ Displays: Full customer details
    └─ Quick lookup

18. Exit
    ├─ Saves all data
    ├─ Displays goodbye message
    └─ Graceful shutdown
```

---

## 🔧 Core Functions Reference

### Customer Management Functions
- `add_customer(data)` - Register new customer
- `view_customers(data)` - List all customers
- `search_customer(data)` - Find customer by name/ID
- `get_customer_id()` - Auto-generate customer ID

### Account Functions
- `open_account(data)` - Create new account
- `check_balance(data)` - View account balance
- `get_account_id()` - Auto-generate account number
- `calculate_account_interest()` - Interest calculation

### Transaction Functions
- `deposit_money(data)` - Deposit operation
- `withdraw_money(data)` - Withdrawal operation
- `transfer_funds(data)` - Inter-account transfer
- `log_transaction()` - Record transaction

### Loan Functions
- `apply_loan(data)` - Apply for loan
- `pay_loan_emi(data)` - Pay EMI
- `view_loan_details(data)` - View loan info
- `calculate_emi(amount, rate, tenure)` - EMI calculation
- `generate_amortization_schedule()` - Payment schedule
- `calculate_credit_score()` - Dynamic scoring

### Card Functions
- `issue_card(data)` - Issue new card
- `view_cards(data)` - View cards
- `activate_card(data)` - Activate card
- `block_card(data)` - Block card
- `generate_card_number()` - 16-digit auto-gen
- `generate_cvv()` - 3-digit CVV auto-gen

### Cheque Functions
- `issue_cheque(data)` - Issue cheque
- `deposit_cheque(data)` - Clear cheque
- `view_cheques(data)` - View cheques
- `generate_cheque_number()` - Auto-generate

### Report Functions
- `report_transaction_history()` - Transaction report
- `report_bank_summary()` - Bank summary
- `report_customer_balances()` - Balance report
- `visualize_account_distribution()` - Pie chart
- `visualize_loan_status()` - Bar chart
- `visualize_monthly_trends()` - Line chart
- `display_credit_score()` - Credit score display
- `view_audit_log()` - Audit trail

### Advanced Feature Functions ⭐
- `generate_account_statement(data)` - Statement generator
- `calculate_account_interest(data)` - Interest calculator
- `view_customer_financial_dashboard(data)` - Dashboard
- `compare_loan_offers(data)` - Loan comparison

### Data Functions
- `load_data()` - Load database
- `save_data(data)` - Save database
- `backup_data()` - Create backup
- `initialize_data()` - Initialize empty database
- `log_audit()` - Log operation

### Utility Functions
- `get_date()` - Current date (YYYY-MM-DD)
- `validate_pan(pan)` - Validate PAN
- `validate_aadhar(aadhar)` - Validate Aadhar
- `validate_email(email)` - Validate email
- `validate_phone(phone)` - Validate phone
- `mask_sensitive_data()` - Hide sensitive info
- `hash_password()` - SHA-256 hashing

---

## 📊 Data Structures

### Customers Table
```
CustomerID, Name, DOB, Gender, PAN, Aadhar, Address,
City, State, PIN, Phone, Email, RegistrationDate,
Status, KYCStatus
```

### Accounts Table
```
AccountNumber, CustomerID, AccountType, Balance,
InterestRate, MinBalance, RegistrationDate, Status
```

### Transactions Table
```
TransactionID, AccountNumber, TransactionType,
Amount, Date, BalanceAfter, Description
```

### Loans Table
```
LoanID, CustomerID, LoanType, PrincipalAmount,
InterestRate, EMI, Tenure, OutstandingAmount,
Status, DisbursementDate
```

### Cards Table
```
CardID, CustomerID, CardNumber, CardType,
CVV, ExpiryDate, DailyLimit, Status, IssueDate
```

### Cheques Table
```
ChequeNumber, AccountNumber, IssuedTo, Amount,
IssueDate, ClearanceDate, Status, Remarks
```

### Transfers Table
```
TransferID, FromAccount, ToAccount, Amount,
Date, Status, TransferCharge
```

### Audit Table
```
AuditID, Timestamp, Operation, Details, Status
```

---

## 🎯 Key Highlights

✅ **50+ Functions** - Comprehensive banking operations  
✅ **18 Menu Options** - Complete feature coverage  
✅ **6 Report Types** - Visual & textual analytics  
✅ **10 Data Tables** - Normalized JSON-in-CSV  
✅ **5 Loan Types** - With EMI & amortization  
✅ **3 Card Types** - Debit/Credit/Premium  
✅ **4 Advanced Features** - Dashboard, calculator, comparison  
✅ **Complete Security** - Hashing, validation, audit trail  
✅ **Professional UI** - Colors, formatting, ASCII art  
✅ **Real-world Banking** - Industry-standard calculations

