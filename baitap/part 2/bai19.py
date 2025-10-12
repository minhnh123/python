ftext = open("romeo.txt", encoding="utf-8")
tu_dien_cac_tu = {}

for dong in ftext:
    danh_sach_tu = dong.split()
    for tu in danh_sach_tu:
        tu_dien_cac_tu[tu] = tu_dien_cac_tu.get(tu, 0) + 1

ftext.close()

danh_sach = []
for key, val in tu_dien_cac_tu.items():
    newtup = (val, key)
    danh_sach.append(newtup)

danh_sach = sorted(danh_sach, reverse=True)

print("10 từ xuất hiện nhiều nhất:")
for val, key in danh_sach[:10]:
    print(key, val)
