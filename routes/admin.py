import logging
import re

from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.api import users
from jinjaHandler import JinjaTemplateHandler

from models import User
from models import Institution
from models import Author
from models import Conference
from models import Publication
from models import Content
from models import Project

class CheckLogin(JinjaTemplateHandler):
    def dispatch(self):
        # Define temporary variables.
        self.user = users.get_current_user()
        logUrl = ""
        linkText = ""

        if self.user:
            user = User.gql("WHERE email = :1" , self.user.email()).get()
            if not user:
                user = User(email=self.user.email())
                user.put()
            self.user = user
            url = users.create_logout_url(dest_url='/')
            linkText = "Logout"
        else:
            url = users.create_login_url(dest_url="/")
            linkText = "Login"
        self.templateVars['user'] = self.user
        self.templateVars['loginLinkText'] = linkText
        self.templateVars['loginLinkURL'] = url
        
        allowed = [r'^static/*', r'^/$']
        # If the user is logged in, or you are accessing any file in the static
        # directory you allow access.
        if self.user or any(re.match(path, self.request.path)
                            for path in allowed):
            super(CheckLogin, self).dispatch()
        else:
            return webapp2.redirect('/')   

class Admin(CheckLogin):
    def get(self):
        return self.render("admin.html")

    def post(self):
        if not self.user.administrator:
            return webapp2.redirect('/')
        
        mode = self.request.POST['mode']

        if mode == '0':
            # Institution
            pass
        elif mode == '1':    
            # Author
            pass
        elif mode == '2':    
            # Conference
            pass
        elif mode == '3':    
            # Publication
            pass
        elif mode == '4':    
            # Content
            pass
        elif mode == '5':    
            # Project
            pass
        return
