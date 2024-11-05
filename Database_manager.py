import datetime
import numpy as np
import schedule
import time

# Path to the Database.py file
file_path = 'Database.py'  # Update this with the actual file path

# Function to load the dictionaries
def load_dictionaries():
    import importlib.util
    spec = importlib.util.spec_from_file_location("database", file_path)
    database = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(database)
    return database

# Function to modify the dictionaries and write them back to the file
def update_database_dictionaries():
    # Step 1: Load the dictionaries from the database file
    db = load_dictionaries()

    # Function to modify the employee dictionaries
    def update_employee_status(employee_dict):
        current_date = datetime.datetime.now().date()

        # Iterate over each key (employee) in the dictionary
        for name, details in employee_dict.items():
            # Extract date1 and date2
            date1 = details[6]
            date2 = details[7]

            # Convert date2 to a datetime object for comparison
            try:
                date2_obj = datetime.datetime.strptime(date2, '%Y-%m-%d').date()
            except ValueError:
                continue  # Skip if date2 is invalid

            # Check if the current date is equal to or past date2
            if current_date >= date2_obj:
                # Update date1 to be date2 and set date2 to NaN
                details[6] = date2
                details[7] = "YYYY-DD-MM"

                # Toggle the working status (0 to 1 or 1 to 0)
                details[5] = 1 if details[5] == 0 else 0

    # Step 2: Modify the dictionaries in memory
    update_employee_status(db.fahud_oil_emp)
    update_employee_status(db.yibal_oil_emp)
    update_employee_status(db.yibal_gas_emp)
    update_employee_status(db.kauther_gas_emp)
    update_employee_status(db.nizwa_emp)

    # Function to format dictionaries with custom indentation and structure
    def format_dict(d):
        output = "{\n"
        for key, value in d.items():
            output += f'    "{key}": {value},\n'
        output += "}"
        return output

    # Step 3: Write the modified dictionaries back to the file with proper formatting
    with open(file_path, 'w') as file:
        file.write("# Updated Database.py\n\n")

        # Write each dictionary to the file with custom formatting
        file.write('fahud_oil_emp = ' + format_dict(db.fahud_oil_emp) + '\n\n')
        file.write('yibal_oil_emp = ' + format_dict(db.yibal_oil_emp) + '\n\n')
        file.write('yibal_gas_emp = ' + format_dict(db.yibal_gas_emp) + '\n\n')
        file.write('kauther_gas_emp = ' + format_dict(db.kauther_gas_emp) + '\n\n')
        file.write('nizwa_emp = ' + format_dict(db.nizwa_emp) + '\n\n')

    print("Database file has been updated and formatted successfully.")

# Schedule the task to run at 1 AM every day
schedule.every().day.at("01:00").do(update_database_dictionaries)

# Keep the script running and checking the schedule
while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute
