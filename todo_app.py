import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
import json
import os

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.root.geometry("400x400")

        #Load and set background image
        self.bg_image = PhotoImage(file="your_background_image.png")#Replace the background with the image
        self.background_label = tk.Label(root, image=self.bg_image)
        self.background_label.place(relwidth=1, relheight=1)

        # Initialize tasks list
        self.tasks = []
        self.load_tasks()  # Load tasks from file

        # Create a button that opens the control menu
        self.menu_button = tk.Button(root, text="Open Menu", command=self.open_menu, width=10, height=2, bg='lightblue')
        self.menu_button.pack(pady=10)

        # Task Listbox
        self.task_listbox = tk.Listbox(root, width=50, height=10)
        self.task_listbox.pack(pady=10)
        self.refresh_task_list()

    def open_menu(self):
        # Create a top-level window for the menu with a larger default size
        self.menu_window = tk.Toplevel(self.root)
        self.menu_window.title("Task Menu")
        self.menu_window.geometry("250x400")  # Adjust size as needed

        # Define button colors
        button_colors = ["lightblue", "lightgreen", "lightyellow", "lightcoral", "lightpink"]

        # Create buttons for the menu
        buttons = [
            ("Add Task", self.add_task_popup),
            ("View Tasks", self.view_tasks),
            ("Mark Complete", self.mark_complete),
            ("Delete Task", self.delete_task),
            ("Exit", self.menu_window.destroy)
        ]

        for i, (text, command) in enumerate(buttons):
            button = tk.Button(self.menu_window, text=text, command=command, width=20, height=2, bg=button_colors[i])
            button.pack(pady=10)  # Use pack for vertical arrangement

    def add_task_popup(self):
        # Create a popup for adding a task
        self.add_task_window = tk.Toplevel(self.root)
        self.add_task_window.title("Add Task")
        self.add_task_window.geometry("300x200")

        tk.Label(self.add_task_window, text="Task Title:").pack(pady=5)
        self.title_entry = tk.Entry(self.add_task_window, width=30)
        self.title_entry.pack(pady=5)

        tk.Label(self.add_task_window, text="Description:").pack(pady=5)
        self.desc_entry = tk.Entry(self.add_task_window, width=30)
        self.desc_entry.pack(pady=5)

        tk.Label(self.add_task_window, text="Category:").pack(pady=5)
        self.category_entry = tk.Entry(self.add_task_window, width=30)
        self.category_entry.pack(pady=5)

        add_button = tk.Button(self.add_task_window, text="Add", command=self.add_task)
        add_button.pack(pady=10)

    def add_task(self):
        title = self.title_entry.get()
        description = self.desc_entry.get()
        category = self.category_entry.get()
        if title and description and category:
            task = {"title": title, "description": description, "category": category, "status": "pending"}
            self.tasks.append(task)
            self.save_tasks()
            self.refresh_task_list()
            self.add_task_window.destroy()
        else:
            messagebox.showwarning("Warning", "Please fill all fields before adding a task.")

    def view_tasks(self):
        tasks_str = "\n".join([f"{t['title']} - {t['description']} [{t['category']}] ({t['status']})" for t in self.tasks])
        messagebox.showinfo("Tasks", tasks_str if tasks_str else "No tasks available.")

    def mark_complete(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            self.tasks[selected_task_index[0]]["status"] = "completed"
            self.save_tasks()
            self.refresh_task_list()
        else:
            messagebox.showwarning("Warning", "Please select a task to mark as complete.")

    def delete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            del self.tasks[selected_task_index[0]]
            self.save_tasks()
            self.refresh_task_list()
        else:
            messagebox.showwarning("Warning", "Please select a task to delete.")

    def refresh_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            task_display = f"{task['title']} - {task['description']} [{task['category']}] ({task['status']})"
            self.task_listbox.insert(tk.END, task_display)

    def load_tasks(self):
        if os.path.exists('tasks.json'):
            with open('tasks.json', 'r') as f:
                self.tasks = json.load(f)

    def save_tasks(self):
        with open('tasks.json', 'w') as f:
            json.dump(self.tasks, f, indent=4)

# Create the main application window
root = tk.Tk()
app = ToDoApp(root)
root.mainloop()