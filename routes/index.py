from google.appengine.ext import ndb

from admin import CheckLogin

from models import Project

class Index(CheckLogin):
    def get(self):
        # Render three projects for front page.
        projects = Project.query().order(-Project.modified).fetch(limit = 3)
        self.templateVars['projects'] = projects
        return self.render("index.html")