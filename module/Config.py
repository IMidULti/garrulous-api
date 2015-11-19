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

import yaml
import os

class Config:

    cfg = {}

    @staticmethod
    def load_config():
        etc_path = os.path.dirname(os.path.abspath(__file__))
        etc_path = os.path.join(os.path.dirname(etc_path), "etc")
        etc_path = os.path.join(etc_path, "garrulous.yml")
        with open(etc_path, 'r') as ymlfile:
            Config.cfg = yaml.load(ymlfile)
