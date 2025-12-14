"""
Sample Data Population Script for CoreBank v4.0
This script populates the database with realistic sample data
to showcase all features and functions.
"""

import json
import pandas as pd
from datetime import datetime, timedelta
import random

# Database file
DB_FILE = 'bank_database.csv'

def get_date():
    """Get current date in YYYY-MM-DD format"""
    return datetime.now().strftime('%Y-%m-%d')

def get_datetime():
    """Get current datetime"""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# ==========================================
# SAMPLE DATA SETS
# ==========================================

SAMPLE_CUSTOMERS = [
    {
        'CustomerID': 'CUST001',
        'Name': 'Raghav Agarwal',
        'DOB': '2005-08-15',
        'Gender': 'Male',
        'PAN': 'ABCDE1234F',
        'Aadhar': '123456789012',
        'Address': '123 Maple Street, Downtown',
        'City': 'Delhi',
        'State': 'Delhi',
        'PIN': '110001',
        'Phone': '9876543210',
        'Email': 'raghav.agarwal@email.com',
        'RegistrationDate': '2025-01-15',
        'Status': 'Active',
        'KYCStatus': 'Verified'
    },
    {
        'CustomerID': 'CUST002',
        'Name': 'Priya Sharma',
        'DOB': '2004-03-22',
        'Gender': 'Female',
        'PAN': 'PQRST5678G',
        'Aadhar': '234567890123',
        'Address': '456 Oak Avenue, Westside',
        'City': 'Mumbai',
        'State': 'Maharashtra',
        'PIN': '400001',
        'Phone': '8765432109',
        'Email': 'priya.sharma@email.com',
        'RegistrationDate': '2025-02-10',
        'Status': 'Active',
        'KYCStatus': 'Verified'
    },
    {
        'CustomerID': 'CUST003',
        'Name': 'Amit Kumar',
        'DOB': '2006-05-30',
        'Gender': 'Male',
        'PAN': 'UVWXY9012H',
        'Aadhar': '345678901234',
        'Address': '789 Pine Road, Eastside',
        'City': 'Bangalore',
        'State': 'Karnataka',
        'PIN': '560001',
        'Phone': '7654321098',
        'Email': 'amit.kumar@email.com',
        'RegistrationDate': '2025-03-05',
        'Status': 'Active',
        'KYCStatus': 'Verified'
    },
    {
        'CustomerID': 'CUST004',
        'Name': 'Neha Patel',
        'DOB': '2005-07-12',
        'Gender': 'Female',
        'PAN': 'ABCXY3456I',
        'Aadhar': '456789012345',
        'Address': '321 Elm Court, Northside',
        'City': 'Hyderabad',
        'State': 'Telangana',
        'PIN': '500001',
        'Phone': '6543210987',
        'Email': 'neha.patel@email.com',
        'RegistrationDate': '2025-03-20',
        'Status': 'Active',
        'KYCStatus': 'Verified'
    },
    {
        'CustomerID': 'CUST005',
        'Name': 'Vikram Singh',
        'DOB': '2004-11-08',
        'Gender': 'Male',
        'PAN': 'DEFGH7890J',
        'Aadhar': '567890123456',
        'Address': '654 Birch Lane, Southside',
        'City': 'Pune',
        'State': 'Maharashtra',
        'PIN': '411001',
        'Phone': '5432109876',
        'Email': 'vikram.singh@email.com',
        'RegistrationDate': '2025-04-10',
        'Status': 'Active',
        'KYCStatus': 'Verified'
    },
    {
        'CustomerID': 'CUST006',
        'Name': 'Anjali Verma',
        'DOB': '2005-02-14',
        'Gender': 'Female',
        'PAN': 'IJKLM1234K',
        'Aadhar': '678901234567',
        'Address': '987 Cedar Street, Central',
        'City': 'Ahmedabad',
        'State': 'Gujarat',
        'PIN': '380001',
        'Phone': '4321098765',
        'Email': 'anjali.verma@email.com',
        'RegistrationDate': '2025-05-08',
        'Status': 'Active',
        'KYCStatus': 'Verified'
    },
    {
        'CustomerID': 'CUST007',
        'Name': 'Rohan Desai',
        'DOB': '2006-09-19',
        'Gender': 'Male',
        'PAN': 'NOPQR5678L',
        'Aadhar': '789012345678',
        'Address': '147 Walnut Avenue, Midtown',
        'City': 'Surat',
        'State': 'Gujarat',
        'PIN': '395001',
        'Phone': '3210987654',
        'Email': 'rohan.desai@email.com',
        'RegistrationDate': '2025-06-15',
        'Status': 'Active',
        'KYCStatus': 'Verified'
    },
    {
        'CustomerID': 'CUST008',
        'Name': 'Isha Gupta',
        'DOB': '2005-12-03',
        'Gender': 'Female',
        'PAN': 'STUVW9012M',
        'Aadhar': '890123456789',
        'Address': '258 Chestnut Road, Uptown',
        'City': 'Jaipur',
        'State': 'Rajasthan',
        'PIN': '302001',
        'Phone': '2109876543',
        'Email': 'isha.gupta@email.com',
        'RegistrationDate': '2025-07-20',
        'Status': 'Active',
        'KYCStatus': 'Verified'
    },
    {
        'CustomerID': 'CUST009',
        'Name': 'Arjun Nair',
        'DOB': '2004-06-27',
        'Gender': 'Male',
        'PAN': 'XYZAB3456N',
        'Aadhar': '901234567890',
        'Address': '369 Hickory Lane, Downtown',
        'City': 'Kochi',
        'State': 'Kerala',
        'PIN': '682001',
        'Phone': '1098765432',
        'Email': 'arjun.nair@email.com',
        'RegistrationDate': '2025-08-05',
        'Status': 'Active',
        'KYCStatus': 'Verified'
    },
    {
        'CustomerID': 'CUST010',
        'Name': 'Divya Iyer',
        'DOB': '2005-04-11',
        'Gender': 'Female',
        'PAN': 'CDEFG7890O',
        'Aadhar': '012345678901',
        'Address': '456 Ash Street, Riverside',
        'City': 'Chennai',
        'State': 'Tamil Nadu',
        'PIN': '600001',
        'Phone': '9988776655',
        'Email': 'divya.iyer@email.com',
        'RegistrationDate': '2025-09-12',
        'Status': 'Active',
        'KYCStatus': 'Verified'
    }
]

SAMPLE_ACCOUNTS = [
    {'AccountNumber': 'ACC1001', 'CustomerID': 'CUST001', 'AccountType': 'Savings', 'Balance': 250000.00, 'InterestRate': 4.0, 'MinBalance': 1000.0, 'RegistrationDate': '2025-01-20', 'Status': 'Active'},
    {'AccountNumber': 'ACC1002', 'CustomerID': 'CUST001', 'AccountType': 'Current', 'Balance': 150000.00, 'InterestRate': 0.0, 'MinBalance': 10000.0, 'RegistrationDate': '2025-02-15', 'Status': 'Active'},
    {'AccountNumber': 'ACC2001', 'CustomerID': 'CUST002', 'AccountType': 'Savings', 'Balance': 320000.00, 'InterestRate': 4.0, 'MinBalance': 1000.0, 'RegistrationDate': '2025-02-20', 'Status': 'Active'},
    {'AccountNumber': 'ACC3001', 'CustomerID': 'CUST003', 'AccountType': 'Savings', 'Balance': 180000.00, 'InterestRate': 4.0, 'MinBalance': 1000.0, 'RegistrationDate': '2025-03-10', 'Status': 'Active'},
    {'AccountNumber': 'ACC4001', 'CustomerID': 'CUST004', 'AccountType': 'Current', 'Balance': 500000.00, 'InterestRate': 0.0, 'MinBalance': 10000.0, 'RegistrationDate': '2025-03-25', 'Status': 'Active'},
    {'AccountNumber': 'ACC5001', 'CustomerID': 'CUST005', 'AccountType': 'Savings', 'Balance': 450000.00, 'InterestRate': 4.0, 'MinBalance': 1000.0, 'RegistrationDate': '2025-04-15', 'Status': 'Active'},
    {'AccountNumber': 'ACC6001', 'CustomerID': 'CUST006', 'AccountType': 'Savings', 'Balance': 280000.00, 'InterestRate': 4.0, 'MinBalance': 1000.0, 'RegistrationDate': '2025-05-10', 'Status': 'Active'},
    {'AccountNumber': 'ACC7001', 'CustomerID': 'CUST007', 'AccountType': 'Current', 'Balance': 620000.00, 'InterestRate': 0.0, 'MinBalance': 10000.0, 'RegistrationDate': '2025-06-20', 'Status': 'Active'},
    {'AccountNumber': 'ACC8001', 'CustomerID': 'CUST008', 'AccountType': 'Savings', 'Balance': 340000.00, 'InterestRate': 4.0, 'MinBalance': 1000.0, 'RegistrationDate': '2025-07-25', 'Status': 'Active'},
    {'AccountNumber': 'ACC9001', 'CustomerID': 'CUST009', 'AccountType': 'Savings', 'Balance': 200000.00, 'InterestRate': 4.0, 'MinBalance': 1000.0, 'RegistrationDate': '2025-08-10', 'Status': 'Active'},
    {'AccountNumber': 'ACC10001', 'CustomerID': 'CUST010', 'AccountType': 'Current', 'Balance': 750000.00, 'InterestRate': 0.0, 'MinBalance': 10000.0, 'RegistrationDate': '2025-09-15', 'Status': 'Active'}
]

def generate_transactions():
    """Generate sample transactions"""
    transactions = []
    accounts = ['ACC1001', 'ACC1002', 'ACC2001', 'ACC3001', 'ACC4001', 'ACC5001', 'ACC6001', 'ACC7001', 'ACC8001', 'ACC9001', 'ACC10001']
    
    trans_id = 1
    for acc in accounts:
        # Generate 5-8 transactions per account
        for i in range(random.randint(5, 8)):
            date = (datetime.now() - timedelta(days=random.randint(1, 90))).strftime('%Y-%m-%d')
            trans_type = random.choice(['Deposit', 'Withdrawal'])
            amount = random.choice([10000, 15000, 20000, 25000, 30000, 5000, 8000])
            balance_after = random.randint(100000, 800000)
            
            transactions.append({
                'TransactionID': f'TXN{str(trans_id).zfill(5)}',
                'AccountNumber': acc,
                'TransactionType': trans_type,
                'Amount': amount,
                'Date': date,
                'BalanceAfter': balance_after,
                'Description': f'{trans_type} - {amount}'
            })
            trans_id += 1
    
    return transactions

def generate_loans():
    """Generate sample loans"""
    loans = [
        {'LoanID': 'LOAN001', 'CustomerID': 'CUST001', 'LoanType': 'Personal Loan', 'PrincipalAmount': 500000.0, 'InterestRate': 12.0, 'EMI': 8886.0, 'Tenure': 60, 'OutstandingAmount': 350000.0, 'Status': 'Active', 'DisbursementDate': '2025-03-10'},
        {'LoanID': 'LOAN002', 'CustomerID': 'CUST002', 'LoanType': 'Home Loan', 'PrincipalAmount': 2500000.0, 'InterestRate': 8.5, 'EMI': 25000.0, 'Tenure': 180, 'OutstandingAmount': 2300000.0, 'Status': 'Active', 'DisbursementDate': '2025-02-15'},
        {'LoanID': 'LOAN003', 'CustomerID': 'CUST003', 'LoanType': 'Car Loan', 'PrincipalAmount': 800000.0, 'InterestRate': 9.5, 'EMI': 12500.0, 'Tenure': 72, 'OutstandingAmount': 600000.0, 'Status': 'Active', 'DisbursementDate': '2025-04-20'},
        {'LoanID': 'LOAN004', 'CustomerID': 'CUST005', 'LoanType': 'Education Loan', 'PrincipalAmount': 1000000.0, 'InterestRate': 7.5, 'EMI': 14500.0, 'Tenure': 84, 'OutstandingAmount': 850000.0, 'Status': 'Active', 'DisbursementDate': '2025-05-10'},
        {'LoanID': 'LOAN005', 'CustomerID': 'CUST007', 'LoanType': 'Business Loan', 'PrincipalAmount': 3000000.0, 'InterestRate': 11.0, 'EMI': 45000.0, 'Tenure': 84, 'OutstandingAmount': 2500000.0, 'Status': 'Active', 'DisbursementDate': '2025-06-05'},
        {'LoanID': 'LOAN006', 'CustomerID': 'CUST004', 'LoanType': 'Personal Loan', 'PrincipalAmount': 300000.0, 'InterestRate': 12.0, 'EMI': 5330.0, 'Tenure': 60, 'OutstandingAmount': 100000.0, 'Status': 'Active', 'DisbursementDate': '2025-07-15'},
    ]
    return loans

def generate_loan_payments():
    """Generate sample loan payments"""
    payments = []
    pay_id = 1
    
    loans = [
        {'LoanID': 'LOAN001', 'EMI': 8886.0, 'Payments': 15},
        {'LoanID': 'LOAN002', 'EMI': 25000.0, 'Payments': 20},
        {'LoanID': 'LOAN003', 'EMI': 12500.0, 'Payments': 10},
        {'LoanID': 'LOAN004', 'EMI': 14500.0, 'Payments': 8},
        {'LoanID': 'LOAN005', 'EMI': 45000.0, 'Payments': 12},
        {'LoanID': 'LOAN006', 'EMI': 5330.0, 'Payments': 25},
    ]
    
    for loan in loans:
        for i in range(loan['Payments']):
            date = (datetime.now() - timedelta(days=30 * i)).strftime('%Y-%m-%d')
            payments.append({
                'PaymentID': f'PAY{str(pay_id).zfill(5)}',
                'LoanID': loan['LoanID'],
                'Amount': loan['EMI'],
                'Date': date,
                'Status': 'Success'
            })
            pay_id += 1
    
    return payments

def generate_cards():
    """Generate sample cards"""
    cards = []
    card_id = 1
    
    customers = ['CUST001', 'CUST002', 'CUST003', 'CUST004', 'CUST005', 'CUST006', 'CUST007', 'CUST008']
    accounts = ['ACC1001', 'ACC2001', 'ACC3001', 'ACC4001', 'ACC5001', 'ACC6001', 'ACC7001', 'ACC8001']
    card_types = ['Debit', 'Credit', 'Premium Credit']
    
    for i, customer in enumerate(customers):
        card_type = random.choice(card_types)
        card_num = f"{random.randint(1000, 9999)}{random.randint(1000, 9999)}{random.randint(1000, 9999)}{random.randint(1000, 9999)}"
        cvv = f"{random.randint(100, 999)}"
        expiry_date = (datetime.now() + timedelta(days=365*5)).strftime('%Y-%m-%d')
        
        cards.append({
            'CardID': f'CARD{str(card_id).zfill(4)}',
            'CustomerID': customer,
            'AccountNumber': accounts[i],
            'CardNumber': card_num,
            'CardType': card_type,
            'CVV': cvv,
            'ExpiryDate': expiry_date,
            'DailyLimit': 100000.0,
            'Status': random.choice(['Active', 'Active', 'Blocked']),
            'IssueDate': (datetime.now() - timedelta(days=random.randint(30, 365))).strftime('%Y-%m-%d')
        })
        card_id += 1
    
    return cards

def generate_cheques():
    """Generate sample cheques"""
    cheques = []
    cheque_id = 1
    
    accounts = ['ACC1001', 'ACC2001', 'ACC3001', 'ACC4001', 'ACC5001']
    
    for acc in accounts:
        for i in range(random.randint(2, 5)):
            cheque_num = f"{random.randint(100000, 999999)}"
            amount = random.choice([50000, 75000, 100000, 150000, 200000])
            issue_date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
            status = random.choice(['Issued', 'Cleared', 'Bounced'])
            clearance_date = (datetime.now() - timedelta(days=random.randint(1, 15))).strftime('%Y-%m-%d') if status != 'Issued' else None
            
            cheques.append({
                'ChequeNumber': cheque_num,
                'AccountNumber': acc,
                'IssuedTo': f'Payee {cheque_id}',
                'Amount': amount,
                'IssueDate': issue_date,
                'ClearanceDate': clearance_date,
                'Status': status,
                'Remarks': 'Payment for services' if status == 'Cleared' else ('Insufficient funds' if status == 'Bounced' else '')
            })
            cheque_id += 1
    
    return cheques

def generate_transfers():
    """Generate sample fund transfers"""
    transfers = []
    transfer_id = 1
    
    from_accounts = ['ACC1001', 'ACC2001', 'ACC3001', 'ACC4001', 'ACC5001']
    to_accounts = ['ACC1002', 'ACC6001', 'ACC7001', 'ACC8001', 'ACC9001']
    
    for i in range(10):
        amount = random.choice([10000, 20000, 30000, 50000])
        date = (datetime.now() - timedelta(days=random.randint(1, 60))).strftime('%Y-%m-%d')
        
        transfers.append({
            'TransferID': f'TRF{str(transfer_id).zfill(5)}',
            'FromAccount': random.choice(from_accounts),
            'ToAccount': random.choice(to_accounts),
            'Amount': amount,
            'Date': date,
            'Status': 'Success',
            'TransferCharge': 0.0
        })
        transfer_id += 1
    
    return transfers

def generate_audit_logs():
    """Generate sample audit logs"""
    audit_logs = []
    operations = [
        'CUSTOMER_ADDED', 'ACCOUNT_OPENED', 'DEPOSIT', 'WITHDRAWAL', 
        'TRANSFER_INITIATED', 'LOAN_APPLIED', 'EMI_PAID', 'CARD_ISSUED',
        'CARD_ACTIVATED', 'CARD_BLOCKED', 'CHEQUE_ISSUED', 'CHEQUE_CLEARED'
    ]
    
    for i in range(100):
        timestamp = (datetime.now() - timedelta(days=random.randint(1, 90), hours=random.randint(0, 23))).strftime('%Y-%m-%d %H:%M:%S')
        
        audit_logs.append({
            'AuditID': f'AUD{str(i+1).zfill(5)}',
            'Timestamp': timestamp,
            'Operation': random.choice(operations),
            'Details': f'Operation {i+1} executed successfully',
            'Status': 'Success'
        })
    
    return audit_logs

def populate_database():
    """Populate entire database with sample data"""
    print("Populating CoreBank database with sample data...")
    
    # Create data dictionary
    data = {
        'customers': SAMPLE_CUSTOMERS,
        'accounts': SAMPLE_ACCOUNTS,
        'transactions': generate_transactions(),
        'loans': generate_loans(),
        'loan_payments': generate_loan_payments(),
        'cards': generate_cards(),
        'cheques': generate_cheques(),
        'transfers': generate_transfers(),
        'audit': generate_audit_logs(),
        'users': [
            {'UserID': 'USR001', 'Username': 'admin', 'Password': 'admin@123', 'Role': 'Administrator'},
            {'UserID': 'USR002', 'Username': 'staff', 'Password': 'staff@123', 'Role': 'Staff'},
        ]
    }
    
    # Convert to proper format (indexed dictionary format for JSON-in-CSV)
    db_records = []
    for table_name, records in data.items():
        if isinstance(records, list) and records:
            # Convert list to indexed dictionary format
            indexed_dict = {str(i): record for i, record in enumerate(records)}
            # Add null columns at the end (for schema evolution)
            indexed_dict['Table'] = None
            indexed_dict['Data'] = None
            json_data = json.dumps(indexed_dict)
            db_records.append({'Table': table_name, 'Data': json_data})
    
    # Create and save DataFrame
    df = pd.DataFrame(db_records)
    df.to_csv(DB_FILE, index=False)
    
    print(f"✅ Database populated successfully!")
    print(f"\nSample Data Summary:")
    print(f"  Customers: {len(SAMPLE_CUSTOMERS)}")
    print(f"  Accounts: {len(SAMPLE_ACCOUNTS)}")
    print(f"  Transactions: {len(data['transactions'])}")
    print(f"  Loans: {len(data['loans'])}")
    print(f"  Loan Payments: {len(data['loan_payments'])}")
    print(f"  Cards: {len(data['cards'])}")
    print(f"  Cheques: {len(data['cheques'])}")
    print(f"  Transfers: {len(data['transfers'])}")
    print(f"  Audit Logs: {len(data['audit'])}")
    print(f"\n✅ Ready to showcase all features!")

if __name__ == "__main__":
    populate_database()
