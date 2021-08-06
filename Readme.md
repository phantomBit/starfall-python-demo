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

## Evaluations

Flake8 Results
```
(venv) zanson@Gibson: ~/projects/starfall [master▲]
./venv/bin/flake8 ./starfall/
(venv) zanson@Gibson: ~/projects/starfall [master▲]

```

Bandit Results
```
$ bandit -r ./starfall
[main]	INFO	profile include tests: None
[main]	INFO	profile exclude tests: None
[main]	INFO	cli include tests: None
[main]	INFO	cli exclude tests: None
[main]	INFO	running on Python 3.8.10
Run started:2021-08-06 23:44:12.500179

Test results:
	No issues identified.

Code scanned:
	Total lines of code: 313
	Total lines skipped (#nosec): 0

Run metrics:
	Total issues (by severity):
		Undefined: 0.0
		Low: 0.0
		Medium: 0.0
		High: 0.0
	Total issues (by confidence):
		Undefined: 0.0
		Low: 0.0
		Medium: 0.0
		High: 0.0
Files skipped (0):

```