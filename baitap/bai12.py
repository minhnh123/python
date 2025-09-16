meal_cost = float(input("Nhập chi phí bữa ăn: "))
tax = meal_cost * 0.05
tip = meal_cost * 0.18
total = meal_cost + tax + tip

print("Tiền bữa ăn: {:.2f}".format(meal_cost))
print("Tiền thuế: {:.2f}".format(tax))
print("Tiền boa: {:.2f}".format(tip))
print("Tổng cộng: {:.2f}".format(total))