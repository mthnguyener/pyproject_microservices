[<mark style="font-size:20px; background-color: grey">OVERVIEW</mark>](../README.md) |
[<mark style="font-size:20px; background-color: grey">GETTING STARTED</mark>](GETTINGSTARTED.md) |
[<mark style="font-size:20px; background-color: lightblue">NEW SERVICES</mark>](NEWSERVICES.md) |
[<mark style="font-size:20px; background-color: grey">DOCUMENTATION</mark>](DOCUMENTATION.md) |
[<mark style="font-size:20px; background-color: grey">PROFILERS</mark>](PROFILERS.md)

# New Services
Below are steps to creating a new microservice. Keep in mind that unused services
should be deleted. We don't need a sword to cut butter...

## Available Services
This template contains 3 working microservices and its sample endpoints.

Completed microservices:
- `api_gateway`
- `front_end`
- `model_serving`

Potential microservices:
- `data_management`
- `model_inference`
- `model_training`
- `monitoring`

These potential microservices, can be deleted if not used upon new project creation.

## Creating a new microservice
1. Create the required `Dockerfile` and add the new service to the `docker-compose.yaml` 
under the `services` section. I recommend using the other services as guidance. 

Instead of hard-coding the ports, you can add the ports to `scripts/create_usr_vars.sh`. 
This will update `usr_vars` and `docker/.env` which has a symbolic link with `usr_vars`.

The following directories and files were mounted to the completed/working services:
- `utils`: mounted to `/usr/src/<service>/<service>/utils`
- `logs`: mounted to `/usr/src/<service>/logs`
- `usr_vars`: mounted to `/usr/src/<service>/usr_vars`
- `.yapfignore`: mounted to `/usr/src/<service>/.yapfignore`
- `.env`: mounted to `/usr/src/<service>/docker/.env`

3. Copy`Makefile`, `README.md`, `requirements.txt`, `setup.cfg`, and `setup.py` over to
your new microservice.

For example, if only `model_training` of the potential microservices is needed, 
delete the folders of unused services and copy the above files over to `<project>/model_training`

4. Update the "main" `Makefile` from project root to include the new service details.

For example, update `docs-init` of the `Makefile` to include `model_training`:
```
docs-init:
	@-cd pyproject_microservices/api_gateway && make docs-init
	@-cd pyproject_microservices/front_end && make docs-init
	@-cd pyproject_microservices/model_serving && make docs-init
	@-cd pyproject_microservices/model_training && make docs-init <--- new service
```

<br>

[<mark style="font-size:20px; background-color: grey">OVERVIEW</mark>](../README.md) |
[<mark style="font-size:20px; background-color: grey">GETTING STARTED</mark>](GETTINGSTARTED.md) |
[<mark style="font-size:20px; background-color: lightblue">NEW SERVICES</mark>](NEWSERVICES.md) |
[<mark style="font-size:20px; background-color: grey">DOCUMENTATION</mark>](DOCUMENTATION.md) |
[<mark style="font-size:20px; background-color: grey">PROFILERS</mark>](PROFILERS.md)
