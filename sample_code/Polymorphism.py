# 4. Polymorphism
# Polymorphism allows objects to be treated as instances of their parent class rather than their actual class. It provides the ability to redefine methods for different objects.

# Key Idea: Use the same method name but different implementations.
# Example:


class Bird:
    def fly(self):
        print("Most birds can fly.")

class Sparrow(Bird):
    def fly(self):
        print("Sparrow flies at low altitudes.")

class Penguin(Bird):
    def fly(self):
        print("Penguins cannot fly!")

# Usage
birds = [Bird(), Sparrow(), Penguin()]
for bird in birds:
    bird.fly()
