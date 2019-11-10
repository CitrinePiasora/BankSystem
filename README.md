# Project
Project Repository for first project

# Features
2 different parts, one admin program, one customer program
All data is saved in the form of **".json"**
Each Bank's admin account has their own specific databases with a master database file for admin accounts

# Admin Account Features
1. Change Bank Interest Rate
2. Change Customer Password 
3. Customer List
4. Remove Customer
5. Adding Customers
6. Change Admin Password

# Admin Feature Extra Information
1. The Interest Rate is **Monthly Interest**
2. Customers can choose to transfer funds to accounts from different or samee banks as well as physical return upon cancellation of account

# Customer Account Features
1. You can choose which bank to access
2. Balance Inquiry
3. Withdrawal and Deposits
4. Transfer locally between the same bank
5. Transfer between different banks
6. Change User Password

# Some Extra General Information
1. All banks have a unique salt to hash the passwords of their customers
2. Since hashing is used, there is no chance of a leak of customer data
3. All passwords are hashed (Customer and Admin accounts included)
4. Customer accounts can be **"blocked"**, preventing the account from being accessed in case of a breach
5. Customers get 3 attempts total (when changing passwords and logging in) before the account is blocked
