# dfa.py
# Kiểm tra chuỗi có thuộc ngôn ngữ (a+b+c)*ab hay không
# Sử dụng DFA nhận các ký tự 'a','b','c' và chấp nhận các xâu kết thúc bằng "ab".


# Các trạng thái: 0 = start / không có hậu tố phù hợp,
# 1 = hậu tố hiện tại là 'a',
# 2 = hậu tố hiện tại là 'ab' (trạng thái chấp nhận)
TRANS = {
    0: {'a': 1, 'b': 0, 'c': 0},
    1: {'a': 1, 'b': 2, 'c': 0},
    2: {'a': 1, 'b': 0, 'c': 0},
}
START = 0
ACCEPT = {2}
ALPHABET = {'a', 'b', 'c'}

def accepts(s: str) -> bool:
    state = START
    for ch in s:
        if ch not in ALPHABET:
            # Ký tự không thuộc bảng chữ cái ngôn ngữ -> không chấp nhận
            return False
        state = TRANS[state][ch]
    return state in ACCEPT

def main():
    # Không dùng thư viện ngoài; chỉ nhập từ input()
    s = input("Nhập chuỗi (chỉ a,b,c): ").strip()
    ok = accepts(s)
    print("Accepted" if ok else "Rejected")

if __name__ == "__main__":
    main()