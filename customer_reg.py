import tkinter as tk
from tkinter import messagebox

# 고객 등록 / 수정
class CustomerRegistrationDialog:
    def __init__(self, parent, db_manager, customer_frame=None, customer_data=None):
        self.db_manager = db_manager
        self.customer_frame = customer_frame
        self.customer_data = customer_data
        self.result = None

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("고객 등록" if customer_data is None else "고객 수정")
        self.dialog.geometry("400x280")
        self.dialog.transient(parent)
        self.dialog.grab_set()

        self.create_widgets()

    # 화면 생성
    def create_widgets(self):
        main_frame = tk.Frame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # 이름
        tk.Label(main_frame, text="이름:").grid(row=0, column=0, sticky="w", pady=5)
        self.name_var = tk.StringVar(value=self.customer_data[1] if self.customer_data else "")
        tk.Entry(main_frame, textvariable=self.name_var, width=30).grid(row=0, column=1, pady=5)

        # 연락처
        tk.Label(main_frame, text="연락처:").grid(row=1, column=0, sticky="w", pady=5)
        self.phone_var = tk.StringVar(value=self.customer_data[2] if self.customer_data else "")
        tk.Entry(main_frame, textvariable=self.phone_var, width=30).grid(row=1, column=1, pady=5)

        # 성별
        tk.Label(main_frame, text="성별:").grid(row=2, column=0, sticky="w", pady=5)
        self.gender_var = tk.StringVar(value=self.customer_data[3] if self.customer_data else "F")
        gender_frame = tk.Frame(main_frame)
        gender_frame.grid(row=2, column=1, sticky="w", pady=5)
        tk.Radiobutton(gender_frame, text="여성", variable=self.gender_var, value="F").pack(side="left")
        tk.Radiobutton(gender_frame, text="남성", variable=self.gender_var, value="M").pack(side="left")

        # 생년월일
        tk.Label(main_frame, text="생년월일:").grid(row=3, column=0, sticky="w", pady=5)
        self.birth_var = tk.StringVar(
            value=str(self.customer_data[4]) if self.customer_data and self.customer_data[4] else "")
        tk.Entry(main_frame, textvariable=self.birth_var, width=30).grid(row=3, column=1, pady=5)
        tk.Label(main_frame, text="(YYYY-MM-DD 형식)", font=("Arial", 8)).grid(row=4, column=1, sticky="w")

        # 메모
        tk.Label(main_frame, text="메모:").grid(row=5, column=0, sticky="w", pady=5)
        self.memo_text = tk.Text(main_frame, width=25, height=4)
        self.memo_text.grid(row=5, column=1, pady=5)
        if self.customer_data and self.customer_data[7]:
            self.memo_text.insert("1.0", self.customer_data[7])
        # 버튼
        btn_frame = tk.Frame(main_frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=0)

        tk.Button(btn_frame, text="저장", command=self.save_customer).pack(side="left", padx=10)
        tk.Button(btn_frame, text="취소", command=self.dialog.destroy).pack(side="left", padx=10)

    # 저장
    def save_customer(self):
        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()
        gender = self.gender_var.get()
        birth = self.birth_var.get().strip() if self.birth_var.get().strip() else None
        memo = self.memo_text.get("1.0", tk.END).strip()

        if not name or not phone or not gender or not birth:
            messagebox.showerror("입력 오류", "필수 입력 사항입니다.")
            return

        if self.customer_data is None:
            # 새 고객 등록 (등급과 포인트는 기본값 사용)
            query = """INSERT INTO customer (name, phone, gender, birth_date, memo) 
                       VALUES (%s, %s, %s, %s, %s)"""
            params = (name, phone, gender, birth, memo)
        else:
            # 기존 고객 수정
            query = """UPDATE customer SET name=%s, phone=%s, gender=%s, birth_date=%s, memo=%s 
                       WHERE customer_id=%s"""
            params = (name, phone, gender, birth, memo, self.customer_data[0])

        if self.db_manager.execute_query(query, params):
            messagebox.showinfo("성공", "고객 정보가 저장되었습니다.")
            if self.customer_frame:
                self.customer_frame.search_customers()
            self.dialog.destroy()
