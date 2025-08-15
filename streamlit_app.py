# streamlit_app.py
import streamlit as st
from register import SignUp, SignIn
from customer import Customer
from bank import Bank
from database import db_query
from random import randint

# Page config
st.set_page_config(page_title="Colony Bank App", layout="wide")
st.title("Colony Bank of India")

# Session init
if "username" not in st.session_state:
    st.session_state.username = None

# Set default admins (hardcoded for demo)
for default_admin in ["admin", "Bharat"]:
    admin_exists = db_query(f"SELECT username FROM customers WHERE username='{default_admin}';")
    if admin_exists:
        db_query(f"UPDATE customers SET is_admin=1 WHERE username='{default_admin}';")
        st.caption(f"Note: Default user '{default_admin}' has been promoted to administrator.")

# Sidebar navigation
menu = ["Home", "Register", "Login", "Dashboard", "Transactions", "Admin"]
choice = st.sidebar.radio("Navigate", menu)

# Home Page
if choice == "Home":
    st.write("Welcome to Colony Bank's digital banking system.")

# Register Page
elif choice == "Register":
    st.subheader("Register New Account")
    uname = st.text_input("Username")
    passwd = st.text_input("Password", type="password")
    name = st.text_input("Full Name")
    age = st.number_input("Age", min_value=10, max_value=100)
    city = st.text_input("City")

    if st.button("Register"):
        acct = randint(10000000, 99999999)
        if db_query(f"SELECT username FROM customers WHERE username = '{uname}';"):
            st.error("Username already exists")
        else:
            cust = Customer(uname, passwd, name, age, city, acct)
            cust.createuser()
            bank = Bank(uname, acct)
            bank.create_transaction_table()
            st.success(f"Account created. Your Account Number: {acct}")

# Login Page
elif choice == "Login":
    st.subheader("Login")
    uname = st.text_input("Username")
    passwd = st.text_input("Password", type="password")

    if st.button("Login"):
        result = db_query(f"SELECT password FROM customers WHERE username = '{uname}';")
        if not result:
            st.error("Username not found")
        elif result[0][0] == passwd:
            st.session_state.username = uname
            st.success(f"Welcome {uname}")
        else:
            st.error("Incorrect password")

# Dashboard Page
elif choice == "Dashboard":
    if st.session_state.username:
        st.subheader("Dashboard")
        st.write(f"Logged in as: {st.session_state.username}")
        amount = st.number_input("Amount", min_value=1)
        if st.button("Deposit"):
            Bank(st.session_state.username, 0).deposit(amount)
            st.success(f"Deposited ₹{amount}")
        if st.button("Withdraw"):
            success = Bank(st.session_state.username, 0).withdraw(amount)
            if success:
                st.success(f"Withdrew ₹{amount}")
            else:
                st.error("Insufficient Balance")
    else:
        st.warning("Please login to access dashboard.")

# Transactions Page
elif choice == "Transactions":
    if st.session_state.username:
        st.subheader("Transaction History")
        data = db_query(f"SELECT * FROM transaction_{st.session_state.username} ORDER BY date DESC LIMIT 10;")
        if data:
            st.table(data)
        else:
            st.info("No transactions available.")
    else:
        st.warning("Please login to view transactions.")

# Admin Page
elif choice == "Admin":
    if st.session_state.username in ["admin", "Bharat"]:
        st.subheader("Admin Dashboard")
        st.write("Manage all users below")
        users = db_query("SELECT username, name, age, city FROM customers;")
        st.table(users)

        promote_user = st.text_input("Promote user to admin")
        if st.button("Promote"):
            db_query(f"UPDATE customers SET is_admin=1 WHERE username='{promote_user}';")
            st.success(f"{promote_user} promoted to admin.")

        delete_user = st.text_input("Delete user")
        if st.button("Delete"):
            db_query(f"DELETE FROM customers WHERE username='{delete_user}';")
            st.success(f"Deleted {delete_user} and their data.")
    else:
        st.warning("Admin access only")
