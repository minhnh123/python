# Bài 7
num = int(input("Enter a number: "))
level = int(input("Bậc: "))
total = 0
temp = num
while temp > 0:
    digit = temp % 10
    total += digit ** level
    temp //= 10
if num == total:
    print(num, "is Amstrong, level:", level)
else:
    print(num, "is not Amstrong")
