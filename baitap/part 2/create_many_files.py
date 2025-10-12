for i in range(2, 56):  
    with open(f"bai{i}.py", "w", encoding="utf-8") as f:
        f.write(f"# Bài {i}\n")
print("Đã tạo xong các file bai2.py đến bai55.py")