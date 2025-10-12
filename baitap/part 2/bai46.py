# Bài 46

def squares_list():
    return [i**2 for i in range(1, 21)]

if __name__ == "__main__":
    lst = squares_list()
    print("5 phần tử cuối:", lst[-5:])
