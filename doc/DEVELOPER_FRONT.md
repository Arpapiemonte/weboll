# weboll - Front-end Developer Guide

The front-end is implemented in HTML5 with:

- the [Bootstrap CSS framework](https://getbootstrap.com/) version 5

- the [Vue.js front-end JavaScript framework](https://vuejs.org/) version 3

- mixed JavaScript and TypeScript 4.7

- [esbuild](https://esbuild.github.io/) in development mode and for transpilation / minification during build - for production the bundling is performed by [Rollup](https://rollupjs.org/guide/en/)

## Features

- SPA (single-page-application) with dynamic routing, see [/src/router/index.ts](/src/router/index.ts)

- pages are rendered by views, see [pages dir](/src/pages)

- reusable components, see [components dir](/src/components)

- development mode support:
    - source maps are installed and allow debugging of components in [Chrome DevTools](https://developers.google.com/web/tools/chrome-devtools/)
    - [Vue.js devtools](https://chrome.google.com/webstore/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd) Chrome extension allows live inspection of routes and models

- back-end RESTful API proxying
    - the back-end must be running locally or via docker (see the [back-end Developer Guide](DEVELOPER_BACK.md) at http://localhost:8080/api
    - during development API requests to the API server get proxied using [`server.proxy` setting in `vite.config.ts`](https://vitejs.dev/config/server-options.html#server-proxy)
    - with the default settings the API endpoints are proxied like this: https://localhost:8000/api/token/ -> http://localhost:8080/api/token/

- authentication:
    - The pages home (http://localhost:8080) and login (http://localhost:8080/login) can be accessed anonimously
    - To access any of the protected pages (for example about: http://localhost:8080/about) you need to log in first
    - To login, the proxied api at http://localhost:8080/api is accessed.
    - The authentication status is tracked with the [store pattern](https://v3.vuejs.org/guide/state-management.html#state-management), see [store dir](/src/store)

## Project setup

Install node dependencies (you'll need nodejs 14+) with:
```
yarnpkg
```

### Compile and hot-reload for development
```
yarnpkg dev --port 8080
```

### Compile and minify for production
```
yarnpkg build
```

### Lint and fix files
```
yarnpkg lint
```

### Customize configuration
See [Configuring Vite](https://vitejs.dev/config/).

## Unit tests

Unit tests are written using:
- [vitest](https://vitest.dev) as the test framework
- the [Vue Testing Library](https://testing-library.com/docs/vue-testing-library/intro) to test component rendering
- the low-level [Vue Test Utils](https://vue-test-utils.vuejs.org/) to test component methods

To run them all in the local install:
```
yarnpkg test --run
```
and to run a specific test:
```
yarnpkg test --run map.spec.js
```

## Reference

**Essential Links**

- [Core Docs](https://vuejs.org)
- [Forum](https://forum.vuejs.org)
- [Community Chat](https://chat.vuejs.org)

**Ecosystem**:

- [vite](https://vitejs.dev)
- [vue-router](https://router.vuejs.org)
- [vuex](https://vuex.vuejs.org)
- [vue-devtools](https://github.com/vuejs/vue-devtools#vue-devtools)
- [vue-loader](https://vue-loader.vuejs.org)
- [awesome-vue](https://github.com/vuejs/awesome-vue)
