# Bài 30
year = int(input("Nhập năm: "))
if (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0):
    print(f"{year} là năm nhuận")
else:
    print(f"{year} không phải là năm nhuận")
