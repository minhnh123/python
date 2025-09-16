width = float(input("Nhập chiều rộng cánh đồng (m): "))
length = float(input("Nhập chiều dài cánh đồng (m): "))
area_m2 = width * length
area_acre = area_m2 / 43560
print("Diện tích cánh đồng theo mét vuông:", area_m2)
print("Diện tích cánh đồng theo Mẫu Anh:", area_acre)