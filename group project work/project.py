class Project():
    def __init__(self, project_id, name, project_description):
        self.project_id = project_id
        self.name = name
        self.project_description = project_description

        def to_dict(self):
            return{ 
                'id':self.project_id,
                'name': self.name,
                'description':self.project_description
                } 
        

