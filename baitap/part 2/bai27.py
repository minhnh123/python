# Bài 27

shapes = {
    3: "Tam giác",
    4: "Tứ giác",
    5: "Ngũ giác",
    6: "Lục giác",
    7: "Thất giác",
    8: "Bát giác",
    9: "Cửu giác",
    10: "Thập giác"
}

n = int(input("Nhập số cạnh (3-10): "))
if n in shapes:
    print(f"Hình có {n} cạnh là: {shapes[n]}")
else:
    print("Số cạnh không hợp lệ! Chỉ hỗ trợ từ 3 đến 10 cạnh.")
