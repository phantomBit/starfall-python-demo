# Starfall Project

A demo API in Python3 using Tornado

Some code for server init and api handling came from open source projects and other exmaples 
as a base but highly modified for this specific usecase. This is my first ground up python API using tornado.

## Setup and Install

This package requires some pre-reqs.
* python 3.8
* python-venv
* sqlite3

If you do not have poetry installed globally, this script will add it as well as create the python venv
```bash
make pre-req
```

To run the env from nothing
```bash
make first-init startup
```
then goto http://localhost:8090/

for subsequent restarts run
```bash
make startup
```

## Useful Commands

Always check the Makefile for more in depth commands and env variables

#### Cleanup the env
```bash
make clean-all
```

#### Build
```bash
make build
```

#### Server
Starts the server with the env vars set in the make file.
```bash
make server
```