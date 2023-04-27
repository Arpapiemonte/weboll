// Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <div>
    <nav class="navbar justify-content-center">
      <ul class="nav">
        <li class="nav-item px-2">
          <button
            type="button"
            class="nav-link btn btn-outline-secondary"
            @click="toTop"
          >
            ^ Top
          </button>
        </li>
      </ul>
    </nav>
    <hr class="mb-5">
  </div>  
</template>

<script>
export default {
  name: 'ToTop',
  methods: {
    toTop() {
      const element = document.getElementById("top")
      element.scrollIntoView({ behavior: "smooth" })
    }
  }
}
</script>
