from google.appengine.ext import ndb

from admin import CheckLogin

class Project(CheckLogin):
    def get(self, project_id):
    	project = Project.query(Project.id == project_id).get()
        return self.render("project.html")