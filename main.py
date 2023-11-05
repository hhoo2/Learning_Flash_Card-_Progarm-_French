# Import the necessary libraries
from tkinter import *
import pandas
import random

# Define a constant for the background color
BACKGROUND_COLOR = "#B1DDC6"

# Initialize variables
current_card = {}  # Dictionary to store the current flashcard data
to_learn = []  # List of dictionaries to store words to learn

# Try to load data from a CSV file
try:
    data = pandas.read_csv("words_to_learn.csv")
except FileNotFoundError:
    # If "words_to_learn.csv" is not found, load data from "french_words.csv"
    original_data = pandas.read_csv("french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    # If "words_to_learn.csv" is found, populate the 'to_learn' list with its data
    to_learn = data.to_dict(orient="records")

# Function to display the next flashcard
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)  # Cancel the flip timer
    current_card = random.choice(to_learn)  # Select a random word from the 'to_learn' list
    canvas.itemconfig(card_title, text="French", fill="black")  # Set the card title to "French"
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")  # Display the French word
    canvas.itemconfig(card_background, image=card_front_img)  # Display the front of the flashcard
    flip_timer = window.after(3000, func=flip_card)  # Start a timer to automatically flip the card

# Function to flip the flashcard to show the English translation
def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")  # Set the card title to "English"
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")  # Display the English translation
    canvas.itemconfig(card_background, image=card_back_img)  # Display the back of the flashcard

# Function to mark a word as known
def is_known():
    to_learn.remove(current_card)  # Remove the current card from the 'to_learn' list
    data = pandas.DataFrame(to_learn)  # Create a DataFrame from the updated list
    data.to_csv("words_to_learn.csv", index=False)  # Write the updated data to "words_to_learn.csv"
    next_card()  # Display the next flashcard

# UI Setup
window = Tk()  # Create the main window
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)  # Set window properties

flip_timer = window.after(3000, func=flip_card)  # Start a timer to flip the card initially

# Create a canvas to display the flashcard and load image files
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="card_front.png")
card_back_img = PhotoImage(file="card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
canvas.grid(row=0, column=0, columnspan=2)  # Display the canvas

# Create text elements for card title and word
card_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="word", font=("Ariel", 60, "bold"))

# Create buttons for marking words as known or unknown
cross_image = PhotoImage(file="wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

check_image = PhotoImage(file="right.png")
known_button = Button(image=check_image, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

next_card()  # Display the first flashcard

# Start the application's main event loop
window.mainloop()
