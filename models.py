from google.appengine.ext import ndb

class Institution(ndb.Model):
    """ Represents the institution of an author. """
    name = ndb.StringProperty()
    website = ndb.StringProperty()

class Author(ndb.Model):
    """ Represents an author who has worked on a project or publication. """
    name = ndb.StringProperty()
    thumbnail = ndb.BlobProperty() # TODO(dcastro): Admin page?
    website = ndb.StringProperty()
    institution = ndb.KeyProperty(kind = Institution)

class Conference(ndb.Model):
    """ Represents a conference.

    Do not add a year, as that is identified by the date of publication.

    """
    name = ndb.StringProperty()

class Publication(ndb.Model):
    """ Represents a publication that has been conducted as part of a project.

    This is assumed to be a part of a project. Publications will not get their
    own page but rather have a link to the actual project page. Maintains the
    consistency for each project page (having two pages that are near identical
    for one publication is silly).

    """
    title = ndb.StringProperty()
    abstract = ndb.StringProperty()
    date = ndb.DateProperty()
    authors = ndb.KeyProperty(kind = Author, repeated = True)
    citation = ndb.StringProperty()
    conference = ndb.KeyProperty(kind = Conference)
    pdf = ndb.StringProperty() # URL
    pdf_image = ndb.StringProperty()
    arxiv_link = ndb.StringProperty()
    project_page = ndb.StringProperty() # URL

class Content(ndb.Model):
    """ Created for random HTML content we wish to inject into a project.

    The HTML is injected into the project page as a repeated property from
    project (unescaped).

    """
    title = ndb.StringProperty()
    content = ndb.StringProperty()


class Project(ndb.Model):
    """ Project that I have undergone, am undergoing, will undergo, etc.

    This includes publications for the project, note that publications will be
    rendered as snippets in a project and not as their own page (because their
    own page will be hosted on the CPL sites).

    """
    title = ndb.StringProperty()
    abstract = ndb.StringProperty()
    authors = ndb.KeyProperty(kind = Author, repeated = True)
    paper_image = ndb.StringProperty()

    publications = ndb.KeyProperty(kind = Publication, repeated = True)
    extra_content = ndb.KeyProperty(kind = Content, repeated = True)

    @property
    def published(self):
        return len(self.publications) > 0