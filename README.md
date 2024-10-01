# weboll - Bulletin back-office for ARPA Piemonte Centro Funzionale

If you want to use weboll, read the **user docs**:

- [User Guide (Italian)](doc/manuale_utente.md) to learn how to view and edit bulletins;

- [System Administraton Guide (Italian)](doc/manuale_amministratore.md) to learn how to manage an instance of weboll.

If you want to hack on the source code, read the **developer docs**:

- [Installation Guide](doc/INSTALL.md)

- [Conceptual Description](doc/CONCEPTS.md)

- [Front-end Developer Guide](doc/DEVELOPER_FRONT.md)

- [Back-end Developer Guide](doc/DEVELOPER_BACK.md)

- [New Bulletin Guide](doc/new_bulletin.md)

- [PDF Guide](doc/manuale_pdf.md)

- [Data Models (Italian)](doc/data_models.md)

## [TL;DR](https://en.wiktionary.org/wiki/tl;dr)

Start the local services on your workstation with this command (requires make, docker and docker-compose):

    make

the webapp will then be live at: http://localhost:8080.

## Compatibility

- Docker Engine 21.10.0+ (Compose file format 3.8)

- Browsers (can be checked launching `node_modules/browserslist/cli.js` from project root):

    - Chrome/Chromium 107 and 108
    - Chromium-based Microsoft Edge 107 and 108
    - Firefox 91 (Debian stable 11 Extended Support Release), 107 and 108
    - iOS Safari 15.6 to 16.2
    - macOS Safari 15.6 to 16.2
    - **weboll does not run on Internet Explorer**

Other tools, libraries and components we depend upon:

**JAVASCRIPT**

| Name                          | Our version         | Latest release         | End-of-life| reference |
|-------------------------------|---------------------|------------------------|------------|-----------|
| chartjs-adapter-date-fns      | 3.0.0               | 3.0.0 (2022-12-11)     | ?          | https://github.com/chartjs/chartjs-adapter-date-fns|
| chartjs-plugin-zoom           | 2.0.1               | 2.0.1 (2023-03-22)     | ?          | https://www.chartjs.org/chartjs-plugin-zoom/latest/|
| bootstrap                     | 5.3.3               | 5.3.3 (2024-02-20)     | ?          | https://github.com/twbs/release|
| date-fns/locale               | 3.6.0               | 3.6.0 (2024-03-18)     | ?          | https://github.com/date-fns/date-fns|
| vue-chartjs                   | 5.3.1               | 5.3.1 (2024-04-09)     | ?          | https://vue-chartjs.org/ |
| typescript                    | 5.4.5 (2024-04-10)  | 5.5.4 (2024-07-23)     | ?          | https://github.com/microsoft/TypeScript/releases|
| vitest                        | 1.6.0 (2024-05-03)  | 2.0.5 (2024-07-31)     | ?          | https://github.com/vitest-dev/vitest|
| vue-router                    | 4.3.3 (2024-06-10)  | 4.4.3 (2024-08-06)     | ?          | https://router.vuejs.org|
| ag-grid-vue3 community edition| 32.1.0              | 32.1.0 (2024-08-08)    | ?          | https://www.ag-grid.com/vue-data-grid/getting-started/|  
| chartjs                       | 4.4.4               | 4.4.4 (2024-08-20)     | ?          | https://www.chartjs.org/|
| vite                          | 5.4.2               | 5.4.2 (2024-08-20)     | ?          | https://github.com/vitejs/vite|
| node                          | 22.7.0              | 22.7.0 LTS (2024-08-22)| 2027-04-30 | https://github.com/nodejs/release#release-schedule|
| eslint                        | 8.57.0 (2024-02-23) | 9.9.1 (2024-08-23)     | ?          | https://esbuild.github.io/|
| vue.js                        | 3.4.38 (2024-08-15) | 3.5.0 (2024-09-03)     | ?          | https://github.com/vuejs/vue/projects/6|


**PYTHON summary**

| Name                          | Our version      | Latest release | End-of-life       | reference                                                                          |
|-------------------------------|------------------|---------------|-------------------|------------------------------------------------------------------------------------|
| python                        | 3.11.2 (2023-02-07)     | 3.12.5 (2024-08-06)| 2027-10           | https://devguide.python.org/versions/#supported-versions|
| django                        | 4.2.15 (LTS) 2024-08-06 | 5.1 (2024-08-07)   | 2026-04-30           | https://www.djangoproject.com/download/#supported-versions|
| celery                        | 5.4.0                   | 5.4.0 (2024-04-17) |            |https://github.com/celery/celery/releases|
| djangorestframework           | 3.15.2                  | 3.15.2 (2024-06-19)| ?                 | https://www.django-rest-framework.org/community/release-notes/#deprecation-policy|
| djangorestframework_simplejwt | 5.3.1                   | 5.3.1(2023-12-04)  | ?                 | https://github.com/jazzband/djangorestframework-simplejwt/blob/master/CHANGELOG.md|
| drf-spectacular               | 0.27.2                  | 0.27.2(2024-04-01) | ?                 | https://github.com/tfranzel/drf-spectacular|
| postgresql                    | 13.8 (2022-08-08)       | 16.4(2024-08-05)   | 2025-11-13       | https://www.postgresql.org/support/versioning/|

### Python requirements base
| Name                                  | release date|
|---------------------------------------|-----------|
| djangorestframework-xml==2.0.0		| 2020-04-13|
| django-wkhtmltopdf==3.4.0		        | 2022-02-25|
| django-cryptography==1.1		        | 2022-08-06|
| django-celery-results==2.5.1		    | 2023-05-08|
| django-extensions==3.2.3		        | 2023-06-05|
| flower==2.0.1				            | 2023-08-13|
| argon2-cffi==23.1.0			        | 2023-08-15|
| django-mass-edit==3.5.0		        | 2023-08-22|
| django-environ==0.11.2			    | 2023-09-01|
| psycopg2==2.9.9		                | 2023-10-03|
| rcssmin==1.1.2				        | 2023-10-03|
| python-ldap==3.4.4			        | 2023-11-17|
| djangorestframework-simplejwt==5.3.1	| 2023-12-04|
| python-slugify==8.0.4		            | 2024-02-08|
| drf-spectacular==0.27.2			    | 2024-04-01|
| django-auth-ldap==4.8.0		        | 2024-04-04|
| celery==5.4.0				            | 2024-04-17|
| requests==2.32.3			            | 2024-05-29|
| django-debug-toolbar==4.4.6	        | 2024-06-10|
| djangorestframework==3.15.2	        | 2024-06-19|
| hiredis==3.0.0				        | 2024-06-19|
| whitenoise==6.7.0			            | 2024-06-19|
| django-crispy-forms==2.3		        | 2024-06-19|
| Pillow==10.4.0				        | 2024-07-01|
| redis==5.0.8				            | 2024-07-30|
| PyJWT==2.9.0				            | 2024-08-01|	
| django_filter==24.3			        | 2024-08-02|
| django==4.2.15				        | 2024-08-06|
| uvicorn[standard]==0.30.6		        | 2024-08-13|
| matplotlib==3.9.2			            | 2024-08-13|
| django-celery-beat==2.7.0		        | 2024-08-22|
| numpy==2.1.1				            | 2024-09-03|
| django-model-utils==5.0.0		        | 2024-09-04|
| pytz==2024.2				            | 2024-09-11|

### Python requirements test
| Name                                  | release date| used by |
|---------------------------------------|-------------|---------|
| needle==0.5.0                         | 2017-04-03  | test    |
| selenium==3.141.0				        | 2018-12-19  | test    |
| urllib3==1.26.12				        | 2022-08-22  | test    |
| ipdb==0.13.13				            | 2023-03-09  |         |
| django-extensions==3.2.3		        | 2023-06-05  |         |
| django-coverage-plugin==3.1.0         | 2023-07-10  |         |
| types-urllib3==1.26.25.14		        | 2023-07-20  |         |
| types-requests==2.31.0.6		        | 2023-09-27  |         |
| pylint-django==2.5.5			        | 2023-10-23  |         |
| flake8-isort==6.1.1			        | 2023-11-03  |         |
| pytest-sugar==1.0.0			        | 2024-02-01  |         |
| types-pytz==2024.1.0.20240417		    | 2024-04-17  |         |
| django-stubs==5.0.4			        | 2024-07-28  |         |
| pre-commit==3.8.0			            | 2024-07-28  |         |
| black==24.8.0				            | 2024-08-02  |         |
| coverage==7.6.1			            | 2024-08-04  |         |
| flake8==7.1.1				            | 2024-08-04  |         |
| factory-boy==3.3.1			        | 2024-08-18  |         |
| mypy==1.11.2				            | 2024-08-25  |         |
| pytest-django==4.9.0			        | 2024-09-02  |         |
| pytest==8.3.3				            | 2024-09-10  |         |


## Project structure

- **documentation** content is in `doc` dir and the following files:
    - `CONTRIBUTORS.txt`
    - `LICENSE`
    - `README.md`

- **docker** setup is in the following dirs and files:
    - `compose`: contains the "multistage" Dockerfiles used to generate all the images
    - the multi-container Docker applications:
        - `production.yml`: main config, should match what will go in production, pulls pre-build images from the Gitlab CI
        - `local.yml`: for local development, builds all images locally for development
        - `test.yml`: to run tests locally
        - `localtest.yml`: to run tests in the CI

- **back-end** implementation is in the following dirs and files:
    - `config`: configuration files
    - `manage.py`: the main entry point to start, stop and control the apps
    - `requirements`: specify the 3rd party Python libraries used
    - `website`: where the common Python code resides
      - other files and dirs: common classes, DB interface, templates etc.

- **front-end** implementation is in the following dirs and files:
    - `.eslintrc.cjs`: configuration file for the [ESLint JavaScript statical analyzer](https://eslint.org/docs/latest/use/configure/configuration-files)
    - `package.json` and `yarn.lock`: specify the 3rd party JavaScript libraries used
    - `public`: static files
    - `src`: mixed JavaScript ES6 / TypeScript source code for the webapp's pages and components
      - other files and dirs: common components, pages, assets etc.
    - `tsconfig*.json`: [TypeScript configuration](https://www.typescriptlang.org/docs/handbook/tsconfig-json.html)
    - `vite.config.ts`: configuration file for the [Vite Frontend Tooling](https://vitejs.dev/config/)

- **bulletins folders** each bulletin has its specific folder with this structure:
    - a `w` followed by the identification number of the bulletin gives the name for the folder, in particular
        - `w05`: for Meteo bulletins
        - `w16`: for Ozono bulletins
    - `/back` subfolder containing the backend for the specific bulletin
    - `/front` subfolder containing the frontend for the specific bulletin
    - `/templates` subfolder containing the templates 
    

- **tests** are in:
    - `screenshots`: the reference screenshots for how the UI should look like
    - `tests`: test implementation
      - `tests/unit`: JavaScript unit tests
        - `tests/unit/w05`: for Meteo bulletins
        - `tests/unit/w16`: for Ozono bulletins
    - `.pylintrc`, `pytest.ini` and `setup.cfg`: Python test configuration

## Containerization and Continuous integration

The Gitlab Continuous Integration is used to run a number of tests each time a commit is pushed to any branch, and to build container images that can be used to quickly reproduce things and/or for deployment.

The entire pipeline runs on each branch except tagging the images with `latest`, so when you open an Merge Request (MR) you're pretty sure that you are not breaking things.

The Gitlab CI runs 4 stages:

- **Prepare**: define some variables that control the rest of the pipeline and run the linters for Python etc. in parallel

- **Build images** in three steps, and push the to the GitLab registry with a `test-xyz` tag:
    1. application dependencies for production
    2. intermediate images with build / test dependencies
    3. the applications

- **Test**: run tests in parallel:
    1. unit tests
    2. static type checking with [mypy](http://mypy-lang.org/)
    3. integration tests of the entire architecture using Docker Compose inside a docker container (!), including visual regression testing

- **Tag** (only runs on master branch): If all tests pass, the pipeline tags the images as `latest` (makeing them the current ones used by docker).

From the single "multistage" Dockerfile 4 images are derived:

1. application dependencies for production
2. build / test dependencies
3. the complete images for production
4. the complete image for testing

Images 1 and 2 are separated to make it easier to reuse them, particularly because the ones for building / testing are big and generating them every time would slow down development.

The images so built and tagged can be used locally to make reproducing errors quicker.

The **unit tests** are faster to write and run but **integration tests** allow you to test something as close as possible to production.

In addition, integration tests use Selenium so they can also test the UI and client-side JavaScript.

For visual regression testing Selenium is used to take screenshots and reports an error when it finds a difference with respect to the expected screenshot (but it is easy to update references when making changes).

## License

Copyright (C) 2024 Arpa Piemonte - Dipartimento Rischi Naturali e Ambientali.

Licensed under the [GNU Affero General Public License version 3 or later](LICENSE) as per [linee guida per l’Acquisizione e il riuso di software per la Pubblica Amministrazione](https://docs.italia.it/italia/developers-italia/lg-acquisizione-e-riuso-software-per-pa-docs/it/stabile/riuso-software/licenze-aperte-e-scelta-di-una-licenza.html#scelta-di-una-licenza).
