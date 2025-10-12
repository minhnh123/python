# Bài 42

def factorial(n):
    result = 1
    for i in range(1, n+1):
        result *= i
    return result

if __name__ == "__main__":
    n = int(input("Nhập số nguyên dương: "))
    print(f"Giai thừa của {n} là: {factorial(n)}")
