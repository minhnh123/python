
# file: models.py
class SinhVien:
    def __init__(self, id, ho_ten, mssv, email, diem_tb, lop_id=None):
        self.id = id
        self.ho_ten = ho_ten
        self.mssv = mssv
        self.email = email
        self.diem_tb = diem_tb
        self.lop_id = lop_id