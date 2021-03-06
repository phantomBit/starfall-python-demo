## ENV
STARFALL_DATABASE=./starfall.sqlite
STARFALL_PORT=8090

## ----------------------
## PRE REQ INSTALLS
## ----------------------
pre-req: pre-req/poetry install

pre-req/poetry:
	@type poetry >/dev/null 2>&1 ||  pip install poetry

env/init:
	python3 -m venv ./venv

install:
	poetry install

## ----------------------
## RUNNING SCRIPTS
## ----------------------
env/activate:
	poetry shell

sqlite/init:
	sqlite3 ${STARFALL_DATABASE} <./tables.sql

sqlite/destroy:
	rm ${STARFALL_DATABASE}

build:
	poetry build

server:
	export STARFALL_PORT=${STARFALL_PORT} \
	STARFALL_DATABASE=${STARFALL_DATABASE} \
	&& poetry run starfall server

flake:
	./venv/bin/flake8 ./starfall/

## ----------------------
## QUICK COMMANDS
## ----------------------

first-init: env/activate sqlite/init

startup: build server

clean-all: sqlite/destroy

nuke: sqlite/destroy
	rm -rf ./venv
	rm -rf dist