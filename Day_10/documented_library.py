"""
Day 10 — Assignment 3: Documented Library — Sphinx / Google-Style Docstrings

Functions from earlier course days, each with full Google-style docstrings
(Args, Returns, Raises, Example) that also double as doctests.

Run doctests:
    python -m doctest assignment3_documented_library.py -v

Generate HTML docs:
    python -m pydoc -w assignment3_documented_library

View in terminal:
    python -c "import assignment3_documented_library; help(assignment3_documented_library)"
"""

# ─────────────────────────────────────────────────────────────────────────────
# Section 1 — Math / Fare Utilities
# ─────────────────────────────────────────────────────────────────────────────

VEHICLE_RATES: dict[str, float] = {
    "car":  20.0,
    "bike": 10.0,
    "auto": 12.0,
}


class FareCalculator:
    """Calculates cab fares for various vehicle types."""

    def calculate_fare(self, distance: float, vehicle: str) -> float:
        """Calculate cab fare by distance and vehicle type.

        Args:
            distance (float): Trip distance in km.
            vehicle (str): One of "car", "bike", or "auto".

        Returns:
            float: Calculated fare in Indian Rupees.

        Raises:
            ValueError: If vehicle type is not supported.
            ValueError: If distance is negative.

        Example:
            >>> FareCalculator().calculate_fare(10.0, "car")
            200.0
            >>> FareCalculator().calculate_fare(5.0, "bike")
            50.0
        """
        if distance < 0:
            raise ValueError(f"Distance must be non-negative, got {distance}.")
        if vehicle not in VEHICLE_RATES:
            raise ValueError(
                f"Unsupported vehicle '{vehicle}'. "
                f"Choose from: {list(VEHICLE_RATES.keys())}"
            )
        return round(distance * VEHICLE_RATES[vehicle], 2)


# ─────────────────────────────────────────────────────────────────────────────
# Section 2 — String Utilities
# ─────────────────────────────────────────────────────────────────────────────

class StringUtils:
    """Collection of string manipulation helpers."""

    def is_palindrome(self, text: str) -> bool:
        """Check whether a string reads the same forwards and backwards.

        Ignores case and non-alphanumeric characters.

        Args:
            text (str): Input string to check.

        Returns:
            bool: True if `text` is a palindrome, False otherwise.

        Raises:
            TypeError: If `text` is not a string.

        Example:
            >>> StringUtils().is_palindrome("Racecar")
            True
            >>> StringUtils().is_palindrome("hello")
            False
            >>> StringUtils().is_palindrome("A man a plan a canal Panama")
            True
        """
        if not isinstance(text, str):
            raise TypeError(f"Expected str, got {type(text).__name__}.")
        cleaned = "".join(ch.lower() for ch in text if ch.isalnum())
        return cleaned == cleaned[::-1]

    def word_frequency(self, sentence: str) -> dict[str, int]:
        """Count how many times each word appears in a sentence.

        Words are compared case-insensitively and punctuation is stripped.

        Args:
            sentence (str): Input sentence or paragraph.

        Returns:
            dict[str, int]: Mapping of word → count, sorted by frequency descending.

        Raises:
            TypeError: If `sentence` is not a string.

        Example:
            >>> StringUtils().word_frequency("the cat sat on the mat")
            {'the': 2, 'cat': 1, 'sat': 1, 'on': 1, 'mat': 1}
        """
        if not isinstance(sentence, str):
            raise TypeError(f"Expected str, got {type(sentence).__name__}.")
        freq: dict[str, int] = {}
        for word in sentence.lower().split():
            cleaned = "".join(ch for ch in word if ch.isalnum())
            if cleaned:
                freq[cleaned] = freq.get(cleaned, 0) + 1
        return dict(sorted(freq.items(), key=lambda kv: kv[1], reverse=True))

    def caesar_cipher(self, text: str, shift: int) -> str:
        """Encrypt or decrypt text using the Caesar cipher.

        Only alphabetic characters are shifted; digits and symbols are
        passed through unchanged.

        Args:
            text (str): Plaintext (or ciphertext) to process.
            shift (int): Number of positions to shift. Use a negative value
                to decrypt.

        Returns:
            str: The transformed string.

        Raises:
            TypeError: If `text` is not a string or `shift` is not an int.

        Example:
            >>> StringUtils().caesar_cipher("Hello, World!", 3)
            'Khoor, Zruog!'
            >>> StringUtils().caesar_cipher("Khoor, Zruog!", -3)
            'Hello, World!'
        """
        if not isinstance(text, str):
            raise TypeError("text must be a string.")
        if not isinstance(shift, int):
            raise TypeError("shift must be an integer.")
        result = []
        for ch in text:
            if ch.isalpha():
                base = ord("A") if ch.isupper() else ord("a")
                result.append(chr((ord(ch) - base + shift) % 26 + base))
            else:
                result.append(ch)
        return "".join(result)


# ─────────────────────────────────────────────────────────────────────────────
# Section 3 — Grade Utilities (standalone, no CSV I/O)
# ─────────────────────────────────────────────────────────────────────────────

class GradeUtils:
    """Helper functions for computing student grades and statistics."""

    def letter_grade(self, percentage: float) -> str:
        """Convert a numeric percentage to a letter grade.

        Grading scale:
            90–100 → A+, 80–89 → A, 70–79 → B,
            60–69 → C, 50–59 → D, below 50 → F.

        Args:
            percentage (float): Score percentage between 0 and 100.

        Returns:
            str: Letter grade string.

        Raises:
            ValueError: If percentage is outside the range 0–100.

        Example:
            >>> GradeUtils().letter_grade(95)
            'A+'
            >>> GradeUtils().letter_grade(73)
            'B'
            >>> GradeUtils().letter_grade(45)
            'F'
        """
        if not (0 <= percentage <= 100):
            raise ValueError(f"Percentage must be 0–100, got {percentage}.")
        thresholds = [(90, "A+"), (80, "A"), (70, "B"), (60, "C"), (50, "D")]
        for threshold, grade in thresholds:
            if percentage >= threshold:
                return grade
        return "F"

    def class_average(self, scores: list[float]) -> float:
        """Compute the arithmetic mean of a list of scores.

        Args:
            scores (list[float]): Non-empty list of numeric scores.

        Returns:
            float: Mean score rounded to 2 decimal places.

        Raises:
            ValueError: If `scores` is empty.
            TypeError: If any element in `scores` is not numeric.

        Example:
            >>> GradeUtils().class_average([80, 90, 70])
            80.0
            >>> GradeUtils().class_average([55, 65, 75, 85])
            70.0
        """
        if not scores:
            raise ValueError("scores list must not be empty.")
        for s in scores:
            if not isinstance(s, (int, float)):
                raise TypeError(f"All scores must be numeric, found {type(s).__name__}.")
        return round(sum(scores) / len(scores), 2)

    def top_scorers(self, score_map: dict[str, float], n: int = 3) -> list[tuple[str, float]]:
        """Return the top-n students by score.

        Args:
            score_map (dict[str, float]): Mapping of student name → score.
            n (int): Number of top scorers to return. Defaults to 3.

        Returns:
            list[tuple[str, float]]: Sorted list of (name, score) tuples,
                highest score first.

        Raises:
            ValueError: If `n` is less than 1.

        Example:
            >>> GradeUtils().top_scorers({"Arjun": 88, "Meera": 95, "Karthik": 72}, n=2)
            [('Meera', 95), ('Arjun', 88)]
        """
        if n < 1:
            raise ValueError(f"n must be at least 1, got {n}.")
        return sorted(score_map.items(), key=lambda kv: kv[1], reverse=True)[:n]


# ─────────────────────────────────────────────────────────────────────────────
# Section 4 — Temperature Converter
# ─────────────────────────────────────────────────────────────────────────────

class TemperatureConverter:
    """Converts temperatures between Celsius, Fahrenheit, and Kelvin."""

    def celsius_to_fahrenheit(self, celsius: float) -> float:
        """Convert Celsius to Fahrenheit.

        Args:
            celsius (float): Temperature in degrees Celsius.

        Returns:
            float: Equivalent temperature in Fahrenheit.

        Raises:
            ValueError: If celsius is below absolute zero (−273.15 °C).

        Example:
            >>> TemperatureConverter().celsius_to_fahrenheit(0)
            32.0
            >>> TemperatureConverter().celsius_to_fahrenheit(100)
            212.0
        """
        if celsius < -273.15:
            raise ValueError(f"Temperature below absolute zero: {celsius} °C.")
        return round(celsius * 9 / 5 + 32, 2)

    def fahrenheit_to_celsius(self, fahrenheit: float) -> float:
        """Convert Fahrenheit to Celsius.

        Args:
            fahrenheit (float): Temperature in degrees Fahrenheit.

        Returns:
            float: Equivalent temperature in Celsius.

        Raises:
            ValueError: If fahrenheit is below absolute zero (−459.67 °F).

        Example:
            >>> TemperatureConverter().fahrenheit_to_celsius(32)
            0.0
            >>> TemperatureConverter().fahrenheit_to_celsius(212)
            100.0
        """
        if fahrenheit < -459.67:
            raise ValueError(f"Temperature below absolute zero: {fahrenheit} °F.")
        return round((fahrenheit - 32) * 5 / 9, 2)

    def celsius_to_kelvin(self, celsius: float) -> float:
        """Convert Celsius to Kelvin.

        Args:
            celsius (float): Temperature in degrees Celsius.

        Returns:
            float: Equivalent temperature in Kelvin.

        Raises:
            ValueError: If celsius is below absolute zero (−273.15 °C).

        Example:
            >>> TemperatureConverter().celsius_to_kelvin(0)
            273.15
            >>> TemperatureConverter().celsius_to_kelvin(100)
            373.15
        """
        if celsius < -273.15:
            raise ValueError(f"Temperature below absolute zero: {celsius} °C.")
        return round(celsius + 273.15, 2)


# ─────────────────────────────────────────────────────────────────────────────
# Entry point — run all doctests inline
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import doctest
    results = doctest.testmod(verbose=True)
    if results.failed == 0:
        print(f"\n✓ All {results.attempted} doctests passed.")
    else:
        print(f"\n✗ {results.failed}/{results.attempted} doctests FAILED.")