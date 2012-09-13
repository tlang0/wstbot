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
