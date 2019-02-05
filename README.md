# Flask Auth Server (REST)

This project is designed to be an *Identity Access Management* (IAM) solution focused around **session based** authentication and authorization. The goal of this software is to securely provide access to protected user resources over a REST API.

### API Endpoints

- */api/authenticate*
    - **POST** - Login with identity and credentials
    - **DELETE** - Dereference current session *
- */api/user*
    - **GET** - Request user's profile *
    - **POST** - Create a new user
    - **PUT** - Update user's profiles *
    - **DELETE** - Deactivate user account

`* - Requires authentication`

## Development
I would recommend developing within a **virtualenv** preferably via *[virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html)*.

Install application dependencies:

`pip install -r requirements.txt`

Run coverage tests:

`python -m pytest tests/`

Start application in development mode:

`flask run`

### Migrations

Generate migrations:

`flask db init`

Upgrade and downgrade the schema using:

`flask db upgrade`

`flask db downgrade`

## Staging

* [Docker](#) is required for staging

Build and start the staging environment using:

`docker-compose up --build`

`docker-compose up`

### Running in Windows

Docker on windows utilizes a [local virtual machine](https://docs.docker.com/machine/get-started/) for networking, this can make accessing exposed ports difficult. First, locate the IP address assigned to the container via the virtual network driver:

`docker-machine inspect | grep IPAddress`

Then, test the access to container, after booting up `docker-compose` use the IP address from the previous step:

`curl http://<docker-machine-ip>:5000/api/profile`

You should receive a JSON response from the Dockerized API.

**NOTE** :
*Staging is the preferred environment for frontend development*

## Deploy

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
