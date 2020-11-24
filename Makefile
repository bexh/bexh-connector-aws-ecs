#!make

export PYTHON_VERSION := 3.7.7

#SHELL := /bin/bash

install-dev:
	@+pipenv install --python ${PYTHON_VERSION} --dev

install:
	@+pipenv install --python ${PYTHON_VERSION}

.PHONY: test
test:
	pipenv run pytest

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

local-setup:
	python scripts/local_setup.py

local-setup:
	python scripts/local_setup.py
