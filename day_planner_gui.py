import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import threading
import time
import winsound
import tkinter.font as tkFont

root = tk.Tk()
root.title("Day Planner")
root.geometry("500x600")
root.configure(bg="#f0f8ff")

font_style = ("Segoe UI", 12)

listbox = tk.Listbox(root, font=font_style, width=50, height=15, bg="#ffffff", fg="#333333")
listbox.pack(pady=20)

entry = tk.Entry(root, font=font_style, width=30)
entry.pack(pady=5)

time_entry = tk.Entry(root, font=font_style, width=20)
time_entry.pack(pady=5)
time_entry.insert(0, "HH:MM")

def check_alarms():
    while True:
        now = datetime.now().strftime("%H:%M")
        for i in range(listbox.size()):
            task = listbox.get(i)
            if now in task and "✅" not in task:
                listbox.delete(i)
                listbox.insert(i, "✅ " + task)
                show_popup(task)
                winsound.PlaySound("2247ee6b-580e-48bd-9bcc-bb648b38ed33.wav", winsound.SND_FILENAME)
        time.sleep(30)

def show_popup(task):
    popup = tk.Toplevel(root)
    popup.title("Task Reminder")
    popup.geometry("300x120+{}+{}".format(
        root.winfo_x() + root.winfo_width()//2 - 150,
        root.winfo_y() + root.winfo_height()//2 - 60
    ))
    popup.configure(bg="#fff3cd")
    tk.Label(popup, text="It's time for:", bg="#fff3cd", font=("Segoe UI", 10, "bold"), fg="#856404").pack(pady=(10,0))
    tk.Label(popup, text=task, bg="#fff3cd", font=("Segoe UI", 11)).pack(pady=(0,10))
    tk.Button(popup, text="OK", bg="#ffd966", command=popup.destroy).pack()

def add_task():
    task = entry.get()
    time_val = time_entry.get()
    if task and time_val:
        listbox.insert(tk.END, f"{task} at {time_val}")
        entry.delete(0, tk.END)
        time_entry.delete(0, tk.END)

def remove_selected(confirm=None, selected=None):
    if selected:
        listbox.delete(selected)
    if confirm:
        confirm.destroy()

def delete_task():
    selected = listbox.curselection()
    if not selected:
        return

    confirm = tk.Toplevel(root)
    confirm.title("Confirm Delete")
    confirm.geometry("300x120+{}+{}".format(
        root.winfo_x() + root.winfo_width()//2 - 150,
        root.winfo_y() + root.winfo_height()//2 - 60
    ))
    confirm.configure(bg="#ffe6e6")
    tk.Label(confirm, text="Delete this task?", font=("Segoe UI", 11, "bold"), bg="#ffe6e6", fg="#b22222").pack(pady=10)
    tk.Button(confirm, text="Yes", bg="#d32f2f", fg="white", command=lambda: remove_selected(confirm, selected)).pack(side="left", padx=30, pady=10)
    tk.Button(confirm, text="No", bg="#9e9e9e", fg="white", command=confirm.destroy).pack(side="right", padx=30, pady=10)

def zoom_in():
    current_font = tkFont.Font(font=listbox.cget("font"))
    new_size = current_font['size'] + 1
    listbox.config(font=(current_font['family'], new_size))

def zoom_out():
    current_font = tkFont.Font(font=listbox.cget("font"))
    new_size = max(8, current_font['size'] - 1)
    listbox.config(font=(current_font['family'], new_size))

button_frame = tk.Frame(root, bg="#f0f8ff")
button_frame.pack(pady=10)

add_button = tk.Button(button_frame, text="➕ Add Task", command=add_task, bg="#4caf50", fg="white", font=("Segoe UI", 10, "bold"))
delete_button = tk.Button(button_frame, text="🗑️ Delete Task", command=delete_task, bg="#f44336", fg="white", font=("Segoe UI", 10, "bold"))
exit_button = tk.Button(button_frame, text="❌ Exit", command=root.quit, bg="#9e9e9e", fg="white", font=("Segoe UI", 10, "bold"))
zoom_in_button = tk.Button(button_frame, text="🔍 Zoom In", command=zoom_in, bg="#2196f3", fg="white", font=("Segoe UI", 10, "bold"))
zoom_out_button = tk.Button(button_frame, text="🔎 Zoom Out", command=zoom_out, bg="#03a9f4", fg="white", font=("Segoe UI", 10, "bold"))

add_button.grid(row=0, column=0, padx=5)
delete_button.grid(row=0, column=1, padx=5)
exit_button.grid(row=0, column=2, padx=5)
zoom_in_button.grid(row=1, column=0, columnspan=2, pady=5)
zoom_out_button.grid(row=1, column=2, columnspan=2, pady=5)

alarm_thread = threading.Thread(target=check_alarms)
alarm_thread.daemon = True
alarm_thread.start()

root.mainloop()
