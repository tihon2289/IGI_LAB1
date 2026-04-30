"""
Laboratory work #4 (Variant 18)
Program: Geometric figures – Equilateral Triangle
Version: 1.0
Developer: Your Name
Date: 2026-04-27

Implements abstract class Figure, Color class, and EquilateralTriangle.
Demonstrates inheritance, super(), property, static attributes, magic methods.
Uses matplotlib to draw and fill the triangle.
"""

from abc import ABC, abstractmethod
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Color:
    """Represents a color for a figure."""
    def __init__(self, color_name='blue'):
        self._color = color_name

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        allowed = ['blue', 'red', 'green', 'yellow', 'black', 'white', 'cyan', 'magenta']
        if value.lower() not in allowed:
            raise ValueError(f"Color must be one of {allowed}")
        self._color = value.lower()

    def __str__(self):
        return self._color

class Figure(ABC):
    """Abstract base class for all geometric figures."""
    figure_count = 0   

    def __init__(self, color: Color):
        self.color = color
        Figure.figure_count += 1

    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def draw(self, label=''):
        pass

    @classmethod
    def get_figure_count(cls):
        return cls.figure_count

class EquilateralTriangle(Figure):
    """Equilateral triangle with side length a."""
    def __init__(self, side_length, color):
        super().__init__(color)
        self._side = side_length

    @property
    def side(self):
        return self._side

    @side.setter
    def side(self, value):
        if value <= 0:
            raise ValueError("Side length must be positive")
        self._side = value

    def area(self):
        """Area of equilateral triangle: (sqrt(3)/4) * a^2."""
        return (math.sqrt(3)/4) * self._side ** 2

    def height(self):
        return (math.sqrt(3)/2) * self._side

    def __str__(self):
        return (f"Equilateral triangle, side={self._side}, "
                f"color={self.color}, area={self.area():.2f}")

    def draw(self, label=''):
        """
        Draw equilateral triangle using matplotlib.
        One side horizontal, triangle centered at (0,0).
        """
        h = self.height()

        x = [-self._side/2, self._side/2, 0]
        y = [-h/3, -h/3, 2*h/3]
        triangle = patches.Polygon(list(zip(x, y)), closed=True,
                                   facecolor=self.color.color,
                                   edgecolor='black', linewidth=2)
        fig, ax = plt.subplots()
        ax.add_patch(triangle)
        ax.set_aspect('equal')
        plt.xlim(-self._side, self._side)
        plt.ylim(-h/2, h)
        if label:
            plt.text(0, -h/3 - 0.2, label, ha='center', fontsize=12)
        plt.title(f'Equilateral Triangle (a={self._side})')
        plt.axis('off')
        filename = "triangle.png"
        plt.savefig(filename)
        plt.show()
        print(f"Figure saved as {filename}")

def run_geometry_demo():
    """Interactive geometry demo."""
    try:
        a = float(input("Enter side length of equilateral triangle: "))
        color_name = input("Enter color (blue, red, green, yellow, etc.): ")
        label = input("Enter label text: ")
    except ValueError as e:
        print(f"Invalid input: {e}")
        return

    try:
        color = Color(color_name)
        triangle = EquilateralTriangle(a, color)
        print(triangle)
        print(f"Area = {triangle.area():.3f}")
        triangle.draw(label)
    except Exception as e:
        print(f"Error: {e}")