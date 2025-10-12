# Bài 5

n = int(input("Enter an integer greater than 0: "))
sum = 0.0
for i in range(1, n+1):
    sum += i / (i+1)
print(sum)
