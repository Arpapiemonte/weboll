# weboll - Installation Guide

## Preparation

Clone this repo:

    git clone git@github.com:Arpapiemonte/weboll.git

**NOTE** on Windows, it is preferred to use `git` from WSL 2:

- follow the [Windows Subsystem for Linux 2 Installation Guide](https://docs.microsoft.com/en-us/windows/wsl/
install-win10)

- install the [Debian "app" from Microsoft Store](https://www.microsoft.com/en-us/p/debian/9msvkqc78pk6)

- open the Debian bash shell and issue these commands to install `git`:

    ```sh
    apt update
    apt upgrade
    apt install git
    ```

- now close the bash shell; clone the repo from the Windows CMD or PowerShell prompt like this (inside a plain Windows folder, not inside `\\wsl$`):

    ```sh
    wsl git clone git@github.com:Arpapiemonte/weboll.git
    ```

For more information:

- https://wiki.debian.org/InstallingDebianOn/Microsoft/Windows/SubsystemForLinux
- https://docs.microsoft.com/en-us/windows/wsl/interop
- https://devblogs.microsoft.com/commandline/access-linux-filesystems-in-windows-and-wsl-2/
- https://devblogs.microsoft.com/commandline/integrate-linux-commands-into-windows-with-powershell-and-the-windows-subsystem-for-linux/
- https://devblogs.microsoft.com/commandline/per-directory-case-sensitivity-and-wsl/
- https://devblogs.microsoft.com/commandline/cross-post-wsl-interoperability-with-docker/

## Docker set-up

The docker set-up is preferred.

### Requirements

macOS 10.13 (High Sierra): install Docker Desktop for Mac from https://docker.com (make sure Docker Desktop is running !)

Debian 12 (bookworm):

```sh
sudo apt install docker.io docker-compose
```
Read `/usr/share/doc/docker.io/README.Debian` !

Fedora 32/33: https://docs.docker.com/engine/install/fedora/

Windows: install Docker Desktop for Windows (with Linux containers) from: https://hub.docker.com/editions/community/docker-ce-desktop-windows/; then enable WSL 2 integration: https://docs.docker.com/docker-for-windows/wsl/.

### Pulling base images

Pull the dependencies from https://hub.docker.com/ with these commands:

```sh
docker pull debian:bookworm-slim
docker pull postgres:13.8
docker pull osixia/openldap:1.5.0
docker pull node:18
docker pull nginx
```

This should be repeated from time to time to refresh the images.

### Build our images

To force a rebuild of our images (this is required when Python or JavaScript dependencies are modified):

    docker-compose -f local.yml build

You can pass the service name ((one of `postgres`, `ldap`, `django` or `frontend`) after `build` to selectively rebuild only one of them at the time.

**NOTE**: starting services will build our images the first time

### Start services in development mode

First shift the dates of the preload data launching this script:

    ./shift_dates.sh

then create an empty `.env` file:

    touch .env

or copy the provided template:

    cp .env.example .env

Now start the app in local development mode with this command (on first launch it builds the images locally, then it mounts the app volumes from the source tree so that modifying files on your filesystem immediately has an effect on the services):

    docker-compose -f local.yml up

You can pass the service name (one of `postgres`, `ldap`, `django` or `frontend`) after `up` to selectively start only one of them at the time, but they should be started in the given order.

### Useful commands

While the services are up you can enter the containers and perform different useful tasks:

- Access the database:

    ```sh
    docker-compose -f local.yml exec postgres psql -U weboll core
    ```

- Run type checks with mypy [inside the django service](https://docs.docker.com/compose/reference/exec/):

    ```sh
    docker-compose -f local.yml exec django mypy website --config setup.cfg
    ```

- Run type checks with mypy in the venv:

    To let the environment get the global variables defined in the docker files from `.env` file,

    ```sh
    set -a
    source .env
    set +a
    ```

    Then you can activate the venv, as explained below in the `Back-end` section, to enter:

    ```sh
    mypy website --config=setup.cfg
    ```

- Run the JavaScript tests with Vitest:

    ```sh
    docker-compose -f local.yml exec frontend yarnpkg test --run
    ```

    BTW:

    - if you have `console.log` statements the output will appear in `stdout` section

    - if you need to launch a specific test, call `... test --run map.spec.js`

- Run the Python tests (make sure to populate the test database `test_core` using `cat sql/* | docker-compose  -f local.yml  exec -T postgres psql -U weboll test_core` !):

    ```sh
    docker-compose exec django pytest-3
    ```

  to run only a specific test with maximum verbosity:
    
    ```
    docker-compose exec django pytest-3 -vvv tests/test_routes.py::TestBullettinsEndpoints::test_full_new_bulletin_authorized
    ```
    
**NOTE**: during tests, any output sent to stdout and stderr is captured by [pytest](https://pytest.org/en/6.2.x/capture.html); start pytest-3 with `-s` option to disable all capturing if you seed to see some `print()` outputs.

- Run the Python tests, check your test coverage, and generate an HTML coverage report:

    ```sh
    docker-compose -f local.yml exec django python3-coverage run -m pytest
    docker-compose -f local.yml exec django python3-coverage html
    open htmlcov/index.html
    ```

- Refresh the visual regression baseline (this is required when the app homepage appearance changes for some reason):

    ```sh
    NEEDLE_SAVE_BASELINE=1 docker-compose -f local.yml -f test.yml up --abort-on-container-exit --exit-code-from tester
    ```

## Local set-up

### Back-end

You can install the back-end without docker if your workstation is running the same base operating system that is used for the `deps-base` image: Debian 12 (bookworm). Running on other O.S. may cause the version of some dependencies to differ and therefore cause unexpected problems.

Install postgresql, Python 3.9 and the dependencies required with:
```
sudo apt install postgresql python3-venv \
    fontconfig \
    locales \
    python3-argon2 \
    python3-distlib \
    python3-factory-boy \
    python3-hiredis \
    python3-pil \
    python3-pip \
    python3-psycopg2 \
    python3-rcssmin \
    python3-redis \
    python3-slugify \
    python3-tz \
    python3-wheel \
    python3-whitenoise \
    python3-yaml \
    wait-for-it \
    curl
```

If you are not using Debian as your operating system you need also:
```
sudo apt install libsasl2-dev \
    libldap2-dev \
    libssl-dev \
    libpq-dev \
    python3-dev \
```

Install [Titillium fonts](https://fonts.google.com/specimen/Titillium+Web) and [manually install the `it-IT.UTF-8 UTF-8` locale](https://wiki.debian.org/Locale#Manually).

Create a [virtual environment](https://docs.python.org/3/library/venv.html) named `venv`, activate it and install dependencies (note the `--system-site-packages` option: we want to give the virtual environment access to the system site-packages dir so that it can use packages installed with `apt`):
```
rm -rf venv
python3 -m venv --system-site-packages venv
source venv/bin/activate
pip3 install -r requirements/test.txt
```

Set required environmental variables in the `.env` file or use the provided sample values:
```
cp .env.example .env
```

### Front-end

Install the front-end prerequisites on Debian 12 (bookworm):

    sudo apt install yarnpkg

or on macOS:

    brew update
    brew install yarn

**NOTE**: due to the [`server.proxy` setting in `vite.config.js`](https://vitejs.dev/config/server-options.html#server-proxy) the front-end will try to proxy the API from http://django:8000; if you run the `yarnpkg dev` command locally either tweak that to http://localhost:8000 in `vite.config.js` or make sure `127.0.0.1       localhost ... django` is present in `/etc/hosts`.

## Mixed set-up

### Back-end with docker and local front-end

To start with docker only the back-end containers:
```
docker-compose -f local.yml up django
```

### Local back-end and front-end with docker

To start with docker only the front-end container:

    docker run --rm -it -p 8080:80 -v "$PWD/compose/frontend/default.conf:/etc/nginx/conf.d/default.conf" --add-host django:172.17.0.1 arpa/weboll/frontend:latest

**NOTE**: on Windows and macOS skip the `--add-host` option and and replace `django` with `host.docker.internal` in `compose/frontend/default.conf`.
