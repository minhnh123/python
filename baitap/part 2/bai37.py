# Bài 37

words = []
while True:
    w = input()
    if w == "":
        break
    if w not in words:
        words.append(w)
for w in words:
    print(w)
