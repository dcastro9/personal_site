import logging
import re
import urllib2

from datetime import datetime
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.api import users
from jinjaHandler import JinjaTemplateHandler


from models import Author
from models import Conference
from models import Content
from models import Institution
from models import Publication
from models import Project
from models import Tag
from models import User

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

        self.templateVars['institutions'] = Institution.query().fetch()
        self.templateVars['authors'] = Author.query().fetch()
        self.templateVars['conferences'] = Conference.query().fetch()
        self.templateVars['publications'] = Publication.query().fetch()
        self.templateVars['contents'] = Content.query().fetch()
        return self.render("admin.html")

    def post(self):
        if not self.user.administrator:
            return webapp2.redirect('/')
        
        mode = self.request.POST['mode']

        if mode == '0':
            # Institution
            institution = Institution(name = self.request.POST['name'],
                                      website = self.request.POST['website'])
            institution.put()
        elif mode == '1':
            thumbnail_url = self.request.POST['thumbnail']
            try:
                content = urllib2.urlopen(thumbnail_url)
                image = content.read()
            except urllib2.HTTPError:
                logging.warning("URL: " + thumbnail_url + "was not found.")
                image = ''

            institution = ndb.Key(urlsafe = self.request.POST['institution'])

            author = Author(name = self.request.POST['name'],
                            website = self.request.POST['website'],
                            thumbnail = image,
                            institution = institution)
            author.put()
        elif mode == '2':    
            # Conference
            conference = Conference(name = self.request.POST['name'],
                                    acronym = self.request.POST['acronym'])
            conference.put()
            pass
        elif mode == '3':    
            # Publication
            date = datetime.strptime(self.request.POST['date'], '%Y-%m-%d')

            # A bit messy, does author order
            authors = self.request.params.getall('authors')
            idx = 0
            author_order = [int(order_idx) for order_idx in 
                self.request.POST['order'].split(",")]
            ordered_authors = []
            for author_idx in range(len(authors)):
                ordered_authors.append(ndb.Key(
                    urlsafe = authors[author_order[author_idx] - 1]))

            conference = ndb.Key(urlsafe = self.request.POST['conference'])

            pdf_image_url = self.request.POST['pdfimage']
            image = ''
            if pdf_image_url:
                try:
                    content = urllib2.urlopen(pdf_image_url)
                    image = content.read()
                except urllib2.HTTPError:
                    logging.warning("URL: " + pdf_image_url + "was not found.")

            publication = Publication(title = self.request.POST['title'],
                                      abstract = self.request.POST['abstract'],
                                      date = date,
                                      authors = ordered_authors,
                                      citation = self.request.POST['citation'],
                                      conference = conference,
                                      pdf = self.request.POST['pdf'],
                                      pdf_image = image,
                                      arxiv_link = self.request.POST['arxiv'],
                                      project_page = self.request.POST['projectpage'])
            publication.put()
        elif mode == '4':    
            # Content
            content = Content(name = self.request.POST['name'],
                              content = self.request.POST['content'])
            content.put()
        elif mode == '5':
            # Project
            authors = []
            for author in self.request.params.getall('authors'):
                authors.append(ndb.Key(urlsafe = author))

            image_url = self.request.POST['image']
            if image_url:
                try:
                    content = urllib2.urlopen(image_url)
                    image = content.read()
                except urllib2.HTTPError:
                    logging.warning("URL: " + image_url + "was not found.")
                    image = ''
            else:
                image = ''

            publications = []
            for publication in self.request.params.getall('publications'):
                publications.append(ndb.Key(urlsafe = publication))

            contents = []
            for content in self.request.params.getall('contents'):
                contents.append(ndb.Key(urlsafe = content))

            tags = []
            for tag in self.request.POST['tags'].split(","):
                # Try to find tag.
                stripped_tag = tag.strip()
                query = Tag.query(Tag.name == stripped_tag)
                if query.count() == 1:
                    query_tag = query.get(keys_only = True)
                    tags.append(query_tag)
                elif query.count() == 0:
                    query_tag = Tag(name = stripped_tag)
                    tags.append(query_tag.put())
                else:
                    logging.error("Tag count > 1 | < 0 (%s)." % stripped_tag)

            project = Project(title = self.request.POST['title'],
                              description = self.request.POST['description'],
                              authors = authors,
                              image = image,
                              publications = publications,
                              extra_content = contents,
                              tags = tags)
            project.put()
        return self.get()
