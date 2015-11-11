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

class AboutUsers(Database):
    def __init__(self):
        super(AboutUsers, self).__init__()

    # Update
    def UpdateAboutUserbyUID(self, uid, age, about_me, location, university):
        try:
            self.db_cursor.execute("UPDATE about_user SET age=?, about_me=?, location=?, university=? \
                WHERE uid=?", (age, about_me, location, university, uid))
        except Exception, e:
            raise e