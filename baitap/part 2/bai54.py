# Bài 54

def format_english_list(words):
    if not words:
        return ""
    if len(words) == 1:
        return words[0]
    if len(words) == 2:
        return f"{words[0]} and {words[1]}"
    return ", ".join(words[:-1]) + " and " + words[-1]

if __name__ == "__main__":
    # Nhập danh sách từ, cách nhau bởi dấu phẩy
    raw = input("Nhập các từ, cách nhau bởi dấu phẩy: ")
    words = [w.strip() for w in raw.split(",") if w.strip()]
    result = format_english_list(words)
    print("Kết quả:", result)
