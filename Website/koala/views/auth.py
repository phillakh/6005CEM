"""
Login / Logout (and security Logic)
"""

import hashlib

from pyramid.view import view_config
from pyramid.response import Response

from pyramid.security import (
    remember,
    forget,
    )

from pyramid.view import forbidden_view_config
from pyramid.httpexceptions import HTTPFound


from sqlalchemy.exc import DBAPIError

from koala.models import User


import logging
log = logging.getLogger("auth")
log.setLevel(logging.DEBUG)

@view_config(route_name='login', renderer='../templates/login.jinja2')
def login(request):

    outdict = {}
    if 'email' in request.params:
        
        email = request.params.get("email")
        password = request.params.get("password")
        #Do the whole database query thing
        log.debug("Attempted User Login {0} With Password {1}".format(email, password))

        log.debug("-"*50)
        qry = f"SELECT * from USER where email='{email}'"
        theQry = request.dbsession.execute(qry)
        user = theQry.first()
        log.debug("Compare to user {0}".format(user))
        if user is not None:

            #SALT the password
            salted = "{0}{1}".format(password, user[1])
            theHash = hashlib.sha256(salted.encode()).hexdigest()
            print(theHash)
            print(user[3])
            #Check the supploed password against the hash
            if theHash == user[3]:
                headers = remember(request, user[0])
                return HTTPFound(location=request.route_url("feed", moduleId=1), headers=headers)
            else:
                log.debug("Password Incorrect")
                outdict["message"] = "Incorrect Password for {0}".format(user[1])
        else:
            outdict["message"] = "No User Found"

    return outdict
    


@view_config(route_name='logout')
def logout(request):
    log.info("User Logs out")
    #Forget who we are
    headers = forget(request)
    homeurl = request.route_url('home')
    return HTTPFound(location=homeurl, headers=headers)

#Overload Forbidden view so we go to login
@forbidden_view_config()
def forbidden_view(request):
    loginurl = request.route_url("login")
    logging.debug(loginurl)
    return HTTPFound(location=loginurl)

