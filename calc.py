import tkinter as tk
import math

class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Enhanced Calculator")
        self.window.geometry("375x667")
        self.window.resizable(False, False)

        self.expression = ""
        self.history = []

        self.display = tk.Entry(
            self.window,
            font=("Arial", 28),
            justify="right",
            state="readonly"
        )
        self.display.pack(fill="both", padx=10, pady=20, ipady=15)

        self.buttons_frame = tk.Frame(self.window)
        self.buttons_frame.pack(expand=True, fill="both")

        buttons = [
            ["C", "⌫", "%", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["+/-", "0", ".", "="],
            ["x²", "√", "History", ""]
        ]

        for r, row in enumerate(buttons):
            self.buttons_frame.rowconfigure(r, weight=1)
            for c, text in enumerate(row):
                self.buttons_frame.columnconfigure(c, weight=1)

                if text:
                    button = tk.Button(
                        self.buttons_frame,
                        text=text,
                        font=("Arial", 18, "bold"),
                        command=lambda value=text: self.click(value)
                    )
                    button.grid(
                        row=r, column=c,
                        sticky="nsew", padx=2, pady=2
                    )

    def update_display(self):
        self.display.config(state="normal")
        self.display.delete(0, tk.END)
        self.display.insert(0, self.expression)
        self.display.config(state="readonly")

    def click(self, value):
        if value == "C":
            self.expression = ""

        elif value == "⌫":
            self.expression = self.expression[:-1]

        elif value == "+/-":
            try:
                self.expression = str(-float(self.expression))
            except ValueError:
                pass

        elif value == "%":
            try:
                self.expression = str(float(self.expression) / 100)
            except ValueError:
                self.expression = "Error"

        elif value == "x²":
            try:
                self.expression = str(eval(self.expression + "**2"))
            except Exception:
                self.expression = "Error"

        elif value == "√":
            try:
                self.expression = str(math.sqrt(float(self.expression)))
            except Exception:
                self.expression = "Error"

        elif value == "=":
            self.calculate()
            return

        elif value == "History":
            self.show_history()
            return

        else:
            if self.expression == "Error":
                self.expression = ""
            self.expression += value

        self.update_display()

    def calculate(self):
        try:
            result = eval(
                self.expression,
                {"__builtins__": None},
                {}
            )

            if isinstance(result, complex):
                raise ValueError("Invalid result")

            original = self.expression
            self.expression = str(result)

            self.history.append(original + " = " + self.expression)

        except Exception:
            self.expression = "Error"

        self.update_display()

    def show_history(self):
        history_window = tk.Toplevel(self.window)
        history_window.title("Calculation History")
        history_window.geometry("350x400")

        tk.Label(
            history_window,
            text="Calculation History",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        history_text = tk.Listbox(
            history_window,
            font=("Arial", 13)
        )
        history_text.pack(expand=True, fill="both", padx=10, pady=10)

        for item in self.history:
            history_text.insert(tk.END, item)

        tk.Button(
            history_window,
            text="Clear History",
            command=lambda: self.clear_history(history_text)
        ).pack(pady=10)

    def clear_history(self, history_text):
        self.history.clear()
        history_text.delete(0, tk.END)

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    calc = Calculator()
    calc.run()
