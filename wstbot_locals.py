import os

BACKUP_PATH = "backup"
DATA_PATH = "data"

# server paths
SERVER_PATH = "botserver" # changing this will lead to problems
SERVER_CONFIG_PATH = os.path.join(SERVER_PATH, "cherryserver.conf")
TEMPLATES_PATH = os.path.join(SERVER_PATH, "templates")
DESCRIPTION_PATH = os.path.join(SERVER_PATH, "modules.yaml")
