import json
import Bank_Functions as bf
import Bank_Classes as bc
from bcrypt import gensalt
from Bank_Classes import Bank

filename = "banks.json"
banks = []
customers = []

# the boolean that controls the appearance of the admin only functions
program = False
# the boolean that controls the appearance of the guest functions
program2 = False
# the boolean that controls the customer login
login = False
# counter used to limit number of attempts for wrong passwords
newuser = False
# boolean to control the new user function
attempts = 3
# indicator if login failed


# gets a list of banks from banks.json
with open(filename) as f_obj:
    bank = json.loads(f_obj.read())
    banks = bank["banks"]

# login process done by external function imported from a different py file
# assigns these 2 values after a prompt loop to determine their boolean values
admin, guest = bf.acctype()

if admin:
    name, newuser = bf.NameLogin(banks, admin)
    # the new bank's database is set
    database = name + ".json"

if newuser:
    # hashing requires a salt in order to match hashed passwords and inputted password
    # a new salt is generated for new admin accounts in order to hash their passwords
    salt = gensalt()
    password = bf.Hashed(str(input("\nPassword: ")), name, banks, salt)
    bf.newbank(name, password, banks, filename, salt)
    # creates an object of class Bank called customerdata
    customerdata = bc.Bank(name)
    # new banks will have a default interest rate of 1.003, which can be changed later
    bankrate = 1.003
    # starts the admin only program
    program = True
    # disables the admin login program
    admin = False

while admin == True:
    password = str(input("\nPassword: "))
    for i in banks:
        if bf.checkName(i, name) and bf.checkPassword(i, password):
            # creates an object of class Bank called customerdata
            customerdata = bc.Bank(name)
            # customer data is loaded into a customers list
            customers = bf.loadcustomers(database)
            # makes sure all new customers have the same rate as every other existing customer
            # all existing customers have the same interest, hence why customers[0]  is called
            try:
                bankrate = customers[0]["interest"]
            # in the event that the bank lost its database, the bankrate is reset to default 1.003
            except IndexError:
                bankrate = 1.003
            # customers list is then loaded into the object to be used in program
            customerdata.loadcustomers(customers)
            # starts the admin only program
            program = True
            # turns off the admin login program
            admin = False
            # this short loop is used to update customers' interest rates in case they got desynced between
            # new and old customers
            for i in customers:
                customerdata.interest(i["name"])
            break
        elif password in ("exit", "quit"):
            admin = False
            break
        else:
            pass

while program == True:
    command = str(
        input(
            "\nHere are a list of commands:\n1. List of Customers\n2. Add Customer\n3. Remove/Cancel Customer\n4. Modify Interest Rate\n5. Change Customer Password\n6. Change Admin Password\n7. Exit \n>>> "
        )
    ).lower()
    if command in ("1", "list", "customers"):
        # class functioned is called in order to return a list of customers
        print("\n%s" % customerdata.customers())
    elif command in ("2", "add", "add customers"):
        cfname = str(input("\nFirst Name: ")).capitalize()
        clname = str(input("Last Name: ")).capitalize()
        # creates a hashed password for the new user that will be stored in the database
        pword = bf.Hashed(str(input("\nPassword: ")), name, banks)
        # class function is called to make a new customer
        customerdata.addcustom(cfname, clname, pword, bankrate)
        fullname = "%s %s" % (cfname, clname)
        # customers are exported and added into the database json file
        bf.newcustomer(fullname, customers, database, pword)
        print("%s %s has been registered" % (cfname, clname))
    elif command in ("3", "remove", "cancel", "remove customer"):
        cname = str(input("\nWhich customer?\n>>> "))
        check = next((True for i in customerdata.exportcustomers() if cname == i["name"]), False)
        # check removes the need for a loop and makes the output only return 1 failure message
        if check:
            if bf.confirmer():
                # sets the customers Customer() class object so that less code needs to be written
                current = customerdata.getcustomer(cname, customers)
                transfer = str(
                    input(
                        "Would you like to transfer remaining funds to a different account? A manual return will have a Rp. 50000 administration fee [Y/N]\n>>> "
                    )
                )
                if transfer in ("y", "1", "yes"):
                    recipient = str(
                        input("Who would you wish to transfer funds to?\n>>> ")
                    )
                    ask = str(
                        input("Does the recipient go to this same bank?\n>>> ")
                    ).lower()
                    if ask in ("y", "1", "yes"):
                        # function to transfer between same bank is called, continued in Bank_Functions
                        bf.transferlocal(
                            recipient, customerdata, customers, cname, current
                        )
                        # customer is removed from database
                        customerdata.removecustomer(cname)
                        print(
                            "Thank you for using our services, your account has now been removed"
                        )
                    else:
                        recipientbank = str(
                            input("What bank does the recipient go to?\n>>> ")
                        )
                        # function to transfer between different bank is called, continued in Bank_Functions
                        bf.transferbetweeen(
                            cname, recipient, current, customerdata, recipientbank
                        )
                        # customer is removed from database
                        customerdata.removecustomer(cname)
                        print(
                            "Thank you for using our services, your account has now been removed"
                        )
                else:
                    # returned amount after Rp. 50k service tax for physical returns
                    returned = current.getaccount().export() - 50000
                    if returned <= 0:
                        print(
                            "Thank you for using our services, your account has now been removed"
                        )
                        # customer is removed
                        customerdata.removecustomer(cname)
                    else:
                        print(
                            "Rp. %s will be returned to you in cash, your account has now been removed"
                            % returned
                        )
                        # customer is removed
                        customerdata.removecustomer(cname)
            else:
                print("Procedure was cancelled")
        else:
            print("User was not found in our database")
    elif command in ("4", "interest", "rate"):
        rate = float(input("\nInput a new rate\n>>> "))
        # class function is called in order to change all customers' interest rate
        customerdata.modifyinterest(rate)
        print("Daily interest rate has been change to %s" % rate)
    elif command in ("5", "change password", "password", "change"):
        cname = str(input("\nWhich customer?\n>>> "))
        pword = bf.Hashed(str(input("Set a new password:\n>>> ")), name, banks)
        if bf.confirmer():
            customerdata.passchange(cname, pword)
            print("\n%s's password has been changed." % cname)
        else:
            pass
    elif command in ("6", "admin pass"):
        ogpword = str(input("\nOriginal Password: "))
        newpword = bf.Hashed(str(input("New Password: ")), name, banks)
        bf.bankpass(banks, name, ogpword, newpword, filename)
        print("\nYour password has been changed.")
    elif command in ("7", "quit", "exit"):
        # bank's database is exported into it's database json file
        program = bf.savedata(database, customerdata, customers)

while guest == True:
    bankname = str(input("\nWhat bank do you go to:\n>>> "))
    for i in banks:
        if bf.checkName(i, bankname):
            database = bankname + ".json"
            # creates an object of class Bank called customerdat
            customerdata = bc.Bank(bankname)
            # customer data is loaded into a customers list
            customers = bf.loadcustomers(database)
            # customers list is then loaded into the object to be used in program
            customerdata.loadcustomers(customers)
            # turns off the bank check
            guest = False
            for i in customers:
                customerdata.interest(i["name"])
            prompt, login = bf.NameLogin(customerdata.exportcustomers())
        else:
            continue

while login == True:
    for i in customerdata.exportcustomers():
        if bf.checkName(i, prompt) and bf.checkPassword(i, "blocked"):
            print(
                "The account you are trying to access is blocked, please seek customer services to get it unblocked"
            )
            login = False
        elif bf.checkName(i, prompt) and bf.checkPassword(i, "blocked") == False:
            pword = str(
                input(
                    "Please input your password (You may use cancel/exit to cancel the transaction):\n>>> "
                )
            )
            # checks if the names and passwords match the data from the list of dictionaries
            # found in customerdata.__customer
            for i in customerdata.exportcustomers():
                if i["name"] == prompt and bf.checkPassword(i, pword):
                    # assigns the account to a variable for cleaner code
                    current = customerdata.getcustomer(prompt, customers)
                    # prints out a greeting!
                    print("\n%s" % current.getname())
                    # disables login sequence
                    login = False
                    # enables the guest program
                    program2 = True
                elif pword in ("exit", "cancel"):
                    # acts like an ATM cancel button and cancels the login session
                    login = False
                elif i["name"] == prompt and attempts == 0:
                    # blocks the customers account
                    customerdata.passchange(prompt, "blocked")
                    print(
                        "This account is now blocked, please contact customer services to get it unblocked"
                    )
                    program = bf.savedata(database, customerdata, customers)
                    login = False
                elif i["name"] == prompt and bf.checkPassword(i, "blocked") == False:
                    # prevents account from being accessed
                    print(
                        "You have %s attempts left before the account is blocked\n"
                        % attempts
                    )
                    attempts -= 1
                    continue
        else:
            pass

while program2 == True:
    command = str(
        input(
            "\nHere are a list of commands:\n1. Balance Inquiry\n2. Deposit\n3. Withdraw\n4. Transfer\n5. Transfer between Banks\n6. Change Password\n7. Exit\n>>> "
        )
    ).lower()
    if command in ("1", "balance", "balance inquiry"):
        # class function is called in order to print a balance statement
        print("\n%s" % current.getaccount().getbal())
    elif command in ("2", "deposit"):
        dep = int(input("\nHow much would you like to deposit?\n>>> "))
        if bf.confirmer():
            bf.DepositAndWithdraw("deposit", prompt, dep, current, customerdata)
        else:
            continue
    elif command in ("3", "withdraw"):
        withdraw = int(input("\nHow much would you like to withdraw?\n>>> "))
        if bf.confirmer():
            bf.DepositAndWithdraw("withdraw", prompt, withdraw, current, customerdata)
    elif command in ("4", "transfer"):
        recipient = str(input("\nWho would you wish to transfer funds to?\n>>> "))
        bf.transferlocal(recipient, customerdata, customers, prompt, current)
        print(current.getaccount().getbal())
    elif command in ("5", "transfer between banks"):
        recipient = str(input("\nWho would you wish to transfer funds to?\n>>> "))
        recipientbank = str(input("\nWhat bank does the recipient go to?\n>>> "))
        bf.transferbetweeen(prompt, recipient, current, customerdata, recipientbank)
    elif command in ("6", "change password", "password"):
        ogpword = bf.Hashed(str(input("\nOriginal Password: ")), bankname, banks)
        pword = bf.Hashed(str(input("\nNew Password: ")), bankname, banks)
        if bf.confirmer():
            if customerdata.passchangecustomeronly(prompt, ogpword, pword):
                print("\nYour password has now been changed")
            else:
                attempts -= 1
                print(
                    "\nYour Original Password is wrong, please try again.\nYou have %s attempts left"
                    % attempts
                )
                if attempts == 0:
                    customerdata.passchange(prompt, "blocked")
                    print(
                        "\nThis account is now blocked, please contact customer services to get it unblocked"
                    )
                    program2 = bf.savedata(database, customerdata, customers)
                else:
                    pass
        else:
            pass
    elif command in ("7", "quit", "exit"):
        # bank's database is exported into it's database json file
        program2 = bf.savedata(database, customerdata, customers, prompt)
