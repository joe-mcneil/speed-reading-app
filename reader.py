## Speed Reader v.0.2 ##
#TODO:
# 1. Get text displaying and cycling through with working buttons. ✔
# 2. Highlight the focal character and keep it consistently in the middle of the screen. ✔
# 3. Work out why Pride and Prejudice Ch.1 isn't reading properly.
# 4. (Big One) Write code for pulling text from epubs and chunking it into bitesize chunks.
# 5. Implement way of selecting epub to be read within UI of the reader.
# 6. Write some tests.
# 7. Tweaks, feature upgrades* and bufixes.

# * Feature Upgrade & Tweak List:
# Put focal point left of centre as cultures who read left to right find that easier.
# Customisable colours and fonts.
# Adjustable window size and fullscreen option with coordinates of buttons/text adapted to fit.

# Imports #
from tkinter import *
from tkinter import font

# Window, Images & UI Setup #
window = Tk()
window.title("Speed Reader")
BACKGROUND_COLOR = "#FDF5E6"
window.config(width=800, height=800, padx=10, pady=20, bg=BACKGROUND_COLOR)
f = font.Font(family="Helvetica", size=24, weight="bold")

start_pause_icon = PhotoImage(file="images/start.png")
faster_icon = PhotoImage(file="images/faster.png")
slower_icon = PhotoImage(file="images/slower.png")

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=2, column=2)
word_start = canvas.create_text(400,263,text="", anchor="e", font=f, fill="black")
focal_letter = canvas.create_text(400,263,text="", anchor='center', font=f, fill="red")
word_end = canvas.create_text(400,263,text="", anchor="w", font=f, fill="black")
speed_text = canvas.create_text(720, 480, text="300 WPM", fill="black", font=("Arial", 28, "bold"))

# Control Variables #
keep_reading = True
words_per_min = 300
word_count = 0
with open("text/text.txt") as file:
    text = file.read()
    word_list = text.split()


# Functions
def reading_speed(wpm):
    return int((60/wpm)*1000)

def get_word():
    # Splitting this function out because eventually getting the words will be its own .py file.
    global word_count
    global word_list
    if word_count < len(word_list) - 1:
        word_count += 1
    else:
        word_count = 0
    current_word = word_list[word_count]
    return current_word

def new_word():
    if keep_reading:
        word = get_word()
        midpoint = (len(word) + 1) // 2
        word_start_text = word[:midpoint - 1]
        focal_letter_text = word[midpoint-1:midpoint]
        word_end_text = word[midpoint:]
        canvas.itemconfig(word_start, text=word_start_text)
        canvas.itemconfig(focal_letter, text=focal_letter_text)
        canvas.itemconfig(word_end, text=word_end_text)
        canvas.coords(word_start, 400-f.measure(focal_letter_text)/2,263)
        canvas.coords(word_end, 400+f.measure(focal_letter_text)/2,263)
    window.after(reading_speed(words_per_min), new_word)

def start_and_stop_reading():
    global keep_reading
    keep_reading = not keep_reading

def speed_up():
    global words_per_min
    if words_per_min < 900:
        words_per_min += 50
        canvas.itemconfig(speed_text, text=f"{words_per_min} WPM")

def slow_down():
    global words_per_min
    if words_per_min > 50:
        words_per_min -= 50
        canvas.itemconfig(speed_text, text=f"{words_per_min} WPM")


# Buttons
slower_button = Button(image=slower_icon, command=slow_down, highlightthickness=0)
slower_button.grid(column=1, row=4)
slower_button.config(padx=20)

# Eventually I want the icon for this to have play and pause separated by a dash, but encountered some sizing issues.
start_and_pause_button = Button(image=start_pause_icon, command=start_and_stop_reading, highlightthickness=0)
start_and_pause_button.grid(column=2, row=4)
start_and_pause_button.config(padx=20)

faster_button = Button(image=faster_icon, command=speed_up, highlightthickness=0)
faster_button.grid(column=3, row=4)
faster_button.config(padx=20)

# Mainloop Logic
new_word()
window.mainloop()
