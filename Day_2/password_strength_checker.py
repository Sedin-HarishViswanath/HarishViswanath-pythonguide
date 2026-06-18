import string

password=input("Enter password")

score=0
tips=[]

if len(password)>=8:
    score+=1

else:
    tips.append("Password must be atleast 8 characters.")

if any(char.isupper() for char in password):
    score+=1
else:
    tips.append("Password should contain atleast one uppercase letter.")

if any(char.islower() for char in password):
    score += 1
else:
    tips.append("Password should contain atleast one lowercas letter,")

if any(char.isdigit() for char in password):
    score += 1
else:
    tips.append("Add at least one digit.")

if any(char in string.punctuation for char in password):
    score += 1
else:
    tips.append("Add at least one special character.")

if score <= 2:
    strength = "Weak"
elif score <= 4:
    strength = "Medium"
else:
    strength = "Strong"

print(f"\nStrength: {strength} ({score}/5)")    

if strength == "Strong":
    print("Your password is secure!")
else:
    print("Tips to improve your password:")
    for tip in tips:
        print("-", tip)