import time
import random

# ─────────────────────────────────────────────
#  Sample BGMI / MPL player leaderboard
# ─────────────────────────────────────────────

players = [
    {"name": "Jonathan",  "score": 5100},
    {"name": "Mavi",      "score": 4800},
    {"name": "Mortal",    "score": 4500},
    {"name": "Shroud",    "score": 4200},
    {"name": "Scout",     "score": 3800},
    {"name": "Zgod",      "score": 3600},
    {"name": "Snax",      "score": 3200},
    {"name": "Hector",    "score": 2900},
]

# ─────────────────────────────────────────────
#  Bubble Sort  —  O(n²) average, O(n) best
# ─────────────────────────────────────────────

def bubble_sort(players:list[dict])->list[dict]:
    arr=players[:]
    n=len(arr)

    for i in range(n):
        swapped=False
        for j in range(n-i-1):
            if arr[j]["score"] < arr[j+1]["score"]:
                arr[j],arr[j+1]=arr[j+1],arr[j]
                swapped=True
            if not swapped:
                break
    return arr

# ─────────────────────────────────────────────
#  Merge Sort  —  O(n log n) guaranteed
# ─────────────────────────────────────────────

def merge_sort(players:list[dict])->list[dict]:
    if len(players) <=1:
        return players[:]
    
    mid=len(players)//2
    left=merge_sort(players[:mid])
    right=merge_sort(players[mid:])

    return _merge(left,right)

def _merge(left:list,right:list)->list:
    result,i,j=[],0,0

    while i <len(left) and j < len(right):
        if left[i]["score"] >=right[j]["score"]:
            result.append(left[i])
            i+=1

        else:
            result.append(right[j])
            j+=1

    result.extend(left[i:])
    result.extend(right[j:])

    return result

# ─────────────────────────────────────────────
#  Quick Sort  —  O(n log n) avg, O(n²) worst
# ─────────────────────────────────────────────
def quick_sort(players: list[dict]) -> list[dict]:
    arr = players[:]
    _quick_sort(arr, 0, len(arr) - 1)
    return arr
 
 
def _quick_sort(arr: list, low: int, high: int) -> None:
    if low < high:
        pi = _partition(arr, low, high)
        _quick_sort(arr, low, pi - 1)
        _quick_sort(arr, pi + 1, high)
 
 
def _partition(arr: list, low: int, high: int) -> int:
    pivot = arr[high]["score"]
    i = low - 1
    for j in range(low, high):
        if arr[j]["score"] >= pivot:   # descending
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
 
 
# ─────────────────────────────────────────────
#  Bonus: Python Timsort (sorted() under the hood)
# ─────────────────────────────────────────────
def timsort(players: list[dict]) -> list[dict]:
    return sorted(players, key=lambda p: p["score"], reverse=True)
 
 
# ─────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────
def print_leaderboard(sorted_players: list[dict], title: str = "Leaderboard") -> None:
    print(f"\n  {title}")
    print("  " + "─" * 38)
    print(f"  {'Rank':<6} {'Player':<16} {'Score':>8}")
    print("  " + "─" * 38)
    for rank, p in enumerate(sorted_players, 1):
        print(f"  {rank:<6} {p['name']:<16} {p['score']:>8}")
    print("  " + "─" * 38)
 
 
def compare_sorts(dataset: list[dict], label: str) -> None:
    reference = sorted(dataset, key=lambda p: p["score"], reverse=True)
    algorithms = [
        ("Bubble Sort", bubble_sort),
        ("Merge Sort",  merge_sort),
        ("Quick Sort",  quick_sort),
        ("Timsort",     timsort),
    ]
    print(f"\n  {label}")
    print("  " + "─" * 48)
    print(f"  {'Algorithm':<14} {'Time (µs)':>12}   {'Correct':>8}")
    print("  " + "─" * 48)
    for name, fn in algorithms:
        start   = time.perf_counter()
        result  = fn(dataset)
        elapsed = (time.perf_counter() - start) * 1_000_000
        correct = [p["score"] for p in result] == [p["score"] for p in reference]
        print(f"  {name:<14} {elapsed:>11.2f}µs   {str(correct):>8}")
    print("  " + "─" * 48)
 
 
# ─────────────────────────────────────────────
#  Main
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("\n╔══════════════════════════════════════════╗")
    print("║      BGMI / MPL Leaderboard Sorter       ║")
    print("╚══════════════════════════════════════════╝")
 
    sorted_players = merge_sort(players)
    print_leaderboard(sorted_players, "Final Standings (Merge Sort)")
 
    compare_sorts(players, "Performance Comparison — 8 players")
 
    large = [
        {"name": f"Player{i}", "score": random.randint(1_000, 99_999)}
        for i in range(1_000)
    ]
    compare_sorts(large, "Performance Comparison — 1,000 players")
 
    large_10k = [
        {"name": f"Player{i}", "score": random.randint(1_000, 99_999)}
        for i in range(10_000)
    ]
    compare_sorts(large_10k, "Performance Comparison — 10,000 players")
 