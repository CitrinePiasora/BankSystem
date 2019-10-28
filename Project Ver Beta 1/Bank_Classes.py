from datetime import datetime
import Bank_Functions as bf
from codecs import encode


class Account:
    __balance = 0
    __interest = 0
    __a = 1.05

    def __init__(self, balance=5000, interest=__a):
        self.__balance = balance
        self.__interest = interest

    def getbal(self):
        # returns a balance statement to the user
        desc = "Account Balance: Rp. %s" % (self.__balance)
        return desc

    def deposit(self, dep):
        # returns True or False depending on if process is successful
        try:
            if dep <= 0:
                return False
            else:
                self.__balance += dep
                return True
        except TypeError:
            return False

    def withdraw(self, amt):
        # returns True or False depending on if process is successful
        try:
            if amt <= 0:
                return False
            elif amt > self.__balance:
                return False
            else:
                self.__balance -= amt
                return True
        except TypeError:
            return False

    def export(self):
        # returns the balance
        return self.__balance


class Customer:
    __firstName = ""
    __lastName = ""
    __account = Account(5000)

    def __init__(self, fname, lname):
        self.__firstName = fname
        self.__lastName = lname

    def getname(self):
        # greets the user
        desc = "Welcome to our service %s %s, we hope you enjoy it!" % (
            self.__firstName,
            self.__lastName,
        )
        return desc

    def bye(self):
        # says goodbye to the user
        desc = "Thank you for using our services %s, we hope to see you soon!" % (
            self.__lastName
        )
        return desc

    def makeaccount(self, bal, interest=1.05):
        # makes a new account for the user
        self.__account = Account(bal, interest)

    def getaccount(self):
        # returns the generated account
        return self.__account


class Bank:
    __customer = []
    __bankName = ""

    def __init__(self, name):
        self.__bankName = name

    def addcustom(self, fname, lname, password, interest=1.05):
        # appends new customer data to the class for use with other class functions
        name = "%s %s" % (fname, lname)
        self.__customer.append(
            {
                "name": name,
                "balance": 5000,
                "password": password,
                "interest": interest,
                "last login": datetime.now().strftime("%Y-%m-%d"),
            }
        )

    def balupdateadd(self, name, add, current):
        # updates balance of an account when depositing
        for i in self.__customer:
            if bf.checkName(i, name):
                i["balance"] += add
            else:
                pass

    def balupdatesub(self, name, sub, current):
        # updates balance of an account when withdrawing
        for i in self.__customer:
            if i["name"] == name:
                i["balance"] -= sub
            else:
                pass

    def getcustomer(self, name, customers):
        # gets generated class object Customer() with updated parameters
        for i in customers:
            if bf.checkName(i, name):
                name = name.split()
                customer = Customer(name[0], name[1])
                customer.makeaccount(i["balance"], i["interest"])
                return customer
        else:
            pass

    def loadcustomers(self, cus):
        # loads a list of dictionaries with customer data
        for i in cus:
            self.__customer.append(i)

    def exportcustomers(self):
        # returns the newly updated data
        return self.__customer

    def customers(self):
        # returns a list of customer names, everything else is ommited
        cus = []
        for i in self.__customer:
            cus.append(i["name"])
        return ", ".join(cus)

    def transfer(self, prompt, sub, current, recipient, rep, customerdata):
        # updates the balance of the sender
        customerdata.balupdatesub(prompt, sub, current)
        # updates the balance of the recipient
        customerdata.balupdateadd(recipient, sub, rep)

    def modifyinterest(self, rate):
        # loop that changes the interest rate of all customers
        for i in self.__customer:
            i["interest"] = rate

    def interest(self, name):
        # daily interest is applied, last login date is then updated
        for i in self.__customer:
            date_format = "%Y-%m-%d"
            now = datetime.now()
            if i["name"] == name and i["last login"] != now.strftime(date_format):
                last = datetime.strptime(i["last login"], date_format)
                difference = (now - last).days
                i["balance"] = int(i["balance"] * i["interest"] ** difference)
                i["last login"] = datetime.now().strftime(date_format)

    def passchange(self, name, pword):
        # changes the customer's password
        for i in self.__customer:
            if bf.checkName(i, name) and pword == "blocked":
                i["password"] = pword
            elif bf.checkName(i, name):
                i["password"] = pword

    def passchangecustomeronly(self, name, ogpword, pword):
        # changes the customers password
        success = False
        for i in self.__customer:
            if i["name"] == name and i["password"] == ogpword:
                i["password"] = pword
                success = True
            else:
                continue
        return success

    def removecustomer(self, name):
        # removes a customer from the database
        for i in self.__customer:
            if bf.checkName(i, name):
                self.__customer.remove(i)
