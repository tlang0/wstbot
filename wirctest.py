#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Salami/wst

import wirc

class myIRC(wirc.wIRC):
    def __init__(self):
        wirc.wIRC.__init__(self, "irc.quakenet.org", "wstbottest", port=6667, ident='wIRC', realname='wIRC bot', debug=True)
        
    def on_receive(self, line):
        if "End of" in line and "376" in line:
            self.join("#hibforum")

if __name__ == '__main__':
    myirc = myIRC()
    myirc.connect()
