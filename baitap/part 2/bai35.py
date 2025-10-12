# Bài 35
nums = input("Nhập dãy số, cách nhau bởi dấu phẩy: ")
lst = [int(x) for x in nums.split(",")]
odd = [x for x in lst if x % 2 == 1]
print("Các số lẻ là:", odd)
