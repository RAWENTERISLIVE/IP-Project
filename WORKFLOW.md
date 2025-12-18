# Restaurant Management System Workflow

## Daily Operations

1.  **Start of Day**:
    *   Run the system: `python3 restaurant_management_system.py`
    *   Check `View Menu` to ensure all items are available.
    *   Check `View Staff` to confirm shift details.

2.  **During Service**:
    *   **New Customer**: Use `Take Order` (Option 4) to log items for a table.
    *   **Kitchen Update**: Chefs view orders via `View Orders` (Option 5).
    *   **Payment**: When customer pays, use `Complete Order` (Option 6).

3.  **End of Day**:
    *   Run `Show Analytics` (Option 9) to see total sales.
    *   Check the generated graph for trends.
    *   Backup `orders.csv` if needed.

## Data Files
*   `menu.csv`: Stores menu items.
*   `orders.csv`: Stores transaction history.
*   `staff.csv`: Stores employee records.
