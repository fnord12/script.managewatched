import xbmc
import xbmcaddon
import sys
import xbmcgui

import managewatched

def debug(msg, *args):
    try: 
        txt = ""
     
        for arg in args:
            txt = txt + arg + " | "
        xbmc.log("WATCH: " + msg + ": " + txt)
    except:
        print("WATCH default: Error in Debugoutput")
        print(msg)
        print(args)
        
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