import tkinter as tk

class MainFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        title = tk.Label(self, text="Hair Salon", font=("Arial", 48, "bold"))
        title.pack(pady=100)

        btn_frame = tk.Frame(self)
        btn_frame.pack()

        buttons = [
            ("고객 화면", "CustomerFrame"),
            ("방문 화면", "VisitFrame"),
            ("통계 화면", "StatsFrame")
        ]
        for i, (text, frame_name) in enumerate(buttons):
            btn = tk.Button(btn_frame, text=text, width=15, height=2,
                            command=lambda n=frame_name: controller.show_frame(n))
            btn.grid(row=0, column=i, padx=20)

        exit_btn = tk.Button(self, text="종료", width=10, command=controller.on_closing)
        exit_btn.pack(side="bottom", anchor="e", padx=20, pady=20)
