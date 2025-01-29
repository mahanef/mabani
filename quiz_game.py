import tkinter as tk
from tkinter import messagebox
import json
import random

def load_questions():
    """بارگذاری سوالات از فایل JSON"""
    try:
        with open("questions.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        messagebox.showerror("خطا", "فایل سوالات پیدا نشد!")
        root.quit()
    except json.JSONDecodeError:
        messagebox.showerror("خطا", "فرمت فایل سوالات صحیح نیست!")
        root.quit()

def show_question():
    """نمایش سوال جاری"""
    global current_question, time_left, game_over
    if game_over:  # اگر بازی تمام شده باشد، سوال جدید نشان داده نمی‌شود
        return
    if current_question < len(questions):
        time_left = 30
        submit_button.config(state="normal")  # فعال کردن دکمه ثبت
        update_timer()
        question_data = questions[current_question]
        question_label.config(text=question_data["question"])
        options_var.set(None)
        for i, option in enumerate(question_data["options"]):
            options_buttons[i].config(text=option, value=option)
    else:
        end_game()

def submit_answer():
    """بررسی پاسخ انتخابی"""
    global current_question, score
    selected_option = options_var.get()
    if not selected_option:
        messagebox.showwarning("هشدار", "لطفاً یک گزینه انتخاب کنید!")
        return

    correct_answer = questions[current_question]["answer"]
    if selected_option == correct_answer:
        score += 1
        messagebox.showinfo("پاسخ صحیح!", "جواب صحیح بود!")
    else:
        messagebox.showerror("پاسخ غلط", "جواب غلط بود!")
    
    current_question += 1
    show_question()

def update_timer():
    """به‌روزرسانی تایمر سوال"""
    global time_left, is_time_up
    if time_left > 0 and not is_time_up:  # تایمر فقط در صورتی به روز می‌شود که زمان تمام نشده باشد
        timer_label.config(text=f"زمان باقی‌مانده: {time_left} ثانیه", fg="#ffffff")
        time_left -= 1
        root.after(1000, update_timer)
    elif time_left == 0 and not is_time_up:  # زمان تمام شد و هنوز هشدار داده نشده است
        is_time_up = True  # علامت‌گذاری زمان تمام شده
        submit_button.config(state="disabled")  # غیرفعال کردن دکمه ثبت
        messagebox.showwarning("زمان تمام شد", "زمان شما برای این سوال به پایان رسید!")
        global current_question  # دسترسی به متغیر global
        current_question += 1  # به سوال بعدی برو
        show_question()  # نمایش سوال بعدی

def end_game():
    """پایان بازی و نمایش امتیاز"""
    global game_over
    game_over = True  # علامت‌گذاری اینکه بازی تمام شده
    messagebox.showinfo("پایان بازی", f"بازی تمام شد! امتیاز شما: {score}/{len(questions)}")
    root.quit()

# تنظیمات اولیه
root = tk.Tk()
root.title("بازی کوییز")
root.config(bg="#2b2b2b")  # پس‌زمینه تیره

# متغیرها
score = 0
current_question = 0
time_left = 30
game_over = False  # متغیر برای بررسی اینکه آیا بازی تمام شده یا نه
is_time_up = False  # متغیر برای بررسی زمان تمام شده
questions = load_questions()
random.shuffle(questions)

# رابط کاربری
question_label = tk.Label(
    root, text="", font=("B Nazanin", 18, "bold"), 
    wraplength=400, justify="right", bg="#2b2b2b", fg="#ffffff"
)
question_label.pack(pady=20)

options_var = tk.StringVar()
options_buttons = []
for i in range(4):
    btn = tk.Radiobutton(
        root, text="", variable=options_var, value=f"option{i}",
        font=("B Nazanin", 14), anchor="w", bg="#3c3c3c", fg="#ffffff",
        activebackground="#555555", activeforeground="#ffffff", 
        selectcolor="#444444"
    )
    btn.pack(fill="x", padx=20, pady=5)
    options_buttons.append(btn)

timer_label = tk.Label(
    root, text="زمان باقی‌مانده: 30 ثانیه", 
    font=("B Nazanin", 14), bg="#2b2b2b", fg="#ffffff"
)
timer_label.pack(pady=10)

submit_button = tk.Button(
    root, text="ثبت پاسخ", command=submit_answer, 
    font=("B Nazanin", 14, "bold"), bg="#4CAF50", fg="white", activebackground="#45a049"
)
submit_button.pack(pady=20)

# شروع بازی
show_question()

root.mainloop()