# -*- coding: utf-8 -*-

import sys
import werkzeug.contrib.sessions
import pickle
import redis

from odoo import http
from odoo.odoo.tools.func import lazy_property

# Parameters for setup
session_duration = 604800
hostName = 'localhost'
hostPort = 6379

# class RedisSessionStore inherits from SessionStore
# implementes methods by using redis-py
class RedisSessionStore(werkzeug.contrib.sessions.SessionStore):

    def __init__(self, *args, **kwargs):
        super(RedisSessionStore, self).__init__(*args, **kwargs)
        self.expire = kwargs.get('expire', session_duration)
        self.redis = redis.Redis(host = hostName, port = hostPort)

    def _get_session_key(self, sid):
        if isinstance(sid, str):
            key = sid.encode('utf-8')
        return key

    def save(self, session):
        key = self._get_session_key(session.sid)
        # save data in dump to access it later
        data = pickle.dumps(dict(session))
        # setex saves session including expiration date
        self.redis.setex(name = key, value = data, time = self.expire)

    def get(self, sid):
        key = self._get_session_key(sid)
        data = self.redis.get(key)
        if data != None:
          self.redis.setex(name = key, value = data, time = self.expire)
          # load data from dump
          data = pickle.loads(data)
        else:
          data = {}
        return self.session_class(data, sid, False)

    def delete(self, session):
        key = self._get_session_key(session.sid)
        self.redis.delete(key)

    # ignore file unlink, because the session expires automatically
    def session_gc(self):
        pass

    # use Redis instead of session_dir as file store
    @lazy_property
    def session_store(self):
        return RedisSessionStore(session_class=http.OpenERPSession)

    # apply changes
    http.session_gc = session_gc
    http.Root.session_store = session_store