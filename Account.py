from datetime import datetime

import Bank
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

    def get_transactions(self):
        return self.transactions

    # Returns a visual presentation all transactions
    def view_transactions(self):
        view = "Inga transaktioner ännu."
        if len(self.transactions) > 0:
            view = "Transaktioner\n"
            for transaction in self.transactions.values():
                view += "%s\n" % transaction.__str__()
        return view

    # Creates a new transaction
    def new_transaction(self, amount):
        transaction_id = Bank.get_new_id(1000, self.transactions)
        date = datetime.now().strftime("%Y-%m-%d %H:%M")
        transaction = Transaction(transaction_id,  date, amount)
        self.transactions[transaction_id] = transaction


