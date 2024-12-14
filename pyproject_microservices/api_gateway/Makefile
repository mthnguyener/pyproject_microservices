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
DOCKER_IMAGE=$(shell head -n 1 ../../docker/$(SERVICE).Dockerfile | cut -d ' ' -f 2)
PKG_MANAGER=pip
SRC_DIR=/usr/src/$(SERVICE)
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
	$(DOCKER_COMPOSE_CMD) -f ../../docker/docker-compose.yaml restart $(PROJECT)-nginx
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
	@rm -rf docs/*
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
	@git checkout origin/main -- docs/

format-style:
	@$(DOCKER_CMD) container exec $(CONTAINER_PREFIX)_$(SERVICE) \
	yapf -i -p -r --style "pep8" ${SRC_DIR}

notebook: notebook-server
	@printf "%s\n" \
		"" \
		"" \
		"" \
		"####################################################################" \
		"Use this link on the host to access the Jupyter server." \
		""
	@$(DOCKER_CMD) container exec $(CONTAINER_PREFIX)_$(SERVICE) \
		/bin/bash -c \
			"jupyter lab list 2>&1 \
			 | grep -o 'http.*$(PORT_JUPYTER)\S*' \
			 | sed -e 's/\(http:\/\/\).*\(:\)/\1localhost:/' && \
			echo "" && \
	        jupyter lab list 2>&1 \
			 | grep -o 'http.*$(PORT_JUPYTER)\S*' \
			 | sed -e 's/\(http:\/\/\).*\(:\)[0-9]*\/?//'"
	@printf "%s\n" \
		"" \
		"####################################################################"

notebook-delete-checkpoints: docker-up
	@$(DOCKER_CMD) container exec $(CONTAINER_PREFIX)_$(SERVICE) \
		rm -rf `find -L -type d -name .ipynb_checkpoints`

notebook-server: notebook-stop-server
	@$(DOCKER_CMD) container exec $(CONTAINER_PREFIX)_$(SERVICE) \
		/bin/bash -c \
			"jupyter lab \
				--allow-root \
				--no-browser \
				--ServerApp.ip=0.0.0.0 \
				--ServerApp.port=$(PORT_JUPYTER) \
				--notebook-dir=/usr/src/$(SERVICE) \
				&"

notebook-stop-server:
	@-$(DOCKER_CMD) container exec $(CONTAINER_PREFIX)_$(SERVICE) \
		/bin/bash -c "jupyter lab stop $(PORT_JUPYTER)"

package-dependencies:
	@printf "%s\n" \
		"# ${SERVICE} Version: $(VERSION)" \
		"# From image: $(DOCKER_IMAGE)" \
		"#" \
		> package_requirements.txt
ifeq ("${PKG_MANAGER}", "conda")
	@$(DOCKER_CMD) container exec $(CONTAINER_PREFIX)_$(SERVICE) \
		/bin/bash -c \
			"conda list --export >> package_requirements.txt \
			 && sed -i -e '/^$(SERVICE)/ s/./# &/' package_requirements.txt"
else ifeq ("${PKG_MANAGER}", "pip")
	@$(DOCKER_CMD) container exec $(CONTAINER_PREFIX)_$(SERVICE) \
		/bin/bash -c \
			"pip freeze -l --exclude $(SERVICE) >> package_requirements.txt"
endif

profile:
	@$(foreach FILE,$(shell find $(SERVICE) -type f -name '*.py'), \
	    $(eval FILENAME := $(shell basename $(FILE))) \
		$(DOCKER_CMD) container exec $(CONTAINER_PREFIX)_$(SERVICE) \
			/bin/bash -c \
				"python -m cProfile -o profiles/$(FILENAME:.py=.prof) $(FILE)";)

snakeviz-server:
	@$(foreach FILE,$(shell find $(SERVICE) -type f -name '*.py'), \
	    $(eval FILENAME := $(shell basename $(FILE))) \
        $(DOCKER_CMD) container exec \
            -w /usr/src/$(SERVICE)/profiles \
            $(CONTAINER_PREFIX)_$(SERVICE) \
            /bin/bash -c \
                "snakeviz $(FILENAME:.py=.prof) \
                    --hostname 0.0.0.0 \
                    --port $(PORT_PROFILE) \
                    --server &";)

test: timestamp := $(shell date +"%Y%m%d_%H%M%S")
test:
	@$(DOCKER_CMD) container exec $(CONTAINER_PREFIX)_$(SERVICE)\
		sh -c 'py.test $(SERVICE) | tee -a logs/tests/$(SERVICE)-$(timestamp)_log.txt'

upgrade-packages:
ifeq ("${PKG_MANAGER}", "pip")
	$(DOCKER_CMD) container exec $(CONTAINER_PREFIX)_$(SERVICE) \
		/bin/bash -c \
			"pip3 install -U pip \
			 && pip3 freeze | \
				grep -v $(PROJECT) | \
				cut -d = -f 1 > new_requirements.txt \
			 && pip3 install -U -r new_requirements.txt \
			 && pip3 freeze > new_requirements.txt \
			 && sed -i -e '/^-e/d' new_requirements.txt"
else ifeq ("${PKG_MANAGER}", "conda")
	$(DOCKER_CMD) container exec $(CONTAINER_PREFIX)_$(SERVICE) \
		/bin/bash -c \
			"conda update conda \
			 && conda update --all \
			 && pip freeze > new_requirements.txt \
			 && sed -i -e '/^-e/d' new_requirements.txt"
endif
