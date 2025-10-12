# Bài 18
chuoi = input("Nhập vào một chuỗi: ")
d = {"chu_hoa": 0, "chu_thuong": 0}
for ch in chuoi:
    if ch.isupper():
        d["chu_hoa"] += 1
    elif ch.islower():
        d["chu_thuong"] += 1
print("Số chữ hoa là:", d["chu_hoa"])
print("Số chữ thường là:", d["chu_thuong"])
