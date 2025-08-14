import tkinter as tk
from tkinter import ttk

# 통계 프레임
class StatsFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.sort_reverse = {}

        # 메인 프레임
        main_content = tk.Frame(self)
        main_content.pack(fill="both", expand=True, padx=20, pady=10)

        # 통계 목록 영역
        list_frame = tk.Frame(main_content)
        list_frame.pack(side="left", fill="both", expand=True)

        # 검색바
        search_frame = tk.Frame(list_frame)
        search_frame.pack(fill="x", pady=(0, 5))

        # "통계" 라벨
        title_label = tk.Label(search_frame, text="통계", font=("Arial", 12, "bold"))
        title_label.grid(row=0, column=0, padx=(0, 10))

        # 검색 콤보박스
        options = ["번호", "고객 이름", "생년월일(월)", "등급"]
        self.search_var = tk.StringVar(value=options[0])
        search_combo = ttk.Combobox(search_frame, textvariable=self.search_var, values=options, state="readonly",
                                    width=12)
        search_combo.grid(row=0, column=1, padx=(0, 5))

        # 검색창 + 검색 버튼
        search_input_frame = tk.Frame(search_frame)
        search_input_frame.grid(row=0, column=2, padx=(0, 10), sticky="w")

        self.search_entry = tk.Entry(search_input_frame, width=40)
        self.search_entry.pack(side="left")
        self.search_entry.bind('<Return>', lambda e: self.search_stats())

        search_btn = tk.Button(search_input_frame, text="검색", command=self.search_stats)
        search_btn.pack(side="left")

        # 통계 목록 Treeview
        self.stats_tree = ttk.Treeview(list_frame, columns=(
            "번호", "고객 이름", "생년월일", "등급", "총 방문 횟수", "총 결제 금액", "마지막 방문 일자"), show="headings")
        for col in self.stats_tree["columns"]:
            self.stats_tree.heading(col, text=col, command=lambda c=col: self.sort_stats(c))
            if col in ["번호", "등급", "총 방문 횟수"]:
                self.stats_tree.column(col, width=50, anchor="center")
            elif col == "고객 이름":
                self.stats_tree.column(col, width=70, anchor="center")
            else:
                self.stats_tree.column(col, width=130, anchor="center")
        self.stats_tree.pack(fill="both", expand=True, pady=(0, 5))

        # 이전 화면 버튼
        back_btn = tk.Button(list_frame, text="이전 화면", command=lambda: controller.show_frame("MainFrame"))
        back_btn.pack(anchor="e", pady=(5, 0))

        # 초기 데이터 로드
        self.search_stats()

    # 검색
    def search_stats(self):
        search_type = self.search_var.get()
        search_value = self.search_entry.get().strip()

        base_query = """
        SELECT c.customer_id, c.name, c.birth_date, c.grade,
               COUNT(v.visit_id) as visit_count,
               COALESCE(SUM(p.amount), 0) as total_amount,
               MAX(v.visit_date) as last_visit
        FROM customer c
        LEFT JOIN visit v ON c.customer_id = v.customer_id
        LEFT JOIN payment p ON v.visit_id = p.visit_id
        """

        params = []

        if search_value:
            if search_type == "고객 번호":
                base_query += " WHERE c.customer_id = %s"
                params = [search_value]
            elif search_type == "고객 이름":
                base_query += " WHERE c.name LIKE %s"
                params = [f"%{search_value}%"]
            elif search_type == "생년월일(월)":
                base_query += " WHERE MONTH(c.birth_date) = %s"
                params = [search_value]
            elif search_type == "등급":
                base_query += " WHERE c.grade = %s"
                params = [search_value]

        base_query += " GROUP BY c.customer_id ORDER BY c.customer_id"

        stats = self.controller.db_manager.fetch_all(base_query, params)

        # 트리뷰 내용 클리어
        for item in self.stats_tree.get_children():
            self.stats_tree.delete(item)

        # 데이터 삽입
        for stat in stats:
            customer_id, name, birth_date, grade, visit_count, total_amount, last_visit = stat
            birth_date_str = str(birth_date) if birth_date else ""
            last_visit_str = str(last_visit) if last_visit else "없음"
            total_amount_str = f"{total_amount:,}원"

            self.stats_tree.insert("", "end", values=(
                customer_id, name, birth_date_str, grade,
                visit_count, total_amount_str, last_visit_str
            ))

    # UI 컬럼명과 DB 컬럼명 매핑
    def get_sql_column_name(self, column):
        mapping = {
            "고객 번호": "c.customer_id",
            "고객 이름": "c.name",
            "생년월일": "c.birth_date",
            "등급": "c.grade",
            "총 방문 횟수": "visit_count",
            "총 결제 금액": "total_amount",
            "마지막 방문일": "last_visit"
        }
        return mapping.get(column, "c.customer_id")

    # 정렬
    def sort_stats(self, column):
        reverse = self.sort_reverse.get(column, False)
        self.sort_reverse[column] = not reverse

        # 모든 헤더의 정렬 표시 제거
        for col in self.stats_tree["columns"]:
            original_text = col.replace(" ▼", "").replace(" ▲", "")
            self.stats_tree.heading(col, text=original_text)

        # 현재 컬럼에 정렬 방향 표시
        sort_symbol = " ▲" if reverse else " ▼"
        self.stats_tree.heading(column, text=column + sort_symbol)

        # SQL 컬럼명 변환
        sql_column = self.get_sql_column_name(column)
        order_direction = "DESC" if reverse else "ASC"

        # DB에서 정렬된 데이터 불러오기
        query = f"""
            SELECT c.customer_id, c.name, c.birth_date, c.grade,
                   COUNT(v.visit_id) AS visit_count,
                   COALESCE(SUM(p.amount), 0) AS total_amount,
                   MAX(v.visit_date) AS last_visit
            FROM customer c
            LEFT JOIN visit v ON c.customer_id = v.customer_id
            LEFT JOIN payment p ON v.visit_id = p.visit_id
            GROUP BY c.customer_id, c.name, c.birth_date, c.grade
            ORDER BY {sql_column} {order_direction}
        """
        results = self.controller.db_manager.fetch_all(query)

        # Treeview 갱신
        self.stats_tree.delete(*self.stats_tree.get_children())
        for stat in results:
            customer_id, name, birth_date, grade, visit_count, total_amount, last_visit = stat
            birth_date_str = str(birth_date) if birth_date else ""
            last_visit_str = str(last_visit) if last_visit else "없음"
            total_amount_str = f"{total_amount:,}원"

            self.stats_tree.insert("", "end", values=(
                customer_id, name, birth_date_str, grade,
                visit_count, total_amount_str, last_visit_str
            ))