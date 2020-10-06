#!/usr/bin/env bash

sudo psql -U postgres <<EOF
CREATE DATABASE django_platon;
CREATE USER django WITH PASSWORD 'django_password';
GRANT ALL PRIVILEGES ON DATABASE django_platon TO django;
ALTER USER django CREATEDB;
EOF

pip3 install -r requirements.txt
python3 manage.py migrate 

