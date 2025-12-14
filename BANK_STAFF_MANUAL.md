# CoreBank System - Bank Staff User Manual

## System Overview

**CoreBank** is a comprehensive bank management system designed to streamline daily banking operations. It supports customer management, account operations, transaction processing, and loan management.

---

## Getting Started

### Prerequisites

- Python 3.6 or higher
- Required libraries: pandas, matplotlib, numpy

### Installation

1. Install Python libraries:
```bash
pip install pandas matplotlib numpy
```

2. Navigate to the project directory:
```bash
cd /path/to/IP\ Project
```

3. Run the application:
```bash
python bank_management_system.py
```

### Default Credentials

- **Username**: admin
- **Password**: admin@123

---

## System Architecture

The system is implemented as a **Single Python File** for easy deployment:

```
CoreBank/
├── bank_management_system.py    (Main application - contains all logic)
└── bank_database.csv            (Single database file - stores all records)
```

All data (customers, accounts, transactions, etc.) is stored in the single `bank_database.csv` file.


---

## Module Descriptions

### 1. Customer Management

**Purpose**: Register and manage customer information with full KYC (Know Your Customer) details.

**Features**:
- Add new customers with complete details
- Search customers by ID or name
- Update customer contact information
- View all registered customers
- Delete customers (with validation)

**Data Captured**:
- Personal: Name, DOB, Gender
- Identification: PAN, Aadhar
- Contact: Address, City, State, PIN, Phone, Email
- Account Status: Active/Inactive, KYC Status

**Step-by-Step Guide**:

#### Adding a Customer
1. From Main Menu, select **Option 1: Customer Management**
2. Select **Option 1: Add Customer**
3. Enter the following information:
   - Name (e.g., "Raghav Agarwal")
   - Date of Birth (format: YYYY-MM-DD, e.g., "2005-08-15")
   - Gender (Male/Female/Other)
   - PAN number (format: ABCDE1234F)
   - Aadhar number (12 digits)
   - Complete address
   - City, State, PIN (6 digits)
   - Phone (10 digits)
   - Email

4. System auto-generates **Customer ID** (e.g., CUST001)
5. Customer is set to "Active" with "Pending" KYC status

#### Searching Customers
1. From Customer Management menu, select **Option 3: Search Customer**
2. Enter Customer ID or Name
3. System displays matching customers with summary details

#### Updating Customer Details
1. From Customer Management menu, select **Option 4: Update Customer**
2. Enter Customer ID to update
3. Press Enter to skip fields you don't want to change
4. Updated details are saved immediately

#### Deleting a Customer
1. From Customer Management menu, select **Option 5: Delete Customer** (Admin only)
2. Enter Customer ID
3. System verifies customer has no active accounts
4. Confirm deletion
5. Customer record is permanently removed

---

### 2. Account Management

**Purpose**: Open and manage multiple account types for customers.

**Supported Account Types**:

| Account Type | Interest Rate | Min Balance | Features |
|---|---|---|---|
| Savings | 4.0% p.a. | ₹1,000 | Best for personal savings |
| Current | 0% | ₹5,000 | For business use, unlimited transactions |
| Fixed Deposit (FD) | 7.5% p.a. | None | Locked amount for tenure |

**Step-by-Step Guide**:

#### Opening a New Account
1. From Main Menu, select **Option 2: Account Management**
2. Select **Option 1: Open New Account**
3. Enter Customer ID (must be pre-registered)
4. Select Account Type:
   - Press **1** for Savings Account
   - Press **2** for Current Account
   - Press **3** for Fixed Deposit
5. Enter initial deposit amount (must meet minimum balance)
6. For FD accounts, specify tenure (6, 12, 24, or 60 months)
7. System generates **Account Number** (e.g., ACC1001)
8. Confirmation with account details is displayed

**Example**:
```
Account Number: ACC1001
Account Type: Savings
Initial Balance: ₹25,000
Interest Rate: 4.0% p.a.
Opening Date: 2025-12-13
Status: Active
```

#### Checking Account Balance
1. From Account Management menu, select **Option 3: Check Balance**
2. Enter Account Number
3. System displays:
   - Current balance
   - Account type
   - Account status

---

### 3. Transaction Processing

**Purpose**: Execute all account transactions securely.

**Transaction Types**:
- Cash Deposit: Add money to account
- Cash Withdrawal: Remove money (with balance validation)
- Fund Transfer: Transfer between accounts
- Account Statement: View transaction history

**Important Limits**:
- Daily withdrawal limit: ₹50,000
- Minimum balance (Savings): ₹1,000
- Minimum balance (Current): ₹5,000

**Step-by-Step Guide**:

#### Depositing Money
1. From Main Menu, select **Option 3: Transaction Processing**
2. Select **Option 1: Deposit Money**
3. Enter Account Number
4. Enter deposit amount
5. Confirmation with new balance is displayed

#### Withdrawing Money
1. From Transaction menu, select **Option 2: Withdraw Money**
2. Enter Account Number
3. Enter withdrawal amount
4. System checks:
   - Sufficient balance above minimum requirement
   - Daily withdrawal limit not exceeded
5. If successful, confirmation with new balance is displayed

**Example Withdrawal Flow**:
```
Account Number: ACC1001
Current Balance: ₹25,000
Minimum Required: ₹1,000
Available to Withdraw: ₹24,000

Enter withdrawal amount: ₹5,000
✓ Withdrawal successful!
New Balance: ₹20,000
```

#### Transferring Funds
1. From Transaction menu, select **Option 3: Transfer Funds**
2. Enter From Account Number
3. Enter To Account Number
4. Enter transfer amount
5. System validates both accounts and sufficient balance
6. Transfer is processed; both accounts updated

**Transfer Process**:
- From account is debited
- To account is credited
- Two transaction records are created
- Transfer reference number is generated

#### Viewing Account Statement
1. From Transaction menu, select **Option 5: Account Statement**
2. Enter Account Number
3. System displays:
   - Account holder name and type
   - Current balance
   - Last 10 transactions with details

---

### 4. Loan Management

**Purpose**: Handle loan applications, approvals, and EMI tracking.

**Supported Loan Types**:

| Loan Type | Max Amount | Interest Rate | Max Tenure |
|---|---|---|---|
| Home Loan | ₹50,00,000 | 8.5% | 20 years |
| Personal Loan | ₹10,00,000 | 12.0% | 5 years |
| Car Loan | ₹15,00,000 | 9.0% | 7 years |
| Education Loan | ₹20,00,000 | 7.0% | 15 years |
| Business Loan | ₹1,00,00,000 | 10.0% | 10 years |

**EMI Calculation Formula**:
```
EMI = [P × R × (1+R)^N] / [(1+R)^N - 1]
where:
P = Principal (loan amount)
R = Monthly interest rate (Annual rate ÷ 12 ÷ 100)
N = Number of months (tenure)
```

**Step-by-Step Guide**:

#### Applying for a Loan
1. From Main Menu, select **Option 4: Loan Management**
2. Select **Option 1: Apply for Loan**
3. Enter Customer ID
4. Select linked bank account (account where EMI will be debited)
5. Select loan type from list
6. Enter desired loan amount
7. Enter tenure in months
8. System calculates EMI and displays:
   - Loan ID (e.g., LOAN001)
   - Monthly EMI amount
   - Total tenure
   - Status: "Pending Approval"

**Example**:
```
Loan Type: Personal Loan
Principal: ₹2,00,000
Interest Rate: 12.0% p.a.
Tenure: 36 months
Calculated EMI: ₹6,644.00

Loan ID: LOAN001
Status: Pending Approval
```

#### Approving Loans (Manager/Admin Only)
1. From Loan Management menu, select **Option 4: Approve Loan Application**
2. System lists all "Pending Approval" loans
3. Select loan to approve
4. Confirm approval
5. System:
   - Changes status to "Active"
   - Records approval date
   - Disburses amount to linked account

#### Paying Loan EMI
1. From Loan Management menu, select **Option 2: Pay Loan EMI**
2. Enter Loan ID
3. System displays:
   - Current EMI amount
   - Outstanding amount
   - Required balance
4. System auto-debits EMI from linked account
5. Confirmation shows:
   - Principal portion credited
   - Interest portion credited
   - New outstanding amount

**Example EMI Payment**:
```
Loan ID: LOAN001
EMI: ₹6,644.00
Outstanding Before: ₹195,356.00

Payment Details:
Principal: ₹4,644.00
Interest: ₹2,000.00
Outstanding After: ₹190,712.00
```

---

## System Features

### Data Validation

The system validates all inputs:

| Input | Format | Example |
|---|---|---|
| PAN | 10 alphanumeric (5 letters, 4 digits, 1 letter) | ABCDE1234F |
| Aadhar | 12 digits | 123456789012 |
| Phone | 10 digits | 9876543210 |
| PIN | 6 digits | 305001 |
| Email | Valid email format | user@example.com |
| Amount | Positive number | 5000.50 |
| Date | YYYY-MM-DD format | 2005-08-15 |

### Reports & Analytics

**Purpose**: Generate insights and visualizations from banking data.

**Available Reports**:

#### 1. Transaction History
- View complete transaction log for any account
- Shows Date, Type, Amount, Debit/Credit, Balance
- Useful for account reconciliation

**Steps**:
1. From Main Menu, select **Option 8: Reports & Analytics**
2. Select **Option 1: Transaction History**
3. Enter Account Number
4. View formatted transaction list

#### 2. Bank Financial Summary
- High-level overview of bank's financial position
- Shows:
  - Total Deposits Held
  - Total Loans Outstanding
  - Net Liquidity (Deposits - Loans)
  - Total Credit/Debit Transaction Volume
  - Customer Base Count

**Steps**:
1. From Reports menu, select **Option 2: Bank Financial Summary**
2. View comprehensive financial dashboard

#### 3. Customer Balances Report
- Lists all customers with their total balances
- Aggregates balance across multiple accounts
- Shows number of accounts per customer

**Steps**:
1. From Reports menu, select **Option 3: Customer Balances Report**
2. View customer-wise balance summary

#### 4. Visual Analytics - Account Distribution (Pie Chart)
- Visual representation of account type distribution
- Shows percentage breakdown: Savings vs Current vs Fixed Deposit
- Opens in new matplotlib window

**Steps**:
1. From Reports menu, select **Option 4: Visualize Account Distribution**
2. Chart window opens automatically
3. Close window to return to menu

**Chart Shows**:
- Percentage of each account type
- Color-coded segments
- Total account count

#### 5. Visual Analytics - Loan Portfolio (Bar Chart)
- Bar chart showing total principal amount by loan type
- Helps understand loan distribution across categories
- Opens in new matplotlib window

**Steps**:
1. From Reports menu, select **Option 5: Visualize Loan Portfolio**
2. Chart window opens automatically
3. Close window to return to menu

**Chart Shows**:
- Loan types on X-axis
- Total principal amounts on Y-axis
- Color-coded bars

**Best Practices**:
- Run Financial Summary daily for overview
- Use Transaction History for customer inquiries
- Generate visual charts for presentations/reports
- Export data if analysis needed in Excel

---

### Backup System

**Creating Backups**:
1. From Main Menu, select **Option 9: Backup Data**
2. System automatically:
   - Creates timestamped folder (e.g., `backup_20251213_145230`)
   - Copies all data files
   - Saves in `backups/` directory

**Backup Contents**:
- All customer records
- Account information
- Transaction history
- Loan details
- Payment records

---

## Dashboard

The dashboard displays:
- Total customers in system
- Total accounts
- Total balance across all accounts
- Active and total loans
- Total outstanding loan amount
- Transaction count

**Dashboard appears on every main menu access**

---

## Troubleshooting

### Common Issues

**Issue**: "Customer not found"
- **Solution**: Verify Customer ID exists; add customer if new

**Issue**: "Insufficient balance"
- **Solution**: Check balance; ensure minimum balance is maintained

**Issue**: "Account not found"
- **Solution**: Verify Account Number; open new account if needed

**Issue**: "Invalid PAN format"
- **Solution**: PAN must be 10 characters: 5 letters, 4 digits, 1 letter (e.g., ABCDE1234F)

**Issue**: "Withdrawal limit exceeded"
- **Solution**: Daily limit is ₹50,000; split transaction if needed

---

## Security Best Practices

1. **Password Management**:
   - Change default password immediately
   - Use strong passwords (8+ characters with mix of letters, numbers, symbols)

2. **Transaction Security**:
   - Always verify amount before confirming
   - Double-check account numbers during transfers

3. **Data Safety**:
   - Regular backups created automatically
   - Manual backups recommended daily

4. **Access Control**:
   - Admin: Full system access
   - Manager: Loan approvals, customer management
   - Teller: Transaction processing only

---

## Quick Reference

### Main Menu Options
| Option | Purpose |
|---|---|
| 1 | Customer Management |
| 2 | Account Management |
| 3 | Transaction Processing |
| 4 | Loan Management |
| 5 | Backup Data |
| 6 | Exit |

### Customer Management Options
| Option | Purpose |
|---|---|
| 1 | Add Customer |
| 2 | View All Customers |
| 3 | Search Customer |
| 4 | Update Customer |
| 5 | Delete Customer |
| 6 | Back to Main Menu |

### Transaction Processing Options
| Option | Purpose |
|---|---|
| 1 | Deposit Money |
| 2 | Withdraw Money |
| 3 | Transfer Funds |
| 4 | View Transactions |
| 5 | Account Statement |
| 6 | Back to Main Menu |

---

## Support & Feedback

For issues or feature requests:
- Review the implementation plan: `bank_implementation_plan.md`
- Check technical documentation: `TECHNICAL.md`
- Contact system administrator

---

**Version**: 2.0  
**Last Updated**: December 2025  
**Status**: Production Ready
