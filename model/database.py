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

import sqlite3
import json
import os
import collections

class Database(object):
    def __init__(self):
        super(Database, self).__init__()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir + "../database", "garrulous.db")
        #Here just to debug the path of the db file
        print(db_path)
        self.conn = sqlite3.connect(db_path)
        self.db_cursor = self.conn.cursor()


    # Create User table if it does not exist.
    def CreateUserTable(self):
        self.db_cursor.execute("")

    # Create About User table if it does not exist.
    def CreateAboutUserTable(self):
        self.db_cursor.execute()

    # Create Friendship Table if it does not exist.
    def CreateFriendshipTable(self):
        self.db_cursor.execute()

    # Create Message Table if it does not exist.
    def CreateMessagesTable(self):
        try:
            self.db_cursor.execute("")
        except Exception, e:
            raise e
