import tkinter as tk

# Function to update the expression when a button is pressed
def press(key):
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, current + str(key))

# Function to evaluate the expression
def evaluate():
    try:
        result = eval(entry.get())
        entry.delete(0, tk.END)
        entry.insert(0, result)
    except Exception as e:
        entry.delete(0, tk.END)
        entry.insert(0, "Error")

# Function to clear the entry field
def clear():
    entry.delete(0, tk.END)

# Setting up the main window
root = tk.Tk()
root.title("Calculator")
root.geometry("400x500")  # Set window size
root.resizable(False, False)  # Prevent window resizing

# Styling
entry_font = ("Helvetica", 20)
button_font = ("Helvetica", 16)
button_bg = "#f4f4f4"
button_fg = "#333"
button_active_bg = "#dcdcdc"
entry_bg = "#282828"
entry_fg = "#fff"

# Entry field for input/output
entry = tk.Entry(root, width=20, borderwidth=5, font=entry_font, bg=entry_bg, fg=entry_fg, justify="right")
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

# Buttons for digits and operations
buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3),
    ('C', 5, 0)
]

# Creating and placing the buttons
for (text, row, col) in buttons:
    if text == '=':
        button = tk.Button(root, text=text, width=5, height=2, font=button_font, bg=button_bg, fg=button_fg,
                           activebackground=button_active_bg, command=evaluate)
    elif text == 'C':
        button = tk.Button(root, text=text, width=5, height=2, font=button_font, bg="#ff6666", fg=button_fg,
                           activebackground=button_active_bg, command=clear)
    else:
        button = tk.Button(root, text=text, width=5, height=2, font=button_font, bg=button_bg, fg=button_fg,
                           activebackground=button_active_bg, command=lambda t=text: press(t))
    
    button.grid(row=row, column=col, padx=10, pady=10)

# Run the application
root.mainloop()
