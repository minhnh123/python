# Bài 36

lst = []
while True:
    n = int(input())
    if n == 0:
        break
    lst.append(n)
lst.sort()
for x in lst:
    print(x)
