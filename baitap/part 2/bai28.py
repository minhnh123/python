# Bài 28

month = input("Nhập tên tháng (tiếng Việt, không dấu, ví dụ: thang 1): ").strip().lower()

days_31 = ["thang 1", "thang 3", "thang 5", "thang 7", "thang 8", "thang 10", "thang 12"]
days_30 = ["thang 4", "thang 6", "thang 9", "thang 11"]
days_28_29 = ["thang 2"]

if month in days_31:
    print("Tháng này có 31 ngày.")
elif month in days_30:
    print("Tháng này có 30 ngày.")
elif month in days_28_29:
    print("Tháng này có 28 hoặc 29 ngày.")
else:
    print("Tên tháng không hợp lệ.")
