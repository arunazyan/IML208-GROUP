import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from PIL import Image, ImageTk
from os.path import dirname, join

# Set the full path of the data file
file_path = join(dirname(__file__), "graduation_data.txt")

def generate_seat_map():
    # Generate a seat map for students and 2 parents based on user ID numbers
    student_seat_map = {(i, j): f"Seat {i*10 + j + 1}" for i in range(10) for j in range(10)}
    parent_seat_map = {(i + 10, j): f"Parent Seat {i*10 + j + 1}" for i in range(10) for j in range(10)}
    return {**student_seat_map, **parent_seat_map}

def determine_robe_size(height):
    if 146 <= height <= 150:
        return "38"
    elif 151 <= height <= 155:
        return "40"
    elif 156 <= height <= 160:
        return "42"
    elif 161 <= height <= 165:
        return "44"
    else:
        return "50"

def save_booking_data_to_file(data):
    with open(file_path, "a") as file:
        file.write(data + "\n")

def read_data_from_file():
    data_list = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                data_list.append(line.strip())
    except FileNotFoundError:
        pass  # Handle the case when the file does not exist
    return data_list

def delete_data_from_file(student_id_to_delete):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
        with open(file_path, "w") as file:
            for line in lines:
                if line.split(',')[1] != student_id_to_delete:  # Assuming student ID is the second element in the CSV
                    file.write(line)
    except FileNotFoundError:
        pass  # Handle the case when the file does not exist

def update_data_in_file(student_id_to_update, new_data):
    delete_data_from_file(student_id_to_update)  # Delete the old data
    save_booking_data_to_file(new_data)  # Append the updated data

def submit_registration():
    student_name = entry_name.get().upper()
    student_id = entry_id.get()
    student_email = entry_email.get()
    student_phone = "+60 " + entry_phone.get()
    parent1_name = entry_parent1.get().upper()
    parent2_name = entry_parent2.get().upper()
    selected_date = calendar.get_date()

    if not student_name or not student_id:
        messagebox.showerror("Error", "Please fill in all the required fields.")
    else:
        data = f"{student_name},{student_id},{student_email},{student_phone},{parent1_name},{parent2_name},{selected_date}"
        root.withdraw()
        show_second_interface(student_name, student_id, student_email, student_phone, parent1_name, parent2_name,
                               selected_date, data)

def show_second_interface(name, student_id, email, phone, parent1, parent2, selected_date, graduation_data):
    second_window = tk.Toplevel(root)
    second_window.title("GRADUATION SEAT AND ROBE SIZE SELECTION")
    second_window.geometry('1000x500+200+100')
    second_window.configure(bg='#997950')

    #SETTING COLOUR BACKGROUND 
    second_window.configure(bg='#997950')

    # Generate seat map
    seat_map = generate_seat_map()

    # Interface for selecting graduation seat
    label_seat = tk.Label(second_window, text="SELECT GRADUATION SEAT", width=40, fg='black', border=0, font=('Times New Roman', 12), bg='#997950')
    label_seat.pack(padx=20, pady=5)

    student_seat_var = tk.StringVar(second_window)
    parent_seat_var = tk.StringVar(second_window)

    # Assign seats based on student and parent IDs
    student_seat_var.set(seat_map.get(divmod(int(student_id), 10)))
    parent_seat_var.set(seat_map.get(divmod(int(student_id) + 100, 10)))
    parent_seat_var.set(seat_map.get(divmod(int(student_id) + 100, 10)))

    student_label_height = tk.Label(second_window, text="Student's seats", width=30, fg='black', border=0, font=('Times New Roman', 12))
    student_label_height.pack(padx=10, pady=10, anchor='center')

    student_seat_menu = tk.OptionMenu(second_window, student_seat_var, *seat_map.values())
    student_seat_menu.pack(padx=10, pady=20)

    parent_label_height = tk.Label(second_window, text="Parents' seats", width=30, fg='black', border=0, font=('Times New Roman', 12))
    parent_label_height.pack(padx=10, pady=10, anchor='center')

    parent_seat_menu = tk.OptionMenu(second_window, parent_seat_var, *seat_map.values())
    parent_seat_menu.pack(padx=10, pady=10)

    parent_seat_menu = tk.OptionMenu(second_window, parent_seat_var, *seat_map.values())
    parent_seat_menu.pack(padx=10, pady=10)

    # Interface for selecting graduation robe size
    label_height = tk.Label(second_window, text="STUDENTS GRADUATION ROBE (CM)", width=40, fg='black', border=0, font=('Times New Roman', 12))
    label_height.pack(padx=20, pady=10, anchor='center')

    label_height = tk.Label(second_window, text="Enter height in CM:", width=20, fg='black', border=0, font=('Times New Roman', 12))
    label_height.pack(padx=10, pady=5, anchor='center')

    entry_height = tk.Entry(second_window, width=20)
    entry_height.pack(padx=10, pady=20, anchor='center')

    size_chart_label = tk.Label(second_window, text="Size Chart: 38 (146-150cm), 40 (151-155cm), 42 (156-160cm), 44 (161-165cm), 50 (166cm and above)", font=('Times New Roman', 10))
    size_chart_label.pack(padx=10, pady=5, anchor='center')

    submit_button = tk.Button(second_window, text="SUBMIT", command=lambda: save_data_and_show_summary(name, student_id, email, phone, parent1, parent2, selected_date,student_seat_var.get(), parent_seat_var.get(), entry_height.get(), determine_robe_size(int(entry_height.get()))))
    submit_button.pack(padx=20, pady=10, anchor='center')

def save_data_and_show_summary(name, student_id, email, phone, parent1, parent2, selected_date, student_seat, parent_seat, height, robe_size):
    messagebox.showinfo("Registration Summary", f"Registration successful!\n\nName: {name}\nStudent ID: {student_id}\nEmail: {email}\nPhone: {phone}\nParent 1: {parent1}\nParent 2: {parent2}\nDate: {selected_date}\nStudent Seat: {student_seat}\nParent Seat: {parent_seat}\nHeight: {height} cm\nRobe Size: {robe_size}")

    # Save the data to the file after showing the summary
    save_booking_data_to_file(f"{name},{student_id},{email},{phone},{parent1},{parent2},{selected_date},{student_seat},{parent_seat},{height},{robe_size}")

# Create the main window
root = tk.Tk()
root.title("Graduation Seat Registration")
root.geometry('1000x500+200+100')
root.resizable(False, False)

# Load background image
background_image = Image.open("D:/New folder/MERBOOK-ING GRADUATION!/uitm_di_hatiku.png")
background_photo = ImageTk.PhotoImage(background_image)

# Calculate center coordinates
center_x = root.winfo_screenwidth() // 2.2  
center_y = root.winfo_screenheight() // 2.1

# Create a Label with the background image
background_label = tk.Label(root, image=background_photo)
background_label.place(x=center_x, y=center_y, anchor="center")

# Create and place heading text at the top and center using pack
heading = tk.Label(root, text="UITM GRADUATION DAY", fg='#ff9248', font=('Microsoft YaHei UI Light', 20, 'bold'))
heading.pack(pady=5) 

heading = tk.Label(root, text="Brought to you by MERBOOK-ING team", fg='#000000', font=('Microsoft YaHei UI Light', 12,))
heading.pack(pady=10) 

# STUDENT NAME
label_name = tk.Label(root, text="STUDENT NAME", width=20, fg='black', border=0, font=('Times New Roman', 12))
label_name.pack(padx=20, pady=5)

entry_name_var = tk.StringVar()  # Create a StringVar to hold the entry value
entry_name = tk.Entry(root, width=35, textvariable=entry_name_var)  
entry_name.pack(padx=20, pady=0)

# Function to automatically convert the name to uppercase
def uppercase_name(*args):
    current_value = entry_name_var.get()
    if current_value:
        entry_name_var.set(current_value.upper())

# Set the trace on the StringVar to update the value to uppercase when focus is out
entry_name_var.trace_add('write', uppercase_name)

# Function to convert to uppercase when focus is out
def uppercase_on_focus_out(event):
    current_value = entry_name_var.get()
    if current_value:
        entry_name_var.set(current_value.upper())

# Bind the function to the focus out event
entry_name.bind("<FocusOut>", uppercase_on_focus_out)

# STUDENT ID
label_id = tk.Label(root, text="STUDENT ID", width=15, fg='black', border=0, font=('Times New Roman', 12))
label_id.pack(padx=20, pady=5)

entry_id_var = tk.StringVar()  # Create a StringVar to hold the entry value
entry_id = tk.Entry(root, width=20, textvariable=entry_id_var)  
entry_id.pack(padx=20, pady=0)

# Validate function to allow only integers and limit length to 10 digits
validate_int_id = root.register(lambda s: s.isdigit() and len(s) <= 10)
entry_id.config(validate="key", validatecommand=(validate_int_id, "%P"))

# Function to automatically convert the name to uppercase when student ID box is clicked
def uppercase_name_on_id_click(event):
    uppercase_name()

# Bind the function to the click event of the student ID entry box
entry_id.bind("<ButtonRelease-1>", uppercase_name_on_id_click)

# STUDENT EMAIL
label_email = tk.Label(root, text="STUDENT EMAIL", width=15, fg='black', border=0, font=('Times New Roman', 12))
label_email.pack(padx=20, pady=5)

entry_email = tk.Entry(root, width=25)
entry_email.pack(padx=20, pady=0)

# STUDENT PHONE NUMBER
label_phone = tk.Label(root, text="STUDENT PHONE NUMBER", width=25, fg='black', border=0, font=('Times New Roman', 12))
label_phone.pack(padx=20, pady=5)

entry_phone_var = tk.StringVar()  # Create a StringVar to hold the entry value
entry_phone = tk.Entry(root, width=20, textvariable=entry_phone_var)  
entry_phone.pack(padx=20, pady=0)

# Validate function to allow only integers and limit length to 13 digits
validate_int_phone = root.register(lambda s: s.isdigit() and len(s) <= 13)
entry_phone.config(validate="key", validatecommand=(validate_int_phone, "%P"))

# Function to add "+60" prefix automatically
def add_prefix(event=None):
    current_value = entry_phone_var.get()
    if current_value and not current_value.startswith("+60"):
        entry_phone_var.set("+60" + current_value)

# Bind the function to the focus out event
entry_phone.bind("<FocusOut>", add_prefix)

# CALENDAR 
calendar_label = tk.Label(root, text="SELECT DATE", width=15, fg='black', border=0, font=('Times New Roman', 12))
calendar_label.pack(pady=5)

calendar = DateEntry(root, width=12, background='orange', foreground='white', borderwidth=2)
calendar.pack(pady=0)

# PARENT NAME (1)
label_parent1 = tk.Label(root, text="PARENT NAME (1)", width=15, fg='black', border=0, font=('Times New Roman', 12))
label_parent1.pack(padx=20, pady=5)

entry_parent1_var = tk.StringVar()  # Create a StringVar to hold the entry value
entry_parent1 = tk.Entry(root, width=35, textvariable=entry_parent1_var)
entry_parent1.pack(padx=20, pady=0)

# Function to automatically convert the parent name to uppercase
def uppercase_parent1(*args):
    current_value = entry_parent1_var.get()
    if current_value:
        entry_parent1_var.set(current_value.upper())

# Set the trace on the StringVar to update the value to uppercase when focus is out
entry_parent1_var.trace_add('write', uppercase_parent1)

# Function to convert to uppercase when focus is out
def uppercase_on_focus_out_parent1(event):
    current_value = entry_parent1_var.get()
    if current_value:
        entry_parent1_var.set(current_value.upper())

# Bind the function to the focus out event
entry_parent1.bind("<FocusOut>", uppercase_on_focus_out_parent1)

#6 PARENT NAME (2)
label_parent2 = tk.Label(root, text="PARENT NAME (2)", width=15, fg='black', border=0, font=('Times New Roman', 12))
label_parent2.pack(padx=20, pady=5)

entry_parent2_var = tk.StringVar()  # Create a StringVar to hold the entry value
entry_parent2 = tk.Entry(root, width=35, textvariable=entry_parent2_var)
entry_parent2.pack(padx=20, pady=0)

# Function to automatically convert the parent name to uppercase
def uppercase_parent2(*args):
    current_value = entry_parent2_var.get()
    if current_value:
        entry_parent2_var.set(current_value.upper())

# Set the trace on the StringVar to update the value to uppercase when focus is out
entry_parent2_var.trace_add('write', uppercase_parent2)

# Function to convert to uppercase when focus is out
def uppercase_on_focus_out_parent2(event):
    current_value = entry_parent2_var.get()
    if current_value:
        entry_parent2_var.set(current_value.upper())

# Bind the function to the focus out event
entry_parent2.bind("<FocusOut>", uppercase_on_focus_out_parent2)

# SAVING STUDENT DATA INTO THE FILE (graduation_data.txt)
def save_booking_data_to_file(data):
    with open("graduation_data.txt", "a") as file:
        file.write(data + "\n")

# BUTTON NEXT AND CANCEL
# BUTTON NEXT
next_button = tk.Button(root, text="NEXT", width=10, fg='black', border=2, font=('Times New Roman', 12), command=submit_registration)
next_button.pack(side=tk.RIGHT, padx=10, pady=10)

# BUTTON CANCEL
cancel_button = tk.Button(root, text="CANCEL", width=10, fg='black', border=2, font=('Times New Roman', 12), command=root.destroy)
cancel_button.pack(side=tk.LEFT, padx=10, pady=10)

# Run the Tkinter event loop
root.mainloop()
