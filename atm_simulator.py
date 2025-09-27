from collections import deque

# --- Data Structure Implementation ---

class Node:
    """A single node in a linked list-based queue."""
    def __init__(self, data=None):
        self.data = data
        self.next = None

class Queue:
    """
    A Queue data structure implemented using a Singly Linked List.
    This ensures transactions are stored in a First-In, First-Out (FIFO) manner.
    """
    def __init__(self):
        self.head = None
        self.tail = None

    def enqueue(self, data):
        """Adds a new node with data to the end (tail) of the queue."""
        new_node = Node(data)
        if self.tail is None:
            self.head = new_node
            self.tail = new_node
            return
        self.tail.next = new_node
        self.tail = new_node

    def to_list(self):
        """Converts the queue to a standard Python list for easy display."""
        transactions = []
        current_node = self.head
        while current_node:
            transactions.append(current_node.data)
            current_node = current_node.next
        return transactions

# --- Core Application Logic ---

class Account:
    """Represents a user's bank account with a balance and transaction history."""
    def __init__(self, account_holder, account_number, initial_deposit=0.0):
        self.account_holder = account_holder
        self.account_number = account_number
        self.balance = initial_deposit
        self.transaction_history = Queue()
        if initial_deposit > 0:
            self.transaction_history.enqueue(f"Initial deposit: ${initial_deposit:.2f}")

    def deposit(self, amount):
        """Deposits funds into the account."""
        if amount > 0:
            self.balance += amount
            self.transaction_history.enqueue(f"Deposit: ${amount:.2f}")
            return True
        return False

    def withdraw(self, amount):
        """Withdraws funds from the account if the balance is sufficient."""
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.transaction_history.enqueue(f"Withdrawal: ${amount:.2f}")
            return True
        return False

    def get_balance(self):
        """Returns the current account balance."""
        return self.balance

    def get_transaction_history(self):
        """Returns the transaction history as a list."""
        return self.transaction_history.to_list()

class Bank:
    """Manages all customer accounts and account creation."""
    def __init__(self):
        self.accounts = {}
        self.next_account_number = 1001

    def create_account(self, account_holder, initial_deposit):
        """Creates a new account, assigns a unique number, and returns it."""
        account_number = self.next_account_number
        new_account = Account(account_holder, account_number, initial_deposit)
        self.accounts[account_number] = new_account
        self.next_account_number += 1
        return new_account

    def get_account(self, account_number):
        """Retrieves an account by its number."""
        return self.accounts.get(account_number)

class ATM:
    """Represents the ATM machine that interacts with the bank's accounts."""
    def __init__(self, bank):
        self.bank = bank
        self.current_account = None

    def main_menu(self):
        """Displays the main login/creation menu."""
        print("\n===== Welcome to the Bank ATM =====")
        print("1. Login to Existing Account")
        print("2. Create New Account")
        print("3. Exit")
        print("===================================")

    def transaction_menu(self):
        """Displays the transaction menu for a logged-in user."""
        print(f"\n===== ATM Menu (Logged in as {self.current_account.account_holder}) =====")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. View Transaction History")
        print("5. Logout")
        print("================================================")

    def run(self):
        """Starts the main ATM loop, handling both login and transaction states."""
        while True:
            if self.current_account is None:
                self.main_menu()
                choice = input("Please select an option (1-3): ")
                if choice == '1':
                    self.login()
                elif choice == '2':
                    self.create_new_account()
                elif choice == '3':
                    print("\nThank you for using the Bank ATM. Goodbye!")
                    break
                else:
                    print("Invalid choice. Please try again.")
            else:
                self.transaction_menu()
                choice = input("Please select an option (1-5): ")
                if choice == '1':
                    self.check_balance()
                elif choice == '2':
                    self.make_deposit()
                elif choice == '3':
                    self.make_withdrawal()
                elif choice == '4':
                    self.view_history()
                elif choice == '5':
                    self.logout()
                else:
                    print("Invalid choice. Please try again.")

    def login(self):
        try:
            acc_num = int(input("Enter your account number: "))
            account = self.bank.get_account(acc_num)
            if account:
                self.current_account = account
                print(f"\nLogin successful. Welcome, {self.current_account.account_holder}!")
            else:
                print("Error: Account not found.")
        except ValueError:
            print("Invalid input. Please enter a valid account number.")
    
    def logout(self):
        print(f"\nLogging out. Goodbye, {self.current_account.account_holder}.")
        self.current_account = None

    def create_new_account(self):
        name = input("Enter your full name: ")
        try:
            deposit = float(input("Enter initial deposit amount: $"))
            if deposit < 0:
                print("Initial deposit cannot be negative.")
                return
            new_account = self.bank.create_account(name, deposit)
            print("\nAccount created successfully!")
            print(f"Your new account number is: {new_account.account_number}")
            print("Please log in to continue.")
        except ValueError:
            print("Invalid input. Please enter a valid number for the deposit.")

    def check_balance(self):
        balance = self.current_account.get_balance()
        print(f"\nYour current balance is: ${balance:.2f}")

    def make_deposit(self):
        try:
            amount = float(input("Enter deposit amount: $"))
            if self.current_account.deposit(amount):
                print(f"Deposit of ${amount:.2f} successful.")
                self.check_balance()
            else:
                print("Invalid deposit amount. Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    def make_withdrawal(self):
        try:
            amount = float(input("Enter withdrawal amount: $"))
            if self.current_account.withdraw(amount):
                print(f"Withdrawal of ${amount:.2f} successful.")
                self.check_balance()
            else:
                print("Invalid withdrawal amount or insufficient funds.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    def view_history(self):
        history = self.current_account.get_transaction_history()
        print("\n--- Transaction History ---")
        if not history:
            print("No transactions to display.")
        else:
            for transaction in history:
                print(transaction)
        print("-----------------------")

if __name__ == "__main__":
    # Initialize the bank
    my_bank = Bank()
    
    # Pre-create a sample account for easy testing
    my_bank.create_account(account_holder="Aarush Ajay", initial_deposit=1000.0)
    print("Sample account created with Account Number: 1001")
    
    # Initialize and run the ATM with the bank
    atm_instance = ATM(bank=my_bank)
    atm_instance.run()

