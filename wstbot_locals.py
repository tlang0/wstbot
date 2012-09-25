########################################################################
# Copyright 2012 wst, wstcode@gmail.com
#
# This file is part of wstbot.
#
# wstbot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wstbot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with wstbot.  If not, see <http://www.gnu.org/licenses/>.
########################################################################

import os

BACKUP_PATH = "backup"
DATA_PATH = "data"

# server paths
SERVER_PATH = "botserver" # changing this will lead to problems
SERVER_CONFIG_PATH = os.path.join(SERVER_PATH, "cherryserver.conf")
TEMPLATES_PATH = os.path.join(SERVER_PATH, "templates")
DESCRIPTION_PATH = os.path.join(SERVER_PATH, "modules.yaml")
