# Bài 29

a = float(input("Nhập cạnh a: "))
b = float(input("Nhập cạnh b: "))
c = float(input("Nhập cạnh c: "))

if a + b > c and a + c > b and b + c > a:
    if a == b == c:
        print("Tam giác đều")
    elif a == b or b == c or a == c:
        print("Tam giác cân")
    else:
        print("Tam giác thường")
else:
    print("Ba cạnh không tạo thành tam giác")
