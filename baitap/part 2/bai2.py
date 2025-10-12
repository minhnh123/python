st = input("Nhập vào một chuỗi: ")

if st.isupper():
    print("Chuỗi toàn ký tự hoa.")
elif st.islower():
    print("Chuỗi toàn ký tự thường.")
else:
    print("Chuỗi chứa cả ký tự hoa và ký tự thường.")