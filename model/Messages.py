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

from Database import Database

class Messages(Database):
    def __init__(self):
        super(Messages, self).__init__()

    def createIfNotExists(self):
        """
        CREATE TABLE IF NOT EXISTS `garrulous`.`Messages` (
          `id` INT(20) NOT NULL,
          `message` LONGTEXT NOT NULL,
          `is_read` TINYINT NULL,
          `sent_datetime` INT(15) NULL,
          `uid_to` INT(11) NOT NULL,
          `uid_from` INT(11) NOT NULL,
          PRIMARY KEY (`id`, `uid_to`, `uid_from`),
          INDEX `fk_Messages_Users1_idx` (`uid_to` ASC),
          INDEX `fk_Messages_Users2_idx` (`uid_from` ASC),
          CONSTRAINT `fk_Messages_Users1`
            FOREIGN KEY (`uid_to`)
            REFERENCES `garrulous`.`Users` (`id`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
          CONSTRAINT `fk_Messages_Users2`
            FOREIGN KEY (`uid_from`)
            REFERENCES `garrulous`.`Users` (`id`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION)
        ENGINE = InnoDB
        :return:
        """
        pass

    def getMessageById(self, id):
        pass

    def updateMessageById(self, id, message=None, datetime=None, id_read=None):
        pass

    def createMessage(self, from_id, to_id, message, datetime):
        # Default is_read to false
        pass

    # Read Messages By User IDs.
    def getMessageThread(self, to_id, from_id, time_constraint=None):
        self.db_cursor.execute('SELECT uid_message_from, uid_message_to, subject, \
            message, is_read, date_time WHERE uid_message_to=? AND uid_message_from=?',
            (uid, sender_id))
        rows = self.db_cursor.fetchall()
        objects_list = []
        for row in rows:
            d = collections.OrderedDict()
            d['uid_message_from'] = row[0]
            d['uid_message_to'] = row[1]
            d['subject'] = row[2]
            d['is_read'] = row[3]
            d['date_time'] = row[4]
        return uid