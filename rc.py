import random

# ================================================================
# CÁC HÀM TỪ GIST (Giữ nguyên logic KSA/PRNG)
# ================================================================

def key_scheduling(key):
    sched = [i for i in range(0, 256)]
    i = 0
    for j in range(0, 256):
        i = (i + sched[j] + key[j % len(key)]) % 256
        tmp = sched[j]
        sched[j] = sched[i]
        sched[i] = tmp
    return sched

def stream_generation(sched):
    i = 0
    j = 0
    while True:
        i = (1 + i) % 256
        j = (sched[j] + j) % 256
        tmp = sched[j]
        sched[j] = sched[i]
        sched[i] = tmp
        yield sched[(sched[i] + sched[j]) % 256]

# ================================================================
# CÁC HÀM MÃ HÓA / GIẢI MÃ (ĐÃ SỬA LỖI UNICODE)
# ================================================================

def encrypt(text, key_str):
    # 1. Chuyển text và key sang bytes bằng UTF-8 thay vì dùng ord()
    # Điều này đảm bảo mọi phần tử đều nằm trong khoảng 0-255
    text_bytes = text.encode('utf-8')
    key_bytes = key_str.encode('utf-8')
    
    # 2. KSA
    # Chuyển key_bytes thành list số nguyên để tương thích với hàm key_scheduling cũ
    sched = key_scheduling(list(key_bytes))
    
    # 3. PRNG
    key_stream = stream_generation(sched)
    
    ciphertext_bytes = []
    # 4. XOR
    for byte in text_bytes:
        encrypted_byte = byte ^ next(key_stream)
        ciphertext_bytes.append(encrypted_byte)
        
    # 5. Chuyển sang Hex
    ciphertext_hex = ''.join([f'{b:02X}' for b in ciphertext_bytes])
    return ciphertext_hex

def decrypt(ciphertext_hex, key_str):
    # 1. Chuyển Hex về mảng số nguyên (bytes)
    ciphertext_bytes = [int(ciphertext_hex[i:i+2], 16) for i in range(0, len(ciphertext_hex), 2)]
    # Key cũng phải encode utf-8 giống hệt lúc mã hóa
    key_bytes = key_str.encode('utf-8')
    
    # 2. KSA
    sched = key_scheduling(list(key_bytes))
    
    # 3. PRNG
    key_stream = stream_generation(sched)
    
    # Sử dụng bytearray để hứng kết quả
    plaintext_bytes = bytearray()
    
    # 4. XOR ngược lại
    for byte in ciphertext_bytes:
        decrypted_byte = byte ^ next(key_stream)
        plaintext_bytes.append(decrypted_byte)
        
    # 5. Decode từ bytes về string UTF-8 để hiển thị tiếng Việt
    return plaintext_bytes.decode('utf-8')

# ================================================================
# CHẠY THỬ
# ================================================================

ho_va_ten = "Trần Nhật Minh"
khoa_bi_mat = "KhoaAnToanThongTin"

print(f"Họ và tên (Plaintext): {ho_va_ten}")
print(f"Khóa bí mật: {khoa_bi_mat}")
print("-" * 30)

ban_ma_hex = encrypt(ho_va_ten, khoa_bi_mat)
print(f"Bản mã (Ciphertext): {ban_ma_hex}")

giai_ma = decrypt(ban_ma_hex, khoa_bi_mat)
print(f"Giải mã (Decrypted): {giai_ma}")
print("-" * 30)

if giai_ma == ho_va_ten:
    print("Thành công: Giải mã trùng khớp với bản gốc.")
else:
    print("Thất bại: Giải mã KHÔNG trùng khớp.")