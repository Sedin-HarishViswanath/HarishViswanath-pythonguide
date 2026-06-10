marks=[]

for i in range(5):
    mark=float(input(f"Enter marks for Subject {i+1}:"))
    marks.append(mark)

total=sum(marks)
percentage=(total/500)*100

if percentage >=90:
    grade='A'
elif percentage >=80:
    grade='B'
elif percentage >=70:
    grade='C'
elif percentage >=60:
    grade='D'
else:
    grade='F'

count=0
for mark in marks:
    if mark<40:
        count+=1

print("\nREPORT CARD")
for i in range(5):
    print(f"Subject {i + 1}: {marks[i]:.2f}")
print(f"\nTotal Marks : {total:.2f} / 500")
print(f"Percentage : {percentage:.2f}%")
print(f"Grade : {grade}")

if count:
    print(f"Number of subjects failed:{count}")
else:
    print("All subjects passed!")