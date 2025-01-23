# 3. Inheritance
# Inheritance allows one class (child) to inherit the properties and methods of another class (parent). It helps promote code reuse.

# Key Idea: Use the parent class to define common behavior and child classes to extend or override it.
# Example:

class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        pass  # To be implemented by subclasses

class Dog(Animal):
    def speak(self):
        return f"{self.name} says Woof!"

class Cat(Animal):
    def speak(self):
        return f"{self.name} says Meow!"

# Usage
dog = Dog("Buddy")
cat = Cat("Kitty")

print(dog.speak())
print(cat.speak())
