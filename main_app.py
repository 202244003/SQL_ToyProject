import tkinter as tk
from datetime import datetime
from db_manager import DatabaseManager
from customer_frame import CustomerFrame
from main_frame import MainFrame
from stats_frame import StatsFrame
from visit_frame import VisitFrame


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hair Salon")
        self.geometry("1270x700")

        self.db_manager = DatabaseManager()

        self.frames = {}
        for F in (MainFrame, CustomerFrame, VisitFrame, StatsFrame):
            frame = F(self, self)
            self.frames[F.__name__] = frame
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.show_frame("MainFrame")

        # 오른쪽 상단 날짜/시간 표시
        self.time_label = tk.Label(self, font=("Arial", 11))
        self.time_label.place(relx=0.85, rely=0.02)
        self.update_time()

    # 시계 업데이트
    def update_time(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=now)
        self.after(1000, self.update_time)

    # 프레임 이동
    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

    # 종료
    def on_closing(self):
        self.db_manager.close_connection()
        self.destroy()