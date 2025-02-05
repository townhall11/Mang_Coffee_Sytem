# 2. Abstraction
# Abstraction is the concept of hiding unnecessary details and showing only essential information to the user. This is achieved using abstract classes or interfaces.

# Key Idea: Use abstract base classes (ABC) to enforce abstraction.
# Example:

from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def calculate_area(self):
        pass  # Abstract method

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def calculate_area(self):
        return 3.14 * self.radius ** 2

class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def calculate_area(self):
        return self.length * self.width

# Usage
circle = Circle(5)
print(f"Circle area: {circle.calculate_area()}")

rectangle = Rectangle(4, 6)
print(f"Rectangle area: {rectangle.calculate_area()}")
