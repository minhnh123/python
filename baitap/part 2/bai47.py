# Bài 47

def squares_list():
    return [i**2 for i in range(1, 21)]

if __name__ == "__main__":
    lst = squares_list()
    print("Các phần tử trừ 5 phần tử đầu:", lst[5:])
