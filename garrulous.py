__author__ = 'Richard Meyers'

import os
import cherrypy
import sqlite3
import json

class SiteIndex(object):
    exposed = True

    def GET(self):
        cherrypy.response.headers['Content-Type'] = 'text/html'
        try:
            f = open('html/index.html')
            content = f.readlines()
            f.close()
        except IOError:
            raise cherrypy.HTTPError("500", "Contact administrators")

        return content

class SiteApi(object):
    exposed = True

    def __init__(self):
        self.user = UserApi()

    def GET(self):
        return "API for Garrulous. Read API documentation to use /v1/ resources."

class UserApi(object):
    exposed = True

    @cherrypy.tools.json_out()
    def GET(self):
        return {'error': True, 'msg': "Error during request"}

    @cherrypy.tools.json_out()
    def POST(self):
        return {'error': True, 'msg': "Error during request"}

    @cherrypy.tools.json_out()
    def PUT(self):
        return {'error': True, 'msg': "Error during request"}

    @cherrypy.tools.json_out()
    def DELETE(self):
        return {'error': True, 'msg': "Error during request"}

if __name__ == '__main__':
    #get SQLite started.
    conn = sqlite3.connect('database.db')
    #The database needs to be queried here. If the
    # tables don't exist they need to be created.
    # Add the schema here.
    db_cursor = conn.cursor()

    #This is just an example
    """db_cursor.execute("CREATE TABLE IF NOT EXISTS `abuses` (" +
                      "`abuse_id` int(11) NOT NULL AUTO_INCREMENT," +
                      "`user_id` int(11) NOT NULL DEFAULT '0',")"""

    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.dirname(os.path.realpath(__file__)) + '/static/'
        }
    }
    api_conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        }
    }
    cherrypy.config.update({'environment': 'production'})
    cherrypy.tree.mount(SiteIndex(), '/', conf)
    cherrypy.tree.mount(SiteApi(), '/v1/', api_conf)

    cherrypy.engine.start()
    cherrypy.engine.block()