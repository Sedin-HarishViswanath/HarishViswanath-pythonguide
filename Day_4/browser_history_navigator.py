from collections import deque

class Browser:
    def __init__(self):
        self.back_stack   = []     
        self.fwd_stack    = [] 
        self.history_log  = deque() 
        self.current      = None

    def visit(self, url: str) -> None:
        if self.current:
            self.back_stack.append(self.current)

        self.current   = url
        self.fwd_stack.clear()
        self.history_log.append(url)
        print(f"Visiting:  {url}")

    def back(self) -> None:
        if not self.back_stack:
            print("Nothing to go back to.")
            return
        self.fwd_stack.append(self.current)
        self.current = self.back_stack.pop()
        print(f"Back:{self.current}")

    def forward(self) -> None:
        if not self.fwd_stack:
            print("Nothing to go forward to.")
            return
        self.back_stack.append(self.current)
        self.current = self.fwd_stack.pop()
        print(f"Forward:   {self.current}")

    def show_history(self) -> None:
        if not self.history_log:
            print("No history yet.")
            return
        print("\nFull history (chronological):")
        for i, url in enumerate(self.history_log, 1):
            marker = "current" if url == self.current else ""
            print(f"  {i:>3}. {url}{marker}")
        print()

    def search_history(self, keyword: str) -> list:
        return [url for url in self.history_log if keyword.lower() in url.lower()]


MENU = """
Commands:
  v <url>       - visit url
  b             - back
  f             - forward
  h             - show full history
  s <keyword>   - search history
  x             - exit
"""

if __name__ == "__main__":
    browser = Browser()

    for url in ["https://google.com", "https://github.com", "https://docs.python.org"]:
        browser.visit(url)

    print(f"\nCurrent: {browser.current}")
    print(MENU)

    while True:
        raw = input(">> ").strip()
        if not raw:
            continue

        parts = raw.split(maxsplit=1)
        cmd   = parts[0].lower()

        if cmd == "v" and len(parts) == 2:
            browser.visit(parts[1].strip())

        elif cmd == "b":
            browser.back()

        elif cmd == "f":
            browser.forward()

        elif cmd == "h":
            browser.show_history()

        elif cmd == "s" and len(parts) == 2:
            results = browser.search_history(parts[1].strip())
            if results:
                print(f"Found {len(results)} match(es):")
                for url in results:
                    print(f"  {url}")
            else:
                print("No matches found.")

        elif cmd == "x":
            break
        else:
            print(MENU)