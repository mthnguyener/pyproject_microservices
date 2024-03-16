PROJECT=pyproject_microservices
SERVICE=api_gateway

ifeq (,$(wildcard docker/.env))
    $(shell ln -s ../usr_vars docker/.env 2>/dev/null)
endif

ifneq (,$(wildcard usr_vars))
    include usr_vars
    export
endif

ifeq ("$(shell uname -s)", "Linux*")
	BROWSER=/usr/bin/firefox
else ifeq ("$(shell uname -s)", "Linux")
	BROWSER=/usr/bin/firefox
else
	BROWSER=open
endif

CONTAINER_PREFIX:=$(USER_NAME)_$(PROJECT)
DOCKER_CMD=docker
DOCKER_COMPOSE_CMD=docker compose
USER:=$(shell echo $${USER%%@*})
USER_ID:=$(shell id -u $(USER))
VERSION=$(shell echo $(shell cat $(SERVICE)/__init__.py | grep "^__version__" | cut -d = -f 2))

docs-first-run-delete:
	find docs -maxdepth 1 -type f -delete
	$(DOCKER_CMD) container exec $(CONTAINER_PREFIX)_$(SERVICE) \
		/bin/bash -c \
			"cd docs \
			 && sphinx-quickstart -q \
				-p $(SERVICE) \
				-a "Minh Nguyen" \
				-v $(VERSION) \
				--ext-autodoc \
				--ext-viewcode \
				--makefile \
				--no-batchfile"
	$(DOCKER_COMPOSE_CMD) -f ../../docker/docker-compose.yaml restart nginx
ifeq ("$(shell git remote)", "origin")
	git fetch
	git checkout origin/main -- docs/
else
	$(DOCKER_CMD) container run --rm \
		-v `pwd`:/usr/src/$(SERVICE) \
		-w /usr/src/$(SERVICE)/docs \
		ubuntu \
		/bin/bash -c \
			"sed -i -e 's/# import os/import os/g' conf.py \
			 && sed -i -e 's/# import sys/import sys/g' conf.py \
			 && sed -i \"/# sys.path.insert(0, os.path.abspath('.'))/d\" \
				conf.py \
			 && sed -i -e \"/import sys/a \
				from $(SERVICE) import __version__ \
				\n\nsys.path.insert(0, os.path.abspath('../$(SERVICE)'))\" \
				conf.py \
			 && sed -i -e \"s/version = '0.1.0'/version = __version__/g\" \
				conf.py \
			 && sed -i -e \"s/release = '0.1.0'/release = __version__/g\" \
				conf.py \
			 && sed -i -e \"s/alabaster/sphinx_rtd_theme/g\" \
				conf.py \
			 && sed -i -e 's/[ \t]*$$//g' conf.py \
			 && echo >> conf.py \
			 && sed -i \"/   :caption: Contents:/a \
				\\\\\n   package\" \
				index.rst"
endif

docs-init:
	@rm -rf pyproject_microservices/$(SERVICE)/docs/*
	@$(DOCKER_COMPOSE_CMD) -f ../../docker/docker-compose.yaml  up -d
	@$(DOCKER_CMD) container run --rm -v `pwd`:/usr/src/$(SERVICE) $(PROJECT)_$(SERVICE) \
		/bin/bash -c \
			"cd /usr/src/$(SERVICE)/docs \
			 && sphinx-quickstart -q \
				-p $(SERVICE) \
				-a "Minh Nguyen" \
				-v $(VERSION) \
				--ext-autodoc \
				--ext-viewcode \
				--makefile \
				--no-batchfile \
			 && cd .. \
			 adduser --system --no-create-home --uid $(USER_ID) --group $(USER) &> /dev/null \
			 chown -R $(USER):$(USER) docs"
	@git fetch
	@git checkout origin/main -- pyproject_microservices/$(SERVICE)/docs/
