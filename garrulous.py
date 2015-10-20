__author__ = 'Richard Meyers'

import os

import cherrypy

class SiteIndex(object):
    exposed = True

    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        return "Garrulous Project Page"

    def POST(self):
        return "Cannot POST anything yet"

    def PUT(self):
        return "Don't do PUTs either"

    def DELETE(self):
        return "There is nothing to delete"

class SiteApi(object):
    exposed = True

    def __init__(self):
        self.user = UserApi()

    def GET(self):
        return "NO"

    def POST(self):
        return "NO"

    def PUT(self):
        return "NO"

    def DELETE(self):
        return "NO"

class UserApi(object):
    exposed = True

    def GET(self):
        return "User NO"

    def POST(self):
        return "User NO"

    def PUT(self):
        return "User NO"

    def DELETE(self):
        return "User NO"

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