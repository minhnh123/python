# Bài 26

char = input("Nhập một chữ cái: ").lower()

if char in "aeiou":
    print(f"'{char}' là nguyên âm.")
elif char == "y":
    print(f"'{char}' có thể là nguyên âm hoặc phụ âm.")
elif char.isalpha() and len(char) == 1:
    print(f"'{char}' là phụ âm.")
else:
    print("Vui lòng nhập một chữ cái hợp lệ.")
