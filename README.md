wstbot
======

Wstbot is a chat bot for IRC and XMPP (Jabber) with modular features.
It is developed by wst, wstcode@gmail.com.

Dependencies
------------

* python 3.1+
* cherrypy
* pyyaml
* sleekxmpp for xmpp

Installation
------------

* Edit wstbot.conf.EXAMPLE and rename it to wstbot.conf.
* Rename data/regex.yaml.EXAMPLE to data/regex.yaml (and add some sites if you want to).
* Modules may have their own setup scripts. Run this to execute all of them:

  $ python3 setup.py

Usage
-----

Wstbot consists of 3 Parts:
* A chat bot, which is the main part. There is a Jabber and an IRC version.
* A web application server that is used by some of the main modules in wstbot.
* A control interface that lets you start and stop the bot and the server.

The most comfortable way to run wstbot is to just start the control interface and use that.
Run it like this:

$ python3 -m botserver.control_interface

Then visit http://localhost:8112/ in a web browser (8112 is the default port).

---

You can also start everything manually:

To start the server, run:

    python3 -m botserver.server

To start the IRC bot, run:

    python3 -m wstbot_irc

To start the XMPP bot, run:

    python3 -m wstbot_xmpp

License
-------

Wstbot is licensed unter the GPLv3, which can be found in the COPYING 
file.
