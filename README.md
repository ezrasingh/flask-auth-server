# Flask Auth Server (REST)

This project is designed to be an *Identity Access Management* (IAM) solution focused around **token based** authentication and authorization. The goal of this software is to securely provide access to protected user resources over a REST API.

### API Summary

- */api/authenticate*
    - **GET** - Refresh Token *
    - **POST** - Login
    - **PUT** - Update Password *
    - **PATCH** - Recover Account
    - **DELETE** - Delete Account *
- */api/user*
    - **GET** - Profile *
    - **POST** - Create User
    - **PUT** - Update Profiles *
    - **PATCH** - Update Email *
    - **DELETE** - Deactivate User *
- */api/validate*
    - */confirm*
        - **POST** - Confirm User Confirmation
        - **PUT** - Re-send User Confirmation
    - */reset*
        - **POST** - Validate Password Reset

`* - Requires auth token`

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

* [Docker](https://www.docker.com/get-started) is required for staging

Build or start the staging environment using:

`docker-compose up --build`

`docker-compose up`

**NOTE** :
*Staging is the preferred environment for frontend development*

### Running in Windows

Docker on windows utilizes a [local virtual machine](https://docs.docker.com/machine/get-started/) for networking, this can make accessing exposed ports difficult. First, start the virtual host then locate the host's IP address:

`docker-machine start`

`echo %DOCKER_HOST%`

If you are using [MinGW](http://www.mingw.org/) or happen to have `grep` installed, run the following command after starting the host.

`docker-machine inspect | grep IPAddress`

Then, test the access to container, after `docker-compose up` use the IP address from the previous step:

`curl http://<docker-machine-ip>:5000/api/profile`

You should receive a JSON response from the Dockerized API.

## Deploy

* This codebase supports deployment over [Heroku](https://devcenter.heroku.com/articles/getting-started-with-python)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
