class Student:
    def __init__(self, name: str, roll_no: int):
        self.__name = name
        self.__roll_no = roll_no
        self.__marks = {}  # private dictionary

    # Read-only property
    @property
    def name(self):
        return self.__name

    # Add marks with validation
    def add_marks(self, subject: str, marks: int):
        if subject in self.__marks:
            raise ValueError(f"Marks for '{subject}' already entered.")

        if not (0 <= marks <= 100):
            raise ValueError("Marks must be between 0 and 100.")

        self.__marks[subject] = marks

    # Read-only percentage property
    @property
    def percentage(self) -> float:
        if not self.__marks:
            return 0.0

        total = sum(self.__marks.values())
        return round(total / len(self.__marks), 2)

    # Read-only grade property
    @property
    def grade(self) -> str:
        p = self.percentage

        if p >= 90:
            return "A+"
        elif p >= 80:
            return "A"
        elif p >= 70:
            return "B"
        elif p >= 60:
            return "C"
        elif p >= 50:
            return "D"
        else:
            return "F"

    # Bonus: compare students by percentage
    def __gt__(self, other):
        return self.percentage > other.percentage

    def __str__(self):
        return (
            f"Name: {self.__name}\n"
            f"Roll No: {self.__roll_no}\n"
            f"Percentage: {self.percentage}%\n"
            f"Grade: {self.grade}"
        )

s1 = Student("Harish", 101)
s1.add_marks("Maths", 95)
s1.add_marks("Science", 88)
s1.add_marks("English", 91)

s2 = Student("Rahul", 102)
s2.add_marks("Maths", 80)
s2.add_marks("Science", 78)
s2.add_marks("English", 82)

print("Student 1")
print(s1)

print("\nStudent 2")
print(s2)

print("\nComparison")
if s1 > s2:
    print(f"{s1.name} has a higher percentage.")
else:
    print(f"{s2.name} has a higher percentage.")

# Direct access not allowed
# print(s1.__marks)   # AttributeError