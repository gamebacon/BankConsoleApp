from datetime import datetime

from Transaction import Transaction


class Account:
    def __init__(self, id, type, balance, transactions):
        self.id = id
        self.type = type
        self.balance = balance
        self.transactions = transactions

    def __str__(self):
        return "%s | %s | %s SEK " % (self.id, self.type, self.balance)

    def withdraw(self, amount):
        self.balance -= amount
        self.new_transaction(-amount)

    def deposit(self, amount):
        self.balance += amount
        self.new_transaction(amount)

    def get_balance(self):
        return self.balance

    def get_id(self):
        return self.id

    def get_transactions(self):
        return self.transactions

    # Returns a visual presentation all transactions
    def view_transactions(self):
        view = "Inga transaktioner ännu."
        if len(self.transactions) > 0:
            view = "Transaktioner\n"
            for transaction in self.transactions:
                view += "%s\n" % transaction.__str__()
        return view

    # Creates a new transaction
    def new_transaction(self, amount):
        transaction_id = len(self.transactions) + 1;
        date = datetime.now().strftime("%Y-%m-%d %H:%M")
        transaction = Transaction(transaction_id,  date, amount)
        self.transactions.append(transaction)


