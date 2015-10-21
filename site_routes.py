import webapp2

from routes import index

application = webapp2.WSGIApplication([
    ('/', index.Index),
], debug=True)