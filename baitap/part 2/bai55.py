import zipfile
import os

def compress_file(input_file, output_zip):
    with zipfile.ZipFile(output_zip, 'w') as zf:
        zf.write(input_file, os.path.basename(input_file))
    print(f"Đã nén {input_file} thành {output_zip}")

def decompress_file(input_zip, extract_dir):
    with zipfile.ZipFile(input_zip, 'r') as zf:
        zf.extractall(extract_dir)
    print(f"Đã giải nén {input_zip} vào {extract_dir}")

if __name__ == "__main__":
    print("1. Nén file")
    print("2. Giải nén file")
    choice = input("Chọn chức năng (1/2): ")
    if choice == "1":
        file_path = input("Nhập đường dẫn file cần nén: ")
        zip_path = input("Nhập tên file zip đầu ra: ")
        compress_file(file_path, zip_path)
    elif choice == "2":
        zip_path = input("Nhập đường dẫn file zip cần giải nén: ")
        extract_dir = input("Nhập thư mục giải nén: ")
        decompress_file(zip_path, extract_dir)
    else:
        print("Lựa chọn không hợp lệ.")
