# Banking Enterprise Management System

This is a full-stack Banking Enterprise Management System built with **Python**, **Streamlit**, and **MySQL**. It allows users to register, log in, deposit, withdraw, and view transaction history. Admin users can manage all users and perform administrative tasks.

## Features

- User registration and login
- Secure session management
- Account creation with auto-generated account number
- Deposit and withdrawal functionality
- Transaction history tracking
- Admin dashboard to:
  - View all users
  - Promote users to admin
  - Delete users
- Responsive UI using Streamlit with sidebar navigation

## Technologies Used

- Python 3
- Streamlit
- MySQL
- `mysql-connector-python`

## File Structure

- **`streamlit_app.py`**:  
  Main Streamlit script. Controls navigation, session management, routing between pages (Home, Register, Login, Dashboard, Admin), and integrates all modules.

- **`register.py`**:  
  Contains functions or classes (e.g., `SignUp`, `SignIn`) for creating new users and authenticating existing ones.

- **`customer.py`**:  
  Manages customer creation and information. Handles account number generation and storage of personal details.

- **`bank.py`**:  
  Encapsulates deposit, withdrawal, and balance tracking. Also creates per-user transaction tables on account creation.

- **`database.py`**:  
  Abstracts MySQL database connection and query execution. Used across all modules for DB access.

- **`requirements.txt`**:  
  List of all required Python packages (`streamlit`, `mysql-connector-python`, etc.) for setting up the project environment.

- **`README.md`**:  
  This documentation file. Describes the project, setup steps, database schema, and development notes.



## Database Schema

You must create a MySQL database with a `customers` table and individual transaction tables per user.

```sql
CREATE DATABASE bank_system;

USE bank_system;

CREATE TABLE customers (
    username VARCHAR(50) PRIMARY KEY,
    password VARCHAR(100),
    name VARCHAR(100),
    age INT,
    city VARCHAR(100),
    account_number BIGINT,
    is_admin BOOLEAN DEFAULT FALSE
);
