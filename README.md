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

| Name                          | Our version     | First release | End-of-life       | reference                                                                          |
|-------------------------------|-----------------|---------------|-------------------|------------------------------------------------------------------------------------|
| python                        | 3.9 (debian 11) | 2020-10-05    | 2025-10           | https://devguide.python.org/#status-of-python-branches                             |
| django                        | 4.0.7 (pip)     | 2022-08-03    | 2023-04           | https://www.djangoproject.com/download/#supported-versions                         |
| djangorestframework           | 3.13.1 (pip)    | 2021-12-15    | ?                 | https://www.django-rest-framework.org/community/release-notes/#deprecation-policy  |
| djangorestframework_simplejwt | 5.2.0 (pip)     | 2022-05-24    | ?                 | https://github.com/jazzband/djangorestframework-simplejwt/blob/master/CHANGELOG.md |
| drf-spectacular               | 0.25.1          | 2022-12-16    | =                 | https://github.com/tfranzel/drf-spectacular                                        |
| postgresql                    | 13.8 (docker)   | 2022-08-11    | current: 14       | https://www.postgresql.org/support/versioning/                                     |
| node                          | 16 (docker)     | 2021-04-20    | 2024-04-30        | https://nodejs.org/en/about/releases/                                              |
| babel                         | 7.18.13         | 2022-08-22    | ?                 | https://babeljs.io/docs/en/roadmap#docsNav                                         |
| bootstrap                     | 5.2.0           | 2022-07-19    | TBD               | https://github.com/twbs/release                                                    |
| eslint                        | 0.16.16         | 2023-01-08    | ?                 | https://esbuild.github.io/                                                         |
| typescript                    | 4.7.4           | 2022-06-17    | current: 4.9.4    | https://devblogs.microsoft.com/typescript/announcing-typescript-4-7/               |
| vee-validate                  | 4.6.6           | 2022-08-16    | ?                 | https://vee-validate.logaretm.com/v4/                                              |
| vite                          | 4.0.4           | 2023-01-03    | ?                 | https://github.com/vitejs/vite                                                     |
| vitest                        | 0.27.0          | 2023-01-09    | ?                 | https://github.com/vitest-dev/vitest                                               |
| vue.js                        | 3.2.37          | 2022-06-06    | ?                 | https://github.com/vuejs/vue/projects/6                                            |
| vue-router                    | 4.0.14          | 2022-03-10    | ?                 | https://router.vuejs.org                                                           |

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
    - `vite.config.js`: configuration file for the [Vite Frontend Tooling](https://vitejs.dev/config/)

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

Copyright (C) 2020-2023 [simevo s.r.l.](https://simevo.com) for ARPA Piemonte - Dipartimento Rischi Naturali e Ambientali.

Licensed under the [GNU Affero General Public License version 3 or later](LICENSE) as per [linee guida per l’Acquisizione e il riuso di software per la Pubblica Amministrazione](https://docs.italia.it/italia/developers-italia/lg-acquisizione-e-riuso-software-per-pa-docs/it/stabile/riuso-software/licenze-aperte-e-scelta-di-una-licenza.html#scelta-di-una-licenza).
