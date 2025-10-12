# Bài 9

# my_str = "Hello this Is an Example With cased letters"
my_str = input("Enter a string: ")

# Tách từ trong chuỗi và lưu vào danh sách
ds_tu = my_str.split()

# Sắp xếp các phần tử (từ) trong danh sách
ds_tu.sort()

# Hiển thị từ trong danh sách
print("Các từ đã được tách và sắp xếp theo Alphabet:")
for tu in ds_tu:
    print(tu)
