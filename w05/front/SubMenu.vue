// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <nav
    class="navbar justify-content-center sticky-top bg-light border-bottom"
    style="top:88px;"
  >
    <ul class="nav">
      <li class="nav-item px-1">
        <a
          class="nav-link"
          :class="{'text-danger': skyconditInvalid}"
          @click="goto('SkyCond')"
        >
          Sky Condition
        </a>
      </li>
      <li class="nav-item px-1">
        <a
          class="nav-link"
          :class="{'text-danger': nuvolositaInvalid}"
          @click="goto('Nuvolosita')"
        >
          Nuvolosità
        </a>
      </li>
      <li class="nav-item px-1">
        <a
          class="nav-link"
          :class="{'text-danger': precipitazioniInvalid}"
          @click="goto('Precipitazioni')"
        >
          Precipitazioni
        </a>
      </li>
      <li class="nav-item px-1">
        <a
          class="nav-link"
          :class="{'text-danger': zeroInvalid}"
          @click="goto('ZeroTermico')"
        >
          Zero Termico
        </a>
      </li>
      <li class="nav-item px-1">
        <a
          class="nav-link"
          :class="{'text-danger': ventiInvalid}"
          @click="goto('Venti')"
        >
          Venti
        </a>
      </li>
      <li class="nav-item px-1">
        <a
          class="nav-link"
          :class="{'text-danger': altriFenomeniInvalid}"
          @click="goto('AltriFenomeni')"
        >
          Altri Fenomeni
        </a>
      </li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: 'SubMenu',
  props: {
    skyconditInvalid: {
      type: Boolean,
      default: true
    },
    nuvolositaInvalid: {
      type: Boolean,
      default: true
    },
    precipitazioniInvalid: {
      type: Boolean,
      default: true
    },
    zeroInvalid: {
      type: Boolean,
      default: true
    },
    ventiInvalid: {
      type: Boolean,
      default: true
    },
    altriFenomeniInvalid: {
      type: Boolean,
      default: true
    },
  },
  methods: {
    goto(id) {
      const element = document.getElementById(id)
      element.scrollIntoView({ behavior: "smooth" })
    }
  }
}
</script>
