from datetime import datetime

class BankAccount:
    MAX_HISTORY = 5

    def __init__(self, holder: str, acc_num: str, balance: float = 0) -> None:
        self.holder       = holder
        self.acc_num      = acc_num
        self._balance     = balance       # _ prefix = encapsulated (private by convention)
        self._transactions: list[dict] = []
        if balance > 0:
            self._record("CR", balance, note="Opening balance")

    #Public methods

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError(f"Deposit must be positive, got ₹{amount}")
        self._balance += amount
        self._record("CR", amount)

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError(f"Withdrawal must be positive, got ₹{amount}")
        if amount > self._balance:
            raise ValueError(
                f"Insufficient funds — need ₹{amount:,.2f}, have ₹{self._balance:,.2f}"
            )
        self._balance -= amount
        self._record("DR", amount)

    def get_balance(self) -> float:
        return self._balance

    def mini_statement(self) -> None:
        print(f"\n  Mini Statement  ·  {self.holder}  ·  {self.acc_num}")
        print("  " + "─" * 58)
        print(f"  {'Type':<5} {'Amount':>14}   {'Balance':>14}   {'Time'}")
        print("  " + "─" * 58)
        for txn in self._transactions:
            sign   = "+" if txn["type"] == "CR" else "-"
            note   = f"  ({txn['note']})" if txn.get("note") else ""
            print(
                f"  {txn['type']:<5} {sign}₹{txn['amount']:>12,.2f}"
                f"   ₹{txn['balance']:>12,.2f}"
                f"   {txn['time']}{note}"
            )
        print("  " + "─" * 58)
        print(f"  Current Balance: ₹{self._balance:,.2f}\n")

    #transfer between two accounts

    def transfer(self, amount: float, target: "BankAccount") -> None:
        self.withdraw(amount)                   # raises if insufficient
        target.deposit(amount)
        print(f"  ✔  Transferred ₹{amount:,.2f}  ·  {self.acc_num} → {target.acc_num}")

    # ── Private helper 

    def _record(self, txn_type: str, amount: float, note: str = "") -> None:
        self._transactions.append({
            "type":    txn_type,
            "amount":  amount,
            "balance": self._balance,
            "note":    note,
            "time":    datetime.now().strftime("%d %b %H:%M"),
        })
        # Keep only the last MAX_HISTORY entries
        if len(self._transactions) > self.MAX_HISTORY:
            self._transactions.pop(0)

    #Dunder

    def __str__(self) -> str:
        return (
            f"BankAccount(holder='{self.holder}', "
            f"acc='{self.acc_num}', "
            f"balance=₹{self._balance:,.2f})"
        )


#
#  Main — demo
# 
if __name__ == "__main__":
    print("\n ")
    print("║HDFC / SBI Bank Account System")

    ronny = BankAccount("Ronaldo",  "HDFC001", balance=5_000)
    kohli = BankAccount("Kohli",  "HDFC002", balance=2_000)

    print(ronny)
    print(kohli)

    print("\n  ── Ronny's transactions ──")
    ronny.deposit(2_000)
    ronny.withdraw(1_500)
    ronny.deposit(500)
    ronny.withdraw(200)
    ronny.deposit(3000)
    ronny.deposit(100)       # 6th entry — oldest gets dropped from history
    ronny.mini_statement()

    print("  ── Transfer: Ronny → Kohli ──")
    ronny.transfer(1_000, kohli)
    ronny.mini_statement()
    ronny.mini_statement()

    print("  ── Error handling ──")
    try:
        ronny.withdraw(999_999)
    except ValueError as e:
        print(f"  ✘  {e}")

    try:
        ronny.deposit(-500)
    except ValueError as e:
        print(f"  ✘  {e}")

    print(f"\n  {ronny}")
    print(f"  {kohli}")