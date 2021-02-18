FROM eu.gcr.io/management-42nerds/gitpod-odoo:13-1.1

RUN pip install redis
# RUN curl -fsSL http://download.redis.io/redis-stable.tar.gz | tar xzs
# RUN cd redis-stable && sudo make install
