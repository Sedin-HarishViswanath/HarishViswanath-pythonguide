import time
import random

# ─────────────────────────────────────────────
#  Sample Flipkart / Amazon product catalog
# ─────────────────────────────────────────────
products = [
    {"name": "boAt Rockerz 450",        "price": 1299},
    {"name": "Redmi Buds 4",            "price": 1799},
    {"name": "Noise ColorFit Pro 4",    "price": 2499},
    {"name": "OnePlus Nord Buds 2",     "price": 2999},
    {"name": "boAt Airdopes 141",       "price": 3499},
    {"name": "Realme Watch 3",          "price": 3999},
    {"name": "Samsung Galaxy Buds FE",  "price": 4999},
    {"name": "Mi Smart Band 7 Pro",     "price": 6499},
    {"name": "OnePlus Watch 2R",        "price": 8999},
    {"name": "Apple AirPods (3rd Gen)", "price": 14900},
    {"name": "Samsung Galaxy Watch 6",  "price": 22999},
    {"name": "Apple Watch SE (2nd Gen)","price": 29900},
    {"name": "Apple AirPods Pro 2",     "price": 24900},
    {"name": "Sony WH-1000XM5",         "price": 26990},
    {"name": "Apple Watch Series 9",    "price": 41900},
]

# Keep a sorted price list; products list is already sorted by price.
prices = sorted(p["price"] for p in products)


# ─────────────────────────────────────────────
#  Binary Search — exact match, O(log n)
# ─────────────────────────────────────────────
def binary_search(prices: list[int], target: int) -> int:
    """Return index of target in prices, or -1 if not found."""
    left, right = 0, len(prices) - 1
    while left <= right:
        mid = (left + right) // 2
        if prices[mid] == target:
            return mid
        elif prices[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


# ─────────────────────────────────────────────
#  Linear Search — O(n), for benchmark only
# ─────────────────────────────────────────────
def linear_search(prices: list[int], target: int) -> int:
    for i, p in enumerate(prices):
        if p == target:
            return i
    return -1


# ─────────────────────────────────────────────
#  Find Closest Price — binary search variant
# ─────────────────────────────────────────────
def find_closest(prices: list[int], target: int) -> int:
    """Return the price in the list closest to target."""
    idx = binary_search(prices, target)
    if idx != -1:
        return prices[idx]   # exact match

    # Binary search ended with left > right.
    # At this point: prices[right] < target < prices[left]
    # (clamp to valid indices)
    left, right = 0, len(prices) - 1
    lo, hi = 0, len(prices) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if prices[mid] < target:
            left = mid
            lo = mid + 1
        else:
            right = mid
            hi = mid - 1

    # Compare the two neighbours
    candidates = []
    if 0 <= left < len(prices):
        candidates.append(prices[left])
    if 0 <= right < len(prices):
        candidates.append(prices[right])

    return min(candidates, key=lambda p: abs(p - target))


# ─────────────────────────────────────────────
#  Product lookup by price
# ─────────────────────────────────────────────
def get_product(price: int) -> dict | None:
    for p in products:
        if p["price"] == price:
            return p
    return None


# ─────────────────────────────────────────────
#  Benchmark: Binary vs Linear
# ─────────────────────────────────────────────
def benchmark(n: int = 100_000) -> None:
    large_prices = sorted(random.randint(100, 1_000_000) for _ in range(n))
    targets = [random.choice(large_prices) for _ in range(1_000)]   # all guaranteed hits

    # Linear
    start = time.perf_counter()
    for t in targets:
        linear_search(large_prices, t)
    linear_time = (time.perf_counter() - start) * 1000

    # Binary
    start = time.perf_counter()
    for t in targets:
        binary_search(large_prices, t)
    binary_time = (time.perf_counter() - start) * 1000

    speedup = linear_time / binary_time if binary_time else float("inf")

    print(f"\n  Benchmark — {n:,} prices, 1,000 searches")
    print("  " + "─" * 42)
    print(f"  {'Linear Search':<20} {linear_time:>8.2f} ms")
    print(f"  {'Binary Search':<20} {binary_time:>8.2f} ms")
    print(f"  {'Speedup':<20} {speedup:>7.1f}×")
    print("  " + "─" * 42)


# ─────────────────────────────────────────────
#  Display helpers
# ─────────────────────────────────────────────
def print_catalog(prices: list[int]) -> None:
    print(f"\n  {'#':<5} {'Price (₹)':>10}   Product")
    print("  " + "─" * 52)
    for i, price in enumerate(prices):
        product = get_product(price)
        name = product["name"] if product else "—"
        print(f"  {i:<5} {price:>10,}   {name}")
    print("  " + "─" * 52)


def search_result(prices: list[int], target: int) -> None:
    idx = binary_search(prices, target)
    if idx != -1:
        product = get_product(prices[idx])
        name = product["name"] if product else "—"
        print(f"  ✔  ₹{target:,} found at index {idx}  →  {name}")
    else:
        closest = find_closest(prices, target)
        product = get_product(closest)
        name = product["name"] if product else "—"
        print(f"  ✘  ₹{target:,} not found  →  Closest: ₹{closest:,}  ({name})")


# ─────────────────────────────────────────────
#  Main
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("\n╔══════════════════════════════════════════╗")
    print("║    Flipkart / Amazon Price Finder 🔍     ║")
    print("╚══════════════════════════════════════════╝")

    print("\n  ── Sorted Price Catalog ──")
    print_catalog(prices)

    print("\n  ── Exact Match Searches ──")
    search_result(prices, 2999)    # OnePlus Nord Buds 2 — exists
    search_result(prices, 14900)   # AirPods 3rd Gen — exists
    search_result(prices, 41900)   # Apple Watch S9 — exists

    print("\n  ── Closest Price Searches (budget finder) ──")
    search_result(prices, 2000)    # between 1799 and 2499
    search_result(prices, 10000)   # between 8999 and 14900
    search_result(prices, 500)     # below minimum
    search_result(prices, 50000)   # above maximum

    print("\n  ── Step trace for binary_search(prices, 2999) ──")
    target = 2999
    left, right, step = 0, len(prices) - 1, 1
    print(f"  {'Step':<6} {'left':<6} {'right':<6} {'mid':<6} {'prices[mid]':>12}   {'Direction'}")
    print("  " + "─" * 52)
    while left <= right:
        mid = (left + right) // 2
        direction = "FOUND" if prices[mid] == target else ("→ go right" if prices[mid] < target else "← go left")
        print(f"  {step:<6} {left:<6} {right:<6} {mid:<6} {prices[mid]:>12,}   {direction}")
        if prices[mid] == target:
            break
        elif prices[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
        step += 1

    benchmark(100_000)
    benchmark(1_000_000)