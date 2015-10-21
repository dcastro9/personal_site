from google.appengine.ext import ndb

from jinjaHandler import JinjaTemplateHandler

class Index(JinjaTemplateHandler):
    def get(self):
        return self.render("index.html")