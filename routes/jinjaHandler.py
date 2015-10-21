import jinja2
import os
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'views')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class JinjaTemplateHandler(webapp2.RequestHandler):
    def __init__(self, req, res):
        super(JinjaTemplateHandler, self).__init__(req, res)
        self.templateVars = {}

    def render(self, templateName):
        template = JINJA_ENVIRONMENT.get_template(templateName)
        return self.response.write(template.render(self.templateVars))
