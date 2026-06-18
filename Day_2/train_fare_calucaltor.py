# Take a password as input.
# Check for length ≥8, uppercase, lowercase, digit, and special character.
# Show a strength score (Weak / Medium / Strong) with tips to improve. 

name=input("Enter your name:")
age=int(input("Enter your age:"))
preferred_class=input("Enter class type(Sleeper/3AC,2AC):").strip().upper()
distance=float(input("Enter distance(km) of travel:"))

price_rates={
    "SLEEPER":0.8,
    "3AC":1.2,
    "2AC":1.7
}

if preferred_class not in price_rates:
    print("Invalid travel class entered.")

else:
    base_price=distance * price_rates[preferred_class]

    discount=0
    discount_percent=0

    if age<12:
        discount_percent=10
        discount=base_price*0.10
        discount_type="Children's fare."
    elif age>=60:
        discount_percent=10
        discount=base_price*0.10
        discount_type="Senior citizen discount."

    else:
        discount_type="Discount."

    ticket_price=base_price - discount    

    gst=ticket_price * 0.05

    total_price=ticket_price +gst

    print("\n--- Ticket Summary ---")
    print(f"Passenger : {name}")
    print(f"Age       : {age}")
    print(f"Class     : {preferred_class}")
    print(f"Distance  : {distance:.0f} km")

    if discount>0:
        print(f"{discount_type}-{discount:.2f} ({discount_percent}%)")

    else:
        print("No Discount.")

    print(f"GST (5%): + {gst:.2f}")
    print(f"Total: {total_price:.2f}")

    print(f'\nBooking confirmed for {name} — Happy travel!')