# weboll - How to create a new bulletin

## General

- **README.md**

    - in `project structure` update the bulletins folders list in the parts about *backend*, *frontend*, *tests*.

## Back-end

- **config/settings/base.py** some of the arrays in the file may need an update:

    - `LOCAL_APPS` add the new path to `ApiConfig`

    - `TEMPLATES` in the key "DIRS" add a new path like: `str(ROOT_DIR / "wXY" / "templates")`

- **config/urls.py**

    - add a new path in the array `URLLIST` like: `path("wXY/", include("wXY.back.urls"))`

- **.gitlab-ci.yml**

    - in the section about `mypy` tests, `scripts` need to be updated eith the new bulletin folder like: `mypy wXY --config=setup.cfg`

In addition, it is important for production to remember to update the pages `wXY/back/signals.py` and `website/core/admin.py`

## Front-end

The new bulletin properties must be added in the `bulletins_list` array in the file `public/bulletins.js`.

Make sure the bulletin logo is available in `wXY/back/static/images/logo_wXY.svg`

- **compose/frontend/Dockerfile**

    - add a new `COPY` line like: `COPY wXY ./wXY`

- **local.yml** 

    - in the section *frontend/volumes* add a new path like: `./wXY:/app/wXY`
