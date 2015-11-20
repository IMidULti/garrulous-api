# Garrulous API
# Authors: Michael Pierre and Richard Meyers

"""
Copyright (C) <year>  <name of author>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import cherrypy
import json
import logging
import yaml
from itsdangerous import URLSafeSerializer

from model.Users import Users
from model.Friendships import Friendships
from model.Messages import Messages
from model.AboutUsers import AboutUsers

from module.Config import Config

# parse the yml file and load it up.
Config.load_config()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

log_file = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(log_file, "logs")
log_file = os.path.join(log_file, "garrulous.log")
handler = logging.FileHandler(log_file)
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

logger.debug("testing logger")

class SiteIndex(object):
    exposed = True

    def GET(self):
        cherrypy.response.headers['Content-Type'] = 'text/html'
        base_dir = os.path.dirname(os.path.abspath(__file__))
        try:
            f = open(base_dir + '/view/index.html')
            content = f.readlines()
            f.close()
        except IOError:
            raise cherrypy.HTTPError("500", "Contact administrators")

        return content

class SiteApi(object):
    exposed = True

    def __init__(self):
        self.user = UserApi()
        self.msg = MessageApi()
        self.auth = AuthApi()
        self.friend = FriendApi()

    """def GET(self):
        return "API for Garrulous. Read API documentation to use /v1/ resources."""""

#Create User
#Updates user
class UserApi(object):
    exposed = True

    # this can return username for searching other people.
    @cherrypy.tools.json_out()
    def GET(self):
        try:
            users = Users()
            return users.getUsers()
        except:
            return {'error': True, 'msg': "Error during request"}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST(self):
        users = Users()
        input_json = cherrypy.request.json
        users.createUser(input_json['username'], input_json['password'], email=input_json['email'])

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

@cherrypy.popargs('username', 'password')
class AuthApi(object):
    exposed = True

    # Get auth token back
    @cherrypy.tools.json_out()
    def GET(self, username, password):
        users = Users()
        if username and password:
            uid = users.authenticateUser(username=username, password=password)
            if uid:
                s = URLSafeSerializer(Config.cfg['auth']['key'])
                return {'error': False, 'msg': "No Error", 'token': s.dumps(['uid', 'username'])}
            else:
                raise cherrypy.HTTPError("403", "Not authenticated")
        return {'error': True, 'msg': "Error during request"}


if __name__ == '__main__':
    # Run the code to create the DB tables if they don't exists.
    # This is necessary for a fresh run of the application.
    tables = (Users, AboutUsers, Friendships, Messages)
    for table in tables:
        instance = table()
        instance.createIfNotExists()

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
    # Production mode is so that it does not display a stack trace to the users on 500 errors.
    #cherrypy.config.update({'environment': 'production'})
    cherrypy.tree.mount(SiteIndex(), '/', conf)
    cherrypy.tree.mount(SiteApi(), '/v1/', api_conf)
    cherrypy.tree.mount(SiteApi().user, '/user/', api_conf)
    cherrypy.tree.mount(SiteApi().msg, '/msg/', api_conf)
    cherrypy.tree.mount(SiteApi().user, '/friend/', api_conf)
    cherrypy.tree.mount(SiteApi().auth, '/auth/', api_conf)

    cherrypy.engine.start()
    cherrypy.engine.block()