import random
from tkinter import *
from tkinter import ttk
import pyperclip

gui = Tk()
gui.title('Password Generator')
gui.geometry('350x350')
gui.resizable(0,0)

def generate_password():
    try:
        length = int(entry_length.get())
    except ValueError:
        label_result.config(text="Please enter a valid password length.",fg="red")
        return
    
    if length <= 0:
        label_result.config(text="please enter a positive number for the length.",fg="red",)
        return
    charecter_set=[]

    if var_lower.get():
        charecter_set.extend(lower)
    if var_upper.get():
        charecter_set.extend(upper)
    if var_num.get():
        charecter_set.extend(num)
    if var_special.get():
        charecter_set.extend(special)
    if not charecter_set:
        label_result.config(text="Select atleast on charecter set.", fg="red")
        return

    Password = "".join(random.sample(charecter_set,length))
    label_result.config(text=Password,fg="black")
    update_strength_bar(Password)

def copy_password():
    Password = label_result.cget("text")
    if Password and not Password.startswith("Select"):
        pyperclip.copy(Password)
        button_copy.config(text="Copied!")
        gui.after(1500, lambda: button_copy.config(text="Copy to Clipboard"))
    else:
        label_result.config(text="No password to copy.")

def update_strength_bar(Password):
    strength = assess_strength(Password)
    strength_bar['value']=strength
    label_strength.config(text=f"Strength: {strength}%")

def assess_strength(password):
    length = len(password)
    count_lower = sum(1 for char in password if char in lower)
    count_upper = sum(1 for char in password if char in upper)
    count_num = sum(1 for char in password if char in num)
    count_special = sum(1 for char in password if char in special)

    strength_points = length * 4
    if count_lower > 0:
        strength_points += 10
    if count_upper > 0:
        strength_points += 10
    if count_num > 0:
        strength_points += 10
    if count_special > 0:
        strength_points += 10

    # Normalize to a percentage scale
    strength_percentage = min(strength_points, 100)
    return strength_percentage

# Set background color
gui.configure(background='light blue')

# Style configuration for progress bars
style = ttk.Style(gui)
style.configure('Red.Horizontal.TProgressbar', foreground='red', background='red')
style.configure('Yellow.Horizontal.TProgressbar', foreground='yellow', background='yellow')
style.configure('Green.Horizontal.TProgressbar', foreground='green', background='green')

# Customizing widget colors
label_color = 'white'
button_color = 'blue'
text_color = 'black'

lower = 'abcdefghijklmnopqrstuvwxyz'
upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
num = '0123456789'
special = '@#$%&*'

var_lower = BooleanVar()
var_upper = BooleanVar()
var_num = BooleanVar()
var_special = BooleanVar()

Label(gui, text="Password Length:", bg='light blue', fg='black').pack(pady=10)
entry_length = Entry(gui)
entry_length.pack()

Checkbutton(gui, text="Include lowercase", var=var_lower, bg='light blue', fg=text_color, selectcolor='light blue').pack(anchor=W)
Checkbutton(gui, text="Include uppercase", var=var_upper, bg='light blue', fg=text_color, selectcolor='light blue').pack(anchor=W)
Checkbutton(gui, text="Include numbers", var=var_num, bg='light blue', fg=text_color, selectcolor='light blue').pack(anchor=W)
Checkbutton(gui, text="Include special characters", var=var_special, bg='light blue', fg=text_color, selectcolor='light blue').pack(anchor=W)

Button(gui, text="Generate Password", command=generate_password, bg=button_color, fg='white').pack(pady=10)

label_result = Label(gui, text="", font=('Helvetica', 12, 'bold'), bg='light blue', fg=text_color)
label_result.pack(pady=10)

button_copy = Button(gui, text="Copy to Clipboard", command=copy_password, bg=button_color, fg='white')
button_copy.pack(pady=5)

label_strength = Label(gui, text="Entropy: 0 bits", font=('Helvetica', 10), bg='light blue', fg=text_color)
label_strength.pack()

strength_bar = ttk.Progressbar(gui, length=200, maximum=100, style='Red.Horizontal.TProgressbar')
strength_bar.pack()


gui.mainloop()