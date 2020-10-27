"""
Deal with things like image uploads
"""

from pyramid.view import view_config
from pyramid.response import Response

from pyramid.httpexceptions import (
    HTTPForbidden,
    HTTPFound,
    HTTPNotFound,
    )

from pyramid_storage.exceptions import FileNotAllowed

from sqlalchemy.exc import DBAPIError

from .. import models

import logging
log = logging.getLogger("upload")
log.setLevel(logging.DEBUG)

@view_config(route_name='avatarupload', request_method='POST')
def uploadAvatar(request):
    log.info("Image Upload")
    log.debug(request.params)

    user = request.user
    if user is None:
        raise HTTPForbidden


    #Now look for Image
    theImg = request.POST.get('uploadimage')
    if theImg is None:
        return  
    else:
        log.debug("Attempt to upload image {0}".format(theImg))
        try:
            out = request.storage.save(theImg, folder="avatars", extensions=('jpg', 'gif', 'png'), randomize=True)
            request.session.flash("Image Uploaded Successfully")

            #And update the user profile
            log.debug("User Profile is {0}".format(user.profile))
            if user.profile is None:
                log.debug("NO USER PROFILE")
                theProfile = models.UserProfile(user.id)
                request.dbsession.add(theProfile)
            
            else:
                log.debug("User HAs Profile")
                #We could have multiple profiels for some reason
                theProfile = user.profile

            #And update the URL
            theProfile.avatar = out


        except FileNotAllowed:
            request.session.flash('File Type not allowed')
            

        

        #Grab the URL 
        theRoute = request.POST['from']
        log.debug("ROUT IS {0}".format(theRoute))
        return HTTPFound(theRoute)
    
