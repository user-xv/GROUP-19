import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3

class Project:
    def __init__(self, project_id=None, name="", description=""):
        self.project_id = project_id; self.name = name; self.description = description

class Ticket:
    def __init__(self, ticket_id=None, project_id=None, title="", status="To Do", severity="Medium", assignee="Unassigned"):
        self.ticket_id = ticket_id; self.project_id = project_id; self.title = title
        self.status = status; self.severity = severity; self.assignee = assignee

class DatabaseManager:
    def __init__(self, db_name="bug_tracker.db"): pass
    def get_project_by_id(self, project_id): return Project(project_id, "Sample Project", "Sample Description")
    def add_ticket(self, ticket): ticket.ticket_id = 999; return ticket
    def update_ticket(self, ticket): return True
    def delete_ticket(self, ticket_id): return True
    def get_tickets_by_project(self, project_id, status_filter=None, severity_filter=None, search_term=None): return []

class BugTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__(); self.title("Mini JIRA Clone"); self.geometry("800x600")
        self.db = DatabaseManager(); self.current_project = None
        self.create_widgets()
        self.project_listbox = tk.Listbox(self, height=1)
        self.project_info_label = tk.Label(self)
        self.status_filter_var = tk.StringVar(self, value="All")
        self.severity_filter_var = tk.StringVar(self, value="All")
        self.search_entry = tk.Entry(self)
        self.load_tickets() # TM4 relies on this to display tickets

    def _get_id_from_listbox_item(self, s):
        try:
            start_idx = s.rfind("(ID: "); end_idx = s.rfind(")")
            if start_idx == -1 or end_idx == -1: return None
            return int(s[start_idx + 5:end_idx])
        except (ValueError, IndexError): print(f"Warning: Failed to parse ID from '{s}'"); return None

    def load_tickets(self, *args):
        self.ticket_listbox.delete(0, tk.END)
        if self.current_project:
            tickets = self.db.get_tickets_by_project(
                self.current_project.project_id, self.status_filter_var.get(),
                self.severity_filter_var.get(), self.search_entry.get().strip()
            )
            for t in tickets: self.ticket_listbox.insert(tk.END, f"{t.title} (ID: {t.ticket_id}) - Status: {t.status}, Severity: {t.severity}, Assignee: {t.assignee}")
        else: self.ticket_listbox.insert(tk.END, "No project selected to display tickets.")

    def create_widgets(self):
        self.ticket_frame = tk.LabelFrame(self, text="Tickets for Selected Project", padx=10, pady=10)
        self.ticket_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        self.project_info_label = tk.Label(self.ticket_frame, text="Select a project to view tickets.", wraplength=400, justify="left")
        self.project_info_label.pack(pady=5)
        filter_frame = tk.Frame(self.ticket_frame); filter_frame.pack(fill="x", pady=5)
        tk.Label(filter_frame, text="Status:").pack(side="left", padx=5)
        self.status_filter_var = tk.StringVar(self, value="All"); tk.OptionMenu(filter_frame, self.status_filter_var, "All").pack(side="left", padx=5)
        tk.Label(filter_frame, text="Severity:").pack(side="left", padx=5)
        self.severity_filter_var = tk.StringVar(self, value="All"); tk.OptionMenu(filter_frame, self.severity_filter_var, "All").pack(side="left", padx=5)
        tk.Label(filter_frame, text="Search:").pack(side="left", padx=5)
        self.search_entry = tk.Entry(filter_frame, width=20); self.search_entry.pack(side="left", padx=5)
        tk.Button(filter_frame, text="Search").pack(side="left", padx=5)
        self.ticket_listbox = tk.Listbox(self.ticket_frame, height=15); self.ticket_listbox.pack(fill="both", expand=True, pady=5)
        self.ticket_listbox.bind("<<ListboxSelect>>", self.on_ticket_select)
        self.add_ticket_button = tk.Button(self.ticket_frame, text="Add New Ticket", command=self.add_ticket); self.add_ticket_button.pack(fill="x", pady=2)
        self.edit_ticket_button = tk.Button(self.ticket_frame, text="Edit Selected Ticket", command=self.edit_ticket); self.edit_ticket_button.pack(fill="x", pady=2)
        self.delete_ticket_button = tk.Button(self.ticket_frame, text="Delete Selected Ticket", command=self.delete_ticket); self.delete_ticket_button.pack(fill="x", pady=2)

    def add_ticket(self):
        if not self.current_project: messagebox.showwarning("No Project", "Select a project."); return
        dialog = TicketDialog(self, "Add New Ticket")
        if dialog.result:
            title, status, severity, assignee = dialog.result
            new_ticket = Ticket(project_id=self.current_project.project_id, title=title, status=status, severity=severity, assignee=assignee)
            if self.db.add_ticket(new_ticket): self.load_tickets(); messagebox.showinfo("Success", "Ticket added!")
            else: messagebox.showerror("Error", "Failed to add ticket.")

    def edit_ticket(self):
        selected_idx = self.ticket_listbox.curselection()
        if not selected_idx: messagebox.showwarning("No Ticket", "Select a ticket."); return
        item = self.ticket_listbox.get(selected_idx[0])
        ticket_id = self._get_id_from_listbox_item(item)
        if ticket_id is None: messagebox.showerror("Error", "Invalid ticket ID."); return
        
        all_tickets = self.db.get_tickets_by_project(self.current_project.project_id)
        selected_ticket = next((t for t in all_tickets if t.ticket_id == ticket_id), None)

        if selected_ticket:
            dialog = TicketDialog(self, "Edit Ticket", ticket_data=selected_ticket)
            if dialog.result:
                title, status, severity, assignee = dialog.result
                selected_ticket.title = title; selected_ticket.status = status
                selected_ticket.severity = severity; selected_ticket.assignee = assignee
                if self.db.update_ticket(selected_ticket): self.load_tickets(); messagebox.showinfo("Success", "Ticket updated!")
                else: messagebox.showerror("Error", "Failed to update ticket.")
        else: messagebox.showerror("Error", "Ticket not found.")

    def delete_ticket(self):
        selected_idx = self.ticket_listbox.curselection()
        if not selected_idx: messagebox.showwarning("No Ticket", "Select a ticket."); return
        item = self.ticket_listbox.get(selected_idx[0])
        ticket_id = self._get_id_from_listbox_item(item)
        if ticket_id is None: messagebox.showerror("Error", "Invalid ticket ID."); return

        if messagebox.askyesno("Confirm Delete", f"Delete '{item}'?"):
            if self.db.delete_ticket(ticket_id): self.load_tickets(); messagebox.showinfo("Deleted", "Ticket deleted!")
            else: messagebox.showerror("Error", "Failed to delete ticket.")

    def on_ticket_select(self, event=None):
        selected_idx = self.ticket_listbox.curselection()
        if selected_idx: print(f"Selected: {self.ticket_listbox.get(selected_idx[0])}")

class TicketDialog(simpledialog.Dialog):
    def __init__(self, parent, title, ticket_data=None):
        self.ticket_data = ticket_data; super().__init__(parent, title)

    def body(self, master):
        tk.Label(master, text="Title:").grid(row=0, sticky="w")
        tk.Label(master, text="Status:").grid(row=1, sticky="w")
        tk.Label(master, text="Severity:").grid(row=2, sticky="w")
        tk.Label(master, text="Assignee:").grid(row=3, sticky="w")

        self.title_entry = tk.Entry(master, width=40); self.status_var = tk.StringVar(master)
        self.status_options = ["To Do", "In Progress", "Done"]; self.status_menu = tk.OptionMenu(master, self.status_var, *self.status_options)
        self.severity_var = tk.StringVar(master); self.severity_options = ["Low", "Medium", "High"]
        self.severity_menu = tk.OptionMenu(master, self.severity_var, *self.severity_options)
        self.assignee_entry = tk.Entry(master, width=40)

        self.title_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.status_menu.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.severity_menu.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.assignee_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        if self.ticket_data:
            self.title_entry.insert(0, self.ticket_data.title); self.status_var.set(self.ticket_data.status)
            self.severity_var.set(self.ticket_data.severity); self.assignee_entry.insert(0, self.ticket_data.assignee)
        else:
            self.status_var.set(self.status_options[0]); self.severity_var.set(self.severity_options[1]); self.assignee_entry.insert(0, "Unassigned")
        return self.title_entry

    def apply(self):
        title = self.title_entry.get().strip(); status = self.status_var.get()
        severity = self.severity_var.get(); assignee = self.assignee_entry.get().strip()
        if not title: messagebox.showwarning("Input Error", "Title needed."); self.result = None; return
        self.result = (title, status, severity, assignee)