# bank_app.py
# Run with: python -m streamlit run project.py

import streamlit as st
import json
import random
import string
from pathlib import Path

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Bank Management System",
    page_icon="🏦",
    layout="centered"
)

# -----------------------------
# Bank Class
# -----------------------------
class Bank:
    database = "data.json"

    @classmethod
    def load_data(cls):
        file = Path(cls.database)

        if file.exists():
            try:
                with open(file, "r") as f:
                    return json.load(f)
            except:
                return []
        return []

    @classmethod
    def save_data(cls, data):
        with open(cls.database, "w") as f:
            json.dump(data, f, indent=4)

    @classmethod
    def generate_account(cls):
        letters = random.choices(string.ascii_uppercase, k=3)
        digits = random.choices(string.digits, k=4)
        return "".join(letters + digits)

# -----------------------------
# Load Data
# -----------------------------
accounts = Bank.load_data()

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("🏦 Bank Menu")

menu = st.sidebar.radio(
    "Select Option",
    [
        "Create Account",
        "Deposit Money",
        "Withdraw Money",
        "Show Details",
        "Update Details",
        "Delete Account"
    ]
)

# -----------------------------
# Create Account
# -----------------------------
if menu == "Create Account":
    st.title("📝 Create New Account")

    name = st.text_input("Enter Name")
    mobile = st.text_input("Mobile Number")
    email = st.text_input("Email")
    age = st.number_input("Age", min_value=1, max_value=100)
    pin = st.text_input("4 Digit PIN", type="password")

    if st.button("Create Account"):

        if age < 18:
            st.error("Minimum age should be 18.")
        elif len(pin) != 4:
            st.error("PIN must be 4 digits.")
        else:
            account_no = Bank.generate_account()

            data = {
                "name": name,
                "number": mobile,
                "email": email,
                "age": age,
                "pin": pin,
                "accountNo": account_no,
                "balance": 0
            }

            accounts.append(data)
            Bank.save_data(accounts)

            st.success("Account Created Successfully!")
            st.info(f"Your Account Number: {account_no}")

# -----------------------------
# Deposit Money
# -----------------------------
elif menu == "Deposit Money":
    st.title("💰 Deposit Money")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount", min_value=1)

    if st.button("Deposit"):

        found = False

        for user in accounts:
            if user["accountNo"] == acc and user["pin"] == pin:
                user["balance"] += amount
                Bank.save_data(accounts)
                st.success("Money Deposited Successfully!")
                found = True
                break

        if not found:
            st.error("Invalid Account Number or PIN")

# -----------------------------
# Withdraw Money
# -----------------------------
elif menu == "Withdraw Money":
    st.title("🏧 Withdraw Money")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount", min_value=1)

    if st.button("Withdraw"):

        found = False

        for user in accounts:
            if user["accountNo"] == acc and user["pin"] == pin:

                if user["balance"] >= amount:
                    user["balance"] -= amount
                    Bank.save_data(accounts)
                    st.success("Withdraw Successful!")
                else:
                    st.error("Insufficient Balance")

                found = True
                break

        if not found:
            st.error("Invalid Account Number or PIN")

# -----------------------------
# Show Details
# -----------------------------
elif menu == "Show Details":
    st.title("📄 Account Details")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Show Details"):

        found = False

        for user in accounts:
            if user["accountNo"] == acc and user["pin"] == pin:
                st.json(user)
                found = True
                break

        if not found:
            st.error("Invalid Account Number or PIN")

# -----------------------------
# Update Details
# -----------------------------
elif menu == "Update Details":
    st.title("✏️ Update Account")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    name = st.text_input("New Name")
    mobile = st.text_input("New Mobile")
    email = st.text_input("New Email")

    if st.button("Update"):

        found = False

        for user in accounts:
            if user["accountNo"] == acc and user["pin"] == pin:

                if name:
                    user["name"] = name
                if mobile:
                    user["number"] = mobile
                if email:
                    user["email"] = email

                Bank.save_data(accounts)
                st.success("Updated Successfully!")

                found = True
                break

        if not found:
            st.error("Invalid Account Number or PIN")

# -----------------------------
# Delete Account
# -----------------------------
elif menu == "Delete Account":
    st.title("❌ Delete Account")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Delete"):

        found = False

        for user in accounts:
            if user["accountNo"] == acc and user["pin"] == pin:
                accounts.remove(user)
                Bank.save_data(accounts)
                st.success("Account Deleted Successfully!")
                found = True
                break

        if not found:
            st.error("Invalid Account Number or PIN")