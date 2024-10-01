// Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 426.26 557.1"
  >
    <g data-name="Piemonte vari layer 480x600">
      <MapRegion />
      <MapOrography v-if="orography" />
      <MapRivers v-if="rivers" />
      <MapProvinces v-if="provinces" />
      <MapCapitals v-if="capitals" />
    </g>
    <slot name="venues" />
  </svg>
</template>

<script>
// @ is an alias to /src
import MapRegion from '@/components/MapRegion.vue'
import MapOrography from '@/components/MapOrography.vue'
import MapRivers from '@/components/MapRivers.vue'
import MapProvinces from '@/components/MapProvinces.vue'
import MapCapitals from '@/components/MapCapitals.vue'

export default {
  name: 'MapPiemonte',
  components: {
    MapRegion,
    MapOrography,
    MapRivers,
    MapProvinces,
    MapCapitals
  },
  props: {
    orography: {
      type: Boolean,
      default: true
    },
    rivers: {
      type: Boolean,
      default: true
    },
    provinces: {
      type: Boolean,
      default: true
    },
    capitals: {
      type: Boolean,
      default: true
    }
  }
}
</script>

<style scoped="scoped">
  /* orography colore */
  ::v-deep(.cls-1) {fill:#6ba843}
  ::v-deep(.orography-1) {fill:#6db144}
  ::v-deep(.orography-2) {fill:#85c143}
  ::v-deep(.orography-3) {fill:#acd24f}
  ::v-deep(.orography-4) {fill:#c7b299}
  ::v-deep(.orography-5) {fill:#998675}
  ::v-deep(.orography-6) {fill:#736357}
  ::v-deep(.orography-7) {fill:#534741}
  ::v-deep(.cls-9) {fill:#55caff}
  ::v-deep(.cls-11) {fill:#55caff}
  
  /* orography bianconero 
  ::v-deep(.cls-1) {fill:#eee}
  ::v-deep(.orography-1) {fill:#ddd}
  ::v-deep(.orography-2) {fill:#bbb}
  ::v-deep(.orography-3) {fill:#999}
  ::v-deep(.orography-4) {fill:#888}
  ::v-deep(.orography-5) {fill:#777}
  ::v-deep(.orography-6) {fill:#666}
  ::v-deep(.orography-7) {fill:#555}
  ::v-deep(.cls-9) {fill:#aed9ff}
  ::v-deep(.cls-11) {fill:#aed9ff}
  */

  ::v-deep(.provinces)  {fill:#ffffff00;stroke:#333}
  ::v-deep(.cls-10,.cls-11,.cls-9) {stroke:#0083ca;stroke-linecap:round}
  ::v-deep(.cls-10,.cls-11,.cls-20,.cls-9) {stroke-linejoin:round}
  ::v-deep(.cls-10,.cls-20,.cls-21) {fill:none}
  ::v-deep(.cls-10,.cls-11) {stroke-width:1.5px}
  ::v-deep(.cls-12,.cls-20) {stroke:#000;stroke-width:2px}
  ::v-deep(.cls-12) {stroke-linecap:square;stroke-linejoin:bevel}
  ::v-deep(.cls-13,.cls-14,.cls-15,.cls-17,.cls-18,.cls-19) {isolation:isolate}
  ::v-deep(.cls-13,.cls-15,.cls-16,.cls-17,.cls-18,.cls-19) {font-size:14px;font-family:Arial-BoldMT,Arial;font-weight:700}
  ::v-deep(.cls-15) {letter-spacing:-.02em}
  ::v-deep(.cls-17) {letter-spacing:-.11em}
  ::v-deep(.cls-18) {letter-spacing:-.04em}
  ::v-deep(.cls-19) {letter-spacing:-.04em}
</style>
