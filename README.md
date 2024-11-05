# SAS_Mgmt_Project
 The Employee Leave Management System is a Python-based GUI app for efficient leave tracking across industries. With an intuitive interface and automated database, it allows managers to view, update, and analyze leave schedules, helping maintain staffing levels and streamline administrative tasks for enhanced workforce planning.

# Employee Management and Timetable Tracking System

This project is a Python-based application designed to help managers in various industries, such as oil and gas, to efficiently track and manage employee schedules, including leave and work assignments. Built with a Tkinter GUI, the application provides an interactive interface to view, edit, and update employee data. Additionally, the application automates database updates and schedules daily updates, ensuring data accuracy and accessibility.

## Features

- **User-Friendly GUI**: A Tkinter-based interface with a modern Azure theme for intuitive navigation and employee management.
- **Dynamic Database Management**: Automates updates to employee data, schedules daily updates, and stores all information in a Python dictionary.
- **Employee Search & Management**: Easily search for employees by name, view detailed information, and perform actions like adding, editing, or deleting employees.
- **Timetable View**: Separate tabs display work and leave schedules by location, ensuring quick access to employee availability and schedule conflicts.
- **Theme Toggle**: Switch between light and dark modes for enhanced readability in various lighting conditions.

## File Structure

- **`Database.py`**: Contains employee data for different locations. It’s updated daily with the automated scheduler to ensure current information is available.
- **`Database_manager.py`**: Manages database updates, handling daily tasks such as reorganizing employee data for quick access by the GUI.
- **`GUI.py`**: The main application file that sets up the graphical interface, handles user input, and displays employee and timetable data.

## Requirements

- Python 3.x
- Tkinter (usually included with Python)
- `PIL` library for image handling in Tkinter

## How to Run

1. Clone or download this repository.
2. Run the `GUI.py` file to launch the application:

   ```bash
   python GUI.py
   ```

3. Follow the prompts to view, edit, or update employee data.

## Key Functionalities

- **Search Functionality**: Type in an employee’s name to view detailed information.
- **Edit/Delete Employee**: Modify employee details or remove an employee record.
- **Add New Employee**: Add new employee details, including ID, location, designation, and status.
- **Timetable View**: Access schedules for employees across various locations, including "On Duty" and "On Leave" sections.
- **Automated Database Updates**: Scheduled daily updates refresh the database at 1 AM.

## Future Enhancements

- Multi-user access with authentication.
- Integration with external databases.
- Advanced reporting and analytics on employee availability and scheduling trends.

## License

This project is open-source and available for use under the MIT License.
