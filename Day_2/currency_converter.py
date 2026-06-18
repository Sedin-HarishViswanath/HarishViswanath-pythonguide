
rates = {
    "USD": 1.00,
    "INR": 84.50,
    "EUR": 0.87,
    "GBP": 0.75,
    "JPY": 154.00,
    "AED": 3.67,
    "CAD": 1.36
}

symbols = {
    "USD": "$",
    "INR": "₹",
    "EUR": "€",
    "GBP": "£",
    "JPY": "¥",
    "AED": "د.إ",
    "CAD": "CA$"
}

print("\nAvailable currencies:")
for currency in rates:
    print(currency)

source = input("\nFrom currency: ").upper()
target = input("To currency: ").upper()
amount = float(input("Enter amount: "))

if source not in rates or target not in rates:
    print("\nInvalid currency code!")
else:
    if source == "USD":
        usd_amount = amount
    else:
        usd_amount = amount / rates[source]

    if target == "USD":
        converted_amount = usd_amount
    else:
        converted_amount = usd_amount * rates[target]

    print(f"{symbols[source]}{amount:,.2f} {source}  →  "f"{symbols[target]}{converted_amount:,.2f} {target}")

    print("=" * 40)
    print(f"Exchange rate: 1 USD = "f"{rates[target]:.4f} {target}" )
    print("Rates as of: June 2026")
    print("-" * 40)

    print(f"{symbols[source]}{amount:,.2f} {source} in all currencies:")

    for currency, rate in rates.items():
        if currency == source:
            continue

        if currency == "USD":
            value = usd_amount
        else:
            value = usd_amount * rate

        print(f"{currency}: "f"{symbols[currency]}{value:,.2f}")

    print("=" * 40)