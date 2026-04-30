"""
Laboratory work #1 (Variant 18)
Program: Notebook (CSV and Pickle serialization)
Version: 1.0
Developer: Your Name
Date: 2026-04-27

The program manages a notebook with friends' data:
- full name (surname and initials),
- birth day, birth month, birth year.
It allows:
- saving data to CSV and Pickle files,
- reading data from files,
- searching and sorting,
- printing friends who will turn a given age this year.
Classes: Person, Notebook.
Demonstrates: static/class attributes, properties, getters/setters,
magic methods, mixins, inheritance, polymorphism.
"""

import csv
import pickle
import os
from datetime import date
from abc import ABC, abstractmethod


class LogMixin:
    """Mixin that adds logging capability to any class."""
    def log(self, message):
        print(f"[LOG] {self.__class__.__name__}: {message}")

class Serializer(ABC):
    @abstractmethod
    def save(self, data, filepath):
        pass

    @abstractmethod
    def load(self, filepath):
        pass

# ---- Person class ----
class Person(LogMixin):
    """
    Represents a contact person with full name, birth day, month, year.
    Provides property for full name, validation of inputs.
    """
    _total_persons = 0           # static attribute (class level)

    def __init__(self, full_name: str, day: int, month: int, year: int):
        self._full_name = full_name
        self._day = day
        self._month = month
        self._year = year
        Person._total_persons += 1
        self.log(f"New person created: {full_name}")

    @property
    def full_name(self):
        """Getter for full name."""
        return self._full_name

    @full_name.setter
    def full_name(self, value):
        if not value or len(value.strip()) == 0:
            raise ValueError("Name cannot be empty")
        self._full_name = value.strip()

    @property
    def birth_day(self):
        return self._day

    @birth_day.setter
    def birth_day(self, value):
        if not 1 <= value <= 31:
            raise ValueError("Day must be between 1 and 31")
        self._day = value

    @property
    def birth_month(self):
        return self._month

    @birth_month.setter
    def birth_month(self, value):
        if not 1 <= value <= 12:
            raise ValueError("Month must be between 1 and 12")
        self._month = value

    @property
    def birth_year(self):
        return self._year

    @birth_year.setter
    def birth_year(self, value):
        if value < 1900 or value > date.today().year:
            raise ValueError("Invalid birth year")
        self._year = value

    @classmethod
    def get_total_persons(cls):
        return cls._total_persons

    def age_this_year(self, current_year=None):
        """Return how old the person will become this year."""
        if current_year is None:
            current_year = date.today().year
        return current_year - self._year

    def __str__(self):
        return f"{self._full_name} ({self._day:02d}.{self._month:02d}.{self._year})"

    def __repr__(self):
        return f"Person(full_name='{self._full_name}', day={self._day}, month={self._month}, year={self._year})"

    def to_dict(self):
        return {
            "full_name": self._full_name,
            "day": self._day,
            "month": self._month,
            "year": self._year
        }

    @staticmethod
    def from_dict(data):
        return Person(data["full_name"], data["day"], data["month"], data["year"])

class CSVSerializer(Serializer):
    def save(self, data, filepath):
        """Save list of Person objects to CSV file."""
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["full_name", "day", "month", "year"])
            writer.writeheader()
            for person in data:
                writer.writerow(person.to_dict())
        print(f"Data saved to {filepath} (CSV)")

    def load(self, filepath):
        """Load list of Person objects from CSV file."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"CSV file {filepath} not found")
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return [Person.from_dict(row) for row in reader]

class PickleSerializer(Serializer):
    def save(self, data, filepath):
        """Save list of Person objects to Pickle file."""
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
        print(f"Data saved to {filepath} (Pickle)")

    def load(self, filepath):
        """Load list of Person objects from Pickle file."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Pickle file {filepath} not found")
        with open(filepath, 'rb') as f:
            return pickle.load(f)

class Notebook:
    """Represents a collection of Person contacts with operations."""
    def __init__(self):
        self._persons = []

    def add_person(self, person):
        self._persons.append(person)

    def remove_person(self, full_name):
        self._persons = [p for p in self._persons if p.full_name != full_name]

    def get_all(self):
        return self._persons

    def find_by_age_this_year(self, target_age):
        """Return list of persons whose age this year equals target_age."""
        current_year = date.today().year
        return [p for p in self._persons if p.age_this_year(current_year) == target_age]

    def sort_by_surname(self):
        """Sort persons by surname (first word of full name)."""
        self._persons.sort(key=lambda p: p.full_name.split()[0].lower())

    def sort_by_birth_date(self):
        """Sort persons by birth date (year, month, day)."""
        self._persons.sort(key=lambda p: (p.birth_year, p.birth_month, p.birth_day))

    def search_by_name(self, query):
        """Search persons whose full name contains query (case-insensitive)."""
        return [p for p in self._persons if query.lower() in p.full_name.lower()]

    def __len__(self):
        return len(self._persons)

    def __str__(self):
        return "\n".join(str(p) for p in self._persons)

def input_person():
    """Input person data from user with validation loop."""
    while True:
        try:
            name = input("Enter full name (surname and initials): ").strip()
            if not name:
                raise ValueError("Name cannot be empty")
            day = int(input("Birth day (1-31): "))
            month = int(input("Birth month (1-12): "))
            year = int(input("Birth year (1900-current): "))
            return Person(name, day, month, year)
        except ValueError as e:
            print(f"Error: {e}. Please try again.")

def run_task1_demo():
    """Interactive demonstration of notebook operations."""
    notebook = Notebook()
    
    sample = [
        Person("Ivanov I.I.", 15, 5, 2005),
        Person("Petrov P.P.", 20, 3, 2004),
        Person("Sidorov S.S.", 10, 12, 2006),
        Person("Kuznetsov K.K.", 25, 7, 2005)
    ]
    for p in sample:
        notebook.add_person(p)

    print("\n--- Notebook: Friends Age This Year ---")
    while True:
        print("\nOptions:")
        print("1. Show all")
        print("2. Add person")
        print("3. Find by age this year")
        print("4. Search by name")
        print("5. Sort by surname")
        print("6. Save to CSV")
        print("7. Load from CSV")
        print("8. Save to Pickle")
        print("9. Load from Pickle")
        print("0. Return to main menu")
        choice = input("Choice: ")
        if choice == '1':
            print("\n".join(str(p) for p in notebook.get_all()) or "Empty")
        elif choice == '2':
            notebook.add_person(input_person())
        elif choice == '3':
            try:
                age = int(input("Enter age: "))
                res = notebook.find_by_age_this_year(age)
                print(f"Friends turning {age} this year:")
                for p in res:
                    print(p)
                if not res:
                    print("None")
            except ValueError:
                print("Invalid age")
        elif choice == '4':
            query = input("Search by name: ")
            res = notebook.search_by_name(query)
            for p in res:
                print(p)
            if not res:
                print("Not found")
        elif choice == '5':
            notebook.sort_by_surname()
            print("Sorted.")
        elif choice == '6':
            csv_ser = CSVSerializer()
            csv_ser.save(notebook.get_all(), "notebook.csv")
        elif choice == '7':
            csv_ser = CSVSerializer()
            try:
                notebook._persons = csv_ser.load("notebook.csv")
                print("Loaded from CSV")
            except Exception as e:
                print(f"Error: {e}")
        elif choice == '8':
            pickle_ser = PickleSerializer()
            pickle_ser.save(notebook.get_all(), "notebook.pkl")
        elif choice == '9':
            pickle_ser = PickleSerializer()
            try:
                notebook._persons = pickle_ser.load("notebook.pkl")
                print("Loaded from Pickle")
            except Exception as e:
                print(f"Error: {e}")
        elif choice == '0':
            break
        else:
            print("Invalid choice")