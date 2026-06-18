# Simulate a basic ATM. 
# User enters a PIN (3 attempts max). 
# On success, show balance and let them withdraw/deposit. 
# Block the card after 3 wrong PINs

correct_pin=1234
balance=12500.00
attempts=3

print("Welcome to SBI bank")
logged_in = False

while attempts>0:
    pin=int(input("Enter pin for your account:"))
    if pin==correct_pin:    
        logged_in = True
        print(f"Your Current Balance: {balance}")
        while True:
            print("\n1.Withdraw amount")
            print("2.Deposite amount")
            print("3.Exit")

            choice=int(input("Enter your choice:"))
            if choice==1:
                amount=float(input("Enter amount:"))
                if amount<=balance:
                    balance-=amount
                    print(f"Withdrawan amount: {amount:,.2f}")
                    print(f"Current Balance: {balance:,.2f}")
                else:
                    print("Insufficient balance")

            elif choice==2:
                amount=float(input("Enter amount:"))
                balance+=amount
                print(f"Deposited amount: {amount:,.2f}")
                print(f"Current Balance: {balance:,.2f}")
            elif choice==3:
                print("Thank you for using SBI ATM.")
                logged_in = False
                break

            else:
                print("Invalid choice") 
                
    else:
        attempts-=1
        if attempts>0:
            print(f"Incorrect pin.You have {attempts} attempts left.") 
        else:
            print("Your account is blocked.Come again tomorrow")           