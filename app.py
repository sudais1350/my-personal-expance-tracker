
import streamlit as st
from datetime import date

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💰",
    layout="wide"
)

# ==========================================
# APPLICATION TITLE
# ==========================================

st.title("💰 Personal Expense Tracker")
st.write("Manage your daily expenses easily and track your spending.")

# ==========================================
# INITIALIZE SESSION STATE
# ==========================================

if "expenses" not in st.session_state:
    st.session_state.expenses = []

if "next_id" not in st.session_state:
    st.session_state.next_id = 1


# ==========================================
# FUNCTIONS
# ==========================================

# Function to add an expense
def add_expense(name, amount, category, expense_date):

    expense = {
        "ID": st.session_state.next_id,
        "Expense Name": name,
        "Amount": amount,
        "Category": category,
        "Date": expense_date
    }

    st.session_state.expenses.append(expense)
    st.session_state.next_id += 1


# Function to delete an expense
def delete_expense(expense_id):

    st.session_state.expenses = [
        expense for expense in st.session_state.expenses
        if expense["ID"] != expense_id
    ]


# Function to calculate total expenses
def calculate_total(expenses):

    total = 0

    for expense in expenses:
        total += expense["Amount"]

    return total


# Function to find highest expense
def highest_expense(expenses):

    if not expenses:
        return 0

    highest = max(expenses, key=lambda x: x["Amount"])

    return highest["Amount"]


# Function to calculate category-wise expenses
def category_summary(expenses):

    summary = {}

    for expense in expenses:

        category = expense["Category"]
        amount = expense["Amount"]

        if category in summary:
            summary[category] += amount
        else:
            summary[category] = amount

    return summary


# ==========================================
# SIDEBAR - SEARCH AND FILTERS
# ==========================================

st.sidebar.title("🔍 Search & Filters")

search_name = st.sidebar.text_input(
    "Search Expense",
    placeholder="Enter expense name..."
)

categories = ["All", "Food", "Travel", "Shopping", "Bills", "Other"]

selected_category = st.sidebar.selectbox(
    "Select Category",
    categories
)

# Get current expenses for slider range
if st.session_state.expenses:

    amounts = [
        expense["Amount"]
        for expense in st.session_state.expenses
    ]

    min_amount = min(amounts)
    max_amount = max(amounts)

    if min_amount == max_amount:
        max_amount += 1

    amount_range = st.sidebar.slider(
        "Filter by Amount",
        min_value=float(min_amount),
        max_value=float(max_amount),
        value=(float(min_amount), float(max_amount))
    )

else:

    amount_range = (0.0, 10000.0)

    st.sidebar.slider(
        "Filter by Amount",
        min_value=0.0,
        max_value=10000.0,
        value=amount_range,
        disabled=True
    )


# ==========================================
# TASK 1 - ADD EXPENSE FORM
# ==========================================

st.header("➕ Add New Expense")

with st.form("expense_form", clear_on_submit=True):

    expense_name = st.text_input(
        "Expense Name",
        placeholder="Enter expense name"
    )

    amount = st.number_input(
        "Amount",
        min_value=0.01,
        value=100.0,
        step=10.0
    )

    category = st.selectbox(
        "Category",
        ["Food", "Travel", "Shopping", "Bills", "Other"]
    )

    expense_date = st.date_input(
        "Date",
        value=date.today()
    )

    submit = st.form_submit_button("Add Expense")

    if submit:

        if expense_name.strip() == "":
            st.error("Please enter an expense name.")

        elif amount <= 0:
            st.error("Amount must be greater than zero.")

        else:

            add_expense(
                expense_name.strip(),
                amount,
                category,
                expense_date
            )

            st.success("Expense added successfully! 🎉")


# ==========================================
# TASK 2 - DASHBOARD SUMMARY
# ==========================================

st.header("📊 Dashboard Summary")

expenses = st.session_state.expenses

total_expenses = calculate_total(expenses)

total_transactions = len(expenses)

highest = highest_expense(expenses)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Total Expenses",
        value=f"Rs. {total_expenses:,.2f}"
    )

with col2:
    st.metric(
        label="Total Transactions",
        value=total_transactions
    )

with col3:
    st.metric(
        label="Highest Expense",
        value=f"Rs. {highest:,.2f}"
    )


# ==========================================
# TASK 4 - SEARCH AND FILTERING
# ==========================================

filtered_expenses = []

for expense in expenses:

    # Search filter
    search_match = (
        search_name.lower() in expense["Expense Name"].lower()
    )

    # Category filter
    category_match = (
        selected_category == "All"
        or expense["Category"] == selected_category
    )

    # Amount filter
    amount_match = (
        amount_range[0]
        <= expense["Amount"]
        <= amount_range[1]
    )

    if search_match and category_match and amount_match:
        filtered_expenses.append(expense)


# ==========================================
# TASK 3 - DISPLAY EXPENSE RECORDS
# ==========================================

st.header("📋 Expense Records")

if filtered_expenses:

    # Prepare records for display
    display_records = []

    for expense in filtered_expenses:

        display_records.append({
            "Expense Name": expense["Expense Name"],
            "Amount": f"Rs. {expense['Amount']:,.2f}",
            "Category": expense["Category"],
            "Date": expense["Date"]
        })

    st.dataframe(
        display_records,
        use_container_width=True,
        hide_index=True
    )

    st.success(
        f"{len(filtered_expenses)} expense record(s) found."
    )

else:

    if expenses:
        st.warning("No expenses match your search or filters.")
    else:
        st.warning("No expenses available. Add your first expense!")


# ==========================================
# TASK 5 - DELETE EXPENSE
# ==========================================

st.header("🗑️ Delete Expense")

if expenses:

    for expense in expenses:

        col1, col2 = st.columns([4, 1])

        with col1:

            st.write(
                f"**{expense['Expense Name']}** | "
                f"Rs. {expense['Amount']:,.2f} | "
                f"{expense['Category']} | "
                f"{expense['Date']}"
            )

        with col2:

            if st.button(
                "Delete",
                key=f"delete_{expense['ID']}"
            ):

                delete_expense(expense["ID"])

                st.success(
                    f"{expense['Expense Name']} deleted successfully!"
                )

                st.rerun()

else:

    st.warning("No expenses available to delete.")


# ==========================================
# TASK 6 - CATEGORY-WISE SUMMARY
# ==========================================

st.header("📂 Category-wise Expense Summary")

if expenses:

    summary = category_summary(expenses)

    for category_name, total in summary.items():

        st.subheader(category_name)

        st.write(f"Total: Rs. {total:,.2f}")

else:

    st.warning("No category data available yet.")


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.write(
    "💰 Personal Expense Tracker | "
    "Developed using Python and Streamlit"
)
