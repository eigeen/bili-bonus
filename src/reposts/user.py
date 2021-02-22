# -*- coding: utf-8 -*-

class RepostUser(object):
    cid = 1

    def __init__(self, uid, uname, content, timestamp):
        self.id = RepostUser.cid
        self.uid = uid
        self.uname = uname
        self.content = content
        self.timestamp = timestamp
        RepostUser.cid += 1
