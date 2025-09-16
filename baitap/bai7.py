from math import sin

a = float(input("Enter side a: "))
b = float(input("Enter side b: "))
c = float(input("Enter side c: "))
A = float(input("Enter angle A (radian): "))
B = float(input("Enter angle B (radian): "))
C = float(input("Enter angle C (radian): "))

# You can use any of the formulas below:
area1 = 0.5 * a * b * sin(C)
area2 = 0.5 * a * c * sin(B)
area3 = 0.5 * b * c * sin(A)

print("Area using ab*sin(C)/2: ", area1)
print("Area using ac*sin(B)/2: ", area2)
print("Area using bc*sin(A)/2: ", area3)