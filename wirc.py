# -*- coding: utf-8 -*-

import socket, re

class wIRC(object):

    def __init__(self, server, nick, port=6667, ident='wIRC', realname='wIRC bot', debug=False):
        self.server = server
        self.nick = nick
        self.port = port
        self.ident = ident
        self.realname = realname
        self.debug = debug
        
        self.connected = False
        
    def connect(self):
        """Connect to server"""
        
        if self.connected:
            return
            
        self.connected = False
        try:
            self.sock = socket.socket()
            self.sock.connect((self.server, self.port))
            self.dbg_info("Connected to %s:%s!" % (self.server, self.port))
        except:
            self.dbg_error("Could not connect to %s!" % self.server)
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
                self.dbg_incoming(line)
            
            self.on_receive(line)
                
            line=line.rstrip()
            words=line.split(" ")

            if words[0] == "PING":
                self.send("PONG %s\n" % words[1])
            elif len(words) > 1 and words[1] == "JOIN":
                nick, ident, server, channel = re.match(":(.*)!(.*)@(.*) JOIN (.*)", line).groups()
                print nick, ident, server, channel
                if nick == self.nick:
                    self.on_me_join(channel)
                else:
                    self.on_join(nick, ident, server)
            elif len(words) > 1 and words[1] == "PRIVMSG":
                try:
                    privmsgdata = re.match(":(.*)!(.*)@(.*) PRIVMSG (#.*) :(.*)", line).groups()
                    nick = privmsgdata[0]
                    ident = privmsgdata[1]
                    server = privmsgdata[2]
                    target = privmsgdata[3]
                    msg = privmsgdata[4]
                except:
                    print "Could not parse link!"
                
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
        self.dbg_outgoing(data)
        
    def msg(self, target, data):
        self.dbg_outgoing("Msg: (%s) %s" % (target, data))
        self.sock.send("PRIVMSG %s :%s\n" % (target, data))
            
    def send_nick(self):
        self.send("NICK " + self.nick + "\n")
        
    def send_user(self):
        self.send("USER %s %s bla :%s\n" % (self.ident, self.server, self.realname))
                
    # debug output
            
    def dbg_info(self, debugstr):
        if self.debug:
            print "WIRC (*) " + debugstr
            
    def dbg_error(self, debugstr):
        if self.debug:
            print "WIRC [!] " + debugstr
            
    def dbg_incoming(self, debugstr):
        if self.debug:
            br = debugstr.find('\n')
            if br != -1:
                leftover = debugstr[br+1:len(debugstr)-1]
                debugstr = debugstr[0:br]

            if debugstr.strip():
                print "WIRC <- " + debugstr;
                
            if br != -1:
                self.dbg_incoming(leftover)
            
    def dbg_outgoing(self, debugstr):
        if self.debug:
            print "WIRC -> " + debugstr;
        
