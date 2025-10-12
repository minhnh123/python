# Bài 11

numlist = []
while True:
    inp = input("Enter a number: ")
    if inp == "done":
        break
    value = float(inp)
    numlist.append(value)

average = sum(numlist) / len(numlist)
print("Giá trị Trung bình:", average)
print(numlist)
