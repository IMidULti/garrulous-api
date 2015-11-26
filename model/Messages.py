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
import sqlite3
import logging
import pprint

from Database import Database

class Messages(Database):
    def __init__(self):
        super(Messages, self).__init__()

    # Crate Message Database if not exist.
    def createIfNotExists(self):
        self.write("""CREATE TABLE IF NOT EXISTS `messages` (
          `id` INTEGER PRIMARY KEY AUTOINCREMENT,
          `uid_message_from` INTEGER,
          `uid_message_to` INTEGER,
          `message` TEXT,
          `is_read` TEXT,
          `date_time` INTEGER
        )""")

    def getMessageById(self, id):
        rows = self.query('SELECT id, uid_message_from, uid_message_to, message, '
                          'is_read, date_time FROM messages where id = %s' % id)
        objects_list = []
        for row in rows:
            d = collections.OrderedDict()
            d['id'] = row[0]
            d['uid_message_from'] = row[1]
            d['uid_message_to'] = row[2]
            d['message'] = row[3]
            d['is_read'] = row[4]
            d['date_time'] = row[5]
        return objects_list

    def updateMessageById(self, id, message=None, datetime=None, id_read=None):
        pass

    def createMessage(self, from_id, to_id, message, datetime):
        if self.write('INSERT INTO MESSAGES (uid_message_from, uid_message_to, message, is_read, date_time) VALUES '
                   '(?,?,?,?,?)', (from_id, to_id, message, 0, datetime)):
            return True
        return False

    # Read Messages By User IDs.
    def getMessageThread(self, from_id, to_id, start_count=None, end_count=None):
        if start_count and end_count:
            rows = self.query('SELECT uid_message_from, uid_message_to, message, '
                               'is_read, date_time FROM messages WHERE '
                               '(uid_message_to=? AND uid_message_from=?) OR'
                               '(uid_message_from=? AND uid_message_to=?)'
                               'LIMIT ?, ?;',
                               (to_id, from_id, to_id, from_id, str(int(start_count) - 1), end_count))
        else:
            rows = self.query('SELECT uid_message_from, uid_message_to, message, '
                                   'is_read, date_time FROM messages WHERE '
                                   '(uid_message_to=? AND uid_message_from=?) OR'
                                   '(uid_message_from=? AND uid_message_to=?)',
                                   (to_id, from_id, to_id, from_id))
        objects_list = []
        for row in rows:
            d = collections.OrderedDict()
            d['uid_message_from'] = row[0]
            d['uid_message_to'] = row[1]
            d['message'] = row[2]
            d['is_read'] = row[3]
            d['date_time'] = row[4]
            objects_list.append(d)
        return objects_list

    def getUsersMessaged(self, uid):
        """
        Returns a relation between to people.

        :param uid:
        :return:
        """

        rows = self.query('SELECT DISTINCT uid_message_from, uid_message_to FROM messages WHERE '
                          'uid_message_to=? or uid_message_from=? '
                          'GROUP BY uid_message_to, uid_message_from;',
                          (uid, uid))
        for row in rows:
            pass
        objects_list = []
        for row in rows:
            d = collections.OrderedDict()
            d['uid_message_from'] = row[0]
            d['uid_message_to'] = row[1]
            objects_list.append(d)
        return objects_list