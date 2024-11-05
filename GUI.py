import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import importlib.util
import os

# Load the Azure theme
root = tk.Tk()
style = ttk.Style(root)
root.tk.call("source", "azure.tcl")  # Make sure azure.tcl is in the same directory
root.tk.call("set_theme", "light")  # Apply the light theme initially

# Load Database.py
database_file_path = 'Database.py'  # Update this with the correct path if needed
module_name = os.path.splitext(os.path.basename(database_file_path))[0]
spec = importlib.util.spec_from_file_location(module_name, database_file_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

# Extract employee dictionaries from Database.py
fahud_oil_emp = module.fahud_oil_emp
yibal_oil_emp = module.yibal_oil_emp
yibal_gas_emp = module.yibal_gas_emp
kauther_gas_emp = module.kauther_gas_emp
nizwa_emp = module.nizwa_emp

# Function to get all employee dictionaries combined dynamically
def get_employee_dicts():
    return {**fahud_oil_emp, **yibal_oil_emp, **yibal_gas_emp, **kauther_gas_emp, **nizwa_emp}

# Available locations for the combobox
locations = ["Fahud-oil", "Yibal-oil", "Yibal-gas", "Kauther-gas", "Nizwa"]

# Create the main window
root.title("Employee Management and Timetable")
root.geometry("1200x700")

# Create a paned window to split the UI into two sections
paned_window = tk.PanedWindow(root, orient=tk.HORIZONTAL, sashrelief=tk.RAISED)
paned_window.pack(fill=tk.BOTH, expand=1, padx=20, pady=20)

# --------- Left pane: Employee Search and Display ---------
left_frame = ttk.Frame(paned_window)
paned_window.add(left_frame, width=400)

# Create a frame for search bar and search button
search_frame = ttk.Frame(left_frame)
search_frame.pack(pady=10, anchor='w', fill=tk.X)

# Combobox for searching employees
employee_names = list(get_employee_dicts().keys())
combobox = ttk.Combobox(search_frame, width=25)
combobox.pack(side=tk.LEFT, padx=10)
combobox['values'] = employee_names

# Function to refresh the combobox values dynamically
def refresh_combobox():
    global employee_names
    employee_names = list(get_employee_dicts().keys())  # Fetch updated employee names
    combobox['values'] = employee_names

# Search button beside the search bar
search_button = ttk.Button(search_frame, text="Search", command=lambda: show_employee_details())
search_button.pack(side=tk.LEFT, padx=5)

# Function to toggle between light and dark mode
def toggle_theme():
    current_theme = root.tk.call("ttk::style", "theme", "use")
    if current_theme == "azure-light":
        root.tk.call("set_theme", "dark")  # Switch to dark theme
    else:
        root.tk.call("set_theme", "light")  # Switch to light theme

# Create a switch for dark mode toggle beside the search button
dark_mode_switch = ttk.Checkbutton(search_frame, text="Dark Mode", style="Switch.TCheckbutton", command=toggle_theme)
dark_mode_switch.pack(side=tk.LEFT, padx=5)

# Initially hide the edit and delete buttons
edit_button = ttk.Button(left_frame, text="Edit", style="Accent.TButton", command=lambda: open_edit_window())
edit_button.pack(side=tk.LEFT)
edit_button.pack_forget()  # Hide the edit button initially

delete_button = ttk.Button(left_frame, text="Delete", style="Accent.TButton", command=lambda: confirm_delete())
delete_button.pack(side=tk.LEFT, padx=5)
delete_button.pack_forget()  # Hide the delete button initially

# Function to update suggestions in Combobox
def update_suggestions(event):
    value = event.widget.get().lower()
    suggestions = [name for name in employee_names if name.lower().startswith(value)]
    combobox['values'] = suggestions
    combobox.event_generate('<Down>')  # Show suggestions

combobox.bind('<KeyRelease>', update_suggestions)

# Display employee details with color styling for "From" and "To" sections
details_label = ttk.Label(left_frame, anchor='w', justify=tk.LEFT)
details_label.pack(pady=2, anchor='w')  # Minimal padding between labels and employee info

# Labels for "Status," "From," and "To" fields with color styling
status_label = ttk.Label(left_frame, anchor='w', justify=tk.LEFT)
from_label = ttk.Label(left_frame, anchor='w', justify=tk.LEFT)
to_label = ttk.Label(left_frame, anchor='w', justify=tk.LEFT)

# Function to display employee details
def show_employee_details():
    selected_name = combobox.get()
    employee_dicts = get_employee_dicts()  # Get the latest employee dictionary

    if selected_name in employee_dicts:
        employee_info = employee_dicts[selected_name]

        # Basic employee details
        details_text = (
            f"\n\nEmployee: {selected_name}\n"
            f"ID: {employee_info[0]}\n"
            f"Location: {employee_info[1]}\n"
            f"Designation: {employee_info[2]}\n"
            f"Nationality: {employee_info[3]}\n"
            f"Reliever: {employee_info[4]}"
        )
        details_label.config(text=details_text)

        # Apply color to "Status," "From" and "To" based on the employee's status
        if employee_info[5] == 1:
            status_label.config(text="Status: Working", foreground="green")
            from_label.config(text=f"From: {employee_info[6]}", foreground="green")
            to_label.config(text=f"To: {employee_info[7]}", foreground="green")
        else:
            status_label.config(text="Status: On Leave", foreground="red")
            from_label.config(text=f"From: {employee_info[6]}", foreground="red")
            to_label.config(text=f"To: {employee_info[7]}", foreground="red")

        # Pack the labels after updating
        status_label.pack(pady=0, anchor='w')
        from_label.pack(pady=0, anchor='w')
        to_label.pack(pady=0, anchor='w')

        # Show edit and delete buttons
        edit_button.pack(pady=2, side=tk.LEFT)
        delete_button.pack(pady=2, side=tk.LEFT, padx=10)
    else:
        details_label.config(text="Employee not found.")
        status_label.pack_forget()
        from_label.pack_forget()
        to_label.pack_forget()
        edit_button.pack_forget()
        delete_button.pack_forget()

# Function to confirm delete operation
def confirm_delete():
    selected_name = combobox.get()
    if selected_name in get_employee_dicts():
        # Create a confirmation window
        confirm_window = tk.Toplevel(root)
        confirm_window.title("Confirm Delete")
        confirm_window.geometry("300x150")

        label = ttk.Label(confirm_window, text=f"Are you sure you want to delete {selected_name}?", font=("TkDefaultFont", 10))
        label.pack(pady=20)

        # Function to delete employee data
        def delete_employee_data():
            employee_info = get_employee_dicts()[selected_name]
            current_location = employee_info[1]

            # Remove employee from location dictionary
            remove_employee_from_location(selected_name, current_location)

            # Update the database file
            update_database_file()

            # Refresh the employee list in the combobox
            refresh_combobox()

            # Close the confirmation and reset UI
            confirm_window.destroy()
            details_label.config(text="")
            status_label.pack_forget()
            from_label.pack_forget()
            to_label.pack_forget()
            edit_button.pack_forget()
            delete_button.pack_forget()

        # Confirm button
        confirm_button = ttk.Button(confirm_window, text="Confirm", style="Danger.TButton", command=delete_employee_data)
        confirm_button.pack(side=tk.LEFT, padx=20, pady=10)

        # Cancel button
        cancel_button = ttk.Button(confirm_window, text="Cancel", command=confirm_window.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=20, pady=10)

# Function to open the edit employee window
def open_edit_window():
    selected_name = combobox.get()
    if selected_name in get_employee_dicts():
        open_employee_window("Edit Employee", selected_name)

# Function to open the Add Employee window
def open_add_employee_window():
    open_employee_window("Add New Employee", None)

# General function to open employee window (both for editing and adding)
def open_employee_window(title, selected_name=None):
    employee_info = None if selected_name is None else get_employee_dicts()[selected_name]

    # Create a new window for adding or editing
    employee_window = tk.Toplevel(root)
    employee_window.title(title)
    employee_window.geometry("400x630")

    # Set a smaller font for labels and entry fields (font size 9)
    small_font = ("TkDefaultFont", 9)

    # Define editable fields
    fields = ['ID', 'Location', 'Designation', 'Nationality', 'Reliever', 'Status', 'From', 'To']
    entries = {}

    current_location = None if employee_info is None else employee_info[1]

    # Display employee name as a label if editing, otherwise show an entry widget for adding
    if selected_name is not None:
        # Display the employee name as a label (for editing)
        name_label = ttk.Label(employee_window, text=f"Name: {selected_name}", font=small_font)
        name_label.pack(anchor='w', padx=20, pady=3)
    else:
        # Entry for the employee name (for adding a new employee)
        label = ttk.Label(employee_window, text="Name:", font=small_font)
        label.pack(anchor='w', padx=20, pady=3)
        entry = ttk.Entry(employee_window, font=small_font)
        entry.pack(anchor='w', fill='x', padx=20, pady=3)
        entries['Name'] = entry

    # Create labels and entry widgets for each editable field
    for idx, field in enumerate(fields):
        label = ttk.Label(employee_window, text=f"{field}:", font=small_font)
        label.pack(anchor='w', padx=20, pady=3)
        if field == 'Location':
            location_combobox = ttk.Combobox(employee_window, font=small_font, values=locations)
            location_combobox.pack(anchor='w', fill='x', padx=20, pady=3)
            if employee_info:
                location_combobox.set(employee_info[1])  # Set current location
            entries[field] = location_combobox
        elif field == 'Status':
            status_combobox = ttk.Combobox(employee_window, font=small_font, values=["Working", "On Leave"])
            status_combobox.pack(anchor='w', fill='x', padx=20, pady=3)
            if employee_info:
                current_status = "Working" if employee_info[5] == 1 else "On Leave"
                status_combobox.set(current_status)
            entries[field] = status_combobox
        else:
            entry = ttk.Entry(employee_window, font=small_font)
            entry.pack(anchor='w', fill='x', padx=20, pady=3)
            if employee_info:
                entry.insert(0, employee_info[idx])  # Existing employee data
            entries[field] = entry

    # Save button to add or update employee information
    def save_employee():
        if selected_name is None:
            # For new employees, get the name from the entry field
            name = entries['Name'].get()
        else:
            # For editing, use the existing name
            name = selected_name

        new_location = entries['Location'].get()

        # Update employee details in-memory
        employee_info = [
            entries['ID'].get(),
            new_location,
            entries['Designation'].get(),
            entries['Nationality'].get(),
            entries['Reliever'].get(),
            1 if entries['Status'].get() == "Working" else 0,
            entries['From'].get(),
            entries['To'].get(),
        ]

        # Handle location change for editing
        if selected_name is not None and new_location != current_location:
            remove_employee_from_location(selected_name, current_location)
            add_employee_to_location(name, new_location, entries)
        elif selected_name is None:  # New employee case
            add_employee_to_location(name, new_location, entries)
        else:
            # Update existing employee info in the current location dictionary
            update_employee_in_location(name, current_location, employee_info)

        # Update the database file
        update_database_file()

        # Refresh the combobox and search functionality with updated names
        refresh_combobox()

        # Refresh the employee details after save
        show_employee_details()

        # Close the employee window after saving
        employee_window.destroy()

    save_button = ttk.Button(employee_window, text="Save", command=save_employee, style="Accent.TButton")
    save_button.pack(pady=10)

# Function to remove an employee from a location dictionary
def remove_employee_from_location(name, location):
    if location == "Fahud-oil" and name in fahud_oil_emp:
        del fahud_oil_emp[name]
    elif location == "Yibal-oil" and name in yibal_oil_emp:
        del yibal_oil_emp[name]
    elif location == "Yibal-gas" and name in yibal_gas_emp:
        del yibal_gas_emp[name]
    elif location == "Kauther-gas" and name in kauther_gas_emp:
        del kauther_gas_emp[name]
    elif location == "Nizwa" and name in nizwa_emp:
        del nizwa_emp[name]

# Function to add an employee to a location dictionary
def add_employee_to_location(name, location, entries):
    employee_info = [
        entries['ID'].get(),
        location,
        entries['Designation'].get(),
        entries['Nationality'].get(),
        entries['Reliever'].get(),
        1 if entries['Status'].get() == "Working" else 0,
        entries['From'].get(),
        entries['To'].get(),
    ]
    if location == "Fahud-oil":
        fahud_oil_emp[name] = employee_info
    elif location == "Yibal-oil":
        yibal_oil_emp[name] = employee_info
    elif location == "Yibal-gas":
        yibal_gas_emp[name] = employee_info
    elif location == "Kauther-gas":
        kauther_gas_emp[name] = employee_info
    elif location == "Nizwa":
        nizwa_emp[name] = employee_info

# Function to update employee data in the same location dictionary
def update_employee_in_location(name, location, employee_info):
    if location == "Fahud-oil":
        fahud_oil_emp[name] = employee_info
    elif location == "Yibal-oil":
        yibal_oil_emp[name] = employee_info
    elif location == "Yibal-gas":
        yibal_gas_emp[name] = employee_info
    elif location == "Kauther-gas":
        kauther_gas_emp[name] = employee_info
    elif location == "Nizwa":
        nizwa_emp[name] = employee_info

# Function to update the Database.py file
def update_database_file():
    database_file_path = 'Database.py'
    all_employee_data = {
        'fahud_oil_emp': fahud_oil_emp,
        'yibal_oil_emp': yibal_oil_emp,
        'yibal_gas_emp': yibal_gas_emp,
        'kauther_gas_emp': kauther_gas_emp,
        'nizwa_emp': nizwa_emp
    }
    with open(database_file_path, 'w') as f:
        f.write("# Updated Employee Database\n")
        for location, employees in all_employee_data.items():
            f.write(f"{location} = {{\n")
            for employee_name, employee_details in employees.items():
                employee_data = ', '.join([f"'{value}'" if isinstance(value, str) else str(value) for value in employee_details])
                f.write(f"    '{employee_name}': [{employee_data}],\n")
            f.write("}\n\n")

# --------- Right pane: Timetable (Tabbed Interface) ---------
right_frame = ttk.Frame(paned_window)
paned_window.add(right_frame)

# Notebook widget for tabbed interface
notebook = ttk.Notebook(right_frame)
notebook.pack(fill="both", expand=True)

# Function to load timetable data
def load_timetable_data():
    if notebook.tabs():
        current_tab = notebook.index(notebook.select())
    else:
        current_tab = None
    for tab in notebook.tabs():
        notebook.forget(tab)
    all_employee_data = {
        "Fahud-oil": fahud_oil_emp,
        "Yibal-oil": yibal_oil_emp,
        "Yibal-gas": yibal_gas_emp,
        "Kauther-gas": kauther_gas_emp,
        "Nizwa": nizwa_emp
    }
    for location, employees in all_employee_data.items():
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=location)
        tree = ttk.Treeview(frame, columns=("Employee", "Emp ID", "Discipline", "Reliever", "From", "To"), show="headings")
        tree.pack(fill=tk.BOTH, expand=True)
        tree.heading("Employee", text="On Duty Employee")
        tree.heading("Emp ID", text="Emp ID")
        tree.heading("Discipline", text="Discipline")
        tree.heading("Reliever", text="Reliever")
        tree.heading("From", text="From")
        tree.heading("To", text="To")
        tree.column("Employee", width=150)
        tree.column("Emp ID", width=100)
        tree.column("Discipline", width=150)
        tree.column("Reliever", width=150)
        tree.column("From", width=80)
        tree.column("To", width=80)
        on_duty = []
        on_leave = []
        for employee_name, employee_details in employees.items():
            if employee_details[5] == 1:
                on_duty.append((employee_name, employee_details))
            else:
                on_leave.append((employee_name, employee_details))
        for employee_name, employee_details in on_duty:
            tree.insert('', 'end', values=[
                employee_name,
                employee_details[0],
                employee_details[2],
                employee_details[4],
                employee_details[6],
                employee_details[7]
            ])
        tree.insert('', 'end', values=[""] * 6)
        tree.insert('', 'end', values=[""] * 6)
        tree.insert('', 'end', values=["On Leave Employees"], tags=('on_leave_header',))
        for employee_name, employee_details in on_leave:
            tree.insert('', 'end', values=[
                employee_name,
                employee_details[0],
                employee_details[2],
                employee_details[4],
                employee_details[6],
                employee_details[7]
            ], tags=('on_leave',))
        tree.tag_configure('on_leave', foreground='red')
        tree.tag_configure('on_leave_header', font=('TkDefaultFont', 10, 'bold'), foreground='red')
    if current_tab is not None and notebook.tabs():
        notebook.select(current_tab)

# Load the initial timetable data
load_timetable_data()

# Button container for centering "Refresh" and "Add Employee" buttons
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

refresh_button = ttk.Button(button_frame, text="Refresh", command=load_timetable_data, style="Accent.TButton")
refresh_button.pack(side=tk.LEFT, padx=10)

add_employee_button = ttk.Button(button_frame, text="Add Employee", command=open_add_employee_window, style="Accent.TButton")
add_employee_button.pack(side=tk.LEFT, padx=10)

# Start the Tkinter main loop
root.mainloop()
