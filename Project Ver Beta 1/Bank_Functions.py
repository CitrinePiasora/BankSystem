import json
from datetime import datetime
import bcrypt


def checkName(i, name):
    # simple function to make checking easier due to intellisense
    return i["name"] == name


def checkPassword(i, pword):
    if pword == "blocked":
        return (True if i["password"] == pword else False)
    else:
        # uses bcrypt's password checker to see if the plain text password (converted into bytes)
        # matches the hashed password stored in the json (converted back into bytes)
        return bcrypt.checkpw(pword.encode(), i["password"].encode())


def confirmer():
    # simple function to ask for confirmation. Returning True if Yes and False if No
    confirm = str(input("\nAre you sure? [Y/N]\n>>> ")).lower()
    if confirm in ("y", "1", "yes"):
        return True
    else:
        return False


def DepositAndWithdraw(transaction, prompt, amt, current, customerdata):
    # A function to make the code cleaner by condensing 2 similar types of code
    # these 2 transaction types are used in a lot of different parts of the code
    if transaction == "deposit":
        # if transaction type is a deposit, it will run the code for depositing funds
        if current.getaccount().deposit(amt):
            # class function is called in order to update the user's balance
            customerdata.balupdateadd(prompt, amt, current)
            print("\nYou have deposited Rp.", amt)
            # class function is called in order to print a balance statement
            print("\n%s" % current.getaccount().getbal())
    elif transaction == "withdraw":
        # if transaction type is a withdrawal, it will run the code for withdrawal
        if current.getaccount().withdraw(amt):
            # class function is called in order to update the user's balance
            customerdata.balupdatesub(prompt, amt, current)
            print("\nYou have withdrawn Rp.", amt)
            # class function is called in order to print a balance statement
            print("\n%s" % current.getaccount().getbal())
        else:
            print("\nError, Can't withdraw beyond your total balance!")


def newbank(name, password, banks, filename, hasher):
    # updates the database of banks to be exported into the master banks file
    # this is done immediately when a new bank is made
    banks.append({"name": name, "password": password, "hasher": hasher.decode()})
    with open(filename, "w") as f_obj:
        f_obj.write(json.dumps({"banks": banks}, indent=2))


def newcustomer(name, customers, database, password, interest=1.05, balance=5000):
    # updates the database of customers to be exported into a banks' specific
    # database json file
    customers.append(
        {
            "name": name,
            "balance": balance,
            "password": password,
            "interest": interest,
            "last login": datetime.now().strftime("%Y-%m-%d"),
        }
    )
    with open(database, "w") as f_obj:
        f_obj.write(json.dumps({"customers": customers}, indent=2))


def loadcustomers(database):
    # loads the list of dictionaries containing customer data and returns it
    try:
        with open(database) as f_obj:
            dataset = json.loads(f_obj.read())
            customers = dataset["customers"]
        return customers
    except FileNotFoundError:
        # in the event that a bank has lost its database or has no customers
        # return an empty list to prevent errors
        customers = []
        return customers


def acctype(admin=False, guest=False):
    # a loop to determine which boolean gets turned into True for use in the
    # main program
    while True:
        logintype = str(input("Login as an:\n1. User\n2. Admin\n>>> ")).lower()
        # returns guest = True if guest is selected
        if logintype in ("user", "guest", "1"):
            guest = True
            return admin, guest
        # returns admin = True if guest is selected
        elif logintype in ("admin", "2"):
            admin = True
            return admin, guest
        else:
            continue


def transferbetweeen(prompt, recipient, current, customerdata, recipientbank):
    # transfers funds from customer's account to an account from a different banks'
    secondbase = recipientbank + ".json"
    # loads the target banks' database for editing
    temp = loadcustomers(secondbase)
    for i in temp:
        if checkName(i, recipient):
            # if the recipient is found, asks for the amount
            transfer = int(input("\nHow much would you like to transfer?\n>>> "))
            if confirmer():
                # calls DepositAndWithdraw to update customer balance (in this case reduce)
                DepositAndWithdraw("withdraw", prompt, transfer, current, customerdata)
                for b in temp:
                    if checkName(b, recipient):
                        # the balance of the recipient is updated to the temp list
                        b["balance"] += transfer
                        # the temp list is no longer needed as the transaction is over
                        # and is exported out into the target banks' database
                        with open(secondbase, "w") as f_out:
                            f_out.write(json.dumps({"customers": temp}, indent=2))
                    else:
                        pass
                print(
                    "\nYou have transferred Rp.",
                    transfer,
                    "to %s of %s bank" % (recipient, recipientbank),
                )
                # class function is called in order to print a balance statement
                print(current.getaccount().getbal())
            else:
                # if transaction is not possible, return an error statement
                print("\nError, Can't transfer beyond your total balance!")
    else:
        pass


def transferlocal(recipient, customerdata, customers, cname, current):
    # transfers funds to a different account from the same bank
    for i in customerdata.exportcustomers():
        if checkName(i, recipient):
            # rec is assigned the recipient's account data if True
            rec = customerdata.getcustomer(recipient, customers)
            transfer = int(input("\nHow much would you like to transfer?\n>>> "))
            if confirmer():
                # if the transaction is possible (True is returned)
                if current.getaccount().withdraw(transfer):
                    # both recipient's and sender's balances are updated in the database
                    # via class function
                    customerdata.transfer(
                        cname, transfer, current, recipient, rec, customerdata
                    )
                else:
                    # if transaction is not possible, return an error statement
                    print("\nError, Can't transfer beyond your total balance!")


def bankpass(banks, name, ogpword, pword, filename):
    # changes the password of the bank admin account
    # "success" determines whether the new data was added
    success = False
    for i in banks:
        if i["name"] == name and checkPassword(i, ogpword):
            i["password"] = pword
            success = True
    if success:
        # if success is True, process has succeeded and the new data
        # is exported immediately to the bank admin account database
        with open(filename, "w") as f_obj:
            f_obj.write(json.dumps({"banks": banks}, indent=2))
    else:
        # otherwise it returns a failure message
        print("Error! Original Password is wrong!")


def savedata(database, customerdata, customers, prompt=None):
    # function used to export each banks' customer database
    with open(database, "w") as f_obj:
        f_obj.write(json.dumps({"customers": customerdata.exportcustomers()}, indent=2))
    # if admin, bids admin farewell
    if prompt == None:
        print("\nGoodbye!")
        program = False
        return program
    # if guest, thanks guest and bids them farewell
    elif prompt != None:
        print("\n%s" % customerdata.getcustomer(prompt, customers).bye())
        program2 = False
        return program2


def Hashed(string, name, banks, salt=None):
    # a function to hash the passwords
    # if there is no input for salt, it defaults to none which loads
    # an existing salt from the database
    if salt != None:
        salt = salt
    else:
        # it has to check as each bank has a completely unique salt
        for i in banks:
            if checkName(i, name):
                salt = i["hasher"].encode()
                break
            else:
                pass
    try:
        # tries to hash the password and then returns the data in str form
        hashed = bcrypt.hashpw(string.encode(), salt)
        return hashed.decode()
    except NameError:
        pass


def NameLogin(lists, admin=False):
    # function that contains a loop to determine if a user is registered
    # admin is defaulted to False as an optional parameter
    while True:
        name = str(input("\nUsername: "))
        # the lists lets this function be used for both admin and guest accounts
        for i in lists:
            if checkName(i, name):
                success = 1
                break
            else:
                success = 0
                continue

        if success == 1:
            if admin:
                # false is returned so that the new user loop doesn't trigger
                return name, False
            else:
                # true is returned so that a new user will be created
                return name, True
        else:
            if admin:
                new = str(
                    input(
                        "\nThe username is not in our database.\nWould you like to make a new account? [Y/N]:\n>>> "
                    )
                ).lower()
                if new in ("y", "1", "yes"):
                    # true is returned so that a new user will be created
                    return name, True
                else:
                    continue
            else:
                quit = str(
                    input(
                        "\nThat user is not registered in our database.\nWould you like to try again or quit?\n>>> "
                    )
                ).lower()
                if quit in ("quit", "y", "exit", "y"):
                    print("Goodbye!")
                    # returns False so that the login process will end and the program will exit
                    return name, False
                else:
                    continue
