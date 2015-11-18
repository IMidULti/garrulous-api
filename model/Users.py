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

from Database import Database

class Users(Database):
    def __init__(self):
        super(Users, self).__init__()

    # Create user table is not exist.    
    def createIfNotExists(self):
        self.write("""CREATE TABLE IF NOT EXISTS `users` (
          `uid` INTEGER PRIMARY KEY AUTOINCREMENT,
          `first_name` TEXT,
          `last_name` TEXT,
          `email` TEXT,
          `password` TEXT
        )""")

    # Create
    # Create New User
    def createUser(self, user_name, password, first_name=None, last_name=None, email=None, phone=None):
        #set the datejoined column from inside this method
        self.write("INSERT INTO users (first_name,last_name,email,password) "
                   "VALUES (%s,%s,%s,%s) " % (first_name, last_name, email, password))


    def updateUserByUid(self, uid, user_name=None, password=None, first_name=None, last_name=None, email=None,
                        phone=None):
        try:
            self.db_cursor.execute("UPDATE users SET first_name=?, last_name=?, email=?, password=? \
                WHERE uid=?", (first_name, last_name, email, password, uid))
            self.db_cursor.commit()
        except Exception, e:
            raise e

    # Read
    # Read All Users
    def getUsers(self):
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
        return objects_list

    # Read User Information By User ID.
    def getUserByUID(self, uid):
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
        return objects_list

