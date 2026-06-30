"""
Day 7 — Assignment 2: List Comprehensions & Generator Expressions
--------------------------------------------------------------------
Five common for-loop patterns rewritten as comprehensions, plus a
generator-expression benchmark proving generators are dramatically
more memory-efficient than lists for large sequences.

Constraint check:
  - No for-loops anywhere (comprehension syntax only)
  - Task 4 uses a generator expression
  - Memory measured with sys.getsizeof()
"""

import sys

def task1_squares_of_evens():
    """Squares of even numbers from 1-100."""
    squares = [x**2 for x in range(1, 101) if x % 2 == 0]
    return squares


def task2_flatten_2d():
    """Flatten a 2D list into a 1D list."""
    matrix = [[1, 2], [3, 4], [5, 6]]
    flat = [n for row in matrix for n in row]
    return flat


def task3_filter_emails():
    """Filter a list of strings down to ones that look like valid emails."""
    data = [
        "harish@example.com",
        "not-an-email",
        "support@chennaisaas.in",
        "just text",
        "billing@company.co",
    ]
    emails = [s for s in data if "@" in s and "." in s]
    return emails


def task4_generator_sum_1m():
    """Sum 1 to 1,000,000 squared using a generator expression (no RAM spike)."""
    gen = (x**2 for x in range(1, 1_000_001))
    total = sum(gen)
    return total


def task5_discounted_prices():
    """Apply a 10% discount to a dict of prices using dict comprehension."""
    prices = {"laptop": 75000, "mouse": 800, "keyboard": 2200, "monitor": 15000}
    discounted = {k: round(v * 0.9, 2) for k, v in prices.items()}
    return discounted


def memory_comparison(n: int = 100_000):
    """Compare memory footprint of a list vs. a generator for n items."""
    lst = [x**2 for x in range(n)]
    gen = (x**2 for x in range(n))

    list_size = sys.getsizeof(lst)
    gen_size = sys.getsizeof(gen)
    ratio = list_size / gen_size

    return list_size, gen_size, ratio


def main():
    print("Task 1 — Squares of even numbers (1-100):")
    print(task1_squares_of_evens())

    print("\nTask 2 — Flatten 2D list:")
    print(task2_flatten_2d())

    print("\nTask 3 — Filter valid emails:")
    print(task3_filter_emails())

    print("\nTask 4 — Sum of squares 1 to 1,000,000 (via generator):")
    print(task4_generator_sum_1m())

    print("\nTask 5 — Prices with 10% discount:")
    print(task5_discounted_prices())

    print("\nMemory comparison — list vs generator (100,000 items):")
    list_size, gen_size, ratio = memory_comparison(100_000)
    print(f"  list size:      {list_size:>10,} bytes")
    print(f"  generator size: {gen_size:>10,} bytes")
    print(f"  → generator is ~{ratio:,.0f}x more memory efficient")


if __name__ == "__main__":
    main()