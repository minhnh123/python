# Bài 43

def print_longer_string(s1, s2):
    if len(s1) > len(s2):
        print(s1)
    elif len(s2) > len(s1):
        print(s2)
    else:
        print(s1)
        print(s2)

if __name__ == "__main__":
    a = input("Nhập chuỗi thứ nhất: ")
    b = input("Nhập chuỗi thứ hai: ")
    print_longer_string(a, b)
