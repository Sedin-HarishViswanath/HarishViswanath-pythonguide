"""
Day 8 — Assignment 1: Multi-threaded File Downloader
Concepts: threading.Thread, threading.Lock, concurrent.futures.ThreadPoolExecutor

Why threads work well here: downloading is I/O-bound (waiting on the network),
not CPU-bound. While a thread is inside time.sleep(), Python's GIL is released,
so other threads get to run. That's why threading gives real concurrency for
I/O-bound work, even though only one thread ever executes Python bytecode
at a time.
"""

import threading
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

files = [("report.pdf", 5), ("video.mp4", 120), ("image.jpg", 2), ("data.csv", 15)]


# ---------------------------------------------------------------------------
# Part A: raw threading.Thread + threading.Lock
# ---------------------------------------------------------------------------
def download_file(filename, size_mb, completed, lock):
    delay = random.uniform(1, 4)
    print(f"[START] {filename} ({size_mb} MB) on {threading.current_thread().name}")
    time.sleep(delay)  # simulates network latency
    with lock:  # protects the shared list from race conditions
        completed.append((filename, delay))
    print(f"[DONE]  {filename} in {delay:.1f}s")


def run_with_threads():
    completed = []
    lock = threading.Lock()

    threads = [
        threading.Thread(target=download_file, args=(f, s, completed, lock), name=f)
        for f, s in files
    ]

    start = time.time()

    # Start ALL threads first...
    for t in threads:
        t.start()

    # ...then join all. This is what gives true concurrency: every thread is
    # already sleeping simultaneously before we wait for any single one.
    for t in threads:
        t.join()

    elapsed = time.time() - start
    sequential_estimate = sum(delay for _, delay in completed)

    print("\n--- threading.Thread results ---")
    print(f"Files completed:      {[f for f, _ in completed]}")
    print(f"Wall-clock time:      {elapsed:.2f}s")
    print(f"Sequential estimate:  {sequential_estimate:.2f}s")
    print(f"Speedup:              {sequential_estimate / elapsed:.2f}x")


# ---------------------------------------------------------------------------
# Part B (Bonus): same job using concurrent.futures.ThreadPoolExecutor
# ---------------------------------------------------------------------------
def download_file_pool(filename, size_mb):
    delay = random.uniform(1, 4)
    print(f"[START] {filename} ({size_mb} MB) on {threading.current_thread().name}")
    time.sleep(delay)
    print(f"[DONE]  {filename} in {delay:.1f}s")
    return filename, delay


def run_with_threadpool(max_workers=3):
    start = time.time()
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(download_file_pool, f, s): f for f, s in files}
        for future in as_completed(futures):
            results.append(future.result())

    elapsed = time.time() - start
    sequential_estimate = sum(delay for _, delay in results)

    print(f"\n--- ThreadPoolExecutor(max_workers={max_workers}) results ---")
    print(f"Wall-clock time:      {elapsed:.2f}s")
    print(f"Sequential estimate:  {sequential_estimate:.2f}s")
    print(f"Speedup:              {sequential_estimate / elapsed:.2f}x")
    print("Note: 3 workers for 4 files means one file waits for a free slot,")
    print("so speedup is a bit lower than with 4 unrestricted threads.")


if __name__ == "__main__":
    print("=" * 60)
    print("PART A: threading.Thread + threading.Lock")
    print("=" * 60)
    run_with_threads()

    print("\n" + "=" * 60)
    print("PART B (Bonus): concurrent.futures.ThreadPoolExecutor")
    print("=" * 60)
    run_with_threadpool(max_workers=3)