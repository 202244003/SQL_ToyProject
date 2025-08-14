import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# 방문 추가 / 수정
class VisitRegistrationDialog:
    def __init__(self, parent, db_manager, visit_frame=None, visit_data=None):
        self.db_manager = db_manager
        self.visit_frame = visit_frame
        self.visit_data = visit_data

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("방문 등록")
        self.dialog.geometry("500x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()

        self.create_widgets()

    # 화면 생성
    def create_widgets(self):
        main_frame = tk.Frame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # 고객 선택
        tk.Label(main_frame, text="고객:").grid(row=0, column=0, sticky="w", pady=5)
        self.customer_var = tk.StringVar()
        customer_combo = ttk.Combobox(main_frame, textvariable=self.customer_var, width=40)
        customer_combo.grid(row=0, column=1, pady=5)

        # 고객 목록 로드
        customers = self.db_manager.fetch_all("SELECT customer_id, name, points FROM customer ORDER BY customer_id")
        customer_values = [f"{c[0]} - {c[1]} (포인트: {c[2]})" for c in customers]
        customer_combo['values'] = customer_values
        customer_combo.bind('<<ComboboxSelected>>', self.on_customer_select)

        # 방문 일시
        tk.Label(main_frame, text="방문 일시:").grid(row=1, column=0, sticky="w", pady=5)
        self.visit_date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        tk.Entry(main_frame, textvariable=self.visit_date_var, width=40).grid(row=1, column=1, pady=5)

        # 서비스 선택
        tk.Label(main_frame, text="시술:").grid(row=2, column=0, sticky="w", pady=5)
        service_frame = tk.Frame(main_frame)
        service_frame.grid(row=2, column=1, sticky="w", pady=5)

        self.service_listbox = tk.Listbox(service_frame, selectmode=tk.MULTIPLE, height=5)
        self.service_listbox.pack(side="left", fill="both", expand=True)
        self.service_listbox.bind('<<ListboxSelect>>', self.calculate_total_amount)

        # 서비스 목록 로드
        self.services = self.db_manager.fetch_all("SELECT service_id, service_name, price FROM service")
        for service in self.services:
            self.service_listbox.insert(tk.END, f"{service[0]} - {service[1]} ({service[2]:,}원)")

        # 결제 금액 (자동 계산)
        tk.Label(main_frame, text="결제 금액:").grid(row=3, column=0, sticky="w", pady=5)
        self.amount_var = tk.StringVar(value="0")
        amount_label = tk.Label(main_frame, textvariable=self.amount_var, relief="sunken", width=35, anchor="w")
        amount_label.grid(row=3, column=1, pady=5, sticky="w")

        # 결제 방식
        tk.Label(main_frame, text="결제 방식:").grid(row=4, column=0, sticky="w", pady=5)
        self.payment_var = tk.StringVar(value="현금")
        payment_combo = ttk.Combobox(main_frame, textvariable=self.payment_var, values=["현금", "카드", "포인트"],
                                     state="readonly")
        payment_combo.grid(row=4, column=1, sticky="w", pady=5)

        # 메모
        tk.Label(main_frame, text="메모:").grid(row=5, column=0, sticky="w", pady=5)
        self.memo_text = tk.Text(main_frame, width=35, height=4)
        self.memo_text.grid(row=5, column=1, pady=5)

        # 버튼
        btn_frame = tk.Frame(main_frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=20)

        tk.Button(btn_frame, text="저장", command=self.save_visit).pack(side="left", padx=10)
        tk.Button(btn_frame, text="취소", command=self.dialog.destroy).pack(side="left", padx=10)

    # 고객 선택 시
    def on_customer_select(self, event):
        # 고객 선택 시 포인트 정보 업데이트
        self.calculate_total_amount()

    # 결제 금액 계산
    def calculate_total_amount(self, event=None):
        selected_indices = self.service_listbox.curselection()
        total_amount = 0

        for idx in selected_indices:
            service = self.services[idx]
            total_amount += service[2]  # price

        self.amount_var.set(f"{total_amount:,}원")

    # 고객 포인트 불러오기
    def get_customer_points(self):
        customer_text = self.customer_var.get()
        if not customer_text:
            return 0
        customer_id = int(customer_text.split(" - ")[0])
        result = self.db_manager.fetch_all("SELECT points FROM customer WHERE customer_id = %s", [customer_id])
        return result[0][0] if result else 0

    # 등급, 포인트 업데이트
    def update_customer_grade_and_points(self, customer_id, amount, payment_method):
        # 방문 횟수 조회
        visit_count_query = "SELECT COUNT(*) FROM visit WHERE customer_id = %s"
        visit_count = self.db_manager.fetch_all(visit_count_query, [customer_id])[0][0]

        # 등급 결정
        if visit_count >= 10:
            new_grade = "VIP"
        elif visit_count >= 5:
            new_grade = "단골"
        else:
            new_grade = "일반"

        # 포인트 계산
        current_points = self.get_customer_points()

        if payment_method == "포인트":
            # 포인트 차감
            new_points = current_points - amount
        else:
            # 결제 금액의 30% 포인트 적립
            earned_points = int(amount * 0.3)
            new_points = current_points + earned_points

        # 고객 정보 업데이트
        update_query = "UPDATE customer SET grade = %s, points = %s WHERE customer_id = %s"
        self.db_manager.execute_query(update_query, (new_grade, new_points, customer_id))

    # 방문 저장
    def save_visit(self):

        customer_text = self.customer_var.get()
        if not customer_text:
            messagebox.showerror("입력 오류", "고객을 선택해주세요.")
            return

        customer_id = int(customer_text.split(" - ")[0])
        visit_date = self.visit_date_var.get()
        payment_method = self.payment_var.get()
        note = self.memo_text.get("1.0", tk.END).strip()

        selected_services = [self.service_listbox.get(i) for i in self.service_listbox.curselection()]
        if not selected_services:
            messagebox.showerror("입력 오류", "시술을 선택해주세요.")
            return

        # 총 결제 금액 계산
        total_amount = 0
        selected_service_ids = []
        for idx in self.service_listbox.curselection():
            service = self.services[idx]
            total_amount += service[2]
            selected_service_ids.append(service[0])

        # 포인트 결제 시 포인트 부족 체크
        if payment_method == "포인트":
            current_points = self.get_customer_points()
            if current_points < total_amount:
                messagebox.showerror("포인트 부족", f"보유 포인트({current_points:,})가 결제 금액({total_amount:,})보다 부족합니다.")
                return

        # 방문 등록
        visit_query = "INSERT INTO visit (customer_id, visit_date, note) VALUES (%s, %s, %s)"
        cursor = self.db_manager.execute_query(visit_query, (customer_id, visit_date, note))

        if cursor:
            visit_id = cursor.lastrowid

            # 시술 상세 등록
            for service_id in selected_service_ids:
                detail_query = "INSERT INTO visit_detail (visit_id, service_id) VALUES (%s, %s)"
                self.db_manager.execute_query(detail_query, (visit_id, service_id))

            # 결제 등록
            payment_query = "INSERT INTO payment (visit_id, amount, method) VALUES (%s, %s, %s)"
            self.db_manager.execute_query(payment_query, (visit_id, total_amount, payment_method))

            # 고객 등급과 포인트 업데이트
            self.update_customer_grade_and_points(customer_id, total_amount, payment_method)

            messagebox.showinfo("성공", "방문 정보가 저장되었습니다.")
            if self.visit_frame:
                self.visit_frame.search_visits()
            self.dialog.destroy()
