// Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 426.26 600.1"
  >
    <g data-name="Piemonte vari layer 480x600">
      <RegionePiene />
    </g>
    <slot name="venues" />
  </svg>
</template>

<script>
// preso della stessa cartella
import RegionePiene from './RegionePiene.vue'

export default {
  name: 'MapBase',
  components: {
    RegionePiene
  },
  props: {

  }
}
</script>

<style scoped="scoped">

</style>
