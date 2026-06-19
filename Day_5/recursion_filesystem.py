import os
import sys

# SECTION 1 ── FACTORIAL  (Simplest recursion pattern)

def factorial(n):
    if n==0:
        return 1
    
    return n * factorial(n-1)

    # Call stack for factorial(4):
    #   factorial(4)
    #     └─ 4 * factorial(3)
    #            └─ 3 * factorial(  2)
    #                   └─ 2 * factorial(1)
    #                          └─ 1 * factorial(0)
    #                                     └─ 1  ← base case returns
    #                          └─ 1 * 1  = 1
    #                   └─ 2 * 1  = 2
    #            └─ 3 * 2  = 6
    #     └─ 4 * 6  = 24

# SECTION 2 ── FIBONACCI WITH MEMOIZATION

fibonacci_cache={}

def fibonacci(n):
    if n==0:
        return 0
    if n==1:
        return 1
    
    if n in fibonacci_cache:
        return fibonacci_cache[n]
    
    result=fibonacci(n-1) + fibonacci(n-2)

    fibonacci_cache[n]=result
    return result

# SECTION 3 ── HELPER: FORMAT BYTES → KB / MB / GB

def format_size(byte_count):

    if byte_count < 0:
        return "0 B"
    
    elif byte_count < 1024:
        return f"{byte_count} B"
    
    elif byte_count < 1024 ** 2:
        return f"{byte_count/1024:.2f} KB"
    
    elif byte_count < 1024 ** 3:
        return f"{byte_count/(1024 ** 2):.2f} MB"
    
    else:
        return f"{byte_count/(1024 ** 3):.2f} GB"

# SECTION 4 ── FOLDER SIZE  (Core recursive logic)

def folder_size(path):

    total=0

    try:
        for entry in os.scandir(path): 

            if entry.is_file(follow_symlinks=False):
                total+=entry.stat().st_size

            elif entry.is_dir(follow_symlinks=False):

                total+=folder_size(entry.path) 

    except PermissionError:

        pass

    return total

# SECTION 5 ── PRINT TREE  (Recursive tree display)


def print_tree(path,indent=0):

    name=os.path.basename(path)
    prefix=" " * indent

    if os.path.isfile(path):
        size=os.path.getsize(path)
        print(f"{prefix} {name} ({format_size(size)})")
        return
    
    total=folder_size(path)
    print(f"{prefix} {name}/[{format_size(total)}]")

    try:
        entries=sorted(
            os.scandir(path),
            key=lambda e:(e.is_file(),e.name.lower())
            )
        
        for entry in entries:
            print_tree(entry.path,indent+1)

    except PermissionError:
        print(f"{prefix} [Permission Denied]")

def demo_factorial():
    print("=" * 25)
    for n in [0,1,2,4,6,8]:
        print(f"factorial({n:>2})={factorial(n)}")

def demo_fibonacci():
    print("=" * 25)
    sequence=[fibonacci(i) for i in range(13)]
    
    print(f"  First 13 terms : {sequence}")
    print(f"  fib(30)        = {fibonacci(30)}")
    print(f"  fib(50)        = {fibonacci(50)} ")
    print(f"  Cache entries  : {len(fibonacci_cache)}")

def demo_filesystem(target_path):
    if not os.path.exists(target_path):
        print(f"\n Path not found: {target_path}")
        return
    if not os.path.isdir(target_path):
        print(f"\n Not a directory: {target_path}")
        return
 
    abs_path = os.path.abspath(target_path)
 
    print()
    print("═" * 58)
    print("  SECTION 3 — FOLDER SIZE CALCULATOR")
    print("═" * 58)
    total_bytes = folder_size(abs_path)
    print(f"  Path  : {abs_path}")
    print(f"  Total : {format_size(total_bytes)}  ({total_bytes:,} bytes)")
 
    print()
    print("═" * 25)
    print("  SECTION 4 — DIRECTORY TREE  (recursive print)")
    print("═" * 25)
    print_tree(abs_path)

if __name__ == "__main__":
    """
    Full program flow:
    1. demo_factorial()   → shows classic base/recursive pattern
    2. demo_fibonacci()   → shows memoization benefit
    3. demo_filesystem()  → combines folder_size + print_tree
                            Uses CLI argument or defaults to "."
    """
    demo_factorial()
    demo_fibonacci()    

    target = sys.argv[1] if len(sys.argv) > 1 else "."
    demo_filesystem(target)