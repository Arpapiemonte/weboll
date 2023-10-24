// Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <div class="row m-5">
    <div class="col-md-8 offset-md-2">
      <h1>ARPA Piemonte - weboll - bulletin back-office</h1>
      <h2>Bollettini disponibili:</h2>
      <div class="row row-cols-1 row-cols-sm-2 mt-5">
        <div
          v-for="bulletin in filtered_bulletins_list"
          :key="bulletin.id"
          class="col"
        >
          <router-link
            v-slot="{ navigate }"
            :to="'/' + bulletin.id"
            custom
          >
            <div
              class="alert alert-dark d-flex align-items-center mb-1 pb-3 h-75"
              role="button"
              @click="navigate"
            >
              <img
                :src="`/api/static/images/logo_${bulletin.id}.svg`"
                width="80"
                class="img-fluid rounded-start"
                :alt="`Logo ${bulletin.name}`"
              >
              <div class="ms-3 h5">
                {{ bulletin.name }}
              </div>
            </div>
          </router-link>
        </div>
      </div>
      <hr>
      <a
        target="_blank"
        :href="repo_home"
      >Codice sorgente e issues per segnalare malfunzionamenti </a>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue"

const filtered_bulletins_list = computed(() => {
  if (appmode.value === 'development') {
    return window.bulletins_list
  } else {
    return window.bulletins_list.filter(bulletin => bulletin.readyForProduction)
  }
})

const appmode = computed(() => {
  return import.meta.env.MODE
})

const repo_home = computed(() => {
  return import.meta.env.VITE_REPO_HOME || 'https://github.com/Arpapiemonte/weboll'
})
</script>
