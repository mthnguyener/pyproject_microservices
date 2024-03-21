PROJECT=pyproject_microservices

$(shell scripts/create_usr_vars.sh)
ifeq (, $(wildcard docker/.env))
        $(shell ln -s ../usr_vars docker/.env)
endif
include usr_vars
export

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
PKG_MANAGER=pip
TENSORBOARD_DIR:="ai_logs"
USER:=$(shell echo $${USER%%@*})
USER_ID:=$(shell id -u $(USER))

.PHONY: docs format-style prompt-service upgrade-packages

docker-down:
	@$(DOCKER_COMPOSE_CMD) -f docker/docker-compose.yaml down

docker-images-update:
	@$(DOCKER_CMD) image ls | grep -v REPOSITORY | cut -d ' ' -f 1 | xargs -L1 $(DOCKER_CMD) pull

docker-rebuild: setup.py
	@$(DOCKER_COMPOSE_CMD) -f docker/docker-compose.yaml up -d --build 2>&1 | tee docker/image_build.log

docker-up:
	@$(DOCKER_COMPOSE_CMD) -f docker/docker-compose.yaml up -d

# docker-update-config: docker-up docker-update-compose-file docker-rebuild
# 	@echo "Docker environment updated successfully"
#
# docker-update-compose-file:
# 	@$(DOCKER_CMD) container exec $(CONTAINER_PREFIX)_python scripts/docker_config.py

docs: docker-up
	@$(DOCKER_CMD) container exec $(CONTAINER_PREFIX)_api_gateway \
		/bin/bash -c "cd docs && sphinx-build -b html . _build"
	@$(DOCKER_CMD) container exec $(CONTAINER_PREFIX)_front_end \
		/bin/bash -c "cd docs && sphinx-build -b html . _build"
	@$(DOCKER_CMD) container exec $(CONTAINER_PREFIX)_model_serving \
		/bin/bash -c "cd docs && sphinx-build -b html . _build"
	@$(BROWSER) http://localhost:$(PORT_NGINX) 2>&1 &

docs-first-run-delete: docker-up
	@cd pyproject_microservices/api_gateway && make docs-first-run-delete
	@cd pyproject_microservices/front_end && make docs-first-run-delete
	@cd pyproject_microservices/model_serving && make docs-first-run-delete

docs-init:
	@-cd pyproject_microservices/api_gateway && make docs-init
	@-cd pyproject_microservices/front_end && make docs-init
	@-cd pyproject_microservices/model_serving && make docs-init

docs-view: docker-up
	@${BROWSER} http://localhost:$(PORT_NGINX)

format-style: docker-up
	@cd pyproject_microservices/api_gateway && make format-style
	@cd pyproject_microservices/front_end && make format-style
	@cd pyproject_microservices/model_serving && make format-style

getting-started: secret-templates
	@mkdir -p cache \
	    && mkdir -p logs \
		&& mkdir -p logs/apps \
		&& mkdir -p logs/tests \
		&& printf "Project started successfully!%s\n" \
		&& printf "Available microservices:%s\n" \
		&& printf "API Gateway: Handles requests and routes them to the desired services%s\n" \
		&& printf "Front-End: Serves as a user interface%s\n" \
		&& printf "Model Serving: Post-process outputs before serving them to the front-end via API gateway%s\n"
	@make docs-init

new-project:
	@read -p "Enter the new project name: " NEW_PROJECT; \
	./scripts/create_new_project.sh $(PROJECT) $$NEW_PROJECT

notebook: prompt-service
	@read SERVICE; \
    ./scripts/update_ports.sh $$SERVICE JUPYTER && \
    make docker-up && \
    cd pyproject_microservices/$$SERVICE && make notebook

notebook-delete-checkpoints: docker-up prompt-service
	@read SERVICE; \
	$(DOCKER_CMD) container exec $(CONTAINER_PREFIX)_$$SERVICE \
		rm -rf `find -L -type d -name .ipynb_checkpoints`

package-dependencies: docker-up
	@cd pyproject_microservices/api_gateway && make package-dependencies
	@cd pyproject_microservices/front_end && make package-dependencies
	@cd pyproject_microservices/model_serving && make package-dependencies

profile: profile-directory docker-up
	@cd pyproject_microservices/api_gateway && make profile
	@cd pyproject_microservices/front_end && make profile
	@cd pyproject_microservices/model_serving && make profile

profile-directory:
	@mkdir -p pyproject_microservices/api_gateway/profiles \
		&& mkdir -p pyproject_microservices/front_end/profiles \
		&& mkdir -p pyproject_microservices/model_serving/profiles \

prompt-service:
	@echo "AVAILABLE SERVICES: \n \
	- api_gateway \n \
	- front_end \n \
	- model_serving\n\
	Enter service name:"

secret-templates:
	@mkdir -p docker/secrets \
		&& cd docker/secrets \
		&& printf '%s' "$(PROJECT)" > 'db_database.txt' \
		&& printf '%s' "admin" > 'db_init_password.txt' \
		&& printf '%s' "admin" > 'db_init_username.txt' \
		&& printf '%s' "password" > 'db_password.txt' \
		&& printf '%s' "username" > 'db_username.txt' \
		&& printf '%s' "$(PROJECT)" > 'package.txt' \
		&& printf '%s' "model_serving" > 'model_serving.txt'

snakeviz: docker-up profile prompt-service
	@read SERVICE; \
    ./scripts/update_ports.sh $$SERVICE PROFILE && \
    make docker-up && \
	cd pyproject_microservices/$$SERVICE && make snakeviz-server
	@sleep 0.5
	@${BROWSER} http://0.0.0.0:$(PORT_PROFILE)/snakeviz/ &

tensorboard: docker-up tensorboard-server
	@printf "%s\n" \
			"" \
			"" \
			"" \
			"####################################################################" \
			"Use this link on the host to access the TensorBoard." \
			"" \
			"http://localhost:$(PORT_GOOGLE)" \
			"" \
			"####################################################################"
	@${BROWSER} http://localhost:$(PORT_GOOGLE)

tensorboard-server: docker-up prompt-service
	@read SERVICE; \
    ./scripts/update_ports.sh $$SERVICE TENSORBOARD && \
	$(DOCKER_CMD) container exec $(CONTAINER_PREFIX)_$$SERVICE \
		/bin/bash -c \
			"tensorboard --load_fast=false --logdir=$(TENSORBOARD_DIR) \
			--port=${PORT_GOOGLE} &"

tensorboard-stop-server: docker-up prompt-service
	@read SERVICE; \
	$(DOCKER_CMD) container exec $(CONTAINER_PREFIX)_$$SERVICE \
		/bin/bash -c \
			"ps -e | grep tensorboard | tr -s ' ' | cut -d ' ' -f 2 | xargs kill"

test: docker-up format-style
	@cd pyproject_microservices/api_gateway && make test
	@cd pyproject_microservices/front_end && make test
	@cd pyproject_microservices/model_serving && make test

test-coverage: test
	@${BROWSER} pyproject_microservices/api_gateway/htmlcov/index.html &
	@${BROWSER} pyproject_microservices/front_end/htmlcov/index.html &
	@${BROWSER} pyproject_microservices/model_serving/htmlcov/index.html &

upgrade-packages: docker-up
	@cd pyproject_microservices/api_gateway && make upgrade-packages
	@cd pyproject_microservices/front_end && make upgrade-packages
	@cd pyproject_microservices/model_serving && make upgrade-packages
