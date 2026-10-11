###   Speed Reader v.0.3   ###
#TODO:
# 1. Get text displaying and cycling through with working buttons. ✔
# 2. Highlight the focal character and keep it consistently in the middle of the screen. ✔
# 3. Work out why Pride and Prejudice Ch.1 isn't reading properly. ✔
# 4. Pull text from epub_parser.py rather than text file. ✔
# 5. Implement book selection in reader UI at startup. (Will help with testing chapter selection.)
# 6. Write basic chapter selection for P&P, including a chaptered book dataclass that the parser sends to the reader.
# 7. Test on lots of different epub layouts.
# 8. Tweaks, feature upgrades* and bug fixes.

# * Feature Upgrade & Tweak List:
# Put focal point left of centre as research shows cultures who read left to right find that easier.
# Customisable colours and fonts.
# Adjustable window size and fullscreen option with coordinates of buttons/text adapted to fit.
# Individual chapter selection.

##  Imports  ##
from tkinter import *
from tkinter import font
from epub_parser import epub_to_words
from pathlib import Path


##  Config & Control Variables  ##
keep_reading = False
words_per_min = 300
word_count = 0
word_list = []
book_paths = sorted(Path("books").glob("*.epub"))


##  Functions  ##
def load_book(path):
    global word_list, word_count
    word_count = 0
    word_list = epub_to_words(path)
    print(word_count, path)
    return word_list

def book_chosen(path):
    load_book(path)
    bookshelf_frame.grid_remove()
    reader_frame.grid()

def reading_speed(wpm):
    return int((60/wpm)*1000)

def get_word():
    # Splitting this function out because eventually getting the words will be its own .py file.
    global word_list, word_count
    if word_count < len(word_list) - 1:
        current_word = word_list[word_count]
        word_count += 1
    else:
        current_word = word_list[word_count]
        word_count = 0
    return current_word

def new_word():
    if keep_reading:
        word = get_word()
        midpoint = (len(word) + 1) // 2
        word_start_text = word[:midpoint - 1]
        focal_letter_text = word[midpoint-1:midpoint]
        word_end_text = word[midpoint:]
        reader_canvas.itemconfig(word_start, text=word_start_text)
        reader_canvas.itemconfig(focal_letter, text=focal_letter_text)
        reader_canvas.itemconfig(word_end, text=word_end_text)
        reader_canvas.coords(word_start, 400 - f.measure(focal_letter_text) / 2, 263)
        reader_canvas.coords(word_end, 400 + f.measure(focal_letter_text) / 2, 263)
    window.after(reading_speed(words_per_min), new_word)

def start_and_stop_reading():
    global keep_reading
    keep_reading = not keep_reading

def speed_up():
    global words_per_min
    if words_per_min < 900:
        words_per_min += 50
        reader_canvas.itemconfig(speed_text, text=f"{words_per_min} WPM")

def slow_down():
    global words_per_min
    if words_per_min > 50:
        words_per_min -= 50
        reader_canvas.itemconfig(speed_text, text=f"{words_per_min} WPM")


## UI & Tkinter  ##
# Window
window = Tk()
window.title("Speed Reader")
BACKGROUND_COLOR = "#FDF5E6"
window.config(width=800, height=800, padx=10, pady=20, bg=BACKGROUND_COLOR)
f = font.Font(family="Helvetica", size=32, weight="bold")
# Icons
start_pause_icon = PhotoImage(file="images/start.png")
faster_icon = PhotoImage(file="images/faster.png")
slower_icon = PhotoImage(file="images/slower.png")

# Bookshelf Frame #
bookshelf_frame = Frame(window, bg=BACKGROUND_COLOR)
shelf_title = Label(bookshelf_frame, text= "Bookshelf", bg=BACKGROUND_COLOR, font=f)
shelf_title.grid(row=0, column=0, pady=(0, 20))
# Bookshelf Buttons
for row, path_name in enumerate(book_paths, start=1):
    book_button = Button(bookshelf_frame, text=path_name.stem, command=lambda p=path_name: book_chosen(p)) # Stops pathname freezing at last value.
    book_button.grid(row=row, column=0)

# Reader Frame #
reader_frame = Frame(window, bg=BACKGROUND_COLOR)
reader_canvas = Canvas(reader_frame, width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
reader_canvas.grid(row=2, column=2)
word_start = reader_canvas.create_text(400 - f.measure("d") / 2, 263, text="Spee", anchor="e", font=f, fill="black")
focal_letter = reader_canvas.create_text(400, 263, text="d", anchor='center', font=f, fill="red")
word_end = reader_canvas.create_text(400 + f.measure("d") / 2, 263, text=" Reader", anchor="w", font=f, fill="black")
speed_text = reader_canvas.create_text(720, 480, text="300 WPM", fill="black", font=("Arial", 28, "bold"))
# Reader Buttons
slower_button = Button(reader_frame, image=slower_icon, command=slow_down, highlightthickness=0)
slower_button.grid(column=1, row=4)
slower_button.config(padx=20)
# Eventually I want the icon for this to have play and pause separated by a dash, but encountered some sizing issues.
start_and_pause_button = Button(reader_frame, image=start_pause_icon, command=start_and_stop_reading, highlightthickness=0)
start_and_pause_button.grid(column=2, row=4)
start_and_pause_button.config(padx=20)
faster_button = Button(reader_frame, image=faster_icon, command=speed_up, highlightthickness=0)
faster_button.grid(column=3, row=4)
faster_button.config(padx=20)

## Window Logic ##
# Startup
bookshelf_frame.grid(row=0,column=0)
reader_frame.grid(row=0,column=0)
reader_frame.grid_remove()
# Mainloop
new_word()
window.mainloop()
