import webapp2

from routes import index, admin, project

application = webapp2.WSGIApplication([
    ('/', index.Index),
    ('/admin', admin.Admin),
    #webapp2.Route(r'/projects/<project_id>',
    #              handler=projects.Project),
], debug=True)