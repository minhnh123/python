# Bài 8

remove_chars = """!()-[]{};:'"\,<>./?@#$%^&*_~"""
my_str = input("Enter a string: ")
result = ""
for char in my_str:
    if char not in remove_chars:
        result += char
print(result)
