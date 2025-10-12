
import random

def random_password():
    length = random.randint(7, 10)
    return ''.join(chr(random.randint(33, 126)) for _ in range(length))

if __name__ == "__main__":
    print("Mật khẩu ngẫu nhiên:", random_password())
