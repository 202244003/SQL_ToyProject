import tkinter as tk
from tkinter import ttk, messagebox
from reg.customer_reg import CustomerRegistrationDialog

# 고객 프레임
class CustomerFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.sort_reverse = {}

        main_content = tk.Frame(self)
        main_content.pack(fill="both", expand=True, padx=20, pady=(10, 10))

        # 고객 목록 프레임
        customer_frame = tk.Frame(main_content)
        customer_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # 방문 기록 프레임
        visit_frame = tk.Frame(main_content)
        visit_frame.pack(side="right", fill="both", expand=True)

        # 검색바 프레임
        search_frame = tk.Frame(customer_frame)
        search_frame.pack(fill="x", pady=(0, 5))

        # '고객' 라벨
        screen_label = tk.Label(search_frame, text="고객", font=("Arial", 12, "bold"))
        screen_label.grid(row=0, column=0, padx=(0, 10))

        # 검색 콤보 박스
        options = ["번호", "이름", "성별", "생일(월)", "등급"]
        self.search_var = tk.StringVar(value=options[0])
        search_combo = ttk.Combobox(search_frame, textvariable=self.search_var, values=options, state="readonly",
                                    width=10)
        search_combo.grid(row=0, column=1, padx=0, sticky="w")

        # 검색창 + 검색 버튼
        search_input_frame = tk.Frame(search_frame)
        search_input_frame.grid(row=0, column=2, padx=(0, 10), sticky="w")

        self.search_entry = tk.Entry(search_input_frame, width=40)
        self.search_entry.pack(side="left", padx=(0, 0))
        self.search_entry.bind('<Return>', lambda e: self.search_customers())

        search_btn = tk.Button(search_input_frame, text="검색", command=self.search_customers)
        search_btn.pack(side="left", padx=(0, 0))

        # 등록 버튼
        reg_btn = tk.Button(search_frame, text="등록", width=8, command=self.register_customer)
        reg_btn.grid(row=0, column=4, sticky="e")

        search_frame.grid_columnconfigure(2, weight=1)

        # 고객 목록 트리뷰
        self.customer_tree = ttk.Treeview(customer_frame, columns=("번호", "이름", "연락처", "성별", "생일", "등급", "포인트", "메모"),
                                          show="headings")
        for col in self.customer_tree["columns"]:
            self.customer_tree.heading(col, text=col, command=lambda c=col: self.sort_customers(c))
            if col == "메모":
                self.customer_tree.column(col, width=150, anchor="center")
            elif col in ("번호", "성별", "등급"):
                self.customer_tree.column(col, width=50, anchor="center")
            else:
                self.customer_tree.column(col, width=100, anchor="center")

        self.customer_tree.pack(fill="both", expand=True)
        self.customer_tree.bind('<ButtonRelease-1>', self.on_customer_select)

        # 방문 기록 버튼 (수정, 삭제)
        btn_frame = tk.Frame(visit_frame)
        btn_frame.pack(anchor="ne", pady=5)

        edit_btn = tk.Button(btn_frame, text="수정", width=6, command=self.edit_customer)
        del_btn = tk.Button(btn_frame, text="삭제", width=6, command=self.delete_customer)
        edit_btn.pack(side="left", padx=5)
        del_btn.pack(side="left", padx=5)

        # 방문 기록 (고객 상세 내용)
        visit_label = tk.Label(visit_frame, text="방문 기록", font=("Arial", 14))
        visit_label.pack(anchor="w")

        # 고객 상세 트리뷰
        self.visit_tree = ttk.Treeview(visit_frame, columns=("번호", "방문 일자", "시술 이름", "시술 설명"), show="headings")
        for col in self.visit_tree["columns"]:
            self.visit_tree.heading(col, text=col)
            if col == "번호":
                self.visit_tree.column(col, width=30, anchor="center")
            else:
                self.visit_tree.column(col, width=120, anchor="center")
        self.visit_tree.pack(fill="both", expand=True)

        # 이전 화면 버튼
        bottom_frame = tk.Frame(self)
        bottom_frame.pack(fill="x", padx=20, pady=(0, 20))

        back_btn = tk.Button(bottom_frame, text="이전 화면", command=lambda: controller.show_frame("MainFrame"))
        back_btn.pack(side="right")

        # 초기 데이터 로드
        self.search_customers()

    # 고객 검색
    def search_customers(self):
        search_type = self.search_var.get()
        search_value = self.search_entry.get().strip()

        base_query = "SELECT customer_id, name, phone, gender, birth_date, grade, points, memo FROM customer"
        params = []

        if search_value:
            if search_type == "번호":
                base_query += " WHERE customer_id = %s"
                params = [search_value]
            elif search_type == "이름":
                base_query += " WHERE name LIKE %s"
                params = [f"%{search_value}%"]
            elif search_type == "성별":
                base_query += " WHERE gender = %s"
                params = [search_value]
            elif search_type == "생일(월)":
                base_query += " WHERE MONTH(birth_date) = %s"
                params = [search_value]
            elif search_type == "등급":
                base_query += " WHERE grade = %s"
                params = [search_value]

        base_query += " ORDER BY customer_id"

        customers = self.controller.db_manager.fetch_all(base_query, params)

        # 트리뷰 내용 클리어
        for item in self.customer_tree.get_children():
            self.customer_tree.delete(item)

        # 데이터 삽입
        for customer in customers:
            self.customer_tree.insert("", "end", values=customer)

    # UI 컬럼명과 DB 컬럼명 매핑
    def get_sql_column_name(self, column):
        mapping = {
            "번호": "customer_id",
            "이름": "name",
            "연락처": "phone",
            "성별": "gender",
            "생년월일": "birth_date",
            "등급": "grade",
            "포인트": "points",
            "메모": "memo"
        }
        return mapping.get(column, "customer_id")

    # 고객 정렬
    def sort_customers(self, column):
        # 정렬 방향 토글
        reverse = self.sort_reverse.get(column, False)
        self.sort_reverse[column] = not reverse

        # 모든 헤더의 정렬 표시 제거
        for col in self.customer_tree["columns"]:
            original_text = col.replace(" ▼", "").replace(" ▲", "")
            self.customer_tree.heading(col, text=original_text)

        # 현재 컬럼에 정렬 방향 표시
        sort_symbol = " ▲" if reverse else " ▼"
        self.customer_tree.heading(column, text=column + sort_symbol)

        # SQL 컬럼명 변환
        sql_column = self.get_sql_column_name(column)
        order_direction = "DESC" if reverse else "ASC"

        # DB에서 정렬된 데이터 불러오기
        query = f"""
            SELECT customer_id, name, phone, gender, birth_date, grade, points, memo
            FROM customer
            ORDER BY {sql_column} {order_direction}
        """
        results = self.controller.db_manager.fetch_all(query)

        # Treeview 갱신
        self.customer_tree.delete(*self.customer_tree.get_children())
        for row in results:
            self.customer_tree.insert("", "end", values=row)

    # 고객 선택 시
    def on_customer_select(self, event):
        selected = self.customer_tree.selection()
        if selected:
            customer_id = self.customer_tree.item(selected[0])['values'][0]
            self.load_customer_visits(customer_id)

    # 고객 방문 기록 불러오기
    def load_customer_visits(self, customer_id):
        query = """
        SELECT v.visit_id, v.visit_date, GROUP_CONCAT(s.service_name), GROUP_CONCAT(s.service_detail)
        FROM visit v
        LEFT JOIN visit_detail vd ON v.visit_id = vd.visit_id
        LEFT JOIN service s ON vd.service_id = s.service_id
        WHERE v.customer_id = %s
        GROUP BY v.visit_id, v.visit_date
        ORDER BY v.visit_id
        """

        visits = self.controller.db_manager.fetch_all(query, [customer_id])

        # 방문 기록 트리뷰 클리어
        for item in self.visit_tree.get_children():
            self.visit_tree.delete(item)

        # 데이터 삽입
        for visit in visits:
            visit_id, visit_date, service_names, service_details = visit
            service_names = service_names or "없음"
            service_details = service_details or "없음"
            self.visit_tree.insert("", "end", values=(visit_id, visit_date, service_names, service_details))

    # 고객 등록
    def register_customer(self):
        CustomerRegistrationDialog(self, self.controller.db_manager, self)

    # 고객 정보 수정
    def edit_customer(self):
        selected = self.customer_tree.selection()
        if not selected:
            messagebox.showwarning("선택 필요", "수정할 고객을 선택해주세요.")
            return

        customer_data = self.customer_tree.item(selected[0])['values']
        CustomerRegistrationDialog(self, self.controller.db_manager, self, customer_data)

    # 고객 삭제
    def delete_customer(self):
        selected = self.customer_tree.selection()
        if not selected:
            messagebox.showwarning("선택 필요", "삭제할 고객을 선택해주세요.")
            return

        customer_id = self.customer_tree.item(selected[0])['values'][0]
        customer_name = self.customer_tree.item(selected[0])['values'][1]

        if messagebox.askyesno("삭제 확인", f"고객 '{customer_name}'을(를) 삭제하시겠습니까?"):
            query = "DELETE FROM customer WHERE customer_id = %s"
            if self.controller.db_manager.execute_query(query, [customer_id]):
                messagebox.showinfo("성공", "고객이 삭제되었습니다.")
                self.search_customers()
