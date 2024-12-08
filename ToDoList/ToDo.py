import tkinter as tk
from tkinter import messagebox

def AddToDO():
    ToDO = entry.get().strip()
    if ToDO:
        Output.insert(tk.END,ToDO +"\n")
        entry.delete(0, tk.END)

def Delete():
    try:
        SelectionIndex = Output.curselection()

        if SelectionIndex:
            for Selected in reversed(SelectionIndex):
                Output.delete(Selected)
        else:
            messagebox.showerror("error","No selection, please select item to delete")
    except IndexError:
        messagebox.showerror("error","Error in delete operation")
            
def DoneTask():
    messagebox.showinfo("info","implementing")

root = tk.Tk()
root.title("TO-DO Application")
root.wm_geometry("400x400")

entry = tk.Entry(root, width = 40)
entry.grid(row=0, column=0, padx=5,pady=10)

Button = tk.Button(root,text = "Add", width =5, command=AddToDO)
Button.grid(row=0,column=1,padx=5, pady=10)

Output = tk.Listbox(root, width = 50, height = 10, selectmode=tk.EXTENDED)
Output.grid(row=1, columnspan=2, padx =5, pady=5)

button_frame = tk.Frame(root)
button_frame.grid(row=2, column=0, pady=10, sticky="w")

Button_Del = tk.Button(button_frame, text="Delete", width=10, command=Delete)
Button_Del.pack(side=tk.LEFT, padx=5)

Button_Done = tk.Button(button_frame, text="Done", width=10, command=DoneTask)
Button_Done.pack(side=tk.LEFT, padx=5)

root.mainloop()