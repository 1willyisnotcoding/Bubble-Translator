import tkinter as tk
from tkinter import ttk
from deep_translator import GoogleTranslator
import time
import threading

bubble = tk.Tk()
bubble.title("Bubble")
bubble.overrideredirect(True)
bubble.geometry("100x100+100+100")
bubble.wm_attributes("-topmost", True)
bubble.wm_attributes("-transparentcolor", "black")

bubble_canvas = tk.Canvas(bubble, width=100, height=100, bg="black", highlightthickness=0)
bubble_canvas.pack(fill="both", expand=True)

for i in range(40, 0, -1):
    r = min(255, 10 + i * 6)
    g = min(255, 50 + i * 3)
    b = min(255, 180 + i * 2)
    color = f"#{r:02x}{g:02x}{b:02x}"
    bubble_canvas.create_oval(10+i, 10+i, 90-i, 90-i, fill=color, outline=color)

bubble_canvas.create_oval(65, 65, 45, 45, fill="white", outline="white")

translator_window = tk.Toplevel()
translator_window.title("Translator")
translator_window.overrideredirect(True)
translator_window.geometry("500x400")
translator_window.withdraw()
translator_window.configure(bg="#121212")

def close_translator():
    fade_out(translator_window, bubble)

exit_button = tk.Button(translator_window, text="X", bg="#121212", fg="white",
                        borderwidth=0, font=("Arial", 12, "bold"),
                        activebackground="#1f1f1f", activeforeground="red",
                        command=close_translator)
exit_button.pack(anchor="ne", padx=5, pady=5)

lang_frame = tk.Frame(translator_window, bg="#121212")
lang_frame.pack(pady=5, anchor="w", padx=15)

tk.Label(lang_frame, text="From:", bg="#121212", fg="white", font=("Arial", 10)).pack(side="left", padx=5)

lang_options = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
}
input_lang_var = tk.StringVar(value="English")

style = ttk.Style()
style.theme_use("clam")
style.configure("Custom.TCombobox",
                fieldbackground="#000000",
                background="#000000",
                foreground="white",
                arrowcolor="white")
style.map("Custom.TCombobox",
          fieldbackground=[("readonly", "#000000")],
          foreground=[("readonly", "white")])

lang_dropdown = ttk.Combobox(lang_frame, textvariable=input_lang_var,
                             values=list(lang_options.keys()), state="readonly",
                             width=12, font=("Arial", 10),
                             style="Custom.TCombobox")
lang_dropdown.pack(pady=5, padx=15, anchor="w")

def translate_text():
    text_in = input_box.get("1.0", tk.END).strip()
    if text_in:
        try:
            source_lang = lang_options[input_lang_var.get()]
            translated = GoogleTranslator(source=source_lang, target="zh-CN").translate(text_in)

            output_box.config(state="normal")
            output_box.delete("1.0", tk.END)
            output_box.insert(tk.END, translated)
            output_box.see("end")
        except Exception as e:
            output_box.config(state="normal")
            output_box.delete("1.0", tk.END)
            output_box.insert(tk.END, f"Error: {e}")

translate_button = tk.Button(translator_window, text="Translate",
                             bg="#2b2b2b", fg="white",
                             activebackground="#3a3a3a", activeforeground="white",
                             relief="flat", font=("Arial", 11, "bold"),
                             padx=12, pady=5, command=translate_text)
translate_button.pack(pady=8, anchor="w", padx=15)

tk.Label(translator_window, text="Input (Language selected):", bg="#121212", fg="white",
         font=("Arial", 10)).pack(anchor="w", padx=15)

input_box = tk.Text(translator_window, height=5, width=55, bg="#1e1e1e", fg="white",
                    insertbackground="white", relief="flat", wrap="word")
input_box.pack(pady=5, padx=15, anchor="w")

tk.Label(translator_window, text="Output (Mandarin):", bg="#121212", fg="white",
         font=("Arial", 10)).pack(anchor="w", padx=15)

output_frame = tk.Frame(translator_window, bg="#121212")
output_frame.pack(pady=5, padx=15, anchor="w", fill="both", expand=True)

output_box = tk.Text(output_frame, height=12, bg="#1e1e1e", fg="#00ff7f",
                     insertbackground="white", relief="flat", wrap="word", state="normal")
output_box.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(output_frame, command=output_box.yview)
scrollbar.pack(side="right", fill="y")
output_box.config(yscrollcommand=scrollbar.set)

def _on_mousewheel_win(event):
    output_box.yview_scroll(-int(event.delta/120), "units")

def _on_mousewheel_linux_up(event):
    output_box.yview_scroll(-1, "units")

def _on_mousewheel_linux_down(event):
    output_box.yview_scroll(1, "units")

output_box.bind("<MouseWheel>", _on_mousewheel_win)     
output_box.bind("<Button-4>", _on_mousewheel_linux_up)  
output_box.bind("<Button-5>", _on_mousewheel_linux_down)

def fade_in(win, other):
    bx, by = bubble.winfo_x(), bubble.winfo_y()
    win.geometry(f"500x400+{bx}+{by}")

    screen_w = win.winfo_screenwidth()
    screen_h = win.winfo_screenheight()
    win_w = win.winfo_width()
    win_h = win.winfo_height()

    x = min(max(bx, 0), screen_w - win_w)
    y = min(max(by, 0), screen_h - win_h)

    win.geometry(f"{win_w}x{win_h}+{x}+{y}")

    other.withdraw()
    win.deiconify()
    win.lift()
    win.attributes("-alpha", 0.0)
    for i in range(11):
        win.attributes("-alpha", i / 10)
        win.update()
        time.sleep(0.02)

def fade_out(win, other):
    for i in reversed(range(11)):
        win.attributes("-alpha", i / 10)
        win.update()
        time.sleep(0.02)
    win.withdraw()
    other.deiconify()
    other.lift()

dragging = False
start_x = start_y = 0

def start_drag(event):
    global dragging, start_x, start_y
    dragging = False
    start_x, start_y = event.x_root, event.y_root 

def do_drag(event):
    global dragging, start_x, start_y
    dragging = True

    dx = event.x_root - start_x
    dy = event.y_root - start_y
    start_x, start_y = event.x_root, event.y_root

    x = bubble.winfo_x() + dx
    y = bubble.winfo_y() + dy

    bubble.geometry(f"+{x}+{y}")

def stop_drag(event):
    global dragging
    if not dragging:
        threading.Thread(target=lambda: fade_in(translator_window, bubble), daemon=True).start()

bubble_canvas.bind("<ButtonPress-1>", start_drag)
bubble_canvas.bind("<B1-Motion>", do_drag)
bubble_canvas.bind("<ButtonRelease-1>", stop_drag)

bubble.mainloop()
