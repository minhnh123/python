import binascii

# Bộ khóa đã cho (giả sử là 4 khóa)
KEYS = [
    b'\x01\x02\x03\x04\x05\x06\x07\x08',
    b'\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10',
    b'\x11\x12\x13\x14\x15\x16\x17\x18',
    b'\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20'
]

# Số round (n = tháng sinh: tháng 3)
N_ROUNDS = 3

# Hàm F: Hàm trộn đơn giản sử dụng XOR
# (Phải đảm bảo K và R có cùng độ dài. Ở đây chúng ta XOR byte-by-byte.)
def f_function(R, K):
    # Đảm bảo R và K có cùng độ dài (Nếu không, cần padding hoặc XOR theo byte/bit)
    # Giả định ở đây: độ dài L, R bằng nhau, bằng độ dài khóa
    
    # Chuyển bytes sang list of integers (bytes) để XOR
    R_int = [b for b in R]
    K_int = [b for b in K]
    
    # Thực hiện XOR
    F_result_int = [R_int[i] ^ K_int[i] for i in range(len(R_int))]
    
    # Chuyển lại thành bytes
    return bytes(F_result_int)


# Mã hóa Feistel
def feistel_encrypt(plaintext_bytes, keys, n_rounds):
    # Chia khối đầu vào làm hai nửa L0 và R0
    half_len = len(plaintext_bytes) // 2
    L = plaintext_bytes[:half_len]
    R = plaintext_bytes[half_len:]

    # Thực hiện N_ROUNDS
    for i in range(n_rounds):
        K = keys[i]  # Khóa tương ứng với round i
        
        # L_i = R_{i-1}
        L_next = R
        
        # R_i = L_{i-1} XOR f(R_{i-1}, K_i)
        f_output = f_function(R, K)
        
        # Đảm bảo L và f_output có cùng độ dài để XOR
        # Chuyển bytes sang list of integers (bytes) để XOR
        L_int = [b for b in L]
        f_int = [b for b in f_output]
        
        R_next_int = [L_int[j] ^ f_int[j] for j in range(len(L_int))]
        R_next = bytes(R_next_int)

        L = L_next
        R = R_next
    
    # Hợp nhất: R_n || L_n (đổi chỗ lần cuối)
    ciphertext_bytes = R + L
    return ciphertext_bytes

# ----------------- CHUYỂN ĐỔI DỮ LIỆU ĐẦU VÀO -----------------

STUDENT_ID = "22NS035"

# Chuyển mã sinh viên sang bytes (ASCII/UTF-8)
# Mã sinh viên 7 ký tự. Giả sử ta thêm padding để có độ dài chẵn (8 bytes)
# (Đây là bước quan trọng để chia khối Feistel)
# Ví dụ: Thêm một byte 0x00 vào cuối
PLAINTEXT_PADDED = STUDENT_ID.encode('ascii') + b'\x00'

# Kiểm tra độ dài: 8 bytes. Hai nửa L0, R0 đều là 4 bytes.
print(f"Mã sinh viên (bytes): {PLAINTEXT_PADDED.hex()}") # Debug

# Khóa cần dùng (3 khóa đầu)
USED_KEYS = [KEYS[i][:len(PLAINTEXT_PADDED)//2] for i in range(N_ROUNDS)] # Chỉ lấy 4 bytes đầu của khóa cho phù hợp độ dài L, R = 4 bytes
# print(f"Khóa dùng: {[k.hex() for k in USED_KEYS]}") # Debug

# ----------------- THỰC THI MÃ HÓA -----------------

# Mã hóa
CIPHERTEXT_BYTES = feistel_encrypt(PLAINTEXT_PADDED, USED_KEYS, N_ROUNDS)

# Chuyển kết quả mã hóa sang dạng hex string
CIPHERTEXT_HEX = CIPHERTEXT_BYTES.hex()

# In kết quả theo cú pháp cờ CTF
print(f"crypto{{{CIPHERTEXT_HEX}}}")

# ----------------- THỰC HIỆN GIẢI MÃ (Kiểm tra) -----------------
# Để giải mã, chỉ cần thực hiện lại quá trình mã hóa với thứ tự khóa đảo ngược

def feistel_decrypt(ciphertext_bytes, keys, n_rounds):
    # Lấy danh sách khóa đã đảo ngược
    decryption_keys = keys[:n_rounds]
    decryption_keys.reverse()
    
    # Chia khối đầu vào (đã được đổi chỗ lần cuối)
    half_len = len(ciphertext_bytes) // 2
    R = ciphertext_bytes[:half_len] # R_n (sẽ là L_{n-1})
    L = ciphertext_bytes[half_len:] # L_n (sẽ là R_{n-1})
    
    # Thực hiện N_ROUNDS
    for i in range(n_rounds):
        K = decryption_keys[i]  # Khóa tương ứng với round i (đảo ngược)
        
        # R_{i-1} = L_i (Đã là R)
        R_prev = L
        
        # L_{i-1} = R_i XOR f(L_i, K_i) (Đã là L)
        f_output = f_function(L, K)
        
        # Chuyển bytes sang list of integers (bytes) để XOR
        R_int = [b for b in R]
        f_int = [b for b in f_output]
        
        L_prev_int = [R_int[j] ^ f_int[j] for j in range(len(R_int))]
        L_prev = bytes(L_prev_int)

        L = L_prev
        R = R_prev

    # Hợp nhất: L_0 || R_0 (Không đổi chỗ lần cuối)
    decrypted_bytes = L + R
    return decrypted_bytes

# PLANETEXT_DECRYPTED = feistel_decrypt(CIPHERTEXT_BYTES, USED_KEYS, N_ROUNDS)
# print(f"Giải mã: {PLANETEXT_DECRYPTED.hex()}") # Debug
# print(f"Giải mã (text): {PLANETEXT_DECRYPTED.rstrip(b'\x00').decode('ascii')}") # Debug