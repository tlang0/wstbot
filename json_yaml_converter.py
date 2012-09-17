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

import json
import yaml

fp_json = open("REGEX", "r")
fp_yaml = open("regex.yaml", "w")

data = json.load(fp_json)

# new data
source_list = []
general = {"separator": "::"} # new output

for source in data:
    newsource = {"name": source[0], "url pattern": source[1]}
    patterns = []
    for i in range(2, len(source)):
        pattern = {"pattern": source[i]}
        if i == 2:
            color = "purple"
            description = "title or headline"
            style = "bold"
        else:
            color = "green"
            description = "secondary information"
            style = "default"
        pattern["description"] = description
        pattern["color"] = color
        pattern["style"] = style
        patterns.append(pattern)
    newsource["patterns"] = patterns
    source_list.append(newsource)

general["sources"] = source_list

yaml.dump(general, stream=fp_yaml, default_flow_style=False)

fp_json.close()
fp_yaml.close()
