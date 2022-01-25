from Account import Account
from Customer import Customer
from DataSource import DataSource


# create new account id
def get_new_id(start_id, keys):
    # self.customers = {k: v for k, v in sorted(list(self.customers.items()))}
    g = list(keys)
    list.sort(g)
    id = start_id
    for existing_id in g:
        if existing_id == id:
            id += 1
        else:
            break
    return id


class Bank:

    def __init__(self):
        self.load()
        self.all_customer_accounts = {}
        for customer in self.customers.values():
            for account in customer.get_accounts().values():
                self.all_customer_accounts[account.id] = account;


    def save(self):
        self.datasource.save_all(self.customers)

    def load(self):
        self.datasource = DataSource()
        self.customers = self.datasource.get_all()

    def is_account(self, account_id):
        return self.all_customer_accounts.__contains__(account_id)


    # Returns a dictionary with all accounts
    def get_all_customer_accounts(self):
        return self.all_customer_accounts

    # Returns a list of all customers
    def get_customers(self):
        return self.customers.values()

    # Returns a specified customer
    def get_customer(self, person_number):
        return self.customers.get(person_number)

    # Change customer names
    # Returns true if successful, returns false if no customer was found
    def change_customer_name(self, new_first_name, new_last_name, person_number):
        customer = self.get_customer(person_number)
        if customer is not None:
            customer.first_name = new_first_name
            customer.last_name = new_last_name
            return True
        return False

    # Creates a new customer.
    # Returns false if the person is already a customer, true otherwise.
    def add_customer(self, first_name, last_name, person_number):
        if self.customers.get(person_number) is None:
            new_id = get_new_id(111111, self.get_customer_ids())
            new_customer = Customer(new_id, first_name, last_name, person_number, {})
            self.customers[person_number] = new_customer
            return True
        else:
            return False



    def get_customer_ids(self):
        ids = []
        for customer in self.customers.values():
            ids.append(customer.id)
        return ids


    # Removes a customer from the bank.
    # Returns account information including the total balance.
    def remove_customer(self, person_number):
        customer = self.get_customer(person_number)
        del self.customers[person_number]
        return customer.accounts_str()

    # Add account to existing customer.
    # returns newly created id. -1 if no account was created.
    def add_account(self, person_number):
        customer = self.get_customer(person_number)
        new_account_id = -1
        if customer is not None:
            new_account_id = get_new_id(1000, self.all_customer_accounts.keys())
            new_account = Account(new_account_id, "Debit konto", 0.0, [])
            customer.add_account(new_account)
            self.all_customer_accounts[new_account.id] = new_account
        return new_account_id

    # Returns a textual presentation of a specified account
    def get_account(self, person_number, account_id):
        customer = self.get_customer(person_number)
        account = customer.get_accounts()[account_id]
        return account.__str__

    # Withdraw money from a specified account
    # Returns true if successful, false if the amount wasn't available.
    def withdraw(self, person_number, account_id, amount):
        customer = self.get_customer(person_number)
        account = customer.get_account(account_id)
        if account.get_balance() - amount >= 0:
            account.withdraw(amount)
            return True
        return False

    # Withdraw money from a specified account
    # Returns true if successful
    def deposit(self, person_number, account_id, amount):
        customer = self.get_customer(person_number)
        account = customer.get_account(account_id)
        account.deposit(amount)
        return True

    # Removes the account
    # Returns a textual presentation of the removed account
    def close_account(self, person_number, account_id):
        customer = self.get_customer(person_number)
        account = customer.get_account(account_id)
        del customer.get_accounts()[account_id]
        del self.all_customer_accounts[account_id]
        return account.__str__



    # Returns all transaction history for specified account
    def get_transactions(self, person_number, account_id):
        customer = self.get_customer(person_number)
        account = customer.get_account(account_id)
        return account.get_transactions()
