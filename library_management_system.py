import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import shutil
from datetime import datetime, timedelta

# --- Configuration ---
BOOKS_FILE = 'books.csv'
MEMBERS_FILE = 'members.csv'
TRANSACTIONS_FILE = 'transactions.csv'
FINE_PER_DAY = 20.0

# --- Initialization ---
def initialize_files():
    """Creates CSV files if they don't exist."""
    if not os.path.exists(BOOKS_FILE):
        df = pd.DataFrame(columns=['BookID', 'Title', 'Author', 'Publisher', 'ISBN', 'Category', 'Quantity', 'Available'])
        df.to_csv(BOOKS_FILE, index=False)
    
    if not os.path.exists(MEMBERS_FILE):
        df = pd.DataFrame(columns=['MemberID', 'Name', 'Class', 'Contact', 'Email', 'JoinDate'])
        df.to_csv(MEMBERS_FILE, index=False)
        
    if not os.path.exists(TRANSACTIONS_FILE):
        df = pd.DataFrame(columns=['TransactionID', 'BookID', 'MemberID', 'IssueDate', 'DueDate', 'ReturnDate', 'Fine'])
        df.to_csv(TRANSACTIONS_FILE, index=False)

def load_data():
    """Loads dataframes from CSV files."""
    books_df = pd.read_csv(BOOKS_FILE)
    members_df = pd.read_csv(MEMBERS_FILE)
    transactions_df = pd.read_csv(TRANSACTIONS_FILE)
    return books_df, members_df, transactions_df

def save_data(books_df, members_df, transactions_df):
    """Saves dataframes to CSV files."""
    books_df.to_csv(BOOKS_FILE, index=False)
    members_df.to_csv(MEMBERS_FILE, index=False)
    transactions_df.to_csv(TRANSACTIONS_FILE, index=False)

def backup_data():
    """Creates a timestamped backup of data files."""
    print("\n--- Backup Data ---")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = "backups"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    try:
        shutil.copy2(BOOKS_FILE, os.path.join(backup_dir, f"books_{timestamp}.csv"))
        shutil.copy2(MEMBERS_FILE, os.path.join(backup_dir, f"members_{timestamp}.csv"))
        shutil.copy2(TRANSACTIONS_FILE, os.path.join(backup_dir, f"transactions_{timestamp}.csv"))
        print(f"Backup created successfully in '{backup_dir}' folder!")
    except Exception as e:
        print(f"Backup failed: {e}")

# --- Book Management ---
def add_book(books_df):
    print("\n--- Add New Book ---")
    try:
        book_id = input("Enter Book ID: ")
        if book_id in books_df['BookID'].astype(str).values:
            print("Error: Book ID already exists!")
            return books_df
            
        title = input("Enter Title: ")
        author = input("Enter Author: ")
        publisher = input("Enter Publisher: ")
        isbn = input("Enter ISBN: ")
        category = input("Enter Category: ")
        qty = int(input("Enter Quantity: "))
        
        new_book = {
            'BookID': book_id, 'Title': title, 'Author': author, 
            'Publisher': publisher, 'ISBN': isbn, 'Category': category,
            'Quantity': qty, 'Available': qty
        }
        books_df = pd.concat([books_df, pd.DataFrame([new_book])], ignore_index=True)
        print("Book added successfully!")
        return books_df
    except ValueError:
        print("Invalid input! Quantity must be a number.")
        return books_df

def view_books(books_df):
    print("\n--- All Books ---")
    if books_df.empty:
        print("No books available.")
    else:
        print(books_df.to_string(index=False))

def search_book(books_df):
    print("\n--- Search Book ---")
    query = input("Enter Title, Author, ISBN or Category to search: ").lower()
    results = books_df[books_df['Title'].str.lower().str.contains(query) | 
                       books_df['Author'].str.lower().str.contains(query) |
                       books_df['ISBN'].astype(str).str.contains(query) |
                       books_df['Category'].str.lower().str.contains(query)]
    if results.empty:
        print("No books found.")
    else:
        print(results.to_string(index=False))

def update_book(books_df):
    print("\n--- Update Book Details ---")
    book_id = input("Enter Book ID to update: ")
    if book_id not in books_df['BookID'].astype(str).values:
        print("Book ID not found.")
        return books_df
    
    idx = books_df.index[books_df['BookID'].astype(str) == book_id][0]
    print("Leave blank to keep current value.")
    
    title = input(f"Enter Title ({books_df.at[idx, 'Title']}): ")
    if title: books_df.at[idx, 'Title'] = title
    
    author = input(f"Enter Author ({books_df.at[idx, 'Author']}): ")
    if author: books_df.at[idx, 'Author'] = author
    
    publisher = input(f"Enter Publisher ({books_df.at[idx, 'Publisher']}): ")
    if publisher: books_df.at[idx, 'Publisher'] = publisher
    
    isbn = input(f"Enter ISBN ({books_df.at[idx, 'ISBN']}): ")
    if isbn: books_df.at[idx, 'ISBN'] = isbn
    
    category = input(f"Enter Category ({books_df.at[idx, 'Category']}): ")
    if category: books_df.at[idx, 'Category'] = category
    
    qty_str = input(f"Enter Quantity ({books_df.at[idx, 'Quantity']}): ")
    if qty_str:
        try:
            new_qty = int(qty_str)
            diff = new_qty - books_df.at[idx, 'Quantity']
            books_df.at[idx, 'Quantity'] = new_qty
            books_df.at[idx, 'Available'] += diff
        except ValueError:
            print("Invalid quantity. Skipping quantity update.")

    print("Book details updated successfully!")
    return books_df

def delete_book(books_df):
    print("\n--- Delete Book ---")
    book_id = input("Enter Book ID to delete: ")
    if book_id in books_df['BookID'].astype(str).values:
        books_df = books_df[books_df['BookID'].astype(str) != book_id]
        print("Book deleted successfully!")
    else:
        print("Book ID not found.")
    return books_df

# --- Member Management ---
def add_member(members_df):
    print("\n--- Add New Member ---")
    try:
        member_id = input("Enter Member ID: ")
        if member_id in members_df['MemberID'].astype(str).values:
            print("Error: Member ID already exists!")
            return members_df
            
        name = input("Enter Name: ")
        class_sec = input("Enter Class & Section: ")
        contact = input("Enter Contact No: ")
        email = input("Enter Email: ")
        join_date = datetime.now().strftime("%Y-%m-%d")
        
        new_member = {
            'MemberID': member_id, 'Name': name, 'Class': class_sec,
            'Contact': contact, 'Email': email, 'JoinDate': join_date
        }
        members_df = pd.concat([members_df, pd.DataFrame([new_member])], ignore_index=True)
        print("Member added successfully!")
        return members_df
    except Exception as e:
        print(f"Error adding member: {e}")
        return members_df

def view_members(members_df):
    print("\n--- All Members ---")
    if members_df.empty:
        print("No members found.")
    else:
        print(members_df.to_string(index=False))

def search_member(members_df):
    print("\n--- Search Member ---")
    query = input("Enter Name or Member ID to search: ").lower()
    results = members_df[members_df['Name'].str.lower().str.contains(query) | 
                         members_df['MemberID'].astype(str).str.contains(query)]
    if results.empty:
        print("No members found.")
    else:
        print(results.to_string(index=False))

def update_member(members_df):
    print("\n--- Update Member Details ---")
    member_id = input("Enter Member ID to update: ")
    if member_id not in members_df['MemberID'].astype(str).values:
        print("Member ID not found.")
        return members_df
    
    idx = members_df.index[members_df['MemberID'].astype(str) == member_id][0]
    print("Leave blank to keep current value.")
    
    name = input(f"Enter Name ({members_df.at[idx, 'Name']}): ")
    if name: members_df.at[idx, 'Name'] = name
    
    class_sec = input(f"Enter Class ({members_df.at[idx, 'Class']}): ")
    if class_sec: members_df.at[idx, 'Class'] = class_sec
    
    contact = input(f"Enter Contact ({members_df.at[idx, 'Contact']}): ")
    if contact: members_df.at[idx, 'Contact'] = contact
    
    email = input(f"Enter Email ({members_df.at[idx, 'Email']}): ")
    if email: members_df.at[idx, 'Email'] = email
    
    print("Member details updated successfully!")
    return members_df

def delete_member(members_df):
    print("\n--- Delete Member ---")
    member_id = input("Enter Member ID to delete: ")
    if member_id in members_df['MemberID'].astype(str).values:
        members_df = members_df[members_df['MemberID'].astype(str) != member_id]
        print("Member deleted successfully!")
    else:
        print("Member ID not found.")
    return members_df

# --- Issue / Return ---
def issue_book(books_df, members_df, transactions_df):
    print("\n--- Issue Book ---")
    book_id = input("Enter Book ID: ")
    member_id = input("Enter Member ID: ")
    
    # Validation
    if book_id not in books_df['BookID'].astype(str).values:
        print("Book not found!")
        return books_df, transactions_df
    if member_id not in members_df['MemberID'].astype(str).values:
        print("Member not found!")
        return books_df, transactions_df
    
    # Check availability
    book_idx = books_df.index[books_df['BookID'].astype(str) == book_id][0]
    if books_df.at[book_idx, 'Available'] <= 0:
        print("Book is not available!")
        return books_df, transactions_df
    
    # Issue
    issue_date = datetime.now().strftime("%Y-%m-%d")
    due_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d") # 7 days issue period
    trans_id = len(transactions_df) + 1
    
    new_trans = {
        'TransactionID': trans_id, 'BookID': book_id, 'MemberID': member_id,
        'IssueDate': issue_date, 'DueDate': due_date, 'ReturnDate': np.nan, 'Fine': 0.0
    }
    
    transactions_df = pd.concat([transactions_df, pd.DataFrame([new_trans])], ignore_index=True)
    books_df.at[book_idx, 'Available'] -= 1
    
    print(f"Book issued successfully! Due Date: {due_date}")
    return books_df, transactions_df

def return_book(books_df, transactions_df):
    print("\n--- Return Book ---")
    book_id = input("Enter Book ID: ")
    member_id = input("Enter Member ID: ")
    
    # Find active transaction
    mask = (transactions_df['BookID'].astype(str) == book_id) & \
           (transactions_df['MemberID'].astype(str) == member_id) & \
           (transactions_df['ReturnDate'].isna())
           
    if not mask.any():
        print("No active issue record found for this Book and Member.")
        return books_df, transactions_df
    
    trans_idx = transactions_df[mask].index[0]
    
    return_date = datetime.now()
    due_date = datetime.strptime(transactions_df.at[trans_idx, 'DueDate'], "%Y-%m-%d")
    
    # Calculate Fine
    fine = 0.0
    if return_date > due_date:
        overdue_days = (return_date - due_date).days
        fine = overdue_days * FINE_PER_DAY
        print(f"Book is overdue by {overdue_days} days. Fine: ₹{fine}")
    else:
        print("Returned on time. No fine.")
        
    # Update Transaction
    transactions_df.at[trans_idx, 'ReturnDate'] = return_date.strftime("%Y-%m-%d")
    transactions_df.at[trans_idx, 'Fine'] = fine
    
    # Update Book Availability
    if book_id in books_df['BookID'].astype(str).values:
        book_idx = books_df.index[books_df['BookID'].astype(str) == book_id][0]
        books_df.at[book_idx, 'Available'] += 1
        
    print("Book returned successfully!")
    return books_df, transactions_df

def view_issued_books(transactions_df, books_df, members_df):
    print("\n--- Currently Issued Books ---")
    issued = transactions_df[transactions_df['ReturnDate'].isna()]
    if issued.empty:
        print("No books are currently issued.")
        return

    # Merge with books and members to show names instead of IDs
    merged = issued.merge(books_df[['BookID', 'Title']], on='BookID', how='left')
    merged = merged.merge(members_df[['MemberID', 'Name']], on='MemberID', how='left')
    
    display_df = merged[['TransactionID', 'BookID', 'Title', 'MemberID', 'Name', 'IssueDate', 'DueDate']]
    print(display_df.to_string(index=False))

def check_availability(books_df):
    print("\n--- Check Book Availability ---")
    query = input("Enter Book Title or ID: ").lower()
    results = books_df[books_df['Title'].str.lower().str.contains(query) | 
                       books_df['BookID'].astype(str).str.contains(query)]
    
    if results.empty:
        print("No books found.")
    else:
        print(results[['BookID', 'Title', 'Author', 'Available', 'Quantity']].to_string(index=False))

# --- Analytics ---
def check_overdue_books(transactions_df, books_df, members_df):
    print("\n--- Overdue Books Report ---")
    today = datetime.now().strftime("%Y-%m-%d")
    overdue = transactions_df[(transactions_df['ReturnDate'].isna()) & (transactions_df['DueDate'] < today)]
    
    if overdue.empty:
        print("No overdue books.")
        return

    merged = overdue.merge(books_df[['BookID', 'Title']], on='BookID', how='left')
    merged = merged.merge(members_df[['MemberID', 'Name', 'Contact']], on='MemberID', how='left')
    
    print(merged[['BookID', 'Title', 'MemberID', 'Name', 'Contact', 'DueDate']].to_string(index=False))

def member_history(transactions_df, books_df):
    print("\n--- Member Issue History ---")
    member_id = input("Enter Member ID: ")
    history = transactions_df[transactions_df['MemberID'].astype(str) == member_id]
    
    if history.empty:
        print("No history found for this member.")
        return
        
    merged = history.merge(books_df[['BookID', 'Title']], on='BookID', how='left')
    print(merged[['TransactionID', 'Title', 'IssueDate', 'ReturnDate', 'Fine']].to_string(index=False))

def monthly_stats(transactions_df):
    print("\n--- Monthly Statistics ---")
    if transactions_df.empty:
        print("No transactions found.")
        return
        
    transactions_df['IssueDate'] = pd.to_datetime(transactions_df['IssueDate'])
    transactions_df['Month'] = transactions_df['IssueDate'].dt.to_period('M')
    
    stats = transactions_df.groupby('Month').size()
    print(stats)
    
    plt.figure(figsize=(10, 6))
    stats.plot(kind='bar', color='orange')
    plt.title('Monthly Transaction Volume')
    plt.xlabel('Month')
    plt.ylabel('Number of Issues')
    plt.tight_layout()
    plt.show()

def show_analytics(books_df, transactions_df, members_df):
    print("\n--- Analytics Menu ---")
    print("1. Most Issued Books")
    print("2. Books Category Distribution")
    print("3. Overdue Books Report")
    print("4. Member Issue History")
    print("5. Monthly Statistics")
    print("6. Back to Main Menu")
    
    choice = input("Enter choice: ")
    
    if choice == '1':
        if transactions_df.empty:
            print("No transactions data available.")
            return
        
        top_books = transactions_df['BookID'].value_counts().head(5)
        titles = []
        for bid in top_books.index:
            title = books_df[books_df['BookID'].astype(str) == str(bid)]['Title'].values
            titles.append(title[0] if len(title) > 0 else str(bid))
            
        plt.figure(figsize=(10, 6))
        plt.bar(titles, top_books.values, color='skyblue')
        plt.title('Top 5 Most Issued Books')
        plt.xlabel('Book Title')
        plt.ylabel('Number of Issues')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
        
    elif choice == '2':
        if books_df.empty:
            print("No books data available.")
            return
            
        cat_counts = books_df['Category'].value_counts()
        plt.figure(figsize=(8, 8))
        plt.pie(cat_counts.values, labels=cat_counts.index, autopct='%1.1f%%', startangle=140)
        plt.title('Books Distribution by Category')
        plt.show()
        
    elif choice == '3':
        check_overdue_books(transactions_df, books_df, members_df)
        
    elif choice == '4':
        member_history(transactions_df, books_df)
        
    elif choice == '5':
        monthly_stats(transactions_df)

# --- Main Menu ---
def main_menu():
    initialize_files()
    books_df, members_df, transactions_df = load_data()
    
    while True:
        print("\n=================================")
        print(" SCHOOL LIBRARY MANAGEMENT SYSTEM")
        print("=================================")
        print("1. Book Management")
        print("2. Member Management")
        print("3. Issue/Return Book")
        print("4. Reports & Analytics")
        print("5. Backup Data")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ")
        
        if choice == '1':
            while True:
                print("\n--- Book Management ---")
                print("1. Add Book")
                print("2. View All Books")
                print("3. Search Book")
                print("4. Update Book Details")
                print("5. Delete Book")
                print("6. Back")
                b_choice = input("Enter choice: ")
                if b_choice == '1': books_df = add_book(books_df)
                elif b_choice == '2': view_books(books_df)
                elif b_choice == '3': search_book(books_df)
                elif b_choice == '4': books_df = update_book(books_df)
                elif b_choice == '5': books_df = delete_book(books_df)
                elif b_choice == '6': break
                else: print("Invalid choice")
                save_data(books_df, members_df, transactions_df)

        elif choice == '2':
            while True:
                print("\n--- Member Management ---")
                print("1. Add Member")
                print("2. View All Members")
                print("3. Search Member")
                print("4. Update Member Details")
                print("5. Delete Member")
                print("6. Back")
                m_choice = input("Enter choice: ")
                if m_choice == '1': members_df = add_member(members_df)
                elif m_choice == '2': view_members(members_df)
                elif m_choice == '3': search_member(members_df)
                elif m_choice == '4': members_df = update_member(members_df)
                elif m_choice == '5': members_df = delete_member(members_df)
                elif m_choice == '6': break
                else: print("Invalid choice")
                save_data(books_df, members_df, transactions_df)

        elif choice == '3':
            while True:
                print("\n--- Issue / Return ---")
                print("1. Issue Book")
                print("2. Return Book")
                print("3. View Issued Books")
                print("4. Check Availability")
                print("5. Back")
                i_choice = input("Enter choice: ")
                if i_choice == '1':
                    books_df, transactions_df = issue_book(books_df, members_df, transactions_df)
                elif i_choice == '2':
                    books_df, transactions_df = return_book(books_df, transactions_df)
                elif i_choice == '3':
                    view_issued_books(transactions_df, books_df, members_df)
                elif i_choice == '4':
                    check_availability(books_df)
                elif i_choice == '5': break
                else: print("Invalid choice")
                save_data(books_df, members_df, transactions_df)
            
        elif choice == '4':
            show_analytics(books_df, transactions_df, members_df)
            
        elif choice == '5':
            backup_data()
            
        elif choice == '6':
            print("Thank you for using Library Management System!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main_menu()
