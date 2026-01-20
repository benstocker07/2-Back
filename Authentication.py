# Copyright Ben Stocker, 2025
# See LICENSE.md for terms of use and restrictions.

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess, sys, requests, hashlib, time, os, socket, pkg_resources, threading
from datetime import datetime

subprocess.check_call([sys.executable, "-m", "pip", "install", "setuptools"])
#subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

url = "http://8mews.ddns.net:3312/numbers"

def show_offline_window():
    global status
    root = tk.Tk()
    root.title("Server Offline")
    w = 350
    h = 150
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw - w) // 2
    y = (sh - h) // 2
    root.geometry(f"{w}x{h}+{x}+{y}")
    root.resizable(False, False)

    label = tk.Label(root, text="Server is offline.\n\nWhat would you like to do?", font=("Arial", 12))
    label.pack(pady=10)

    def continue_local():
        global status
        status = 'local'
        root.destroy()

    def close_program():
        global status
        root.destroy()
        sys.exit()

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Continue Locally", width=15, font=("Arial", 10), command=continue_local).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Close Program", width=15, font=("Arial", 10), command=close_program).grid(row=0, column=1, padx=5)

    root.mainloop()

try:
    response = requests.get(url)

    if response.status_code == 200:
        numbers = response.text.split(", ")
        status = 'server'
        print('Server is online')

    if response.status_code == 502:
        show_offline_window()

except requests.exceptions.ConnectionError as e:
    show_offline_window()

global ResearcherKey

RID = None

from datetime import datetime
import os
import socket
import requests
import tkinter as tk
from tkinter import messagebox

def get_ip():
    return requests.get("https://api.ipify.org").text

def check_password(event=None):
    entered = entry.get()

    try:
        if entered in numbers:
            RID = entered
            ResearcherKey = f'UoP_Researcher_{RID}'
            URL = "http://8mews.ddns.net:3312/users/idcode" 

            now = datetime.now().isoformat(sep=" ", timespec="seconds")

            try:
                ip_addr = get_ip()

            except requests.exceptions.ConnectionError as e:
                print(e)
                ip_addr = None

            payload = {
                "IDCode": ResearcherKey,
                "created_at": now,
                "ip_address": str(ip_addr)
            }

            headers = {
                "X-API-Key": ResearcherKey
            }
            
            if status == 'server':
                response = requests.post(URL, json=payload, headers=headers)

            os.environ["ResearcherKey"] = ResearcherKey
            
            root.destroy()
        else:
            messagebox.showerror("Access Denied", "Incorrect password.")
            entry.delete(0, tk.END)

    except NameError as e:
        print(e)

def on_closing():
    messagebox.showwarning("Action Denied", "You must login to access the task")
    
root = tk.Tk()
root.iconbitmap(default="")
root.title("Password Entry")
root.configure(bg="white")

window_width = 400
window_height = 200
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

frame = tk.Frame(root, bg="white")
frame.pack(expand=True, fill="both")

tk.Label(frame, text="Enter Researcher Key:", bg="white", fg="#333", font=("Arial", 14)).pack(pady=20)
entry = tk.Entry(frame, show="*", font=("Arial", 14), justify="center")
entry.pack(pady=10)
entry.focus()

tk.Button(frame, text="Submit", command=check_password, bg="#4caf50", fg="white", font=("Arial", 12, "bold")).pack(pady=20)

root.bind("<Return>", check_password)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

def update_status(message, percent_value):
    global percent
    percent = percent_value
    status_label.config(text=message)
    progress_bar['value'] = percent
    percent_label.config(text=f"{percent}%")
    root.update_idletasks()

def installation_and_joystick_check():
    packages_to_install = [
        "pygame", "pandas", "pymysql", "numpy", "scipy", "setuptools"
    ]

    installed_packages = {pkg.key for pkg in pkg_resources.working_set}
    package_to_find = 'pandas'
    update_status(f"Checking dependencies...", 10)
    time.sleep(1)
    
    if package_to_find not in installed_packages:
        progress = 20
        increment = int(80 / len(packages_to_install))

        for package in packages_to_install:
            progress = min(progress + increment, 80)
            update_status(f"Importing {package}...", progress)
            try:
                subprocess.check_call(["pip", "install", package])
            except subprocess.CalledProcessError as e:
                print(f"Failed to install {package}: {e}")
                    
    else:
        update_status("All packages already installed.", 80)
        time.sleep(1)

    update_status("Initialising Dependencies...", 80)
    time.sleep(0.3)

    update_status("Initialising remaining modules...", 90)
    time.sleep(0.3)

    try:
        update_status("Connecting to pygame window", 97)
        update_status(f"Pygame connected", 100)
    except pygame.error as e:
        print()

    root.after(2000, root.destroy)

def start_thread():
    thread = threading.Thread(target=installation_and_joystick_check)
    thread.start()

root = tk.Tk()
root.title("2-Back Setup")
root.geometry("400x120")
root.resizable(False, False)
root.configure(bg="white")
root.attributes("-topmost", True)

root.update_idletasks()
window_width = root.winfo_width()
window_height = root.winfo_height()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

status_label = tk.Label(root, bg="white", text="Preparing installation...", font=("Arial", 12))
status_label.pack(pady=5)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=5)
progress_bar['maximum'] = 100

percent_label = tk.Label(root, bg="white", text="0%", font=("Arial", 10))
percent_label.pack()

percent = 0
root.after(99, start_thread)
update_status("Welcome to the task!\n\n It is now loading the required files.", 0)
time.sleep(5)
root.mainloop()

