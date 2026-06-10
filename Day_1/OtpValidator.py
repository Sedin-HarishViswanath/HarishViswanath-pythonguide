import random

otp = random.randint(100000, 999999)
print(f"Your OTP is:{otp}")

attempts = 3

while attempts > 0:
    user_otp = int(input("Enter the OTP: "))

    if user_otp == otp:
        print("OTP verified successfully!")
        break
    else:
        attempts -= 1

        if attempts > 0:
            print(f"Incorrect OTP. Attempts remaining: {attempts}")
        else:
            print("Account locked. All 3 attempts have been used.")