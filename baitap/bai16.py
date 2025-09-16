import math

h = float(input("Nhập chiều cao thả vật (m): "))
vi = 0  
a = 9.8  

vf = math.sqrt(vi**2 + 2 * a * h)
print("Tốc độ của vật khi chạm đất (m/s):", vf)