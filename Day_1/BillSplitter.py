bill_amount=float(input("Enter the total bill amount:"))
total_people=int(input("Enter the no.of people:"))

tip_percent=(input("Enter the tip percent:"))
if tip_percent:
    tip_percent=float(tip_percent)
else:
    tip_percent=0

tip_amount=bill_amount*tip_percent/100

total_amount = bill_amount + tip_amount

tip_share=total_amount/total_people

print("\nBill Summary")
print(f"Original Bill Amount:{bill_amount:.2f}")
print(f"Tip Percent:{tip_percent:.2f}%")
print(f"Tip Amount:{tip_amount:.2f}")
print(f"Total Amount: {total_amount:.2f}")
print(f"Number of People:{total_people}")
print(f"Amount per Person:₹{tip_share:.2f}")

