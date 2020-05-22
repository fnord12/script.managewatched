import xbmc
import xbmcaddon
import sys
import xbmcgui

import managewatched

parser = sys.argv[1]

if parser == "mark":
    managewatched.markWatch()
    
elif parser == "reset":
    managewatched.resetWatch()
    
elif parser == "clear":
    managewatched.clearResume()

elif parser == "edit":
    managewatched.editLastPlayed()    

else:
    debug("Unknown parser")