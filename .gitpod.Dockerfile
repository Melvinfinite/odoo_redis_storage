FROM eu.gcr.io/management-42nerds/gitpod-odoo:13-1.1

RUN sudo apt-get update -q && \
    sudo apt-get install -yq redis-server