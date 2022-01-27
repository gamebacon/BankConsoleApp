class Customer:

    def __init__(self, id, first_name, last_name, person_number, accounts):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.person_number = person_number
        self.accounts = accounts

    # Returns a string representation of the customer.
    def __str__(self):
        return "%s | %s | %s %s" % (self.id, self.person_number, self.first_name, self.last_name)

    # Returns account dictionary
    # with account_id as key and the account for value
    def get_accounts(self):
        return self.accounts

    # Get a specific account
    def get_account(self, account_id):
        return self.accounts.get(account_id)

    # Add an account
    def add_account(self, account):
        self.accounts[account.id] = account

    # Returns firstname concatenated with lastname.
    def get_full_name(self):
        return self.first_name + " " + self.last_name

    # Returns the total balance from all accounts.
    def get_total_balance(self):
        total_balance = 0
        for account in self.get_accounts().values():
            total_balance += account.balance
        return total_balance

    # returns a string representation for all accounts
    def accounts_str(self):
        result = "\n------ Konton -------\n";
        for account in self.get_accounts().values():
            result += "%s\n" % account.__str__()
        result += "\nTotalt värde: %.1f SEK\n" % self.get_total_balance()
        return result
