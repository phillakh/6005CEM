"""
Class for Modules and Module Related Stuff
"""

import markdown

import sqlalchemy

#Allow articles to have a position
from sqlalchemy.ext.orderinglist import ordering_list


from .meta import Base


class Module(Base):
    """Base Class for Modules"""

    __tablename__ = "module"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key = True)

    #Code
    code = sqlalchemy.Column(sqlalchemy.Text)

    #Title
    name = sqlalchemy.Column(sqlalchemy.Text)

    #Menu Stuff
    navmenu = sqlalchemy.orm.relationship("MenuItem", order_by="MenuItem.position",
                                          collection_class=ordering_list('position'))
    

    def __str__(self):
        return "{0} {1}".format(self.code, self.name)

class MenuItem(Base):
    """
    Store our information in the Menu
    """

    __tablename__ = "menuitem"

    #PK
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key = True)

    #Moudle
    moduleId = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("module.id"))
    
    #If we are in the Tree
    parentId = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("menuitem.id"))

    #Where in the List of objects we are
    position = sqlalchemy.Column(sqlalchemy.Integer)

    #And Text Assosicated with it (It Titles)
    text = sqlalchemy.Column(sqlalchemy.Text)

    articles = sqlalchemy.orm.relationship("Article", order_by="Article.position",
                                          collection_class=ordering_list('position'))


    def __eq__(self, other):
        """
        Basic test for Equality

        This lets us manage the item in the navmenu object
        """

        return (self.moduleId == other.moduleId) and (self.text == other.text)

class Article(Base):
    """
    Base Class to show Module Materials
    """

    __tablename__ = "article"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key = True)

    #TODO:  Rename this to be heading.id 
    moduleId = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("menuitem.id"))

    #Position in the Module
    position = sqlalchemy.Column(sqlalchemy.Integer)

    title = sqlalchemy.Column(sqlalchemy.Text)

    text = sqlalchemy.Column(sqlalchemy.Text)

    def __eq__(self, other):
        """
        Again, simple comparison. for managment
        """

        return (self.moduleId == other.moduleId) and (self.title == other.title)

    def render(self):
        """
        Render Markdown to HTML
        """

        #Loads of Extensitons to enable here.
        htmloutput = markdown.markdown(self.text, extensions=['fenced_code', 'codehilite', 'admonition', 'tables'])
        return htmloutput