import sqlite3

def init_db():
    conn = sqlite3.connect('bug_tracker.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            project_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            project_description TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            status TEXT NOT NULL,
            severity TEXT NOT NULL,
            assignee TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

        
def add_project(name, project_description):
    conn = sqlite3.connect('bug_tracker.db')
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO projects (name, project_description) VALUES (?, ?)",
                   (name, project_description))
    conn.commit()
    conn.close()

def get_projects():
    conn = sqlite3.connect('bug_tracker.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects")
    projects = cursor.fetchall()
    conn.close()
    return projects
    
def add_ticket(project_id, title, status, severity, assignee):
        conn = sqlite3.connect('bug_tracker.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tickets (project_id, title, status, severity, assignee) VALUES (?, ?, ?, ?, ?)",
                       (project_id, title, status, severity, assignee))
        conn.commit()
        conn.close()
        
def get_tickets_by_project(project_id):
    conn = sqlite3.connect('bug_tracker.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets WHERE project_id = ?", (project_id,))
    tickets = cursor.fetchall()
    conn.close()
    return tickets

def update_ticket_status(ticket_id, new_status):
    conn = sqlite3.connect('bug_tracker.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE tickets SET status = ? WHERE ticket_id = ?", (new_status, ticket_id))
    conn.commit()
    conn.close()
    
def delete_project(project_id):
    conn = sqlite3.connect('bug_tracker.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM projects WHERE project_id = ?", (project_id,))
    conn.commit()
    conn.close()
    
def delete_ticket(ticket_id):
    conn = sqlite3.connect('bug_tracker.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tickets WHERE ticket_id = ?", (ticket_id,))
    conn.commit()
    conn.close()
    
def update_ticket_severity(ticket_id, new_severity):
    conn = sqlite3.connect('bug_tracker.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE tickets SET severity = ? WHERE ticket_id = ?", (new_severity, ticket_id))
    conn.commit()
    conn.close()
    
def update_ticket_assignee(ticket_id, new_assignee):
    conn = sqlite3.connect('bug_tracker.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE tickets SET assignee = ? WHERE ticket_id = ?", (new_assignee, ticket_id))
    conn.commit()
    conn.close()
    
def get_ticket_by_status(status):
    conn = sqlite3.connect('bug_tracker.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets WHERE status = ?", (status,))
    tickets = cursor.fetchall()
    conn.close()
    return tickets

def search_tickets_by_title(keyword):
    conn = sqlite3.connect('bug_tracker.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets WHERE title LIKE ?", ('%' + keyword + '%',))
    tickets = cursor.fetchall()
    conn.close()
    return tickets

