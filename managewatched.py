# import the kodi python modules we are going to use
# see the kodi api docs to find out what functionality each module provides
import xbmc
import xbmcaddon
import sys
import json
import re
import datetime

from CWatchedDatabase import CVideoDatabase

Updater = "JSON"

def debug(msg, *args):
    try:
        txt=u''
        msg=unicode(msg)
        for arg in args:
            if type(arg) == int:
                arg = unicode(arg)
            if type(arg) == list:
                arg = unicode(arg)
            txt = txt + u"/" + arg
        if txt == u'':
            xbmc.log(u"WATCH: {0}".format(msg).encode('ascii','xmlcharrefreplace'), xbmc.LOGDEBUG)
        else:
            xbmc.log(u"WATCH: {0}#{1}#".format(msg, txt).encode('ascii','xmlcharrefreplace'), xbmc.LOGDEBUG)
    except:
        print "Error in Debugoutput"
        print msg
        print args

def GetVideosInCollection(assetTYPE,ID):
    debug("GetVideosInCollection")
    
    vdb = CVideoDatabase()
    if assetTYPE == 'tvshow':
        VideosTuple = vdb.GetEpisodesInShowDB(assetTYPE,ID)
    elif assetTYPE == 'season':
        VideosTuple = vdb.GetEpisodesInSeasonDB(assetTYPE,ID)
    elif assetTYPE == 'set':
        VideosTuple = vdb.GetMoviesInSetDB(assetTYPE,ID)
    
    debug ("VideosTuple = ", VideosTuple)
    return VideosTuple

def getFileID(assetTYPE,ID):
    debug("getFileID")
    vdb = CVideoDatabase()
    FileIDTuple = vdb.getFileIDDB(assetTYPE,ID)
    FileIDList = [list(x) for x in FileIDTuple]
    FileID = FileIDList[0][0]
    return FileID

def process(assetTYPE,ID,NewCount,NewResume,NewLastPlayed):
    debug("process")
    if Updater == "DB":
        processWithDB(assetTYPE,ID,NewCount,NewResume,NewLastPlayed)
    else:
        processWithJSON(assetTYPE,ID,NewCount,NewResume,NewLastPlayed)

def processWithJSON(assetTYPE,ID,NewCount,NewResume,NewLastPlayed):
    debug("processWithJSON")
    
    if assetTYPE == 'movie':
        response = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id": 1, "method": "VideoLibrary.SetMovieDetails", "params": {"movieid" : %d, "playcount": %d, "lastplayed": "%s", "resume": {"position": %d} }} ' % (ID, NewCount, NewLastPlayed, NewResume))
    elif assetTYPE == 'episode':
        response = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id": 1, "method": "VideoLibrary.SetEpisodeDetails", "params": {"episodeid" : %d, "playcount": %d, "lastplayed": "%s", "resume": {"position": %d} }} ' % (ID, NewCount, NewLastPlayed, NewResume))
    else:
        assetMsg = "Invalid item selected: '%s'" % assetTYPE
        xbmc.executebuiltin("Notification(\"Reset Watched\", \"%s\")" % assetMsg)
        
def processWithDB(assetTYPE,ID,NewCount,NewResume,NewLastPlayed):
    debug("processWithDB")
    vdb = CVideoDatabase()
    FileID = getFileID(assetTYPE,ID)
    vdb.updateResumeDB(FileID,NewResume)
    
    if NewLastPlayed == "":
        vdb.markUnWatchedDB(FileID)
    else:
        vdb.markWatchedDB(FileID,NewCount,NewLastPlayed)
        
def reset(assetTYPE,ID,NewResume,NewLastPlayed):
     debug("reset")
     if Updater == "DB":
        resetWithDB(assetTYPE,ID,NewResume,NewLastPlayed)
     else:
        resetWithJSON(assetTYPE,ID,NewResume,NewLastPlayed)       
        
def resetWithJSON(assetTYPE,ID,NewResume,NewLastPlayed):
    debug("resetWithJSON")
    
    if assetTYPE == 'movie':
        response = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id": 1, "method": "VideoLibrary.SetMovieDetails", "params": {"movieid" : %d, "lastplayed": "%s", "resume": {"position": %d} }} ' % (ID, NewLastPlayed, NewResume))
        
        debug(response)
    elif assetTYPE == 'episode':
        response = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id": 1, "method": "VideoLibrary.SetEpisodeDetails", "params": {"episodeid" : %d, "lastplayed": "%s", "resume": {"position": %d} }} ' % (ID, NewLastPlayed, NewResume))
    else:
        assetMsg = "Invalid item selected: '%s'" % assetTYPE
        xbmc.executebuiltin("Notification(\"Reset Watched\", \"%s\")" % assetMsg)
        
def resetWithDB(assetTYPE,ID,NewResume,NewLastPlayed):
    debug("resetWithDB")
    
    debug("processWithDB")
    vdb = CVideoDatabase()
    FileID = getFileID(assetTYPE,ID)
    vdb.updateResumeDB(FileID,NewResume)
    vdb.resetWatchedDB(FileID,NewLastPlayed)
        
def clear(assetTYPE,ID,NewResume):
    debug("clear")
    
    if Updater == "DB":
        clearWithDB(assetTYPE,ID,NewResume)
    else:
        clearWithJSON(assetTYPE,ID,NewResume)
        
def clearWithJSON(assetTYPE,ID,NewResume):
    debug ("clearWithJSON")
    
    if assetTYPE == 'movie':
        response = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id": 1, "method": "VideoLibrary.SetMovieDetails", "params": {"movieid" : %d, "resume": {"position": %d} }} ' % (ID, NewResume))
    elif assetTYPE == 'episode':
        response = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id": 1, "method": "VideoLibrary.SetEpisodeDetails", "params": {"episodeid" : %d, "resume": {"position": %d} }} ' % (ID, NewResume))
    else:
        assetMsg = "Invalid item selected: '%s'" % assetTYPE
        xbmc.executebuiltin("Notification(\"Reset Watched\", \"%s\")" % assetMsg)
        
        
def clearWithDB(assetTYPE,ID,NewResume):
    debug ("clearWithDB")
    
    debug("processWithDB")
    vdb = CVideoDatabase()
    FileID = getFileID(assetTYPE,ID)
    vdb.updateResumeDB(FileID,NewResume)

def markWatch():
    debug ("markWatch")
    
    assetTYPE = xbmc.getInfoLabel('ListItem.DBtype')
    path = xbmc.getInfoLabel('ListItem.FileNameAndPath')
    ID = int(xbmc.getInfoLabel('ListItem.DBID'))

    debug('assetTYPE', assetTYPE)
    debug('path', path)
    debug('ID', ID)

    NewCount = 1
    NewResume = 0
    NewLastPlayed = "2000-01-01 00:00:01"

    if assetTYPE == 'movie' or assetTYPE == 'episode':
        process(assetTYPE,ID,NewCount,NewResume,NewLastPlayed)
        xbmc.executebuiltin('ReloadSkin()')
        
    elif assetTYPE == 'tvshow':
        EpisodesTuple = GetVideosInCollection(assetTYPE,ID)
        debug ("EpisodesList = ", EpisodesTuple)
        Max = len(EpisodesTuple)
        i=0
        while i < Max:
            EpisodeID = EpisodesTuple[i][0]
            process('episode',EpisodeID,NewCount,NewResume,NewLastPlayed)
            i+= 1
        xbmc.executebuiltin('ReloadSkin()')
    elif assetTYPE == 'season':    
        EpisodesTuple = GetVideosInCollection(assetTYPE,ID)
        debug ("EpisodesList = ", EpisodesTuple)
        Max = len(EpisodesTuple)
        i=0
        while i < Max:
            EpisodeID = EpisodesTuple[i][0]
            debug ('EpisodeID= ', EpisodeID)
            process('episode',EpisodeID,NewCount,NewResume,NewLastPlayed)
            i+= 1
        xbmc.executebuiltin('ReloadSkin()')    
    elif assetTYPE == 'set':    
        MoviesTuple = GetVideosInCollection(assetTYPE,ID)
        debug ("MoviesList = ", MoviesTuple)
        Max = len(MoviesTuple)
        i=0
        while i < Max:
            MovieID = MoviesTuple[i][0]
            debug ('MovieID= ', MovieID)
            process('movie',MovieID,NewCount,NewResume,NewLastPlayed)
            i+= 1
        xbmc.executebuiltin('ReloadSkin()')
    else:
        assetMsg = "Invalid item selected: '%s'" % assetTYPE
        xbmc.executebuiltin("Notification(\"Reset Watched\", \"%s\")" % assetMsg)

def markUnWatch():
    debug("markUnWatch")
    
    assetTYPE = xbmc.getInfoLabel('ListItem.DBtype')
    path = xbmc.getInfoLabel('ListItem.FileNameAndPath')
    ID = int(xbmc.getInfoLabel('ListItem.DBID'))

    debug('assetTYPE', assetTYPE)
    debug('path', path)
    debug('ID', ID)

    NewCount = 0
    NewResume = 0
    NewLastPlayed = ""
    
    if assetTYPE == 'movie' or assetTYPE == 'episode':
        process(assetTYPE,ID,NewCount,NewResume,NewLastPlayed)
        xbmc.executebuiltin('ReloadSkin()')
        
    elif assetTYPE == 'tvshow':
        EpisodesTuple = GetVideosInCollection(assetTYPE,ID)
        debug ("EpisodesList = ", EpisodesTuple)
        Max = len(EpisodesTuple)
        i=0
        while i < Max:
            EpisodeID = EpisodesTuple[i][0]
            debug ('EpisodeID= ', EpisodeID)
            process('episode',EpisodeID,NewCount,NewResume,NewLastPlayed)
            i+= 1
        xbmc.executebuiltin('ReloadSkin()')
    elif assetTYPE == 'season':    
        EpisodesTuple = GetVideosInCollection(assetTYPE,ID)
        debug ("EpisodesList = ", EpisodesTuple)
        Max = len(EpisodesTuple)
        i=0
        while i < Max:
            EpisodeID = EpisodesTuple[i][0]
            debug ('EpisodeID= ', EpisodeID)
            process('episode',EpisodeID,NewCount,NewResume,NewLastPlayed)
            i+= 1
        xbmc.executebuiltin('ReloadSkin()')
    elif assetTYPE == 'set':    
        MoviesTuple = GetVideosInCollection(assetTYPE,ID)
        debug ("MoviesList = ", MoviesTuple)
        Max = len(MoviesTuple)
        i=0
        while i < Max:
            MovieID = MoviesTuple[i][0]
            debug ('MovieID= ', MovieID)
            process('movie',MovieID,NewCount,NewResume,NewLastPlayed)
            i+= 1
        xbmc.executebuiltin('ReloadSkin()')
    else:
        assetMsg = "Invalid item selected: '%s'" % assetTYPE
        xbmc.executebuiltin("Notification(\"Reset Watched\", \"%s\")" % assetMsg)
        
def resetWatch():
    debug("resetWatch")
    
    assetTYPE = xbmc.getInfoLabel('ListItem.DBtype')
    path = xbmc.getInfoLabel('ListItem.FileNameAndPath')
    ID = int(xbmc.getInfoLabel('ListItem.DBID'))

    debug('assetTYPE', assetTYPE)
    debug('path', path)
    debug('ID', ID)

    NewResume = 0
    NewLastPlayed = "2000-01-01 00:00:01"
    
    if assetTYPE == 'movie' or assetTYPE == 'episode':
        reset(assetTYPE,ID,NewResume,NewLastPlayed)
        xbmc.executebuiltin('ReloadSkin()')
        
    elif assetTYPE == 'tvshow':
        EpisodesTuple = GetVideosInCollection(assetTYPE,ID)
        debug ("EpisodesList = ", EpisodesTuple)
        Max = len(EpisodesTuple)
        i=0
        while i < Max:
            EpisodeID = EpisodesTuple[i][0]
            debug ('EpisodeID= ', EpisodeID)
            reset('episode',EpisodeID,NewResume,NewLastPlayed)
            i+= 1
        debug('Resetting Sking')
        xbmc.executebuiltin('ReloadSkin()')
    elif assetTYPE == 'season':    
        EpisodesTuple = GetVideosInCollection(assetTYPE,ID)
        debug ("EpisodesList = ", EpisodesTuple)
        Max = len(EpisodesTuple)
        i=0
        while i < Max:
            EpisodeID = EpisodesTuple[i][0]
            debug ('EpisodeID= ', EpisodeID)
            reset('episode',EpisodeID,NewResume,NewLastPlayed)
            i+= 1
        xbmc.executebuiltin('ReloadSkin()')
    elif assetTYPE == 'set':    
        MoviesTuple = GetVideosInCollection(assetTYPE,ID)
        debug ("MoviesList = ", MoviesTuple)
        Max = len(MoviesTuple)
        i=0
        while i < Max:
            MovieID = MoviesTuple[i][0]
            debug ('MovieID= ', MovieID)
            reset('movie',MovieID,NewResume,NewLastPlayed)
            i+= 1
        xbmc.executebuiltin('ReloadSkin()')
    else:
        assetMsg = "Invalid item selected: '%s'" % assetTYPE
        xbmc.executebuiltin("Notification(\"Reset Watched\", \"%s\")" % assetMsg)
        
def clearResume():
    debug("clearResume")
    
    assetTYPE = xbmc.getInfoLabel('ListItem.DBtype')
    path = xbmc.getInfoLabel('ListItem.FileNameAndPath')
    ID = int(xbmc.getInfoLabel('ListItem.DBID'))

    debug('assetTYPE', assetTYPE)
    debug('path', path)
    debug('ID', ID)

    NewResume = 0
    
    if assetTYPE == 'movie' or assetTYPE == 'episode':
        clear(assetTYPE,ID,NewResume)
        xbmc.executebuiltin('ReloadSkin()')
        
    elif assetTYPE == 'tvshow':
        EpisodesTuple = GetVideosInCollection(assetTYPE,ID)
        debug ("EpisodesList = ", EpisodesTuple)
        Max = len(EpisodesTuple)
        i=0
        while i < Max:
            EpisodeID = EpisodesTuple[i][0]
            debug ('EpisodeID= ', EpisodeID)
            clear('episode',EpisodeID,NewResume)
            i+= 1
        xbmc.executebuiltin('ReloadSkin()')
    elif assetTYPE == 'season':    
        EpisodesTuple = GetVideosInCollection(assetTYPE,ID)
        debug ("EpisodesList = ", EpisodesTuple)
        Max = len(EpisodesTuple)
        i=0
        while i < Max:
            EpisodeID = EpisodesTuple[i][0]
            debug ('EpisodeID= ', EpisodeID)
            clear('episode',EpisodeID,NewResume)
            i+= 1
        xbmc.executebuiltin('ReloadSkin()')
    elif assetTYPE == 'set':    
        MoviesTuple = GetVideosInCollection(assetTYPE,ID)
        debug ("MoviesList = ", MoviesTuple)
        Max = len(MoviesTuple)
        i=0
        while i < Max:
            MovieID = MoviesTuple[i][0]
            debug ('MovieID= ', MovieID)
            clear('movie',MovieID,NewResume)
            i+= 1
        xbmc.executebuiltin('ReloadSkin()')
    else:
        assetMsg = "Invalid item selected: '%s'" % assetTYPE
        xbmc.executebuiltin("Notification(\"Reset Watched\", \"%s\")" % assetMsg)
        
def validateDate(DateTime):
    
    Date, Time = DateTime.split(" ")    
    year,month,day = Date.split('-')
    
    isValidDate = True
    try :
        datetime.datetime(int(year),int(month),int(day))
    except:
        isValidDate = False

    hour,minute,second = Time.split(':')
    
    isValidTime = True
    try:
        if (int(hour) < 25) and (int(minute) < 60) and (int(second) < 60):
            isValidTime = True
        else:
            isValidTime = False
    except:
        isValidTime = False
    
    if (isValidDate) and (isValidTime) :
        return True
    else :
        return False
        
def editLastPlayed():
    debug("editLastPlayed")
    
    assetTYPE = xbmc.getInfoLabel('ListItem.DBtype')
    path = xbmc.getInfoLabel('ListItem.FileNameAndPath')
    ID = int(xbmc.getInfoLabel('ListItem.DBID'))

    debug('assetTYPE', assetTYPE)
    debug('path', path)
    debug('ID', ID)
    
    if assetTYPE == 'movie':
        paramsRaw = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovieDetails", "params": {"movieid": %d, "properties": ["title","lastplayed","playcount","resume"]}, "id": 1}' % ID)
        
        paramsRaw = paramsRaw.decode(encoding="utf-8",errors="ignore")
        params = json.loads(paramsRaw)
        result = params['result']
        debug("result =", result)
        moviedetails = result['moviedetails']
        debug("moviedetails =", moviedetails)
        LastPlayedDate = moviedetails.get('lastplayed')
        Title = moviedetails.get('title')
        debug("LastPlayedDate =", LastPlayedDate)
        
        keyboard = xbmc.Keyboard(LastPlayedDate, "Edit Last Played Date for " + Title)
        keyboard.doModal()
        
        if keyboard.isConfirmed() and keyboard.getText():
            NewLastPlayed = (keyboard.getText().strip())
            
            debug ('NewLastPlayed = ', NewLastPlayed)
            
            if validateDate(NewLastPlayed):
                response = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id": 1, "method": "VideoLibrary.SetMovieDetails", "params": {"movieid" : %d, "lastplayed": "%s" }} ' % (ID, NewLastPlayed))
            
                debug('JSON response =', response)
                xbmc.executebuiltin('ReloadSkin()')
            else:
                Msg = "Invalid date format: '%s'" % NewLastPlayed
                xbmc.executebuiltin("Notification(\"Reset Watched\", \"%s\")" % Msg)
            
    elif assetTYPE == 'episode':
        paramsRaw = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodeDetails", "params": {"episodeid": %d, "properties": ["title","lastplayed","playcount","resume"]}, "id": 1}' % ID)
        
        paramsRaw = paramsRaw.decode(encoding="utf-8",errors="ignore")
        params = json.loads(paramsRaw)
        result = params['result']
        debug("result =", result)
        moviedetails = result['episodedetails']
        debug("moviedetails =", moviedetails)
        LastPlayedDate = moviedetails.get('lastplayed')
        Title = moviedetails.get('title')
        debug("LastPlayedDate =", LastPlayedDate)
        
        keyboard = xbmc.Keyboard(LastPlayedDate, "Edit Last Played Date for " + Title)
        keyboard.doModal()
        
        if keyboard.isConfirmed() and keyboard.getText():
            NewLastPlayed = (keyboard.getText().strip())
            
            debug ('NewLastPlayed = ', NewLastPlayed)
            
            if validateDate(NewLastPlayed):
                response = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id": 1, "method": "VideoLibrary.SetEpisodeDetails", "params": {"movieid" : %d, "lastplayed": "%s" }} ' % (ID, NewLastPlayed))
            
                debug('JSON response =', response)
                xbmc.executebuiltin('ReloadSkin()')
            else:
                Msg = "Invalid date format: '%s'" % NewLastPlayed
                xbmc.executebuiltin("Notification(\"Reset Watched\", \"%s\")" % Msg)
    else:
        assetMsg = "Invalid item selected: '%s'" % assetTYPE
        xbmc.executebuiltin("Notification(\"Reset Watched\", \"%s\")" % assetMsg)