"""
Classes to manage the feed
"""

import html
import datetime

import sqlalchemy
import markdown


from .meta import Base



class Post(Base):
    """
    Main Class for a post
    """

    __tablename__ = "post"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key = True)

    #FK to the module
    module = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("module.id"))

    parent = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('post.id'))

    #Foreign Key to whoever wrote it
    author = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id")) 

    title = sqlalchemy.Column(sqlalchemy.Text)

    content = sqlalchemy.Column(sqlalchemy.Text)

    date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.utcnow)

    # ---------- RELATIONSHIPS --------
    #Back ref so we can get the user if we want them
    theAuthor = sqlalchemy.orm.relationship("User")
    #Dammit cant make this part work...
    replies = sqlalchemy.orm.relationship("Post", remote_side=[parent])

    
    def __init__(self, author, content, module=None, parent=None, title=None):
        self.module = module
        self.author = author
        self.content = content
        self.title = title
        self.parent = parent


    def renderMarkdown(self):
        """
        Render the Markdown for this post
        """

        #Clean the data up
        sanitised = html.escape(self.content)
        htmloutput = markdown.markdown(sanitised)
        return htmloutput

    def getDate(self):
        """
        Do some nice (ish) date formatting
        """

        return self.date.strftime("%c")
        
    def getReplies(self, request):
        """
        Get the replies for this post
        Kludge for the moment
        """
        replies = request.dbsession.query(Post).filter_by(parent = self.id)
        return replies.all()
        

    
# class Response(Base):
#     """
#     And a response to a post
#     """

#     __tablename__ = "response"

#     id = sqlalchemy.Column(sqlalchemy.Integer, primary_key = True)

#     #FK to post
#     postId = sqlalchemy.Column(sqlalchemy.Integer)

#     #Id of Whoever Wrote it
#     author = sqlalchemy.Column(sqlalchemy.Integer)

#     #Text Content
#     content = sqlalchemy.Column(sqlalchemy.Text)
    
