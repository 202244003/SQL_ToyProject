import tkinter as tk
from tkinter import ttk, messagebox
from reg.visit_reg import VisitRegistrationDialog

# 방문 프레임
class VisitFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.sort_reverse = {}

        main_content = tk.Frame(self)
        main_content.pack(fill="both", expand=True, padx=20, pady=(10, 10))

        # 방문 목록 프레임
        list_frame = tk.Frame(main_content)
        list_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # 방문 상세 프레임
        detail_frame = tk.Frame(main_content)
        detail_frame.pack(side="right", fill="both", expand=True)

        # 검색바 프레임
        search_frame = tk.Frame(list_frame)
        search_frame.pack(fill="x", pady=(0, 5))

        # "방문" 라벨
        title_label = tk.Label(search_frame, text="방문", font=("Arial", 12, "bold"))
        title_label.grid(row=0, column=0, padx=(0, 10))

        # 검색 콤보 박스
        options = ["번호", "고객 이름", "방문 일자(일)", "방문 일자(월)", "시술 이름"]
        self.search_var = tk.StringVar(value=options[0])
        search_combo = ttk.Combobox(search_frame, textvariable=self.search_var, values=options, state="readonly",
                                    width=12)
        search_combo.grid(row=0, column=1, padx=(0, 5), sticky="w")

        # 검색창 + 검색 버튼 프레임
        search_input_frame = tk.Frame(search_frame)
        search_input_frame.grid(row=0, column=2, padx=(0, 10), sticky="w")

        self.search_entry = tk.Entry(search_input_frame, width=40)
        self.search_entry.pack(side="left")
        self.search_entry.bind('<Return>', lambda e: self.search_visits())

        search_btn = tk.Button(search_input_frame, text="검색", command=self.search_visits)
        search_btn.pack(side="left")

        # 추가 버튼
        add_btn = tk.Button(search_frame, text="추가", width=8, command=self.add_visit)
        add_btn.grid(row=0, column=3, sticky="e")

        search_frame.grid_columnconfigure(2, weight=1)

        # 방문 목록 Treeview
        self.visit_tree = ttk.Treeview(list_frame, columns=("번호", "방문 일자", "고객 이름", "시술 이름", "방문 메모"),
                                       show="headings")
        for col in self.visit_tree["columns"]:
            self.visit_tree.heading(col, text=col, command=lambda c=col: self.sort_visits(c))
            if col == "번호":
                self.visit_tree.column(col, width=50, anchor="center")
            elif col == "고객 이름":
                self.visit_tree.column(col, width=70, anchor="center")
            else:
                self.visit_tree.column(col, width=120, anchor="center")
        self.visit_tree.pack(fill="both", expand=True)
        self.visit_tree.bind('<ButtonRelease-1>', self.on_visit_select)

        # 식제 버튼
        btn_frame = tk.Frame(detail_frame)
        btn_frame.pack(anchor="ne", pady=5)

        del_btn = tk.Button(btn_frame, text="삭제", width=6, command=self.delete_visit)
        del_btn.pack(side="left", padx=5)

        # 상세 라벨
        detail_label = tk.Label(detail_frame, text="방문 상세", font=("Arial", 14))
        detail_label.pack(anchor="w")

        # 상세 Treeview
        self.detail_tree = ttk.Treeview(detail_frame, columns=("번호", "결제 금액", "결제 방식"), show="headings")
        for col in self.detail_tree["columns"]:
            self.detail_tree.heading(col, text=col)
            if col =="번호":
                self.detail_tree.column(col, width=30, anchor="center")
            else:
                self.detail_tree.column(col, width=100, anchor="center")
        self.detail_tree.pack(fill="both", expand=True)

        # 이전 화면 버튼
        bottom_frame = tk.Frame(self)
        bottom_frame.pack(fill="x", padx=20, pady=(0, 20))

        back_btn = tk.Button(bottom_frame, text="이전 화면", command=lambda: controller.show_frame("MainFrame"))
        back_btn.pack(side="right")

        # 초기 데이터 로드
        self.search_visits()

    # 검색
    def search_visits(self):
        search_type = self.search_var.get()
        search_value = self.search_entry.get().strip()

        base_query = """
        SELECT v.visit_id, v.visit_date, c.name, 
               GROUP_CONCAT(s.service_name SEPARATOR ', ') as services,
               v.note
        FROM visit v
        JOIN customer c ON v.customer_id = c.customer_id
        LEFT JOIN visit_detail vd ON v.visit_id = vd.visit_id
        LEFT JOIN service s ON vd.service_id = s.service_id
        """

        params = []

        if search_value:
            if search_type == "번호":
                base_query += " WHERE v.visit_id = %s"
                params = [search_value]
            elif search_type == "고객 이름":
                base_query += " WHERE c.name LIKE %s"
                params = [f"%{search_value}%"]
            elif search_type == "방문 일자(일)":
                base_query += " WHERE DAY(v.visit_date) = %s"
                params = [search_value]
            elif search_type == "방문 일자(월)":
                base_query += " WHERE MONTH(v.visit_date) = %s"
                params = [search_value]
            elif search_type == "시술 이름":
                base_query += " WHERE s.service_name LIKE %s"
                params = [f"%{search_value}%"]

        base_query += " GROUP BY v.visit_id ORDER BY v.visit_id"

        visits = self.controller.db_manager.fetch_all(base_query, params)

        # 트리뷰 내용 클리어
        for item in self.visit_tree.get_children():
            self.visit_tree.delete(item)

        # 데이터 삽입
        for visit in visits:
            visit_id, visit_date, customer_name, services, note = visit
            services = services or "없음"
            note = note or ""
            self.visit_tree.insert("", "end", values=(visit_id, visit_date, customer_name, services, note))

    # UI 컬럼명과 DB 컬럼명 매핑
    def get_sql_column_name(self, column):
        mapping = {
            "번호": "v.visit_id",
            "방문 일자": "v.visit_date",
            "고객 이름": "c.name",
            "시술 이름": "services",
            "방문 메모": "v.note"
        }
        return mapping.get(column, "visit_id")

    # 정렬
    def sort_visits(self, column):
        reverse = self.sort_reverse.get(column, False)
        self.sort_reverse[column] = not reverse

        # 모든 헤더의 정렬 표시 제거
        for col in self.visit_tree["columns"]:
            original_text = col.replace(" ▼", "").replace(" ▲", "")
            self.visit_tree.heading(col, text=original_text)

        # 현재 컬럼에 정렬 방향 표시 추가
        sort_symbol = " ▲" if reverse else " ▼"
        self.visit_tree.heading(column, text=column + sort_symbol)

        # SQL 컬럼명 변환
        sql_column = self.get_sql_column_name(column)
        order_direction = "DESC" if reverse else "ASC"

        # 정렬된 데이터 불러오기
        query = f"""
            SELECT v.visit_id, v.visit_date, c.name, 
                   GROUP_CONCAT(s.service_name SEPARATOR ', ') AS services,
                   v.note
            FROM visit v
            JOIN customer c ON v.customer_id = c.customer_id
            LEFT JOIN visit_detail vd ON v.visit_id = vd.visit_id
            LEFT JOIN service s ON vd.service_id = s.service_id
            GROUP BY v.visit_id, v.visit_date, c.name, v.note
            ORDER BY {sql_column} {order_direction}
        """
        results = self.controller.db_manager.fetch_all(query)

        # Treeview 갱신
        self.visit_tree.delete(*self.visit_tree.get_children())
        for row in results:
            self.visit_tree.insert("", "end", values=row)

    # 방문 기록 선택 시
    def on_visit_select(self, event):
        selected = self.visit_tree.selection()
        if selected:
            visit_id = self.visit_tree.item(selected[0])['values'][0]
            self.load_visit_details(visit_id)

    # 방문 상세 불러오기
    def load_visit_details(self, visit_id):
        query = """
        SELECT p.payment_id, p.amount, p.method
        FROM payment p
        WHERE p.visit_id = %s
        """

        payments = self.controller.db_manager.fetch_all(query, [visit_id])

        # 상세 트리뷰 클리어
        for item in self.detail_tree.get_children():
            self.detail_tree.delete(item)

        for payment in payments:
            payment_id, amount, method = payment
            self.detail_tree.insert("", "end", values=(visit_id, f"{amount:,}원", method))

    # 추가
    def add_visit(self):
        VisitRegistrationDialog(self, self.controller.db_manager, self)

    # 삭제
    def delete_visit(self):
        selected = self.visit_tree.selection()
        if not selected:
            messagebox.showwarning("선택 필요", "삭제할 방문을 선택해주세요.")
            return

        visit_id = self.visit_tree.item(selected[0])['values'][0]
        visit_date = self.visit_tree.item(selected[0])['values'][1]

        if messagebox.askyesno("삭제 확인", f"방문 기록 '{visit_date}'을(를) 삭제하시겠습니까?"):
            query = "DELETE FROM visit WHERE visit_id = %s"
            if self.controller.db_manager.execute_query(query, [visit_id]):
                messagebox.showinfo("성공", "방문 기록이 삭제되었습니다.")
                self.search_visits()