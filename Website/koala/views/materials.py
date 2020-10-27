"""
View Materials
"""
from pyramid.view import view_config
from pyramid.response import Response

from pyramid.httpexceptions import (
    HTTPForbidden,
    HTTPFound,
    HTTPNotFound,
    )

from sqlalchemy.exc import DBAPIError

from .. import models

import logging
log = logging.getLogger("Materials")
log.setLevel(logging.DEBUG)


@view_config(route_name='materials', renderer='../templates/materials.jinja2')
def materials(request):
    user = request.user
    if user is None:
        raise HTTPForbidden

    log.debug(request.matchdict)

    #Module Id
    moduleId = request.matchdict.get('moduleId')
    log.debug("Page for {0}".format(moduleId))
    articleId = request.matchdict.get('pageId')
    log.debug("Get Article {0}".format(articleId))

    thisModule = request.dbsession.query(models.Module).filter_by(id = moduleId).first()
    if thisModule is None:
        raise HTTPNotFound


    if user.role != models.ADMIN:
        #Check if the user can see this page
        if thisModule not in user.modules:
            log.warning("Attempts to view unallocated module")
            raise HTTPNotFound

    #We can also calculate Effective Roles
    effectiveRole = "STUDENT"
    if request.user.role == models.TEACHER:
        #TODO: Downgrade a module if there is a role allocated
        
        effectiveRole = "TEACHER"
    elif request.user.role == models.ADMIN:
        effectiveRole = "TEACHER"    


    #Grab the Current Page
    

    #Code to get the Article for rendering
    theArticle = request.dbsession.query(models.Article).filter_by(id = articleId).first()
    log.debug("Article is {0}".format(theArticle))

    #If We dont have an article, fall back to the first one
    if theArticle is None:
        menuIds = [x.id for x in thisModule.navmenu]
        log.debug("Menuitem Ids {0}".format(menuIds))
        theArticle = request.dbsession.query(models.Article).filter(models.Article.moduleId.in_(menuIds)).first()
        log.debug("First Article is {0} {1}".format(theArticle, theArticle.id))

    modules = request.user.modules
    return {'moduleId': moduleId,
            'currentModule': thisModule,
            'modules': modules,
            'effectiveRole': effectiveRole,
            'thisArticle': theArticle}



@view_config(route_name='newArticle', renderer='../templates/newArticle.jinja2')
def newArticle(request):
    user = request.user
    if user is None:
        raise HTTPForbidden

    log.debug(request.matchdict)

    #Module Id
    moduleId = request.matchdict.get('moduleId')
    log.debug("Page for {0}".format(moduleId))


    thisModule = request.dbsession.query(models.Module).filter_by(id = moduleId).first()
    if thisModule is None:
        raise HTTPNotFound


    if user.role != models.ADMIN:
        #Check if the user can see this page
        if thisModule not in user.modules:
            log.warning("Attempts to view unallocated module")
            raise HTTPNotFound

    log.debug(request.POST)
    heading = request.POST.get('topicSelect', None)
    title = request.POST.get('topicTitle', None)
    content = request.POST.get('articleContent', None)
    
    msg = ""
    if content:
        log.debug("Create a new Article")
        #Find the Topci we live under
        log.debug("Heading We are Searching for {0}".format(heading))
        theTopic = request.dbsession.query(models.MenuItem).filter_by(id= heading).first()
        log.debug(theTopic)
        if theTopic is None:
            log.warning("Attempt to add to non existant topic")
            msg += "Non Existant Topic "
        if title is None:
            msg += "Supply a Title "
        if content is None:
            msg += "You need Content"
        else:
            theArticle = models.Article(moduleId=theTopic.id, title=title, text=content)
            theTopic.articles.append(theArticle)

            return HTTPFound(location=request.route_url("materials", moduleId=thisModule.id, pageId = theArticle.id))  
            #And go back to the main page
            #return HTTPFound
        #Lets create a new post




    modules = request.user.modules
    return {'moduleId': moduleId,
            'currentModule': thisModule,
            'modules': modules,
            "msg": msg,
            }
    