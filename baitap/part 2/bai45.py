# Bài 45

def print_first_five_squares():
    lst = []
    for i in range(1, 21):
        lst.append(i ** 2)
    print(lst[:5])

if __name__ == "__main__":
    print_first_five_squares()
