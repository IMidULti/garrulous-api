__author__ = 'Richard Meyers'

import os
import cherrypy
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
        return "User NO"

    @cherrypy.tools.json_out()
    def POST(self):
        return "User NO"


    @cherrypy.tools.json_out()
    def PUT(self):
        return False

    @cherrypy.tools.json_out()
    def DELETE(self):
        return False

if __name__ == '__main__':
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