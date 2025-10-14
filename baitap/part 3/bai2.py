filename = 'alice.txt'
try:
    with open(filename) as f_obj:
        contents = f_obj.read()
except FileNotFoundError:
    msg = "File " + filename + " không tồn tại."
    print(msg)
else:
    words = contents.split()
    num_words = len(words)
    print("File " + filename + " có " + str(num_words) + " từ.")