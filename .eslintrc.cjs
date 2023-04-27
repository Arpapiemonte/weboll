// Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt

/* eslint-env node */
require("@rushstack/eslint-patch/modern-module-resolution")

module.exports = {
  "root": true,
  "extends": [
    "plugin:vue/vue3-recommended",
    "eslint:recommended",
    "@vue/eslint-config-typescript"
  ],
  "parserOptions": {
    "ecmaVersion": "latest"
  },
  "plugins": [
    "notice"
  ],
  "rules": {
    "notice/notice": [
      "error",
      {
        "onNonMatchingHeader": "replace",
        "templateFile": "config/copyright.js"
      }
    ]
  },
  "ignorePatterns": [
    "/website",
    "/tests"
  ]
}
