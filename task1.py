import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import json
import os

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ To-Do List Manager")
        self.root.geometry("950x700")
        self.root.configure(bg='#f9fafb')

        # Data storage
        self.tasks = []
        self.data_file = "tasks.json"
        self.dark_mode = False

        # Load existing tasks
        self.load_tasks()

        # Apply styles
        self.setup_styles()

        # Create GUI
        self.create_widgets()

        # Update task display
        self.refresh_task_list()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.apply_light_mode()

        # Treeview row hover effect
        self.task_tree_hover = None

    def apply_light_mode(self):
        self.root.configure(bg="#f9fafb")
        self.style.configure("TLabel", font=("Segoe UI", 11), background="#f9fafb")
        self.style.configure("TButton", font=("Segoe UI", 11, "bold"),
                             padding=8, relief="flat",
                             background="#2563eb", foreground="white")
        self.style.map("TButton", background=[("active", "#1d4ed8")])
        self.style.configure("Treeview", font=("Segoe UI", 11),
                             rowheight=30, background="white",
                             fieldbackground="white")
        self.style.configure("Treeview.Heading",
                             font=("Segoe UI", 11, "bold"),
                             background="#e5e7eb")

    def apply_dark_mode(self):
        self.root.configure(bg="#1e293b")
        self.style.configure("TLabel", font=("Segoe UI", 11), background="#1e293b", foreground="white")
        self.style.configure("TButton", font=("Segoe UI", 11, "bold"),
                             padding=8, relief="flat",
                             background="#3b82f6", foreground="white")
        self.style.map("TButton", background=[("active", "#1d4ed8")])
        self.style.configure("Treeview", font=("Segoe UI", 11),
                             rowheight=30, background="#0f172a",
                             fieldbackground="#0f172a", foreground="white")
        self.style.configure("Treeview.Heading",
                             font=("Segoe UI", 11, "bold"),
                             background="#334155", foreground="white")

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.apply_dark_mode()
        else:
            self.apply_light_mode()
        self.refresh_task_list()

    def create_widgets(self):
        # Title bar with theme switch
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill=tk.X, pady=10, padx=20)

        title_label = ttk.Label(top_frame, text="📋 My To-Do List",
                                font=('Segoe UI', 20, 'bold'))
        title_label.pack(side=tk.LEFT)

        theme_btn = ttk.Button(top_frame, text="🌙 Toggle Theme", command=self.toggle_theme)
        theme_btn.pack(side=tk.RIGHT)

        # Input frame
        input_frame = ttk.LabelFrame(self.root, text="➕ Add New Task", padding="15")
        input_frame.pack(fill=tk.X, padx=20, pady=(0, 15))

        self.task_entry = ttk.Entry(input_frame, width=40, font=("Segoe UI", 11))
        self.task_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        self.task_entry.bind('<Return>', lambda e: self.add_task())

        self.priority_var = tk.StringVar(value="Medium")
        priority_combo = ttk.Combobox(input_frame, textvariable=self.priority_var,
                                     values=["High", "Medium", "Low"], state="readonly", width=12)
        priority_combo.grid(row=0, column=1, padx=(0, 10))

        add_btn = ttk.Button(input_frame, text="➕ Add Task", command=self.add_task)
        add_btn.grid(row=0, column=2)

        # Search bar
        search_frame = ttk.Frame(self.root)
        search_frame.pack(fill=tk.X, padx=20, pady=(0, 10))

        ttk.Label(search_frame, text="🔍 Search:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.bind("<KeyRelease>", lambda e: self.refresh_task_list())

        # Task list frame
        list_frame = ttk.LabelFrame(self.root, text="📌 Tasks", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))

        columns = ('Task', 'Priority', 'Status', 'Created', 'Completed')
        self.task_tree = ttk.Treeview(list_frame, columns=columns, show='headings')

        self.task_tree.heading('Task', text='Task Description')
        self.task_tree.heading('Priority', text='Priority')
        self.task_tree.heading('Status', text='Status')
        self.task_tree.heading('Created', text='Created Date')
        self.task_tree.heading('Completed', text='Completed Date')

        self.task_tree.column('Task', width=350)
        self.task_tree.column('Priority', width=90, anchor="center")
        self.task_tree.column('Status', width=120, anchor="center")
        self.task_tree.column('Created', width=120, anchor="center")
        self.task_tree.column('Completed', width=120, anchor="center")

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.task_tree.yview)
        self.task_tree.configure(yscrollcommand=scrollbar.set)

        self.task_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Buttons frame
        buttons_frame = ttk.Frame(self.root)
        buttons_frame.pack(pady=10)

        ttk.Button(buttons_frame, text="✅ Complete", command=self.mark_complete).pack(side=tk.LEFT, padx=6)
        ttk.Button(buttons_frame, text="✏️ Edit", command=self.edit_task).pack(side=tk.LEFT, padx=6)
        ttk.Button(buttons_frame, text="🗑️ Delete", command=self.delete_task).pack(side=tk.LEFT, padx=6)
        ttk.Button(buttons_frame, text="🧹 Clear Completed", command=self.clear_completed).pack(side=tk.LEFT, padx=6)

        # Bottom frame
        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(fill=tk.X, pady=10, padx=20)

        self.filter_var = tk.StringVar(value="All")
        filter_combo = ttk.Combobox(bottom_frame, textvariable=self.filter_var,
                                   values=["All", "Pending", "Completed", "High Priority",
                                           "Medium Priority", "Low Priority"],
                                   state="readonly", width=18)
        filter_combo.pack(side=tk.LEFT, padx=5)
        filter_combo.bind('<<ComboboxSelected>>', lambda e: self.refresh_task_list())

        # Progress bar
        self.progress = ttk.Progressbar(bottom_frame, orient="horizontal", length=200, mode="determinate")
        self.progress.pack(side=tk.RIGHT, padx=(0, 10))

        self.stats_label = ttk.Label(bottom_frame, text="Total: 0 | Pending: 0 | Completed: 0",
                                     font=("Segoe UI", 10, "italic"))
        self.stats_label.pack(side=tk.RIGHT, padx=(0, 20))

    def add_task(self):
        text = self.task_entry.get().strip()
        if not text:
            self.update_status("⚠️ Please enter a task!", "red")
            return

        task = {
            'id': len(self.tasks) + 1,
            'description': text,
            'priority': self.priority_var.get(),
            'status': 'Pending',
            'created_date': datetime.now().strftime('%Y-%m-%d'),
            'completed_date': ''
        }
        self.tasks.append(task)
        self.task_entry.delete(0, tk.END)
        self.save_tasks()
        self.refresh_task_list()
        self.update_status("✅ Task added!", "green")

    def mark_complete(self):
        selected = self.task_tree.selection()
        if not selected:
            self.update_status("⚠️ Select a task first!", "red")
            return
        item = self.task_tree.item(selected[0])
        desc = item['values'][0]

        for task in self.tasks:
            if task['description'] == desc:
                task['status'] = 'Completed'
                task['completed_date'] = datetime.now().strftime('%Y-%m-%d')
                break
        self.save_tasks()
        self.refresh_task_list()
        self.update_status("🎉 Task completed!", "green")

    def edit_task(self):
        selected = self.task_tree.selection()
        if not selected:
            self.update_status("⚠️ Select a task to edit!", "red")
            return
        item = self.task_tree.item(selected[0])
        desc = item['values'][0]

        task = next((t for t in self.tasks if t['description'] == desc), None)
        if not task:
            return

        new_desc = simpledialog.askstring("Edit Task", "Enter new description:", initialvalue=desc)
        if new_desc and new_desc.strip():
            task['description'] = new_desc.strip()
            self.save_tasks()
            self.refresh_task_list()
            self.update_status("✏️ Task updated!", "green")

    def delete_task(self):
        selected = self.task_tree.selection()
        if not selected:
            self.update_status("⚠️ Select a task to delete!", "red")
            return
        item = self.task_tree.item(selected[0])
        desc = item['values'][0]

        self.tasks = [t for t in self.tasks if t['description'] != desc]
        self.save_tasks()
        self.refresh_task_list()
        self.update_status("🗑️ Task deleted!", "green")

    def clear_completed(self):
        before = len(self.tasks)
        self.tasks = [t for t in self.tasks if t['status'] != 'Completed']
        cleared = before - len(self.tasks)
        self.save_tasks()
        self.refresh_task_list()
        if cleared > 0:
            self.update_status(f"🧹 Cleared {cleared} task(s)!", "green")
        else:
            self.update_status("ℹ️ No completed tasks!", "blue")

    def refresh_task_list(self):
        for i in self.task_tree.get_children():
            self.task_tree.delete(i)

        search = self.search_var.get().lower()
        filter_val = self.filter_var.get()
        tasks = self.tasks

        if filter_val == "Pending":
            tasks = [t for t in tasks if t['status'] == "Pending"]
        elif filter_val == "Completed":
            tasks = [t for t in tasks if t['status'] == "Completed"]
        elif filter_val.endswith("Priority"):
            pr = filter_val.split()[0]
            tasks = [t for t in tasks if t['priority'] == pr]

        if search:
            tasks = [t for t in tasks if search in t['description'].lower()]

        for t in tasks:
            tags = []
            if t['status'] == "Completed":
                tags.append("completed")
            elif t['priority'] == "High":
                tags.append("high")
            elif t['priority'] == "Medium":
                tags.append("medium")
            else:
                tags.append("low")

            self.task_tree.insert("", tk.END, values=(t['description'], t['priority'],
                                t['status'], t['created_date'], t['completed_date']), tags=tags)

        self.task_tree.tag_configure("completed", foreground="gray")
        self.task_tree.tag_configure("high", foreground="red")
        self.task_tree.tag_configure("medium", foreground="orange")
        self.task_tree.tag_configure("low", foreground="green")

        self.update_statistics()

    def update_statistics(self):
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t['status'] == "Completed")
        pending = total - completed
        self.stats_label.config(text=f"📊 Total: {total} | Pending: {pending} | Completed: {completed}")
        self.progress["maximum"] = total if total else 1
        self.progress["value"] = completed

    def update_status(self, msg, color="black"):
        self.stats_label.config(text=msg, foreground=color)
        self.root.after(3000, self.update_statistics)

    def save_tasks(self):
        with open(self.data_file, "w") as f:
            json.dump(self.tasks, f, indent=2)

    def load_tasks(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                try:
                    self.tasks = json.load(f)
                except:
                    self.tasks = []

def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
