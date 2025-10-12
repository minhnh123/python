# Bài 31
msg = input("Nhập tin nhắn: ")
result = ""
for ch in msg:
    if 'A' <= ch <= 'Z':
        result += chr((ord(ch) - ord('A') + 3) % 26 + ord('A'))
    elif 'a' <= ch <= 'z':
        result += chr((ord(ch) - ord('a') + 3) % 26 + ord('a'))
    else:
        result += ch
print("Tin nhắn đã mã hóa:", result)
