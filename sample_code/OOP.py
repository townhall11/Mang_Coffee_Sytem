# Explaining Object-Oriented Programming (OOP) to students in Python requires simplicity and practical examples they can relate to. 
# Here's how to break it down:

# 1. Start with a Simple Analogy
# Use an analogy they can easily understand, such as "Objects in Real Life."

# Example:
# A car is an object. It has:
# Attributes (properties): color, brand, speed, etc.
# Methods (actions): drive, stop, honk, etc.
# A car's design (blueprint) is like a class in programming. When you create a specific car (e.g., a red Toyota), that's like creating an object from the class.

# 2. Explain the Basic Terms
# Use a simple Python example for each term:

# a. Class:
# A class is a blueprint for creating objects.

class Car:
    def __init__(self, brand, color):
        self.brand = brand  # Attribute
        self.color = color  # Attribute

    def drive(self):  # Method
        print(f"The {self.color} {self.brand} is driving.")

# b. Object:
# An object is an instance of a class.

# Create objects from the Car class
car1 = Car("Toyota", "red")
car2 = Car("Honda", "blue")

# Access methods and attributes
car1.drive()  # Output: The red Toyota is driving.
car2.drive()  # Output: The blue Honda is driving.

# 3. Demonstrate the Four Principles of OOP
# Keep it simple and use relatable examples.


# A. Encapsulation (Data Hiding)
# Wrap data (attributes) and methods into a single unit (class). Use private attributes to control access.

class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.__balance = balance  # Private attribute

    def deposit(self, amount):
        self.__balance += amount

    def get_balance(self):
        return self.__balance

# Usage
account = BankAccount("Alice", 1000)
account.deposit(500)
print(account.get_balance())  # Output: 1500

# B. Abstraction (Hiding Details)
# Focus on what an object does, not how it does it.

from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def sound(self):
        pass

class Dog(Animal):
    def sound(self):
        return "Woof!"

class Cat(Animal):
    def sound(self):
        return "Meow!"

# Usage
animals = [Dog(), Cat()]
for animal in animals:
    print(animal.sound())

# C. Inheritance (Code Reusability)
# A child class can inherit attributes and methods from a parent class.

class Vehicle:
    def __init__(self, brand):
        self.brand = brand

    def start(self):
        print(f"{self.brand} is starting.")

class Car(Vehicle):
    def drive(self):
        print(f"{self.brand} is driving.")

# Usage
car = Car("Toyota")
car.start()  # Output: Toyota is starting.
car.drive()  # Output: Toyota is driving.

# D. Polymorphism (One Name, Many Forms)
# Different objects can use the same method name but perform different actions.

class Bird:
    def fly(self):
        print("Most birds can fly.")

class Penguin(Bird):
    def fly(self):
        print("Penguins cannot fly!")

# Usage
birds = [Bird(), Penguin()]
for bird in birds:
    bird.fly()

# 4. Relate to Their Daily Lives
# Ask students to think about objects they interact with daily:

# A mobile phone: Attributes (brand, model), Methods (make calls, take pictures).
# A student: Attributes (name, age, grade), Methods (study, take exams).

# 5. Focus on Practice
# Encourage students to create simple programs using OOP:

# Create a class for a Student with attributes like name, age, and grade, and methods like study() and take_exam().
# Build a small library system:
# Class: Book (title, author, availability)
# Method: borrow(), return_book()

# 6. Summarize Key Takeaways
# A class is a blueprint.
# An object is an instance of a class.
# Use encapsulation to protect data, abstraction to focus on essential features, inheritance to reuse code, and polymorphism to perform tasks differently with the same method.