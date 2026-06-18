
products = {
    1: ("Rice", 250),
    2: ("Milk", 50),
    3: ("Bread", 40),
    4: ("Eggs", 80),
    5: ("Oil", 180),
    6: ("Sugar", 60),
    7: ("Tea", 120)
}

cart = []

print("Available Products")
for pid, (item, price) in products.items():
    print(f"{pid}. {item} - ₹{price}")

while True:
    choice = int(input("\nEnter product number to add to cart (0 to finish): "))

    if choice == 0:
        break

    if choice in products:
        cart.append(choice)
        print(f"{products[choice][0]} added to cart")
    else:
        print("Invalid product number")

total = 0

print("\n========== BILL ==========")

for item in cart:
    name, price = products[item]
    total += price
    print(f"{name:<15} ₹{price}")

discount = 0

if total > 1000:
    discount = total * 0.10

final_amount = total - discount

print(f"\nTotal Amount    : ₹{total}")
print(f"Discount (10%)  : ₹{discount:.2f}")
print(f"Final Amount    : ₹{final_amount:.2f}")
print("==========================")