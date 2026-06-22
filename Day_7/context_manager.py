"""
Day 7 — Assignment 3: Context Manager — Resource Handler
-------------------------------------------------------------
Implements the context manager protocol two different ways:

  1. FileHandler       -- class-based, __enter__ / __exit__
  2. db_connection      -- generator-based, via @contextmanager

Both guarantee cleanup runs even if an exception is raised inside the
`with` block. This is exactly the mechanism behind `with open(...)` and
Django's `transaction.atomic()`.

Bonus: a Timer context manager that prints how long any `with` block took.
"""

import time
from contextlib import contextmanager


class FileHandler:
    """Class-based context manager for safe file handling."""

    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
        if exc_type:
            print(f"  Error handled: {exc_val}")
        return True  # suppress exception, cleanup already happened


@contextmanager
def db_connection(db_name):
    """Generator-based context manager simulating a DB connection."""
    conn = {"db": db_name, "status": "open"}
    print(f"  Connection to '{db_name}' opened")
    try:
        yield conn
    finally:
        conn["status"] = "closed"
        print("  Connection closed")


@contextmanager
def timer():
    """Bonus: prints execution time of any `with` block."""
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"  ⏱ Block took {elapsed:.4f} seconds")


def demo_file_handler():
    print("1) FileHandler — normal write/read")
    with FileHandler("demo.txt", "w") as f:
        f.write("Hello from Day 7 assignment 3\n")

    with FileHandler("demo.txt", "r") as f:
        print(f"  Read back: {f.read().strip()}")

    print("\n2) FileHandler — deliberately raise an exception")
    with FileHandler("demo.txt", "r") as f:
        # This will raise NameError, but __exit__ still closes the file
        # and suppresses the crash because it returns True.
        undefined_variable  # noqa: F821
    print("  Program continued — exception was suppressed, file was closed")


def demo_db_connection():
    print("\n3) db_connection — normal use")
    with db_connection("freelancer_saas") as conn:
        print(f"  Using connection: {conn}")

    print("\n4) db_connection — exception inside block (cleanup still runs)")
    try:
        with db_connection("freelancer_saas") as conn:
            raise ValueError("Simulated query failure")
    except ValueError as e:
        print(f"  Caught outside: {e}")
        print("  (Connection was still closed before the exception propagated)")


def demo_timer():
    print("\n5) Bonus Timer context manager")
    with timer():
        total = sum(x**2 for x in range(1_000_000))
    print(f"  (computed sum = {total})")


def main():
    demo_file_handler()
    demo_db_connection()
    demo_timer()


if __name__ == "__main__":
    main()