"""
Create a demoonstration Database
"""

import argparse
import sys

import logging
log = logging.getLogger("Setup")
log.setLevel(logging.DEBUG)
#logging.basicConfig(level=logging.DEBUG)

from pyramid.paster import bootstrap, setup_logging
from sqlalchemy.exc import OperationalError

from .. import models


def createUsers(dbsession):
    """
    Create a set of users

    We create two example users

      - Teacher. Assigned to both modules
      - Student. Assigned to both modules

    @return (teacher, student)
    """

    log.info("Creating Users")
    teacher = dbsession.query(models.User).filter_by(name = "teacher").first()
    if not teacher:
        log.debug("Creating Teacher")
        teacher = models.User(name="teacher", email="teacher@coventry.ac.uk", role = models.TEACHER)
        dbsession.add(teacher)
        
    teacher.setPassword("teacher")
    

    student = dbsession.query(models.User).filter_by(name = "student").first()
    if not student:
        log.debug("Creating Student")
        student = models.User(name="student", email="student@coventry.ac.uk", role = models.STUDENT)
        dbsession.add(student)
    student.setPassword("student")
        

    return teacher, student

def createModules(dbsession):
    """
    We also create a couple of example modules
    """

    log.info("Creating Modules")

    security = dbsession.query(models.Module).filter_by(code="6005-CEM").first()
    if not security:
        log.debug("Create Security Module")
        security = models.Module(name="Security", code="6005-CEM")
        dbsession.add(security)

    hacking = dbsession.query(models.Module).filter_by(code="1337-CEM").first()
    if not hacking:
        log.debug("Create Hacking Module")
        hacking = models.Module(name="HaX0ring", code="1337-CEM")        
        dbsession.add(hacking)
    
    #This should be hidden from the student
    hidden = dbsession.query(models.Module).filter_by(code="404-Module").first()
    if not hidden:
        log.debug("Create Hidden (From Student) Module")
        hidden = models.Module(name="Not 4 Students", code="404-Module")        
        dbsession.add(hidden)


    return security, hacking

def setupRoles(dbsession):
    """
    Setup some roles for our existing users
    """

    log.debug("Setting up roles")
    #Admin gets everything So we dont need to worry there

    #Assign the TEacher to the Security Module
    security = dbsession.query(models.Module).filter_by(code="6005-CEM").first()
    hacking = dbsession.query(models.Module).filter_by(code="1337-CEM").first()
    notfound = dbsession.query(models.Module).filter_by(code="404-Module").first()

    teacher = dbsession.query(models.User).filter_by(name = "teacher").first()
    student = dbsession.query(models.User).filter_by(name = "student").first()

    log.debug("Modules for the Teacher")
    log.debug(teacher.modules)
    for item in [security, hacking, notfound]:
        if item not in teacher.modules:
            log.debug("Adding {0} To Teacher Modules".format(item.name))
            teacher.modules.append(item)

    log.debug("Modules for the Student")
    log.debug(student.modules)
    for item in [security, hacking]:
        if item not in student.modules:
            log.debug("Adding {0} To Student Modules".format(item.name))
            student.modules.append(item)
    

def setupPosts(dbsession):
    """
    Create some example posts (and replys) For the 6005-CEM module
    """

    log.info("Creating Posts")
    #Get the module itself
    security = dbsession.query(models.Module).filter_by(name="Security").first()

    if security is None:
        log.warning("FATAL ERROR: No Security Module Found")
        sys.exit(0)

    admin = dbsession.query(models.User).filter_by(name="admin").first()
    teacher = dbsession.query(models.User).filter_by(name="teacher").first()
    student = dbsession.query(models.User).filter_by(name="student").first()

    #Otherwise create our posts
    firstpost = dbsession.query(models.Post).filter_by(title="Welcome").first()

    if not firstpost:
        log.debug("Creating first post")
        firstpost = models.Post(author=admin.id,
                                content = "## WELCOME TO THE COURSE\n  A Post by the Admin User",
                                module = security.id,
                                title = "Welcome"
            )
        dbsession.add(firstpost)

    #And a more Markdowny post
    postText = """
# Main Heading

This is testing a post again

## Sub Heading

We have sub Headings here

## Lists

  - A List Item
  - Another List Item
  - A Final List Item
"""

    secondPost = dbsession.query(models.Post).filter_by(title="Testing Post for Text").first()
    
    if secondPost is None:

        secondPost = models.Post(teacher.id,
                                 content = postText,
                                 module = security.id,
                                 title = "Testing Post for Text"
        )
        dbsession.add(secondPost)

    dbsession.flush()

    if not secondPost.replies:
        log.debug("Adding some replies")
        #if not secondPost.replies:
        replyOne = models.Post(student.id,
                               content = "Reply to the post",
                               parent = secondPost.id)

        dbsession.add(replyOne)

        replyTwo = models.Post(teacher.id,
                               content = "A Second reply to the post.  ```def testing()``` Markdown?",
                               parent = secondPost.id)

    
        dbsession.add(replyTwo)


    log.debug("Check: repies")
    log.debug(secondPost.replies)
                            
        
def createModuleItems(dbsession):
    """
    Create some items for the modules
    """
    log.debug("Creating Module Content")
    #Navidation First

    security = dbsession.query(models.Module).filter_by(name="Security").first()

    for item in ["First Topic", "Second Topic", "Third Topic"]:
        log.debug("\tChecking topic {0}".format(item))
        theTopic = models.MenuItem(moduleId = security.id, text= item)
        if theTopic in security.navmenu:
            log.debug("\tTopic Exists")
        else:
            log.debug("\tCreate Topic")
            security.navmenu.append(theTopic)

    #And somehting for the Other
    for item in ["1337-CEM", "404-Module"]:
        log.debug("Adding Itesm to {0}".format(item))
        theModule = dbsession.query(models.Module).filter_by(code=item).first()
        theTopic = models.MenuItem(moduleId = theModule.id, text="Example Text")
        if theTopic in theModule.navmenu:
            log.debug("\tTopic Exists")
        else:
            log.debug("\tCreate Topic")
            theModule.navmenu.append(theTopic)

def createModulePages(dbsession):
    """And Create Some Pages for the Modules"""
    log.debug("Creating Module Pages")

    security = dbsession.query(models.Module).filter_by(name="Security").first()

    pageText = """
# REPLACE: An Example Page Content

This is content for **REPLACE**

This is exmaple page content.  Isn't it great

## Sub Headings Exist
     
  - As
  - Do 
  - Lists

## Fancy Code Blocks also

``` python
def hello(person):
    print(f"Hello {person}")

if __name__ == "__main__":
    hello("Dan")
```

"""
    
    secondText = """
# Second Text Example

This is another example for REPLACE

## Numbered Lists

  1. Uno
  1. Dos
  1. Tres

## Notes

!!! note
    You should note that the title will be automatically capitalized.

## Tables

| Col One | Col 2 |
| ------- | ----- |
| Foo     | Bar   |
"""




    for item in ["First Topic", "Second Topic", "Third Topic"]:
        #Add this to the First Menu Item
        menuItem = dbsession.query(models.MenuItem).filter_by(moduleId = security.id,  text=item).first()
        if not menuItem:
            log.warning("Menuitem expected but none found")
            sys.exit(0)

        for title in ["Example Page {0}".format(item), "Second Example Page {0}".format(item)]:
            if title.startswith("Example"):
                pageText = pageText.replace("REPLACE", item)
            else:
                pageText = secondText.replace("REPLACE", item)
            examplePage = models.Article(moduleId=menuItem.id, title=title, text=pageText)
            if examplePage not in menuItem.articles:
                log.debug("\tCreate New Page")
                menuItem.articles.append(examplePage)
            else:
                idx = menuItem.articles.index(examplePage)
                log.debug("\tPage Exsits at {0}".format(idx))
                #And update the text if needed
                menuItem.articles[idx].text = pageText
    

    otherText = """
# Text for another module

Placeholder text for REPLACE
"""

    #And Examples for all other modules
    for module in ["1337-CEM", "404-Module"]:
        log.debug("Adding Content to {0}".format(item))
        theModule = dbsession.query(models.Module).filter_by(code=module).first()
        menuItem = dbsession.query(models.MenuItem).filter_by(moduleId = theModule.id).first()
        
        pageText = otherText.replace("REPLACE", theModule.name)
        examplePage = models.Article(moduleId = menuItem.id, title="Example", text=pageText)
        if examplePage not in menuItem.articles:
            log.debug("\tCreate Page")
            menuItem.articles.append(examplePage)
        else:
            log.debug("\tPage Exists")
            #Upadte Text
            idx = menuItem.articles.index(examplePage)
            menuItem.articles[idx].text = pageText

def createStudents(dbsession):
    
    userlist = ["Ryan SMITH",
                "Amal PATERSON",
                "Tegan GRAY",
                "Temple HENDERSON",
                "Ren HENDERSON",
                "Amani ROSS",
                "Shannon MACDONALD",
                "Shelley MITCHELL",
                "Imani WILSON",
                "Kary TAYLOR",
                "Rin ROSS",
                "Chadi BROWN",
                "Jo THOMSON",
                "Rei MCDONALD",
                "Shane ROBERTSON",
                "Mitsuki KERR",
                "Cocky YOUNG",
                "Adar MILLER",
                "Demy STEWART",
                "Mikoto FRASER",
                "Cocky MURRAY",
                "Lane SMITH",
                "Sam HAMILTON",
                "Taylor MACDONALD"]
    
    security = dbsession.query(models.Module).filter_by(code="6005-CEM").first()
    hacking = dbsession.query(models.Module).filter_by(code="1337-CEM").first()
    notfound = dbsession.query(models.Module).filter_by(code="404-Module").first()
    
    #And Add the little buggers
    idx = 0
    for item in userlist:
        name = item.lower()
        parts = name.split()
        email = "{0}.{1}@coventry.ac.uk".format(parts[0][0], parts[1])
        #log.debug("Create Student {0} With Email {1}".format(name, email))
        student = dbsession.query(models.User).filter_by(name = name).first()
        if not student:
            log.debug("Creating {0}".format(student))
            student = models.User(name=name, email=email, role = models.STUDENT)
            dbsession.add(student)
        #As its a demo we dont care about default passwords
        student.setPassword("student")

        #Every student is part of secuity
        if security not in student.modules:
            student.modules.append(security)

        #And Evey 3rd one in hacking
        if idx % 3 == 0:
            if hacking not in student.modules:

                student.modules.append(hacking)
            
def setup_models(dbsession):
    """
    Add or update models / fixtures in the database.

    """
    
    #And populate each part of the Thing
    createUsers(dbsession)
    createModules(dbsession)
    setupPosts(dbsession)
    setupRoles(dbsession)    
    createModuleItems(dbsession)
    createModulePages(dbsession)
    createStudents(dbsession)

def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'config_uri',
        help='Configuration file, e.g., development.ini',
    )
    return parser.parse_args(argv[1:])


def main(argv=sys.argv):
    args = parse_args(argv)
    setup_logging(args.config_uri)
    env = bootstrap(args.config_uri)

    try:
        with env['request'].tm:
            dbsession = env['request'].dbsession
            setup_models(dbsession)
    except OperationalError:
        print('''
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to initialize your database tables with `alembic`.
    Check your README.txt for description and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.
            ''')
