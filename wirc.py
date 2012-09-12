# -*- coding: utf-8 -*-

import socket
import re
import botlog

FILE_LOG = "wirc.log"

class wIRC:
    """IRC client with minimal features"""

    def __init__(self, server, nick, port=6667, ident='wIRC', realname='wIRC bot', debug=False):
        self.server = server
        self.nick = nick
        self.port = port
        self.ident = ident
        self.realname = realname
        self.debug = debug
        self.log = botlog.Logger(botlog.Printer(), botlog.FileWriter(FILE_LOG))
        self.log.prefix = "WIRC"
        if not debug:
            self.log.enabled = False
        
        self.connected = False

    @property
    def debug(self):
        return self.debug

    @debug.setter
    def debug(self, value):
        self.debug = value
        self.log.enabled = value
        
    def connect(self):
        """Connect to server"""
        
        if self.connected:
            return
            
        self.connected = False
        try:
            self.sock = socket.socket()
            self.sock.connect((self.server, self.port))
            self.log.info("Connected to {}:{}!".format(self.server, self.port))
        except:
            self.log.error("Could not connect to {}!".format(self.server))
            return
            
        self.connected = True
        self.send_nick()
        self.send_user()
        
        self.on_connected()
            
    def run(self):
        """This has to be called after connecting!"""
        while True:
            self.doirc()
            
    def doirc(self):
        rdata = self.sock.recv(1024)
        lines = rdata.split("\n")

        for line in lines:
            if self.debug:
                self.log.recv(line)
            
            self.on_receive(line)
                
            line=line.rstrip()
            words=line.split(" ")

            if words[0] == "PING":
                self.send("PONG {0}\n".format(words[1]))
            elif len(words) > 1 and words[1] == "JOIN":
                nick, ident, server, channel = re.match(":(.*)!(.*)@(.*) JOIN (.*)", line).groups()
                self.log.debug(nick, ident, server, channel)
                if nick == self.nick:
                    self.on_me_join(channel)
                else:
                    self.on_join(nick, ident, server)
            elif len(words) > 1 and words[1] == "PRIVMSG":
                privmsgdata = re.match(":(.*)!(.*)@(.*) PRIVMSG (#.*) :(.*)", line).groups()
                nick = privmsgdata[0]
                ident = privmsgdata[1]
                server = privmsgdata[2]
                target = privmsgdata[3]
                msg = privmsgdata[4]
                
                self.on_privmsg(nick, ident, server, target, msg)
                    
    def disconnect(self):
        self.sock.disconnect()
        
    def quit(self):
        self.disconnect()

    def on_join(self, nick, ident, server):
        pass

    def on_receive(self, line):
        pass

    def on_connected(self):
        pass
        
    def on_privmsg(self, nick, ident, server, target, msg):
        pass
        
    def join(self, chan):
        self.send("JOIN {}\n".format(chan))
        #self.on_me_join(chan)

    def part(self, chan):
        self.send("PART {}\n".format(chan))
        
    def on_me_join(self, channel):
        pass
        
    def disconnect(self):
        if self.connected:
            self.sock.close()
            
    def send(self, data):
        self.sock.send(data)
        self.log.send(data)
        
    def msg(self, target, data):
        self.log.send("Msg: ({0}) {1}".format(target, data))
        self.sock.send("PRIVMSG {0} :{1}\n".format(target, data))
            
    def send_nick(self):
        self.send("NICK " + self.nick + "\n")
        
    def send_user(self):
        self.send("USER {0} {1} awsm :{2}\n".format(self.ident, self.server, self.realname))
