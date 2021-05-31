#!/bin/sh
echo Initialize database
export DB_ENDPOINT=postgresql://postgres:postgres@localhost
flask db init
flask db migrate
flask db upgrade