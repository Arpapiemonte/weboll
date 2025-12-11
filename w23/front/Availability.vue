// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <span
    class="badge rounded-pill user-select-none"
    :class="{'text-bg-secondary': availability, 'text-bg-danger': !availability}"
    :title="availability ? 'disponibile' : 'non disponibile'"
  >
    {{ name }}
  </span>
</template>

<script>
export default {
  name: 'AvailabilityPill',
  props: {
    name: {
      type: String,
      default: ""
    },
    availability: {
      type: Boolean,
      default: false
    }
  }
}
</script>
