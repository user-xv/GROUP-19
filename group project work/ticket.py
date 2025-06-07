class Ticket():
    Statuses = {"To Do","In Progress", "Done"}
    Severities = {"Low", "Medium", "High"}

    def __init__(self, ticket_id, project_id, title, status, severity, assignee):
        self.ticket_id = ticket_id
        self.project_id = project_id 
        self.title = title
        self.status = status
        self.severity = severity
        self.assignee = assignee

        def update_staus(self, new_status):
           if new_status in self.Stauses:
            self.status = new_status

        def update_severity(self, new_severity):
           if new_severity in self.Severities:
            self.severity = new_severity

        def reassign_to(self, new_person):
            self.assignee = new_person

        def to_dict(self):
            return{ 
                 'ticket_id':self.ticket_id,
                 'project_id':self.project_id,
                 'title':self.title,
                 'status':self.status,
                 'severity':self.severity,
                 'assignee':self.assignee
                } 