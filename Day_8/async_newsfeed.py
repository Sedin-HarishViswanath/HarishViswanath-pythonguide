"""
Day 8 — Assignment 2: Async News Feed Fetcher
Concepts: async def, await, asyncio.gather

Why this beats threading for this use case: asyncio runs everything on a
SINGLE thread using an event loop. await asyncio.sleep(delay) hands control
back to the event loop instead of blocking, so the loop can start the next
fetch immediately. No threads, no locks, no race conditions -- just
cooperative multitasking. This is the exact model FastAPI/aiohttp use to
handle thousands of concurrent requests on one process.
"""

import asyncio
import time


async def fetch(source: str, delay: float) -> dict:
    print(f"[START] fetching {source} (~{delay}s)")
    await asyncio.sleep(delay)  # simulates network I/O, non-blocking
    print(f"[DONE]  {source}")
    return {"source": source, "headlines": [f"{source} story 1", f"{source} story 2"]}

async def main():
    sources = [("BBC", 1.5), ("Times", 2.0), ("Reuters", 1.2)]
    sequential_estimate = sum(delay for _, delay in sources)

    start = time.time()

    # asyncio.gather schedules every coroutine concurrently on the event loop
    # and waits for all of them to finish -- NOT sequential awaits.
    results = await asyncio.gather(*(fetch(src, delay) for src, delay in sources))

    elapsed = time.time() - start

    print("\n--- Results ---")
    for r in results:
        print(f"{r['source']}: {r['headlines']}")

    print(f"\nDone in {elapsed:.1f}s (vs {sequential_estimate:.1f}s sequential)")
    print(f"Speedup: {sequential_estimate / elapsed:.2f}x")

if __name__ == "__main__":
    asyncio.run(main())

