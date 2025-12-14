"""
CoreBank - Comprehensive Bank Management System
Version: 3.0 (Single File Edition)
Author: Raghav Agarwal
Date: December 13, 2025

This is a complete Banking Management System implemented in a single Python file.
It includes:
1. Configuration & Constants
2. Input Validators
3. Security Utilities (Hashing/Masking)
4. Financial Calculators (EMI, Interest)
5. Data Persistence (Single CSV Database)
6. Core Banking Logic (Customers, Accounts, Transactions, Loans)
"""

import os
import sys
import json
import hashlib
import re
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# ==========================================
# SECTION 1: CONFIGURATION & CONSTANTS
# ==========================================

# Database File
DB_FILE = 'bank_database.csv'
BACKUP_DIR = 'backups/'

# System Configuration
FINE_PER_DAY = 2.0  # Rupees per day for overdue

# Interest Rates (Annual Percentage)
SAVINGS_INTEREST = 4.0
CURRENT_INTEREST = 0.0
FD_INTEREST = 7.5
RD_INTEREST = 5.5

# Loan Interest Rates
LOAN_RATES = {
    'Home Loan': 8.5,
    'Personal Loan': 12.0,
    'Car Loan': 9.0,
    'Education Loan': 7.0,
    'Business Loan': 10.0
}

# Minimum Balances
MIN_SAVINGS = 1000
MIN_CURRENT = 5000

# Transaction Limits
DAILY_WITHDRAWAL_LIMIT = 50000
LARGE_TRANSACTION_THRESHOLD = 100000

# EMI Calculation
EMI_PRECISION = 2

# Table Schemas (for initialization)
SCHEMAS = {
    'customers': ['CustomerID', 'Name', 'DOB', 'Gender', 'PAN', 'Aadhar', 'Address', 'City', 'State', 'PIN', 'Phone', 'Email', 'RegistrationDate', 'Status', 'KYC_Status'],
    'accounts': ['AccountNumber', 'CustomerID', 'AccountType', 'Balance', 'MinBalance', 'InterestRate', 'OpeningDate', 'MaturityDate', 'Status', 'LastInterestCredited'],
    'transactions': ['TransactionID', 'AccountNumber', 'TransactionType', 'Amount', 'DebitCredit', 'Balance_After', 'Date', 'Time', 'Remarks', 'Status'],
    'transfers': ['TransferID', 'FromAccount', 'ToAccount', 'Amount', 'TransferType', 'Charges', 'Date', 'Status', 'Reference'],
    'loans': ['LoanID', 'CustomerID', 'LinkedAccount', 'LoanType', 'PrincipalAmount', 'InterestRate', 'Tenure_Months', 'EMI', 'StartDate', 'MaturityDate', 'OutstandingAmount', 'Status', 'ApprovalDate'],
    'loan_payments': ['PaymentID', 'LoanID', 'PaymentDate', 'AmountPaid', 'PrincipalPart', 'InterestPart', 'OutstandingAfter', 'PaymentMethod', 'Status'],
    'cards': ['CardNumber', 'CustomerID', 'LinkedAccount', 'CardType', 'CreditLimit', 'IssueDate', 'ExpiryDate', 'CVV', 'PIN_Hash', 'Status'],
    'cheques': ['ChequeNumber', 'AccountNumber', 'IssuedTo', 'Amount', 'IssueDate', 'ClearanceDate', 'Status', 'Remarks'],
    'users': ['UserID', 'Username', 'Password_Hash', 'Role', 'EmployeeID', 'Email', 'Status', 'LastLogin'],
    'audit': ['LogID', 'UserID', 'Action', 'Details', 'Timestamp', 'IPAddress', 'Status']
}

# Message Colors for Better UX
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'

# ==========================================
# SECTION 2: UTILITY FUNCTIONS (Validators, Security, Calculators)
# ==========================================

# --- Validators ---

def validate_pan(pan):
    """Validate PAN format (10 alphanumeric: ABCDE1234F)"""
    pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'
    return bool(re.match(pattern, pan))

def validate_aadhar(aadhar):
    """Validate Aadhar format (12 digits)"""
    return aadhar.isdigit() and len(aadhar) == 12

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone):
    """Validate phone format (10 digits)"""
    return phone.isdigit() and len(phone) == 10

def validate_pin_code(pin):
    """Validate PIN code (6 digits)"""
    return pin.isdigit() and len(pin) == 6

def validate_amount(amount):
    """Validate amount (positive number)"""
    try:
        amt = float(amount)
        return amt > 0
    except ValueError:
        return False

def validate_date_format(date_str):
    """Validate date format (YYYY-MM-DD)"""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

# --- Security ---

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hash_value):
    """Verify password against hash"""
    return hash_password(password) == hash_value

def mask_pan(pan):
    """Mask PAN - show only last 4 characters"""
    if len(pan) >= 4:
        return "XXXX" + pan[-4:]
    return pan

def mask_aadhar(aadhar):
    """Mask Aadhar - show only last 4 digits"""
    if len(aadhar) >= 4:
        return "XXXXXXXX" + aadhar[-4:]
    return aadhar

def mask_account_number(account_num):
    """Mask account number - show only last 4 digits"""
    if len(account_num) >= 4:
        return "XXX" + account_num[-4:]
    return account_num

def get_timestamp():
    """Get current timestamp"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_date():
    """Get current date in YYYY-MM-DD format"""
    return datetime.now().strftime("%Y-%m-%d")

# --- Calculators ---

def calculate_emi(principal, annual_interest_rate, tenure_months):
    """Calculate EMI: [P x R x (1+R)^N] / [(1+R)^N - 1]"""
    if principal <= 0 or annual_interest_rate < 0 or tenure_months <= 0:
        return 0
    
    monthly_rate = annual_interest_rate / (12 * 100)
    if monthly_rate == 0:
        return round(principal / tenure_months, 2)
    
    numerator = principal * monthly_rate * ((1 + monthly_rate) ** tenure_months)
    denominator = ((1 + monthly_rate) ** tenure_months) - 1
    
    emi = numerator / denominator
    return round(emi, 2)

def calculate_simple_interest(principal, annual_rate, days):
    """Calculate simple interest: (P x R x T) / 100"""
    time_in_years = days / 365
    interest = (principal * annual_rate * time_in_years) / 100
    return round(interest, 2)

# ==========================================
# SECTION 3: DATA MANAGEMENT
# ==========================================

def initialize_data():
    """Initialize database file if it doesn't exist"""
    if not os.path.exists(DB_FILE):
        print(f"{Colors.YELLOW}Initializing new database...{Colors.END}")
        # Create empty file with headers
        pd.DataFrame(columns=['Table', 'Data']).to_csv(DB_FILE, index=False)
        
        # Create default admin user
        admin_user = {
            'UserID': 'USR001',
            'Username': 'admin',
            'Password_Hash': hash_password('admin@123'),
            'Role': 'Admin',
            'EmployeeID': 'EMP001',
            'Email': 'admin@corebank.com',
            'Status': 'Active',
            'LastLogin': get_timestamp()
        }
        
        # Save initial data
        data = {table: pd.DataFrame(columns=cols) for table, cols in SCHEMAS.items()}
        data['users'] = pd.DataFrame([admin_user])
        save_data(data)

def load_data():
    """Load data from single CSV into dictionary of DataFrames"""
    try:
        if not os.path.exists(DB_FILE):
            initialize_data()
            
        df = pd.read_csv(DB_FILE)
        data = {}
        
        for table, columns in SCHEMAS.items():
            # Filter rows for this table
            table_rows = df[df['Table'] == table]['Data']
            
            if not table_rows.empty:
                # Parse JSON records
                records = [json.loads(row) for row in table_rows]
                data[table] = pd.DataFrame(records)
                # Ensure all columns exist (handle schema evolution)
                for col in columns:
                    if col not in data[table].columns:
                        data[table][col] = None
            else:
                # Create empty DataFrame with correct schema
                data[table] = pd.DataFrame(columns=columns)
                
        return data
    except Exception as e:
        print(f"{Colors.RED}Error loading data: {str(e)}{Colors.END}")
        # Return empty structure on error to prevent crash
        return {table: pd.DataFrame(columns=cols) for table, cols in SCHEMAS.items()}

def save_data(data_dict):
    """Save dictionary of DataFrames to single CSV"""
    try:
        all_rows = []
        for table, df in data_dict.items():
            if not df.empty:
                # Convert to dict records
                records = df.to_dict(orient='records')
                for record in records:
                    # Clean NaN values
                    clean_record = {k: (None if pd.isna(v) else v) for k, v in record.items()}
                    all_rows.append({
                        'Table': table,
                        'Data': json.dumps(clean_record)
                    })
        
        pd.DataFrame(all_rows).to_csv(DB_FILE, index=False)
        return True
    except Exception as e:
        print(f"{Colors.RED}Error saving data: {str(e)}{Colors.END}")
        return False

def backup_data():
    """Create backup of the database file"""
    print(f"\n{Colors.CYAN}--- Creating Data Backup ---{Colors.END}")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(BACKUP_DIR, exist_ok=True)
    backup_path = os.path.join(BACKUP_DIR, f"bank_database_{timestamp}.csv")
    
    try:
        if os.path.exists(DB_FILE):
            with open(DB_FILE, 'r') as src:
                with open(backup_path, 'w') as dst:
                    dst.write(src.read())
            print(f"{Colors.GREEN}✓ Backup created: {backup_path}{Colors.END}")
            return True
    except Exception as e:
        print(f"{Colors.RED}✗ Backup failed: {str(e)}{Colors.END}")
        return False

# ==========================================
# SECTION 4: CORE FEATURES
# ==========================================

# --- Customer Management ---

def add_customer(data):
    print(f"\n{Colors.CYAN}--- Add New Customer ---{Colors.END}")
    try:
        # Generate ID
        existing_ids = data['customers']['CustomerID'].tolist() if not data['customers'].empty else []
        new_id_num = max([int(cid.replace('CUST', '')) for cid in existing_ids if 'CUST' in cid], default=0) + 1
        customer_id = f"CUST{new_id_num:03d}"
        
        name = input("Enter customer name: ").strip()
        if len(name) < 2: return data
        
        dob = input("Enter DOB (YYYY-MM-DD): ").strip()
        if not validate_date_format(dob): 
            print(f"{Colors.RED}Invalid date{Colors.END}")
            return data
            
        gender = input("Enter gender: ").strip()
        pan = input("Enter PAN: ").strip().upper()
        if not validate_pan(pan): 
            print(f"{Colors.RED}Invalid PAN{Colors.END}")
            return data
            
        aadhar = input("Enter Aadhar: ").strip()
        if not validate_aadhar(aadhar): 
            print(f"{Colors.RED}Invalid Aadhar{Colors.END}")
            return data
            
        address = input("Enter address: ").strip()
        city = input("Enter city: ").strip()
        state = input("Enter state: ").strip()
        pin = input("Enter PIN: ").strip()
        phone = input("Enter phone: ").strip()
        email = input("Enter email: ").strip()
        
        new_customer = {
            'CustomerID': customer_id, 'Name': name, 'DOB': dob, 'Gender': gender,
            'PAN': pan, 'Aadhar': aadhar, 'Address': address, 'City': city,
            'State': state, 'PIN': pin, 'Phone': phone, 'Email': email,
            'RegistrationDate': get_date(), 'Status': 'Active', 'KYC_Status': 'Pending'
        }
        
        data['customers'] = pd.concat([data['customers'], pd.DataFrame([new_customer])], ignore_index=True)
        print(f"{Colors.GREEN}✓ Customer {customer_id} added!{Colors.END}")
        
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.END}")
    return data

def view_customers(data):
    print(f"\n{Colors.CYAN}--- Customer List ---{Colors.END}")
    if data['customers'].empty:
        print("No customers found.")
        return
    print(data['customers'][['CustomerID', 'Name', 'Phone', 'Status']].to_string(index=False))

def search_customer(data):
    print(f"\n{Colors.CYAN}--- Search Customer ---{Colors.END}")
    query = input("Enter ID or Name: ").strip()
    results = data['customers'][
        (data['customers']['CustomerID'].str.contains(query, case=False, na=False)) |
        (data['customers']['Name'].str.contains(query, case=False, na=False))
    ]
    if results.empty:
        print("No results.")
    else:
        print(results[['CustomerID', 'Name', 'Phone', 'Email']].to_string(index=False))

# --- Account Management ---

def open_account(data):
    print(f"\n{Colors.CYAN}--- Open New Account ---{Colors.END}")
    customer_id = input("Enter Customer ID: ").strip()
    
    if data['customers'][data['customers']['CustomerID'] == customer_id].empty:
        print(f"{Colors.RED}Customer not found{Colors.END}")
        return data
        
    print("1. Savings (4%)  2. Current (0%)  3. Fixed Deposit (7.5%)")
    choice = input("Select type: ").strip()
    
    types = {'1': ('Savings', SAVINGS_INTEREST, MIN_SAVINGS), 
             '2': ('Current', CURRENT_INTEREST, MIN_CURRENT), 
             '3': ('Fixed Deposit', FD_INTEREST, 0)}
             
    if choice not in types: return data
    acc_type, rate, min_bal = types[choice]
    
    amount = float(input("Initial deposit: ").strip())
    if amount < min_bal:
        print(f"{Colors.RED}Minimum balance is ₹{min_bal}{Colors.END}")
        return data
        
    # Generate Account Number
    existing = data['accounts']['AccountNumber'].tolist() if not data['accounts'].empty else []
    new_num = max([int(a.replace('ACC', '')) for a in existing if 'ACC' in a], default=1000) + 1
    acc_num = f"ACC{new_num}"
    
    new_acc = {
        'AccountNumber': acc_num, 'CustomerID': customer_id, 'AccountType': acc_type,
        'Balance': amount, 'MinBalance': min_bal, 'InterestRate': rate,
        'OpeningDate': get_date(), 'MaturityDate': '', 'Status': 'Active',
        'LastInterestCredited': get_date()
    }
    
    data['accounts'] = pd.concat([data['accounts'], pd.DataFrame([new_acc])], ignore_index=True)
    
    # Log Transaction
    txn = {
        'TransactionID': f"TXN{len(data['transactions'])+1:05d}",
        'AccountNumber': acc_num, 'TransactionType': 'Account Opening',
        'Amount': amount, 'DebitCredit': 'Credit', 'Balance_After': amount,
        'Date': get_date(), 'Time': datetime.now().strftime("%H:%M:%S"),
        'Remarks': 'Initial Deposit', 'Status': 'Success'
    }
    data['transactions'] = pd.concat([data['transactions'], pd.DataFrame([txn])], ignore_index=True)
    
    print(f"{Colors.GREEN}✓ Account {acc_num} opened!{Colors.END}")
    return data

def check_balance(data):
    acc_num = input("Enter Account Number: ").strip()
    acc = data['accounts'][data['accounts']['AccountNumber'] == acc_num]
    if acc.empty:
        print("Account not found.")
    else:
        row = acc.iloc[0]
        print(f"\nAccount: {row['AccountNumber']} ({row['AccountType']})")
        print(f"Balance: ₹{row['Balance']:.2f}")

# --- Transactions ---

def deposit_money(data):
    print(f"\n{Colors.CYAN}--- Deposit ---{Colors.END}")
    acc_num = input("Account Number: ").strip()
    acc = data['accounts'][data['accounts']['AccountNumber'] == acc_num]
    
    if acc.empty:
        print("Account not found.")
        return data
        
    amount = float(input("Amount: ").strip())
    if amount <= 0: return data
    
    idx = acc.index[0]
    new_bal = data['accounts'].at[idx, 'Balance'] + amount
    data['accounts'].at[idx, 'Balance'] = new_bal
    
    txn = {
        'TransactionID': f"TXN{len(data['transactions'])+1:05d}",
        'AccountNumber': acc_num, 'TransactionType': 'Deposit',
        'Amount': amount, 'DebitCredit': 'Credit', 'Balance_After': new_bal,
        'Date': get_date(), 'Time': datetime.now().strftime("%H:%M:%S"),
        'Remarks': 'Cash Deposit', 'Status': 'Success'
    }
    data['transactions'] = pd.concat([data['transactions'], pd.DataFrame([txn])], ignore_index=True)
    print(f"{Colors.GREEN}✓ Deposited ₹{amount}. New Balance: ₹{new_bal:.2f}{Colors.END}")
    return data

def withdraw_money(data):
    print(f"\n{Colors.CYAN}--- Withdraw ---{Colors.END}")
    acc_num = input("Account Number: ").strip()
    acc = data['accounts'][data['accounts']['AccountNumber'] == acc_num]
    
    if acc.empty:
        print("Account not found.")
        return data
        
    amount = float(input("Amount: ").strip())
    idx = acc.index[0]
    current_bal = data['accounts'].at[idx, 'Balance']
    min_bal = data['accounts'].at[idx, 'MinBalance']
    
    if current_bal - amount < min_bal:
        print(f"{Colors.RED}Insufficient balance (Min: ₹{min_bal}){Colors.END}")
        return data
        
    new_bal = current_bal - amount
    data['accounts'].at[idx, 'Balance'] = new_bal
    
    txn = {
        'TransactionID': f"TXN{len(data['transactions'])+1:05d}",
        'AccountNumber': acc_num, 'TransactionType': 'Withdrawal',
        'Amount': amount, 'DebitCredit': 'Debit', 'Balance_After': new_bal,
        'Date': get_date(), 'Time': datetime.now().strftime("%H:%M:%S"),
        'Remarks': 'Cash Withdrawal', 'Status': 'Success'
    }
    data['transactions'] = pd.concat([data['transactions'], pd.DataFrame([txn])], ignore_index=True)
    print(f"{Colors.GREEN}✓ Withdrawn ₹{amount}. New Balance: ₹{new_bal:.2f}{Colors.END}")
    return data

# --- Loans ---

def apply_loan(data):
    print(f"\n{Colors.CYAN}--- Apply Loan ---{Colors.END}")
    cust_id = input("Customer ID: ").strip()
    if data['customers'][data['customers']['CustomerID'] == cust_id].empty:
        print("Customer not found.")
        return data
        
    print("Loan Types: " + ", ".join(LOAN_RATES.keys()))
    l_type = input("Type: ").strip()
    if l_type not in LOAN_RATES: return data
    
    amount = float(input("Amount: ").strip())
    months = int(input("Tenure (months): ").strip())
    
    rate = LOAN_RATES[l_type]
    emi = calculate_emi(amount, rate, months)
    
    loan_id = f"LOAN{len(data['loans'])+1:03d}"
    new_loan = {
        'LoanID': loan_id, 'CustomerID': cust_id, 'LinkedAccount': '',
        'LoanType': l_type, 'PrincipalAmount': amount, 'InterestRate': rate,
        'Tenure_Months': months, 'EMI': emi, 'StartDate': get_date(),
        'MaturityDate': '', 'OutstandingAmount': amount, 'Status': 'Active',
        'ApprovalDate': get_date()
    }
    
    data['loans'] = pd.concat([data['loans'], pd.DataFrame([new_loan])], ignore_index=True)
    print(f"{Colors.GREEN}✓ Loan {loan_id} approved! EMI: ₹{emi:.2f}{Colors.END}")
    return data

# ==========================================
# SECTION 5: REPORTS & ANALYTICS
# ==========================================

def report_transaction_history(data):
    print(f"\n{Colors.CYAN}--- Transaction History ---{Colors.END}")
    acc_num = input("Enter Account Number: ").strip()
    
    txns = data['transactions'][data['transactions']['AccountNumber'] == acc_num]
    if txns.empty:
        print("No transactions found for this account.")
        return

    print(f"\nHistory for {acc_num}:")
    print("-" * 80)
    print(f"{'Date':<12} {'Type':<20} {'Amount':<12} {'Type':<8} {'Balance':<12}")
    print("-" * 80)
    
    for _, row in txns.iterrows():
        print(f"{row['Date']:<12} {row['TransactionType']:<20} ₹{row['Amount']:<11.2f} {row['DebitCredit']:<8} ₹{row['Balance_After']:<12.2f}")
    print("-" * 80)

def report_bank_summary(data):
    print(f"\n{Colors.CYAN}--- Bank Financial Summary ---{Colors.END}")
    
    total_deposits = data['accounts']['Balance'].sum()
    total_loans = data['loans']['OutstandingAmount'].sum()
    total_customers = len(data['customers'])
    
    # Calculate total transaction volume
    credit_txns = data['transactions'][data['transactions']['DebitCredit'] == 'Credit']['Amount'].sum()
    debit_txns = data['transactions'][data['transactions']['DebitCredit'] == 'Debit']['Amount'].sum()
    
    print(f"Total Deposits Held:    ₹{total_deposits:,.2f}")
    print(f"Total Loans Outstanding: ₹{total_loans:,.2f}")
    print(f"Net Liquidity:          ₹{(total_deposits - total_loans):,.2f}")
    print("-" * 40)
    print(f"Total Credit Volume:    ₹{credit_txns:,.2f}")
    print(f"Total Debit Volume:     ₹{debit_txns:,.2f}")
    print(f"Customer Base:          {total_customers}")

def report_customer_balances(data):
    print(f"\n{Colors.CYAN}--- Customer Balances Report ---{Colors.END}")
    
    if data['customers'].empty:
        print("No customers.")
        return

    print(f"{'ID':<10} {'Name':<25} {'Total Balance':<15} {'Accounts':<5}")
    print("-" * 60)
    
    for _, cust in data['customers'].iterrows():
        cid = cust['CustomerID']
        accounts = data['accounts'][data['accounts']['CustomerID'] == cid]
        total_bal = accounts['Balance'].sum()
        count = len(accounts)
        
        print(f"{cid:<10} {cust['Name']:<25} ₹{total_bal:<14.2f} {count:<5}")

def visualize_account_distribution(data):
    print(f"\n{Colors.CYAN}--- Generating Account Distribution Chart ---{Colors.END}")
    if data['accounts'].empty:
        print("No accounts data to visualize.")
        return

    try:
        # Group by Account Type
        type_counts = data['accounts']['AccountType'].value_counts()
        
        plt.figure(figsize=(10, 6))
        plt.pie(type_counts, labels=type_counts.index, autopct='%1.1f%%', startangle=140, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
        plt.title('Distribution of Account Types')
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        
        print("Displaying chart window...")
        plt.show()
    except Exception as e:
        print(f"{Colors.RED}Error generating chart: {e}{Colors.END}")

def visualize_loan_status(data):
    print(f"\n{Colors.CYAN}--- Generating Loan Status Chart ---{Colors.END}")
    if data['loans'].empty:
        print("No loan data to visualize.")
        return

    try:
        # Group by Loan Type and Status
        loan_summary = data['loans'].groupby('LoanType')['PrincipalAmount'].sum()
        
        plt.figure(figsize=(10, 6))
        loan_summary.plot(kind='bar', color='skyblue')
        plt.title('Total Loan Amount by Type')
        plt.xlabel('Loan Type')
        plt.ylabel('Total Principal Amount (₹)')
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        print("Displaying chart window...")
        plt.show()
    except Exception as e:
        print(f"{Colors.RED}Error generating chart: {e}{Colors.END}")

def generate_reports(data):
    while True:
        print(f"\n{Colors.BOLD}{Colors.BLUE}=== REPORTS & ANALYTICS ==={Colors.END}")
        print("1. Transaction History")
        print("2. Bank Financial Summary")
        print("3. Customer Balances Report")
        print("4. Visualize Account Distribution (Pie Chart)")
        print("5. Visualize Loan Portfolio (Bar Chart)")
        print("6. Back to Main Menu")
        
        choice = input("\nSelect Report: ").strip()
        
        if choice == '1': report_transaction_history(data)
        elif choice == '2': report_bank_summary(data)
        elif choice == '3': report_customer_balances(data)
        elif choice == '4': visualize_account_distribution(data)
        elif choice == '5': visualize_loan_status(data)
        elif choice == '6': break
        else: print("Invalid option.")

# ==========================================
# SECTION 6: MENUS & MAIN LOOP
# ==========================================

def dashboard(data):
    print(f"\n{Colors.BOLD}{Colors.BLUE}=== COREBANK DASHBOARD ==={Colors.END}")
    print(f"Customers: {len(data['customers'])}")
    print(f"Accounts:  {len(data['accounts'])}")
    print(f"Balance:   ₹{data['accounts']['Balance'].sum():,.2f}")
    print(f"Loans:     {len(data['loans'])}")
    print(f"Time:      {datetime.now().strftime('%H:%M:%S')}")
    print("="*30)

def main():
    initialize_data()
    data = load_data()
    
    print(f"\n{Colors.BOLD}{Colors.GREEN}Welcome to CoreBank System (Single File Edition){Colors.END}")
    
    while True:
        dashboard(data)
        print("\n1. Add Customer")
        print("2. Open Account")
        print("3. Deposit")
        print("4. Withdraw")
        print("5. Check Balance")
        print("6. Apply Loan")
        print("7. View Customers")
        print("8. Reports & Analytics")
        print("9. Backup Data")
        print("10. Exit")
        
        choice = input("\nSelect Option: ").strip()
        
        if choice == '1': data = add_customer(data)
        elif choice == '2': data = open_account(data)
        elif choice == '3': data = deposit_money(data)
        elif choice == '4': data = withdraw_money(data)
        elif choice == '5': check_balance(data)
        elif choice == '6': data = apply_loan(data)
        elif choice == '7': view_customers(data)
        elif choice == '8': generate_reports(data)
        elif choice == '9': backup_data()
        elif choice == '10': 
            save_data(data)
            print("Goodbye!")
            break
        else:
            print("Invalid option.")
            
        save_data(data)

if __name__ == "__main__":
    main()
