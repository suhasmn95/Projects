import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import subprocess
import os
import webbrowser
import threading
import queue
import sys
import time
import datetime

# File to store the commands
COMMANDS_FILE = "commands.txt"
APPLICATION_NAME = "Command Line Executor"

# Queue to hold command output
output_queue = queue.Queue()

# Track running thread
thread_running = False
command_thread = None
execution_thread = None

QUEUED_COMMANDS_FILE = "queued_commands.txt"  # File to store queued commands

def update_command():
    selected_command = listbox_commands.curselection()
    if not selected_command:
        messagebox.showwarning("No Selection", "Please select a command to edit.")
        return
    
    # Get the selected command index and new command from the Entry widget
    selected_index = selected_command[0]
    new_command = command_entry.get()
    
    if new_command.strip():  # Ensure the command is not empty
        listbox_commands.delete(selected_index)  # Delete the old command
        listbox_commands.insert(selected_index, new_command)  # Insert the updated command
        command_entry.delete(0, tk.END)  # Clear the Entry widget after saving
        save_commands()
    else:
        messagebox.showwarning("Empty Command", "Command cannot be empty.")
        
# Function to handle when a command is selected for editing
def select_command(event):
    selected_command = listbox_commands.curselection()
    if selected_command:
        selected_index = selected_command[0]
        current_command = listbox_commands.get(selected_index)
        command_entry.delete(0, tk.END)  # Clear previous content in the entry
        command_entry.insert(0, current_command)  # Display selected command in entry

def NonIPython(command):
    """Execute a system command."""
    try:
        os.system(command)  # Run the command as a system command
    except Exception as e:
        print(f"An error occurred while executing the command: {e}")

def save_queued_commands():
    """Save the queued commands to a file."""
    with open(QUEUED_COMMANDS_FILE, "w") as file:
        for i in range(selected_commands_listbox.size()):
            file.write(selected_commands_listbox.get(i) + "\n")
            
def update_command_count():
    """Update the count of commands in the listboxes."""
    count_commands = listbox_commands.size()
    count_selected_commands = selected_commands_listbox.size()

    # Update the command count labels
    label_command_count.config(text=f"Commands Added: {count_commands}")
    label_selected_command_count.config(text=f"Queued Commands: {count_selected_commands}")

def ensure_commands_file():
    if not os.path.exists(COMMANDS_FILE):
        # Create the file with write permissions
        with open(COMMANDS_FILE, "w") as file:
            pass  # Just create the file, no content needed yet.


def load_commands():
    """Load commands from the file into the listbox."""
    if os.path.exists(COMMANDS_FILE):
        with open(COMMANDS_FILE, "r") as file:
            commands = file.readlines()
            for command in commands:
                command = command.strip()
                listbox_commands.insert(tk.END, command)

def save_commands():
    """Save all commands in the listbox to the file."""
    with open(COMMANDS_FILE, "w") as file:
        for i in range(listbox_commands.size()):
            file.write(listbox_commands.get(i) + "\n")

def add_command():
    """Add a new command to the Available Commands listbox."""
    command = entry_command.get()
    if command:
        # Add the command to Available Commands listbox (listbox_commands)
        listbox_commands.insert(tk.END, command)
        entry_command.delete(0, tk.END)  # Clear the input field
        save_commands()  # Save Available Commands
        update_command_count()  # Update counts
    else:
        messagebox.showwarning("Input Error", "Please enter a command to add.")

def delete_command():
    """Delete the selected command from the listbox and save changes."""
    selected_indices = listbox_commands.curselection()
    if selected_indices:
        for index in reversed(selected_indices):
            listbox_commands.delete(index)
        save_commands()
        update_command_count()  # Update command counts after deleting
    else:
        messagebox.showwarning("Selection Error", "Please select a command to delete.")

def select_commands():
    """Add selected commands from Available Commands to the Queued Commands listbox."""
    selected_indices = listbox_commands.curselection()
    if selected_indices:
        for index in selected_indices:
            command = listbox_commands.get(index)
            selected_commands_listbox.insert(tk.END, command)  # Add to Queued Commands
        update_command_count()  # Update counts after adding
        save_queued_commands()  # Save Queued Commands
    else:
        messagebox.showwarning("Selection Error", "Please select at least one command.")



def move_up():
    """Move the selected command up in the order."""
    selected_index = selected_commands_listbox.curselection()
    if selected_index and selected_index[0] > 0:
        index = selected_index[0]
        command = selected_commands_listbox.get(index)
        selected_commands_listbox.delete(index)
        selected_commands_listbox.insert(index - 1, command)
        selected_commands_listbox.selection_set(index - 1)
        update_command_count()  # Update command counts after moving
    else:
        messagebox.showwarning("Move Error", "Cannot move the selected command up.")

def move_down():
    """Move the selected command down in the order."""
    selected_index = selected_commands_listbox.curselection()
    if selected_index and selected_index[0] < selected_commands_listbox.size() - 1:
        index = selected_index[0]
        command = selected_commands_listbox.get(index)
        selected_commands_listbox.delete(index)
        selected_commands_listbox.insert(index + 1, command)
        selected_commands_listbox.selection_set(index + 1)
        update_command_count()  # Update command counts after moving
    else:
        messagebox.showwarning("Move Error", "Cannot move the selected command down.")
        
        
def process_output_queue():
    """Process output from the queue and update the output_text widget."""
    while not output_queue.empty():
        message = output_queue.get()
        output_text.insert(tk.END, message)
        output_text.see(tk.END)  # Scroll to the latest message
    root.after(100, process_output_queue)  # Check queue every 100ms
    
def on_minimize(event):
    """Handle minimize event."""
    # Application can continue running when minimized
    pass

def on_closing():
    """Handle application close event."""
    global thread_running
    if thread_running:
        thread_running = False
        update_indicator()
        messagebox.showinfo("Info", "Stopping ongoing execution. Please wait...")
    root.destroy()
    sys.exit()  # Ensure the application exits completely
        
def remove_command():
    """Remove the selected command from the selected commands listbox."""
    selected_indices = selected_commands_listbox.curselection()
    if selected_indices:
        for index in reversed(selected_indices):
            selected_commands_listbox.delete(index)
        update_command_count()  # Update command counts after removing selected commands
        save_queued_commands()
    else:
        messagebox.showwarning("Selection Error", "Please select a command to remove.")


# Function to get the current position of the main window
def get_window_position(window):
    """Get the position of the window on the screen."""
    x = window.winfo_rootx()
    y = window.winfo_rooty()
    return x, y

# Create a simple About window
def show_about():
    """Create an About window with detailed information about the app and developer."""
    about_window = tk.Toplevel(root)
    about_window.title("About")
    about_window.geometry("800x600")  # Adjust size as needed
    about_window.config(bg="#f4f4f4")
    
    # Position the about window near the main window
    x, y = get_window_position(root)
    about_window.geometry(f"+{x + 50}+{y + 50}")
    
    # About text with application features and developer details
    about_text = (
        "About Command Line Executor (CLE)\n\n"
        "CLE is a powerful tool designed to make running multiple command-line tasks easier and more efficient.\n"
        "With CLE, users can:\n\n"
        "1. **Add Commands**: Easily add any shell or command-line command to the system.\n"
        "2. **Manage Commands**: Edit, delete, or organize commands in a list for future execution.\n"
        "3. **Queue Commands**: Select and queue commands in a specific order to be executed sequentially.\n"
        "4. **Repeat Commands**: Repeat any command multiple times with a specified count.\n"
        "5. **Execute Commands**: Run queued commands sequentially with real-time output and progress updates.\n"
        "6. **Monitor Execution**: A visual indicator shows whether commands are currently executing.\n"
        "7. **Stop Execution**: Stop the execution of commands at any time during the process.\n"
        "8. **Import/Export Commands**: Save and load commands from external files.\n"
        
        "This application was built with ease of use and functionality in mind to help users manage and automate command-line tasks.\n\n"
        
        "Developer Information:\n\n"
        "Developer Name: Suhas Nayak\n\n"
        
        "CLE is for anyone who wishes to simplify their command-line task management.\n"
        "Feel free to provide feedback, suggestions, or report issues on feedback form to help improve the application."
    )
    about_text_widget = tk.Text(about_window, wrap="word", font=("Arial", 8), bg="#f4f4f4", fg="black", borderwidth=0)
    about_text_widget.insert(tk.END, about_text)
    about_text_widget.config(state="disabled")  # Make the text read-only
    about_text_widget.pack(expand=True, fill="both", padx=10, pady=10)

# Create a simple Help window
def show_help():
    """Create a Help window with detailed steps to use the application."""
    help_window = tk.Toplevel(root)
    help_window.title("Instructions")
    help_window.geometry("700x800")  # Adjust size as needed
    help_window.config(bg="#f4f4f4")
    
    # Position the help window near the main window
    x, y = get_window_position(root)
    help_window.geometry(f"+{x + 50}+{y + 50}")
    
    # Add detailed instructions
    help_text = (
        "How to Use the Command Line Executor (CLE):\n\n"
        "1. **Add Commands**:\n"
        "   - Enter a command in the 'Add Commands' section (left column).\n"
        "   - Click the 'Add Command' button to save it.\n"
        "   - The command will appear in the 'Available Commands' list.\n\n"
        "2. **Manage Commands**:\n"
        "   - Use the following buttons below the 'Available Commands' list:\n"
        "     - **Edit Command**: Modify the selected command.\n"
        "     - **Delete Command**: Remove the selected command(s).\n"
        "     - **Queue Command**: Add selected commands to the execution queue.\n\n"
        "3. **Queue Commands**:\n"
        "   - View your queued commands in the 'Queued Commands' section (middle right column).\n"
        "   - Use these buttons to organize your queue:\n"
        "     - **Move Up/Down**: Change the order of commands.\n"
        "     - **Repeat Command**: Repeat a selected command multiple times.\n"
        "     - **Remove Command**: Remove commands from the queue.\n\n"
        "4. **Execute Commands**:\n"
        "   - Click the 'Execute Commands' button in the 'Queued Commands' section.\n"
        "   - The commands will run sequentially, and progress will be shown in the 'Execution Output' section.\n"
        "   - Use the 'Stop Execution' button to halt the process.\n\n"
        "5. **Monitor Execution**:\n"
        "   - The round indicator above the 'Execution Output' title shows:\n"
        "     - **Green**: No command is executing.\n"
        "     - **Red**: Commands are currently executing.\n\n"
        "6. **Import/Export Commands**:\n"
        "   - Use the 'Export Commands' button to save all commands to a file.\n"
        "   - Use the 'Import Commands' button to load commands from a file.\n\n"
        "For feedback or support, click the 'Feedback' option in the menu bar."
    )
    
    text_widget = tk.Text(help_window, wrap="word", font=("Arial", 8), bg="#f4f4f4", fg="black", borderwidth=0)
    text_widget.insert(tk.END, help_text)
    text_widget.config(state="disabled")  # Make the text read-only
    text_widget.pack(expand=True, fill="both", padx=10, pady=10)

def show_api_commands():
    """Create a window with details about the available API/commands."""
    api_window = tk.Toplevel(root)
    api_window.title("API/Commands")
    api_window.geometry("600x400")
    api_window.config(bg="#f4f4f4")
    
    # Position the window near the main window
    x, y = get_window_position(root)
    api_window.geometry(f"+{x + 50}+{y + 50}")
    
    # Information about available commands
    api_text = (
        "Inbuilt Commands in CLE (Command Line Executor):\n\n"
        
        "1. **NonIPython(command)**:\n"
        "   - Usage: `NonIPython('command')`\n"
        "   - Description: Executes a system command without using interative Python syntax.\n"
        "   - Example: `NonIPython('ls')` will execute the non interactive command in the system shell.\n\n"
        
        "2. **DELAY seconds**:\n"
        "   - Usage: `DELAY 2s` (where '2s' is the number of seconds to wait)\n"
        "   - Description: Introduces a delay in command execution. The argument should be a number followed by 's'.\n"
        "   - Example: `DELAY 5s` will pause the execution for 5 seconds before moving to the next command.\n\n"
        
        "3. **Other Commands**:\n"
        "   - All regular system commands can be used (e.g., 'ls', 'dir', 'mkdir', etc.) directly.\n\n"
        
        "For any questions or help, please refer to the documentation or contact support."
    )
    
    # Create a text widget to display the API information
    api_text_widget = tk.Text(api_window, wrap="word", font=("Arial", 8), bg="#f4f4f4", fg="black", borderwidth=0)
    api_text_widget.insert(tk.END, api_text)
    api_text_widget.config(state="disabled")  # Make the text read-only
    api_text_widget.pack(expand=True, fill="both", padx=10, pady=10)

# Create a simple Feedback window
def show_feedback():
    feedback_window = tk.Toplevel(root)
    feedback_window.title("Feedback")
    feedback_window.geometry("400x300")
    feedback_window.config(bg="#f4f4f4")
    
    # Position the feedback window near the main window
    x, y = get_window_position(root)
    feedback_window.geometry(f"+{x + 50}+{y + 50}")
    
    feedback_label = tk.Label(feedback_window, text="We would love your feedback!", font=("Arial", 10), bg="#f4f4f4")
    feedback_label.pack(pady=20)
    
    # Create a button that opens the Google Feedback Form
    google_form_url = "https://forms.gle/AwYsK7RHQ5y55XocA"  # Replace with your Google Form URL
    submit_button = tk.Button(feedback_window, text="Open Feedback Form", command=lambda: webbrowser.open(google_form_url), **button_style)
    submit_button.pack(pady=10)
    submit_button.bind("<Enter>", lambda event, btn=submit_button: on_enter(event, btn))
    submit_button.bind("<Leave>", lambda event, btn=submit_button: on_leave(event, btn))
    
def on_enter(event, button, hover_color="lightblue"):
    """Change button color when mouse enters."""
    button.config(bg=hover_color)

def on_leave(event, button, default_color="black"):
    """Revert button color when mouse leaves."""
    button.config(bg=default_color)
    
def export_commands():
    """Export commands to a user-specified file."""
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        title="Export Commands"
    )
    if file_path:
        try:
            with open(file_path, "w") as file:
                for i in range(listbox_commands.size()):
                    file.write(listbox_commands.get(i) + "\n")
            messagebox.showinfo("Export Successful", f"Commands exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Export Error", f"An error occurred: {e}")

def import_commands():
    """Import commands from a user-specified file."""
    file_path = filedialog.askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        title="Import Commands"
    )
    if file_path:
        try:
            with open(file_path, "r") as file:
                commands = file.readlines()
            for command in commands:
                command = command.strip()
                if command:  # Add command to the list if it is not empty
                    listbox_commands.insert(tk.END, command)
            save_commands()  # Save changes to the default commands file
            messagebox.showinfo("Import Successful", f"Commands imported from {file_path}")
            update_command_count()
        except Exception as e:
            messagebox.showerror("Import Error", f"An error occurred: {e}")

def repeat_command(listbox, entry):
    """Repeat the selected command a specified number of times, sequentially."""
    selected_index = listbox.curselection()
    if selected_index:
        try:
            repeat_count = int(entry.get())
            if repeat_count <= 0:
                raise ValueError("Repeat count must be positive and more than once.")
            
            index = selected_index[0]
            command = listbox.get(index)
            
            # Insert the repeated commands sequentially
            for _ in range(repeat_count):
                listbox.insert(index, command)
            
            # Update the command count
            update_command_count()
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid repeat count: {e}")
    else:
        messagebox.showwarning("Selection Error", "Please select a command to repeat.")

def stop_execution():
    """Stop the currently running commands."""
    global thread_running
    if thread_running:
        thread_running = False
        update_indicator()
        messagebox.showinfo("Info", "Command execution will stop after the current command.")
        if command_thread is not None:
            command_thread.join()  # Wait for the current command to finish gracefully
    else:
        messagebox.showwarning("Stop Error", "No command is currently executing.")
        
def update_indicator():
    """Update the indicator color based on the thread_running state."""
    if thread_running:
        indicator_canvas.itemconfig(indicator_circle, fill="red")
    else:
        indicator_canvas.itemconfig(indicator_circle, fill="green")
    #root.after(100, update_indicator)  # Recheck every 100ms
    
def add_delay(listbox, entry):
    """Add a delay (in seconds) immediately after the selected command."""
    selected_index = listbox.curselection()
    if selected_index:
        try:
            delay = float(entry.get())
            if delay <= 0:
                raise ValueError("Delay must be positive.")
            
            index = selected_index[0]
            listbox.insert(index + 1, f"DELAY {delay}s")  # Insert delay after selected command
            update_command_count()  # Update counts
            save_queued_commands()  # Save changes
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid delay value: {e}")
    else:
        messagebox.showwarning("Selection Error", "Please select a command to add a delay after.")


def export_queued_commands():
    """Export queued commands to a user-specified file."""
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        title="Export Queued Commands"
    )
    if file_path:
        try:
            with open(file_path, "w") as file:
                for i in range(selected_commands_listbox.size()):
                    file.write(selected_commands_listbox.get(i) + "\n")
            messagebox.showinfo("Export Successful", f"Queued commands exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Export Error", f"An error occurred: {e}")

def load_queued_commands():
    """Load queued commands from a file."""
    if os.path.exists(QUEUED_COMMANDS_FILE):
        with open(QUEUED_COMMANDS_FILE, "r") as file:
            for command in file:
                command = command.strip()
                if command:  # Add only non-empty lines
                    selected_commands_listbox.insert(tk.END, command)
        update_command_count()  # Update counts

################ Testing field:start

def run_commands_in_background(commands):
    """Run commands in the background, redirecting to the Python interpreter if started."""
    global thread_running
    thread_running = True
    update_indicator()

    python_process = None  # Track if Python interpreter is running
    progress_bar["maximum"] = len(commands)
    progress_bar["value"] = 0

    for index, command in enumerate(commands, start=1):
        if not thread_running:
            if python_process:
                python_process.stdin.write("exit()\n")
                python_process.stdin.close()
                #append_output("Exiting Python interpreter...\n")
                python_process.wait()
                python_process = None
            break  # Stop execution if the thread_running flag is unset

        command = command.strip()

        # Start Python interpreter
        if command == "python" and python_process is None:
            python_process = subprocess.Popen(
                "python", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            append_output("Python interpreter started. Redirecting commands...\n")
            continue

        # Handle exit() from Python interpreter
        if command == "exit()" and python_process:
            python_process.stdin.write("exit()\n")
            python_process.stdin.close()
            for line in python_process.stdout:
                append_output(line)
            for line in python_process.stderr:
                append_output(line, is_error=True)
            append_output("Exiting Python interpreter...\n")
            python_process.wait()
            python_process = None  # Reset to indicate the interpreter is no longer running
            continue
        
        # Commands within Python interpreter
        if python_process:
            try:
                if command.lower().startswith("delay"):
                    # Implement delay within interpreter
                    delay_time = float(command.split()[1].replace("s", ""))
                    python_process.stdin.write(f"print(f\'Delayed for {delay_time} seconds in Python interpreter...\')\n")
                    python_process.stdin.write(f"import time\ntime.sleep({delay_time})\nimport sys\nsys.stdout.flush()\n")
                    python_process.stdin.flush()
                    
                elif command.startswith("NonIPython("):
                    # Handle NonIPython commands in interpreter
                    argument = command[11:-1]  # Extract the argument
                    python_process.stdin.write(f"print('Executed NonIPython('{argument}') in Python interpreter...\')\n")
                    python_process.stdin.write(f"import os\nos.system('{argument}')\nimport sys\nsys.stdout.flush()\n")
                    python_process.stdin.flush()
                    #append_output(f"Executing NonIPython('{argument}') in Python interpreter...\n")
                else:
                    # Send other commands to the interpreter
                    python_process.stdin.write(f"print('Executed in Python: {command}\')\n")
                    python_process.stdin.write(command + "\n")
                    python_process.stdin.write(f"import sys\nsys.stdout.flush()\n")  # Explicit flush
                    python_process.stdin.flush()
                    #append_output(f"Executing in Python: {command}\n")

            except Exception as e:
                append_output(f"Error executing command in Python interpreter: {e}\n", is_error=True)
            continue  # Ensure commands handled here are not processed again outside this block
        
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        # Standalone delay command
        if command.lower().startswith("delay"):
            try:
                delay_time = float(command.split()[1].replace("s", ""))
                append_output(f"@{timestamp} : Delaying for {delay_time} seconds...\n")
                time.sleep(delay_time)
            except Exception as e:
                append_output(f"@{timestamp} : Error processing delay: {e}\n", is_error=True)
            continue

        # NonIPython command outside interpreter
        if command.startswith("NonIPython("):
            try:
                argument = command[11:-1]  # Remove "NonIPython(" and ")"
                append_output(f"@{timestamp} : Running NonIPython API outside IPython no outputs to be expected in GUI\n")
                NonIPython(argument)
            except Exception as e:
                append_output(f"@{timestamp} : Error executing NonIPython: {e}\n", is_error=True)
            continue

        # Standard commands outside interpreter
        try:
            append_output(f"@{timestamp} : Executed in outside IPython: {command}\n")
            process = subprocess.Popen(
                command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            for line in process.stdout:
                append_output(line)
            for line in process.stderr:
                append_output(line, is_error=True)
        except Exception as e:
            append_output(f"@{timestamp} : Error executing command: {e}\n", is_error=True)

        progress_bar["value"] = index
        root.update_idletasks()

    thread_running = False
    update_indicator()
    progress_bar["value"] = 0
    root.update_idletasks()


################ Testing field:stop


def append_output(line, is_error=False):
    """Appends a line of output to the output widget."""
    output_widget.insert(tk.END, line, "error" if is_error else "stdout")
    output_widget.see(tk.END)  # Scroll to the end

def RunButton():
    
    global command_thread
    
    # Get selected commands from the Listbox
    commands = selected_commands_listbox.get(0, tk.END)
    
    # Clear the output widget before running new commands
    output_widget.delete("1.0", tk.END)

    # Run commands in a background thread
    command_thread = threading.Thread(target=run_commands_in_background, args=(commands,))
    command_thread.start()

def save_log():
    """Saves the log to a file."""
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if file_path:
        try:
            with open(file_path, "w") as file:
                file.write(output_widget.get("1.0", tk.END))
            messagebox.showinfo("Save Log", f"Log saved successfully to {file_path}")
        except Exception as e:
            messagebox.showerror("Save Log", f"Error saving log: {e}")

def clear_log():
    """Clears the output widget."""
    output_widget.delete("1.0", tk.END)

# Main window setup
root = tk.Tk()
root.title(APPLICATION_NAME)
root.geometry("1250x700")
root.configure(bg="#f4f4f4")

# Add the "CLE" logo in bold
logo_label = tk.Label(root, text="CLE", font=("Arial", 20, "bold"), fg="#0078D4", bg="#f4f4f4")
logo_label.grid(row=0, column=0, columnspan=4, pady=20)

# Make the window resizable
root.grid_columnconfigure(0, weight=1, minsize=200)
root.grid_columnconfigure(1, weight=1, minsize=200)
root.grid_columnconfigure(2, weight=1, minsize=200)
root.grid_columnconfigure(3, weight=1, minsize=500)
root.grid_rowconfigure(1, weight=1)

# Create frames for the four-column layout
frame_left = tk.Frame(root, bg="#f4f4f4")
frame_left.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

frame_mid1 = tk.Frame(root, bg="#f4f4f4")
frame_mid1.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

frame_mid2 = tk.Frame(root, bg="#f4f4f4")
frame_mid2.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)

frame_right = tk.Frame(root, bg="#f4f4f4")
frame_right.grid(row=1, column=3, sticky="nsew", padx=10, pady=10)

# Button style
button_style = {
    "fg": "white", "font": ("Arial", 8, "bold"),  # Smaller font size
    "relief": "flat", "width": 18, "height": 1,  # Smaller width and height
    "bg": "black"
}

# First column (Command List)
heading_add_command = tk.Label(frame_left, text="Add Commands", font=("Arial", 10, "bold"), bg="#f4f4f4")
heading_add_command.grid(row=0, column=0, pady=10)

entry_command = ttk.Entry(frame_left, width=40)
entry_command.grid(row=1, column=0, pady=10)

button_add = tk.Button(frame_left, text="Add Command", command=add_command, **button_style)
button_add.grid(row=2, column=0, pady=5)
button_add.bind("<Enter>", lambda event, btn=button_add: on_enter(event, btn))
button_add.bind("<Leave>", lambda event, btn=button_add: on_leave(event, btn))

# Second column (Selected Command List)
heading_command_list = tk.Label(frame_mid1, text="Available Commands", font=("Arial", 10, "bold"), bg="#f4f4f4")
heading_command_list.grid(row=0, column=0, pady=10)

listbox_commands = tk.Listbox(frame_mid1, width=40, height=10, selectmode=tk.EXTENDED)
listbox_commands.grid(row=1, column=0, pady=10)

command_entry = tk.Entry(frame_mid1, width=50)
command_entry.grid(row=2, column=0, padx=10, pady=10)###

done_button = tk.Button(frame_mid1, text="Done Edit", command=update_command)
done_button.grid(row=3, column=0, padx=10, pady=10)

button_delete = tk.Button(frame_mid1, text="Delete Command", command=delete_command, **button_style)
button_delete.grid(row=4, column=0, pady=5)
button_delete.bind("<Enter>", lambda event, btn=button_delete: on_enter(event, btn))
button_delete.bind("<Leave>", lambda event, btn=button_delete: on_leave(event, btn))

button_select = tk.Button(frame_mid1, text="Queue Command", command=select_commands, **button_style)
button_select.grid(row=5, column=0, pady=5)
button_select.bind("<Enter>", lambda event, btn=button_select: on_enter(event, btn))
button_select.bind("<Leave>", lambda event, btn=button_select: on_leave(event, btn))

label_command_count = tk.Label(frame_mid1, text="Commands Added: 0", font=("Arial", 8), bg="#f4f4f4")
label_command_count.grid(row=6, column=0, pady=5)

# Third column

#selection method
heading_queued_commands = tk.Label(frame_mid2, text="Queued Commands", font=("Arial", 10, "bold"), bg="#f4f4f4")
heading_queued_commands.grid(row=0, column=0, pady=10)

selected_commands_listbox = tk.Listbox(frame_mid2, width=40, height=10, selectmode=tk.EXTENDED)
selected_commands_listbox.grid(row=1, column=0, pady=10)

repeat_label = tk.Label(frame_mid2, text="Repeat Count:", font=("Arial", 8), bg="#f4f4f4")
repeat_label.grid(row=2, column=0, pady=5)

repeat_entry = ttk.Entry(frame_mid2, width=10)
repeat_entry.grid(row=3, column=0, pady=5)

button_repeat = tk.Button(frame_mid2, text="Repeat Command", command=lambda: repeat_command(selected_commands_listbox, repeat_entry), **button_style)
button_repeat.grid(row=4, column=0, pady=5)
button_repeat.bind("<Enter>", lambda event, btn=button_repeat: on_enter(event, btn))
button_repeat.bind("<Leave>", lambda event, btn=button_repeat: on_leave(event, btn))

# Label for delay input
label_delay = tk.Label(frame_mid2, text="Add Delay (seconds):", font=("Arial", 8), bg="#f4f4f4")
label_delay.grid(row=5, column=0, pady=5)

# Entry for delay input
entry_delay = ttk.Entry(frame_mid2, width=10)
entry_delay.grid(row=6, column=0, pady=5)

# Button to add delay
button_add_delay = tk.Button(frame_mid2, text="Add Delay", command=lambda: add_delay(selected_commands_listbox, entry_delay), **button_style)
button_add_delay.grid(row=7, column=0, pady=5)
button_add_delay.bind("<Enter>", lambda event, btn=button_add_delay: on_enter(event, btn))
button_add_delay.bind("<Leave>", lambda event, btn=button_add_delay: on_leave(event, btn))


# Move Up button
button_move_up = tk.Button(frame_mid2, text="Move Up", command=move_up, **button_style)
button_move_up.grid(row=8, column=0, pady=5)
button_move_up.bind("<Enter>", lambda event, btn=button_move_up: on_enter(event, btn))
button_move_up.bind("<Leave>", lambda event, btn=button_move_up: on_leave(event, btn))

# Move Down button
button_move_down = tk.Button(frame_mid2, text="Move Down", command=move_down, **button_style)
button_move_down.grid(row=9, column=0, pady=5)
button_move_down.bind("<Enter>", lambda event, btn=button_move_down: on_enter(event, btn))
button_move_down.bind("<Leave>", lambda event, btn=button_move_down: on_leave(event, btn))

# Remove Command button
button_remove = tk.Button(frame_mid2, text="Remove Command", command=remove_command, **button_style)
button_remove.grid(row=10, column=0, pady=5)
button_remove.bind("<Enter>", lambda event, btn=button_remove: on_enter(event, btn))
button_remove.bind("<Leave>", lambda event, btn=button_remove: on_leave(event, btn))

"""
# Execute Commands button
button_execute = tk.Button(frame_mid2, text="Execute Commands", command=execute_commands, **button_style)
button_execute.grid(row=11, column=0, pady=5)
button_execute.bind("<Enter>", lambda event, btn=button_execute: on_enter(event, btn))
button_execute.bind("<Leave>", lambda event, btn=button_execute: on_leave(event, btn))
"""

button_run = tk.Button(frame_mid2, text="Run Commands", command=RunButton)
button_run.grid(row=11, column=0, pady=10)

label_selected_command_count = tk.Label(frame_mid2, text="Queued Commands: 0", font=("Arial", 8), bg="#f4f4f4")
label_selected_command_count.grid(row=12, column=0, pady=5)

# Fourth Column (Output Section)
frame_output_header = tk.Frame(frame_right, bg="#f4f4f4")
frame_output_header.grid(row=0, column=0, pady=(10, 0), sticky="ew")

indicator_canvas = tk.Canvas(frame_output_header, width=20, height=20, bg="#f4f4f4", highlightthickness=0)
indicator_canvas.pack(side="left", padx=5)

indicator_circle = indicator_canvas.create_oval(2, 2, 18, 18, fill="green")

# Add the "Execution Output" title next to the indicator
heading_output = tk.Label(frame_output_header, text="Execution Output", font=("Arial", 10, "bold"), bg="#f4f4f4")
heading_output.pack(side="left", padx=10)

save_icon_data = "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAAsTAAALEwEAmpwYAAADfElEQVR4nO2W224bVRSG8xagSsRt4qRJ0xzMHQ/CsSriBXgDJIRQhYAbbqGlomlC0hzsxE6btiS0SFUF9IISxxlPbM/JM+PZc/IhJiQo0o/29jjpNhfeipUrsqRf9t33rbXX3nZf33mdV0e9uRneSmyER4mNKoYWHcRmbPT/oKPeaKKx10Sj0US9vodqrQE/rMH1QjjEh1UhMMwKVN1EUTGQL6j4MCNjdIWYI2nnrT7RSkTwxE8hJ0CB7YTVOoKwBs8P4bg+bMfFB7ef4v3bT3Ej8wKFkg6poLQEVl2Mpkh9JCkokYjgUx0CflCFH9TYpxdUW527PiqOB9MmeO2TZZZ3b/0MuahhRy7hOpuAixGapCMmkYjgU495AeIGIF4UN2Bjp51TOB39qwL5goJcvojr6XwLniK4TJN0yl0FpiL45CNegMJsx4visjM3bYfBNcM6Fnjn5ibrPivt4hoVOIYTDC8TdBd43IJPPgowtHAiULYcmFHodwrWyzZUw0JJKx8LvH1zE9tSAX/mZFxb2eHgw8tOd4HJCD75MEC8LXBHR0m3oJXtVgyLbbuilVFUDbZ0tHMK/zT5HFs5GX9kJbyX2uHgw0tCAgGDT1CBJcIEYndNfPNMxa5aZt2WVINdNQqmC0fPnI6ddt6Gr/66g8RckYMPCQk8bMEn1gOM3fcQXySI33MwOGdiYEbHwF3tJNMaLv0nKsvgrM6gr8LpTnUVmIjg4+s+xh/4uHo/ypqHMZqMhys0aa91x2naV61j4Trh8cWKgMD62cHjCwIC42cIH7wnIvDg7OBCAlc74B//XkPa+AtrehMZbQ9ptYFVpY5ksYrl3RBLcoDFvI8FycN8zsFctoLZLRvTLy18tGFz8MF5UYG1k87rf/+Dw8NDHBwcYH9/H80m/UVsoFarIQxDBEEAz/NACEGlUoFlWTBNE4ZhQFJ0Dj4wbwsIrPFjPy1c0zQoisLBB+YEBMY6zrwXeKlU4uCXfhQRyPAL1wu8UChwcCGBKx3b3gtclmUOfnHWEhBI81etF7gkSRxcSGC04573As/lchz84oygwBtfv0D/l8/ZI9MLfHt7m4Ffv/EbLnz+DDEhgRVyROGxL35hL5zrnx7+civLBCj8wmdPEJsuH3UVuJwi342knKP28/p9lv4VOx38qycyGzvtnML775jfdhU4r/9d/QsEcQiOeKRKDwAAAABJRU5ErkJggg=="
save_icon = tk.PhotoImage(data=save_icon_data)

save_button = tk.Button(frame_output_header, image=save_icon, command=save_log, bg="#f4f4f4", relief="flat")
save_button.pack(side="right", padx=1)

clear_icon = tk.PhotoImage(data="iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAAsTAAALEwEAmpwYAAAAgUlEQVR4nO2USw6AIAwFeyefd/CInE12XETThRsXlk+JPmQSEghtM6QNIpPJDYR49FxCIyDOVAnA2Je8mlPAE74hxNsC4swUwO9bkA1GE0BpPTALwONTArNATr5ZH6MJwDh/VwCVA8Uv0ErzENILLGFPVrs0ppvAGuL2JKF3GnMlnLGuDjbPwA4gAAAAAElFTkSuQmCC")

clear_button = tk.Button(frame_output_header, image=clear_icon, command=clear_log, bg="#f4f4f4", relief="flat")
clear_button.pack(side="right", padx=1)

output_widget = scrolledtext.ScrolledText(frame_right, width=40, height=10, wrap=tk.WORD)
output_widget.grid(row=1, column=0, pady=10)

# Tags for output styles
output_widget.tag_config("stdout", foreground="black")
output_widget.tag_config("error", foreground="red")

"""
# Place the output text widget below the header
output_text = tk.Text(frame_right, width=40, height=10, wrap="word", font=("Arial", 12), bg="white", fg="black")
output_text.grid(row=1, column=0, pady=10)
# Clear the output text on initialization
output_text.delete("1.0", tk.END)
"""
progress_bar = ttk.Progressbar(frame_right, orient="horizontal", length=300, mode="determinate")
progress_bar.grid(row=2, column=0, pady=10)  # Place the progress bar below the output text
progress_bar["value"] = 0

# Add a "Stop Execution" button
button_stop_execution = tk.Button(frame_right, text="Stop Execution", command=stop_execution, **button_style)
button_stop_execution.grid(row=3, column=0, pady=10)
button_stop_execution.bind("<Enter>", lambda event, btn=button_stop_execution: on_enter(event, btn))
button_stop_execution.bind("<Leave>", lambda event, btn=button_stop_execution: on_leave(event, btn))


# Menu Bar for Help, About, and Feedback
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Add the File menu
menu_file = tk.Menu(menu_bar, tearoff=0)

menu_file.add_command(label="Import Commands", command=import_commands)
menu_file.add_command(label="Export Available Commands", command=export_commands)
menu_file.add_command(label="Export Queued Commands", command=export_queued_commands)
#menu_file.add_command(label="Import Queued Commands", command=import_queued_commands)
menu_bar.add_cascade(label="File", menu=menu_file)

menu_help = tk.Menu(menu_bar, tearoff=0)
menu_help.add_command(label="Instructions", command=show_help)
menu_help.add_command(label="API/Commands", command=show_api_commands)
menu_bar.add_cascade(label="Help", menu=menu_help)

menu_about = tk.Menu(menu_bar, tearoff=0)
menu_about.add_command(label="About", command=show_about)
menu_bar.add_cascade(label="About", menu=menu_about)

menu_feedback = tk.Menu(menu_bar, tearoff=0)
menu_feedback.add_command(label="Feedback", command=show_feedback)
menu_bar.add_cascade(label="Feedback", menu=menu_feedback)


# Call the function to ensure the file is created
ensure_commands_file()

# Load commands when the app starts
load_commands()
load_queued_commands()
update_command_count()

# Start monitoring the output queue
root.after(100, process_output_queue)

root.mainloop()
