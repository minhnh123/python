# Bài 6

st = input("Enter your sentence: ")
Sum_upper_Char = 0
Sum_lower_Char = 0
for c in st:
    if c.isupper():
        Sum_upper_Char += 1
    elif c.islower():
        Sum_lower_Char += 1
print("Sum of Upper Character:", Sum_upper_Char)
print("Sum of Lower Character:", Sum_lower_Char)
