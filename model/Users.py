# Garrulous API
# Authors: Michael Pierre and Richard Meyers

"""
Copyright (C) 2015

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
import hashlib
import time
import logging
import pprint

from Database import Database

class Users(Database):
    def __init__(self):
        super(Users, self).__init__()

    # Create user table is not exist.    
    def createIfNotExists(self):
        self.write("""CREATE TABLE IF NOT EXISTS `users` (
          `uid` INTEGER PRIMARY KEY AUTOINCREMENT,
          `username` TEXT,
          `first_name` TEXT,
          `last_name` TEXT,
          `email` TEXT,
          `phone` TEXT,
          `password` TEXT,
          `date_joined` INTEGER
        )""")

    # Create
    # Create New User
    def createUser(self, user_name="", password="", first_name="", last_name="", email="", phone=""):
        #This time is the date they joined
        times = int(time.time())
        hash = hashlib.md5(password)
        hashword = hash.hexdigest()

        if self.username_exists(user_name):
            return "Username already taken"

        if self.write("INSERT INTO users (username,first_name,last_name,email,password,phone,date_joined) "
                      "VALUES (?,?,?,?,?,?,?) ", (user_name, first_name, last_name, email, hashword,
                      phone, times)):
            return True
        return False


    def updateUserByUid(self, uid, user_name=None, password=None, first_name=None, last_name=None, email=None,
                        phone=None):
        # This needs to build the query out of the amount of parameters that exist. That way a all the existing
        # data doesn't get overwritten.
        if self.write('UPDATE users SET user_name=?, password=?, first_name=?, last_name=? '
                      'WHERE uid=?', (user_name, password, first_name, last_name)):
            return True
        return False


    def authenticateUser(self, user_name="", password="", phone="", email=""):
        hash = hashlib.md5(password)
        hashword = hash.hexdigest()
        # This gets the one row and returns only the first column
        try:
            rows = self.queryOne("SELECT uid FROM users WHERE username = ? and password = ?", (user_name, hashword))[0]
        except TypeError:
            return False
        return rows

    def username_exists(self, username):
        """
        Check if this username exists already.
        :param username:
        :return:
        """
        try:
            ifexist = self.queryOne("SELECT username FROM users WHERE username = ?", (username,))[0]
        except TypeError:
            return False
        if ifexist:
            return True
        return False

    # Read All Users
    def getUsers(self):
        # We are not returning all the rows
        # We definitely don't want to return the password column, that is only used for auth.
        # There should be the option of passing in the row quantity.
        rows = self.query("SELECT uid, username, first_name, last_name, email FROM users")
        objects_list = []
        for row in rows:
            d = collections.OrderedDict()
            d['uid'] = row[0]
            d['username'] = row[1]
            d['first_name'] = row[2]
            d['last_name'] = row[3]
            d['email'] = row[4]
            objects_list.append(d)
        return objects_list

    def getUsersLike(self, search):
        search = "%" + search + "%"
        rows = self.query("SELECT uid, username, first_name, last_name FROM users WHERE username LIKE ? OR first_name LIKE ? OR last_name LIKE ? LIMIT 20", (search, search, search,))
        objects_list = []
        for row in rows:
            d = collections.OrderedDict()
            d['uid'] = row[0]
            d['username'] = row[1]
            d['first_name'] = row[2]
            d['last_name'] = row[3]
            objects_list.append(d)
        return objects_list

    # Read User Information By User ID.
    def getUserByUID(self, uid):
        uid = str(uid)
        row = self.queryOne("SELECT uid, username, first_name, last_name, email FROM users WHERE uid=?", (uid))
        d = {}
        d['uid'] = row[0]
        d['username'] = row[1]
        d['first_name'] = row[2]
        d['last_name'] = row[3]
        d['email'] = row[4]
        return d

    # Read User Information By Username.
    def getUserByUsername(self, username):
        row = self.queryOne("SELECT uid, username, first_name, last_name, email FROM users WHERE username=%s" % username)
        d = {}
        d['uid'] = row[0]
        d['username'] = row[1]
        d['first_name'] = row[2]
        d['last_name'] = row[3]
        d['email'] = row[4]
        return d