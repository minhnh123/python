# Bài 20

x = int(input("Nhập số cần tính giai thừa: "))

def giaithua(x):
    if x == 0:
        return 1
    return x * giaithua(x - 1)

print("Giai thừa của", x, "là:", giaithua(x))
