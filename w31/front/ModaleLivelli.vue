// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt

<template>
  <div
    id="ModaleLivelli"
    class="modal"
    tabindex="-1"
    aria-labelledby="iconModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5
            id="iconModalLabel"
            class="modal-title"
          >
            Cambia il livello per la macroarea {{ selectedShape }}: {{ selectedDenominazione }}
          </h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          />
        </div>
        <div class="modal-body">
          <div
            class="btn-group"
            role="group"
            aria-label="Icons"
          >
            <button
              v-for="livello in livelli"
              :key="livello.id_w31_livelli"
              type="button"
              class="btn btn-outline-dark"
              @click="setLevel(livello.id_w31_livelli)"
            >
              <svg
                width="75"
                height="60"
                viewBox="0 0 750 600"
              >
                <rect
                  x="0"
                  y="0"
                  width="750"
                  height="600"
                  :fill="livello.colore"
                />
              </svg>
              {{ livello.id_w31_livelli }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ModaleLivelli',
  props: {
    selectedShape: {
      type: Number,
      default: null
    },
    selectedDenominazione: {
      type: String,
      default: null
    },
    livelli: {
      type: Array,
      default: () => []
    },
    venueData: {
      type: Object,
      default: () => {}
    },
  },
  emits: ['saveLevel'],
  methods: {
    setLevel(value) {
      // console.log(`setLevel(${value})`)
      this.$emit('saveLevel', value)
    },
  }
}
</script>