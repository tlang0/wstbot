import os

class Logger:
    """Simple logging class"""

    def __init__(self, *outputs):
        self.outputs = None
        self.prefix = ""
        self.enabled = True
        if outputs is not None and len(outputs) > 0:
            self.outputs = outputs

    def add_output(self, output):
        if output is not None:
            # check for write method
            try:
                output.write
                self.outputs.append(output)
            except NameError:
                print("Output handler has no write method!")

    def write(self, message):
        if not self.enabled:
            return

        for output in self.outputs:
            output.write(self.prefix + " " + message)

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

    def debug(self, message):
        self.write("DEBUG: " + message)

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
