from CDatabase import CDatabase

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

      
class CVideoDatabase:
    def __init__(self, *args, **kwargs):
        debug("CWatchedDatabase init")
        self.db = CDatabase()
        self.cur = self.db.con.cursor()
    
    def GetEpisodesInShowDB(self,assetTYPE,ID):
        sql = "select idEpisode from episode where idShow = '%s'" % (ID)
        
        debug("sql = ", sql)
        
        self.cur.execute(sql)
        return self.cur.fetchall()
        
    def GetEpisodesInSeasonDB(self,assetTYPE,ID):
        sql = "select idEpisode from episode where idSeason = '%s'" % (ID)
        
        debug("sql = ", sql)
        
        self.cur.execute(sql)
        return self.cur.fetchall()
        
    def GetMoviesInSetDB(self,assetTYPE,ID):
        sql = "select idMovie from movie where idSet = '%s'" % (ID)
        
        debug("sql = ", sql)
        
        self.cur.execute(sql)
        return self.cur.fetchall()