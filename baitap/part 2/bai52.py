# Bài 52

def is_perfect_number(n):
    if n < 2:
        return False
    total = sum(i for i in range(1, n) if n % i == 0)
    return total == n

if __name__ == "__main__":
    n = int(input("Nhập số nguyên dương: "))
    if is_perfect_number(n):
        print(f"{n} là số hoàn hảo.")
    else:
        print(f"{n} không phải là số hoàn hảo.")

    print("Các số hoàn hảo từ 1 đến 10000 là:")
    for i in range(1, 10001):
        if is_perfect_number(i):
            print(i, end=" ")
