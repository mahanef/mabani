import tkinter as tk
from tkinter import messagebox
import json
import random

class QuizGame:
    def __init__(self, root):
        self.root = root
        self.root.title("بازی کوییز")
        self.root.config(bg="#f0f0f0")
        self.score = 0
        self.current_question = 0
        self.time_left = 30
        self.questions = self.load_questions()
        random.shuffle(self.questions)

        self.question_label = tk.Label(root, text="", font=("Arial", 18, "bold"), wraplength=400, justify="right", bg="#f0f0f0", fg="#333")
        self.question_label.pack(pady=20)

        self.options_var = tk.StringVar()
        self.options_buttons = []
        for i in range(4):
            btn = tk.Radiobutton(root, text="", variable=self.options_var, value=f"option{i}", font=("Arial", 14), anchor="w", bg="#e0e0e0", activebackground="#c0c0c0", selectcolor="#c0e0f0")
            btn.pack(fill="x", padx=20, pady=5)
            self.options_buttons.append(btn)

        self.timer_label = tk.Label(root, text="زمان باقی‌مانده: 30 ثانیه", font=("Arial", 14), bg="#f0f0f0", fg="#333")
        self.timer_label.pack(pady=10)

        self.submit_button = tk.Button(root, text="ثبت پاسخ", command=self.submit_answer, font=("Arial", 14, "bold"), bg="#4CAF50", fg="white")
        self.submit_button.pack(pady=20)

        self.show_question()

    def load_questions(self):
        try:
            with open("questions.json", "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            messagebox.showerror("خطا", "فایل سوالات پیدا نشد!")
            self.root.quit()
        except json.JSONDecodeError:
            messagebox.showerror("خطا", "فرمت فایل سوالات صحیح نیست!")
            self.root.quit()

    def show_question(self):
        if self.current_question < len(self.questions):
            self.time_left = 30
            self.update_timer()
            question_data = self.questions[self.current_question]
            self.question_label.config(text=question_data["question"])
            self.options_var.set(None)
            for i, option in enumerate(question_data["options"]):
                self.options_buttons[i].config(text=option, value=option)
        else:
            self.end_game()

    def submit_answer(self):
        selected_option = self.options_var.get()
        if not selected_option:
            messagebox.showwarning("هشدار", "لطفاً یک گزینه انتخاب کنید!")
            return

        correct_answer = self.questions[self.current_question]["answer"]
        if selected_option == correct_answer:
            self.score += 1
            messagebox.showinfo("پاسخ صحیح!", "جواب صحیح بود!")
        else:
            messagebox.showerror("پاسخ غلط", "جواب غلط بود!")

        self.current_question += 1
        self.show_question()

    def update_timer(self):
        if self.time_left > 0:
            self.timer_label.config(text=f"زمان باقی‌مانده: {self.time_left} ثانیه", fg="#333")
            self.time_left -= 1
            self.root.after(1000, self.update_timer)
        else:
            messagebox.showinfo("پایان زمان", "زمان شما برای این سوال به پایان رسید!")
            self.current_question += 1
            self.show_question()

    def end_game(self):
        messagebox.showinfo("پایان بازی", f"بازی تمام شد! امتیاز شما: {self.score}/{len(self.questions)}")
        self.root.quit()
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizGame(root)
    root.mainloop()