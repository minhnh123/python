# Bài 53

def all_subsets(lst):
    result = [[]]
    for item in lst:
        result += [x + [item] for x in result]
    return result

if __name__ == "__main__":
    # Nhập danh sách số, ví dụ: 1 2 3
    nums = list(map(int, input("Nhập các số, cách nhau bởi dấu cách: ").split()))
    subsets = all_subsets(nums)
    print("Tất cả các danh sách con là:")
    for s in subsets:
        print(s)
