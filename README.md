# Django Trip App

App that allow customers to collaborate being moved around the city by either creating or searching relevant trips.

## What's used

* Docker + Docker Compose
* Django + Django REST Framework
* Postgres

## Setup Steps

### Main:

1. Install Docker: `https://docs.docker.com/install/linux/docker-ce/ubuntu/` (check the menu on the left for other OS-s)
2. Install Docker Compose: `https://docs.docker.com/compose/install/`
3. Clone the current repo somewhere.

4. Go to the `{project_name}`:<br/>

    `cd {project_name}`

5. To run the tests you should type:

* `make test` - this will build a test Docker image and run the tests automatically.

6. Run `docker-compose -f docker-compose.yaml -f docker-compose.setup.yaml up` if you have
   you have dependencies updated / model migrations changed, otherwise run `docker-compose up'

    You can check that your server is now working in a browser:
        `http://127.0.0.1:8000/api/accounts/`
    Press `Ctrl+C` when completed to stop the services.

