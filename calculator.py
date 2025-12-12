import tkinter as tk
import random

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator & Quiz App")
        self.root.geometry("400x600")
        self.root.configure(bg="#1e1e1e")
        self.calculator_menu()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def calculator_menu(self):
        self.clear_window()
        self.expression = ""

        # Display - put Entry inside a grey frame so grey background extends to the right
        display_frame = tk.Frame(self.root, bg="#2d2d2d")
        display_frame.pack(fill="x", padx=15, pady=20)

        display = tk.Entry(display_frame, font=("Arial", 28), justify="right", bd=0, relief="flat",
                           bg="#2d2d2d", fg="#00bcd4", insertbackground="#00bcd4", highlightthickness=0)
        # internal right padding so cursor appears shifted left while grey extends to right
        display.pack(fill="both", expand=True, padx=(0, 30), ipady=25)
        display.insert(0, "0")

        def update_display():
            display.delete(0, tk.END)
            display.insert(0, self.expression if self.expression else "0")

        def on_button_click(value):
            if value == "=":
                try:
                    result = eval(self.expression)
                    self.expression = str(result)
                    update_display()
                except Exception:
                    self.expression = ""
                    display.delete(0, tk.END)
                    display.insert(0, "Error")
            elif value == "C":
                self.expression = ""
                update_display()
            elif value == "←":
                self.expression = self.expression[:-1]
                update_display()
            else:
                self.expression += str(value)
                update_display()

        def on_key_press(event):
            ch = event.char
            keysym = event.keysym

            if ch and ch.isprintable():
                if ch.isdigit() or ch in "+-*/.":
                    on_button_click(ch)
                    return "break"   # prevent default insertion (avoids duplication)
            if keysym == "Return":
                on_button_click("=")
                return "break"
            if keysym == "BackSpace":
                on_button_click("←")
                return "break"
            # allow other keys

        display.bind("<Key>", on_key_press)
        display.focus()

        # Button frame with grid (4 columns x 5 rows)
        button_frame = tk.Frame(self.root, bg="#1e1e1e")
        button_frame.pack(fill="both", expand=True, padx=8, pady=8)

        # Equal weight columns/rows -> symmetric grid
        for c in range(4):
            button_frame.grid_columnconfigure(c, weight=1, uniform="col")
        for r in range(5):
            button_frame.grid_rowconfigure(r, weight=1, uniform="row")

        # Colors
        dark_btn_bg = "#000000"      # numbers, dot, backspace
        accent_bg = "#736868"        # operators, quiz, equals, clear
        dont_bg = "#800000"          # maroon for DON'T

        # DON'T button at row 0, colspan=2 (spans col 0 and 1)
        dont_btn = tk.Button(button_frame, text="DON'T", font=("Arial", 12, "bold"),
                             bg=dont_bg, fg="white", relief="flat", bd=0,
                             activebackground="#993333", activeforeground="white")
        dont_btn.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=4, pady=4)

        # Button factory helper
        def make_button(text, row, col, bg, cmd=None, font=("Arial", 16, "bold")):
            if cmd is None:
                btn = tk.Button(button_frame, text=text, font=font,
                                bg=bg, fg="#00bcd4" if bg == dark_btn_bg else "white",
                                relief="flat", bd=0,
                                activebackground="#1a1a1a" if bg == dark_btn_bg else "#8a7f7f",
                                activeforeground="#00bcd4" if bg == dark_btn_bg else "white",
                                command=(lambda v=text: on_button_click(v)))
            else:
                btn = tk.Button(button_frame, text=text, font=font,
                                bg=bg, fg="white",
                                relief="flat", bd=0,
                                activebackground="#8a7f7f",
                                activeforeground="white",
                                command=cmd)
            btn.grid(row=row, column=col, sticky="nsew", padx=4, pady=4)
            return btn

        # Row 0 remaining buttons (C at col2, Quiz at col3)
        make_button("C", 0, 2, accent_bg)
        make_button("Quiz", 0, 3, accent_bg, cmd=self.quiz_menu)

        # Row 1
        make_button("7", 1, 0, dark_btn_bg)
        make_button("8", 1, 1, dark_btn_bg)
        make_button("9", 1, 2, dark_btn_bg)
        make_button("*", 1, 3, accent_bg)

        # Row 2
        make_button("4", 2, 0, dark_btn_bg)
        make_button("5", 2, 1, dark_btn_bg)
        make_button("6", 2, 2, dark_btn_bg)
        make_button("-", 2, 3, accent_bg)

        # Row 3
        make_button("1", 3, 0, dark_btn_bg)
        make_button("2", 3, 1, dark_btn_bg)
        make_button("3", 3, 2, dark_btn_bg)
        make_button("+", 3, 3, accent_bg)

        # Row 4 bottom row
        make_button("0", 4, 0, dark_btn_bg)
        make_button(".", 4, 1, dark_btn_bg)
        make_button("←", 4, 2, dark_btn_bg)
        make_button("=", 4, 3, accent_bg)

    # Quiz-related methods (unchanged behavior)
    def generate_ques(self):
        num1 = random.randint(1, 15)
        num2 = random.randint(1, 15)
        operator = random.choice(["+", "-", "*"])
        if operator == "+":
            answer = num1 + num2
        elif operator == "-":
            answer = num1 - num2
        else:
            answer = num1 * num2
        return f"{num1} {operator} {num2}", answer

    def quiz_menu(self):
        self.clear_window()
        self.quiz_index = 0
        self.quiz_score = 0
        self.rounds = 5
        self.show_quiz_question()

    def show_quiz_question(self):
        self.clear_window()
        if self.quiz_index >= self.rounds:
            self.show_quiz_result()
            return

        question, answer = self.generate_ques()
        self.current_answer = answer

        tk.Label(self.root, text=f"Question {self.quiz_index + 1}/{self.rounds}",
                 font=("Arial", 12), bg="#1e1e1e", fg="#00bcd4").pack(pady=10)
        tk.Label(self.root, text=question, font=("Arial", 18, "bold"),
                 bg="#1e1e1e", fg="#ffffff").pack(pady=30)

        tk.Label(self.root, text="Your Answer:", bg="#1e1e1e", fg="#00bcd4").pack()
        entry = tk.Entry(self.root, width=20, font=("Arial", 14), bg="#2d2d2d",
                         fg="#00bcd4", insertbackground="#00bcd4", bd=0, relief="flat")
        entry.pack(pady=10, ipady=8)
        entry.focus()

        feedback_label = tk.Label(self.root, text="", font=("Arial", 12), bg="#1e1e1e")
        feedback_label.pack(pady=10)

        def check_answer():
            try:
                your_ans = int(entry.get())
                if your_ans == self.current_answer:
                    self.quiz_score += 1
                    feedback_label.config(text="✓ Correct!", fg="#4caf50")
                else:
                    feedback_label.config(text=f"✗ Wrong! Answer: {self.current_answer}", fg="#f44336")
                self.root.after(1000, lambda: self.next_question())
            except ValueError:
                feedback_label.config(text="Invalid input!", fg="#f44336")
                self.root.after(1000, lambda: entry.delete(0, tk.END))

        tk.Button(self.root, text="Submit", font=("Arial", 12), command=check_answer,
                  bg="#736868", fg="white", relief="flat", bd=0, padx=20, pady=8).pack(pady=10)
        tk.Button(self.root, text="Back to Calculator", font=("Arial", 12), command=self.calculator_menu,
                  bg="#736868", fg="white", relief="flat", bd=0, padx=20, pady=8).pack(pady=5)
        entry.bind("<Return>", lambda e: check_answer())

    def next_question(self):
        self.quiz_index += 1
        self.show_quiz_question()

    def show_quiz_result(self):
        self.clear_window()
        tk.Label(self.root, text="---GAME OVER---", font=("Arial", 18, "bold"),
                 bg="#1e1e1e", fg="#00bcd4").pack(pady=20)
        tk.Label(self.root, text=f"You scored {self.quiz_score} out of 5!", font=("Arial", 16),
                 bg="#1e1e1e", fg="#ffffff").pack(pady=20)
        if self.quiz_score == self.rounds:
            feedback = "EXCELLENT! You're a GENIUS!!"
        elif self.quiz_score > 2:
            feedback = "WORST EVER"
        else:
            feedback = "Can do better!"
        tk.Label(self.root, text=feedback, font=("Arial", 14, "bold"),
                 fg="#4caf50", bg="#1e1e1e").pack(pady=10)
        tk.Button(self.root, text="Back to Calculator", font=("Arial", 12), command=self.calculator_menu,
                  bg="#736868", fg="white", relief="flat", bd=0, padx=20, pady=8).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()