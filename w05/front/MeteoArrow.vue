// Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <span>
    <img
      v-if="idTrend == 0"
      src="~bootstrap-icons/icons/arrows-collapse.svg"
      alt="steady"
      width="18"
      height="18"
    >
    <img
      v-if="idTrend == 1"
      src="~bootstrap-icons/icons/arrow-up.svg"
      alt="increasing"
      width="18"
      height="18"
    >
    <img
      v-if="idTrend == 2"
      src="~bootstrap-icons/icons/arrow-down.svg"
      alt="decreasing"
      width="18"
      height="18"
    >
  </span>
</template>

<script>
export default {
  name: 'MeteoArrow',
  props: {
    idTrend: {
      type: Number,
      default: 0
    }
  }
}
</script>
