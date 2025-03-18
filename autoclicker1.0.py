import tkinter as tk
from tkinter import messagebox
import threading
import time
import webbrowser
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Listener
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

toggle_key = ""
click_interval = 0.1
clicking = False
program_running = True
listener = None
clicker_thread = None
mouse = MouseController()
root = None
toggle_key_label = None
interval_entry = None
info_label = None
status_label = None
capture_button = None
start_button = None
linkedin_button = None

def key_to_str(key):
    try:
        return key.char.lower()
    except AttributeError:
        return str(key).replace("Key.", "").lower()

def clicker():
    global clicking, program_running
    while program_running:
        if clicking:
            mouse.click(Button.left)
            time.sleep(click_interval)
        else:
            time.sleep(0.1)

def on_press(key):
    global clicking, program_running, toggle_key
    if toggle_key and key_to_str(key) == toggle_key:
        clicking = not clicking
        root.after(0, update_status_label)
    elif key_to_str(key) == "esc":
        program_running = False
        root.after(0, exit_program)

def start_key_capture():
    info_label.configure(text="Presiona la tecla para asignar como toggle...", foreground="#FFD700")
    root.bind("<Key>", capture_key)

def capture_key(event):
    global toggle_key
    key_str = event.keysym.lower()
    root.unbind("<Key>")
    if messagebox.askyesno("Confirmar tecla", f"¿Asignar '{key_str.upper()}' como toggle?"):
        toggle_key = key_str
        toggle_key_label.configure(text=f"Toggle: {toggle_key.upper()}")
        info_label.configure(text="Tecla asignada correctamente.", foreground="#00FF00")
    else:
        info_label.configure(text="Captura cancelada. Intenta de nuevo.", foreground="#FF4500")

def start_autoclicker():
    global click_interval, listener, clicker_thread
    try:
        ms = int(interval_entry.get())
        click_interval = ms / 1000.0
    except ValueError:
        messagebox.showerror("Error", "Intervalo inválido. Usa un número entero.")
        return
    if not toggle_key:
        messagebox.showerror("Error", "Asigna una tecla toggle antes de iniciar.")
        return
    capture_button.configure(state="disabled")
    start_button.configure(state="disabled")
    interval_entry.configure(state="disabled")
    info_label.configure(text="Configuración guardada. Usa el toggle para activar/desactivar.", foreground="#00FF00")
    if listener is None:
        listener = Listener(on_press=on_press)
        listener.start()
    if clicker_thread is None or not clicker_thread.is_alive():
        clicker_thread = threading.Thread(target=clicker, daemon=True)
        clicker_thread.start()

def update_status_label():
    if clicking:
        status_label.configure(text="Estado: ACTIVADO", bootstyle="success")
        capture_button.configure(state="disabled")
        interval_entry.configure(state="disabled")
        start_button.configure(state="disabled")
    else:
        status_label.configure(text="Estado: DESACTIVADO", bootstyle="danger")
        capture_button.configure(state="normal")
        interval_entry.configure(state="normal")
        start_button.configure(state="normal")

def exit_program():
    global program_running
    program_running = False
    if listener is not None:
        listener.stop()
    root.destroy()

def open_linkedin():
    webbrowser.open("https://www.linkedin.com/in/martiaaguilera/")

def create_interface():
    global root, capture_button, start_button, interval_entry, info_label, toggle_key_label, status_label, linkedin_button
    style = ttk.Style("darkly")
    root = style.master
    root.title("Autoclicker 1.0")
    root.geometry("500x400")
    root.resizable(False, False)
    title_frame = ttk.Frame(root)
    title_frame.pack(pady=15)
    title_label = ttk.Label(title_frame, text="Autoclicker 1.0", font=("Helvetica", 24, "bold"))
    title_label.pack()
    frame_toggle = ttk.Frame(root)
    frame_toggle.pack(pady=10, padx=20, fill="x")
    toggle_key_label = ttk.Label(frame_toggle, text="Toggle: ---", font=("Helvetica", 14))
    toggle_key_label.pack(side="left", padx=5)
    capture_button = ttk.Button(frame_toggle, text="Capturar toggle", command=start_key_capture, bootstyle="info")
    capture_button.pack(side="right", padx=5)
    frame_interval = ttk.Frame(root)
    frame_interval.pack(pady=10, padx=20, fill="x")
    interval_label = ttk.Label(frame_interval, text="Intervalo (ms):", font=("Helvetica", 14))
    interval_label.pack(side="left", padx=5)
    interval_entry = ttk.Entry(frame_interval, width=10, font=("Helvetica", 14))
    interval_entry.insert(0, "100")
    interval_entry.pack(side="right", padx=5)
    start_button = ttk.Button(root, text="Iniciar Autoclicker", command=start_autoclicker, bootstyle="primary")
    start_button.pack(pady=15)
    info_label = ttk.Label(root, text="Configura el toggle y el intervalo.", font=("Helvetica", 12))
    info_label.pack(pady=5)
    status_label = ttk.Label(root, text="Estado: DESACTIVADO", font=("Helvetica", 14, "bold"), bootstyle="danger")
    status_label.pack(pady=5)
    exit_button = ttk.Button(root, text="Salir", command=exit_program, bootstyle="secondary")
    exit_button.pack(pady=10)
    bottom_frame = ttk.Frame(root)
    bottom_frame.pack(pady=5, fill="x", padx=20)
    linkedin_button = ttk.Button(bottom_frame, text="LinkedIn", command=open_linkedin, bootstyle="info-outline")
    linkedin_button.pack(side="left", anchor="w", padx=5)
    credits_label = ttk.Label(bottom_frame, text="Créditos: martiaaguilera", font=("Helvetica", 10))
    credits_label.pack(side="right", anchor="e")
    root.mainloop()

if __name__ == '__main__':
    create_interface()
