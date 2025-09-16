C = 4.186  

M = float(input("Nhập khối lượng nước (gram): "))
delta_T = float(input("Nhập độ tăng nhiệt độ (°C): "))

Q = M * C * delta_T  
print("Năng lượng cần thiết (Joules):", Q)

Q_kWh = Q * 2.777e-7

cost = Q_kWh * 8.9  

print("Chi phí làm nóng nước (cent):", cost)