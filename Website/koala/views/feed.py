"""
View Feed
"""

#To Escape HTML
import html

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
log = logging.getLogger("Feed")
log.setLevel(logging.DEBUG)

@view_config(route_name='feed', renderer='../templates/feed.jinja2')
def feed(request):
    user = request.user
    if user is None:
        raise HTTPForbidden



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


    log.debug("="*50)
    # ------- Form Handling ----------
    log.debug(request.matchdict)
    log.debug(request.POST)
    if "postContent" in request.POST:
        log.debug("Content Has been posted")
        title = request.POST.get("posttitle")
        content = request.POST.get("postContent")
        parent = request.POST.get("postparent")

        #So here we create our new post
        if parent == "0":
            log.debug("--- CREATE A NEW POST ---")
            log.debug("\tModule Id\t {0}".format(moduleId))
            log.debug("\tAuthor Id\t {0}".format(user.id))
            log.debug("\tTitle\t\t{0}".format(title))
            log.debug("\tContent\t\t{0}".format(content))
            thePost = models.Post(user.id,
                                  content,
                                  moduleId,
                                  title=title)
            
            request.dbsession.add(thePost)
        else:
            log.debug("---- Create a Reply -----")
            #Again we can create a reply
            thePost = models.Post(user.id,
                                  content,
                                  module = None,
                                  parent = parent,
                                  )
            request.dbsession.add(thePost)
            
    else:
        log.debug("NO CONTENT")


    # Now we can get the list of posts

    postqry = request.dbsession.query(models.Post).filter_by(module = moduleId)
    postqry = postqry.order_by(models.Post.date.desc())  
    #Add A Limut ??      

    modules = request.user.modules
    return {'moduleId': moduleId,
            'currentModule': thisModule,
            'modules': modules,
            'posts' : postqry,
            }
