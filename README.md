# README for test

[![Build status](https://gitlab.com/thorgate/test/badges/master/pipeline.svg)](https://github.com/vegetablejuiceftw/test/commits/master)
[![Coverage report](https://gitlab.com/thorgate/test/badges/master/coverage.svg)](https://github.com/vegetablejuiceftw/test/commits/master)

TODO: verify that the following info is correct:

 - Python:  3.6
 - DB:      PostgreSQL 10
 - Node:    8.x LTS
 - NPM:     5.x
 - React:   16.x

Browser support is defined in the `test/browserslist` file that is used for autoprefixing CSS.


## Setting up development

### Installing Docker and Docker Compose

Refer to original [Docker documentation](https://docs.docker.com/engine/installation/) for installing Docker.

After installing Docker you need to install [Docker Compose](https://docs.docker.com/compose/install/) to run
 multi-container Docker applications (such as ours). The `curl` method is preferred for installation.

To run Docker commands without `sudo`, you also need to
[create a Docker group and add your user to it](https://docs.docker.com/engine/installation/linux/ubuntulinux/#/create-a-docker-group).

### Setting up test

The easy way is to use `make` to set up everything automatically:

    make setup

This command:

- copies PyCharm project directory
- creates local settings file from local.py.example
- builds Docker images
- sets up database and runs Django migrations
- runs `docker-compose up`

Refer to `Makefile` to see what actually happens. You can then use the same commands to set everything up manually.


## Running development server

Both docker and docker-compose are used to run this project, so the run command is quite straightforward.

    docker-compose up

This builds, (re)creates and starts containers for Django, Node, PostgreSQL and Redis. Refer to `docker-compose.yml` for
more insight.

Logs from all running containers are shown in the terminal. To run in "detached mode", pass the `-d` flag to
docker-compose. To see running containers, use `docker-compose ps`. To see logs from these containers, run
`docker-compose logs`.

To _stop_ all running containers, use

    docker-compose stop

This stops running containers without removing them. The same containers can be started again with
`docker-compose start`. To stop a single container, pass the name as an extra argument, e.g.
`docker-compose stop django`.

To _stop and remove_ containers, run

    docker-compose down

This stops all running containers and removes containers, networks, volumes and images created by `up`.

### Using a different configuration file

By default docker-compose uses the `docker-compose.yml` file in the current directory. To use other configuration files,
e.g. production configuration, specify the file to use with the `-f` flag.

    docker-compose -f docker-compose.production.yml up

Note that the production configuration lacks PostgreSQL, since it runs on a separate container on our servers.

## Running Django commands in Docker

    docker-compose run django python manage.py <command>

### Command shortcuts in the Makefile

|Action                             |Makefile shortcut                  |Actual command                                                              |
|:----------------------------------|:----------------------------------|:---------------------------------------------------------------------------|
|make migrations                    |`make makemigrations cmd=<command>`|`docker-compose run --rm django ./manage.py makemigrations $(cmd)`          |
|migrating                          |`make migrate cmd=<command>`       |`docker-compose run --rm django ./manage.py migrate $(cmd)`                 |
|manage.py commands                 |`make docker-manage cmd=<command>` |`docker-compose run --rm django ./manage.py $(cmd)`                         |
|any command in Django container    |`make docker-django cmd=<command>` |`docker-compose run --rm django $(cmd)`                                     |
|run tests                          |`make test`                        |`docker-compose run --rm django py.test`                                    |
|run linters                        |`make quality`                     |                                                                            |
|run StyleLint                      |`make stylelint`                   |`docker-compose run --rm node npm run stylelint`                            |
|run ESLint                         |`make eslint`                      |`docker-compose run --rm node npm run lint`                                 |
|run Prospector                     |`make prospector`                  |`docker-compose run --rm django prospector`                                 |
|run psql                           |`make psql`                        |`docker-compose exec postgres psql --user test --dbname test` |
|generate docs                      |`make docs`                        |`docker-compose run --rm django sphinx-build ./docs ./docs/_build` |

## Running commands on the server

    docker-compose -f docker-compose.production.yml run --rm --name test_tmp django python manage.py <command>

## Installing new pip or npm packages

Since both `pip` and `npm` are inside their containers, currently the easiest way to install new packages is to add them
to the respective requirements file and rebuild the container.

## Rebuilding Docker images

To rebuild the images run `docker-compose build`. This builds images for all containers specified in the configuration
file.

To rebuild a single image, add the container name as extra argument, e.g. `docker-compose build node`.

## Swapping between branches

After changing to a different branch, run `docker-compose up --build`. This builds the images before starting
containers.

If you switch between multiple branches that you have already built once, but haven't actually changed any configuration
(e.g. installed new pip or npm packages), Docker finds the necessary steps from its cache and doesn't actually build
anything.

## Running tests

You can also use `--reuse-db` or `--nomigrations` flags to the actual command above to speed things up a bit. See also:
https://pytest-django.readthedocs.org/en/latest/index.html


## Generating documentation with Sphinx

To build **.rst** files into html, run `make docs`. View the documentation at `/docs/_build/index.html`.
Read more about contributing to docs from `/docs/contributing.rst`.


### Coverage

You can also calculate tests coverage with `coverage run -m py.test && coverage html`,

TODO: Expose this directory outside of docker
the results will be in `cover/` directory.


## Running linters

Linters check your code for common problems. Running them is a good idea before submitting pull requests, to ensure you
don't introduce problems to the codebase.

We use _ESLint_ (for JavaScript parts) and _Prospector_ (for Python) and StyleLint (for SCSS).
To use them, run those commands in the Django app dir:

    # Check Javascript sources with ESLint:
    make eslint
    # Check SCSS sources with StyleLint:
    make stylelint
    # Check Python sources with Prospector:
    make prospector
    # Run all of above:
    make quality


## Django translations

Project contains two commands for updating and compiling translations. Those two are `make makemessages` and `make compilemessages`.
Howewer if you are adding a new language or are creating translations for the first time after setting up project, you need to run
different command to create the initial locale files. The command is `add-locale`. After you have used this command once per each
new language you can safely use `makemessages` and `compilemessages`


## Deploys

### Python 2 environment

We use Fabric for deploys, which doesn't support Python 3. Thus you need to create a Python 2 virtualenv.
It needn't be project specific and it's recommended you create one 'standard' Python 2 environment
which can be used for all projects. You will also need to install django and tg-hammer==0.6, our fabric deployment helper.


### Server setup

Your server needs to have [Docker Engine](https://docs.docker.com/engine/installation/)
as well as [Docker Compose](https://docs.docker.com/compose/) installed.

We also assume that you have Nginx and Postgres (version 10 by default) running in Docker containers and reachable via
'private' network. We also make a few assumptions regards directories that will be used as volumes for static assets,
media, etc. You can find these paths in `fabfile.py` and `docker-compose.production.yml`.


### Types of deploys

There are basically two types of deploys:

* initial deploy, where the project doesn't exist in the server yet.
* incremental deploy, where the project only needs to be updated.


### Incremental deploy

* Ensure that whatever you want deployed is committed and pushed.
* Just run `fab ENV deploy` where `ENV` is either `test` or `live`.
  You'll see the changes to be applied and can continue or abort.
  * You can specify revision (either id or branch name) by running `fab ENV deploy:id=REV`
    Future deploys will stick to the same branch/rev and you'll need to explicitly deploy master/default
    branch to get back to it.


### Initial deploy

* Figure out which server you're going to deploy to.
  We usually have one main test server and one main production server for new project.
* Check `fabfile.py` in Django project dir. It has two tasks (functions) - `test` and `live`.
  Ensure that the one you'll use has correct settings (mostly hostname).
* Check django settings (`settings/staging.py` and/or `settings/production.py`)
  and Nginx config (`deploy/nginx/*.conf`, `deploy/letsencrypt/*.conf`) - ensure that they have proper hostnames etc.
* Add the server's SSH key (`/root/.ssh/id_rsa.pub`) to the project repo as deployment key.
* Ensure you've committed and pushed all relevant changes.
* Run `fab ENV setup_server` where `ENV` is either `test` or `live`.
  * If it worked, you're all done, congrats!
  * If something else broke, you might need to either nuke the code dir, database and database user on the server;
    or comment out parts of fabfile (after fixing the problem) to avoid trying to e.g. create database twice. Ouch.
