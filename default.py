import xbmc
import xbmcaddon
import sys
import xbmcgui

import managewatched

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
        
assetTYPE = xbmc.getInfoLabel('ListItem.DBtype')
acceptedAssetTypes = ['episode', 'tvshow', 'movie', 'set', 'season']

parser = sys.argv[1]

if assetTYPE in acceptedAssetTypes:

    if parser == "mark":
        managewatched.markWatch()
        
    elif parser == "reset":
        managewatched.resetWatch()
        
    elif parser == "clear":
        managewatched.clearResume()
        
    elif parser == "edit":
        managewatched.editLastPlayed()    

    elif parser == "unmark":
        managewatched.markUnWatch()

    else:
        debug("Unknown parser")
        
else:
    assetMsg = "Invalid item selected: '%s'" % assetTYPE
    xbmc.executebuiltin("Notification(\"Reset Watched\", \"%s\")" % assetMsg)