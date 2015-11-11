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
import sqlite3

from Database import Database

class Users(Database):
    def __init__(self):
        super(Users, self).__init__()

    def createIfNotExists(self):
        """
        CREATE TABLE IF NOT EXISTS `garrulous`.`Users` (
          `id` INT(11) NOT NULL,
          `username` VARCHAR(45) NOT NULL,
          `datejoined` INT NOT NULL,
          `email` VARCHAR(45) NULL,
          `firstname` VARCHAR(45) NULL,
          `lastname` VARCHAR(45) NULL,
          `password` VARCHAR(45) NOT NULL,
          `phone` INT NULL,
          PRIMARY KEY (`id`),
          UNIQUE INDEX `userId_UNIQUE` (`id` ASC))
        ENGINE = InnoDB
        :return:
        """
        pass

    # Create
    # Create New User
    def createUser(self, user_name, password, first_name=None, last_name=None, email=None, phone=None):
        #set the datejoined column from inside this method
        try:
            self.db_cursor.execute("INSERT INTO users (first_name,last_name,email,password) \
                VALUES (?,?,?,?) ", (first_name, last_name, email, password))
        except Exception, e:
            raise e


    def updateUserByUid(self, uid, user_name=None, password=None, first_name=None, last_name=None, email=None,
                        phone=None):
        try:
            self.db_cursor.execute("UPDATE users SET first_name=?, last_name=?, email=?, password=? \
                WHERE uid=?", (first_name, last_name, email, password, uid))
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

