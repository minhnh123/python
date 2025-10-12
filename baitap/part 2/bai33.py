# Bài 33

s = input("Nhập chuỗi: ")
is_palindrome = True
for i in range(len(s)//2):
    if s[i] != s[-i-1]:
        is_palindrome = False
        break
if is_palindrome:
    print(f'"{s}" là chuỗi Palindrom.')
else:
    print(f'"{s}" không phải là chuỗi Palindrom.')
