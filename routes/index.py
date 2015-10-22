from google.appengine.ext import ndb

from admin import CheckLogin

class Index(CheckLogin):
    def get(self):
        return self.render("index.html")