'''
This Python script, is a comprehensive task management system designed for both administrators and users. 
It enables user registration with secure password verification, task assignment with detailed specifications, 
and personal task viewing for efficient management. 
Administrators have exclusive access to generate detailed reports and view system-wide statistics, 
enhancing oversight and productivity. This high-level overview serves as a guide for navigating the application's functionalities, 
ensuring a user-friendly experience for task administration and tracking

'''
# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Declare the global variable at the top of your script
curr_user = None
# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

task_list = []  # Initialize an empty list to hold task dictionaries
with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

    # Parse each task string into a dictionary and add to task_list
    for t_str in task_data:
        task_components = t_str.split(";")
        curr_t = {
            'username': task_components[0],
            'title': task_components[1],
            'description': task_components[2],
            'assigned_date': datetime.strptime(task_components[3], DATETIME_STRING_FORMAT),
            'due_date': datetime.strptime(task_components[4], DATETIME_STRING_FORMAT),
            'completed': task_components[5] == "Yes"
        }
        task_list.append(curr_t)


#====Login Section====
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password\n")  # Ensure newline character for proper reading

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().strip().split("\n")  # Use strip to remove potential trailing newline

# Convert to a dictionary
username_password = {user.split(';')[0]: user.split(';')[1] for user in user_data}

logged_in = False
while not logged_in:
    print("LOGIN")
    curr_user_input = input("Username: ")
    curr_pass = input("Password: ")

    if curr_user_input not in username_password:
        print("User does not exist")
        continue
    elif username_password[curr_user_input] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True
        curr_user = curr_user_input  # Set the global variable upon successful login


#create a helper function named safe_write that ensures new entries are always added on a new line:
def safe_write(file_path, content):
    """Appends content to a file, ensuring it starts on a new line if the file is not empty."""
    with open(file_path, 'a+') as file:
        file.seek(0, os.SEEK_END)  # Go to the end of the file
        if file.tell() > 0:  # Check if the file is not empty
            file.seek(-1, os.SEEK_END)  # Check the last character
            if file.read(1) != '\n':
                content = '\n' + content  # Prepend a newline if the last character is not a newline
        file.write(content + '\n')  # Always append a newline to content


def reg_user():
    """Registers a new user with password verification."""
    username = input("Enter new username: ").strip()
    password = input("Enter new password: ").strip()
    password_verify = input("Re-enter your password for verification: ").strip()

    if not username:
        print("Username cannot be empty.")
        return
    if not password or password != password_verify:
        print("Passwords do not match or are empty.")
        return

    try:
        with open('user.txt', 'r') as users_file:
            users = users_file.readlines()
            for user in users:
                if username == user.split(';')[0].strip():
                    print("Username already exists.")
                    return

        # Use safe_write to append the new user
        safe_write('user.txt', f"{username};{password}")
        print("User registered successfully.")
    except IOError as e:
        print(f"An error occurred while accessing 'user.txt': {e}")


def add_task():
    """Adds a new task directly to the tasks.txt file."""
    task_title = input("Enter task title: ").strip()
    task_description = input("Enter task description: ").strip()
    assigned_to = input("Enter the username of the person this task is assigned to: ").strip()
    due_date = input("Enter due date (YYYY-MM-DD): ").strip()
    
    try:
        datetime.strptime(due_date, '%Y-%m-%d')
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    current_date = datetime.now().strftime('%Y-%m-%d')
    completed = "No"

    # Use safe_write to append the new task
    safe_write("tasks.txt", f"{assigned_to};{task_title};{task_description};{current_date};{due_date};{completed}")

    print("Task added successfully.")


def view_all():
    """Displays all tasks."""
    try:
        with open('tasks.txt', 'r') as tasks_file:
            tasks = tasks_file.readlines()
        
        if not tasks:
            print("There are no tasks to display.")
            return

        print("All tasks:\n")
        for index, task in enumerate(tasks, start=1):
            task_details = task.strip().split(';')
            assigned_date = datetime.strptime(task_details[3], "%Y-%m-%d").strftime("%d-%m-%Y")
            due_date = datetime.strptime(task_details[4], "%Y-%m-%d").strftime("%d-%m-%Y")
            
            print(f"Task {index}:\nAssigned to: {task_details[0]}\nTitle: {task_details[1]}\n"
                  f"Description: {task_details[2]}\nDate Assigned: {assigned_date}\n"
                  f"Due Date: {due_date}\nCompleted: {task_details[5]}\n")
            print("--------------------------------------------------")
    except IOError:
        print("Could not read 'tasks.txt'. Please ensure the file exists and is accessible.")
            

def mark_task_as_complete(task_index, tasks):
    """Marks a task as complete."""
    task_details = tasks[task_index].strip().split(';')
    if task_details[5] != 'Yes':
        task_details[5] = 'Yes'
        tasks[task_index] = ';'.join(task_details) + '\n'


def edit_task(task_index, tasks):
    """Edits a task."""
    task_details = tasks[task_index].strip().split(';')
    if task_details[5] == 'Yes':
        print("This task has already been completed and cannot be edited.")
        return

    print("Edit task:\n1. Assignee username\n2. Due date")
    choice = input("Enter your choice (1 or 2): ").strip()
    if choice == '1':
        new_username = input("Enter new username: ").strip()
        task_details[0] = new_username
    elif choice == '2':
        new_due_date = input("Enter new due date (YYYY-MM-DD): ").strip()
        task_details[4] = new_due_date

    tasks[task_index] = ';'.join(task_details) + '\n'
    print("Task updated successfully.")


def view_mine():
    global curr_user
    try:
        with open('tasks.txt', 'r') as tasks_file:
            tasks = tasks_file.readlines()

        user_tasks = [task for task in tasks if task.split(';')[0] == curr_user]
        if not user_tasks:
            print(f"No tasks found for user {curr_user}.")
            return

        print(f"Tasks assigned to {curr_user}:")
        for i, task in enumerate(user_tasks, start=1):
            parts = task.strip().split(';')
            print(f"{i}. Title: {parts[1]}\n   Description: {parts[2]}\n"
                  f"   Date Assigned: {parts[3]}\n   Due Date: {parts[4]}\n"
                  f"   Completed: {parts[5]}\n")

        task_choice = int(input("Select a task number to edit or mark as "
                                "complete, or '-1' to return to the main menu: "))
        if task_choice == -1:
            return

        if 1 <= task_choice <= len(user_tasks):
            task_index = tasks.index(user_tasks[task_choice - 1])
            print("Do you want to:\n1. Mark this task as complete\n2. Edit this task")
            user_choice = input("Enter your choice (1 or 2): ")
            if user_choice == '1':
                mark_task_as_complete(task_index, tasks)
            elif user_choice == '2':
                edit_task(task_index, tasks)

        # Instead of writing only user_tasks, write back all tasks
        with open('tasks.txt', 'w') as file:
            file.writelines(tasks)

    except IOError:
        print("Could not read 'tasks.txt'. Please ensure the file exists and is accessible.")

    
def display_statistics():
    global curr_user
    if curr_user != 'admin':
        print("Access denied: This feature is available to admin only.")
        return

    # Verify or generate necessary files
    if not os.path.exists("tasks.txt") or not os.path.exists("user.txt"):
        print("Required files are missing, generating reports...")
        generate_reports()  # Assumes generate_reports() function creates tasks.txt and user.txt if missing

    # Proceed with displaying statistics
    with open('user.txt', 'r') as users_file:
        users = users_file.readlines()
    num_users = len(users)

    with open('tasks.txt', 'r') as tasks_file:
        tasks = tasks_file.readlines()
    num_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if "Yes" in task.split(';')[5])
    incomplete_tasks = num_tasks - completed_tasks
    overdue_tasks = sum(1 for task in tasks if "No" in task.split(';')[5] and datetime.strptime(task.split(';')[4], "%Y-%m-%d") < datetime.now())

    # Display calculated statistics
    print("-----------------------------------")
    print(f"Number of users: {num_users}")
    print(f"Total tasks: {num_tasks}")
    print(f"Completed tasks: {completed_tasks}")
    print(f"Incomplete tasks: {incomplete_tasks}")
    print(f"Overdue tasks: {overdue_tasks}")
    print(f"Percentage incomplete: {(incomplete_tasks / num_tasks * 100) if num_tasks else 0:.2f}%")
    print(f"Percentage overdue: {(overdue_tasks / num_tasks * 100) if num_tasks else 0:.2f}%")
    print("-----------------------------------")


def generate_user_overview():
    tasks = []
    with open('tasks.txt', 'r') as f:
        for line in f:
            parts = line.strip().split(';')
            if len(parts) == 6:  # Ensure task line is complete
                tasks.append(parts)

    users = {}
    with open('user.txt', 'r') as f:
        for line in f:
            username = line.strip().split(';')[0]
            users[username] = {'tasks': [], 'completed': 0, 'incomplete': 0, 'overdue': 0}

    for task in tasks:
        username, title, description, assigned_date, due_date, completed = task
        task_dict = {'title': title, 'description': description, 'assigned_date': assigned_date, 'due_date': due_date, 'completed': completed}
        users[username]['tasks'].append(task_dict)
        if completed == "Yes":
            users[username]['completed'] += 1
        else:
            users[username]['incomplete'] += 1
            if datetime.strptime(due_date, DATETIME_STRING_FORMAT) < datetime.now():
                users[username]['overdue'] += 1

    total_tasks = len(tasks)
    with open('user_overview.txt', 'w') as f:
        f.write(f"Total number of users: {len(users)}\n")
        f.write(f"Total number of tasks: {total_tasks}\n")
        for username, details in users.items():
            total_user_tasks = len(details['tasks'])
            completed = details['completed']
            incomplete = details['incomplete']
            overdue = details['overdue']
            f.write(f"\nUser: {username}\n")
            f.write(f"Total tasks assigned: {total_user_tasks}\n")
            if total_tasks > 0:
                f.write(f"Percentage of total tasks: {(total_user_tasks / total_tasks) * 100:.2f}%\n")
            if total_user_tasks > 0:
                f.write(f"Tasks completed: {(completed / total_user_tasks) * 100:.2f}%\n")
                f.write(f"Tasks incomplete: {(incomplete / total_user_tasks) * 100:.2f}%\n")
                f.write(f"Tasks overdue: {(overdue / total_user_tasks) * 100:.2f}%\n")


def generate_reports():
    global curr_user
    if curr_user != 'admin':
        print("Access denied: This feature is available to admin only.")
        return
    # Load tasks and calculate statistics
    with open('tasks.txt', 'r') as file:
        tasks = file.readlines()
    
    # Load users
    with open('user.txt', 'r') as file:
        users = file.readlines()
    
    # Initialize statistics
    total_tasks = len(tasks)
    completed_tasks = sum('Yes' in task.split(';')[5] for task in tasks)
    uncompleted_tasks = total_tasks - completed_tasks
    overdue_tasks = sum('No' in task.split(';')[5] and datetime.strptime(task.split(';')[4], "%Y-%m-%d") < datetime.now() for task in tasks)
    incomplete_percentage = (uncompleted_tasks / total_tasks) * 100 if total_tasks else 0
    overdue_percentage = (overdue_tasks / total_tasks) * 100 if total_tasks else 0
    
    # Write task_overview.txt
    with open('task_overview.txt', 'w') as file:
        file.write(f"Total number of tasks: {total_tasks}\n")
        file.write(f"Total number of completed tasks: {completed_tasks}\n")
        file.write(f"Total number of uncompleted tasks: {uncompleted_tasks}\n")
        file.write(f"Total number of tasks that are overdue: {overdue_tasks}\n")
        file.write(f"Percentage of tasks incomplete: {incomplete_percentage:.2f}%\n")
        file.write(f"Percentage of tasks overdue: {overdue_percentage:.2f}%\n")

     # Initialize user statistics
    user_tasks = {user.split(';')[0]: [] for user in users}  # Dict to store tasks per user
    for task in tasks:
        task_details = task.strip().split(';')
        if task_details[0] in user_tasks:
            user_tasks[task_details[0]].append(task_details)

    # Write user_overview.txt
    with open('user_overview.txt', 'w') as file:
        file.write(f"Total number of users: {len(users)}\n")
        file.write(f"Total number of tasks: {total_tasks}\n")
        for user, tasks in user_tasks.items():
            total_user_tasks = len(tasks)
            completed = sum(1 for task in tasks if task[5] == 'Yes')
            incomplete = total_user_tasks - completed
            overdue = sum(1 for task in tasks if task[5] == 'No' and datetime.strptime(task[4], "%Y-%m-%d") < datetime.now())
            file.write(f"\nUser: {user}\n")
            file.write(f"Total tasks assigned: {total_user_tasks}\n")
            if total_user_tasks > 0:
                file.write(f"Percentage of total tasks: {(total_user_tasks / total_tasks * 100):.2f}%\n")
                file.write(f"Tasks completed: {completed} ({(completed / total_user_tasks * 100):.2f}%)\n")
                file.write(f"Tasks incomplete: {incomplete} ({(incomplete / total_user_tasks * 100):.2f}%)\n")
                file.write(f"Tasks overdue: {overdue} ({(overdue / total_user_tasks * 100):.2f}%)\n")
        if curr_user == 'admin':
            print("Reports successfully generated.")

def main():
    """Main program loop."""
    curr_user = 'admin'  # This should be dynamically determined based on the actual login mechanism
    while True:
        # Updated print statement to include "gr - generate reports" option
        print("\na - Add a new task\nr - Register a new user\nva - View all tasks\nvm - View my tasks\nds - Display statistics\ngr - Generate reports\ne - Exit")
        choice = input("Enter your choice: ").lower()

        if choice == 'a':
            add_task()
        elif choice == 'r':
            reg_user()
        elif choice == 'va':
            view_all()
        elif choice == 'vm':
            view_mine()
        elif choice == 'gr':
            if curr_user == 'admin':
                generate_reports()
            else:
                print("Access denied: This feature is available to admin only.")
        elif choice == 'ds':
            if curr_user == 'admin':
                display_statistics()
            else:
                print("Access denied: This feature is available to admin only.")
        elif choice == 'e':
            print('Goodbye!!!')
            print("Exiting the program...")
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()

