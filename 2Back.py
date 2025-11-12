# Copyright Ben Stocker, 2025
# See LICENSE.md for terms of use and restrictions.

import tkinter as tk
from tkinter import messagebox
import hashlib
from pathlib import Path

def check_password(event=None):
    global entered
    entered = entry.get()
    if len(entered) > 0:
        print(entered)
        root.destroy()
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
entry = tk.Entry(frame, show="*", font=("Arial", 14), justify="center")
entry.pack(pady=10)
entry.focus()

tk.Button(frame, text="Submit", command=check_password, bg="#4caf50", fg="white", font=("Arial", 12, "bold")).pack(pady=20)

root.bind("<Return>", check_password)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

import subprocess
import pygame, math
import sys, shutil, ctypes
from pygame.locals import *
import random, time
import os

os.chdir(os.path.dirname(__file__))

import csv
import time
import pandas as pd
from datetime import datetime
from scipy.stats import norm
import sqlite3
import numpy as np
import json
import threading
import os
from datetime import datetime

LOCAL_SAVE_PATH = f'Participant {entered}.csv'

def save_locally(participant_number, reactiontime, score):
    file_exists = os.path.isfile(LOCAL_SAVE_PATH)
    with open(LOCAL_SAVE_PATH, mode="a", newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["timestamp", "participant_number", "reaction_time", "score"])
        writer.writerow([datetime.now().isoformat(), participant_number, reactiontime, score])
    print("Saved locally")

def display_license():
        with open("LICENSE.txt", "r", encoding="utf-8") as f:
            license_text = f.read()
        print("\n=== LICENSE NOTICE ===")
        print(license_text)
        print("======================\n")
        time.sleep(5)

display_license()
learning = 12
noise_trials = learning

def installation():

    packages_to_install = ["pygame", "pandas", "pyxid2", "numpy"]

    for package in packages_to_install:
        try:
            subprocess.check_call(["pip", "install", package])
            print(f"Successfully installed {package}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {package}: {e}")

count_file = 'N-Back count.txt'

if os.path.exists(count_file):
    with open(count_file, 'r') as f:
        count = int(f.read())
else:
    count = 0

count += 1

with open(count_file, 'w') as f:
    f.write(str(count))

def login():
    global participant_number
    while True:
        participant_number = entered
        p2 = participant_number

        if p2 == participant_number:
            print("\nCorrect login")
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

now = datetime.now()

date_time_string = now.strftime("%d-%m-%y")
outputtime = now.strftime("%H:%M:%S")

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = (
    pygame.display.Info().current_w,
    pygame.display.Info().current_h,
)

WINDOW_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
pygame.display.set_caption("N-Back")

pygame.font.init()
FONT_SIZE = 240
font = pygame.font.SysFont('Arial', FONT_SIZE)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

KEY_MAPPING = {
    pygame.K_j: True,
    pygame.K_f: False
}

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
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=position)
    screen.blit(text_surface, text_rect)

global nb

nb = None

def introduction():

    skip = None
    pygame.font.init()

    os.environ["SDL_VIDEO_CENTERED"] = "1"

    font = pygame.font.Font(None, 32)

    order = 1

    start_time = pygame.time.get_ticks()

    Game_Running = True

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
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

    n = 2  
    sequence_length = 360

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
        if current_index < learningconv:
            screen.blit(incorrectinterval, incorrectintervaldimensions)
        pygame.time.wait(500)
        pygame.display.update()
        pygame.time.wait(500)
        
    def correct():
        correctanswer = True
        endRT = time.time()
        screen.fill(WHITE)
        if current_index < learningconv:
            screen.blit(correctinterval, correctintervaldimensions)
        pygame.time.wait(500)
        pygame.display.update()
        pygame.time.wait(500)
        score =+ 1
            
    global timer2
    
    timer2 = time.time()
    hits = 0
    false_alarms = 0
    stim = True

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
                                correct()
                                score += 1
                                hits += 1

                            elif event.key == pygame.K_f:
                                incorrect()
                                false_alarms += 1
               
                        else:
                            if event.key == pygame.K_j:
                                incorrect()
                                false_alarms += 1
                      
                            elif event.key == pygame.K_f:
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
                    with db_connection:
                        db_cursor.execute(
                            "INSERT INTO Scores (timestamp, participant_number, counter, score, task_type, NoResponse) VALUES (?, ?, ?, ?, ?, ?)",
                            (date_time_string, participant_number, count, "0", name, "No Response")
                        )
                        
                def emptyrtrecord():
                    with db_connection:
                        db_cursor.execute(
                            "INSERT INTO ReactionTimes (timestamp, participant_number, counter, reaction_time, task_type, NoResponse) VALUES (?, ?, ?, ?, ?, ?)",
                            (date_time_string, participant_number, count, "0", name, "No Response")
                        )

                def scorerecord():
                    with db_connection:
                        db_cursor.execute(
                            "INSERT INTO Scores (timestamp, participant_number, counter, score, task_type, key) VALUES (?, ?, ?, ?, ?, ?)",
                            (date_time_string, participant_number, count, score, name, key_name)


                            )
                def rtrecord():
                    with db_connection:
                        db_cursor.execute(
                            "INSERT INTO ReactionTimes (timestamp, participant_number, counter, reaction_time, task_type, key) VALUES (?, ?, ?, ?, ?, ?)",
                            (date_time_string, participant_number, count, reactiontime, name, key_name)
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

        if current_index == sequence_length/3:
            print('Block 1 finishes')
            
            for i in range(0,5):
                three_sec = [1,2,3]
                time.sleep(1)
                
                if i in three_sec:
                    print(f'{i} to go')
            
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

                print("Z-Hit:", z_hit)
                print("Z-False:", z_false_alarm)
                print("d' (Sensitivity):", d_prime)
                print("c (Response Bias):", c_prime)

                with db_connection:
                    db_cursor.execute(
                        "INSERT INTO SensitivityScores (Z_Hit, Z_False, Sensitivity, ResponseBias) VALUES (?, ?, ?, ?)",
                        (z_hit, z_false_alarm, d_prime, c_prime))
            else:
                print("No hits or false alarms to calculate d' and c.")
                d_prime = 0
                c_prime = 0    
        
    pygame.quit()     
    
introduction()
