"""
Day 10 — Assignment 1: CSV Grade Report Generator
Reads multiple subject CSVs from data/, computes totals, percentages,
grades, and writes results to output/report.csv.
"""

import csv
import glob
from pathlib import Path


GRADE_THRESHOLDS = [
    (90, "A+"),
    (80, "A"),
    (70, "B"),
    (60, "C"),
    (50, "D"),
    (0,  "F"),
]


class GradeCalculator:
    """Handles grade logic for a given percentage score."""

    def get_grade(self, percentage: float) -> str:
        """
        Return letter grade based on percentage.

        Args:
            percentage (float): Score percentage (0–100).

        Returns:
            str: Letter grade string such as "A+", "B", or "F".

        Example:
            >>> GradeCalculator().get_grade(95)
            'A+'
            >>> GradeCalculator().get_grade(45)
            'F'
        """
        for threshold, grade in GRADE_THRESHOLDS:
            if percentage >= threshold:
                return grade
        return "F"


class StudentRecord:
    """Holds aggregated marks for a single student across all subjects."""

    def __init__(self, name: str, roll_no: str):
        """
        Initialize a student record.

        Args:
            name (str): Student's full name.
            roll_no (str): Student's roll number.
        """
        self.name = name
        self.roll_no = roll_no
        self.subject_marks: dict[str, float] = {}

    def add_marks(self, subject: str, marks: float) -> None:
        """
        Add marks for a subject.

        Args:
            subject (str): Subject name (e.g. "math").
            marks (float): Marks scored in the subject.
        """
        self.subject_marks[subject] = marks

    def total(self) -> float:
        """
        Compute total marks across all subjects.

        Returns:
            float: Sum of all subject marks.

        Example:
            >>> s = StudentRecord("Ravi", "101")
            >>> s.add_marks("math", 80)
            >>> s.add_marks("science", 90)
            >>> s.total()
            170
        """
        return sum(self.subject_marks.values())

    def percentage(self, max_per_subject: float = 100) -> float:
        """
        Compute percentage based on total possible marks.

        Args:
            max_per_subject (float): Maximum marks per subject. Defaults to 100.

        Returns:
            float: Percentage rounded to 2 decimal places.

        Example:
            >>> s = StudentRecord("Ravi", "101")
            >>> s.add_marks("math", 80)
            >>> s.add_marks("science", 90)
            >>> s.percentage()
            85.0
        """
        max_total = max_per_subject * len(self.subject_marks)
        if max_total == 0:
            return 0.0
        return round((self.total() / max_total) * 100, 2)


class GradeReportGenerator:
    """
    Reads per-subject CSVs from a folder, aggregates by student,
    and writes a summary report CSV.

    Each subject CSV is expected to have columns: name, roll_no, marks.
    Output CSV columns: name, roll_no, total, percentage, grade.
    """

    def __init__(self, data_folder: str = "data", output_folder: str = "output"):
        """
        Initialize paths and ensure output folder exists.

        Args:
            data_folder (str): Folder containing subject CSV files.
            output_folder (str): Folder where the report will be saved.
        """
        self.data_folder = data_folder
        self.output_folder = Path(output_folder)
        self.output_folder.mkdir(parents=True, exist_ok=True)
        self.students: dict[str, StudentRecord] = {}
        self.grade_calc = GradeCalculator()

    def _discover_files(self) -> list[str]:
        """
        Discover all CSV files in the data folder using glob.

        Returns:
            list[str]: Sorted list of CSV file paths.

        Raises:
            FileNotFoundError: If no CSV files are found in data_folder.
        """
        pattern = f"{self.data_folder}/*.csv"
        files = sorted(glob.glob(pattern))
        if not files:
            raise FileNotFoundError(
                f"No CSV files found in '{self.data_folder}/'. "
                "Create subject CSVs with columns: name, roll_no, marks"
            )
        return files

    def _parse_subject_name(self, filepath: str) -> str:
        """
        Extract subject name from filename (stem of the path).

        Args:
            filepath (str): Full or relative path to the CSV file.

        Returns:
            str: Subject name derived from filename stem.

        Example:
            >>> gen = GradeReportGenerator()
            >>> gen._parse_subject_name("data/math.csv")
            'math'
        """
        return Path(filepath).stem

    def _load_subject_csv(self, filepath: str) -> None:
        """
        Read one subject CSV and update student records.

        Args:
            filepath (str): Path to the subject CSV file.

        Raises:
            KeyError: If required columns (name, roll_no, marks) are missing.
        """
        subject = self._parse_subject_name(filepath)
        with open(filepath, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                roll_no = row["roll_no"].strip()
                name = row["name"].strip()
                marks = float(row["marks"])

                if roll_no not in self.students:
                    self.students[roll_no] = StudentRecord(name, roll_no)
                self.students[roll_no].add_marks(subject, marks)

    def load_all(self) -> None:
        """
        Discover and load all subject CSV files from the data folder.

        Raises:
            FileNotFoundError: If no CSV files exist in data_folder.
        """
        files = self._discover_files()
        print(f"Found {len(files)} subject file(s): {[Path(f).name for f in files]}")
        for filepath in files:
            self._load_subject_csv(filepath)
        print(f"Loaded records for {len(self.students)} student(s).")

    def generate_report(self, output_filename: str = "report.csv") -> Path:
        """
        Write the aggregated grade report to output folder.

        Args:
            output_filename (str): Name of the output CSV file.

        Returns:
            Path: Full path to the written report file.

        Raises:
            ValueError: If no student data has been loaded yet.
        """
        if not self.students:
            raise ValueError("No student data loaded. Call load_all() first.")

        output_path = self.output_folder / output_filename
        fieldnames = ["name", "roll_no", "total", "percentage", "grade"]

        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for record in sorted(self.students.values(), key=lambda s: s.roll_no):
                pct = record.percentage()
                writer.writerow({
                    "name":       record.name,
                    "roll_no":    record.roll_no,
                    "total":      record.total(),
                    "percentage": pct,
                    "grade":      self.grade_calc.get_grade(pct),
                })

        print(f"Report written to: {output_path}")
        return output_path


# ── Demo / quick test ─────────────────────────────────────────────────────────

def _create_sample_data() -> None:
    """Create sample subject CSVs in data/ for a quick smoke-test."""
    Path("data").mkdir(exist_ok=True)
    subjects = {
        "hs":      [("Arjun", "101", 78), ("Meera", "102", 85), ("Karthik", "103", 60)],
        "science": [("Arjun", "101", 92), ("Meera", "102", 74), ("Karthik", "103", 55)],
        "english": [("Arjun", "101", 88), ("Meera", "102", 91), ("Karthik", "103", 70)],
        "history": [("Arjun", "101", 65), ("Meera", "102", 80), ("Karthik", "103", 48)],
        "pe":      [("Arjun", "101", 95), ("Meera", "102", 88), ("Karthik", "103", 76)],
    }
    for subject, rows in subjects.items():
        with open(f"data/{subject}.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["name", "roll_no", "marks"])
            writer.writeheader()
            for name, roll, marks in rows:
                writer.writerow({"name": name, "roll_no": roll, "marks": marks})
    print("Sample data created in data/")


if __name__ == "__main__":
    _create_sample_data()
    gen = GradeReportGenerator(data_folder="data", output_folder="output")
    gen.load_all()
    report_path = gen.generate_report()

    # Print report to console
    print("\n── Grade Report ──")
    with open(report_path, newline="") as f:
        for row in csv.DictReader(f):
            print(row)