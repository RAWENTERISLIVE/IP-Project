"""
CoreBank - Comprehensive Bank Management System
Version: 4.0 (Ultimate Single File Edition)
Author: Raghav Agarwal
Date: December 14, 2025

This is a complete Banking Management System implemented in a single Python file.
It includes:
1. Configuration & Constants
2. Input Validators
3. Security Utilities (Hashing/Masking)
4. Financial Calculators (EMI, Interest, Amortization)
5. Data Persistence (Single CSV Database)
6. Core Banking Logic (Customers, Accounts, Transactions, Loans)
7. Fund Transfer System (Internal & External)
8. Card Management System (Debit/Credit Cards)
9. Cheque Processing System
10. Comprehensive Audit Trail
11. Advanced Reports & Visual Analytics
"""

import os
import sys
import json
import hashlib
import re
import random
import string
import pandas as pd
import numpy as np
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
DAILY_TRANSFER_LIMIT = 200000
LARGE_TRANSACTION_THRESHOLD = 100000

# Card Configuration
CARD_VALIDITY_YEARS = 5
CREDIT_CARD_LIMIT_DEFAULT = 50000

# Cheque Configuration
CHEQUE_CLEARANCE_DAYS = 3

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

def calculate_amortization_schedule(principal, annual_rate, tenure_months):
    """Generate complete amortization schedule"""
    schedule = []
    monthly_rate = annual_rate / (12 * 100)
    emi = calculate_emi(principal, annual_rate, tenure_months)
    outstanding = principal
    
    for month in range(1, tenure_months + 1):
        interest_part = outstanding * monthly_rate
        principal_part = emi - interest_part
        outstanding -= principal_part
        
        schedule.append({
            'Month': month,
            'EMI': round(emi, 2),
            'Principal': round(principal_part, 2),
            'Interest': round(interest_part, 2),
            'Outstanding': round(max(0, outstanding), 2)
        })
    
    return schedule

def generate_card_number():
    """Generate a 16-digit card number"""
    return ''.join([str(random.randint(0, 9)) for _ in range(16)])

def generate_cvv():
    """Generate a 3-digit CVV"""
    return ''.join([str(random.randint(0, 9)) for _ in range(3)])

def generate_cheque_number():
    """Generate a 6-digit cheque number"""
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

def mask_card_number(card_num):
    """Mask card number - show only last 4 digits"""
    if len(card_num) >= 4:
        return "XXXX-XXXX-XXXX-" + card_num[-4:]
    return card_num

def get_credit_score(account_age_days, total_transactions, total_balance, defaulted_loans=0):
    """Calculate credit score based on banking activity"""
    base_score = 600
    
    # Account age bonus (max 100 points)
    age_score = min(100, account_age_days // 30 * 5)
    
    # Transaction frequency bonus (max 100 points)
    txn_score = min(100, total_transactions * 2)
    
    # Balance bonus (max 100 points)
    balance_score = min(100, int(total_balance / 10000) * 10)
    
    # Penalty for defaults
    default_penalty = defaulted_loans * 100
    
    final_score = base_score + age_score + txn_score + balance_score - default_penalty
    return max(300, min(900, final_score))

def calculate_credit_score(total_balance, num_loans, num_transactions):
    """Simplified credit score calculation for dashboard"""
    base_score = 600
    
    # Balance bonus (max 150 points)
    balance_score = min(150, int(total_balance / 10000) * 5)
    
    # Transaction activity bonus (max 100 points)
    txn_score = min(100, num_transactions * 3)
    
    # Loan factor (having loans can be positive if managed well)
    loan_score = min(50, num_loans * 10)
    
    final_score = base_score + balance_score + txn_score + loan_score
    return max(300, min(900, final_score))

def log_audit(data, action, details, status='Success'):
    """Log an action to audit trail"""
    log_entry = {
        'LogID': f"LOG{len(data['audit'])+1:06d}",
        'UserID': 'SYSTEM',
        'Action': action,
        'Details': details,
        'Timestamp': get_timestamp(),
        'IPAddress': '127.0.0.1',
        'Status': status
    }
    data['audit'] = pd.concat([data['audit'], pd.DataFrame([log_entry])], ignore_index=True)
    return data

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
                # Parse JSON records (indexed dictionary format)
                json_str = table_rows.iloc[0]
                indexed_dict = json.loads(json_str)
                
                # Extract records - skip 'Table' and 'Data' keys and null values
                records = []
                for key, value in indexed_dict.items():
                    # Skip non-dict values and skip if value is None or empty
                    if isinstance(value, dict) and value and key not in ['Table', 'Data']:
                        records.append(value)
                
                if records:
                    data[table] = pd.DataFrame(records)
                    # Ensure all columns exist (handle schema evolution)
                    for col in columns:
                        if col not in data[table].columns:
                            data[table][col] = None
                else:
                    # Create empty DataFrame with correct schema
                    data[table] = pd.DataFrame(columns=columns)
            else:
                # Create empty DataFrame with correct schema
                data[table] = pd.DataFrame(columns=columns)
        
        # Fix data integrity issues
        data = fix_data_integrity(data)
        return data
    except Exception as e:
        print(f"{Colors.RED}Error loading data: {str(e)}{Colors.END}")
        # Return empty structure on error to prevent crash
        return {table: pd.DataFrame(columns=cols) for table, cols in SCHEMAS.items()}

def fix_data_integrity(data):
    """Fix common data integrity issues in loaded data"""
    # Fix transactions - ensure DebitCredit and Balance columns are populated
    if not data['transactions'].empty:
        # Fix missing DebitCredit based on TransactionType
        debit_types = ['Withdrawal', 'Transfer Debit', 'Cheque Debit', 'Fund Transfer', 'EMI Payment']
        credit_types = ['Deposit', 'Transfer Credit', 'Cheque Credit', 'Account Opening', 'Interest Credit']
        
        for idx, row in data['transactions'].iterrows():
            txn_type = str(row.get('TransactionType', ''))
            
            # Fix DebitCredit if missing
            if pd.isna(row.get('DebitCredit')) or row.get('DebitCredit') is None:
                if any(dt in txn_type for dt in debit_types):
                    data['transactions'].at[idx, 'DebitCredit'] = 'Debit'
                elif any(ct in txn_type for ct in credit_types):
                    data['transactions'].at[idx, 'DebitCredit'] = 'Credit'
                else:
                    data['transactions'].at[idx, 'DebitCredit'] = 'N/A'
            
            # Fix Balance_After if missing (use BalanceAfter if available)
            if pd.isna(row.get('Balance_After')) or row.get('Balance_After') is None:
                balance_after = row.get('BalanceAfter')
                if pd.notna(balance_after):
                    data['transactions'].at[idx, 'Balance_After'] = balance_after
    
    # Fix cards - ensure LinkedAccount is populated
    if not data['cards'].empty and 'LinkedAccount' in data['cards'].columns:
        for idx, row in data['cards'].iterrows():
            if pd.isna(row.get('LinkedAccount')) or row.get('LinkedAccount') is None:
                # Try to get from AccountNumber column
                acc_num = row.get('AccountNumber')
                if pd.notna(acc_num):
                    data['cards'].at[idx, 'LinkedAccount'] = acc_num
    
    return data

def save_data(data_dict):
    """Save dictionary of DataFrames to single CSV (JSON-in-CSV format)"""
    try:
        all_rows = []
        for table, df in data_dict.items():
            if not df.empty:
                # Convert DataFrame to list of records
                records = df.to_dict(orient='records')
                # Create indexed dictionary format
                indexed_dict = {str(i): record for i, record in enumerate(records)}
                # Add null columns for schema evolution
                indexed_dict['Table'] = None
                indexed_dict['Data'] = None
                # Convert to JSON and save as one row per table
                json_data = json.dumps(indexed_dict)
                all_rows.append({
                    'Table': table,
                    'Data': json_data
                })
            else:
                # Save empty table
                all_rows.append({
                    'Table': table,
                    'Data': json.dumps({})
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
    data = log_audit(data, 'LOAN_APPLIED', f'Loan {loan_id} for ₹{amount}')
    print(f"{Colors.GREEN}✓ Loan {loan_id} approved! EMI: ₹{emi:.2f}{Colors.END}")
    return data

def pay_loan_emi(data):
    """Pay EMI for an active loan"""
    print(f"\n{Colors.CYAN}--- Pay Loan EMI ---{Colors.END}")
    
    # Show active loans
    active_loans = data['loans'][data['loans']['Status'] == 'Active']
    if active_loans.empty:
        print("No active loans found.")
        return data
    
    print("\nActive Loans:")
    print(active_loans[['LoanID', 'LoanType', 'EMI', 'OutstandingAmount']].to_string(index=False))
    
    loan_id = input("\nEnter Loan ID: ").strip()
    loan = data['loans'][data['loans']['LoanID'] == loan_id]
    
    if loan.empty or loan.iloc[0]['Status'] != 'Active':
        print(f"{Colors.RED}Loan not found or not active{Colors.END}")
        return data
    
    loan_row = loan.iloc[0]
    emi = loan_row['EMI']
    outstanding = loan_row['OutstandingAmount']
    
    print(f"\nEMI Amount: ₹{emi:.2f}")
    print(f"Outstanding: ₹{outstanding:.2f}")
    
    # Calculate interest and principal portions
    monthly_rate = loan_row['InterestRate'] / (12 * 100)
    interest_part = outstanding * monthly_rate
    principal_part = min(emi - interest_part, outstanding)
    
    new_outstanding = outstanding - principal_part
    
    # Record payment
    payment = {
        'PaymentID': f"PAY{len(data['loan_payments'])+1:05d}",
        'LoanID': loan_id,
        'PaymentDate': get_date(),
        'AmountPaid': emi,
        'PrincipalPart': round(principal_part, 2),
        'InterestPart': round(interest_part, 2),
        'OutstandingAfter': round(new_outstanding, 2),
        'PaymentMethod': 'Cash',
        'Status': 'Success'
    }
    data['loan_payments'] = pd.concat([data['loan_payments'], pd.DataFrame([payment])], ignore_index=True)
    
    # Update loan outstanding
    idx = loan.index[0]
    data['loans'].at[idx, 'OutstandingAmount'] = round(new_outstanding, 2)
    
    # Close loan if fully paid
    if new_outstanding <= 0:
        data['loans'].at[idx, 'Status'] = 'Closed'
        print(f"{Colors.GREEN}✓ Loan fully paid and closed!{Colors.END}")
    else:
        print(f"{Colors.GREEN}✓ EMI paid! Outstanding: ₹{new_outstanding:.2f}{Colors.END}")
    
    data = log_audit(data, 'EMI_PAID', f'EMI ₹{emi} for {loan_id}')
    return data

def view_loan_details(data):
    """View detailed loan information with amortization"""
    print(f"\n{Colors.CYAN}--- Loan Details ---{Colors.END}")
    loan_id = input("Enter Loan ID: ").strip()
    
    loan = data['loans'][data['loans']['LoanID'] == loan_id]
    if loan.empty:
        print("Loan not found.")
        return
    
    row = loan.iloc[0]
    
    # Handle different column names for tenure
    tenure = row.get('Tenure_Months') or row.get('Tenure') or 'N/A'
    if pd.isna(tenure):
        tenure = 'N/A'
    
    principal = float(row.get('PrincipalAmount', 0) or 0)
    interest_rate = float(row.get('InterestRate', 0) or 0)
    emi = float(row.get('EMI', 0) or 0)
    outstanding = float(row.get('OutstandingAmount', 0) or 0)
    
    print(f"\n{'='*50}")
    print(f"Loan ID:        {row['LoanID']}")
    print(f"Type:           {row.get('LoanType', 'N/A')}")
    print(f"Principal:      ₹{principal:,.2f}")
    print(f"Interest Rate:  {interest_rate}% p.a.")
    print(f"Tenure:         {tenure} months")
    print(f"EMI:            ₹{emi:,.2f}")
    print(f"Outstanding:    ₹{outstanding:,.2f}")
    print(f"Status:         {row.get('Status', 'N/A')}")
    
    # Calculate repayment progress
    if principal > 0:
        repaid = principal - outstanding
        progress = (repaid / principal) * 100
        print(f"Repaid:         ₹{repaid:,.2f} ({progress:.1f}%)")
    print(f"{'='*50}")
    
    # Show payment history
    payments = data['loan_payments'][data['loan_payments']['LoanID'] == loan_id]
    if not payments.empty:
        print(f"\n{Colors.YELLOW}Payment History:{Colors.END}")
        # Handle different column names
        display_cols = []
        for col in ['PaymentDate', 'Date', 'AmountPaid', 'Amount', 'PrincipalPart', 'InterestPart']:
            if col in payments.columns:
                display_cols.append(col)
        if display_cols:
            payment_display = payments[display_cols].copy()
            # Format amount columns
            for col in payment_display.columns:
                if 'Amount' in col or 'Part' in col:
                    payment_display[col] = payment_display[col].apply(
                        lambda x: f"₹{float(x):,.2f}" if pd.notna(x) else 'N/A'
                    )
            print(payment_display.to_string(index=False))
        else:
            print("No payment details available.")
    else:
        print("\nNo payments recorded yet.")

# ==========================================
# SECTION 5: FUND TRANSFER SYSTEM
# ==========================================

def transfer_funds(data):
    """Transfer funds between accounts"""
    print(f"\n{Colors.CYAN}--- Fund Transfer ---{Colors.END}")
    print("1. Transfer to own account")
    print("2. Transfer to other customer")
    
    choice = input("Select: ").strip()
    
    from_acc = input("From Account Number: ").strip()
    from_account = data['accounts'][data['accounts']['AccountNumber'] == from_acc]
    
    if from_account.empty:
        print(f"{Colors.RED}Source account not found{Colors.END}")
        return data
    
    to_acc = input("To Account Number: ").strip()
    to_account = data['accounts'][data['accounts']['AccountNumber'] == to_acc]
    
    if to_account.empty:
        print(f"{Colors.RED}Destination account not found{Colors.END}")
        return data
    
    if from_acc == to_acc:
        print(f"{Colors.RED}Cannot transfer to same account{Colors.END}")
        return data
    
    amount = float(input("Amount: ₹").strip())
    
    from_idx = from_account.index[0]
    from_bal = data['accounts'].at[from_idx, 'Balance']
    min_bal = data['accounts'].at[from_idx, 'MinBalance']
    
    if from_bal - amount < min_bal:
        print(f"{Colors.RED}Insufficient balance. Min balance: ₹{min_bal}{Colors.END}")
        return data
    
    if amount > DAILY_TRANSFER_LIMIT:
        print(f"{Colors.RED}Exceeds daily transfer limit of ₹{DAILY_TRANSFER_LIMIT:,}{Colors.END}")
        return data
    
    # Process transfer
    to_idx = to_account.index[0]
    
    new_from_bal = from_bal - amount
    new_to_bal = data['accounts'].at[to_idx, 'Balance'] + amount
    
    data['accounts'].at[from_idx, 'Balance'] = new_from_bal
    data['accounts'].at[to_idx, 'Balance'] = new_to_bal
    
    # Generate transfer reference
    transfer_ref = f"TRF{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Record transfer
    transfer_type = 'Internal' if choice == '1' else 'Inter-Customer'
    transfer_record = {
        'TransferID': f"XFER{len(data['transfers'])+1:05d}",
        'FromAccount': from_acc,
        'ToAccount': to_acc,
        'Amount': amount,
        'TransferType': transfer_type,
        'Charges': 0,
        'Date': get_date(),
        'Status': 'Success',
        'Reference': transfer_ref
    }
    data['transfers'] = pd.concat([data['transfers'], pd.DataFrame([transfer_record])], ignore_index=True)
    
    # Create debit transaction for sender
    txn_debit = {
        'TransactionID': f"TXN{len(data['transactions'])+1:05d}",
        'AccountNumber': from_acc,
        'TransactionType': 'Fund Transfer',
        'Amount': amount,
        'DebitCredit': 'Debit',
        'Balance_After': new_from_bal,
        'Date': get_date(),
        'Time': datetime.now().strftime("%H:%M:%S"),
        'Remarks': f'Transfer to {to_acc} Ref:{transfer_ref}',
        'Status': 'Success'
    }
    data['transactions'] = pd.concat([data['transactions'], pd.DataFrame([txn_debit])], ignore_index=True)
    
    # Create credit transaction for receiver
    txn_credit = {
        'TransactionID': f"TXN{len(data['transactions'])+1:05d}",
        'AccountNumber': to_acc,
        'TransactionType': 'Fund Transfer',
        'Amount': amount,
        'DebitCredit': 'Credit',
        'Balance_After': new_to_bal,
        'Date': get_date(),
        'Time': datetime.now().strftime("%H:%M:%S"),
        'Remarks': f'Transfer from {from_acc} Ref:{transfer_ref}',
        'Status': 'Success'
    }
    data['transactions'] = pd.concat([data['transactions'], pd.DataFrame([txn_credit])], ignore_index=True)
    
    print(f"{Colors.GREEN}✓ Transfer Successful!{Colors.END}")
    print(f"Reference: {transfer_ref}")
    print(f"Amount: ₹{amount:,.2f}")
    print(f"From {from_acc}: ₹{new_from_bal:,.2f}")
    print(f"To {to_acc}: ₹{new_to_bal:,.2f}")
    
    data = log_audit(data, 'FUND_TRANSFER', f'₹{amount} from {from_acc} to {to_acc}')
    return data

# ==========================================
# SECTION 6: CARD MANAGEMENT SYSTEM
# ==========================================

def card_management_menu(data):
    """Card Management Sub-Menu"""
    while True:
        print(f"\n{Colors.BOLD}{Colors.BLUE}=== CARD MANAGEMENT ==={Colors.END}")
        print("1. Issue New Card")
        print("2. View My Cards")
        print("3. Block/Unblock Card")
        print("4. View Card Transactions")
        print("5. Change Card PIN")
        print("6. Back to Main Menu")
        
        choice = input("\nSelect: ").strip()
        
        if choice == '1': data = issue_new_card(data)
        elif choice == '2': view_cards(data)
        elif choice == '3': data = toggle_card_status(data)
        elif choice == '4': view_card_transactions(data)
        elif choice == '5': data = change_card_pin(data)
        elif choice == '6': break
        else: print("Invalid option.")
    
    return data

def issue_new_card(data):
    """Issue a new debit/credit card"""
    print(f"\n{Colors.CYAN}--- Issue New Card ---{Colors.END}")
    
    cust_id = input("Customer ID: ").strip()
    if data['customers'][data['customers']['CustomerID'] == cust_id].empty:
        print(f"{Colors.RED}Customer not found{Colors.END}")
        return data
    
    # Show customer's accounts
    accounts = data['accounts'][data['accounts']['CustomerID'] == cust_id]
    if accounts.empty:
        print(f"{Colors.RED}No accounts found for this customer{Colors.END}")
        return data
    
    print("\nCustomer Accounts:")
    print(accounts[['AccountNumber', 'AccountType', 'Balance']].to_string(index=False))
    
    acc_num = input("\nLink to Account Number: ").strip()
    if data['accounts'][(data['accounts']['AccountNumber'] == acc_num) & 
                        (data['accounts']['CustomerID'] == cust_id)].empty:
        print(f"{Colors.RED}Account not found or doesn't belong to customer{Colors.END}")
        return data
    
    print("\nCard Type:")
    print("1. Debit Card")
    print("2. Credit Card")
    card_choice = input("Select: ").strip()
    
    card_type = 'Debit' if card_choice == '1' else 'Credit'
    credit_limit = 0
    
    if card_type == 'Credit':
        credit_limit = float(input(f"Credit Limit (default ₹{CREDIT_CARD_LIMIT_DEFAULT}): ").strip() or CREDIT_CARD_LIMIT_DEFAULT)
    
    # Generate card details
    card_number = generate_card_number()
    cvv = generate_cvv()
    pin = input("Set 4-digit PIN: ").strip()
    
    if len(pin) != 4 or not pin.isdigit():
        print(f"{Colors.RED}Invalid PIN format{Colors.END}")
        return data
    
    issue_date = get_date()
    expiry_date = (datetime.now() + timedelta(days=CARD_VALIDITY_YEARS*365)).strftime("%Y-%m-%d")
    
    new_card = {
        'CardNumber': card_number,
        'CustomerID': cust_id,
        'LinkedAccount': acc_num,
        'CardType': card_type,
        'CreditLimit': credit_limit,
        'IssueDate': issue_date,
        'ExpiryDate': expiry_date,
        'CVV': cvv,
        'PIN_Hash': hash_password(pin),
        'Status': 'Active'
    }
    
    data['cards'] = pd.concat([data['cards'], pd.DataFrame([new_card])], ignore_index=True)
    
    print(f"\n{Colors.GREEN}✓ Card Issued Successfully!{Colors.END}")
    print(f"{'='*40}")
    print(f"Card Number: {mask_card_number(card_number)}")
    print(f"Card Type:   {card_type}")
    print(f"Linked A/C:  {acc_num}")
    print(f"Valid Till:  {expiry_date}")
    print(f"CVV:         {cvv} (Keep Secret!)")
    print(f"{'='*40}")
    print(f"{Colors.YELLOW}Note: Full card number will be printed on physical card.{Colors.END}")
    
    data = log_audit(data, 'CARD_ISSUED', f'{card_type} card for {cust_id}')
    return data

def view_cards(data):
    """View cards for a customer"""
    print(f"\n{Colors.CYAN}--- View Cards ---{Colors.END}")
    cust_id = input("Customer ID: ").strip()
    
    cards = data['cards'][data['cards']['CustomerID'] == cust_id]
    if cards.empty:
        print("No cards found.")
        return
    
    print(f"\n{'='*70}")
    for _, card in cards.iterrows():
        card_num = str(card.get('CardNumber', 'N/A'))
        print(f"Card:    {mask_card_number(card_num)}")
        print(f"Type:    {card.get('CardType', 'N/A')}")
        # Handle both LinkedAccount and AccountNumber column names
        linked_acc = card.get('LinkedAccount') or card.get('AccountNumber') or 'Not Linked'
        if pd.isna(linked_acc) or linked_acc is None:
            linked_acc = 'Not Linked'
        print(f"Account: {linked_acc}")
        print(f"Expiry:  {card.get('ExpiryDate', 'N/A')}")
        print(f"Status:  {card.get('Status', 'N/A')}")
        card_type = card.get('CardType', '')
        if card_type == 'Credit' or 'Credit' in str(card_type):
            credit_limit = card.get('CreditLimit', 0)
            if pd.notna(credit_limit):
                print(f"Limit:   ₹{float(credit_limit):,.2f}")
        print(f"{'-'*70}")

def toggle_card_status(data):
    """Block or unblock a card"""
    print(f"\n{Colors.CYAN}--- Block/Unblock Card ---{Colors.END}")
    
    card_num = input("Enter last 4 digits of card: ").strip()
    cards = data['cards'][data['cards']['CardNumber'].str.endswith(card_num)]
    
    if cards.empty:
        print("Card not found.")
        return data
    
    card = cards.iloc[0]
    idx = cards.index[0]
    current_status = card['Status']
    
    print(f"Current Status: {current_status}")
    
    if current_status == 'Active':
        confirm = input("Block this card? (yes/no): ").strip().lower()
        if confirm == 'yes':
            data['cards'].at[idx, 'Status'] = 'Blocked'
            print(f"{Colors.GREEN}✓ Card blocked successfully{Colors.END}")
            data = log_audit(data, 'CARD_BLOCKED', f'Card ending {card_num}')
    else:
        confirm = input("Unblock this card? (yes/no): ").strip().lower()
        if confirm == 'yes':
            data['cards'].at[idx, 'Status'] = 'Active'
            print(f"{Colors.GREEN}✓ Card unblocked successfully{Colors.END}")
            data = log_audit(data, 'CARD_UNBLOCKED', f'Card ending {card_num}')
    
    return data

def view_card_transactions(data):
    """View transactions made by a card's linked account"""
    print(f"\n{Colors.CYAN}--- Card Transactions ---{Colors.END}")
    
    card_num = input("Enter last 4 digits of card: ").strip()
    cards = data['cards'][data['cards']['CardNumber'].str.endswith(card_num)]
    
    if cards.empty:
        print("Card not found.")
        return
    
    linked_acc = cards.iloc[0]['LinkedAccount']
    txns = data['transactions'][data['transactions']['AccountNumber'] == linked_acc].tail(10)
    
    if txns.empty:
        print("No transactions found.")
        return
    
    print(f"\nLast 10 transactions for card ending {card_num}:")
    print(txns[['Date', 'TransactionType', 'Amount', 'DebitCredit', 'Balance_After']].to_string(index=False))

def change_card_pin(data):
    """Change card PIN"""
    print(f"\n{Colors.CYAN}--- Change Card PIN ---{Colors.END}")
    
    card_num = input("Enter last 4 digits of card: ").strip()
    cards = data['cards'][data['cards']['CardNumber'].str.endswith(card_num)]
    
    if cards.empty:
        print("Card not found.")
        return data
    
    idx = cards.index[0]
    old_pin = input("Current PIN: ").strip()
    
    if not verify_password(old_pin, cards.iloc[0]['PIN_Hash']):
        print(f"{Colors.RED}Incorrect PIN{Colors.END}")
        return data
    
    new_pin = input("New 4-digit PIN: ").strip()
    confirm_pin = input("Confirm new PIN: ").strip()
    
    if new_pin != confirm_pin:
        print(f"{Colors.RED}PINs don't match{Colors.END}")
        return data
    
    if len(new_pin) != 4 or not new_pin.isdigit():
        print(f"{Colors.RED}Invalid PIN format{Colors.END}")
        return data
    
    data['cards'].at[idx, 'PIN_Hash'] = hash_password(new_pin)
    print(f"{Colors.GREEN}✓ PIN changed successfully{Colors.END}")
    
    data = log_audit(data, 'PIN_CHANGED', f'Card ending {card_num}')
    return data

# ==========================================
# SECTION 7: CHEQUE PROCESSING SYSTEM
# ==========================================

def cheque_management_menu(data):
    """Cheque Processing Sub-Menu"""
    while True:
        print(f"\n{Colors.BOLD}{Colors.BLUE}=== CHEQUE PROCESSING ==={Colors.END}")
        print("1. Issue New Cheque")
        print("2. Deposit Cheque")
        print("3. View Cheque Status")
        print("4. Cancel Cheque")
        print("5. View All Cheques")
        print("6. Back to Main Menu")
        
        choice = input("\nSelect: ").strip()
        
        if choice == '1': data = issue_cheque(data)
        elif choice == '2': data = deposit_cheque(data)
        elif choice == '3': check_cheque_status(data)
        elif choice == '4': data = cancel_cheque(data)
        elif choice == '5': view_all_cheques(data)
        elif choice == '6': break
        else: print("Invalid option.")
    
    return data

def issue_cheque(data):
    """Issue a new cheque"""
    print(f"\n{Colors.CYAN}--- Issue Cheque ---{Colors.END}")
    
    acc_num = input("From Account Number: ").strip()
    account = data['accounts'][data['accounts']['AccountNumber'] == acc_num]
    
    if account.empty:
        print(f"{Colors.RED}Account not found{Colors.END}")
        return data
    
    issued_to = input("Payee Name: ").strip()
    amount = float(input("Amount: ₹").strip())
    
    balance = account.iloc[0]['Balance']
    min_bal = account.iloc[0]['MinBalance']
    
    if balance - amount < min_bal:
        print(f"{Colors.RED}Insufficient balance for cheque amount{Colors.END}")
        return data
    
    cheque_num = generate_cheque_number()
    
    new_cheque = {
        'ChequeNumber': cheque_num,
        'AccountNumber': acc_num,
        'IssuedTo': issued_to,
        'Amount': amount,
        'IssueDate': get_date(),
        'ClearanceDate': None,
        'Status': 'Issued',
        'Remarks': ''
    }
    
    data['cheques'] = pd.concat([data['cheques'], pd.DataFrame([new_cheque])], ignore_index=True)
    
    print(f"\n{Colors.GREEN}✓ Cheque Issued{Colors.END}")
    print(f"Cheque Number: {cheque_num}")
    print(f"Amount: ₹{amount:,.2f}")
    print(f"Payee: {issued_to}")
    
    data = log_audit(data, 'CHEQUE_ISSUED', f'Cheque {cheque_num} for ₹{amount}')
    return data

def deposit_cheque(data):
    """Deposit/Clear a cheque"""
    print(f"\n{Colors.CYAN}--- Deposit Cheque ---{Colors.END}")
    
    cheque_num = input("Cheque Number: ").strip()
    cheque = data['cheques'][data['cheques']['ChequeNumber'] == cheque_num]
    
    if cheque.empty:
        print(f"{Colors.RED}Cheque not found{Colors.END}")
        return data
    
    cheque_row = cheque.iloc[0]
    
    if cheque_row['Status'] != 'Issued':
        print(f"{Colors.RED}Cheque cannot be deposited. Status: {cheque_row['Status']}{Colors.END}")
        return data
    
    to_acc = input("Deposit to Account Number: ").strip()
    to_account = data['accounts'][data['accounts']['AccountNumber'] == to_acc]
    
    if to_account.empty:
        print(f"{Colors.RED}Destination account not found{Colors.END}")
        return data
    
    # Check if source account has sufficient balance
    from_acc = cheque_row['AccountNumber']
    from_account = data['accounts'][data['accounts']['AccountNumber'] == from_acc]
    from_idx = from_account.index[0]
    from_bal = data['accounts'].at[from_idx, 'Balance']
    min_bal = data['accounts'].at[from_idx, 'MinBalance']
    amount = cheque_row['Amount']
    
    if from_bal - amount < min_bal:
        # Bounce the cheque
        idx = cheque.index[0]
        data['cheques'].at[idx, 'Status'] = 'Bounced'
        data['cheques'].at[idx, 'Remarks'] = 'Insufficient funds'
        print(f"{Colors.RED}Cheque bounced! Insufficient funds in issuer account.{Colors.END}")
        data = log_audit(data, 'CHEQUE_BOUNCED', f'Cheque {cheque_num} bounced')
        return data
    
    # Process cheque clearance
    # Debit from source
    new_from_bal = from_bal - amount
    data['accounts'].at[from_idx, 'Balance'] = new_from_bal
    
    # Credit to destination
    to_idx = to_account.index[0]
    new_to_bal = data['accounts'].at[to_idx, 'Balance'] + amount
    data['accounts'].at[to_idx, 'Balance'] = new_to_bal
    
    # Update cheque status
    idx = cheque.index[0]
    data['cheques'].at[idx, 'Status'] = 'Cleared'
    data['cheques'].at[idx, 'ClearanceDate'] = get_date()
    
    # Create transactions
    txn_debit = {
        'TransactionID': f"TXN{len(data['transactions'])+1:05d}",
        'AccountNumber': from_acc,
        'TransactionType': 'Cheque Debit',
        'Amount': amount,
        'DebitCredit': 'Debit',
        'Balance_After': new_from_bal,
        'Date': get_date(),
        'Time': datetime.now().strftime("%H:%M:%S"),
        'Remarks': f'Cheque {cheque_num} cleared',
        'Status': 'Success'
    }
    data['transactions'] = pd.concat([data['transactions'], pd.DataFrame([txn_debit])], ignore_index=True)
    
    txn_credit = {
        'TransactionID': f"TXN{len(data['transactions'])+1:05d}",
        'AccountNumber': to_acc,
        'TransactionType': 'Cheque Credit',
        'Amount': amount,
        'DebitCredit': 'Credit',
        'Balance_After': new_to_bal,
        'Date': get_date(),
        'Time': datetime.now().strftime("%H:%M:%S"),
        'Remarks': f'Cheque {cheque_num} deposited',
        'Status': 'Success'
    }
    data['transactions'] = pd.concat([data['transactions'], pd.DataFrame([txn_credit])], ignore_index=True)
    
    print(f"\n{Colors.GREEN}✓ Cheque Cleared Successfully!{Colors.END}")
    print(f"Amount: ₹{amount:,.2f}")
    print(f"Deposited to: {to_acc}")
    
    data = log_audit(data, 'CHEQUE_CLEARED', f'Cheque {cheque_num} for ₹{amount}')
    return data

def check_cheque_status(data):
    """Check status of a cheque"""
    print(f"\n{Colors.CYAN}--- Cheque Status ---{Colors.END}")
    
    cheque_num = input("Cheque Number: ").strip()
    cheque = data['cheques'][data['cheques']['ChequeNumber'] == cheque_num]
    
    if cheque.empty:
        print("Cheque not found.")
        return
    
    row = cheque.iloc[0]
    print(f"\nCheque Number: {row['ChequeNumber']}")
    print(f"From Account: {row['AccountNumber']}")
    print(f"Payee:        {row['IssuedTo']}")
    print(f"Amount:       ₹{row['Amount']:,.2f}")
    print(f"Issue Date:   {row['IssueDate']}")
    print(f"Status:       {row['Status']}")
    if row['ClearanceDate']:
        print(f"Cleared On:   {row['ClearanceDate']}")
    if row['Remarks']:
        print(f"Remarks:      {row['Remarks']}")

def cancel_cheque(data):
    """Cancel an issued cheque"""
    print(f"\n{Colors.CYAN}--- Cancel Cheque ---{Colors.END}")
    
    cheque_num = input("Cheque Number: ").strip()
    cheque = data['cheques'][data['cheques']['ChequeNumber'] == cheque_num]
    
    if cheque.empty:
        print("Cheque not found.")
        return data
    
    if cheque.iloc[0]['Status'] != 'Issued':
        print(f"{Colors.RED}Only issued cheques can be cancelled{Colors.END}")
        return data
    
    confirm = input("Cancel this cheque? (yes/no): ").strip().lower()
    if confirm == 'yes':
        idx = cheque.index[0]
        data['cheques'].at[idx, 'Status'] = 'Cancelled'
        data['cheques'].at[idx, 'Remarks'] = 'Cancelled by account holder'
        print(f"{Colors.GREEN}✓ Cheque cancelled{Colors.END}")
        data = log_audit(data, 'CHEQUE_CANCELLED', f'Cheque {cheque_num}')
    
    return data

def view_all_cheques(data):
    """View all cheques for an account"""
    print(f"\n{Colors.CYAN}--- All Cheques ---{Colors.END}")
    
    acc_num = input("Account Number: ").strip()
    cheques = data['cheques'][data['cheques']['AccountNumber'] == acc_num]
    
    if cheques.empty:
        print("No cheques found.")
        return
    
    print(cheques[['ChequeNumber', 'IssuedTo', 'Amount', 'Status', 'IssueDate']].to_string(index=False))

# ==========================================
# SECTION 8: REPORTS & ANALYTICS
# ==========================================

def report_transaction_history(data):
    print(f"\n{Colors.CYAN}--- Transaction History ---{Colors.END}")
    acc_num = input("Enter Account Number: ").strip()
    
    txns = data['transactions'][data['transactions']['AccountNumber'] == acc_num]
    if txns.empty:
        print("No transactions found for this account.")
        return

    # Sort by date descending
    txns = txns.sort_values('Date', ascending=False)
    
    print(f"\nHistory for {acc_num}:")
    print("-" * 85)
    print(f"{'Date':<12} {'Type':<20} {'Amount':>12} {'Dr/Cr':<8} {'Balance':>15}")
    print("-" * 85)
    
    for _, row in txns.iterrows():
        # Handle None/NaN values safely
        date_val = str(row.get('Date', 'N/A') or 'N/A')[:10]
        txn_type = str(row.get('TransactionType', 'N/A') or 'N/A')[:18]
        amount = float(row.get('Amount', 0) or 0)
        debit_credit = str(row.get('DebitCredit', 'N/A') or 'N/A')
        
        # Get balance - check both column names
        balance = row.get('Balance_After') or row.get('BalanceAfter') or 0
        balance = float(balance) if pd.notna(balance) else 0
        
        print(f"{date_val:<12} {txn_type:<20} ₹{amount:>10,.2f} {debit_credit:<8} ₹{balance:>12,.2f}")
    print("-" * 85)

def report_bank_summary(data):
    print(f"\n{Colors.CYAN}--- Bank Financial Summary ---{Colors.END}")
    
    total_deposits = data['accounts']['Balance'].sum()
    total_loans = data['loans']['OutstandingAmount'].sum() if not data['loans'].empty else 0
    total_customers = len(data['customers'])
    total_accounts = len(data['accounts'])
    total_cards = len(data['cards'])
    
    # Calculate total transaction volume
    credit_txns = data['transactions'][data['transactions']['DebitCredit'] == 'Credit']['Amount'].sum() if not data['transactions'].empty else 0
    debit_txns = data['transactions'][data['transactions']['DebitCredit'] == 'Debit']['Amount'].sum() if not data['transactions'].empty else 0
    
    # Loan statistics
    active_loans = len(data['loans'][data['loans']['Status'] == 'Active']) if not data['loans'].empty else 0
    
    print(f"\n{'='*50}")
    print(f"{Colors.BOLD}FINANCIAL OVERVIEW{Colors.END}")
    print(f"{'='*50}")
    print(f"Total Deposits Held:     ₹{total_deposits:>15,.2f}")
    print(f"Total Loans Outstanding: ₹{total_loans:>15,.2f}")
    print(f"Net Liquidity:           ₹{(total_deposits - total_loans):>15,.2f}")
    print(f"{'='*50}")
    print(f"{Colors.BOLD}TRANSACTION VOLUME{Colors.END}")
    print(f"{'='*50}")
    print(f"Total Credit Volume:     ₹{credit_txns:>15,.2f}")
    print(f"Total Debit Volume:      ₹{debit_txns:>15,.2f}")
    print(f"Net Flow:                ₹{(credit_txns - debit_txns):>15,.2f}")
    print(f"{'='*50}")
    print(f"{Colors.BOLD}STATISTICS{Colors.END}")
    print(f"{'='*50}")
    print(f"Total Customers:         {total_customers:>15}")
    print(f"Total Accounts:          {total_accounts:>15}")
    print(f"Active Loans:            {active_loans:>15}")
    print(f"Cards Issued:            {total_cards:>15}")
    print(f"{'='*50}")

def report_customer_balances(data):
    print(f"\n{Colors.CYAN}--- Customer Balances Report ---{Colors.END}")
    
    if data['customers'].empty:
        print("No customers.")
        return

    print(f"\n{'ID':<10} {'Name':<25} {'Total Balance':<15} {'Accounts':<8} {'Loans':<6}")
    print("-" * 70)
    
    for _, cust in data['customers'].iterrows():
        cid = cust['CustomerID']
        accounts = data['accounts'][data['accounts']['CustomerID'] == cid]
        loans = data['loans'][data['loans']['CustomerID'] == cid] if not data['loans'].empty else pd.DataFrame()
        total_bal = accounts['Balance'].sum()
        acc_count = len(accounts)
        loan_count = len(loans)
        
        print(f"{cid:<10} {cust['Name']:<25} ₹{total_bal:<14,.2f} {acc_count:<8} {loan_count:<6}")

def report_daily_transactions(data):
    """Show today's transactions summary"""
    print(f"\n{Colors.CYAN}--- Daily Transaction Summary ---{Colors.END}")
    
    today = get_date()
    today_txns = data['transactions'][data['transactions']['Date'] == today]
    
    if today_txns.empty:
        print("No transactions today.")
        return
    
    credits = today_txns[today_txns['DebitCredit'] == 'Credit']
    debits = today_txns[today_txns['DebitCredit'] == 'Debit']
    
    print(f"\nDate: {today}")
    print(f"{'='*50}")
    print(f"Total Transactions: {len(today_txns)}")
    print(f"{'='*50}")
    print(f"Credits: {len(credits)} transactions, ₹{credits['Amount'].sum():,.2f}")
    print(f"Debits:  {len(debits)} transactions, ₹{debits['Amount'].sum():,.2f}")
    print(f"{'='*50}")
    print(f"\nTransaction Details:")
    print(today_txns[['TransactionID', 'AccountNumber', 'TransactionType', 'Amount', 'DebitCredit']].to_string(index=False))

def report_loan_portfolio(data):
    """Detailed loan portfolio analysis"""
    print(f"\n{Colors.CYAN}--- Loan Portfolio Analysis ---{Colors.END}")
    
    if data['loans'].empty:
        print("No loans in system.")
        return
    
    print(f"\n{'='*60}")
    print(f"{Colors.BOLD}LOAN PORTFOLIO SUMMARY{Colors.END}")
    print(f"{'='*60}")
    
    # By status
    status_summary = data['loans'].groupby('Status').agg({
        'LoanID': 'count',
        'PrincipalAmount': 'sum',
        'OutstandingAmount': 'sum'
    }).rename(columns={'LoanID': 'Count'})
    
    print(f"\nBy Status:")
    print(status_summary.to_string())
    
    # By type
    print(f"\n\nBy Loan Type:")
    type_summary = data['loans'].groupby('LoanType').agg({
        'LoanID': 'count',
        'PrincipalAmount': 'sum',
        'OutstandingAmount': 'sum',
        'InterestRate': 'mean'
    }).rename(columns={'LoanID': 'Count', 'InterestRate': 'Avg Rate'})
    print(type_summary.to_string())

def view_audit_trail(data):
    """View system audit trail"""
    print(f"\n{Colors.CYAN}--- Audit Trail ---{Colors.END}")
    
    if data['audit'].empty:
        print("No audit logs.")
        return
    
    print("1. View all logs")
    print("2. Filter by action type")
    print("3. Filter by date")
    
    choice = input("\nSelect: ").strip()
    
    if choice == '1':
        logs = data['audit'].tail(50)
    elif choice == '2':
        action = input("Enter action type (e.g., DEPOSIT, WITHDRAWAL, TRANSFER): ").strip().upper()
        logs = data['audit'][data['audit']['Action'].str.contains(action, case=False, na=False)]
    elif choice == '3':
        date = input("Enter date (YYYY-MM-DD): ").strip()
        logs = data['audit'][data['audit']['Timestamp'].str.startswith(date)]
    else:
        return
    
    if logs.empty:
        print("No matching logs found.")
        return
    
    print(f"\n{'-'*100}")
    print(f"{'Timestamp':<20} {'Action':<20} {'Details':<50} {'Status':<10}")
    print(f"{'-'*100}")
    
    for _, log in logs.iterrows():
        details = str(log['Details'])[:48] if log['Details'] else ''
        print(f"{str(log['Timestamp']):<20} {str(log['Action']):<20} {details:<50} {str(log['Status']):<10}")

def visualize_account_distribution(data):
    print(f"\n{Colors.CYAN}--- Generating Account Distribution Chart ---{Colors.END}")
    if data['accounts'].empty:
        print("No accounts data to visualize.")
        return

    try:
        # Group by Account Type
        type_counts = data['accounts']['AccountType'].value_counts()
        
        plt.figure(figsize=(10, 6))
        colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99', '#ff99cc']
        plt.pie(type_counts, labels=type_counts.index, autopct='%1.1f%%', startangle=140, colors=colors[:len(type_counts)])
        plt.title('Distribution of Account Types', fontsize=14, fontweight='bold')
        plt.axis('equal')
        
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
        loan_summary = data['loans'].groupby('LoanType')['PrincipalAmount'].sum()
        
        plt.figure(figsize=(12, 6))
        bars = loan_summary.plot(kind='bar', color=['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6'])
        plt.title('Total Loan Amount by Type', fontsize=14, fontweight='bold')
        plt.xlabel('Loan Type')
        plt.ylabel('Total Principal Amount (₹)')
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Add value labels on bars
        for i, v in enumerate(loan_summary):
            plt.text(i, v + v*0.01, f'₹{v:,.0f}', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        print("Displaying chart window...")
        plt.show()
    except Exception as e:
        print(f"{Colors.RED}Error generating chart: {e}{Colors.END}")

def visualize_monthly_transactions(data):
    """Monthly transaction trend chart"""
    print(f"\n{Colors.CYAN}--- Generating Monthly Transaction Trend ---{Colors.END}")
    
    if data['transactions'].empty:
        print("No transaction data to visualize.")
        return
    
    try:
        # Convert date and group by month
        txns = data['transactions'].copy()
        
        # Ensure Amount is numeric
        if 'Amount' in txns.columns:
            txns['Amount'] = pd.to_numeric(txns['Amount'], errors='coerce')
        else:
            print("No Amount column found in transactions.")
            return
        
        # Parse dates - handle multiple date formats
        if 'Date' in txns.columns:
            txns['Date'] = pd.to_datetime(txns['Date'], errors='coerce')
        else:
            print("No Date column found in transactions.")
            return
        
        # Remove rows with invalid dates or amounts
        txns = txns.dropna(subset=['Date', 'Amount'])
        
        if txns.empty:
            print("No valid transaction data to visualize.")
            return
        
        # Extract month and sum by month
        txns['Month'] = txns['Date'].dt.to_period('M')
        monthly = txns.groupby('Month')['Amount'].sum().sort_index()
        
        if monthly.empty or len(monthly) == 0:
            print("No data available for monthly trend chart.")
            return
        
        # Convert period index to string for plotting
        monthly.index = monthly.index.astype(str)
        
        plt.figure(figsize=(12, 6))
        plt.plot(range(len(monthly)), monthly.values, marker='o', linewidth=2, markersize=8, color='#2E86AB')
        plt.title('Monthly Transaction Volume', fontsize=14, fontweight='bold')
        plt.xlabel('Month')
        plt.ylabel('Total Amount (₹)')
        plt.xticks(range(len(monthly)), monthly.index, rotation=45)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        print("Displaying chart window...")
        plt.show()
    except Exception as e:
        print(f"{Colors.RED}Error generating chart: {str(e)}{Colors.END}")

def visualize_customer_growth(data):
    """Customer growth over time"""
    print(f"\n{Colors.CYAN}--- Generating Customer Growth Chart ---{Colors.END}")
    
    if data['customers'].empty:
        print("No customer data to visualize.")
        return
    
    try:
        customers = data['customers'].copy()
        customers['Month'] = pd.to_datetime(customers['RegistrationDate']).dt.to_period('M').astype(str)
        monthly_new = customers.groupby('Month').size().cumsum()
        
        plt.figure(figsize=(12, 6))
        plt.plot(monthly_new.index, monthly_new.values, marker='o', linewidth=2, markersize=8, color='#2ecc71')
        plt.fill_between(monthly_new.index, monthly_new.values, alpha=0.3, color='#2ecc71')
        plt.title('Cumulative Customer Growth', fontsize=14, fontweight='bold')
        plt.xlabel('Month')
        plt.ylabel('Total Customers')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        print("Displaying chart window...")
        plt.show()
    except Exception as e:
        print(f"{Colors.RED}Error generating chart: {e}{Colors.END}")

def customer_credit_score(data):
    """Calculate and display customer credit score"""
    print(f"\n{Colors.CYAN}--- Customer Credit Score ---{Colors.END}")
    
    cust_id = input("Enter Customer ID: ").strip()
    customer = data['customers'][data['customers']['CustomerID'] == cust_id]
    
    if customer.empty:
        print("Customer not found.")
        return
    
    # Calculate factors
    reg_date = datetime.strptime(customer.iloc[0]['RegistrationDate'], '%Y-%m-%d')
    account_age = (datetime.now() - reg_date).days
    
    accounts = data['accounts'][data['accounts']['CustomerID'] == cust_id]
    total_balance = accounts['Balance'].sum() if not accounts.empty else 0
    
    acc_nums = accounts['AccountNumber'].tolist()
    total_txns = len(data['transactions'][data['transactions']['AccountNumber'].isin(acc_nums)]) if not data['transactions'].empty else 0
    
    # Check for defaulted loans
    defaults = 0
    if not data['loans'].empty:
        cust_loans = data['loans'][data['loans']['CustomerID'] == cust_id]
        defaults = len(cust_loans[cust_loans['Status'] == 'Defaulted'])
    
    score = get_credit_score(account_age, total_txns, total_balance, defaults)
    
    # Determine rating
    if score >= 750:
        rating = "Excellent"
        color = Colors.GREEN
    elif score >= 650:
        rating = "Good"
        color = Colors.BLUE
    elif score >= 550:
        rating = "Fair"
        color = Colors.YELLOW
    else:
        rating = "Poor"
        color = Colors.RED
    
    print(f"\n{'='*50}")
    print(f"Customer: {customer.iloc[0]['Name']}")
    print(f"{'='*50}")
    print(f"Credit Score: {color}{score}{Colors.END}")
    print(f"Rating:       {color}{rating}{Colors.END}")
    print(f"{'='*50}")
    print(f"\nScore Factors:")
    print(f"  Account Age:       {account_age} days")
    print(f"  Total Transactions: {total_txns}")
    print(f"  Total Balance:     ₹{total_balance:,.2f}")
    print(f"  Loan Defaults:     {defaults}")

# ==========================================
# SECTION 8B: ADVANCED VISUALIZATIONS
# ==========================================

def visualize_balance_distribution(data):
    """Visualize balance distribution across customers"""
    print(f"\n{Colors.CYAN}--- Balance Distribution Analysis ---{Colors.END}")
    
    if data['accounts'].empty:
        print("No account data to visualize.")
        return
    
    try:
        # Merge accounts with customer names
        acc_cust = data['accounts'].merge(
            data['customers'][['CustomerID', 'Name']], 
            on='CustomerID', 
            how='left'
        )
        
        # Group by customer
        cust_balances = acc_cust.groupby('Name')['Balance'].sum().sort_values(ascending=True)
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # Horizontal bar chart
        colors = plt.cm.viridis(range(0, 256, 256//len(cust_balances)))
        axes[0].barh(cust_balances.index, cust_balances.values, color=colors)
        axes[0].set_xlabel('Total Balance (₹)')
        axes[0].set_title('Customer Balance Comparison', fontweight='bold')
        axes[0].xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x/1000:.0f}K'))
        
        # Balance ranges histogram
        ranges = [0, 100000, 300000, 500000, 1000000, float('inf')]
        labels = ['<₹1L', '₹1-3L', '₹3-5L', '₹5-10L', '>₹10L']
        balance_counts = pd.cut(cust_balances, bins=ranges, labels=labels).value_counts()
        axes[1].bar(balance_counts.index, balance_counts.values, color='#3498DB')
        axes[1].set_xlabel('Balance Range')
        axes[1].set_ylabel('Number of Customers')
        axes[1].set_title('Balance Distribution', fontweight='bold')
        
        plt.tight_layout()
        print("Displaying chart window...")
        plt.show()
    except Exception as e:
        print(f"{Colors.RED}Error generating chart: {str(e)}{Colors.END}")

def visualize_transaction_types(data):
    """Visualize transaction types breakdown"""
    print(f"\n{Colors.CYAN}--- Transaction Types Analysis ---{Colors.END}")
    
    if data['transactions'].empty:
        print("No transaction data to visualize.")
        return
    
    try:
        # Group by transaction type
        txn_types = data['transactions']['TransactionType'].value_counts()
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # Pie chart of transaction count
        colors = plt.cm.Set3(range(len(txn_types)))
        axes[0].pie(txn_types.values, labels=txn_types.index, autopct='%1.1f%%', 
                   colors=colors, startangle=90)
        axes[0].set_title('Transaction Types by Count', fontweight='bold')
        
        # Bar chart of total amounts by type
        txn_amounts = data['transactions'].groupby('TransactionType')['Amount'].sum().sort_values(ascending=False)
        axes[1].bar(range(len(txn_amounts)), txn_amounts.values, color='#2ECC71')
        axes[1].set_xticks(range(len(txn_amounts)))
        axes[1].set_xticklabels(txn_amounts.index, rotation=45, ha='right')
        axes[1].set_ylabel('Total Amount (₹)')
        axes[1].set_title('Transaction Volume by Type', fontweight='bold')
        axes[1].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x/100000:.1f}L'))
        
        plt.tight_layout()
        print("Displaying chart window...")
        plt.show()
    except Exception as e:
        print(f"{Colors.RED}Error generating chart: {str(e)}{Colors.END}")

def visualize_loan_emi_analysis(data):
    """Visualize loan EMI and outstanding analysis"""
    print(f"\n{Colors.CYAN}--- Loan EMI Analysis ---{Colors.END}")
    
    if data['loans'].empty:
        print("No loan data to visualize.")
        return
    
    try:
        loans = data['loans'].copy()
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # 1. Loan Type Distribution (Pie)
        loan_counts = loans['LoanType'].value_counts()
        axes[0, 0].pie(loan_counts.values, labels=loan_counts.index, autopct='%1.1f%%',
                      colors=plt.cm.Pastel1(range(len(loan_counts))))
        axes[0, 0].set_title('Loan Type Distribution', fontweight='bold')
        
        # 2. Principal vs Outstanding (Grouped Bar)
        loan_names = loans['LoanID'].tolist()
        x = range(len(loan_names))
        width = 0.35
        principal = loans['PrincipalAmount'].astype(float).tolist()
        outstanding = loans['OutstandingAmount'].astype(float).tolist()
        
        axes[0, 1].bar([i - width/2 for i in x], principal, width, label='Principal', color='#3498DB')
        axes[0, 1].bar([i + width/2 for i in x], outstanding, width, label='Outstanding', color='#E74C3C')
        axes[0, 1].set_xticks(x)
        axes[0, 1].set_xticklabels(loan_names, rotation=45)
        axes[0, 1].set_ylabel('Amount (₹)')
        axes[0, 1].set_title('Principal vs Outstanding', fontweight='bold')
        axes[0, 1].legend()
        axes[0, 1].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x/100000:.1f}L'))
        
        # 3. EMI by Loan
        emi_values = loans['EMI'].astype(float).tolist()
        axes[1, 0].bar(loan_names, emi_values, color='#9B59B6')
        axes[1, 0].set_ylabel('Monthly EMI (₹)')
        axes[1, 0].set_title('Monthly EMI by Loan', fontweight='bold')
        axes[1, 0].tick_params(axis='x', rotation=45)
        
        # 4. Repayment Progress
        progress = [(p - o) / p * 100 if p > 0 else 0 
                   for p, o in zip(principal, outstanding)]
        colors = ['#27AE60' if p > 50 else '#F39C12' if p > 25 else '#E74C3C' for p in progress]
        axes[1, 1].barh(loan_names, progress, color=colors)
        axes[1, 1].set_xlabel('Repayment Progress (%)')
        axes[1, 1].set_title('Loan Repayment Progress', fontweight='bold')
        axes[1, 1].set_xlim(0, 100)
        
        plt.tight_layout()
        print("Displaying chart window...")
        plt.show()
    except Exception as e:
        print(f"{Colors.RED}Error generating chart: {str(e)}{Colors.END}")

def visualize_daily_activity(data):
    """Visualize daily transaction activity heatmap style"""
    print(f"\n{Colors.CYAN}--- Daily Activity Analysis ---{Colors.END}")
    
    if data['transactions'].empty:
        print("No transaction data to visualize.")
        return
    
    try:
        txns = data['transactions'].copy()
        txns['Date'] = pd.to_datetime(txns['Date'], errors='coerce')
        txns = txns.dropna(subset=['Date'])
        
        if txns.empty:
            print("No valid date data to visualize.")
            return
        
        # Group by date
        daily = txns.groupby(txns['Date'].dt.date).agg({
            'Amount': ['sum', 'count']
        }).reset_index()
        daily.columns = ['Date', 'TotalAmount', 'TxnCount']
        daily = daily.sort_values('Date')
        
        fig, axes = plt.subplots(2, 1, figsize=(14, 8))
        
        # Transaction count by day
        axes[0].fill_between(range(len(daily)), daily['TxnCount'], alpha=0.5, color='#3498DB')
        axes[0].plot(range(len(daily)), daily['TxnCount'], color='#2980B9', linewidth=2)
        axes[0].set_ylabel('Number of Transactions')
        axes[0].set_title('Daily Transaction Count', fontweight='bold')
        axes[0].set_xticks(range(0, len(daily), max(1, len(daily)//10)))
        axes[0].set_xticklabels([str(d)[:10] for d in daily['Date'].iloc[::max(1, len(daily)//10)]], rotation=45)
        
        # Transaction volume by day
        axes[1].bar(range(len(daily)), daily['TotalAmount'], color='#27AE60', alpha=0.7)
        axes[1].set_ylabel('Total Volume (₹)')
        axes[1].set_xlabel('Date')
        axes[1].set_title('Daily Transaction Volume', fontweight='bold')
        axes[1].set_xticks(range(0, len(daily), max(1, len(daily)//10)))
        axes[1].set_xticklabels([str(d)[:10] for d in daily['Date'].iloc[::max(1, len(daily)//10)]], rotation=45)
        axes[1].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x/1000:.0f}K'))
        
        plt.tight_layout()
        print("Displaying chart window...")
        plt.show()
    except Exception as e:
        print(f"{Colors.RED}Error generating chart: {str(e)}{Colors.END}")

def visualize_comprehensive_dashboard(data):
    """Generate a comprehensive visual dashboard"""
    print(f"\n{Colors.CYAN}--- Comprehensive Analytics Dashboard ---{Colors.END}")
    
    try:
        fig = plt.figure(figsize=(16, 12))
        
        # 1. Account Type Distribution (Top Left)
        ax1 = fig.add_subplot(2, 3, 1)
        if not data['accounts'].empty:
            acc_types = data['accounts']['AccountType'].value_counts()
            ax1.pie(acc_types.values, labels=acc_types.index, autopct='%1.1f%%',
                   colors=['#3498DB', '#E74C3C', '#2ECC71', '#F39C12'])
        ax1.set_title('Account Types', fontweight='bold')
        
        # 2. Customer Registration Timeline (Top Middle)
        ax2 = fig.add_subplot(2, 3, 2)
        if not data['customers'].empty:
            cust = data['customers'].copy()
            cust['RegDate'] = pd.to_datetime(cust['RegistrationDate'], errors='coerce')
            cust = cust.dropna(subset=['RegDate']).sort_values('RegDate')
            cust['CumCount'] = range(1, len(cust) + 1)
            ax2.plot(cust['RegDate'], cust['CumCount'], marker='o', color='#9B59B6')
            ax2.set_xlabel('Date')
            ax2.set_ylabel('Total Customers')
            ax2.tick_params(axis='x', rotation=45)
        ax2.set_title('Customer Growth', fontweight='bold')
        
        # 3. Balance Summary (Top Right)
        ax3 = fig.add_subplot(2, 3, 3)
        total_balance = data['accounts']['Balance'].sum() if not data['accounts'].empty else 0
        total_loans = data['loans']['OutstandingAmount'].sum() if not data['loans'].empty else 0
        net_worth = total_balance - total_loans
        categories = ['Total Deposits', 'Loan Outstanding', 'Net Position']
        values = [total_balance, total_loans, net_worth]
        colors = ['#27AE60', '#E74C3C', '#3498DB']
        bars = ax3.bar(categories, values, color=colors)
        ax3.set_ylabel('Amount (₹)')
        ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x/100000:.1f}L'))
        ax3.set_title('Financial Summary', fontweight='bold')
        
        # 4. Transaction Trend (Bottom Left)
        ax4 = fig.add_subplot(2, 3, 4)
        if not data['transactions'].empty:
            txns = data['transactions'].copy()
            txns['Date'] = pd.to_datetime(txns['Date'], errors='coerce')
            txns['Amount'] = pd.to_numeric(txns['Amount'], errors='coerce')
            txns = txns.dropna(subset=['Date', 'Amount'])
            if not txns.empty:
                txns['Month'] = txns['Date'].dt.to_period('M')
                monthly = txns.groupby('Month')['Amount'].sum().sort_index()
                monthly.index = monthly.index.astype(str)
                ax4.bar(range(len(monthly)), monthly.values, color='#1ABC9C')
                ax4.set_xticks(range(len(monthly)))
                ax4.set_xticklabels(monthly.index, rotation=45)
        ax4.set_xlabel('Month')
        ax4.set_ylabel('Volume (₹)')
        ax4.set_title('Monthly Transaction Volume', fontweight='bold')
        
        # 5. Loan Status (Bottom Middle)
        ax5 = fig.add_subplot(2, 3, 5)
        if not data['loans'].empty:
            loan_status = data['loans']['Status'].value_counts()
            colors_status = {'Active': '#27AE60', 'Closed': '#95A5A6', 'Defaulted': '#E74C3C'}
            ax5.pie(loan_status.values, labels=loan_status.index, autopct='%1.1f%%',
                   colors=[colors_status.get(s, '#3498DB') for s in loan_status.index])
        ax5.set_title('Loan Status', fontweight='bold')
        
        # 6. Top Customers by Balance (Bottom Right)
        ax6 = fig.add_subplot(2, 3, 6)
        if not data['accounts'].empty:
            cust_bal = data['accounts'].groupby('CustomerID')['Balance'].sum().nlargest(5)
            cust_names = []
            for cid in cust_bal.index:
                cust = data['customers'][data['customers']['CustomerID'] == cid]
                name = cust.iloc[0]['Name'].split()[0] if not cust.empty else cid
                cust_names.append(name)
            ax6.barh(cust_names, cust_bal.values, color='#F39C12')
            ax6.set_xlabel('Balance (₹)')
        ax6.set_title('Top 5 Customers', fontweight='bold')
        
        plt.suptitle('COREBANK ANALYTICS DASHBOARD', fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
        print("Displaying comprehensive dashboard...")
        plt.show()
    except Exception as e:
        print(f"{Colors.RED}Error generating dashboard: {str(e)}{Colors.END}")

def export_database_summary(data):
    """Export a clean summary of the entire database"""
    print(f"\n{Colors.CYAN}--- Database Summary Export ---{Colors.END}")
    
    print(f"\n{Colors.BOLD}╔{'═'*60}╗")
    print(f"║{'COREBANK DATABASE SUMMARY':^60}║")
    print(f"╚{'═'*60}╝{Colors.END}")
    
    print(f"\n{Colors.YELLOW}=== CUSTOMERS TABLE ==={Colors.END}")
    print(f"Total Records: {len(data['customers'])}")
    if not data['customers'].empty:
        print(data['customers'][['CustomerID', 'Name', 'City', 'Phone', 'Status']].to_string(index=False))
    
    print(f"\n{Colors.YELLOW}=== ACCOUNTS TABLE ==={Colors.END}")
    print(f"Total Records: {len(data['accounts'])}")
    if not data['accounts'].empty:
        acc_display = data['accounts'][['AccountNumber', 'CustomerID', 'AccountType', 'Balance', 'Status']].copy()
        acc_display['Balance'] = acc_display['Balance'].apply(lambda x: f"₹{x:,.2f}")
        print(acc_display.to_string(index=False))
    
    print(f"\n{Colors.YELLOW}=== TRANSACTIONS TABLE ==={Colors.END}")
    print(f"Total Records: {len(data['transactions'])}")
    if not data['transactions'].empty:
        txn_display = data['transactions'][['TransactionID', 'AccountNumber', 'TransactionType', 'Amount', 'Date']].head(20).copy()
        txn_display['Amount'] = txn_display['Amount'].apply(lambda x: f"₹{float(x):,.2f}" if pd.notna(x) else 'N/A')
        print(txn_display.to_string(index=False))
        if len(data['transactions']) > 20:
            print(f"  ... and {len(data['transactions']) - 20} more records")
    
    print(f"\n{Colors.YELLOW}=== LOANS TABLE ==={Colors.END}")
    print(f"Total Records: {len(data['loans'])}")
    if not data['loans'].empty:
        loan_display = data['loans'][['LoanID', 'CustomerID', 'LoanType', 'PrincipalAmount', 'EMI', 'OutstandingAmount', 'Status']].copy()
        for col in ['PrincipalAmount', 'EMI', 'OutstandingAmount']:
            loan_display[col] = loan_display[col].apply(lambda x: f"₹{float(x):,.2f}" if pd.notna(x) else 'N/A')
        print(loan_display.to_string(index=False))
    
    print(f"\n{Colors.YELLOW}=== CARDS TABLE ==={Colors.END}")
    print(f"Total Records: {len(data['cards'])}")
    if not data['cards'].empty:
        cards_display = data['cards'].copy()
        # Safely get card number column
        card_num_col = 'CardNumber' if 'CardNumber' in cards_display.columns else 'CardID'
        if card_num_col in cards_display.columns:
            cards_display['MaskedCard'] = cards_display[card_num_col].apply(lambda x: f"XXXX-{str(x)[-4:]}" if pd.notna(x) else 'N/A')
        else:
            cards_display['MaskedCard'] = 'N/A'
        print(cards_display[['MaskedCard', 'CustomerID', 'CardType', 'Status']].to_string(index=False))
    
    print(f"\n{Colors.YELLOW}=== CHEQUES TABLE ==={Colors.END}")
    print(f"Total Records: {len(data['cheques'])}")
    if not data['cheques'].empty:
        cheque_display = data['cheques'][['ChequeNumber', 'AccountNumber', 'IssuedTo', 'Amount', 'Status']].copy()
        cheque_display['Amount'] = cheque_display['Amount'].apply(lambda x: f"₹{float(x):,.2f}" if pd.notna(x) else 'N/A')
        print(cheque_display.to_string(index=False))
    
    print(f"\n{Colors.YELLOW}=== TRANSFERS TABLE ==={Colors.END}")
    print(f"Total Records: {len(data['transfers'])}")
    if not data['transfers'].empty:
        transfer_display = data['transfers'][['TransferID', 'FromAccount', 'ToAccount', 'Amount', 'Date', 'Status']].copy()
        transfer_display['Amount'] = transfer_display['Amount'].apply(lambda x: f"₹{float(x):,.2f}" if pd.notna(x) else 'N/A')
        print(transfer_display.to_string(index=False))
    
    print(f"\n{Colors.YELLOW}=== AUDIT LOGS TABLE ==={Colors.END}")
    print(f"Total Records: {len(data['audit'])}")
    if not data['audit'].empty:
        print(data['audit'][['LogID', 'Action', 'Timestamp', 'Status']].tail(10).to_string(index=False))
        print(f"  (Showing last 10 entries)")
    
    print(f"\n{Colors.GREEN}{'═'*60}")
    print(f"DATABASE STATISTICS")
    print(f"{'═'*60}{Colors.END}")
    print(f"  Total Customers:     {len(data['customers'])}")
    print(f"  Total Accounts:      {len(data['accounts'])}")
    print(f"  Total Transactions:  {len(data['transactions'])}")
    print(f"  Total Loans:         {len(data['loans'])}")
    print(f"  Total Cards:         {len(data['cards'])}")
    print(f"  Total Cheques:       {len(data['cheques'])}")
    print(f"  Total Transfers:     {len(data['transfers'])}")
    print(f"  Total Audit Logs:    {len(data['audit'])}")
    total_records = sum(len(data[t]) for t in data)
    print(f"\n  {Colors.BOLD}GRAND TOTAL: {total_records} records{Colors.END}")

def generate_reports(data):
    while True:
        print(f"\n{Colors.BOLD}{Colors.BLUE}=== REPORTS & ANALYTICS ==={Colors.END}")
        print(f"\n{Colors.YELLOW}Text Reports:{Colors.END}")
        print("1.  Transaction History")
        print("2.  Bank Financial Summary")
        print("3.  Customer Balances Report")
        print("4.  Daily Transactions Summary")
        print("5.  Loan Portfolio Analysis")
        print("6.  View Audit Trail")
        print("7.  Customer Credit Score")
        print("8.  Database Summary (All Tables)")
        print(f"\n{Colors.YELLOW}Visual Charts (Matplotlib):{Colors.END}")
        print("9.  Account Distribution (Pie Chart)")
        print("10. Loan Portfolio (Bar Chart)")
        print("11. Monthly Transaction Trend")
        print("12. Customer Growth Chart")
        print("13. Balance Distribution Analysis")
        print("14. Transaction Types Breakdown")
        print("15. Loan EMI Analysis (4 Charts)")
        print("16. Daily Activity Timeline")
        print("17. Comprehensive Dashboard (6 Charts)")
        print(f"\n18. Back to Main Menu")
        
        choice = input("\nSelect Report: ").strip()
        
        if choice == '1': report_transaction_history(data)
        elif choice == '2': report_bank_summary(data)
        elif choice == '3': report_customer_balances(data)
        elif choice == '4': report_daily_transactions(data)
        elif choice == '5': report_loan_portfolio(data)
        elif choice == '6': view_audit_trail(data)
        elif choice == '7': customer_credit_score(data)
        elif choice == '8': export_database_summary(data)
        elif choice == '9': visualize_account_distribution(data)
        elif choice == '10': visualize_loan_status(data)
        elif choice == '11': visualize_monthly_transactions(data)
        elif choice == '12': visualize_customer_growth(data)
        elif choice == '13': visualize_balance_distribution(data)
        elif choice == '14': visualize_transaction_types(data)
        elif choice == '15': visualize_loan_emi_analysis(data)
        elif choice == '16': visualize_daily_activity(data)
        elif choice == '17': visualize_comprehensive_dashboard(data)
        elif choice == '18': break
        else: print("Invalid option.")

# ==========================================
# SECTION 9: MENUS & MAIN LOOP
# ==========================================

def dashboard(data):
    print(f"\n{Colors.BOLD}{Colors.BLUE}╔══════════════════════════════════════════╗")
    print(f"║       COREBANK MANAGEMENT SYSTEM         ║")
    print(f"╚══════════════════════════════════════════╝{Colors.END}")
    print(f"\n{Colors.CYAN}Quick Stats:{Colors.END}")
    print(f"  Customers: {len(data['customers']):<8} Accounts: {len(data['accounts']):<8} Cards: {len(data['cards'])}")
    total_balance = data['accounts']['Balance'].sum() if not data['accounts'].empty else 0
    total_loans = data['loans']['OutstandingAmount'].sum() if not data['loans'].empty else 0
    print(f"  Balance:   ₹{total_balance:,.2f}")
    print(f"  Loans:     {len(data['loans']):<8} Outstanding: ₹{total_loans:,.2f}")
    print(f"  Time:      {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{Colors.CYAN}{'─'*44}{Colors.END}")

def loan_management_menu(data):
    """Loan Management Sub-Menu"""
    while True:
        print(f"\n{Colors.BOLD}{Colors.BLUE}=== LOAN MANAGEMENT ==={Colors.END}")
        print("1. Apply for Loan")
        print("2. Pay Loan EMI")
        print("3. View Loan Details")
        print("4. View All Loans")
        print("5. Back to Main Menu")
        
        choice = input("\nSelect: ").strip()
        
        if choice == '1': data = apply_loan(data)
        elif choice == '2': data = pay_loan_emi(data)
        elif choice == '3': view_loan_details(data)
        elif choice == '4':
            if data['loans'].empty:
                print("No loans found.")
            else:
                print(data['loans'][['LoanID', 'CustomerID', 'LoanType', 'PrincipalAmount', 'EMI', 'OutstandingAmount', 'Status']].to_string(index=False))
        elif choice == '5': break
        else: print("Invalid option.")
        
        save_data(data)
    
    return data

# ==========================================
# SECTION 9A: ADVANCED FEATURES
# ==========================================

def generate_account_statement(data):
    """Generate detailed account statement"""
    print(f"\n{Colors.CYAN}--- Account Statement ---{Colors.END}")
    
    acc_num = input("Account Number: ").strip()
    account = data['accounts'][data['accounts']['AccountNumber'] == acc_num]
    
    if account.empty:
        print(f"{Colors.RED}Account not found{Colors.END}")
        return
    
    acc = account.iloc[0]
    customer_id = acc['CustomerID']
    customer = data['customers'][data['customers']['CustomerID'] == customer_id]
    
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}")
    print(f"{'COREBANK ACCOUNT STATEMENT':^60}")
    print(f"{'='*60}{Colors.END}\n")
    
    print(f"Account Holder: {customer.iloc[0]['Name']}")
    print(f"Account Number: {acc_num}")
    print(f"Account Type: {acc['AccountType']}")
    print(f"Statement Date: {get_date()}")
    print(f"\n{Colors.CYAN}Account Summary:{Colors.END}")
    print(f"  Opening Balance: ₹{acc['Balance']:,.2f}")
    print(f"  Current Balance: ₹{acc['Balance']:,.2f}")
    print(f"  Interest Rate: {acc['InterestRate']:.2f}%")
    print(f"  Minimum Balance: ₹{acc['MinBalance']:,.2f}")
    print(f"  Status: {acc['Status']}")
    
    # Get last 10 transactions
    trans = data['transactions'][data['transactions']['AccountNumber'] == acc_num]
    if not trans.empty:
        trans_sorted = trans.sort_values('Date', ascending=False).head(10)
        print(f"\n{Colors.CYAN}Recent Transactions (Last 10):{Colors.END}")
        print(f"{'-'*60}")
        for idx, t in trans_sorted.iterrows():
            txn_type = str(t.get('TransactionType', 'N/A') or 'N/A')
            symbol = "+" if txn_type in ['Deposit', 'Credit', 'Cheque Credit', 'Transfer Credit'] else "-"
            amount = float(t.get('Amount', 0) or 0)
            # Handle both column naming conventions
            balance = t.get('Balance_After') or t.get('BalanceAfter') or 0
            balance = float(balance) if pd.notna(balance) else 0
            date_str = str(t.get('Date', 'N/A') or 'N/A')[:10]
            print(f"{date_str:12} {txn_type[:10]:10} {symbol}₹{abs(amount):>10,.2f} Balance: ₹{balance:>12,.2f}")
        print(f"{'-'*60}\n")
    else:
        print(f"\n{Colors.YELLOW}No transactions found{Colors.END}\n")

def calculate_account_interest(data):
    """Calculate interest accrued on accounts"""
    print(f"\n{Colors.CYAN}--- Interest Calculator ---{Colors.END}")
    
    acc_num = input("Account Number: ").strip()
    account = data['accounts'][data['accounts']['AccountNumber'] == acc_num]
    
    if account.empty:
        print(f"{Colors.RED}Account not found{Colors.END}")
        return
    
    acc = account.iloc[0]
    months = int(input("Number of months to calculate: "))
    
    balance = acc['Balance']
    rate = acc['InterestRate']
    
    # Simple interest
    simple_interest = (balance * rate * months) / (100 * 12)
    
    # Compound interest (quarterly)
    compound_interest = balance * ((1 + rate/(100*4))**(months/3) - 1)
    
    final_balance_simple = balance + simple_interest
    final_balance_compound = balance + compound_interest
    
    print(f"\n{Colors.BOLD}{Colors.BLUE}Interest Calculation{Colors.END}")
    print(f"Current Balance: ₹{balance:,.2f}")
    print(f"Annual Interest Rate: {rate:.2f}%")
    print(f"Period: {months} months")
    print(f"\n{Colors.CYAN}Results:{Colors.END}")
    print(f"  Simple Interest: ₹{simple_interest:,.2f}")
    print(f"  Final Balance (Simple): ₹{final_balance_simple:,.2f}")
    print(f"\n  Compound Interest: ₹{compound_interest:,.2f}")
    print(f"  Final Balance (Compound): ₹{final_balance_compound:,.2f}")

def view_customer_financial_dashboard(data):
    """Comprehensive customer financial dashboard"""
    print(f"\n{Colors.CYAN}--- Customer Financial Dashboard ---{Colors.END}")
    
    cust_id = input("Customer ID: ").strip()
    customer = data['customers'][data['customers']['CustomerID'] == cust_id]
    
    if customer.empty:
        print(f"{Colors.RED}Customer not found{Colors.END}")
        return
    
    cust = customer.iloc[0]
    
    # Get all accounts
    accounts = data['accounts'][data['accounts']['CustomerID'] == cust_id]
    total_balance = accounts['Balance'].sum() if not accounts.empty else 0
    
    # Get all loans
    loans = data['loans'][data['loans']['CustomerID'] == cust_id]
    total_loans = loans['OutstandingAmount'].sum() if not loans.empty else 0
    
    # Get all cards
    cards = data['cards'][data['cards']['CustomerID'] == cust_id]
    
    # Get transactions count
    account_nums = accounts['AccountNumber'].tolist() if not accounts.empty else []
    trans = data['transactions'][data['transactions']['AccountNumber'].isin(account_nums)]
    
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}")
    print(f"{'FINANCIAL DASHBOARD':^60}")
    print(f"{'='*60}{Colors.END}\n")
    
    print(f"Customer Name: {cust['Name']}")
    print(f"Customer ID: {cust_id}")
    print(f"Email: {cust['Email']}")
    print(f"Phone: {cust['Phone']}")
    
    print(f"\n{Colors.CYAN}Portfolio Overview:{Colors.END}")
    print(f"  Total Accounts: {len(accounts)}")
    print(f"  Total Balance: ₹{total_balance:,.2f}")
    print(f"  Total Loans: {len(loans)}")
    print(f"  Total Outstanding: ₹{total_loans:,.2f}")
    print(f"  Cards Issued: {len(cards)}")
    print(f"  Total Transactions: {len(trans)}")
    
    net_worth = total_balance - total_loans
    print(f"\n{Colors.CYAN}Net Worth:{Colors.END}")
    print(f"  Assets (Balance): ₹{total_balance:,.2f}")
    print(f"  Liabilities (Loans): ₹{total_loans:,.2f}")
    print(f"  Net Position: ₹{net_worth:,.2f}")
    
    if total_loans > 0:
        loan_ratio = (total_loans / (total_balance + total_loans)) * 100
        print(f"  Debt-to-Assets Ratio: {loan_ratio:.2f}%")
    
    # Account breakdown
    if not accounts.empty:
        print(f"\n{Colors.CYAN}Account Breakdown:{Colors.END}")
        for idx, acc in accounts.iterrows():
            status_color = Colors.GREEN if acc['Status'] == 'Active' else Colors.RED
            print(f"  {status_color}{acc['AccountNumber']:10} {acc['AccountType']:10} ₹{acc['Balance']:>12,.2f} {acc['Status']}{Colors.END}")
    
    # Credit score
    credit_score = calculate_credit_score(total_balance, len(loans), len(trans))
    print(f"\n{Colors.CYAN}Credit Score: {Colors.BOLD}{credit_score}{Colors.END}")
    if credit_score >= 750:
        rating = "Excellent"
    elif credit_score >= 650:
        rating = "Good"
    elif credit_score >= 550:
        rating = "Fair"
    else:
        rating = "Poor"
    print(f"Rating: {rating}")

def compare_loan_offers(data):
    """Compare different loan types and EMI"""
    print(f"\n{Colors.CYAN}--- Loan Comparison Tool ---{Colors.END}")
    
    amount = float(input("Loan Amount (₹): ").strip())
    tenure = int(input("Tenure (months): ").strip())
    
    print(f"\n{Colors.BOLD}{Colors.BLUE}Loan Comparison:{Colors.END}")
    print(f"Amount: ₹{amount:,.2f}")
    print(f"Tenure: {tenure} months ({tenure/12:.1f} years)\n")
    
    loan_types = {
        'Home Loan': 8.5,
        'Personal Loan': 12.0,
        'Car Loan': 9.5,
        'Education Loan': 7.5,
        'Business Loan': 11.0
    }
    
    print(f"{'Loan Type':<20} {'Interest':<12} {'Monthly EMI':<15} {'Total Amount':<15} {'Total Interest':<15}")
    print(f"{'-'*77}")
    
    for loan_type, rate in loan_types.items():
        emi = calculate_emi(amount, rate, tenure)
        total = emi * tenure
        interest = total - amount
        print(f"{loan_type:<20} {rate:>6.2f}% {emi:>14,.2f} {total:>14,.2f} {interest:>14,.2f}")

# ==========================================
# SECTION 9B: MENUS & MAIN LOOP
# ==========================================

def main():
    initialize_data()
    data = load_data()
    
    print(f"\n{Colors.BOLD}{Colors.GREEN}")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║  Welcome to CoreBank System v4.0 - Ultimate Edition      ║")
    print("║  A Comprehensive Banking Management Solution             ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}")
    
    while True:
        dashboard(data)
        print(f"\n{Colors.YELLOW}═══ MAIN MENU ═══{Colors.END}")
        print(f"\n{Colors.CYAN}Customer & Account:{Colors.END}")
        print("  1.  Add Customer")
        print("  2.  View Customers")
        print("  3.  Open Account")
        print("  4.  Check Balance")
        print(f"\n{Colors.CYAN}Transactions:{Colors.END}")
        print("  5.  Deposit Money")
        print("  6.  Withdraw Money")
        print("  7.  Fund Transfer")
        print(f"\n{Colors.CYAN}Loan Management:{Colors.END}")
        print("  8.  Loan Menu")
        print(f"\n{Colors.CYAN}Card & Cheque:{Colors.END}")
        print("  9.  Card Management")
        print("  10. Cheque Processing")
        print(f"\n{Colors.CYAN}Advanced Features:{Colors.END}")
        print("  11. Account Statement")
        print("  12. Interest Calculator")
        print("  13. Financial Dashboard")
        print("  14. Compare Loan Offers")
        print(f"\n{Colors.CYAN}Reports & Utilities:{Colors.END}")
        print("  15. Reports & Analytics")
        print("  16. Backup Data")
        print("  17. Search Customer")
        print(f"\n  18. Exit")
        
        choice = input(f"\n{Colors.BOLD}Select Option: {Colors.END}").strip()
        
        if choice == '1': data = add_customer(data)
        elif choice == '2': view_customers(data)
        elif choice == '3': data = open_account(data)
        elif choice == '4': check_balance(data)
        elif choice == '5': data = deposit_money(data)
        elif choice == '6': data = withdraw_money(data)
        elif choice == '7': data = transfer_funds(data)
        elif choice == '8': data = loan_management_menu(data)
        elif choice == '9': data = card_management_menu(data)
        elif choice == '10': data = cheque_management_menu(data)
        elif choice == '11': generate_account_statement(data)
        elif choice == '12': calculate_account_interest(data)
        elif choice == '13': view_customer_financial_dashboard(data)
        elif choice == '14': compare_loan_offers(data)
        elif choice == '15': generate_reports(data)
        elif choice == '16': backup_data()
        elif choice == '17': search_customer(data)
        elif choice == '18': 
            save_data(data)
            print(f"\n{Colors.GREEN}Thank you for using CoreBank. Goodbye!{Colors.END}")
            break
        else:
            print(f"{Colors.RED}Invalid option. Please try again.{Colors.END}")
            
        save_data(data)

if __name__ == "__main__":
    main()
