import tkinter as tk
from tkinter import ttk
from Database import search_tickets_by_title, get_ticket_by_status

class FilterSearchFrame(tk.LabelFrame):
    def __init__(self, parent, update_callback, get_project_id_callback):
        super().__init__(parent, text="Search & Filter Tickets")
        self.update_callback = update_callback 
        self.get_project_id = get_project_id_callback  

        # Search by title
        tk.Label(self, text="Search Title:").grid(row=0, column=0, padx=5, pady=5)
        self.search_entry = tk.Entry(self, width=30)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self, text="Search", command=self.search_by_title).grid(row=0, column=2, padx=5, pady=5)

        # Filter by status
        tk.Label(self, text="Status:").grid(row=1, column=0, padx=5, pady=5)
        self.status_var = tk.StringVar()
        self.status_dropdown = ttk.Combobox(self, textvariable=self.status_var, values=["All", "To Do", "In Progress", "Done"], state="readonly")
        self.status_dropdown.grid(row=1, column=1, padx=5, pady=5)
        self.status_dropdown.current(0)

        # Filter by severity
        tk.Label(self, text="Severity:").grid(row=2, column=0, padx=5, pady=5)
        self.severity_var = tk.StringVar()
        self.severity_dropdown = ttk.Combobox(self, textvariable=self.severity_var, values=["All", "Low", "Medium", "High"], state="readonly")
        self.severity_dropdown.grid(row=2, column=1, padx=5, pady=5)
        self.severity_dropdown.current(0)

        # Filter button
        tk.Button(self, text="Apply Filter", command=self.filter_tickets).grid(row=3, column=0, columnspan=3, pady=10)

    def search_by_title(self):
        keyword = self.search_entry.get().strip()
        if keyword:
            results = search_tickets_by_title(keyword)
            self.update_callback(results)

    def filter_tickets(self):
        status = self.status_var.get()
        severity = self.severity_var.get()
        project_id = self.get_project_id()

        if not project_id:
            print("No project selected.")
            return

        # Build dynamic query manually (you may optimize this later)
        import sqlite3
        conn = sqlite3.connect('bug_tracker.db')
        cursor = conn.cursor()

        query = "SELECT * FROM tickets WHERE project_id = ?"
        params = [project_id]

        if status != "All":
            query += " AND status = ?"
            params.append(status)

        if severity != "All":
            query += " AND severity = ?"
            params.append(severity)

        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()

        self.update_callback(results)
