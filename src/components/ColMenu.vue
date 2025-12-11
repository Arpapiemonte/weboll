// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <!-- start col menu -->
  <nav class="col-md-2 d-none d-md-block bg-light sidebar">
    <div class="sidebar-sticky mt-4">
      <h6 class="sidebar-heading d-flex justify-content-between align-items-center px-3 mt-4 mb-1 text-muted">
        <span>ARPA Piemonte extranet</span>
      </h6>
      <ul class="nav flex-column">
        <li class="nav-item">
          <a
            class="nav-link active"
            href="https://www.arpa.piemonte.it/"
            target="_blank"
          >
            Public
          </a>
        </li>
      </ul>

      <hr>

      <h6 class="sidebar-heading d-flex justify-content-between align-items-center px-3 mt-4 mb-1 text-muted">
        <span>Bollettini</span>
      </h6>
      <ul class="nav flex-column mb-2">
        <li class="nav-item">
          <a
            class="nav-link active"
            :href="repo_home"
            target="_blank"
          >
            weboll: codice e issues
          </a>
        </li>
        <li
          v-for="bulletin in bulletins_list"
          :key="bulletin.id"
          class="nav-item"
        >
          <router-link
            v-if="appmode === 'development' ? true : bulletin.readyForProduction"
            class="nav-link active"
            :to="'/' + bulletin.id"
          >
            {{ bulletin.name }}
          </router-link>
        </li>
      </ul>
    </div>
  </nav>
<!-- end menu -->
</template>

<script setup lang="ts">
import { computed } from "vue"

const bulletins_list = window.bulletins_list

const appmode = computed(() => {
  return import.meta.env.MODE
})

const repo_home = computed(() => {
  return import.meta.env.VITE_REPO_HOME || 'https://github.com/Arpapiemonte/weboll'
})
</script>
