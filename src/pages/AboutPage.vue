// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <div class="container-fluid">
    <div class="row">
      <ColMenu />
      <main
        role="main"
        class="col-md-9 ms-sm-auto col-lg-10 pt-3 px-4"
      >
        <div class="pb-2 mb-3 border-bottom">
          <h2>
            weboll è il nuovo back-office per la redazione dei bollettini ARPA Piemonte Centro Funzionale
          </h2>
          <p>
            Il codice sorgente è disponibile sulla <a
              :href="repo_home"
              target="_blank"
            >piattaforma di sviluppo collaborativo Gitlab di ARPA Piemonte</a> dove è anche possibile segnalare malfunzionamenti o suggerire nuove funzioni.
          </p>
          <p>
            weboll è Copyright (C) 2025 Arpa Piemonte - Dipartimento Rischi Ambientali e Naturali e licenziato con la <a
              href="http://www.gnu.org/licenses/agpl-3.0.html"
              target="_blank"
            >GNU Affero General Public License version 3 o successiva</a>.
          </p>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue"
import ColMenu from '@/components/ColMenu.vue'

const repo_home = computed(() => {
  return import.meta.env.VITE_REPO_HOME || 'https://github.com/Arpapiemonte/weboll'
})
</script>
