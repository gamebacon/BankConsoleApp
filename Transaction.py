class Transaction:
    def __init__(self, id, date, amount):
        self.id = id
        self.date = date
        self.amount = int(amount)

    # Returns a string representation of the transaction.
    def __str__(self):
        return "%s | %s | %s%s kr" % (self.id, self.date, "+" if self.amount > 0 else "", self.amount)
