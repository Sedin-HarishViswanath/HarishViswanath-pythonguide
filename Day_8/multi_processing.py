"""
Day 8 — Assignment 3: Multiprocessing Image Processor
Concepts: multiprocessing.Pool, cpu_count, the GIL

Why threading would NOT help here:
This is CPU-bound work (real arithmetic, not waiting on I/O). Python's GIL
(Global Interpreter Lock) lets only one thread execute Python bytecode at a
time, even on a multi-core machine. Threads release the GIL during I/O waits
(sleep, network, disk) -- never during pure computation. So 4 threads doing
this math would still run on effectively 1 core, one at a time, plus extra
overhead from context switching. Threading would not speed this up at all.

multiprocessing sidesteps the GIL entirely by spawning separate OS processes,
each with its own Python interpreter and its own GIL. That's what lets the
work actually spread across multiple CPU cores in parallel.
"""

import multiprocessing
import time


def apply_filter(img):
    result = sum(i ** 2 for i in range(500_000))  # CPU work, not I/O
    return f"Processed: {img} checksum:{result % 9999}"


def run_single_process(images):
    start = time.time()
    results = [apply_filter(i) for i in images]
    return results, time.time() - start


def run_multi_process(images, workers):
    start = time.time()
    with multiprocessing.Pool(workers) as pool:
        results = pool.map(apply_filter, images)
    return results, time.time() - start


if __name__ == "__main__":
    images = [f"photo_{i:03d}.jpg" for i in range(1, 13)]
    cores = multiprocessing.cpu_count()
    print(f"Detected {cores} CPU core(s)\n")

    print("--- Single process ---")
    _, single = run_single_process(images)
    print(f"Single-process time: {single:.2f}s")

    print(f"\n--- Multiprocessing.Pool({cores}) ---")
    results, multi = run_multi_process(images, cores)
    for r in results:
        print(r)
    print(f"Multi-process time:  {multi:.2f}s")

    print(f"\nSpeedup: {single / multi:.2f}x  (theoretical ceiling \u2248 {cores}x;")
    print("real speedup is lower because spawning processes and pickling data")
    print("between them isn't free. On a single-core machine, multiprocessing")
    print("can even be SLOWER than single-process, since you pay process-start")
    print("overhead with no extra cores to actually use.)")