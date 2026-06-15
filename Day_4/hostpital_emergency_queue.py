import heapq


class EmergencyWard:
    def __init__(self):
        self._heap    = []
        self._counter = 0    # FIFO tie-breaker for equal severity

    def admit(self, name: str, age: int, severity: int) -> None:
        """Lower severity = higher priority (1 = critical, 5 = minor)."""
        heapq.heappush(self._heap, (severity, self._counter, name, age))
        self._counter += 1
        print(f"Admitted:  {name}, Age {age}  (severity {severity})")

    def treat_next(self) -> None:
        if not self._heap:
            print("Ward is empty.")
            return
        sev, _, name, age = heapq.heappop(self._heap)
        print(f"Treating:  {name}, Age {age}  (severity {sev})")

    def bump_priority(self, name: str) -> None:
        """Worsen severity by 1 (higher number = less critical)."""
        for i, (sev, counter, n, age) in enumerate(self._heap):
            if n == name:
                self._heap[i] = (sev + 1, counter, n, age)
                heapq.heapify(self._heap)
                print(f"Priority bumped: {name}  severity {sev} -> {sev + 1}")
                return
        print(f"Patient '{name}' not found in queue.")

    def show_queue(self) -> None:
        if not self._heap:
            print("Queue is empty.")
            return
        sorted_view = sorted(self._heap)
        print(f"\n{'Severity':<10} {'Name':<18} {'Age':<6} {'Queue Order'}")
        print("-" * 48)
        for rank, (sev, _, name, age) in enumerate(sorted_view, 1):
            print(f"{sev:<10} {name:<18} {age:<6} #{rank}")
        print()


MENU = """
Commands:
  a <name> <age> <severity 1-5>  - admit patient
  t                              - treat next
  b <name>                       - bump priority (worsen by 1)
  q                              - show queue
  x                              - exit
"""

if __name__ == "__main__":
    ward = EmergencyWard()

    # preload a few patients for demo
    ward.admit("Harish",  65, 1)
    ward.admit("Ronaldo",  34, 3)
    ward.admit("Kohli",  52, 2)
    ward.admit("Messi", 28, 3)
    ward.admit("Neymar",  77, 1)
    print()
    print(MENU)

    while True:
        raw = input(">> ").strip()
        if not raw:
            continue

        parts = raw.split()
        cmd   = parts[0].lower()

        if cmd == "a" and len(parts) == 4:
            name = parts[1]
            age  = int(parts[2]) if parts[2].isdigit() else 0
            sev  = int(parts[3]) if parts[3].isdigit() else 5
            sev  = max(1, min(5, sev))
            ward.admit(name, age, sev)

        elif cmd == "t":
            ward.treat_next()

        elif cmd == "b" and len(parts) == 2:
            ward.bump_priority(parts[1])

        elif cmd == "q":
            ward.show_queue()

        elif cmd == "x":
            break
        else:
            print(MENU)