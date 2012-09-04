import os

class Logger(object):
    """Simple logging class"""

    def __init__(self, *outputs):
        self.outputs = None
        if outputs is not None and len(outputs) > 0:
            self.outputs = outputs

    def add_output(self, output):
        if output is not None:
            try:
                output.write
                self.outputs.append(output)
            except NameError:
                print("Output handler has no write method!")

    def write(self, message):
        for output in self.outputs:
            output.write(message)

    def info(self, message):
        self.write(message)

    def warn(self, message):
        self.write("WARNING: " + message)

    def error(self, message):
        self.write("ERROR: " + message)

    def recv(self, message):
        self.write("<- " + message)

    def send(self, message):
        self.write("-> " + message)

    def close(self):
        for output in self.outputs:
            try:
                output.close()
            except NameError:
                pass

class Printer(object):

    def write(self, message):
        print(message)

class FileWriter(object):

    def __init__(self, filename):
        self.fp = open(filename, "w")

    def write(self, message):
        self.fp.write(message + os.linesep)

    def close(self, message):
        self.fp.close()
