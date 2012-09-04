import cherryserver

class Server(object):

    def __init__(self):
        self.dependency = "cherrypy"
        
    def start(self, port):
        cherryserver.start(port)

if __name__ == "__main__":
    Server().start(8111)
