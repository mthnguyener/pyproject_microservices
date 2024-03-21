#  pyproject_microservices
pyproject_microservices is a Python based microservices project template. 
The template will have sample endpoints and a generic microservices architecture.

This template referenced PyProject Starter: 
https://github.com/mthnguyener/pyproject_starter

<img src="./assets/microservices_diagram.png" alt="Microservice Diagram" width="768" height="auto"/>

## pyproject_microservices Structure
- `docker`: Docker directory
  - `Dockerfile`: Dockerfiles for building Docker container images
  - `docker-compose.yaml`: Yaml file used by Docker Compose to define the services, 
  networks, and volumes for a multi-container application
- `docs`: Project documentation. Documentation for services are in `pyproject_microservices/<service>/docs/` 
of the respective service and are generated using `sphinx`.
- `logs`: Where we logs everything
  - `apps`: Log app level items
  - `tests`: Log of test runs
- `pyproject_microservices`: Contains services and utility directories
  - `api_gateway (COMPLETED)`: API Gateway service for managing and routing requests
  - `data_management`: Data Management service for data related tasks (ETL)
  - `front_end (COMPLETED)`: Streamlit service with sample pages (missing test atm)
  - `model_inference`: Model Inference service processing incoming data and 
  returning inference results to the requesting applications.
  - `model_serving (COMPLETED)`: Model Serving service providing an interface for external systems 
  to interact with the models.
  - `model_training`: Model Training service training machine learning models
  - `monitoring`: Monitoring and Logging service overseeing the health, performance, 
  and operational aspects of the entire microservices architecture
  - `nginx`: Nginx service
    - `default_html`: Nginx default html, index.html, is here
  - `utils`: Folder containing util functions and variables
- `scripts`: Folder with setup related scripts

Notes: future updates will include Endpoints for other services as I continue to update other microservices

## Setting Up New Project
1. From current project root directory, run:
   - `make new-project`
     - `Enter the new project name: new_project`
1. Current project directories and files are created in the new project directory
    - `new_project/`
1. The new project is created 1-level up from the current project root directory
   - if current project directory is `projects/pyproject_microservices` 
     then the new project is created at `projects/new_project`
1. To add to git:
   - `git init`
   - `git add <new_project_files_and_directories>`
   - `git commit -m "first commit or any comments"`
   - `git branch -M main`
   - `git remote add origin https://github.com/<user_or_organization>/<project>.git`
   - `git push -u origin main`

## [Getting Started](docs/GETTINGSTARTED.md)

## [Documentation](docs/DOCUMENTATION.md)

## [Profilers](docs/PROFILERS.md)

## Acknowledgements
If you find this project helpful in your work and decide to mention or reference 
it in your own project, I'd appreciate it! You can acknowledge this project by 
mentioning my username and providing a link back to this repository. Here's an example:

```
This project was inspired by or built upon pyproject_microservices by mthnguyener, 
available at https://github.com/mthnguyener/pyproject_microservices.git.
```
