# Bài 3
st = input("Enter your string: ")
st_search = input("Enter a searching string: ")
if st_search in st:
    print("A search string was found, at location:", st.find(st_search))
else:
    print("Not Found")
