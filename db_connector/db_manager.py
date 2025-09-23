from tkinter import messagebox

import mysql.connector
from mysql.connector import Error

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host='',
                database='',
                user='',  # 실제 사용자명으로 변경
                password=''  # 실제 비밀번호로 변경
            )
            if self.connection.is_connected():
                print("MySQL 데이터베이스에 연결되었습니다.")
        except Error as e:
            messagebox.showerror("데이터베이스 오류", f"MySQL 연결 실패: {e}")

    def execute_query(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            return cursor
        except Error as e:
            messagebox.showerror("쿼리 실행 오류", f"쿼리 실행 실패: {e}")
            return None

    def fetch_all(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        except Error as e:
            messagebox.showerror("데이터 조회 오류", f"데이터 조회 실패: {e}")
            return []

    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
