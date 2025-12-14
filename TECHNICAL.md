# CoreBank System - Technical Documentation

## System Architecture

CoreBank is a modular, Python-based banking system designed for high school level implementation.

### Technology Stack
- **Language**: Python 3.6+
- **Data Storage**: CSV files with Pandas
- **Visualization**: Matplotlib
- **Calculations**: NumPy, custom algorithms
- **Security**: SHA256 hashing (password/PIN)

---

## File Structure

```
/Users/raghav/Developer/IP Project/
├── bank_management_system.py       # Main application (Single File - 1500+ lines)
├── bank_database.csv               # Single Database File (Stores all tables)
├── backups/                        # Timestamped backups
│   └── bank_database_YYYYMMDD_HHMMSS.csv
├── bank_implementation_plan.md     # Project specifications
├── BANK_STAFF_MANUAL.md           # Staff user manual
├── CUSTOMER_GUIDE.md              # Customer guide
├── TECHNICAL.md                   # This file
├── task.md                        # Project tracking
└── project_options.md             # Original options analysis
```

---

## Core Modules (Internal)

The system is implemented as a single file with internal modules:

1. **Configuration**: Constants and settings
2. **Validators**: Input validation functions
3. **Security**: Hashing and masking utilities
4. **Calculators**: Financial algorithms
5. **Data Persistence**: Single CSV management
6. **Core Logic**: Banking operations


**Purpose**: Centralized configuration and constants

**Key Elements**:
```python
# File paths
DATA_DIR = 'data/'
CUSTOMERS_FILE = 'data/customers.csv'
# ... other file paths

# Interest rates
SAVINGS_INTEREST = 4.0
LOAN_RATES = {
    'Home Loan': 8.5,
    'Personal Loan': 12.0,
    # ...
}

# Limits
DAILY_WITHDRAWAL_LIMIT = 50000
LARGE_TRANSACTION_THRESHOLD = 100000

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    # ...
```

**Configuration Variables** (Customizable):
- Interest rates for different account types
- Loan rates for each loan type
- Transaction limits
- Minimum balances
- Backup directory

### 2. Validators (Internal)

**Purpose**: Input validation functions

**Key Functions**:
```python
validate_pan(pan)              # PAN format: ABCDE1234F
validate_aadhar(aadhar)        # 12 digits
validate_email(email)          # Email format
validate_phone(phone)          # 10 digits
validate_pin_code(pin)         # 6 digits
validate_amount(amount)        # Positive number
validate_date_format(date_str) # YYYY-MM-DD
```

**Usage**:
```python
if validate_pan(pan):
    print("Valid PAN")
else:
    print("Invalid PAN format")
```


### 3. Security (Internal)

**Purpose**: Hashing and security functions

**Key Functions**:
```python
hash_password(password)        # SHA-256 hashing
verify_password(stored, provided) # Verify hash
generate_account_number()      # Generate unique 12-digit account number
generate_transaction_id()      # Generate unique transaction ID
```

**Usage**:
```python
hashed_pw = hash_password("securePass123")
is_valid = verify_password(hashed_pw, "securePass123")
```


### 4. Calculators (Internal)

**Purpose**: Financial calculations

**Key Functions**:

#### EMI Calculator
```python
def calculate_emi(principal, annual_interest_rate, tenure_months):
    """
    Formula: EMI = [P × R × (1+R)^N] / [(1+R)^N - 1]
    Example:
    - Principal: ₹2,00,000
    - Rate: 12% p.a.
    - Tenure: 36 months
    - Returns: ₹6,644.00
    """
```

#### Interest Calculator
```python
def calculate_simple_interest(principal, annual_rate, days):
    """
    Formula: SI = (P × R × T) / 100
    For monthly interest in savings accounts
    """
```

#### Amortization Schedule
```python
def calculate_amortization_schedule(principal, annual_interest_rate, tenure_months):
    """
    Returns list of monthly breakdown:
    - Month number
    - EMI amount
    - Principal portion
    - Interest portion
    - Outstanding amount
    """
```

#### FD Maturity
```python
def calculate_fd_maturity(principal, annual_rate, tenure_days):
    """
    Calculates final amount including interest
    """
```

#### Credit Score Simulation
```python
def get_credit_score(account_age_days, total_transactions, defaulted_loans=0):
    """
    Returns score 0-900 based on:
    - Account history
    - Transaction frequency
    - Default history
    """
```

---

## Main Application Flow

### Data Management

#### Initialize System
```python
def initialize_data():
    """
    Called at startup
    - Checks for bank_database.csv
    - Creates it with empty tables if missing
    - Does NOT overwrite existing data
    """
```

#### Load Data
```python
def load_data():
    """
    Loads bank_database.csv
    Parses JSON strings from 'Data' column
    Returns dict with keys:
    - customers
    - accounts
    - transactions
    - transfers
    - loans
    - loan_payments
    - cards
    - cheques
    - users
    - audit
    """
```

#### Save Data
```python
def save_data(data_dict):
    """
    Converts DataFrames to JSON strings
    Writes to bank_database.csv
    Called after every modification
    """
```

#### Backup Data
```python
def backup_data():
    """
    Creates timestamped backup of bank_database.csv
    Copies to: backups/bank_database_YYYYMMDD_HHMMSS.csv
    """
```

### Reports & Analytics Flow

```python
generate_reports(data)      # Main reports menu
```

#### Available Reports
1. **Transaction History**:
   - Input: Account Number
   - Output: Date, Type, Amount, Debit/Credit, Balance

2. **Bank Financial Summary**:
   - Total Deposits (Sum of all account balances)
   - Total Loans Outstanding
   - Net Liquidity (Deposits - Loans)
   - Total Transaction Volume (Credit & Debit)

3. **Customer Balances Report**:
   - Lists all customers
   - Shows aggregated balance across all their accounts

4. **Visual Analytics (Matplotlib)**:
   - **Account Distribution**: Pie chart showing percentage of Savings vs Current vs FD accounts.
   - **Loan Portfolio**: Bar chart showing total principal amount by loan type.

### Customer Management Flow

```python
add_customer(data)          # Input validation → Generate ID → Save
view_customers(data)        # Display all customers
search_customer(data)       # Search by ID or name
update_customer(data)       # Modify existing customer
delete_customer(data)       # Remove customer (if no accounts)
```

**Customer ID Generation**:
```python
# Finds max existing ID number
# Increments by 1
# Format: CUST + 3-digit number (CUST001, CUST002, ...)
```

### Account Management Flow

```python
open_account(data)          # Create new account
view_accounts(data)         # List all accounts
check_balance(data)         # Display balance
```

**Account Number Generation**:
```python
# Finds max existing account number
# Increments by 1
# Format: ACC + 4-digit number (ACC1001, ACC1002, ...)
```

**Account Opening Process**:
1. Verify customer exists
2. Select account type
3. Validate initial deposit (≥ minimum balance)
4. Generate account number
5. Create account record
6. Log opening as transaction
7. Display confirmation

### Transaction Flow

#### Deposit
```
Check account exists
↓
Validate amount > 0
↓
Add amount to balance
↓
Create transaction record (Credit)
↓
Display confirmation
```

#### Withdrawal
```
Check account exists
↓
Validate balance ≥ (amount + minimum balance)
↓
Validate amount ≤ daily limit
↓
Subtract from balance
↓
Create transaction record (Debit)
↓
Display confirmation
```

#### Fund Transfer
```
Validate both accounts exist
↓
Validate sender balance sufficient
↓
Deduct from sender account
↓
Add to receiver account
↓
Create transfer record
↓
Create 2 transaction records (Debit + Credit)
↓
Display confirmation
```

### Loan Management Flow

#### Apply for Loan
```
Verify customer and account
↓
Select loan type (determine interest rate)
↓
Input principal and tenure
↓
Calculate EMI using formula
↓
Calculate maturity date
↓
Create loan record (Status: Pending Approval)
↓
Display confirmation with EMI
```

#### Approve Loan
```
List pending loans
↓
Select loan to approve
↓
Update loan status to "Active"
↓
Disburse principal to linked account
↓
Create deposit transaction
```

#### Pay EMI
```
Verify loan exists
↓
Check linked account has sufficient balance
↓
Calculate principal and interest portions
↓
Deduct EMI from account
↓
Update outstanding amount
↓
If outstanding = 0, mark loan as "Closed"
↓
Record payment with breakdown
```

---

## Data Structures (Single CSV Format)

The system uses a single file `bank_database.csv` with two columns:
1. **Table**: Name of the table (e.g., 'customers', 'accounts')
2. **Data**: JSON string containing the list of records

### Example `bank_database.csv` content:
```csv
Table,Data
customers,"[{'CustomerID': 'CUST001', 'Name': 'Raghav Agarwal', ...}, ...]"
accounts,"[{'AccountNumber': 'ACC1001', 'CustomerID': 'CUST001', ...}, ...]"
transactions,"[{'TransactionID': 'TXN00001', ...}, ...]"
```

### Internal Schema (JSON Keys)

#### customers
```json
{
  "CustomerID": "CUST001",
  "Name": "Raghav Agarwal",
  "DOB": "2005-08-15",
  "Gender": "Male",
  "PAN": "ABCDE1234F",
  "Aadhar": "123456789012",
  ...
}
```

#### accounts
```json
{
  "AccountNumber": "ACC1001",
  "CustomerID": "CUST001",
  "AccountType": "Savings",
  "Balance": 25000.00,
  "MinBalance": 1000,
  "InterestRate": 4.0,
  "Status": "Active",
  ...
}
```

---

## Key Algorithms

### EMI Calculation Algorithm
```
Input: Principal (P), Annual Rate (R%), Tenure (N months)

Monthly Rate = (R / 12 / 100)
If Monthly Rate = 0:
    EMI = Principal / N
Else:
    Numerator = P × Monthly Rate × (1 + Monthly Rate)^N
    Denominator = (1 + Monthly Rate)^N - 1
    EMI = Numerator / Denominator

Return EMI rounded to 2 decimal places
```

### Amortization Schedule
```
For each month from 1 to N:
    Interest = Outstanding × Monthly Rate
    Principal = EMI - Interest
    Outstanding = Outstanding - Principal
    Record: Month, EMI, Principal, Interest, Outstanding
```

### Balance Validation
```
If (Current Balance - Withdrawal Amount) < Minimum Balance:
    Reject withdrawal
Else:
    Process withdrawal
```

### Credit Score Calculation
```
Base Score = 600
Add points for:
    - Account age (0-150 points)
    - Transaction frequency (0-100 points)
Subtract points for:
    - Each default (-100 points per)
Clamp score to 0-900 range
```

---

## Error Handling

### Input Validation Errors
- Invalid PAN/Aadhar format → Show format example
- Invalid amount → Show must be positive number
- Duplicate customer ID → Show already exists
- Customer not found → Show search customers first

### Transaction Errors
- Insufficient balance → Show available amount
- Account not found → Show available accounts
- Daily limit exceeded → Show limit and suggest split transaction
- Minimum balance violation → Show required minimum

### System Errors
- File not found → Initialize data files
- CSV parse error → Show file corruption message
- Backup failure → Log and notify user

---

## Testing Checklist

### Unit Tests
- [ ] PAN validation (valid/invalid formats)
- [ ] Aadhar validation (correct length, digits)
- [ ] Email validation (various formats)
- [ ] Amount validation (positive, zero, negative)
- [ ] Date validation (correct format)
- [ ] EMI calculation accuracy
- [ ] Interest calculation
- [ ] Amortization schedule generation

### Integration Tests
- [ ] Add customer → Open account → Deposit → Withdraw
- [ ] Apply loan → Approve → Pay EMI → Check outstanding
- [ ] Transfer between two accounts → Verify both updated
- [ ] Backup and restore functionality

### System Tests
- [ ] Data persistence (close and reopen application)
- [ ] CSV file integrity (no data loss)
- [ ] Menu navigation (all options accessible)
- [ ] Role-based access (Admin vs Teller permissions)

---

## Performance Considerations

### For Large Datasets

**Current Approach**:
- Loads entire CSV into Pandas DataFrame
- Suitable for 10,000+ records
- Simple filtering with str.contains()

**Optimization Tips** (if needed):
- Index frequently searched columns (CustomerID, AccountNumber)
- Use set operations for membership checks
- Archive old transactions to separate file
- Consider database (MySQL) for 100,000+ records

### Memory Usage
- Average per customer: ~500 bytes
- Average per account: ~300 bytes
- Average per transaction: ~200 bytes

### Typical Performance
- Adding customer: < 100ms
- Searching customer: < 500ms (for 1000 customers)
- Processing transaction: < 200ms
- Calculating EMI: < 50ms

---

## Future Enhancements

### Phase 1 Complete ✓
- Basic customer and account management
- Transaction processing
- Loan management
- Interest calculations

### Phase 2 (Optional)
- Interest auto-crediting (scheduled)
- Card management
- Cheque processing
- Alerts and notifications

### Phase 3 (Optional)
- MySQL database integration
- Web interface (Flask/Django)
- Mobile app simulation
- Multi-branch support

### Phase 4 (Optional)
- Advanced analytics and reporting
- Fraud detection
- Machine learning for credit scoring
- API for external integration

---

## Modification Guide

### Changing Interest Rates
**Location**: `bank_management_system.py` (Section 1: Configuration)
```python
SAVINGS_INTEREST = 4.0  # Change here
LOAN_RATES = {
    'Personal Loan': 12.0,  # Change here
}
```

### Adding New Account Type
**Location**: `bank_management_system.py` (Section 4: Core Features -> `open_account` function)
```python
account_types = {
    '1': ('Savings', SAVINGS_INTEREST, MIN_SAVINGS),
    '2': ('Current', CURRENT_INTEREST, MIN_CURRENT),
    '4': ('New Type', 5.0, 10000),  # Add new type here
}
```

### Adding New Loan Type
**Location**: `bank_management_system.py` (Section 1: Configuration)
```python
LOAN_RATES = {
    'Home Loan': 8.5,
    'New Loan Type': 11.0,  # Add here
}
```

### Changing Transaction Limit
**Location**: `bank_management_system.py` (Section 1: Configuration)
```python
DAILY_WITHDRAWAL_LIMIT = 50000  # Change to new limit
```

---

## Troubleshooting Guide

### Data Not Saving
**Check**:
1. Is data/ directory writable?
2. Are CSV files locked by other program?
3. Is disk space available?

**Solution**:
- Restart application
- Check file permissions
- Free up disk space

### EMI Calculation Seems Wrong
**Check**:
1. Interest rate (annual vs monthly)
2. Tenure in months (not years)
3. Principal amount

**Verify**:
- Formula: EMI = [P × R × (1+R)^N] / [(1+R)^N - 1]
- Test with online calculator

### Customer/Account Not Found
**Check**:
1. Is ID correctly formatted? (CUST001, ACC1001)
2. Does record actually exist?
3. Is record's status "Active"?

**Solution**:
- View all customers/accounts
- Search with correct ID
- Add missing record if needed

---

## Code Statistics

| Component | Lines | Complexity |
|---|---|---|
| Main App (Single File) | 1500+ | High |
| **Total** | **1500+** | - |

---

## Dependencies

### Required
```
pandas >= 1.0.0
```

### Optional
```
matplotlib >= 3.0.0  (for future reports)
numpy >= 1.18.0     (for calculations)
```

### Install
```bash
pip install pandas matplotlib numpy
```

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 2.0 | Dec 2025 | Complete rewrite with modular structure |
| 1.0 | Nov 2025 | Initial library management system |

---

**Documentation Version**: 2.0  
**Last Updated**: December 2025  
**Maintained By**: High School IP Project Team
