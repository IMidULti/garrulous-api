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
        self.msg  = MessageApi()
        self.auth = AuthApi()
        self.friend = FriendApi()

    def GET(self):
        return "API for Garrulous. Read API documentation to use /v1/ resources."

#Create User
#Updates user
class UserApi(object):
    exposed = True

    # this can return username for searching other people.
    @cherrypy.tools.json_out()
    def GET(self):
        return {'error': True, 'msg': "Error during request"}

    @cherrypy.tools.json_out()
    def POST(self):
        return {'error': True, 'msg': "Error during request"}

    # For creating a new user
    @cherrypy.tools.json_out()
    def PUT(self):
        return {'error': True, 'msg': "Error during request"}

    @cherrypy.tools.json_out()
    def DELETE(self):
        return {'error': True, 'msg': "Error during request"}

class FriendApi(object):
    exposed = True

    # get lists of friends for this user
    @cherrypy.tools.json_out()
    def GET(self):
        return {'error': True, 'msg': "Error during request"}

    # Add person to friends list
    @cherrypy.tools.json_out()
    def PUT(self):
        return {'error': True, 'msg': "Error during request"}

    # remove person from friends list
    @cherrypy.tools.json_out()
    def DELETE(self):
        return {'error': True, 'msg': "Error during request"}

# Create Message
# Get Message
class MessageApi(object):
    exposed = True

    # Retrieve
    @cherrypy.tools.json_out()
    def GET(self):
        return {'error': True, 'msg': "Error during request"}

    # Send
    @cherrypy.tools.json_out()
    def PUT(self):
        return {'error': True, 'msg': "Error during request"}

class AuthApi(object):
    exposed = True

    # Get auth token back
    @cherrypy.tools.json_out()
    def GET(self):
        return {'error': True, 'msg': "Error during request"}


if __name__ == '__main__':
    #get SQLite started.
    conn = sqlite3.connect('garrulous.db')
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
    cherrypy.tree.mount(SiteApi().user, '/user/', api_conf)
    cherrypy.tree.mount(SiteApi().msg, '/msg/', api_conf)
    cherrypy.tree.mount(SiteApi().user, '/friend/', api_conf)

    cherrypy.engine.start()
    cherrypy.engine.block()