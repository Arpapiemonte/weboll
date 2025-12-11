// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <span v-if="!readonly">
    <!-- https://icons.getbootstrap.com/icons/caret-up-fill/ -->
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="16"
      height="16"
      fill="currentColor"
      class="bi bi-caret-up-fill"
      viewBox="0 0 16 16"
      style="position:relative;top:-11px;"
      :role="venueSelection.length === 0 ? '' : 'button'"
      :class="{'text-muted': venueSelection.length === 0}"
      @click="$emit('increase')"
    >
      <path d="M7.247 4.86l-4.796 5.481c-.566.647-.106 1.659.753 1.659h9.592a1 1 0 0 0 .753-1.659l-4.796-5.48a1 1 0 0 0-1.506 0z" />
    </svg>
    <!-- https://icons.getbootstrap.com/icons/caret-down-fill/ -->
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="16"
      height="16"
      fill="currentColor"
      class="bi bi-caret-down-fill"
      viewBox="0 0 16 16"
      style="position:relative;left:-16px;bottom:-4px;"
      :role="venueSelection.length === 0 ? '' : 'button'"
      :class="{'text-muted': venueSelection.length === 0}"
      @click="$emit('decrease')"
    >
      <path d="M7.247 11.14L2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z" />
    </svg>
  </span>
</template>

<script>
export default {
  name: 'TermaArrows',
  props: {
    venueSelection: {
      type: Array,
      default: () => []
    },
    readonly: {
      type: Boolean,
      default: false
    },    
  },
  emits: ['decrease', 'increase']
}
</script>
