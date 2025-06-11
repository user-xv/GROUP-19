import tkinter as tk
from tkinter import ttk, messagebox

class AddProjectDialog(tk.Toplevel):
    """
    A dialog window for adding a new project.
    It appears on top of the main application window.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Add New Project")
        self.geometry("350x200")
        self.transient(parent) 
        self.grab_set() 

        self.project_data = None

        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Project Name:").pack(pady=5, anchor="w")
        self.name_entry = ttk.Entry(main_frame, width=40)
        self.name_entry.pack(fill=tk.X)
        self.name_entry.focus_set() 

        ttk.Label(main_frame, text="Project Description:").pack(pady=5, anchor="w")
        self.desc_entry = tk.Text(main_frame, height=4)
        self.desc_entry.pack(fill=tk.X)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=5, fill=tk.X)

        ttk.Button(button_frame, text="Cancel", command=self.destroy).pack(side=tk.RIGHT, padx=(10,5))
        ttk.Button(button_frame, text="Create Project", command=self.on_create).pack(side=tk.RIGHT)

    def on_create(self):
        """
        Handles the logic when the 'Create Project' button is clicked.
        Validates input and stores the data.
        """
        name = self.name_entry.get().strip()
        description = self.desc_entry.get("1.0", tk.END).strip()

        if not name:
            messagebox.showerror("Validation Error", "Project Name cannot be empty.", parent=self)
            return

        self.project_data = {"name": name, "description": description, "tickets": []}
        self.destroy() 
class ProjectManagementApp:
    """
    The main application class for the Project Management GUI.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Team Member 3: Project Management Page")
        self.root.geometry("500x400")
        self.root.minsize(400, 300)

       
    

        self.setup_ui()
        self.update_project_list()

    def setup_ui(self):
        """Sets up the main user interface widgets."""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(header_frame, text="All Projects", font=("Arial", 16, "bold")).pack(side=tk.LEFT)
        ttk.Button(header_frame, text="+ Add New Project", command=self.open_add_project_dialog).pack(side=tk.RIGHT)

        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)

        self.project_listbox = tk.Listbox(list_frame, font=("Arial", 12), selectbackground="#0078D7", selectforeground="white")
        self.project_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.project_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.project_listbox.config(yscrollcommand=scrollbar.set)
        
        self.project_listbox.bind('<<ListboxSelect>>', self.on_project_select)

        self.view_tickets_button = ttk.Button(main_frame, text="Select a Project to View Tickets", command=self.view_project_tickets, state=tk.DISABLED)
        self.view_tickets_button.pack(pady=10, fill=tk.X)

    def update_project_list(self):
        """Clears and repopulates the project listbox from the self.projects data."""
        self.project_listbox.delete(0, tk.END)
        

    def open_add_project_dialog(self):
        """Opens the dialog for adding a new project."""
        dialog = AddProjectDialog(self.root)
        self.root.wait_window(dialog) 

        if dialog.project_data:
            self.projects.append(dialog.project_data)
            self.update_project_list()
            messagebox.showinfo("Success", f"Project '{dialog.project_data['name']}' was created successfully.")

    def on_project_select(self, event=None):
        """Enables the 'View Tickets' button when a project is selected."""
        if self.project_listbox.curselection():
            self.view_tickets_button.config(state=tk.NORMAL, text="View Tickets for Selected Project")
        else:
            self.view_tickets_button.config(state=tk.DISABLED, text="Select a Project to View Tickets")

    def view_project_tickets(self):
        """
        Simulates navigating to the Ticket Management page for the selected project.
        This is the hand-off point to Team Member 4's module.
        """
        selected_indices = self.project_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("No Selection", "Please select a project from the list first.")
            return

        selected_index = selected_indices[0]
        project = self.projects[selected_index]
        
        
        messagebox.showinfo(
            "Navigation", 
            f"HANDOFF TO TEAM 4:\n\nOpening the Ticket Management page for project:\n'{project['name']}'"
        )


if __name__ == "__main__":

    root = tk.Tk()
    app = ProjectManagementApp(root)
    root.mainloop()