import webapp2

from routes import index, admin

application = webapp2.WSGIApplication([
    ('/', index.Index),
    ('/admin', admin.Admin),
], debug=True)