import re

from Bank import Bank


# clears screen and optionally prints message
def clear(num, msg=""):
    print(num * "\n" + msg)


# Checks if the given string is a valid person number.
def is_person_number(person_number):
    return re.fullmatch("[0-9]{12}", person_number)


# Checks if the given string is a word sequence.
def is_word(word):
    return re.fullmatch("[A-Öa-ö]{1,50}", word)


# Prompts the player with information before they can continue.
def ok(prompt=""):
    ok = input(prompt + "\n(1)Ok\n")
    # clear(50)


# Force positive int as input
def intput(prompt, badinp="%s är ej giltigt."):
    while True:
        inp = input(prompt)
        try:
            inp = int(inp)
            if inp > 0:
                return inp
        except:
            print(badinp % inp)


# Get word character input
def stringput(prompt, badinp="%s är ej giltigt."):
    while True:
        inp = input(prompt)
        if is_word(inp):
            return inp
        else:
            print(badinp % inp)


class Main:
    def __init__(self):
        self.bank = Bank()
        self.current_customer = None
        self.start_ui()
        self.bank.save()

    def start_ui(self):
        while True:
            clear(50)
            inp = input("Jag är...\n(1)Kund (2)Bank\n")
            if inp == "1":
                if self.customer_login_ui():
                    break
            elif inp == "2":
                clear(50)
                self.bank_ui()
                break
            elif inp == "0":
                break
            else:
                print("Skriv \"1\" eller \"2\". Alternativt \"0\" för att avsluta.")

    def bank_ui(self):
        while True:
            clear(50)
            inp = input("(1)Visa kunder (2)Hantera kund (3)Ny Kund (4)Avsluta\n")
            if inp is "1":
                self.bank_display_customers_ui()
            elif inp is "2":
                customer = self.get_customer_ui()
                if customer is not None:
                    self.bank_customer_ui(customer)
            elif inp is "3":
                self.bank_new_customer_ui()
            elif inp is "4":
                break

    def bank_display_customers_ui(self):
        clear(50)
        for customer in self.bank.get_customers():
            print(customer.__str__())
        print("   ID       PNR            NAMN   ")
        print("            (%d Kunder)" % len(self.bank.customers))
        ok()

    def get_customer_ui(self):
        while True:
            person_number = self.get_person_number()
            if person_number is None:
                return
            customer = self.bank.get_customer(person_number)
            if customer is None:
                print("En kund med personnummer \"%s\" hittades inte." % person_number)
                ok()
                break
            else:
                return customer

    def bank_customer_ui(self, customer):
        while True:
            print(
                "------- %s %s, %s ---------" % (customer.first_name, customer.last_name, customer.person_number))
            inp = input("(1)Kunduppgifter (2)Konton (3)Radera (4)Avbryt\n")
            if inp is "1":
                self.bank_modify_customer_ui(customer)
                clear(50)
            elif inp is "2":
                self.bank_customer_accounts_ui(customer)
            elif inp is "3":
                self.bank_remove_customer_ui(customer)
                return
            else:
                return

    def bank_modify_customer_ui(self, customer):
        while True:
            clear(50, "%s - %s, %s" % (customer.id, customer.get_full_name(), customer.person_number))
            inp = input("(1)Ändra förnamn (2)Ändra efternamn (3)Avbryt\n")
            if inp is "1":
                customer.first_name = stringput("Nytt förnamn: ")
            elif inp is "2":
                customer.last_name = stringput("Nytt efternamn: ")
            elif inp is "3":
                return

    def bank_customer_accounts_ui(self, customer):
        while True:
            clear(50)
            inp = input(customer.accounts_str() + "\n(1)Nytt konto (2)Hantera konto (3)Avbryt\n")
            if inp is "1":
                new_account_id = self.bank.add_account(customer.person_number)
                print("Ett nytt konto skapades for %s med ID %s." % (customer.get_full_name(), new_account_id))
                ok()
            elif inp is "2":
                self.bank_customer_account_ui(customer)
            elif inp is "3":
                return

    def bank_customer_account_ui(self, customer):
        account = self.get_customer_account(customer)
        if account is not None:
            while True:
                clear(50, "> %s \n" % account.__str__())
                inp = input("(1)Visa transaktioner (2)Avsluta konto (3)Avbryt\n")
                if inp is "1":
                    print(account.view_transactions())
                    ok()
                elif inp is "2":
                    if self.bank_delete_account_ui(customer, account):
                        break
                elif inp is "3":
                    return

    def bank_delete_account_ui(self, customer, account):
        if input("Ange kontonumret för att radera kontot: ") == str(account.id):
            self.bank.close_account(customer.person_number, account.id)
            ok("Kontot togs bort och du fick tillbaka %s kr" % account.balance)
            return True
        else:
            ok("Du angav fel kontonummer.")
            return False

    def bank_remove_customer_ui(self, customer):
        inp = input("Ange personnumret for att slutföra radering.\n")
        if inp == customer.person_number:
            self.bank.remove_customer(customer.person_number)
            print("Kundkontot för %s togs bort." % customer.get_full_name())
        else:
            print("Du angav fel personnummer.")
        ok()

    def bank_new_customer_ui(self):
        first_name = stringput("Ange förnamn: ")
        last_name = stringput("Ange efternamn: ")
        person_number = self.get_person_number()
        if person_number:
            if self.bank.add_customer(first_name, last_name, person_number):
                print("Ett kundkonto skapades för %s %s." % (first_name, last_name))
            else:
                print("Ett kundkonto med personnumret \"%s\" finns redan." % person_number)
        ok()

    def get_person_number(self):
        person_number = input("Ange personnummer (YYYYMMDDXXXX)\n")
        if is_person_number(person_number):
            return person_number
        else:
            ok("\"%s\" är inte ett personnummer." % person_number)
            return None

    def customer_login_ui(self):
        person_number = self.get_person_number()
        if person_number is None:
            return
        customer = self.bank.get_customer(person_number)
        if customer is None:
            print("Det fanns inget konto registrerat med personnumret \"%s\"." % person_number)
            ok()
        else:
            self.current_customer = customer
            self.customer_ui(customer)
        return customer is not None

    def customer_ui(self, customer):
        while True:
            clear(50, "Välkommen %s\n" % customer.get_full_name())
            inp = input("(1)Hantera konton (2)Avsluta\n")
            if inp == "1":
                account = self.get_customer_account(customer)
                if account is not None:
                    self.account_ui(account)
            elif inp == "2":
                return

    def withdraw_ui(self, account, amount):
        withdraw_response = self.bank.withdraw(self.current_customer.person_number, account.id, amount)
        if withdraw_response is True:
            print("\nDu har tagit ut %s kr (Resterande belopp %s SEK)" % (amount, account.balance))
        else:
            print("\nDu har inte tillräckligt med pengar på ditt konto. (%s SEK)" % account.balance)

    def deposit_ui(self, account, amount):
        deposit_response = self.bank.deposit(self.current_customer.person_number, account.id, amount)
        if deposit_response is True:
            print("\nDu har gjort en insättning på %s kr (Nuvarande belopp %s SEK)" % (amount, account.balance))
        else:
            print("\nNågot gick fel..\n")

    def account_ui(self, account):
        while True:
            clear(50)
            print("> %s\n" % account.__str__())
            inp = input("(1)Uttag (2)Insättning (3)Historik (4)Avbryt\n")
            if inp is "1" or inp is "2":
                amount = intput("Ange mängd: ")
                if inp == "1":
                    self.withdraw_ui(account, amount)
                elif inp == "2":
                    self.deposit_ui(account, amount)
            elif inp is "3":
                clear(50, account.view_transactions())
            else:
                return
            ok()

    # Returns a specified account
    def get_customer_account(self, customer):
        clear(50)
        if len(customer.get_accounts()) == 0:
            ok("Inga konton hittades.")
        else:
            print(customer.accounts_str())
            account_id = intput("Ange ett kontonummer: ")
            account = customer.get_account(account_id)

            if account is None:
                print("Ett konto med kontonummer \"%s\" hittades inte." % account_id)
                ok()
            else:
                return account


# Starts the program
Main()
