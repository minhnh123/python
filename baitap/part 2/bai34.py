# Bài 34
n = int(input("Nhập số thập phân: "))
binary = ""
if n == 0:
    binary = "0"
else:
    x = n
    while x > 0:
        binary = str(x % 2) + binary
        x //= 2
print(f"Số {n} ở hệ nhị phân là: {binary}")
