from __future__ import annotations
from dataclasses import dataclass


# ─────────────────────────────────────────────
#  Node
# ─────────────────────────────────────────────
@dataclass
class ContactNode:
    name:  str
    phone: str
    email: str
    left:  ContactNode | None = None
    right: ContactNode | None = None


# ─────────────────────────────────────────────
#  BST Contact Book
# ─────────────────────────────────────────────
class ContactBook:
    def __init__(self) -> None:
        self.root: ContactNode | None = None

    # ── Insert ────────────────────────────────
    def insert(self, name: str, phone: str, email: str) -> None:
        self.root = self._insert(self.root, name, phone, email)

    def _insert(self, node: ContactNode | None, name: str, phone: str, email: str) -> ContactNode:
        if node is None:
            return ContactNode(name, phone, email)
        if name < node.name:
            node.left = self._insert(node.left, name, phone, email)
        elif name > node.name:
            node.right = self._insert(node.right, name, phone, email)
        else:
            # Name already exists — update details
            node.phone = phone
            node.email = email
        return node

    # ── Search ────────────────────────────────
    def search(self, name: str) -> ContactNode | None:
        return self._search(self.root, name)

    def _search(self, node: ContactNode | None, name: str) -> ContactNode | None:
        if node is None:
            return None
        if name == node.name:
            return node
        return self._search(node.left if name < node.name else node.right, name)

    # ── Delete ────────────────────────────────
    def delete(self, name: str) -> None:
        self.root = self._delete(self.root, name)

    def _delete(self, node: ContactNode | None, name: str) -> ContactNode | None:
        if node is None:
            return None

        if name < node.name:
            node.left = self._delete(node.left, name)
        elif name > node.name:
            node.right = self._delete(node.right, name)
        else:
            # Case 1: leaf node
            if node.left is None and node.right is None:
                return None
            # Case 2: one child
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            # Case 3: two children — replace with inorder successor (smallest in right subtree)
            successor    = self._min_node(node.right)
            node.name    = successor.name
            node.phone   = successor.phone
            node.email   = successor.email
            node.right   = self._delete(node.right, successor.name)

        return node

    def _min_node(self, node: ContactNode) -> ContactNode:
        while node.left:
            node = node.left
        return node

    # ── List all (inorder A→Z) ────────────────
    def list_all(self) -> list[dict]:
        result: list[dict] = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node: ContactNode | None, result: list) -> None:
        if node is None:
            return
        self._inorder(node.left, result)
        result.append({"name": node.name, "phone": node.phone, "email": node.email})
        self._inorder(node.right, result)

    # ── Bonus: Height ─────────────────────────
    def height(self) -> int:
        return self._height(self.root)

    def _height(self, node: ContactNode | None) -> int:
        if node is None:
            return 0
        return 1 + max(self._height(node.left), self._height(node.right))

    # ── Bonus: Balance factor of root ─────────
    def balance(self) -> int:
        """Left height − right height. 0 = balanced, >0 = left-heavy, <0 = right-heavy."""
        if self.root is None:
            return 0
        return self._height(self.root.left) - self._height(self.root.right)


# ─────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────
def print_contacts(contacts: list[dict]) -> None:
    if not contacts:
        print("  (empty)\n")
        return
    print(f"\n  {'Name':<22} {'Phone':<18} {'Email'}")
    print("  " + "─" * 62)
    for c in contacts:
        print(f"  {c['name']:<22} {c['phone']:<18} {c['email']}")
    print("  " + "─" * 62)


def show_search(book: ContactBook, name: str) -> None:
    result = book.search(name)
    if result:
        print(f"  ✔  Found  → {result.name} | {result.phone} | {result.email}")
    else:
        print(f"  ✘  '{name}' not found in contact book")


# ─────────────────────────────────────────────
#  Main
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("\n╔══════════════════════════════════════════╗")
    print("║          BST Contact Book  📒            ║")
    print("╚══════════════════════════════════════════╝")

    book = ContactBook()

    seed_contacts = [
        ("Kohli",    "+91-9876543210", "kohli@gmail.com"),
        ("Cristiano Ronaldo",  "+91-8765432109", "Ronaldo@outlook.com"),
        ("Messi",  "+91-7654321098", "Messi@yahoo.com"),
        ("Ajith Kumar",  "+91-6543210987", "Thala@gmail.com"),
        ("Neymar",   "+91-5432109876", "Neymarjr@gmail.com"),
        ("Bala Murugan",  "+91-9123456789", "bala@gmail.com"),
    ]

    # Insert
    print("\n  ── Inserting 7 contacts ──")
    for name, phone, email in seed_contacts:
        book.insert(name, phone, email)

    print_contacts(book.list_all())
    print(f"  Tree height : {book.height()}")
    print(f"  Balance     : {book.balance()}  (left_h − right_h)\n")

    # Search
    print("  ── Search ──")
    show_search(book, "Neymar")
    show_search(book, "Vijay")

    # Update (re-insert with same name)
    print("\n  ── Update Karthik Nair's phone ──")
    book.insert("Ajith", "+91-9999999999", "ajithkumar.new@gmail.com")
    show_search(book, "Ajith kumar")

    # Delete — leaf node
    print("\n  ── Delete 'Vijay' (not present — no crash) ──")
    book.delete("Vijay")

    # Delete — node with one child / two children
    print("\n  ── Delete 'Karthik Nair' ──")
    book.delete("Ajith Kumar")

    print("\n  ── Delete 'Ravi Kumar' ──")
    book.delete("Kohli")

    print("\n  Contacts after deletions:")
    print_contacts(book.list_all())
    print(f"  Tree height : {book.height()}")
    print(f"  Balance     : {book.balance()}\n")