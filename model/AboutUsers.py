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

class AboutUsers(Database):
    def __init__(self):
        super(AboutUsers, self).__init__()

    def createIfNotExists(self):
        """
        CREATE TABLE IF NOT EXISTS `garrulous`.`AboutUsers` (
          `id` INT(11) NOT NULL AUTO_INCREMENT,
          `title` VARCHAR(45) NOT NULL,
          `text` LONGTEXT NULL,
          `userid` INT(11) NOT NULL,
          PRIMARY KEY (`id`, `userid`),
          INDEX `fk_AboutUsers_Users1_idx` (`userid` ASC),
          CONSTRAINT `fk_AboutUsers_Users1`
            FOREIGN KEY (`userid`)
            REFERENCES `garrulous`.`Users` (`id`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION)
        ENGINE = InnoDB
        """
        pass

    def createAboutUser(self, uid, title, content):
        pass

    def getAboutUserById(self, id):
        pass

    def getAboutUserByUserIdAndTitle(self, uid, title):
        pass

    # Update
    # Not done
    def setAboutUserByUid(self, uid, title, content):
        """
        try:
            self.db_cursor.execute("UPDATE AboutUser SET age=?, about_me=?, location=?, university=? \
                WHERE uid=?", (age, about_me, location, university, uid))
        except sqlite3.IntegrityError, e:
            raise e
        except sqlite3.Error, e:
            raise e
        """
        pass

        # Read About User By User ID.
    def getAboutUserByUid(self, uid):
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
        return objects_list