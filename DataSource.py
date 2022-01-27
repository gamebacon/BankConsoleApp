import datetime

from Account import Account
from Customer import Customer
from Transaction import Transaction


# Writes string to file
def __write__(file_name, text):
    file = open(file_name, "wt")
    file.write(text)
    file.close()
    pass


# Returns all lines as string from file
def __read__(file_name):
    file = open(file_name, "rt")
    text = file.read()
    file.close()
    return text


class DataSource:

    def datasource_conn(self):
        pass

    def update_by_id(self):
        pass

    def find_by_id(self):
        pass

    def remove_by_id(self):
        pass

    # Saves all customer data to file.
    def save_all(self, customers):
        text = ""
        for customer in customers.values():
            text += "%s:%s:%s:%s," % (customer.id, customer.first_name, customer.last_name, customer.person_number)
            for account in customer.get_accounts().values():
                text += "%s:%s:%s#" % (account.id, account.type, account.balance)
            text = text[0:-1] + "\n"
        __write__("data/customers.txt", text)
        self.__save_transactions__(customers)

    # Saves all the transactions to file.
    def __save_transactions__(self, customers):
        text = ""
        for customer in customers.values():
            for account in customer.get_accounts().values():
                text += str(account.id) + ","
                for transaction in account.get_transactions().values():
                    text += "%s;%s;%s#" % (transaction.id, transaction.date.strftime("%Y-%m-%d %H:%M:%S"), transaction.amount)
                text = text[0:-1] + "\n"
        __write__("data/transactions.txt", text)

    # Returns a dictionary with all transactions
    def __get_all_transactions__(self):
        all_transactions = {}
        lines = __read__("data/transactions.txt").split("\n")

        for line in lines:
            if len(line) == 0:
                continue
            account_transactions = {}
            data = line.split(",")
            account_id = int(data[0])
            if len(data) > 1 and len(data[1]) > 0:
                for transaction in data[1].split("#"):
                    transaction_details = transaction.split(";")
                    transaction_id = int(transaction_details[0])
                    # date = transaction_details[1]
                    # print(transaction_details[1])
                    date = datetime.datetime.strptime(transaction_details[1], '%Y-%m-%d %H:%M:%S')
                    amount = transaction_details[2]
                    account_transactions[transaction_id] = Transaction(transaction_id, date, amount)
            all_transactions[account_id] = account_transactions
        return all_transactions

    # Returns all customer data.
    def get_all(self):
        customers = {}
        all_transactions = self.__get_all_transactions__()
        lines = __read__("data/customers.txt").split("\n")
        for line in lines:
            accounts = {}
            if len(line) == 0:
                continue
            all_data = line.split(',')
            personal_data = all_data[0].split(":")
            customer_id = int(personal_data[0])
            first_name = personal_data[1]
            last_name = personal_data[2]
            person_number = personal_data[3]
            if len(all_data) > 1:
                for all_account_data in all_data[1].split("#"):
                    account_data = all_account_data.split(":")
                    account_id = int(account_data[0])
                    account_type = account_data[1]
                    account_balance = float(account_data[2])
                    transactions = all_transactions.get(account_id)
                    account = Account(account_id, account_type, account_balance, transactions if transactions else {})
                    accounts[account_id] = account
            customers[customer_id] = Customer(customer_id, first_name, last_name, person_number, accounts)
        return customers
