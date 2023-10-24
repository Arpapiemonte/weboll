// Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <div
    class="bg-light flex-shrink-0"
  >
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm">
      <div class="container-fluid">
        <router-link
          to="/"
          class="navbar-brand ms-3"
        >
          <img
            src="/images/logo.svg"
            width="100"
            height="50"
            alt="ARPA logo"
          >
        </router-link>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon" />
        </button>
        <div
          id="navbarSupportedContent"
          class="collapse navbar-collapse"
        >
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link
                to="/about"
                class="nav-link"
              >
                About
              </router-link>
            </li>
            <li
              v-for="bulletin in bulletins_list"
              :key="bulletin.id"
              class="nav-item dropdown"
            >
              <a
                :id="`navbarDropdownMenuLink_${bulletin.id}`"  
                class="nav-link dropdown-toggle" 
                href="#" 
                role="button" 
                data-bs-toggle="dropdown" 
                aria-expanded="false"
              >
                {{ bulletin.name }}
              </a>
              <ul 
                class="dropdown-menu" 
                :aria-labelledby="`navbarDropdownMenuLink_${bulletin.id}`"
              >
                <li
                  v-for="bulletin_link in bulletin.my_list"
                  :key="bulletin_link.id"
                >
                  <router-link
                    v-if="appmode === 'development' ? true : bulletin_link.readyForProduction"
                    :to="'/' + bulletin_link.id"
                    class="dropdown-item"
                  >
                    {{ bulletin_link.name }}
                  </router-link>
                </li>
              </ul>
            </li>
          </ul>
          <ul class="d-flex navbar-nav">
            <li
              v-if="state.username"
              class="nav-item"
            >
              <router-link
                to="/"
                class="nav-link"
                @click="logout()"
              >
                Logout @{{ state.username }}
              </router-link>
            </li>
            <li
              v-else
              class="nav-item"
            >
              <router-link
                to="/login"
                class="nav-link"
              >
                Login
              </router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <div>
      <router-view />
    </div>
  </div>
  <footer class="footer mt-auto py-1 bg-primary container-fluid">
    <div class="row">
      <div class="col">
        <span
          id="version_mode"
          class="text-light"
        >weboll {{ vue_app_version }} - mode: {{ appmode }}</span>
      </div>
      <div class="col text-end">
        <span class="text-light">Copyright © 2020-2023 <a
          target="_blank"
          href="https://simevo.com"
          class="link-light"
        >simevo s.r.l.</a> for ARPA Piemonte - Dipartimento Rischi Ambientali e Naturali</span>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from "vue"
import store from './store'

let state = ref(store.state)
let vue_app_version = ref(VUE_APP_VERSION) // eslint-disable-line no-undef

const appmode = computed(() => {
  return import.meta.env.MODE
})

const bulletins_list = computed(() => {
  let arr = []
  for (const [key, value] of Object.entries(window.bulletins_list)) {
    var filteredData = arr.filter(d => d.name === value.menu);
    if (filteredData.length == 0)
      arr.push({
        id: value.menu.trim(),
        name: `${value.menu}`, 
        my_list: [{
          name: `${value.name}`,
          id: `${value.id}`,
          readyForProduction: value.readyForProduction
        }],
      })
    else{
      filteredData[0].my_list.push({ 
        name: value.name,
        id: value.id,
        readyForProduction: value.readyForProduction
      })
    }
  }
  return arr
})

onMounted(() => store.load())

function logout() {
  store.logout()
}

</script>

<style lang="scss">
$primary: #1959a6;
$secondary: #009857;
@import 'bootstrap';
</style>
