# Imports
import sys
import werkzeug.contrib.sessions
import pickle
import redis

from redis.sentinel import Sentinel
from odoo import http
from odoo.tools.func import lazy_property

# Parameters for setup
session_duration = 604800
hostName = 'rfs-redisfailover.default.svc.cluster.local'
hostPort = 26379

# Get sentinel
sentinel_service = Sentinel([(hostName, hostPort)], socket_timeout=0.1)

# Class RedisSessionStore inherits from SessionStore from werkzeug
# Methods are overwritten by using redis-py
class RedisSessionStore(werkzeug.contrib.sessions.SessionStore):

    # Get master from sentinel
    def _get_master(self, sentinel):
        return sentinel.discover_master('mymaster')

    def _connect_to_redis(self):
        # Connect to sentinel master
        master = self._get_master(sentinel_service)
        self.redis = redis.Redis(host = master[0], port = master[1])

    # Initialize session store
    def __init__(self, *args, **kwargs):
        super(RedisSessionStore, self).__init__(*args, **kwargs)
        self.expire = kwargs.get('expire', session_duration)
        # Connect to available redis-master
        self._connect_to_redis()

    # Returns session key
    def _get_key(self, sid):
        if isinstance(sid, str):
            key = sid.encode('utf-8')
        return key

    # Save a session
    def save(self, session):
        # Connect to available redis-master
        self._connect_to_redis()

        key = self._get_key(session.sid)
        # Save data in dump to access it later
        data = pickle.dumps(dict(session))
        # Setex saves session including expiration date
        self.redis.setex(name = key, value = data, time = self.expire)

    # Get a session for sid or create a new one if sid is not valid
    def get(self, sid):
        # Connect to available redis-master
        self._connect_to_redis()

        key = self._get_key(sid)
        data = self.redis.get(key)
        if data != None:
          self.redis.setex(name = key, value = data, time = self.expire)
          # Load data from dump
          data = pickle.loads(data)
        else:
          data = {}
        return self.session_class(data, sid, False)

    # Delete a session
    def delete(self, session):
        # Connect to available redis-master
        self._connect_to_redis()
        
        key = self._get_key(session.sid)
        self.redis.delete(key)

    # Ignore file unlink, because the session expires automatically
    def session_gc(self):
        pass

    # Use Redis as session storage instead of filestore
    @lazy_property
    def session_store(self):
        return RedisSessionStore(session_class=http.OpenERPSession)
    
    # Apply file unlink ignortion
    http.session_gc = session_gc
    # Apply changes by overwriting the session store
    http.Root.session_store = session_store