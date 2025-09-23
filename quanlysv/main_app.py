import tkinter as tk
from tkinter import ttk, messagebox
from mysql.connector import Error
import math
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os
from database_manager import QuanLySinhVien
from models import SinhVien
from ttkthemes import ThemedTk
from PIL import Image, ImageTk # <-- Thêm import này


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Hệ thống Quản lý Sinh viên")
        self.root.geometry("1200x650")

        self.style = ttk.Style(self.root)
        self.style.theme_use('clam') 

        self.style.configure("TButton", padding=6, relief="flat", font=('Helvetica', 10))
        self.style.configure("Treeview", rowheight=25, font=('Helvetica', 9))
        self.style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        self.style.configure("TLabelFrame.Label", font=('Helvetica', 10, 'bold'))
        self.style.configure("TLabel", font=('Helvetica', 10))
        self.style.configure("TEntry", font=('Helvetica', 10))
        self.style.configure("TCombobox", font=('Helvetica', 10))

        try:
            self.db = QuanLySinhVien()
        except ConnectionError as e:
            messagebox.showerror("Lỗi kết nối", e); self.root.destroy(); return
        
        self.load_icons()
        self.sv_current_page = 1
        self.sv_page_size = 15
        self.sv_total_records = 0
        self.sv_total_pages = 1
        
        self._after_id = None
        self.create_widgets()
        self.load_initial_data()
    
    def load_icons(self):
        try:
            self.addsv_icon = ImageTk.PhotoImage(Image.open("icons/add-sv.png").resize((16, 16), Image.Resampling.LANCZOS))
            self.add_icon = ImageTk.PhotoImage(Image.open("icons/add.png").resize((16, 16), Image.Resampling.LANCZOS))

            self.update_icon = ImageTk.PhotoImage(Image.open("icons/update.png").resize((16, 16), Image.Resampling.LANCZOS))
            self.delete_icon = ImageTk.PhotoImage(Image.open("icons/delete.png").resize((16, 16), Image.Resampling.LANCZOS))
            self.clear_icon = ImageTk.PhotoImage(Image.open("icons/clear.png").resize((16, 16), Image.Resampling.LANCZOS))
        except FileNotFoundError as e:
            messagebox.showwarning("Thiếu file Icon", f"Không tìm thấy file icon: {e}\nChương trình sẽ chạy mà không có icon.")
            self.add_icon = self.update_icon = self.delete_icon = self.clear_icon = None
        except Exception as e:
            messagebox.showerror("Lỗi Icon", f"Lỗi khi tải icon: {e}")
            self.add_icon = self.update_icon = self.delete_icon = self.clear_icon = None

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, padx=10, fill="both", expand=True)

        self.tab_sv = ttk.Frame(self.notebook, padding=10)
        self.tab_lop = ttk.Frame(self.notebook, padding=10)
        self.tab_khoa = ttk.Frame(self.notebook, padding=10)
        self.tab_mon_hoc = ttk.Frame(self.notebook, padding=10)

        self.notebook.add(self.tab_sv, text='Quản lý Sinh viên')
        self.notebook.add(self.tab_lop, text='Quản lý Lớp')
        self.notebook.add(self.tab_khoa, text='Quản lý Khoa')
        self.notebook.add(self.tab_mon_hoc, text='Quản lý Môn học')
        
        self.create_sv_tab()
        self.create_lop_tab()
        self.create_khoa_tab()
        self.create_mon_hoc_tab()

    def load_initial_data(self):
        self.load_khoa_data()
        self.load_lop_data()
        self.load_mon_hoc_data()
        self.load_sv_data()

    def refresh_all_data(self):
        self.load_initial_data()

    def create_sv_tab(self):
        sv_main_frame = ttk.Frame(self.tab_sv)
        sv_main_frame.pack(fill="both", expand=True)
    
        sv_filter_frame = ttk.LabelFrame(sv_main_frame, text="Bộ lọc và Tìm kiếm", padding=10)
        sv_filter_frame.pack(fill="x", pady=5)
        ttk.Label(sv_filter_frame, text="Khoa:").pack(side="left", padx=(0,5))
        self.sv_filter_khoa_combo = ttk.Combobox(sv_filter_frame, state="readonly", width=25)
        self.sv_filter_khoa_combo.pack(side="left", padx=(0,10))
        self.sv_filter_khoa_combo.bind("<<ComboboxSelected>>", self.on_sv_filter_khoa_select)
        ttk.Label(sv_filter_frame, text="Lớp:").pack(side="left", padx=(0,5))
        self.sv_filter_lop_combo = ttk.Combobox(sv_filter_frame, state="readonly", width=20)
        self.sv_filter_lop_combo.pack(side="left", padx=(0,10))
        self.sv_filter_lop_combo.bind("<<ComboboxSelected>>", lambda e: self.reset_and_load_sv())
        ttk.Label(sv_filter_frame, text="Tìm kiếm (Tên/MSSV):").pack(side="left", padx=(10,5))
        self.sv_search_entry = ttk.Entry(sv_filter_frame, width=25)
        self.sv_search_entry.pack(side="left", padx=(0,10))
        self.sv_search_entry.bind("<KeyRelease>", self.debounce(lambda e: self.reset_and_load_sv(), 500))
        ttk.Button(sv_filter_frame, text="Bỏ lọc", command=self.clear_sv_filter).pack(side="left", padx=5)
    
        sv_content_frame = ttk.Frame(sv_main_frame)
        sv_content_frame.pack(fill="both", expand=True, pady=5)
    
        sv_form_frame = ttk.LabelFrame(sv_content_frame, text="Thông tin Sinh viên", padding=10)
        sv_form_frame.grid(row=0, column=0, rowspan=3, padx=(0,10), sticky="ns")
    
        ttk.Label(sv_form_frame, text="Họ tên:").grid(row=0, column=0, sticky="w", pady=5)
        self.sv_ho_ten_entry = ttk.Entry(sv_form_frame, width=30)
        self.sv_ho_ten_entry.grid(row=0, column=1, sticky="ew", pady=5)
        ttk.Label(sv_form_frame, text="MSSV:").grid(row=1, column=0, sticky="w", pady=5)
        self.sv_mssv_entry = ttk.Entry(sv_form_frame, width=30)
        self.sv_mssv_entry.grid(row=1, column=1, sticky="ew", pady=5)
        ttk.Label(sv_form_frame, text="Email:").grid(row=2, column=0, sticky="w", pady=5)
        self.sv_email_entry = ttk.Entry(sv_form_frame, width=30)
        self.sv_email_entry.grid(row=2, column=1, sticky="ew", pady=5)
        ttk.Label(sv_form_frame, text="Điểm TB (tự tính):").grid(row=3, column=0, sticky="w", pady=5)
        self.sv_diem_tb_entry = ttk.Entry(sv_form_frame, width=30, state="readonly")
        self.sv_diem_tb_entry.grid(row=3, column=1, sticky="ew", pady=5)
        ttk.Label(sv_form_frame, text="Lớp:").grid(row=4, column=0, sticky="w", pady=5)
        self.sv_lop_combo = ttk.Combobox(sv_form_frame, state="readonly", width=28)
        self.sv_lop_combo.grid(row=4, column=1, sticky="ew", pady=5)

        sv_crud_button_frame = ttk.LabelFrame(sv_form_frame, text="Chức năng Cơ bản", padding=10)
        sv_crud_button_frame.grid(row=5, column=0, columnspan=2, sticky="ew", pady=10)
    
        ttk.Button(sv_crud_button_frame, text=" Thêm", image=self.addsv_icon, compound='left', command=self.add_student).pack(side="left", expand=True, fill="x", padx=5)
        ttk.Button(sv_crud_button_frame, text=" Cập nhật", image=self.update_icon, compound='left', command=self.update_student).pack(side="left", expand=True, fill="x", padx=5)
        ttk.Button(sv_crud_button_frame, text=" Xóa", image=self.delete_icon, compound='left', command=self.delete_student).pack(side="left", expand=True, fill="x", padx=5)
        ttk.Button(sv_crud_button_frame, text=" Xóa Form", image=self.clear_icon, compound='left', command=self.clear_sv_form).pack(side="left", expand=True, fill="x", padx=5)
    
        sv_adv_button_frame = ttk.LabelFrame(sv_form_frame, text="Chức năng Nâng cao", padding=10)
        sv_adv_button_frame.grid(row=6, column=0, columnspan=2, sticky="ew", pady=5)
        ttk.Button(sv_adv_button_frame, text="Thống kê điểm TB", command=self.show_statistics).pack(fill="x", pady=2)
        ttk.Button(sv_adv_button_frame, text="Vẽ biểu đồ điểm TB", command=self.draw_chart).pack(fill="x", pady=2)
        ttk.Button(sv_adv_button_frame, text="Gửi Báo cáo Email", command=self.open_email_dialog).pack(fill="x", pady=2)
    
        sv_tree_frame = ttk.Frame(sv_content_frame)
        sv_tree_frame.grid(row=0, column=1, padx=(10,0), sticky="nsew")
    
        self.sv_tree = ttk.Treeview(sv_tree_frame, columns=("ID", "HoTen", "MSSV", "Email", "DiemTB", "Lop", "Khoa"), show="headings")
        self.sv_tree.heading("ID", text="ID"); self.sv_tree.heading("HoTen", text="Họ tên"); self.sv_tree.heading("MSSV", text="MSSV")
        self.sv_tree.heading("Email", text="Email"); self.sv_tree.heading("DiemTB", text="Điểm TB"); self.sv_tree.heading("Lop", text="Lớp"); self.sv_tree.heading("Khoa", text="Khoa")
        self.sv_tree.column("ID", width=30, anchor="center"); self.sv_tree.column("HoTen", width=150); self.sv_tree.column("MSSV", width=80)
        self.sv_tree.column("Email", width=150); self.sv_tree.column("DiemTB", width=60, anchor="center"); self.sv_tree.column("Lop", width=100); self.sv_tree.column("Khoa", width=120)
    
        sv_pagination_frame = ttk.Frame(sv_tree_frame)
        sv_pagination_frame.pack(side="bottom", fill="x", pady=(5,0))
        self.sv_prev_button = ttk.Button(sv_pagination_frame, text="<< Trang trước", command=self.sv_go_to_prev_page)
        self.sv_prev_button.pack(side="left", padx=5)
        self.sv_page_label = ttk.Label(sv_pagination_frame, text="Trang 1 / 1")
        self.sv_page_label.pack(side="left", expand=True)
        self.sv_next_button = ttk.Button(sv_pagination_frame, text="Trang sau >>", command=self.sv_go_to_next_page)
        self.sv_next_button.pack(side="right", padx=5)
    
        self.sv_tree.pack(side="top", fill="both", expand=True)
    
        self.sv_tree.bind("<<TreeviewSelect>>", self.on_sv_select)
        self.sv_context_menu = tk.Menu(self.sv_tree, tearoff=0)
        self.sv_context_menu.add_command(label="Xem/Nhập điểm chi tiết", command=self.open_grades_window)
        self.sv_tree.bind("<Button-3>", self.show_sv_context_menu)
    
        sv_content_frame.grid_columnconfigure(1, weight=1)
        sv_content_frame.grid_rowconfigure(0, weight=1)

    def create_lop_tab(self):
        lop_main_frame = ttk.Frame(self.tab_lop)
        lop_main_frame.pack(fill="both", expand=True)
        
        lop_filter_frame = ttk.LabelFrame(lop_main_frame, text="Bộ lọc", padding=10)
        lop_filter_frame.pack(fill="x", padx=10, pady=5)
        ttk.Label(lop_filter_frame, text="Lọc theo Khoa:").pack(side="left", padx=5)
        self.lop_filter_khoa_combo = ttk.Combobox(lop_filter_frame, state="readonly", width=30)
        self.lop_filter_khoa_combo.pack(side="left", padx=5)
        self.lop_filter_khoa_combo.bind("<<ComboboxSelected>>", self.load_lop_data)
        ttk.Button(lop_filter_frame, text="Bỏ lọc", command=self.clear_lop_filter).pack(side="left", padx=5)

        lop_content_frame = ttk.Frame(lop_main_frame)
        lop_content_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        lop_form_frame = ttk.LabelFrame(lop_content_frame, text="Thông tin Lớp", padding=10)
        lop_form_frame.grid(row=0, column=0, rowspan=2, padx=(0,10), sticky="ns")
        ttk.Label(lop_form_frame, text="Tên Lớp:").grid(row=0, column=0, sticky="w", pady=5)
        self.lop_ten_entry = ttk.Entry(lop_form_frame, width=30)
        self.lop_ten_entry.grid(row=0, column=1, sticky="ew", pady=5)
        ttk.Label(lop_form_frame, text="Thuộc Khoa:").grid(row=1, column=0, sticky="w", pady=5)
        self.lop_khoa_combo = ttk.Combobox(lop_form_frame, state="readonly", width=28)
        self.lop_khoa_combo.grid(row=1, column=1, sticky="ew", pady=5)
        
        lop_button_frame = ttk.LabelFrame(lop_form_frame, text="Chức năng", padding=10)
        lop_button_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")
        ttk.Button(lop_button_frame, text=" Thêm", image=self.add_icon, compound='left', command=self.add_lop).pack(side="left", expand=True, fill="x", padx=5)
        ttk.Button(lop_button_frame, text=" Cập nhật", image=self.update_icon, compound='left', command=self.update_lop).pack(side="left", expand=True, fill="x", padx=5)
        ttk.Button(lop_button_frame, text=" Xóa", image=self.delete_icon, compound='left', command=self.delete_lop).pack(side="left", expand=True, fill="x", padx=5)
        ttk.Button(lop_button_frame, text=" Xóa Form", image=self.clear_icon, compound='left', command=self.clear_lop_form).pack(side="left", expand=True, fill="x", padx=5)
        
        lop_tree_frame = ttk.Frame(lop_content_frame)
        lop_tree_frame.grid(row=0, column=1, padx=(10,0), sticky="nsew")
        
        self.lop_tree = ttk.Treeview(lop_tree_frame, columns=("ID", "TenLop", "TenKhoa"), show="headings")
        self.lop_tree.heading("ID", text="ID"); self.lop_tree.heading("TenLop", text="Tên Lớp"); self.lop_tree.heading("TenKhoa", text="Tên Khoa")
        self.lop_tree.column("ID", width=50, anchor="center"); self.lop_tree.column("TenLop", width=200); self.lop_tree.column("TenKhoa", width=250)
        
        scrollbar_lop = ttk.Scrollbar(lop_tree_frame, orient="vertical", command=self.lop_tree.yview)
        self.lop_tree.configure(yscrollcommand=scrollbar_lop.set)
        self.lop_tree.pack(side="left", fill="both", expand=True)
        scrollbar_lop.pack(side="right", fill="y")
        self.lop_tree.bind("<<TreeviewSelect>>", self.on_lop_select)
        
        lop_content_frame.grid_columnconfigure(1, weight=1)
        lop_content_frame.grid_rowconfigure(0, weight=1)

    def create_khoa_tab(self):
        khoa_main_frame = ttk.Frame(self.tab_khoa)
        khoa_main_frame.pack(fill="both", expand=True)
        khoa_form_frame = ttk.LabelFrame(khoa_main_frame, text="Thông tin Khoa", padding=10)
        khoa_form_frame.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="ns")
        ttk.Label(khoa_form_frame, text="Tên Khoa:").grid(row=0, column=0, sticky="w", pady=5)
        self.khoa_ten_entry = ttk.Entry(khoa_form_frame, width=30)
        self.khoa_ten_entry.grid(row=0, column=1, sticky="ew", pady=5)
        khoa_button_frame = ttk.LabelFrame(khoa_form_frame, text="Chức năng", padding=10)
        khoa_button_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")
        ttk.Button(khoa_button_frame, text=" Thêm", image=self.add_icon, compound='left', command=self.add_khoa).pack(side="left", expand=True, fill="x", padx=5)
        ttk.Button(khoa_button_frame, text=" Cập nhật", image=self.update_icon, compound='left', command=self.update_khoa).pack(side="left", expand=True, fill="x", padx=5)
        ttk.Button(khoa_button_frame, text=" Xóa", image=self.delete_icon, compound='left', command=self.delete_khoa).pack(side="left", expand=True, fill="x", padx=5)
        ttk.Button(khoa_button_frame, text=" Xóa Form", image=self.clear_icon, compound='left', command=self.clear_khoa_form).pack(side="left", expand=True, fill="x", padx=5)
        khoa_tree_frame = ttk.Frame(khoa_main_frame)
        khoa_tree_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.khoa_tree = ttk.Treeview(khoa_tree_frame, columns=("ID", "TenKhoa"), show="headings")
        self.khoa_tree.heading("ID", text="ID"); self.khoa_tree.heading("TenKhoa", text="Tên Khoa")
        self.khoa_tree.column("ID", width=50, anchor="center"); self.khoa_tree.column("TenKhoa", width=400)
        scrollbar_khoa = ttk.Scrollbar(khoa_tree_frame, orient="vertical", command=self.khoa_tree.yview)
        self.khoa_tree.configure(yscrollcommand=scrollbar_khoa.set)
        self.khoa_tree.pack(side="left", fill="both", expand=True)
        scrollbar_khoa.pack(side="right", fill="y")
        self.khoa_tree.bind("<<TreeviewSelect>>", self.on_khoa_select)
        khoa_main_frame.grid_columnconfigure(1, weight=1)
        khoa_main_frame.grid_rowconfigure(0, weight=1)

    def create_mon_hoc_tab(self):
        mh_main_frame = ttk.Frame(self.tab_mon_hoc)
        mh_main_frame.pack(fill="both", expand=True)
        mh_form_frame = ttk.LabelFrame(mh_main_frame, text="Thông tin Môn học", padding=10)
        mh_form_frame.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="ns")
        ttk.Label(mh_form_frame, text="Tên Môn học:").grid(row=0, column=0, sticky="w", pady=5)
        self.mh_ten_entry = ttk.Entry(mh_form_frame, width=30)
        self.mh_ten_entry.grid(row=0, column=1, sticky="ew", pady=5)
        ttk.Label(mh_form_frame, text="Số tín chỉ:").grid(row=1, column=0, sticky="w", pady=5)
        self.mh_tin_chi_entry = ttk.Entry(mh_form_frame, width=30)
        self.mh_tin_chi_entry.grid(row=1, column=1, sticky="ew", pady=5)
        ttk.Label(mh_form_frame, text="Thuộc Khoa:").grid(row=2, column=0, sticky="w", pady=5)
        self.mh_khoa_combo = ttk.Combobox(mh_form_frame, state="readonly", width=28)
        self.mh_khoa_combo.grid(row=2, column=1, sticky="ew", pady=5)
        mh_button_frame = ttk.LabelFrame(mh_form_frame, text="Chức năng", padding=10)
        mh_button_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")
        ttk.Button(mh_button_frame, text=" Thêm", image=self.add_icon, compound='left', command=self.add_mon_hoc).pack(side="left", expand=True, fill="x", padx=5)
        mh_tree_frame = ttk.Frame(mh_main_frame)
        mh_tree_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.mh_tree = ttk.Treeview(mh_tree_frame, columns=("ID", "TenMon", "SoTinChi", "TenKhoa"), show="headings")
        self.mh_tree.heading("ID", text="ID"); self.mh_tree.heading("TenMon", text="Tên Môn học"); self.mh_tree.heading("SoTinChi", text="Tín chỉ"); self.mh_tree.heading("TenKhoa", text="Tên Khoa")
        self.mh_tree.column("ID", width=50, anchor="center"); self.mh_tree.column("TenMon", width=250); self.mh_tree.column("SoTinChi", width=60, anchor="center"); self.mh_tree.column("TenKhoa", width=200)
        scrollbar_mh = ttk.Scrollbar(mh_tree_frame, orient="vertical", command=self.mh_tree.yview)
        self.mh_tree.configure(yscrollcommand=scrollbar_mh.set)
        self.mh_tree.pack(side="left", fill="both", expand=True)
        scrollbar_mh.pack(side="right", fill="y")
        mh_main_frame.grid_columnconfigure(1, weight=1)
        mh_main_frame.grid_rowconfigure(0, weight=1)

    def debounce(self, func, delay):
        def wrapper(*args, **kwargs):
            if self._after_id:
                self.root.after_cancel(self._after_id)
            self._after_id = self.root.after(delay, lambda: func(*args, **kwargs))
        return wrapper

    def load_khoa_data(self):
        try:
            for item in self.khoa_tree.get_children(): self.khoa_tree.delete(item)
            ds_khoa = self.db.hien_thi_ds_khoa()
            self.khoa_map = {khoa['ten_khoa']: khoa['id'] for khoa in ds_khoa}
            for khoa in ds_khoa: self.khoa_tree.insert("", "end", values=(khoa['id'], khoa['ten_khoa']))
            self.load_khoa_to_comboboxes()
        except Error as e: messagebox.showerror("Lỗi", f"Không thể tải ds khoa: {e}")
        
    def load_khoa_to_comboboxes(self):
        khoa_names = list(self.khoa_map.keys())
        self.lop_khoa_combo['values'] = khoa_names
        self.mh_khoa_combo['values'] = khoa_names
        self.lop_filter_khoa_combo['values'] = ["Tất cả"] + khoa_names
        self.sv_filter_khoa_combo['values'] = ["Tất cả"] + khoa_names

    def add_khoa(self):
        ten_khoa = self.khoa_ten_entry.get()
        if not ten_khoa: messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập tên khoa."); return
        try: self.db.them_khoa(ten_khoa); self.clear_khoa_form(); self.load_khoa_data()
        except Error as e: messagebox.showerror("Lỗi", f"Không thể thêm khoa (có thể do trùng tên): {e}")
        
    def update_khoa(self):
        selected_item = self.khoa_tree.focus()
        if not selected_item: messagebox.showwarning("Chưa chọn", "Vui lòng chọn một khoa."); return
        ten_khoa = self.khoa_ten_entry.get()
        if not ten_khoa: messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập tên khoa."); return
        try:
            id_khoa = self.khoa_tree.item(selected_item)['values'][0]
            if self.db.cap_nhat_khoa(id_khoa, ten_khoa): self.clear_khoa_form(); self.load_khoa_data(); self.load_lop_data()
        except Error as e: messagebox.showerror("Lỗi", f"Không thể cập nhật khoa: {e}")
        
    def delete_khoa(self):
        selected_item = self.khoa_tree.focus()
        if not selected_item: messagebox.showwarning("Chưa chọn", "Vui lòng chọn một khoa."); return
        if messagebox.askyesno("Xác nhận xóa", "Xóa khoa sẽ khiến các lớp và môn học thuộc khoa này không xác định.\nBạn có chắc chắn?"):
            try: id_khoa = self.khoa_tree.item(selected_item)['values'][0]; self.db.xoa_khoa(id_khoa); self.clear_khoa_form(); self.load_khoa_data()
            except Error as e: messagebox.showerror("Lỗi", f"Không thể xóa khoa: {e}")
            
    def clear_khoa_form(self):
        self.khoa_ten_entry.delete(0, "end")
        if self.khoa_tree.selection(): self.khoa_tree.selection_remove(self.khoa_tree.selection()[0])
        
    def on_khoa_select(self, event):
        selected_item = self.khoa_tree.focus()
        if not selected_item: return
        values = self.khoa_tree.item(selected_item)['values']
        self.khoa_ten_entry.delete(0, 'end'); self.khoa_ten_entry.insert(0, values[1])

    def load_lop_data(self, event=None):
        try:
            khoa_id = None
            selected_khoa = self.lop_filter_khoa_combo.get()
            if selected_khoa and selected_khoa != "Tất cả":
                khoa_id = self.khoa_map[selected_khoa]
            for item in self.lop_tree.get_children(): self.lop_tree.delete(item)
            ds_lop = self.db.hien_thi_ds_lop(khoa_id)
            for lop in ds_lop: self.lop_tree.insert("", "end", values=(lop['id'], lop['ten_lop'], lop['ten_khoa'] or "N/A"))
            self.load_lop_to_sv_combobox()
        except Error as e: messagebox.showerror("Lỗi", f"Không thể tải ds lớp: {e}")
        
    def clear_lop_filter(self):
        self.lop_filter_khoa_combo.set('')
        self.load_lop_data()
        
    def add_lop(self):
        ten_lop = self.lop_ten_entry.get(); ten_khoa = self.lop_khoa_combo.get()
        if not ten_lop or not ten_khoa: messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập tên lớp và chọn khoa."); return
        try: self.db.them_lop(ten_lop, self.khoa_map[ten_khoa]); self.clear_lop_form(); self.load_lop_data()
        except Error as e: messagebox.showerror("Lỗi", f"Không thể thêm lớp (có thể do trùng tên): {e}")
        
    def update_lop(self):
        selected_item = self.lop_tree.focus()
        if not selected_item: messagebox.showwarning("Chưa chọn", "Vui lòng chọn một lớp."); return
        ten_lop = self.lop_ten_entry.get(); ten_khoa = self.lop_khoa_combo.get()
        if not ten_lop or not ten_khoa: messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập tên lớp và chọn khoa."); return
        try:
            id_lop = self.lop_tree.item(selected_item)['values'][0]
            khoa_id = self.khoa_map[ten_khoa]
            self.db.cap_nhat_lop(id_lop, ten_lop, khoa_id); self.clear_lop_form(); self.load_lop_data()
        except Error as e: messagebox.showerror("Lỗi", f"Không thể cập nhật lớp: {e}")
        
    def delete_lop(self):
        selected_item = self.lop_tree.focus()
        if not selected_item: messagebox.showwarning("Chưa chọn", "Vui lòng chọn một lớp."); return
        if messagebox.askyesno("Xác nhận xóa", "Xóa lớp sẽ khiến sinh viên thuộc lớp này không xác định.\nBạn có chắc chắn?"):
            try: id_lop = self.lop_tree.item(selected_item)['values'][0]; self.db.xoa_lop(id_lop); self.clear_lop_form(); self.load_lop_data()
            except Error as e: messagebox.showerror("Lỗi", f"Không thể xóa lớp: {e}")
            
    def clear_lop_form(self):
        self.lop_ten_entry.delete(0, 'end'); self.lop_khoa_combo.set('')
        if self.lop_tree.selection(): self.lop_tree.selection_remove(self.lop_tree.selection()[0])
        
    def on_lop_select(self, event):
        selected_item = self.lop_tree.focus()
        if not selected_item: return
        values = self.lop_tree.item(selected_item)['values']
        self.lop_ten_entry.delete(0, 'end'); self.lop_ten_entry.insert(0, values[1])
        self.lop_khoa_combo.set(values[2] if values[2] != "N/A" else "")

    def load_mon_hoc_data(self):
        try:
            for item in self.mh_tree.get_children(): self.mh_tree.delete(item)
            ds_mh = self.db.hien_thi_ds_mon_hoc()
            for mh in ds_mh: self.mh_tree.insert("", "end", values=(mh['id'], mh['ten_mon_hoc'], mh['so_tin_chi'], mh['ten_khoa'] or "N/A"))
        except Error as e: messagebox.showerror("Lỗi", f"Không thể tải danh sách môn học: {e}")
        
    def add_mon_hoc(self):
        ten_mh = self.mh_ten_entry.get(); tin_chi = self.mh_tin_chi_entry.get(); ten_khoa = self.mh_khoa_combo.get()
        if not ten_mh or not tin_chi or not ten_khoa: messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đủ thông tin môn học."); return
        try:
            khoa_id = self.khoa_map[ten_khoa]
            self.db.them_mon_hoc(ten_mh, int(tin_chi), khoa_id)
            self.mh_ten_entry.delete(0,'end'); self.mh_tin_chi_entry.delete(0,'end'); self.mh_khoa_combo.set('')
            self.load_mon_hoc_data()
        except ValueError: messagebox.showerror("Lỗi", "Số tín chỉ phải là một con số.")
        except Error as e: messagebox.showerror("Lỗi", f"Không thể thêm môn học: {e}")

    def reset_and_load_sv(self, event=None):
        self.sv_current_page = 1
        self.load_sv_data()

    def load_sv_data(self, event=None):
        try:
            khoa_id, lop_id, search_term = self.get_sv_filters()
            self.sv_total_records = self.db.dem_so_sinh_vien(khoa_id, lop_id, search_term)
            self.sv_total_pages = math.ceil(self.sv_total_records / self.sv_page_size) if self.sv_total_records > 0 else 1
            if self.sv_current_page > self.sv_total_pages: self.sv_current_page = self.sv_total_pages

            for item in self.sv_tree.get_children(): self.sv_tree.delete(item)
            
            ds_sv = self.db.hien_thi_danh_sach(khoa_id, lop_id, search_term, self.sv_current_page, self.sv_page_size)
            for sv in ds_sv: self.sv_tree.insert("", "end", values=(sv['id'], sv['ho_ten'], sv['mssv'], sv['email'], f"{sv['diem_tb']:.2f}" if sv['diem_tb'] is not None else "N/A", sv['ten_lop'] or "N/A", sv['ten_khoa'] or "N/A"))

            self.update_sv_pagination_controls()
        except Error as e: messagebox.showerror("Lỗi", f"Không thể tải ds sinh viên: {e}")

    def get_sv_filters(self):
        khoa_id = None; selected_khoa = self.sv_filter_khoa_combo.get()
        if selected_khoa and selected_khoa != "Tất cả": khoa_id = self.khoa_map[selected_khoa]
        lop_id = None; selected_lop = self.sv_filter_lop_combo.get()
        if selected_lop and selected_lop != "Tất cả" and hasattr(self, 'lop_map_filter'): lop_id = self.lop_map_filter[selected_lop]
        search_term = self.sv_search_entry.get()
        return khoa_id, lop_id, search_term

    def update_sv_pagination_controls(self):
        self.sv_page_label.config(text=f"Trang {self.sv_current_page} / {self.sv_total_pages} (Tổng số: {self.sv_total_records})")
        self.sv_prev_button.config(state="normal" if self.sv_current_page > 1 else "disabled")
        self.sv_next_button.config(state="normal" if self.sv_current_page < self.sv_total_pages else "disabled")

    def sv_go_to_prev_page(self):
        if self.sv_current_page > 1: self.sv_current_page -= 1; self.load_sv_data()
    def sv_go_to_next_page(self):
        if self.sv_current_page < self.sv_total_pages: self.sv_current_page += 1; self.load_sv_data()
        
    def load_lop_to_sv_combobox(self):
        try:
            ds_lop = self.db.hien_thi_ds_lop()
            self.lop_map_sv = {f"{lop['ten_lop']} ({lop['ten_khoa'] or 'N/A'})": lop['id'] for lop in ds_lop}
            self.sv_lop_combo['values'] = list(self.lop_map_sv.keys())
        except Error as e: messagebox.showerror("Lỗi", f"Không thể tải lớp cho combobox: {e}")
        
    def on_sv_filter_khoa_select(self, event=None):
        self.sv_current_page = 1
        khoa_id = None; selected_khoa = self.sv_filter_khoa_combo.get()
        if selected_khoa and selected_khoa != "Tất cả": khoa_id = self.khoa_map[selected_khoa]
        ds_lop = self.db.hien_thi_ds_lop(khoa_id)
        self.lop_map_filter = {lop['ten_lop']: lop['id'] for lop in ds_lop}
        self.sv_filter_lop_combo['values'] = ["Tất cả"] + list(self.lop_map_filter.keys())
        self.sv_filter_lop_combo.set('Tất cả')
        self.load_sv_data()
        
    def clear_sv_filter(self):
        self.sv_current_page = 1
        self.sv_filter_khoa_combo.set(''); self.sv_filter_lop_combo.set(''); self.sv_search_entry.delete(0, 'end')
        self.on_sv_filter_khoa_select()
        
    def is_valid_email(self, email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

    def add_student(self):
        ho_ten, mssv, email, lop_text = self.sv_ho_ten_entry.get(), self.sv_mssv_entry.get(), self.sv_email_entry.get(), self.sv_lop_combo.get()
        if not all([ho_ten, mssv, email, lop_text]):
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin.")
            return
        if not self.is_valid_email(email):
            messagebox.showwarning("Email không hợp lệ", "Vui lòng nhập email hợp lệ.")
            return
        try:
            lop_id = self.lop_map_sv[lop_text]
            sv = SinhVien(None, ho_ten, mssv, email, 0.0, lop_id)
            self.db.them_sinh_vien(sv); self.clear_sv_form(); self.load_sv_data()
        except Error as e: messagebox.showerror("Lỗi Database", f"Không thể thêm sinh viên: {e}")
        
    def update_student(self):
        selected_item = self.sv_tree.focus()
        if not selected_item: messagebox.showwarning("Chưa chọn", "Vui lòng chọn sinh viên."); return
        try:
            id_sv = self.sv_tree.item(selected_item)['values'][0]
            ho_ten, mssv, email = self.sv_ho_ten_entry.get(), self.sv_mssv_entry.get(), self.sv_email_entry.get()
            lop_text = self.sv_lop_combo.get()
            if not all([ho_ten, mssv, email, lop_text]): messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ."); return
            lop_id = self.lop_map_sv[lop_text]
            diem_tb_str = self.sv_diem_tb_entry.get()
            diem_tb = 0.0 if diem_tb_str == "N/A" else float(diem_tb_str)
            if self.db.cap_nhat_sinh_vien(id_sv, ho_ten, mssv, email, diem_tb, lop_id):
                self.clear_sv_form(); self.load_sv_data()
        except Error as e: messagebox.showerror("Lỗi Database", f"Không thể cập nhật: {e}")
        
    def delete_student(self):
        selected_item = self.sv_tree.focus()
        if not selected_item: messagebox.showwarning("Chưa chọn", "Vui lòng chọn sinh viên."); return
        if messagebox.askyesno("Xác nhận xóa", "Bạn có chắc chắn muốn xóa sinh viên này?"):
            try: id_sv = self.sv_tree.item(selected_item)['values'][0]; self.db.xoa_sinh_vien(id_sv); self.clear_sv_form(); self.load_sv_data()
            except Error as e: messagebox.showerror("Lỗi Database", f"Không thể xóa: {e}")
            
    def clear_sv_form(self):
        self.sv_ho_ten_entry.delete(0, "end"); self.sv_mssv_entry.delete(0, "end")
        self.sv_email_entry.delete(0, "end"); self.sv_lop_combo.set('')
        self.sv_diem_tb_entry.config(state="normal"); self.sv_diem_tb_entry.delete(0, "end"); self.sv_diem_tb_entry.config(state="readonly")
        if self.sv_tree.selection(): self.sv_tree.selection_remove(self.sv_tree.selection()[0])
        self.sv_ho_ten_entry.focus_set()

    def on_sv_select(self, event):
        selected_item = self.sv_tree.focus()
        if not selected_item: return
        values = self.sv_tree.item(selected_item)['values']
        self.clear_sv_form()
        self.sv_ho_ten_entry.insert(0, values[1]); self.sv_mssv_entry.insert(0, values[2])
        self.sv_email_entry.insert(0, values[3]); 
        self.sv_diem_tb_entry.config(state="normal"); self.sv_diem_tb_entry.delete(0, "end"); self.sv_diem_tb_entry.insert(0, values[4]); self.sv_diem_tb_entry.config(state="readonly")
        lop_text = f"{values[5]} ({values[6]})" if values[5] != "N/A" else ""
        if lop_text in self.sv_lop_combo['values']: self.sv_lop_combo.set(lop_text)
        
    def show_sv_context_menu(self, event):
        iid = self.sv_tree.identify_row(event.y)
        if iid: self.sv_tree.selection_set(iid); self.sv_context_menu.post(event.x_root, event.y_root)
        
    def open_grades_window(self):
        selected_item = self.sv_tree.focus()
        if not selected_item: return
        sv_data = self.sv_tree.item(selected_item)['values']
        GradesWindow(self.root, self.db, sv_data[0], sv_data[1], self.refresh_all_data)

    def show_statistics(self):
        try:
            diem_list = self.db.get_diem_list()
            if not diem_list:
                messagebox.showinfo("Thống kê", "Không có dữ liệu điểm để thống kê.")
                return
            
            diem_array = np.array(diem_list)
            stats = {
                'mean': np.mean(diem_array), 'median': np.median(diem_array),
                'std_dev': np.std(diem_array), 'max_score': np.max(diem_array),
                'min_score': np.min(diem_array), 'count': len(diem_array)
            }

            stats_window = tk.Toplevel(self.root)
            stats_window.title("Thống kê Điểm số TB")
            stats_window.geometry("300x200")
            
            tk.Label(stats_window, text="BẢNG THỐNG KÊ ĐIỂM SỐ", font=("Helvetica", 12, "bold")).pack(pady=10)
            for key, value in stats.items():
                tk.Label(stats_window, text=f"{key.replace('_',' ').title()}: {value:.2f}").pack(anchor="w", padx=20)
        except Error as e:
            messagebox.showerror("Lỗi", f"Không thể lấy dữ liệu thống kê: {e}")

    def draw_chart(self):
        try:
            diem_list = self.db.get_diem_list()
            if not diem_list:
                messagebox.showwarning("Thiếu dữ liệu", "Không có dữ liệu điểm để vẽ biểu đồ.")
                return

            chart_window = tk.Toplevel(self.root)
            chart_window.title("Biểu đồ Phổ điểm")
            chart_window.geometry("800x600")

            fig = Figure(figsize=(8, 6), dpi=100)
            ax = fig.add_subplot(111)
            ax.hist(diem_list, bins=10, color='skyblue', edgecolor='black')
            ax.set_title('Phổ Điểm Sinh Viên')
            ax.set_xlabel('Điểm Trung Bình')
            ax.set_ylabel('Số Lượng Sinh Viên')
            ax.grid(True, linestyle='--', alpha=0.6)

            canvas = FigureCanvasTkAgg(fig, master=chart_window)
            canvas.draw()
            
            toolbar = NavigationToolbar2Tk(canvas, chart_window)
            toolbar.update()
            
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        except Error as e:
            messagebox.showerror("Lỗi", f"Không thể lấy dữ liệu để vẽ biểu đồ: {e}")

    def open_email_dialog(self):
        sender_email = os.getenv("GMAIL_SENDER")
        sender_password = os.getenv("GMAIL_APP_PASSWORD")

        if not sender_email or not sender_password:
            messagebox.showerror("Lỗi Cấu hình", "Vui lòng thiết lập GMAIL_SENDER và GMAIL_APP_PASSWORD trong file .env")
            return

        email_dialog = tk.Toplevel(self.root)
        email_dialog.title("Gửi báo cáo Email")
        email_dialog.geometry("350x150")
        
        tk.Label(email_dialog, text=f"Gửi từ: {sender_email}", fg="blue").pack(pady=10)
        
        tk.Label(email_dialog, text="Email người nhận:").pack(pady=5)
        recipient_entry = tk.Entry(email_dialog, width=40)
        recipient_entry.pack()
        recipient_entry.focus()

        def send():
            nguoi_nhan = recipient_entry.get()
            if not nguoi_nhan:
                messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập email người nhận.", parent=email_dialog)
                return
            
            try:
                diem_list = self.db.get_diem_list()
                if not diem_list: 
                    messagebox.showerror("Lỗi", "Không có dữ liệu để tạo báo cáo.", parent=email_dialog)
                    return
                
                diem_array = np.array(diem_list)
                stats = {'mean': np.mean(diem_array), 'median': np.median(diem_array), 'std_dev': np.std(diem_array), 
                         'max_score': np.max(diem_array), 'min_score': np.min(diem_array), 'count': len(diem_array)}
                
                fig = Figure(figsize=(8, 6)); ax = fig.add_subplot(111)
                ax.hist(diem_list, bins=10, color='skyblue', edgecolor='black'); ax.set_title('Phổ Điểm Sinh Viên')
                ten_file_anh = 'phodiem_sinhvien.png'; fig.savefig(ten_file_anh)
                
                msg = MIMEMultipart(); msg['Subject'] = 'Báo cáo Thống kê Điểm số Sinh viên'; msg['From'] = sender_email; msg['To'] = nguoi_nhan
                
                body = f"""
                Xin chào,
                Đây là báo cáo thống kê điểm số sinh viên tự động từ ứng dụng Python.
                --- SỐ LIỆU THỐNG KÊ ---
                - Số lượng sinh viên: {stats['count']}
                - Điểm trung bình: {stats['mean']:.2f}
                - Điểm trung vị: {stats['median']:.2f}
                - Điểm cao nhất: {stats['max_score']:.2f}
                - Điểm thấp nhất: {stats['min_score']:.2f}
                Biểu đồ phân bố điểm được đính kèm trong email này.
                """
                msg.attach(MIMEText(body, 'plain'))
                
                with open(ten_file_anh, 'rb') as f: 
                    img = MIMEImage(f.read())
                    img.add_header('Content-Disposition', 'attachment', filename=os.path.basename(ten_file_anh))
                    msg.attach(img)
                
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)
                server.quit()
                
                messagebox.showinfo("Thành công", f"Gửi email báo cáo thành công tới {nguoi_nhan}!", parent=email_dialog)
                email_dialog.destroy()
            except Exception as e:
                messagebox.showerror("Lỗi Email", f"Lỗi khi gửi: {e}", parent=email_dialog)

        ttk.Button(email_dialog, text="Gửi", command=send).pack(pady=10)

class GradesWindow(tk.Toplevel):
    def __init__(self, parent, db_manager, sv_id, sv_ten, refresh_callback):
        super().__init__(parent)
        self.db = db_manager
        self.sv_id = sv_id
        self.refresh_main_window = refresh_callback
        self.title(f"Bảng điểm - {sv_ten} (ID: {sv_id})")
        self.geometry("800x500")
        self.create_widgets()
        self.load_data()
    def create_widgets(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        tree_frame = tk.LabelFrame(main_frame, text="Bảng điểm chi tiết", padx=10, pady=10)
        tree_frame.pack(fill="both", expand=True)
        self.diem_tree = ttk.Treeview(tree_frame, columns=("MonHoc", "TinChi", "DiemCC", "DiemGK", "DiemCK"), show="headings")
        self.diem_tree.heading("MonHoc", text="Tên Môn học"); self.diem_tree.heading("TinChi", text="Tín chỉ"); self.diem_tree.heading("DiemCC", text="Điểm CC")
        self.diem_tree.heading("DiemGK", text="Điểm GK"); self.diem_tree.heading("DiemCK", text="Điểm CK")
        self.diem_tree.column("MonHoc", width=250); self.diem_tree.column("TinChi", width=60, anchor="center"); self.diem_tree.column("DiemCC", width=80, anchor="center")
        self.diem_tree.column("DiemGK", width=80, anchor="center"); self.diem_tree.column("DiemCK", width=80, anchor="center")
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.diem_tree.yview)
        self.diem_tree.configure(yscrollcommand=scrollbar.set)
        self.diem_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.diem_tree.bind("<<TreeviewSelect>>", self.on_grade_select)
        form_frame = tk.LabelFrame(main_frame, text="Nhập/Cập nhật điểm", padx=10, pady=10)
        form_frame.pack(fill="x", pady=10)
        tk.Label(form_frame, text="Môn học:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.mh_combo = ttk.Combobox(form_frame, state="readonly", width=30)
        self.mh_combo.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky="ew")
        tk.Label(form_frame, text="Điểm CC:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.cc_entry = tk.Entry(form_frame, width=10); self.cc_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        tk.Label(form_frame, text="Điểm GK:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.gk_entry = tk.Entry(form_frame, width=10); self.gk_entry.grid(row=1, column=3, padx=5, pady=5, sticky="ew")
        tk.Label(form_frame, text="Điểm CK:").grid(row=1, column=4, padx=5, pady=5, sticky="w")
        self.ck_entry = tk.Entry(form_frame, width=10); self.ck_entry.grid(row=1, column=5, padx=5, pady=5, sticky="ew")
        button_form_frame = ttk.Frame(form_frame)
        button_form_frame.grid(row=2, column=0, columnspan=6, pady=5, sticky="ew")
        button_form_frame.columnconfigure((0,1), weight=1)
        tk.Button(button_form_frame, text="Lưu điểm", command=self.save_grade).pack(side="left", fill="x", expand=True, padx=5)
        tk.Button(button_form_frame, text="Xóa Form", command=self.clear_grade_form).pack(side="left", fill="x", expand=True, padx=5)
        tk.Button(main_frame, text="Tính lại & Cập nhật ĐTB", command=self.recalculate_gpa).pack(pady=10)
        form_frame.grid_columnconfigure(1, weight=1); form_frame.grid_columnconfigure(3, weight=1); form_frame.grid_columnconfigure(5, weight=1)

    def load_data(self):
        try:
            for item in self.diem_tree.get_children(): self.diem_tree.delete(item)
            ds_diem = self.db.hien_thi_diem_cua_sv(self.sv_id)
            for diem in ds_diem: self.diem_tree.insert("", "end", values=list(diem.values()))
            ds_mon_hoc = self.db.hien_thi_ds_mon_hoc()
            self.mon_hoc_map = {mh['ten_mon_hoc']: mh['id'] for mh in ds_mon_hoc}
            self.mh_combo['values'] = list(self.mon_hoc_map.keys())
        except Error as e: messagebox.showerror("Lỗi", f"Không thể tải dữ liệu điểm: {e}", parent=self)
    def save_grade(self):
        ten_mh = self.mh_combo.get()
        diem_cc_str, diem_gk_str, diem_ck_str = self.cc_entry.get(), self.gk_entry.get(), self.ck_entry.get()
        if not all([ten_mh, diem_cc_str, diem_gk_str, diem_ck_str]):
            messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn môn và nhập đủ 3 cột điểm.", parent=self); return
        try:
            mh_id = self.mon_hoc_map[ten_mh]
            diem_cc, diem_gk, diem_ck = float(diem_cc_str), float(diem_gk_str), float(diem_ck_str)
            if not (0 <= diem_cc <= 10 and 0 <= diem_gk <= 10 and 0 <= diem_ck <= 10):
                messagebox.showerror("Lỗi nhập liệu", "Điểm phải nằm trong khoảng từ 0 đến 10.", parent=self); return
            self.db.nhap_diem(self.sv_id, mh_id, diem_cc, diem_gk, diem_ck)
            self.load_data(); self.clear_grade_form()
            messagebox.showinfo("Thành công", "Đã lưu điểm thành công!", parent=self)
        except ValueError: messagebox.showerror("Lỗi", "Các cột điểm phải là số.", parent=self)
        except Error as e: messagebox.showerror("Lỗi", f"Không thể lưu điểm: {e}", parent=self)
    def recalculate_gpa(self):
        try:
            self.db.tinh_va_cap_nhat_diem_tb(self.sv_id)
            messagebox.showinfo("Thành công", "Đã tính và cập nhật điểm trung bình cho sinh viên.", parent=self)
            self.refresh_main_window()
            self.destroy()
        except Error as e: messagebox.showerror("Lỗi", f"Không thể tính điểm TB: {e}", parent=self)
    def clear_grade_form(self):
        self.mh_combo.set(''); self.cc_entry.delete(0,'end')
        self.gk_entry.delete(0,'end'); self.ck_entry.delete(0,'end')
        if self.diem_tree.selection(): self.diem_tree.selection_remove(self.diem_tree.selection()[0])
    def on_grade_select(self, event):
        selected_item = self.diem_tree.focus()
        if not selected_item: return
        values = self.diem_tree.item(selected_item)['values']
        self.mh_combo.set(values[0])
        self.cc_entry.delete(0,'end'); self.cc_entry.insert(0, values[2])
        self.gk_entry.delete(0,'end'); self.gk_entry.insert(0, values[3])
        self.ck_entry.delete(0,'end'); self.ck_entry.insert(0, values[4])

if __name__ == "__main__":
    root = ThemedTk(theme="clam")
    app = App(root)
    if hasattr(app, 'db') and app.db.connection:
        root.protocol("WM_DELETE_WINDOW", lambda: (app.db.dong_ket_noi(), root.destroy()))
    root.mainloop()