# LG U+ WHY NOT SW 8기 - 윤예빈
## 💌 SQL TOY PROJECT

## 💇‍♀️ 프로젝트 소개

### 주제

- 미용실 프로그램
- 고객 관리
- 방문 내역 관리

### 사용 기술
<img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=MySQL&logoColor=white">
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white"> - tkinter


### 기능

- 고객 관리 기능
    - 고객 목록 열람
        - 고객 번호, 이름, 연락처, 성별, 생년월일, 등급, 포인트, 메모
    - 고객 정보 등록
        - 이름, 연락처, 생년월일, 성별, 메모
        - DEFAULT 포인트 0, 등급 ‘일반’
        - 방문 횟수가 5회 이상이면 등급 ‘단골’
        - 방문 횟수가 10회 이상이면 등급 ‘VIP’
        - 결제 금액의 30% 포인트로 적립
    - 고객 정보 수정 / 삭제
        - 고객 선택 시 정보 수정 / 삭제 가능
    - 고객 검색
        - 번호, 이름, 성별, 생일(월), 등급
    - 고객 목록 정렬
        - 각 컬럼 별로 정렬 가능
        - 오름차순, 내림차순
    - 고객 방문 기록
        - 고객 선택 시 방문 기록 열람
        - 방문 번호, 방문 일자, 시술 이름, 시술 설명
- 방문 관리 기능
    - 방문 정보 열람
        - 방문 번호, 방문 일자, 고객 이름, 시술 이름, 방문 메모
    - 방문 정보 등록
        - 고객, 방문 일시, 시술, 결제 금액(자동 입력), 결제 방식, 메모
        - 드롭다운 형식으로 고객 내역 중 선택
        - 시술 다중 선택 가능
        - 시술에 따라 가격 자동 계산
    - 방문 정보 삭제
        - 방문 선택 시 정보 삭제 가능
    - 방문 검색
        - 번호, 고객 이름, 방문 일자(일), 방문 일자(월), 시술 이름
    - 방문 목록 정렬
        - 각 컬럼 별로 정렬 가능
        - 오름차순, 내림차순
    - 방문 상세 내역
        - 방문 선택 시 방문 상세 내역 열람
        - 방문 번호, 결제 금액, 결제 방식
- 통계 기능
    - 전체 정보 열람
        - 번호, 고객 이름, 생년월일, 등급, 총 방문 횟수, 총 결제 금액, 마지막 방문 일자
            - 총 방문 횟수
                - 고객 별 방문 횟수 계산
            - 총 결제 금액
                - 고객 별 결제 금액 계산
            - 마지막 방문 일자
                - 고객 별 가장 최근 방문 일자
                - 방문 이력이 없으면 ‘없음’
    - 전체 검색
        - 번호, 고객 이름, 생년월일(월), 등급
    - 전체 정렬
        - 각 컬럼 별로 정렬 가능
        - 오름차순, 내림차순

---

## 💿 DB

### ERD

<img width="612" height="475" alt="ERD" src="https://github.com/user-attachments/assets/7d5ff726-330f-4f2e-bb48-f174a1ab6c33" />


### SQL

```sql
CREATE SCHEMA hairsalon;

USE hairsalon;

# 고객 테이블
CREATE TABLE customer (
	customer_id INT AUTO_INCREMENT PRIMARY KEY,	-- 고객 번호
    name VARCHAR(100) NOT NULL,					-- 고객 이름
    phone VARCHAR(20) NOT NULL,					-- 연락처
    gender ENUM('F', 'M') NOT NULL,				-- 성별
    birth_date DATE,							-- 생년월일
    memo TEXT,									-- 고객 메모
    points INT DEFAULT 0,						-- 보유 포인트
    grade ENUM('일반', '단골', 'VIP') DEFAULT '일반' -- 고객 등급
);

# 시술 테이블
CREATE TABLE service (
	service_id INT AUTO_INCREMENT PRIMARY KEY, 	-- 시술 번호
    service_name VARCHAR(100) NOT NULL,			-- 시술 이름
    price INT NOT NULL,				-- 가격
    service_detail TEXT 						-- 시술 설명
); 

# 방문 테이블
CREATE TABLE visit (
	visit_id INT AUTO_INCREMENT PRIMARY KEY,	-- 방문 번호
	customer_id INT NOT NULL,					-- 고객 번호
    visit_date DATETIME NOT NULL,				-- 방문 날짜
    note TEXT									-- 방문 메모
);

# 방문 상세 테이블
CREATE TABLE visit_detail (
	visit_id INT NOT NULL,						-- 방문 번호
    service_id INT NOT NULL,					-- 시술 번호
    PRIMARY KEY (visit_id, service_id)
);

# 결제 테이블
CREATE TABLE payment (
	payment_id INT AUTO_INCREMENT PRIMARY KEY,	-- 결제 번호
    visit_id INT NOT NULL,						-- 방문 번호
    amount INT NOT NULL,				-- 금액
    method ENUM('현금', '카드', '포인트') NOT NULL	-- 결제 방식
);

# 방문 테이블 - 고객(고객 번호) FK
ALTER TABLE visit
ADD CONSTRAINT fk_visit_customer
FOREIGN KEY (customer_id)
REFERENCES customer(customer_id)
ON DELETE CASCADE
ON UPDATE CASCADE;

# 방문 상세 테이블 - 방문(방문 번호) FK
ALTER TABLE visit_detail
ADD CONSTRAINT fk_visit_visit_detail
FOREIGN KEY (visit_id)
REFERENCES visit(visit_id)
ON DELETE CASCADE
ON UPDATE CASCADE;

# 방문 상세 테이블 - 시술(시술 번호) FK
ALTER TABLE visit_detail
ADD CONSTRAINT fk_visit_detail_service
FOREIGN KEY (service_id)
REFERENCES service(service_id)
ON DELETE CASCADE
ON UPDATE CASCADE;

# 결제 테이블 - 방문(방문 번호) FK
ALTER TABLE payment
ADD CONSTRAINT fk_payment_visit
FOREIGN KEY (visit_id)
REFERENCES visit(visit_id)
ON DELETE CASCADE
ON UPDATE CASCADE;
```

---

## 📁 파일

### 파일 구조

```bash
SQL_ToyProject/
│
├── customer_frame.py    # 고객 목록 및 검색 화면 UI
├── customer_reg.py      # 고객 등록/수정 화면 UI
├── db_manager.py        # DB 연결, 쿼리 실행, 데이터 처리 로직
├── main.py              # 프로그램 시작점 (실행 스크립트)
├── main_frame.py        # 메인 메뉴 UI (버튼/네비게이션)
├── main_app.py          # Tkinter App 클래스 (프레임 전환, 전체 레이아웃)
├── stats_frame.py       # 통계 화면 UI
├── visit_frame.py       # 방문 내역 및 관리 화면 UI
└── visit_reg.py         # 방문 등록/수정 화면 UI
```

### 파일 흐름

```scss
main.py
  │
  └── main_app.py (App 클래스)
        │
        ├── main_frame.py (MainFrame)
        ├── customer_frame.py (CustomerFrame)
        ├── customer_reg.py (CustomerReg)
        ├── visit_frame.py (VisitFrame)
        ├── visit_reg.py (VisitReg)
        └── stats_frame.py (StatsFrame)
        
db_manager.py  ←  (모든 Frame에서 DB 연결/쿼리 실행 시 사용)

```

---

## 💻 주요 코드

### 검색

**고객 검색**

```python
# /SQL_ToyProject/customer_frame.py

class CustomerFrame(tk.Frame):
...
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
				...
"""
선택된 항목에 따라 WHERE문을 추가하여 고객 정보를 불러온다.
ORDER BY로 customer_id를 기준으로 정렬한다.
"""
```

**방문 내역 검색**

```python
# /SQL_ToyProject/visit_frame.py

class VisitFrame(tk.Frame):
...
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
				...
"""
선택된 항목에 따라 WHERE문을 추가하여 방문 정보를 불러온다.
GROUP_CONCAT(s.service_name SEPARATOR ', ')로 여러 개의 시술 내역을 ','로 분리해서 합친다
고객 정보를 열람하기위해 visit 테이블과 JOIN 한다.
방문 상세, 시술 정보를 열람하기위해 LEFT JOIN으로 visit 기준 JOIN한다.
ORDER BY로 visit_id를 기준으로 정렬한다.
"""
```

**통계 검색**

```python
# /SQL_ToyProject/stats_frame.py

class StatsFrame(tk.Frame):
		...
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
        ...
```

### 상세 정보 불러오기

**고객 방문 기록 불러오기**

```python
# /SQL_ToyProject/customer_frame.py

class CustomerFrame(tk.Frame):
...
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
				...
"""
GROUP_CONCAT()로 여러 행의 문자열 값을 하나의 문자열로 합친다. (여러개의 시술을 받은 경우)
방문 상세 내용과 시술 정보를 열람하기 위해 각각 LEFT JOIN으로 visit 기준 JOIN한다. 
"""
```

**방문 상세 불러오기**

```python
# /SQL_ToyProject/visit_frame.py

class VisitFrame(tk.Frame):
...
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
				...
"""
방문 상세 정보를 선택한 방문 번호를 기준으로 검색한다.
"""
```

### 등록 / 수정

**고객 정보 등록/수정**

```python
# /SQL_ToyProject/customer_reg.py

class CustomerRegistrationDialog:
...
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
				...
"""
INSERT를 통해 새로운 고객 정보를 저장한다.
UPDATE를 통해 기존 고객 정보를 수정한다.
"""
```

### 정렬

**고객 목록 정렬**

```python
# /SQL_ToyProject/customer_frame.py

class CustomerFrame(tk.Frame):
...
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
        ...
"""
모든 컬럼을 기준으로 정렬 가능.
각 컬럼은 토글 방식으로 기본 오름차순에서 내림차순 변경 가능.
DB에서 ORDER BY절을 활용해 선택된 컬럼, 방향 지정하여 정렬
"""
```

**방문 목록 정렬**

```python
# /SQL_ToyProject/visit_frame.py

class VisitFrame(tk.Frame):
...
		# 정렬
    def sort_visits(self, column):
		    ...
				# SQL 컬럼명 변환
        sql_column = self.get_sql_column_name(column)
        order_direction = "DESC" if reverse else "ASC"

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
        ...
"""
모든 컬럼을 기준으로 정렬 가능.
각 컬럼은 토글 방식으로 기본 오름차순에서 내림차순 변경 가능.
DB에서 ORDER BY절을 활용해 선택된 컬럼, 방향 지정하여 정렬
"""
```

**통계 정렬**

```python
# /SQL_ToyProject/stats_frame.py

class StatsFrame(tk.Frame):
		def sort_stats(self, column):
				...
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
        ...
"""
모든 컬럼을 기준으로 정렬 가능.
각 컬럼은 토글 방식으로 기본 오름차순에서 내림차순 변경 가능.
DB에서 ORDER BY절을 활용해 선택된 컬럼, 방향 지정하여 정렬
"""
```

---
### 추가 목표

- 방문 내역 수정 기능
- 방문 내역 추가 시 다중 결제 기능
- 시술 정보 추가/수정/삭제 기능
- 시술 별 소요 시간 추가 후 방문 시간 조절 기능