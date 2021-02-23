# -*- coding: utf-8 -*-

class User(object):
    cid = 1

    def __init__(self, uid, uname, content, timestamp,
                 hashhex="", hashint=""):
        self.id = User.cid
        self.uid = uid
        self.uname = uname
        self.content = content
        self.timestamp = timestamp
        self.hashhex, self.hashint = hashhex, hashint
        User.cid += 1
