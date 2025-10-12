# Bài 32

def caesar_cipher(text, shift):
    result = ""
    for ch in text:
        if 'A' <= ch <= 'Z':
            result += chr((ord(ch) - ord('A') + shift) % 26 + ord('A'))
        elif 'a' <= ch <= 'z':
            result += chr((ord(ch) - ord('a') + shift) % 26 + ord('a'))
        else:
            result += ch
    return result

if __name__ == "__main__":
    choice = input("Bạn muốn (e)ncode hay (d)ecode? ")
    msg = input("Nhập tin nhắn: ")
    shift = int(input("Nhập số ký tự dịch chuyển: "))
    if choice.lower().startswith('e'):
        print("Kết quả mã hóa:", caesar_cipher(msg, shift))
    else:
        print("Kết quả giải mã:", caesar_cipher(msg, -shift))
