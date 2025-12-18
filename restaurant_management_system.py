import pandas as pd
import os
import datetime
import matplotlib.pyplot as plt

# File Paths
MENU_FILE = 'menu.csv'
ORDERS_FILE = 'orders.csv'
STAFF_FILE = 'staff.csv'

class RestaurantSystem:
    def __init__(self):
        self.load_data()

    def load_data(self):
        if not os.path.exists(MENU_FILE):
            self.menu = pd.DataFrame(columns=['item_id', 'name', 'category', 'price', 'is_available'])
            self.menu.to_csv(MENU_FILE, index=False)
        else:
            self.menu = pd.read_csv(MENU_FILE)

        if not os.path.exists(ORDERS_FILE):
            self.orders = pd.DataFrame(columns=['order_id', 'table_number', 'items', 'total_amount', 'status', 'timestamp'])
            self.orders.to_csv(ORDERS_FILE, index=False)
        else:
            self.orders = pd.read_csv(ORDERS_FILE)

        if not os.path.exists(STAFF_FILE):
            self.staff = pd.DataFrame(columns=['staff_id', 'name', 'role', 'shift'])
            self.staff.to_csv(STAFF_FILE, index=False)
        else:
            self.staff = pd.read_csv(STAFF_FILE)

    def save_data(self):
        self.menu.to_csv(MENU_FILE, index=False)
        self.orders.to_csv(ORDERS_FILE, index=False)
        self.staff.to_csv(STAFF_FILE, index=False)

    # --- Menu Management ---
    def view_menu(self):
        print("\n--- Current Menu ---")
        if self.menu.empty:
            print("Menu is empty.")
        else:
            print(self.menu[self.menu['is_available'] == True].to_string(index=False))

    def add_menu_item(self):
        try:
            item_id = len(self.menu) + 1
            name = input("Enter Item Name: ")
            category = input("Enter Category (Starter/Main/Dessert/Beverage): ")
            price = float(input("Enter Price: "))
            is_available = True
            
            new_item = pd.DataFrame({'item_id': [item_id], 'name': [name], 'category': [category], 'price': [price], 'is_available': [is_available]})
            self.menu = pd.concat([self.menu, new_item], ignore_index=True)
            self.save_data()
            print("Item added successfully!")
        except ValueError:
            print("Invalid input. Please try again.")

    def delete_menu_item(self):
        self.view_menu()
        try:
            item_id = int(input("Enter Item ID to delete: "))
            if item_id in self.menu['item_id'].values:
                self.menu = self.menu[self.menu['item_id'] != item_id]
                self.save_data()
                print("Item deleted successfully!")
            else:
                print("Item ID not found.")
        except ValueError:
            print("Invalid input.")

    # --- Order Management ---
    def take_order(self):
        try:
            table_number = int(input("Enter Table Number: "))
            self.view_menu()
            items = []
            total_amount = 0
            
            while True:
                item_id = int(input("Enter Item ID to add (0 to finish): "))
                if item_id == 0:
                    break
                
                item = self.menu[self.menu['item_id'] == item_id]
                if not item.empty and item['is_available'].values[0]:
                    items.append(item['name'].values[0])
                    total_amount += item['price'].values[0]
                    print(f"Added {item['name'].values[0]}")
                else:
                    print("Invalid Item ID or Item unavailable.")
            
            if items:
                order_id = len(self.orders) + 1
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                new_order = pd.DataFrame({
                    'order_id': [order_id],
                    'table_number': [table_number],
                    'items': [", ".join(items)],
                    'total_amount': [total_amount],
                    'status': ['Pending'],
                    'timestamp': [timestamp]
                })
                self.orders = pd.concat([self.orders, new_order], ignore_index=True)
                self.save_data()
                print(f"Order placed! Order ID: {order_id}, Total: {total_amount}")
            else:
                print("No items added to order.")
        except ValueError:
            print("Invalid input.")

    def view_orders(self):
        print("\n--- Orders ---")
        if self.orders.empty:
            print("No orders found.")
        else:
            print(self.orders.to_string(index=False))

    def complete_order(self):
        self.view_orders()
        try:
            order_id = int(input("Enter Order ID to mark as completed: "))
            if order_id in self.orders['order_id'].values:
                self.orders.loc[self.orders['order_id'] == order_id, 'status'] = 'Completed'
                self.save_data()
                print("Order marked as completed!")
            else:
                print("Order ID not found.")
        except ValueError:
            print("Invalid input.")

    # --- Staff Management ---
    def view_staff(self):
        print("\n--- Staff ---")
        if self.staff.empty:
            print("No staff records.")
        else:
            print(self.staff.to_string(index=False))

    def add_staff(self):
        try:
            staff_id = len(self.staff) + 1
            name = input("Enter Staff Name: ")
            role = input("Enter Role: ")
            shift = input("Enter Shift: ")
            
            new_staff = pd.DataFrame({'staff_id': [staff_id], 'name': [name], 'role': [role], 'shift': [shift]})
            self.staff = pd.concat([self.staff, new_staff], ignore_index=True)
            self.save_data()
            print("Staff added successfully!")
        except ValueError:
            print("Invalid input.")

    # --- Analytics ---
    def show_analytics(self):
        if self.orders.empty:
            print("No data for analytics.")
            return

        print("\n--- Analytics ---")
        print(f"Total Revenue: {self.orders['total_amount'].sum()}")
        print(f"Total Orders: {len(self.orders)}")
        
        # Simple visualization: Orders per day
        self.orders['date'] = pd.to_datetime(self.orders['timestamp']).dt.date
        daily_sales = self.orders.groupby('date')['total_amount'].sum()
        
        print("\nDaily Sales:")
        print(daily_sales)

        # Top Selling Items
        all_items = []
        for items_str in self.orders['items']:
            if isinstance(items_str, str):
                all_items.extend([item.strip() for item in items_str.split(',')])
        
        if all_items:
            item_counts = pd.Series(all_items).value_counts()
            print("\nTop Selling Items:")
            print(item_counts.head())
        
        try:
            daily_sales.plot(kind='bar', title='Daily Sales')
            plt.xlabel('Date')
            plt.ylabel('Revenue')
            plt.tight_layout()
            plt.show()
            print("Graph displayed.")
        except Exception as e:
            print(f"Could not display graph: {e}")

def main_menu():
    system = RestaurantSystem()
    while True:
        print("\n=== Restaurant Management System ===")
        print("1. View Menu")
        print("2. Add Menu Item")
        print("3. Delete Menu Item")
        print("4. Take Order")
        print("5. View Orders")
        print("6. Complete Order")
        print("7. View Staff")
        print("8. Add Staff")
        print("9. Show Analytics")
        print("0. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            system.view_menu()
        elif choice == '2':
            system.add_menu_item()
        elif choice == '3':
            system.delete_menu_item()
        elif choice == '4':
            system.take_order()
        elif choice == '5':
            system.view_orders()
        elif choice == '6':
            system.complete_order()
        elif choice == '7':
            system.view_staff()
        elif choice == '8':
            system.add_staff()
        elif choice == '9':
            system.show_analytics()
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
