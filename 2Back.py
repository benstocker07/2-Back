# Copyright Ben Stocker, 2025
# See LICENSE.md for terms of use and restrictions.

global Test

Test = False

import Authentication
import tkinter as tk
from tkinter import messagebox
import hashlib, requests, time
from pathlib import Path
from Authentication import *
from tkinter import ttk

def show_interval_window(seconds=120):
    interval_root = tk.Tk()
    interval_root.title("Interval")
    interval_root.resizable(False, False)
    width, height = 600, 350

    screen_width = interval_root.winfo_screenwidth()
    screen_height = interval_root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    interval_root.geometry(f"{width}x{height}+{x}+{y}")

    label = tk.Label(interval_root, text="", font=("Arial", 24), wraplength=550, justify="center")
    label.pack(pady=20)

    progress = ttk.Progressbar(interval_root, orient="horizontal", length=500, mode="determinate")
    progress.pack(pady=10)
    progress["maximum"] = seconds
    progress["value"] = 0

    def countdown(count):
        label.config(text=f"Thank you for your participation so far!\n\nTake this time to rest.\n\nTime remaining: {count} secs")
        progress["value"] = seconds - count
        if count > 0:
            interval_root.after(1000, countdown, count-1)
        else:
            interval_root.destroy()

    countdown(seconds)
    interval_root.mainloop()

ResearcherKey = os.getenv("ResearcherKey")
host = '8mews.ddns.net'

row_id = None

def send_BAC(value):
    global row_id  
    URL = f"http://{host}:3312/participants/start"

    payload = {
        "participant_number": entered,
        "BAC_Start": value
    }

    headers = {
        "X-API-Key": ResearcherKey,
        "Content-Type": "application/json"
    }

    response = requests.post(URL, json=payload, headers=headers)
    
    if response.status_code == 201:
        data = response.json()
        row_id = data["id"]  
        return row_id
    else:
        print("Error:", response.status_code, response.text)
        return None


def end_BAC(value):
    global row_id
    if row_id is None:
        print("Error: Cannot submit BAC_End before BAC_Start")
        return

    URL = f"http://{host}:3312/participants/end"

    payload = {
        "id": row_id,
        "BAC_End": value
    }

    headers = {
        "X-API-Key": ResearcherKey,
        "Content-Type": "application/json"
    }

    response = requests.post(URL, json=payload, headers=headers)

    if response.status_code == 200:
        print("BAC_End updated:", response.json())
    else:
        print("Error:", response.status_code, response.text)


BAC_Count = 0

def BAC():
    global BAC_Count
    
    BAC_Count += 1

    def submit_bac(event=None):
        entered = entry.get().strip()
        if not entered:
            messagebox.showerror("Error", "Please enter a BAC level.")
            return
        show_confirmation(entered)

    def show_confirmation(value):
        for widget in frame.winfo_children():
            widget.destroy()

        tk.Label(frame, text=f"BAC entered: {value}", bg="white", fg="#333", font=("Arial", 14)).pack(pady=20)

        tick_var = tk.IntVar()
        tk.Checkbutton(frame, text="Confirm this is correct", variable=tick_var, bg="white", font=("Arial", 12)).pack(pady=10)

        def confirm():
            if tick_var.get():
                root.destroy()
                if BAC_Count > 0:
                    send_BAC(value)

                if BAC_Count > 1:
                    end_BAC(value)
            else:
                messagebox.showwarning("Confirmation Needed", "Please tick the box to confirm.")

        def reenter():
            for widget in frame.winfo_children():
                widget.destroy()
            show_entry()

        tk.Button(frame, text="Confirm", command=confirm, bg="#4caf50", fg="white", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Button(frame, text="Re-enter", command=reenter, bg="#f44336", fg="white", font=("Arial", 12, "bold")).pack(pady=5)

    def show_entry():
        tk.Label(frame, text="Enter BAC Level:", bg="white", fg="#333", font=("Arial", 14)).pack(pady=20)
        global entry
        entry = tk.Entry(frame, font=("Arial", 14), justify="center")
        entry.pack(pady=10)
        entry.focus()
        tk.Button(frame, text="Submit", command=submit_bac, bg="#4caf50", fg="white", font=("Arial", 12, "bold")).pack(pady=20)
        root.bind("<Return>", submit_bac)

    def on_closing():
        messagebox.showwarning("BAC Required", "You must provide a BAC measurement.")

    root = tk.Tk()
    root.title("BAC Entry")
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

    show_entry()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

def check_password(event=None):
    global entered
    entered = entry.get()

    def check_participant_number(entered):
        url = f"http://{host}:3312/reaction_times/check"
        params = {"participant_number": entered}

        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data["exists"]:
                messagebox.showerror("Error", data["message"])
                return False
            else:
                root.destroy()
        else:
            messagebox.showerror("Error", "Could not check participant number.")
            return False
    
    if len(entered) > 0:
        check_participant_number(entered)
        
    else:
        messagebox.showerror("Participant ID Entry", "Please provide a participant number.")
        entry.delete(0, tk.END)

def on_closing():
    messagebox.showwarning("Value Missing", "Please provide a participant number")
    
root = tk.Tk()
root.iconbitmap(default="")
root.title("Participant ID Entry")
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

tk.Label(frame, text="Enter Participant Number:", bg="white", fg="#333", font=("Arial", 14)).pack(pady=20)
entry = tk.Entry(frame, font=("Arial", 14), justify="center")
entry.pack(pady=10)
entry.focus()

tk.Button(frame, text="Submit", command=check_password, bg="#4caf50", fg="white", font=("Arial", 12, "bold")).pack(pady=20)

root.bind("<Return>", check_password)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

import subprocess, pygame, math, sys, shutil, ctypes
from pygame.locals import *
import random, time, os

os.chdir(os.path.dirname(__file__))

import pandas as pd
from datetime import datetime
from scipy.stats import norm
import csv, sqlite3
import numpy as np
import json, threading
from datetime import datetime

def display_license():
        with open("LICENSE.txt", "r", encoding="utf-8") as f:
            license_text = f.read()
        print("\n=== LICENSE NOTICE ===")
        print(license_text)
        print("======================\n")
        time.sleep(5)

display_license()
learning = 20
noise_trials = learning

count_file = 'N-Back count.txt'

if os.path.exists(count_file):
    with open(count_file, 'r') as f:
        count = int(f.read())
else:
    count = 0

count += 1

with open(count_file, 'w') as f:
    f.write(str(count))

BAC()

def login():
    global participant_number
    while True:
        participant_number = entered
        p2 = participant_number

        if p2 == participant_number:
            with open('participant number.txt', "w+") as file:
                file.write(participant_number)
            break
        else:
            print("\nIncorrect match of participant number. Re-check the number.\n")

login()

folder_name = f'Data/Participant {participant_number}'

try:
    data_dir = Path(__file__).resolve().parent.parent / "Data"
    data_dir.mkdir(exist_ok=True)

    participant_dir = data_dir / f"Participant {participant_number}"
    participant_dir.mkdir(exist_ok=False)

    print(f"Created folder for Participant {participant_number}: {participant_dir}")

except FileExistsError:
    print(f"Folder for Participant {participant_number} already exists.")

LOCAL_SAVE_PATH = f'{participant_dir}/Participant {entered}.csv'

def save_locally(participant_number, reactiontime, score):
    file_exists = os.path.isfile(LOCAL_SAVE_PATH)
    with open(LOCAL_SAVE_PATH, mode="a", newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["timestamp", "participant_number", "reaction_time", "score"])
        writer.writerow([datetime.now().isoformat(), participant_number, reactiontime, score])

db_filename = f'{data_dir}/N-Back.db'

db_connection = sqlite3.connect(db_filename)
db_cursor = db_connection.cursor()

db_cursor.execute('''
    CREATE TABLE IF NOT EXISTS SensitivityScores (
        Z_Hit VAR(255),
        Z_False VAR(255),
        Sensitivity VAR(255),
        ResponseBias VAR(255)
    )
''')
    
db_cursor.execute('''
    CREATE TABLE IF NOT EXISTS Scores (
        timestamp TEXT,
        participant_number TEXT,
        counter INT,
        score INT,
        task_type TEXT,
        NoResponse TEXT,
        key TEXT
    )
''')

db_cursor.execute('''
    CREATE TABLE IF NOT EXISTS ReactionTimes (
        timestamp TEXT,
        participant_number TEXT,
        counter INT,
        reaction_time REAL,
        task_type TEXT,
        NoResponse TEXT,
        key TEXT
    )
''')

db_connection = sqlite3.connect(db_filename)
db_cursor = db_connection.cursor()

db_cursor.execute('''
    CREATE TABLE IF NOT EXISTS Scores (
        timestamp TEXT,
        participant_number TEXT,
        counter INT, 
        score INT,
        task_type TEXT,
        NoResponse TEXT,
        key TEXT
    )
''')

db_cursor.execute('''
    CREATE TABLE IF NOT EXISTS ReactionTimes (
        timestamp TEXT,
        participant_number TEXT,
        counter INT,
        reaction_time REAL,
        task_type TEXT
        NoResponse TEXT,
        key TEXT
    )
''')

global nb

nb = None

def task():
 
    pygame.init()
    info = pygame.display.Info()


    SCREEN_WIDTH, SCREEN_HEIGHT = (
        pygame.display.Info().current_w,
        pygame.display.Info().current_h,
    )

    WINDOW_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
    
    fullscreen = False

    if fullscreen:
        screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
    
    else:

        screen = pygame.display.set_mode(
            (info.current_w, info.current_h)
        )
        
    pygame.display.set_caption("N-Back")

    now = datetime.now()

    pygame.font.init()

    date_time_string = now.strftime("%d-%m-%y")
    outputtime = now.strftime("%H:%M:%S")

    FONT_SIZE = 240
    nbsize = pygame.font.SysFont('Arial', FONT_SIZE)

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
        
    def generate_sequence(length):
        return [random.randint(0, 9) for _ in range(length)]

    def play_n_back(n, length):
        sequence = generate_sequence(length)
        
        for i in range(n, length):
            if sequence[i] == sequence[i - n]:
                print(f"Match! Current digit is {sequence[i]}")
            else:
                print(f"No match. Current digit is {sequence[i]}")
            time.sleep(1)

    def draw_text(text, position, color):
        text_surface = nbsize.render(text, True, color)
        text_rect = text_surface.get_rect(center=position)
        screen.blit(text_surface, text_rect)

    KEY_MAPPING = {
        pygame.K_j: True,
        pygame.K_f: False
    }

    skip = None
    
    pygame.font.init()

    pygame.event.pump()

    os.environ["SDL_VIDEO_CENTERED"] = "1"

    font = pygame.font.Font(None, 32)

    order = 1

    start_time = pygame.time.get_ticks()

    Game_Running = True

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen.fill(WHITE)
    pygame.display.set_caption("Welcome to the Task")
    font = pygame.font.Font(None, 60)
    text = font.render("Welcome to the Task", True, BLACK)
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(text, text_rect)

    def nbacktrue():
        text = font.render("Welcome to the Task", True, BLACK)
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(text, text_rect)

    correctinterval = pygame.image.load("greentick.png")
    correctintervaldimensions = correctinterval.get_rect(center=screen.get_rect().center) 

    incorrectinterval = pygame.image.load("redcross.png")
    incorrectintervaldimensions = incorrectinterval.get_rect(center=screen.get_rect().center)
    def generate_sequence(length):
        
        global nbackno

        nbackno = math.ceil(sequence_length / 3)

        sequence = [random.randint(1, 9) for _ in range(length)]
        for _ in range(nbackno):
            index = random.randint(n, length - 1)
            sequence[index] = sequence[index - n]

        return sequence

        db_cursor.execute('''
        CREATE TABLE IF NOT EXISTS Configuration (
            NBacks VAR(255),
            SequenceLength VAR(255)
        )
        ''')

        db_cursor.execute(
        "INSERT INTO Configuration (NBacks, SequenceLength) VALUES (?, ?)",
        (nbackno, sequence_length)
        )

        url = f"http://{host}:3312/configuration"

        data = {
            "NBacks": nbackno,
            "SequenceLength": sequence_length
        }

        headers = {
            "X-API-Key": API_KEY
        }

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 201:
            print("Configuration saved")
        else:
            print(response.status_code, response.text)

    n = 2  
    sequence_length = 120

    total_trials = sequence_length + learning
    
    sequence = generate_sequence(sequence_length)

    current_index = 0
    score = 0
    running = True
        
    learningconv = learning-1

    def incorrect():
        incorrectanswer = True
        endRT = time.time()
        screen.fill(WHITE)
        if current_index < 40:
            screen.blit(incorrectinterval, incorrectintervaldimensions)
        pygame.time.wait(500)
        pygame.display.update()
        pygame.time.wait(500)
        score = 0
        
    def correct():
        correctanswer = True
        endRT = time.time()
        screen.fill(WHITE)
        if current_index < 40:
            screen.blit(correctinterval, correctintervaldimensions)
        pygame.time.wait(500)
        pygame.display.update()
        pygame.time.wait(500)
        score = 1
            
    global timer2
    
    timer2 = time.time()
    hits = 0
    false_alarms = 0
    stim = True

    block = 1

    while running:        
        starterRT = time.time()

        keypress = None  

        elapsed = starterRT - timer2

        timer2 = time.time()

        endRT = time.time()
        RT = (endRT - starterRT)

        screen.fill(WHITE)
        pygame.display.update()
        pygame.time.wait(500)

        delay = (random.randint(0,5)*100)+1000
        pygame.time.wait(delay)        

        draw_text(str(sequence[current_index]), (WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2), BLACK)

        starting = pygame.time.get_ticks()
        
        pygame.display.update()
        
        screen.fill(WHITE)

        keyprocessed = False

        score = 0
        
        while True:

            currenttime = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                elif event.type == pygame.KEYDOWN and not keyprocessed:
                    key_name = pygame.key.name(event.key)
                                                     
                    if event.key in KEY_MAPPING:                        
                        keypress = True
                        keyprocessed = True
                        reactiontime = currenttime - starting                           
                        
                        if sequence[current_index] == sequence[current_index - n]:
                            if event.key == pygame.K_j:
                                if block == 1:
                                    correct()
                                score += 1
                                hits += 1

                            elif event.key == pygame.K_f:
                                if block == 1:
                                    incorrect()
                                false_alarms += 1
               
                        else:
                            if event.key == pygame.K_j:
                                if block == 1:
                                    incorrect()
                                false_alarms += 1
                      
                            elif event.key == pygame.K_f:
                                if block == 1:
                                    correct()
                                score += 1
                
            if currenttime - starting >= 2000:
                if keyprocessed == False:
                    reactiontime = 0

                screen.fill(WHITE)
                pygame.display.update()

                global nb

                name = "N-Back" if nb else ""
        
                def emptyscorerecord():
                    date_time_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    with db_connection:
                        db_cursor.execute(
                            "INSERT INTO Scores (timestamp, participant_number, counter, score, task_type, NoResponse) VALUES (?, ?, ?, ?, ?, ?)",
                            (date_time_string, participant_number, count, "0", name, "No Response")
                        )
                    requests.post(
                        f'http://{host}:3312/scores',
                        json={
                            "timestamp": date_time_string,
                            "participant_number": participant_number,
                            "counter": count,
                            "score": '0',
                            "task_type": "2-back",
                            "NoResponse": "1",
                            "user_key": "N/A"
                        },
                        headers={
                            "X-API-Key": ResearcherKey
                        }
                    )

                def emptyrtrecord():
                    date_time_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    with db_connection:
                        db_cursor.execute(
                            "INSERT INTO ReactionTimes (timestamp, participant_number, counter, reaction_time, task_type, NoResponse) VALUES (?, ?, ?, ?, ?, ?)",
                            (date_time_string, participant_number, count, "0", name, "No Response")
                        )
                    requests.post(
                        f'http://{host}:3312/reaction_times',
                        json={
                            "timestamp": date_time_string,
                            "participant_number": participant_number,
                            "counter": count,
                            "reaction_time": '0',
                            "task_type": name,
                            "NoResponse": "1",
                            "user_key": "N/A"
                        },
                        headers={
                            "X-API-Key": ResearcherKey
                        }
                    )

                def scorerecord():
                    date_time_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    with db_connection:
                        db_cursor.execute(
                            "INSERT INTO Scores (timestamp, participant_number, counter, score, task_type, key) VALUES (?, ?, ?, ?, ?, ?)",
                            (date_time_string, participant_number, count, score, name, key_name)
                        )
                    requests.post(
                        f'http://{host}:3312/scores',
                        json={
                            "timestamp": date_time_string,
                            "participant_number": participant_number,
                            "counter": count,
                            "score": score,
                            "task_type": name,
                            "NoResponse": "0",
                            "user_key": key_name
                        },
                        headers={
                            "X-API-Key": ResearcherKey
                        }
                    )

                def rtrecord():
                    date_time_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    with db_connection:
                        db_cursor.execute(
                            "INSERT INTO ReactionTimes (timestamp, participant_number, counter, reaction_time, task_type, key) VALUES (?, ?, ?, ?, ?, ?)",
                            (date_time_string, participant_number, count, reactiontime, name, key_name)
                        )
                    requests.post(
                        f'http://{host}:3312/reaction_times',
                        json={
                            "timestamp": date_time_string,
                            "participant_number": participant_number,
                            "counter": count,
                            "reaction_time": reactiontime,
                            "task_type": name,
                            "NoResponse": "0",
                            "user_key": key_name
                        },
                        headers={
                            "X-API-Key": ResearcherKey 
                        }
                    )
                                        
                save_locally(participant_number, reactiontime, score)

                nb = None
                        
                if keyprocessed == True:
                    rtrecord()
                    scorerecord()

                else:
                    emptyrtrecord()
                    emptyscorerecord()
                break
        
        if sequence[current_index] == sequence[current_index - n]:
            nb = True
            nbacktrue()
            
        current_index += 1

        print(f'Trial No: {current_index}')

        if current_index == sequence_length//3:
            show_interval_window(120)
            block = 2

        if current_index == (sequence_length//3)*2:
            show_interval_window(120)
            block = 3

        print(f'Block: {block}')

        if current_index >= sequence_length:
            running = False

            def calculate_d_prime_and_c(hits, false_alarms, signal_trials, noise_trials):
                hit_rate = hits / signal_trials
                false_alarm_rate = false_alarms / noise_trials

                eps = 1e-10

                false_alarm_rate = max(eps, min(1 - eps, false_alarm_rate))

                z_false_alarm = norm.ppf(false_alarm_rate)
                z_hit = norm.ppf(hit_rate)

                d_prime = z_hit - z_false_alarm
                c_prime = -(z_hit + z_false_alarm) / 2

                return z_hit, z_false_alarm, d_prime, c_prime

            now = datetime.now()

            if hits > 0 and false_alarms > 0:
                z_hit, z_false_alarm, d_prime, c_prime = calculate_d_prime_and_c(hits, false_alarms, total_trials, noise_trials)

                with db_connection:
                    db_cursor.execute(
                        "INSERT INTO SensitivityScores (Z_Hit, Z_False, Sensitivity, ResponseBias) VALUES (?, ?, ?, ?)",
                        (z_hit, z_false_alarm, d_prime, c_prime))
            else:
                d_prime = 0
                c_prime = 0
            
            def main():
                pygame.init()
                width, height = 800, 600
                screen = pygame.display.set_mode((width, height))
                pygame.display.set_caption("Thank You")
                WHITE = (255, 255, 255)
                BLACK = (0, 0, 0)
                GRAY = (200, 200, 200)
                font = pygame.font.Font(None, 72)
                small_font = pygame.font.Font(None, 48)
                text = "Thank you for completing the task"
                text_surf = font.render(text, True, BLACK)
                text_rect = text_surf.get_rect(center=(width // 2, height // 2 - 50))
                button_text = small_font.render("Exit (press J)", True, BLACK)
                button_rect = button_text.get_rect(center=(width // 2, height // 2 + 100))
                clock = pygame.time.Clock()
                running = True
                while running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_j:
                            running = False
                            
                    screen.fill(WHITE)
                    pygame.draw.rect(screen, GRAY, button_rect.inflate(40, 20))
                    screen.blit(text_surf, text_rect)
                    screen.blit(button_text, button_rect)
                    pygame.display.flip()
                    clock.tick(60)
                pygame.quit()
                sys.exit()
        
    pygame.quit()

full = None
    
def introduction():
    root = tk.Tk()
    root.title("Instruction Window")
    
    if full:
        root.attributes('-fullscreen', True)

    frame = tk.Frame(root, bg=root.cget('bg'))
    frame.pack(expand=True, fill="both")

    pages = [
        "\n\n\n\n\n\n\n\nWelcome! This task is called the 2-Back.\n\n\n\nYou will be presented with a series of numbers.\n\n\n\nYou must decide if the current number is the same as the number seen two digits ago.",
        "\n\n\n\n\n\n\n\nAn example is as follows:\n\n7    4    7\n\n\n\nThis would be classed as a 2-Back since the third digit 7 is the same as that two digits ago\n\n\n\nIf the series was\n\n\n\n7    4    8\n\n\n\nThis would not be a 2-Back.",
        "\n\n\n\n\n\n\n\nIf you see a 2-Back, you must press 'J'.\n\n\n\nIf it is not a 2-Back, press 'F'.\n\n\n\nYou must respond on every trial.\n\nYou will have 20 practice trials for familiarisation.\n\nPress 'Next' when you are ready, then the task will begin."
    ]

    styles = [
        {
            "INSTRUCTIONS NEED REPOSITIONING!!": {"foreground": "red", "font": ("Arial", 24, "bold")},
            "2-Back": {"foreground": "red", "font": ("Arial", 24, "bold")}
        },
        {
            "INSTRUCTIONS NEED REPOSITIONING!!": {"foreground": "red", "font": ("Arial", 24, "bold")},
            "2-Back": {"foreground": "red", "font": ("Arial", 24, "bold")},
            "7": {"foreground": "blue", "font": ("Arial", 24, "bold")},
            "8": {"foreground": "blue", "font": ("Arial", 24, "bold")}
        },
        {
            "INSTRUCTIONS NEED REPOSITIONING!!": {"foreground": "red", "font": ("Arial", 24, "bold")},
            "2-Back": {"foreground": "red", "font": ("Arial", 24, "bold")},
            "J": {"foreground": "green", "font": ("Arial", 24, "bold")},
            "F": {"foreground": "green", "font": ("Arial", 24, "bold")}
        }
    ]

    current_page = 0

    text_widget = tk.Text(
        frame,
        font=("Arial", 24),
        wrap="word",
        bd=0,
        highlightthickness=0,
        bg=root.cget('bg')
    )
    text_widget.pack(expand=True, fill="both", padx=50)
    text_widget.tag_configure("center", justify="center")
    text_widget.configure(state="disabled")

    def show_page(page_index):
        text_widget.configure(state="normal")
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, pages[page_index], "center")
        for word, opts in styles[page_index].items():
            start_index = "1.0"
            
            while True:
                pos = text_widget.search(word, start_index, stopindex=tk.END)
                if not pos:
                    break
                
                end_pos = f"{pos}+{len(word)}c"
                text_widget.tag_add(word, pos, end_pos)
                text_widget.tag_config(word, **opts)
                start_index = end_pos
        text_widget.configure(state="disabled")

    def next_page():
        nonlocal current_page
        if current_page < len(pages) - 1:
            current_page += 1
            show_page(current_page)
        else:
            root.destroy()
            pygame.display.init()

    def prev_page():
        nonlocal current_page
        if current_page > 0:
            current_page -= 1
            show_page(current_page)

    nav_frame = tk.Frame(root, bg=root.cget('bg'))
    nav_frame.pack(side="bottom", fill="x", pady=20, padx=20)

    back_button = tk.Button(nav_frame, text="Back", command=prev_page, font=("Arial", 18))
    back_button.pack(side="left")

    next_button = tk.Button(nav_frame, text="Next", command=next_page, font=("Arial", 18))
    next_button.pack(side="right")

    root.bind("<Escape>", lambda e: root.destroy())

    show_page(current_page)
    root.mainloop()

if not Test:
    introduction()

task()
BAC()
