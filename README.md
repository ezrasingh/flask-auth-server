# Flask Auth Server (REST)

This project is designed to be an *Identity Access Management* (IAM) solution focused around **token based** authentication and authorization. The goal of this software is to securely provide access to protected user resources over a REST API.

### API Summary

- */api/authenticate*
    - **GET** - Refresh Token *
    - **POST** - Login
    - **PUT** - Reset Password *
    - **PATCH** - Recover Account
    - **DELETE** - Delete Account *
- */api/user*
    - **GET** - Profile *
    - **POST** - Create User
    - **PUT** - Update Profiles *
    - **PATCH** - Update Email *
    - **DELETE** - Deactivate User *
- */api/validate*
    - */confirmation*
        - **POST** - Confirm User Confirmation
        - **PUT** - Re-send User Confirmation
    - */recovery*
        - **POST** - Password Reset for Account Recovery

`* - Requires auth token`

## Development
I would recommend developing within a **virtualenv** preferably via *[virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html)*.

Install application dependencies:

`pip install -r requirements.txt`

Run tests:

`pytest`

Or more *stringently*:

`python -m pytest tests/`

* *Configure test options in [`pytest.ini`](pytest.ini)*

Start application in development mode:

`flask run`

### Migrations

Initialize database migrations:

`flask db init`

Generate new migrations:

`flask db migrate`

Upgrade and downgrade the schema using:

`flask db upgrade`

`flask db downgrade`

To use the most recent migration *(preferred)*:

`flask db stamp head`

`flask db upgrade`

### Emails

* [Mailtrap](https://mailtrap.io/) is preferred for **development** and **API testing**.

Update the SMTP server parameters in [`.env`](.env) for *development* and *testing*.

For *staging* and *production* feel free to use any SMTP service of your choice, just set the SMTP server parameters within their respective environment keys. 

* *Reference [`.env`](.env) for appropriate keys.*

### API Testing

* [Insomnia](https://insomnia.rest/) is required for API testing

Import [`api.json`](api.json) and use the **Testing** environment.

To generate validation tokens for emulating email based confirmation use:

`flask generate --validation-token <email>`

## Staging

* [Docker](https://www.docker.com/get-started) is required for staging

Build or start the staging environment using:

`docker-compose build`

`docker-compose up`

**NOTE** :
*Staging is the preferred environment for frontend development, be sure to configure **CLIENT_ORIGIN** in [`docker-compose.yml`](docker-compose.yml)*.

### Running in Windows

Docker on windows utilizes a [local virtual machine](https://docs.docker.com/machine/get-started/) for networking, this can make accessing exposed ports difficult. First, start the virtual host then locate the host's IP address:

`docker-machine start`

`echo %DOCKER_HOST%`

If you are using [MinGW](http://www.mingw.org/) or happen to have `grep` installed, run the following command after starting the host.

`docker-machine inspect | grep IPAddress`

Then, test the access to container, after `docker-compose up` use the IP address from the previous step:

`curl http://<docker-machine-ip>:5000/api/auth`

You should receive a JSON response from the Dockerized API.

## Deploy

* This codebase supports deployment over [Heroku](https://devcenter.heroku.com/articles/getting-started-with-python)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
