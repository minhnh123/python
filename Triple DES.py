hex_str = "63727970746f6f7b6e30745f346c6c5f6b3379735f3472335f673030645f6b3379737d060606060606" 
data = bytes.fromhex(hex_str)
pad_len = data[-1]            
flag = data[:-pad_len].decode()
print(flag)
