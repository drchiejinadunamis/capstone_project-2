# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

# Import required modules for handling dates and system operations
import os
from datetime import datetime, date 

USERS_FILE_PATH = "user.txt"
DATETIME_STRING_FORMAT = "%Y-%m-%d"

def check_or_create_users_file():
    """Ensure there's a file for the program; if not, it will be initiated with a default admin record."""
    if not os.path.exists(USERS_FILE_PATH):
        with open(USERS_FILE_PATH, "w") as default_file:
            default_file.write("admin;password\n")

def read_users_file():
    """Fetch and return a data structure to reflect the USERNAME: PASSWORD pairing."""
    with open(USERS_FILE_PATH, 'r') as file:
        users = file.read().strip().split("\n")
        return {user.split(';')[0]: user.split(';')[1] for user in users}

def execute_login():
    """Simplified admin/worksite terminal gate (for scenario and user behaviour replay)."""
    logged_in = False
    user_dict = read_users_file()  # Aggregating the on-record default and other imports

    while not logged_in:
        print("LOGIN")
        current_user = input("Username: ")
        current_pass = input("Password: ")
        
        if current_user not in user_dict:
            print("User does not exist")
            continue
        elif user_dict[current_user] != current_pass:
            print("Wrong password")
            continue
        else:
            print("Login Successful!")
            logged_in = True
            return current_user

if __name__ == "__main__":
    check_or_create_users_file()
    user = execute_login()

def reg_user():
    # Load existing usernames to ensure no duplicates
    with open('user.txt', 'r') as users_file:
        existing_users = users_file.readlines()

    # Extract usernames for comparison
    existing_usernames = [user.split(';')[0].strip() for user in existing_users]

    while True:
        new_username = input("Enter new username: ")
        if new_username in existing_usernames:
            print("This username already exists. Please try another username.")
        else:
            new_password = input("Enter new password: ")
            confirm_password = input("Confirm password: ")
            if new_password == confirm_password:
                with open('user.txt', 'a') as users_file:
                    # Use ';' as the delimiter
                    users_file.write(f"{new_username};{new_password}\n")
                print("New user registered successfully.")
                break
            else:
                print("Passwords do not match. Please try again.")
  

def add_task():
    """
    Add a new task to the task list for the current user.
    
    Args:
    - task (dict): A dictionary containing task details.
    """
    task_title = input("Enter the title of the task: ")
    task_description = input("Enter the description of the task: ")
    task_due_date = input("Enter the due date of the task (YYYY-MM-DD): ")
    assigned_to = input("Enter the username of the person this task is assigned to: ")
    current_date = datetime.now().strftime("%Y-%m-%d")  # Format the current date correctly
    is_completed = "No"

    # Ensure ';' is used as the delimiter consistently, without spaces to avoid parsing issues
    task_entry = f"{assigned_to};{task_title};{task_description};{current_date};{task_due_date};{is_completed}\n"

    with open('tasks.txt', 'a') as file:
        file.write(task_entry)

    print("Task added successfully.")


def view_all():
    """
    Display all tasks for the current user.
    """
    # Ensure only authenticated users can view tasks
    print("All tasks:\n")

    with open('tasks.txt', 'r') as tasks_file:
        tasks = tasks_file.readlines()

    for idx, task in enumerate(tasks, start=1):
        task_details = task.strip().split(";")  # Using ';' as the consistent delimiter

        print(f"Task {idx}:\nAssigned to: {task_details[0]}\nTitle: {task_details[1]}\nDescription: {task_details[2]}\nDate assigned: {task_details[3]}\nDue date: {task_details[4]}\nCompleted: {task_details[5]}\n")




def edit_task(task_id, username, tasks):
    task_details = tasks[task_id - 1].strip().split(";")
    if task_details[5].strip() == "Yes":
        print("This task has already been completed and cannot be edited.")
        return

    print("Do you want to:\n1. Mark this task as complete\n2. Edit this task")
    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        mark_task_as_complete(task_id, tasks)
    elif choice == "2":
        perform_task_editing(task_id, tasks)
    else:
        print("Invalid choice. Please enter 1 or 2.")

def mark_task_as_complete(task_id, tasks):
    updated_tasks = []
    for i, task in enumerate(tasks, start=1):
        if i == task_id:
            task_details = task.strip().split(";")
            task_details[5] = " Yes"  # Mark as completed
            updated_task = ";".join(task_details) + "\n"
            updated_tasks.append(updated_task)
        else:
            updated_tasks.append(task)

    with open('tasks.txt', 'w') as file:
        file.writelines(updated_tasks)
    print("Task marked as complete.")

def perform_task_editing(task_id, tasks):
    task = tasks[task_id - 1]
    task_details = task.strip().split(";")

    print("Edit the task:\n1. Assignee username\n2. Due date")
    edit_choice = input("Enter your choice (1 or 2): ")

    if edit_choice == "1":
        new_username = input("Enter new username: ")
        task_details[0] = new_username
    elif edit_choice == "2":
        new_due_date = input("Enter new due date (YYYY-MM-DD): ")
        task_details[4] = new_due_date
    else:
        print("Invalid choice. Please enter 1 or 2.")
        return

    updated_task = ";".join(task_details)
    tasks[task_id - 1] = updated_task + "\n"
    with open('tasks.txt', 'w') as file:
        file.writelines(tasks)
    print("Task updated successfully.")

def view_mine():
    username = input("Enter your username to view your tasks: ")
    with open('tasks.txt', 'r') as tasks_file:
        tasks = [task for task in tasks_file.readlines() if task.split(";")[0] == username]

    if not tasks:
        print("You have no tasks assigned.")
        return

    for idx, task in enumerate(tasks, start=1):
        task_details = task.strip().split(";")
        print(f"Task {idx}:\nAssigned to: {task_details[0]}\nTitle: {task_details[1]}\nDescription: {task_details[2]}\nDate assigned: {task_details[3]}\nDue date: {task_details[4]}\nCompleted: {task_details[5]}\n")

    task_number = int(input("Enter the number of the task you want to view or edit(such as 1, 2,3 ..), or '-1' to return to the main menu: "))
    if task_number == -1:
        return
    elif 1 <= task_number <= len(tasks):
        edit_task(task_number, username, tasks)
    else:
        print("Invalid task number. Please try again.")

def parse_date(date_string):
    """
    Tries to parse a date string in various formats and return a date object.
    """
    for date_format in ("%Y-%m-%d", "%d-%m-%y"):  # Add more formats as needed
        try:
            return datetime.strptime(date_string, date_format).date()
        except ValueError:
            continue
    raise ValueError(f"Date format for {date_string} not recognized.")


def generate_reports():
    #Generate a report of all tasks, including a summary of completed and pending tasks.
    # Initialize counters and data structures for report generation
    total_tasks = 0
    completed_tasks = 0
    uncompleted_tasks = 0
    overdue_tasks = 0
    total_users = 0
    tasks_per_user = {}

    # Process tasks to update counters
    with open('tasks.txt', 'r') as tasks_file:
        tasks = tasks_file.readlines()
        total_tasks = len(tasks)
        for task in tasks:
            task_details = task.strip().split(';')
            # Ensure task has all required details before processing
            if len(task_details) >= 6:
                # Existing code for handling task details
                try:
                    due_date = parse_date(task_details[4].strip())
                    if due_date < date.today():
                        overdue_tasks += 1
                except ValueError as e:
                    print(e)  # Handle or log the error as needed
                # Count tasks per user
                if task_details[0] in tasks_per_user:
                    tasks_per_user[task_details[0]] += 1
                else:
                    tasks_per_user[task_details[0]] = 1
            else:
                print(f"Task skipped due to missing details: {task}")

    # Process users
    with open('user.txt', 'r') as user_file:
        users = user_file.readlines()
        total_users = len(users)

    # Generate task_overview.txt
    with open('task_overview.txt', 'w') as task_overview_file:
        task_overview_file.write(f"Total number of tasks: {total_tasks}\n")
        task_overview_file.write(f"Total number of completed tasks: {completed_tasks}\n")
        task_overview_file.write(f"Total number of uncompleted tasks: {uncompleted_tasks}\n")
        task_overview_file.write(f"Total number of overdue tasks: {overdue_tasks}\n")
        task_overview_file.write(f"Percentage of incomplete tasks: {uncompleted_tasks / total_tasks * 100:.2f}%\n")
        task_overview_file.write(f"Percentage of overdue tasks: {overdue_tasks / total_tasks * 100:.2f}%\n")

    # Generate user_overview.txt
    with open('user_overview.txt', 'w') as user_overview_file:
        user_overview_file.write(f"Total number of users: {total_users}\n")
        user_overview_file.write(f"Total number of tasks: {total_tasks}\n")
        for user, tasks_count in tasks_per_user.items():
            user_overview_file.write(f"\nUser: {user}\n")
            user_overview_file.write(f"Total tasks assigned: {tasks_count}\n")
            user_overview_file.write(f"Percentage of total tasks: {tasks_count / total_tasks * 100:.2f}%\n")


def display_statistics(current_user):
    # Check if the current user is an admin
    if current_user != "admin":
        print("Access denied: This feature is available to admin only.")
        return

    # Utilize existing function to get the number of users
    username_password = read_users_file()
    num_users = len(username_password.keys())

    # Assuming a similar function exists for tasks or direct file reading
    with open('tasks.txt', 'r') as tasks_file:
        task_list = tasks_file.readlines()
    num_tasks = len(task_list)

    print("-----------------------------------")
    print(f"Number of users: \t\t {num_users}")
    print(f"Number of tasks: \t\t {num_tasks}")
    print("-----------------------------------")

    
# Main function to run the task manager application

def main():
    """
    Main function for running the task manager application.
    """
    
    while True:
        # Display menu with available options to the user
        print("\nPlease choose one of the following options:")
        print("a - Add a new task")
        print("va - View all tasks")
        print("vm - View my tasks")
        print("gr - Generate reports")  # New option for generating reports
        print("ds - Display statistics")
        print("r - Register a new user")
        print("e - Exit the program")
        
        # Get user choice and convert it to lowercase to handle case-insensitive comparisons
        user_choice = input("Enter your choice: ").lower()
        
        # Process the user's choice
        if user_choice == 'a':
            add_task()
        elif user_choice == 'va':
            view_all()
        elif user_choice == 'vm':
            view_mine()
        elif user_choice == 'gr':  # Check if the user selected the option to generate reports
            generate_reports()
            print("Reports generated successfully.")
        elif user_choice == 'ds'and username == 'admin':  
            display_statistics() 
        elif user_choice == 'r':
            reg_user()
        elif user_choice == 'e':
            print('Goodbye!!!')
            print("Exiting the program...")
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()