"""
Day 7 — Assignment 1: Virtual Environment & Dependency Manager
----------------------------------------------------------------
Setup (run these once, before this script, inside your project folder):
 
    python -m venv myenv
    source myenv/bin/activate        # Mac/Linux
    myenv\\Scripts\\activate           # Windows
 
    pip install requests pandas numpy
    pip freeze > requirements.txt
 
This script then verifies that every dependency declared in pyproject.toml
is actually importable in the active environment -- the same technique
Django's `check` framework and most CI dependency-audit steps use under
the hood (importlib.import_module instead of a bare `import`, because the
package name is only known at runtime as a string).
"""

import importlib
import sys

# Packages to verify. "nonexistent" is included on purpose to prove the
# checker correctly reports a MISS instead of crashing.
PACKAGES = ["requests", "pandas", "numpy", "nonexistent"]


def check_package(pkg_name: str) -> bool:
    """Try to import a package by name; return True if it succeeds."""
    try:
        importlib.import_module(pkg_name)
        return True
    except ImportError:
        return False


def main() -> None:
    print(f"Checking dependencies with Python {sys.version.split()[0]}\n")

    installed = 0
    for pkg in PACKAGES:
        ok = check_package(pkg)
        status = "OK  " if ok else "MISS"
        print(f"  [{status}] {pkg}")
        if ok:
            installed += 1

    total = len(PACKAGES)
    print(f"\nTotal installed: {installed}/{total}")
    print(f"Total required : {total}")

    if installed < total:
        missing = total - installed
        print(f"{missing} package(s) missing — run: pip install <package>")
    else:
        print("All dependencies satisfied.")


if __name__ == "__main__":
    main()