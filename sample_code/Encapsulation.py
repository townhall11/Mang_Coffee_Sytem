# 1. Encapsulation
# Encapsulation is the process of wrapping data (variables) and methods (functions) into a single unit (class). It helps restrict direct access to some of the object’s components, which is useful for security and hiding implementation details.

# Key Idea: Use private or protected variables to control access.
# Example:


class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.__balance = balance  # Private attribute

    def deposit(self, amount):
        self.__balance += amount
        print(f"{amount} deposited. New balance: {self.__balance}")

    def withdraw(self, amount):
        if amount > self.__balance:
            print("Insufficient balance!")
        else:
            self.__balance -= amount
            print(f"{amount} withdrawn. Remaining balance: {self.__balance}")

# Usage
account = BankAccount("Alice", 1000)
account.deposit(500)
account.withdraw(200)

# Accessing private attribute directly (not allowed)
# print(account.__balance)  # This will throw an error

