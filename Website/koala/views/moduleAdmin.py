"""
Features for administrating Materials
"""

import pickle
import datetime
import pathlib

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
log = logging.getLogger("Admin")
log.setLevel(logging.DEBUG)

@view_config(route_name='moduleAdmin', renderer='../templates/moduleAdmin.jinja2')
def materials(request):

    log.debug("="*60)
    log.debug("Backup")
    log.debug("="*60)
    user = request.user
    if user is None:
        raise HTTPForbidden

    #Module Id
    moduleId = request.matchdict.get('moduleId')
    thisModule = request.dbsession.query(models.Module).filter_by(id = moduleId).first()
    if thisModule is None:
        raise HTTPNotFound

    #Students should not be able to come here
    if user.role == models.STUDENT:
        log.warning("Attempts to view unallocated module")
        raise HTTPNotFound

    # Kick Teachers if they are not part of this module
    if user.role != models.ADMIN:
        #Check if the user can see this page
        if thisModule not in user.modules:
            log.warning("Attempts to view unallocated module")
            raise HTTPNotFound

    #User Message
    msg = None

    #Now we want to deal with the various backup and restore
    if "backup" in request.POST:
        log.debug("BACKUP FORM SUBMITTED")
        log.debug(request.POST)
        filename = dumpModule(request, thisModule)
        msg = {"type": "alert-success",
               "text": "Module Saved Sucessfully as {0}".format(filename)}

    #We also want to get a list of possible backups
    rawBase = "koala/backups/{0}/".format(thisModule.code)
    basePath = pathlib.Path(rawBase)

    backupList = []
    if basePath.exists():
        #Itreate through the list getting all backups known
        for item in basePath.iterdir():
            #All we want is the filename
            backupList.append(item.name)

    modules = request.user.modules
    return {'moduleId': moduleId,
            'currentModule': thisModule,
            'modules': modules,
            'backupList': backupList,
            'msg': msg}

    
def dumpModule(request, thisModule):
    """Code to Dump A Module"""

    log.debug("Dumping Function")

    #So now we can do the backup
    storeDict = {"module": thisModule,
                 "navmenu": list(thisModule.navmenu),
    }

    #And we also need to add all the contents
    articles = []
    for item in thisModule.navmenu:
        articles.extend(list(item.articles))

    storeDict["articles"] = articles
        #And dump all the Materials
    log.debug(storeDict)
    # -------- ACTUAL BACKUP CODE -------------
    fileName = request.POST["backupName"]
    if not fileName:
        datestr = datetime.datetime.utcnow().strftime("%Y_%M_%d-%H%M")
        fileName = "{0}_{1}.bak".format(thisModule.code, datestr)
    else:
        fileName = "{0}.bak".formaT(fileName)                   
    log.debug("Save File as {0}".format(fileName))

    #Now the Path
    rawBase = "koala/backups/{0}/".format(thisModule.code)
    basePath = pathlib.Path(rawBase)
        

    log.debug("Base PAth is {0} {1}".format(basePath, basePath.absolute()))
    #log.debug("File Path is {0}".format(filePath))
    if not basePath.exists():
        log.debug("\tCreating backup directory")
        basePath.mkdir(parents=True)
    else:
        log.debug("\tExists {0}".format(basePath.exists()))

    #And the file
    rawFile = "{0}{1}".format(rawBase, fileName)
    log.debug("RAW FILE PATH {0}".format(rawFile))
    filePath = pathlib.Path(rawFile)
    log.debug(filePath)


    with filePath.open("wb") as fd:
        pickle.dump(storeDict, fd)
        

    return fileName


@view_config(route_name='moduleRestore', renderer='../templates/moduleRestore.jinja2')
def restoreModule(request):
    #TODO: Make this a function. 
    log.debug("="*60)
    log.debug("Restore")
    log.debug("="*60)
    user = request.user
    if user is None:
        raise HTTPForbidden

    #Module Id
    moduleId = request.matchdict.get('moduleId')
    thisModule = request.dbsession.query(models.Module).filter_by(id = moduleId).first()
    if thisModule is None:
        raise HTTPNotFound

    #Students should not be able to come here
    if user.role == models.STUDENT:
        log.warning("Attempts to view unallocated module")
        raise HTTPNotFound

    # Kick Teachers if they are not part of this module
    if user.role != models.ADMIN:
        #Check if the user can see this page
        if thisModule not in user.modules:
            log.warning("Attempts to view unallocated module")
            raise HTTPNotFound

    #And get the ID of the file we wish to open
    log.debug(request.POST)
    if not request.POST:
        log.warning("Restore without POST")
        return HTTPFound(location=request.route_url("moduleAdmin", moduleId=thisModule.id))  
        
    restoreName = request.POST["restoreName"]
    if not restoreName:
        return HTTPFound(location=request.route_url("moduleAdmin", moduleId=thisModule.id))


    msg = None
    preview = None
    result = None

    #Open the file for preview
    rawBase = "koala/backups/{0}/{1}".format(thisModule.code, restoreName)
    basePath = pathlib.Path(rawBase)
    log.debug(basePath)
    log.debug(basePath.exists())

    #Get a bit of text as a preview
    if not basePath.exists():
        msg = {"type": "alert-error",
               "message": "No such File"}
               #Do we confirm the restore

    else:
        log.debug("Exists:  Getting preview")
        preview = basePath.read_bytes()
        #log.debug(preview)
        
    if request.POST.get("confirmRestore"):
        log.debug("!!!!! CONFIRMING RESTORE !!!!!")
        msg = {"type": "alert-info",
               "message": "Attempt to Restore File {0}".format(basePath)}
        
        #Do the pickle thing
        with basePath.open("rb") as fd:
            out = pickle.load(fd)
            log.debug(out)
            result = out
            preview=None

    modules = request.user.modules
    return {'moduleId': moduleId,
            'currentModule': thisModule,
            'modules': modules,
            'restoreName': restoreName,
            'msg': msg,
            'preview': preview,
            'result' : result

            }


@view_config(route_name='studentList', renderer='../templates/studentList.jinja2')
def studentList(request):
    #TODO: Make this a function. 
    log.debug("="*60)
    log.debug("Restore")
    log.debug("="*60)
    user = request.user
    if user is None:
        raise HTTPForbidden

    #Module Id
    moduleId = request.matchdict.get('moduleId')
    thisModule = request.dbsession.query(models.Module).filter_by(id = moduleId).first()
    if thisModule is None:
        raise HTTPNotFound

    #Students should not be able to come here
    if user.role == models.STUDENT:
        log.warning("Attempts to view unallocated module")
        raise HTTPNotFound

    # Kick Teachers if they are not part of this module
    if user.role != models.ADMIN:
        #Check if the user can see this page
        if thisModule not in user.modules:
            log.warning("Attempts to view unallocated module")
            raise HTTPNotFound

    #And get the data (We dont want to return everything
    qry = request.dbsession.query(models.User.name, models.User.email, models.Module.name)
    #Join to the Modules DB
    qry = qry.join(models.User.modules)
    qry = qry.filter(models.User.role == models.STUDENT)

    #And our other Qeury items
    log.debug(request.GET)
    filterName = request.GET.get("filterName",None)
    filterMod = request.GET.get("filterModule", None)
    groupBy = request.GET.get("groupBy", None)
    
    if filterName:
        log.debug("Filter by Name")
        qry = qry.filter(models.User.name == filterName)
    if filterMod:
        log.debug("Filter b Module")
        qry = qry.filter(models.Module.name == filterMod)

    if groupBy:
        qry = qry.group_by(groupBy)
    log.debug(qry.first())



    
    #qry = qry.limit(10)
    #print(qry.all())
    #Build up the Queries
    
    

        
    modules = request.user.modules
    return {'moduleId': moduleId,
            'currentModule': thisModule,
            'modules': modules,
            'data': qry
            }
