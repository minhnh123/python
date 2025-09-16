st = input("Enter your string: ")
First_five_characters = st[:5]
Last_five_characters = st[len(st)-5:]
Str_1_line = 4 * (st + " ")
Str_4_line = 4 * (st + "\n")

print("First five characters are: " + First_five_characters)
print("Last five characters are: " + Last_five_characters)
print("Four strings of one line are: " + Str_1_line)
print("Four strings of four line are: \n" + Str_4_line)