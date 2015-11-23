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
import itsdangerous
import pprint
import time

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

class ApiEndpoint(object):

    def check_token(self, token):
        """
        Verifies the token. If the token is valid it will return the UID from the token. If it
        is invalid, it will return False.

        :param token:
        :return:
        """
        s = URLSafeSerializer(Config.cfg['auth']['key'])
        try:
            unserialized = s.loads(token)
            return int(unserialized[0])
        except itsdangerous.BadSignature:
            # If the token is not valid.
            logger.debug('User unauthorized.')
            return False

    def authenticate(self, token):
        """
        Returns the UID of the user if the token is valid.
        :param token:
        :return:
        """
        uid = self.check_token(token)
        user = Users()
        if user.getUserByUID(str(uid)):
            return uid
        else:
            logger.debug('Token data invalid. User unauthorized.')
            raise cherrypy.HTTPError("403", "Unauthorized")

    def standardize_json(self, json):
        if type(json) is list:
            pprint.pprint(json)
            return json[0]
        elif type(json) is dict:
            return json

class SiteApi(object):
    exposed = True

    def __init__(self):
        self.user = UserApi()
        self.msg = MessageApi()
        self.auth = AuthApi()
        self.friend = FriendApi()

#Create User
#Updates user
@cherrypy.popargs('token', 'uid')
class UserApi(ApiEndpoint):
    exposed = True

    # this can return username for searching other people.
    @cherrypy.tools.json_out()
    def GET(self,token, uid=None):
        """
        This method needs to be limited based on something like UID, Name, etc.

        Example GET looks like: http://garrulous.xyz/v1/user/WzEsInJpY2t5cmVtIl0.obTFbBDPmTY8Ve2e362d-UvArrc

        Example GET based on username looks like:
            http://garrulous.xyz/v1/user/WzEsInJpY2t5cmVtIl0.obTFbBDPmTY8Ve2e362d-UvArrc/2
        :return:
        """
        uid = self.authenticate(token)
        try:
            users = Users()
            if uid:
                return users.getUserByUID(uid)
            else:
                return users.getUsers()
        except:
            return {'error': True, 'msg': "Error during request"}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST(self):
        """
        No Authentication here yet. They will need to use the app to create an account, or the website.

        Example POST looks like: http://localhost:8080/v1/user
        HEADER: Content-Type: application/json
        BODY: { "username": "rickyrem", "password":"blahblah", "email":"ricky@ricky.com" }
        :return:
        """

        users = Users()
        json = self.standardize_json(cherrypy.request.json)
        #pprint.pprint(json)
        if users.createUser(user_name=json['user_name'], password=json['password'],
                            first_name=json['first_name'], last_name=json['last_name']):
            return {'error': False, 'msg': "message sent"}
        else:
            return {'error': True, 'msg': "Error during request"}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    # For creating a new user
    def PUT(self, token):
        """
        This is used to update profile information. As HTTP PUT usage requires, the JSON in needs to have all of the
        profile information. It cannot have only a single piece to be updated.

        :return:
        """
        uid = self.authenticate(token)
        json = self.standardize_json(cherrypy.request.json)
        users = Users()
        if uid:
            if users.updateUserByUid(uid, user_name=json['username'], password=json['password'],
                                     first_name=json['first_name'], last_name=json['last_name'], ):
                return {'error': True, 'msg': "Updated user information for %s" % json['username']}
        return {'error': True, 'msg': "Error during request"}

    @cherrypy.tools.json_out()
    def DELETE(self):
        return {'error': True, 'msg': "Error during request"}

class FriendApi(ApiEndpoint):
    exposed = True

    # get lists of friends for this user
    @cherrypy.tools.json_out()
    def GET(self):
        return {'error': True, 'msg': "Error during request"}

    # Add person to friends list
    @cherrypy.tools.json_out()
    def POST(self):
        return {'error': True, 'msg': "Error during request"}

    # remove person from friends list
    @cherrypy.tools.json_out()
    def DELETE(self):
        return {'error': True, 'msg': "Error during request"}

# Create Message
# Get Message
@cherrypy.popargs('token', 'to_uid', 'start_count', 'end_count')
class MessageApi(ApiEndpoint):
    exposed = True

    @cherrypy.tools.json_out()
    def GET(self, token, to_uid=None, start_count=None, end_count=None):
        """
        Return messages to the client.

        Doing a GET with only a token will return all the people they have talked to.
        Doing a GET with the UID will result in them actually getting message from that thread.

        :return:
        """

        from_uid = self.authenticate(token)
        msg = Messages()

        if to_uid:
            if start_count and end_count:
                data = msg.getMessageThread(from_uid, to_uid, start_count, end_count)
            else:
                data = msg.getMessageThread(from_uid, to_uid)
        else:
            data = msg.getUsersMessaged(from_uid)

        if data:
            return data
        else:
            return {'error': True, 'msg': "Error during request"}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST(self, token):
        """
        Creates a new message.

        :return:
        """
        uid = self.authenticate(token)
        json = self.standardize_json(cherrypy.request.json)

        msg = Messages()
        times = int(time.time())

        if msg.createMessage(uid, json['to_id'], json['message'], times):
            return {'error': False, 'msg': "message sent"}
        return {'error': True, 'msg': "Error during request"}

@cherrypy.popargs('username', 'password')
class AuthApi(ApiEndpoint):
    exposed = True

    # Get auth token back
    @cherrypy.tools.json_out()
    def GET(self, username, password):
        """
        Get the token to be used for authentication with the other endpoints.

        :param username:
        :param password:
        :return:
        """
        users = Users()
        if username and password:
            uid = users.authenticateUser(username=username, password=password)
            if uid:
                s = URLSafeSerializer(Config.cfg['auth']['key'])
                return {'error': False, 'msg': "No Error", 'token': s.dumps([uid, username])}
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