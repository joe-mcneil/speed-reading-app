# Imports & Constants #
from tkinter import *
BACKGROUND_COLOR = "#FDF5E6"


# Window, Images & UI Setup #
window = Tk()
window.title("Speed Reader")
window.config(width=800, height=800, padx=10, pady=20, bg=BACKGROUND_COLOR)

start_pause_icon = PhotoImage(file="images/start.png")
faster_icon = PhotoImage(file="images/faster.png")
slower_icon = PhotoImage(file="images/slower.png")

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=2, column=2)
word_text = canvas.create_text(400, 263, text="Speed Reader", fill="black", font=("Arial", 38, "bold"))
speed_text = canvas.create_text(720, 480, text="300 WPM", fill="black", font=("Arial", 28, "bold"))


# Control Variables #
keep_reading = True
wpm = 300
word_count = 0
with open("text/text.txt") as file:
    text = file.read()
    word_list = text.split()


# Functions
def reading_speed(wpm):
    return int((60/wpm)*1000)

def new_word():
    global word_count
    global word_list
    if keep_reading:
        if word_count < len(word_list)-1:
            current_word = word_list[word_count]
            canvas.itemconfig(word_text, text=current_word)
            word_count += 1
        else:
            word_count = 0
    window.after(reading_speed(wpm), new_word)

def start_and_stop_reading():
    global keep_reading
    keep_reading = not keep_reading

def speed_up():
    global wpm
    if wpm < 900:
        wpm += 50
        canvas.itemconfig(speed_text, text=f"{wpm} WPM")

def slow_down():
    global wpm
    if wpm > 50:
        wpm -= 50
        canvas.itemconfig(speed_text, text=f"{wpm} WPM")


# Buttons
slower_button = Button(image=slower_icon, command=slow_down, highlightthickness=0)
slower_button.grid(column=1, row=4)
slower_button.config(padx=20)

start_and_pause_button = Button(image=start_pause_icon, command=start_and_stop_reading, highlightthickness=0)
start_and_pause_button.grid(column=2, row=4)
start_and_pause_button.config(padx=20)


faster_button = Button(image=faster_icon, command=speed_up, highlightthickness=0)
faster_button.grid(column=3, row=4)
faster_button.config(padx=20)

new_word()
window.mainloop()
