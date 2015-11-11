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

import collections
import json

from database import Database

class Users(Database):
    def __init__(self):
        super(Users, self).__init__()

    # Create
    # Create New User
    def CreateUser(self, first_name, last_name, email, password):
        try:
            self.db_cursor.execute("INSERT INTO users (first_name,last_name,email,password) \
                VALUES (?,?,?,?) ", (first_name, last_name, email, password))
        except Exception, e:
            raise e


    def UpdateUserByUID(self, uid, first_name, last_name, email, password):
        try:
            self.db_cursor.execute("UPDATE users SET first_name=?, last_name=?, email=?, password=? \
                WHERE uid=?", (first_name, last_name, email, password, uid))
        except Exception, e:
            raise e

    # Read
    # Read All Users
    def ReadUsers(self):
        self.db_cursor.execute("SELECT uid, first_name, last_name, email, password FROM users")
        rows = self.db_cursor.fetchall()
        objects_list = []
        for row in rows:
            d = collections.OrderedDict()
            d['uid'] = row[0]
            d['first_name'] = row[1]
            d['last_name'] = row[2]
            d['email'] = row[3]
            d['password'] = row[4]
            objects_list.append(d)
        return json.dumps(objects_list)

    # Read User Information By User ID.
    def ReadUserByUID(self,uid):
        uid = (uid,)
        self.db_cursor.execute('SELECT uid, first_name, last_name, email, password FROM users WHERE uid=?', uid)
        rows = self.db_cursor.fetchall()
        objects_list = []
        for row in rows:
            d = collections.OrderedDict()
            d['uid'] = row[0]
            d['first_name'] = row[1]
            d['last_name'] = row[2]
            d['email'] = row[3]
            d['password'] = row[4]
            objects_list.append(d)
        return json.dumps(objects_list)

    # Read About User By User ID.
    def ReadAboutUserByUID(self, uid):
        self.db_cursor.execute('SELECT age, about_me, location, university FROM about_user WHERE uid=?', (uid))
        rows = self.db_cursor.fetchall()
        objects_list = []
        for row in rows:
            d = collections.OrderedDict()
            d['age'] = row[0]
            d['about_me'] = row[1]
            d['location'] = row[2]
            d['university'] = row[3]
            objects_list.append(d)
        return json.dumps(objects_list)