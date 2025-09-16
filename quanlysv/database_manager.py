# file: database_manager.py (Đã nâng cấp để Phân trang)
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

class QuanLySinhVien:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD")
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
        except Error as e:
            raise ConnectionError(
                "Không thể kết nối tới MySQL. Vui lòng kiểm tra file .env và cấu hình kết nối.\nChi tiết: " + str(e)
            )

    # ===== HÀM MỚI ĐỂ ĐẾM SINH VIÊN =====
    def dem_so_sinh_vien(self, khoa_id=None, lop_id=None, search_term=None):
        query = "SELECT COUNT(sv.id) as total FROM sinhvien sv LEFT JOIN lop l ON sv.lop_id = l.id LEFT JOIN khoa k ON l.khoa_id = k.id"
        conditions = []
        args = []
        if khoa_id:
            conditions.append("k.id = %s"); args.append(khoa_id)
        if lop_id:
            conditions.append("l.id = %s"); args.append(lop_id)
        if search_term:
            conditions.append("(sv.ho_ten LIKE %s OR sv.mssv LIKE %s)"); args.extend([f"%{search_term}%", f"%{search_term}%"])
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        self.cursor.execute(query, args)
        result = self.cursor.fetchone()
        return result['total'] if result else 0

    # ===== CẬP NHẬT hien_thi_danh_sach ĐỂ PHÂN TRANG =====
    def hien_thi_danh_sach(self, khoa_id=None, lop_id=None, search_term=None, page=1, page_size=20):
        query = """
            SELECT sv.id, sv.ho_ten, sv.mssv, sv.email, sv.diem_tb, l.ten_lop, k.ten_khoa
            FROM sinhvien sv
            LEFT JOIN lop l ON sv.lop_id = l.id
            LEFT JOIN khoa k ON l.khoa_id = k.id
        """
        conditions = []
        args = []
        if khoa_id:
            conditions.append("k.id = %s"); args.append(khoa_id)
        if lop_id:
            conditions.append("l.id = %s"); args.append(lop_id)
        if search_term:
            conditions.append("(sv.ho_ten LIKE %s OR sv.mssv LIKE %s)"); args.extend([f"%{search_term}%", f"%{search_term}%"])

        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        offset = (page - 1) * page_size
        query += " ORDER BY sv.id LIMIT %s OFFSET %s"
        args.extend([page_size, offset])
        
        self.cursor.execute(query, args)
        return self.cursor.fetchall()

    # ... (Tất cả các hàm khác từ KHOA, LỚP, SINH VIÊN (CRUD), MÔN HỌC, ĐIỂM giữ nguyên)
    def them_khoa(self, ten_khoa):
        query = "INSERT INTO khoa (ten_khoa) VALUES (%s)"; self.cursor.execute(query, (ten_khoa,)); self.connection.commit()
    def hien_thi_ds_khoa(self):
        query = "SELECT * FROM khoa ORDER BY id"; self.cursor.execute(query); return self.cursor.fetchall()
    def cap_nhat_khoa(self, id_khoa, ten_moi):
        query = "UPDATE khoa SET ten_khoa = %s WHERE id = %s"; self.cursor.execute(query, (ten_moi, id_khoa)); self.connection.commit(); return self.cursor.rowcount > 0
    def xoa_khoa(self, id_khoa):
        query = "DELETE FROM khoa WHERE id = %s"; self.cursor.execute(query, (id_khoa,)); self.connection.commit(); return self.cursor.rowcount > 0
    def them_lop(self, ten_lop, khoa_id):
        query = "INSERT INTO lop (ten_lop, khoa_id) VALUES (%s, %s)"; self.cursor.execute(query, (ten_lop, khoa_id)); self.connection.commit()
    def hien_thi_ds_lop(self, khoa_id=None):
        query = "SELECT l.id, l.ten_lop, k.ten_khoa FROM lop l LEFT JOIN khoa k ON l.khoa_id = k.id"
        args = []
        if khoa_id: query += " WHERE l.khoa_id = %s"; args.append(khoa_id)
        query += " ORDER BY l.id"
        self.cursor.execute(query, args); return self.cursor.fetchall()
    def cap_nhat_lop(self, id_lop, ten_moi, khoa_id_moi):
        query = "UPDATE lop SET ten_lop = %s, khoa_id = %s WHERE id = %s"; self.cursor.execute(query, (ten_moi, khoa_id_moi, id_lop)); self.connection.commit(); return self.cursor.rowcount > 0
    def xoa_lop(self, id_lop):
        query = "DELETE FROM lop WHERE id = %s"; self.cursor.execute(query, (id_lop,)); self.connection.commit(); return self.cursor.rowcount > 0
    def them_sinh_vien(self, sinh_vien):
        query = "INSERT INTO sinhvien (ho_ten, mssv, email, diem_tb, lop_id) VALUES (%s, %s, %s, %s, %s)"; args = (sinh_vien.ho_ten, sinh_vien.mssv, sinh_vien.email, sinh_vien.diem_tb, sinh_vien.lop_id); self.cursor.execute(query, args); self.connection.commit()
    def cap_nhat_sinh_vien(self, id_sv, ho_ten, mssv, email, diem_tb, lop_id):
        query = "UPDATE sinhvien SET ho_ten=%s, mssv=%s, email=%s, diem_tb=%s, lop_id=%s WHERE id=%s"; args = (ho_ten, mssv, email, diem_tb, lop_id, id_sv); self.cursor.execute(query, args); self.connection.commit(); return self.cursor.rowcount > 0
    def xoa_sinh_vien(self, id_sv):
        query = "DELETE FROM sinhvien WHERE id = %s"; self.cursor.execute(query, (id_sv,)); self.connection.commit(); return self.cursor.rowcount > 0
    def get_diem_list(self):
        query = "SELECT diem_tb FROM sinhvien WHERE diem_tb IS NOT NULL"; self.cursor.execute(query); results = self.cursor.fetchall(); return [item['diem_tb'] for item in results]
    def them_mon_hoc(self, ten, tin_chi, khoa_id):
        query = "INSERT INTO mon_hoc (ten_mon_hoc, so_tin_chi, khoa_id) VALUES (%s, %s, %s)"; self.cursor.execute(query, (ten, tin_chi, khoa_id)); self.connection.commit()
    def hien_thi_ds_mon_hoc(self):
        query = "SELECT mh.id, mh.ten_mon_hoc, mh.so_tin_chi, k.ten_khoa FROM mon_hoc mh LEFT JOIN khoa k ON mh.khoa_id = k.id ORDER BY mh.id"; self.cursor.execute(query); return self.cursor.fetchall()
    def hien_thi_diem_cua_sv(self, sinhvien_id):
        query = "SELECT mh.ten_mon_hoc, mh.so_tin_chi, d.diem_chuyencan, d.diem_giuaky, d.diem_cuoiky FROM diem d JOIN mon_hoc mh ON d.monhoc_id = mh.id WHERE d.sinhvien_id = %s"; self.cursor.execute(query, (sinhvien_id,)); return self.cursor.fetchall()
    def nhap_diem(self, sv_id, mh_id, diem_cc, diem_gk, diem_ck):
        query = "INSERT INTO diem (sinhvien_id, monhoc_id, diem_chuyencan, diem_giuaky, diem_cuoiky) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE diem_chuyencan=VALUES(diem_chuyencan), diem_giuaky=VALUES(diem_giuaky), diem_cuoiky=VALUES(diem_cuoiky)"; self.cursor.execute(query, (sv_id, mh_id, diem_cc, diem_gk, diem_ck)); self.connection.commit()
    def tinh_va_cap_nhat_diem_tb(self, sinhvien_id):
        query = "SELECT d.diem_chuyencan, d.diem_giuaky, d.diem_cuoiky, mh.so_tin_chi FROM diem d JOIN mon_hoc mh ON d.monhoc_id = mh.id WHERE d.sinhvien_id = %s"; self.cursor.execute(query, (sinhvien_id,)); ds_diem = self.cursor.fetchall()
        if not ds_diem: return
        tong_diem_nhan_tin_chi = 0; tong_tin_chi = 0
        for diem in ds_diem: diem_mon = (diem['diem_chuyencan'] * 0.1) + (diem['diem_giuaky'] * 0.3) + (diem['diem_cuoiky'] * 0.6); tong_diem_nhan_tin_chi += diem_mon * diem['so_tin_chi']; tong_tin_chi += diem['so_tin_chi']
        diem_tb_moi = tong_diem_nhan_tin_chi / tong_tin_chi if tong_tin_chi > 0 else 0.0
        update_query = "UPDATE sinhvien SET diem_tb = %s WHERE id = %s"; self.cursor.execute(update_query, (diem_tb_moi, sinhvien_id)); self.connection.commit()
    def dong_ket_noi(self):
        if self.connection and self.connection.is_connected(): self.connection.close()