"""
Day 9 — Assignment 1: Fully Type-Annotated Banking API
typing • dataclass • mypy

Rewrite of the Day 6 BankAccount with full static type annotations:
  Optional[str]                 -> Bank.find(acc_num)
  List[Transaction]             -> BankAccount.transactions, mini_statement()
  Dict[str, BankAccount]        -> Bank.accounts
  Callable[[Transaction], None] -> BankAccount listeners (audit hook)

Run: python3 -m mypy assignment1.py --strict
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List, Optional


@dataclass
class Transaction:
    """@dataclass auto-generates __init__, __repr__, __eq__ for us."""
    type: str
    amount: float
    balance: float
    note: Optional[str] = None

    def __str__(self) -> str:
        tag = f" ({self.note})" if self.note else ""
        return f"{self.type:<10} ₹{self.amount:>9.2f}  bal=₹{self.balance:>10.2f}{tag}"

class InsufficientFundsError(Exception):
    """Raised when a withdrawal would overdraw the account."""


class BankAccount:
    def __init__(self, holder: str, acc_num: str, balance: float = 0.0) -> None:
        self.holder: str = holder
        self.acc_num: str = acc_num
        self.balance: float = balance
        self.transactions: List[Transaction] = []
        self._listeners: List[Callable[[Transaction], None]] = []

    def add_listener(self, callback: Callable[[Transaction], None]) -> None:
        """Register a hook that fires on every transaction (logging, notifications, etc.)."""
        self._listeners.append(callback)

    def _record(self, type_: str, amount: float, note: Optional[str] = None) -> Transaction:
        txn = Transaction(type=type_, amount=amount, balance=self.balance, note=note)
        self.transactions.append(txn)
        for listener in self._listeners:
            listener(txn)
        return txn

    def deposit(self, amount: float, note: Optional[str] = None) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
        self._record("DEPOSIT", amount, note)

    def withdraw(self, amount: float, note: Optional[str] = None) -> bool:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            return False
        self.balance -= amount
        self._record("WITHDRAW", amount, note)
        return True

    def mini_statement(self, last_n: int = 5) -> List[str]:
        recent = self.transactions[-last_n:]
        return [str(txn) for txn in recent]

    def __repr__(self) -> str:
        return f"BankAccount(holder={self.holder!r}, acc_num={self.acc_num!r}, balance={self.balance:.2f})"


class Bank:
    """Manages multiple accounts — this is where Dict[str, BankAccount] earns its keep."""

    def __init__(self, name: str) -> None:
        self.name: str = name
        self.accounts: Dict[str, BankAccount] = {}

    def open_account(self, holder: str, acc_num: str, balance: float = 0.0) -> BankAccount:
        if acc_num in self.accounts:
            raise ValueError(f"Account {acc_num} already exists")
        account = BankAccount(holder, acc_num, balance)
        self.accounts[acc_num] = account
        return account

    def find(self, acc_num: Optional[str]) -> Optional[BankAccount]:
        """Optional in, Optional out — a missing or None acc_num just means 'not found'."""
        if acc_num is None:
            return None
        return self.accounts.get(acc_num)

    def transfer(self, from_acc: str, to_acc: str, amount: float) -> bool:
        source = self.find(from_acc)
        dest = self.find(to_acc)
        if source is None or dest is None:
            return False
        if not source.withdraw(amount, note=f"transfer to {to_acc}"):
            return False
        dest.deposit(amount, note=f"transfer from {from_acc}")
        return True

    def total_assets(self) -> float:
        return sum(acc.balance for acc in self.accounts.values())


def audit_logger(txn: Transaction) -> None:
    """Example Callable[[Transaction], None] passed into add_listener."""
    print(f"  [AUDIT] {txn}")


def main() -> None:
    bank = Bank("Chennai Cooperative Bank")

    alice = bank.open_account("Alice", "ACC001", balance=5000.0)
    bob = bank.open_account("Bob", "ACC002", balance=1500.0)

    alice.add_listener(audit_logger)

    alice.deposit(2000.0, note="salary")
    alice.withdraw(500.0, note="groceries")
    bank.transfer("ACC001", "ACC002", 1000.0)

    print("\nAlice mini statement:")
    for line in alice.mini_statement():
        print(" ", line)

    print("\nBob mini statement:")
    for line in bob.mini_statement():
        print(" ", line)

    missing = bank.find("ACC999")
    print(f"\nLookup missing account -> {missing}")

    print(f"\nTotal bank assets: ₹{bank.total_assets():.2f}")


if __name__ == "__main__":
    main()