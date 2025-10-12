# Bài 38

nums = []
while True:
    s = input()
    if s == "":
        break
    nums.append(int(s))

neg = [x for x in nums if x < 0]
zero = [x for x in nums if x == 0]
pos = [x for x in nums if x > 0]

for x in neg + zero + pos:
    print(x)
