// Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <div
    id="modalNoteSelect"
    class="modal fade"
    tabindex="-1"
    aria-labelledby="exampleModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5
            id="exampleModalLabel"
            class="modal-title"
          >
            Seleziona le note
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
            v-for="nota in note" 
            :key="nota.nota"
            class="form-check"
          >
            <input
              v-model="nota.checked"
              class="form-check-input"
              type="checkbox"
              @change="changeNoteValue()"
            >
            <label
              class="form-check-label"
              for="flexCheckDefault"
            >
              {{ nota.id }} - {{ nota.nota }}
            </label>
          </div>
        </div>
      </div>
    </div>
  </div>
  <!--  -->
</template>

<script setup lang="ts">
import { ref, watch} from 'vue'

const props = defineProps({
    readonly: Boolean,
    selectedarea: {
        type: Object,
        default: () => {}
    },
})

const emit = defineEmits<{
  saveW26Data: [newValue: object, id_w26_data: number, campo: string]
}>()

let note = ref([
    {
        nota: "Valori non disponibili in banca dati",
        id: "(1)",
        checked: false,
    },
    {
        nota: "Verifica valori in corso",
        id: "(2)",
        checked: false,
    },
    {
        nota: "Sensore in anomalia",
        id: "(3)",
        checked: false,
    }, 
    {
        nota: "Scala di deflusso non applicabile in regime di piena",
        id: "(4)",
        checked: false,
    },
    {
        nota: "Scala non applicabile in regime di magra",
        id: "(5)",
        checked: false,
    },
    {
        nota: "Sensore in secca",
        id: "(6)",
        checked: false,
    },
    {
        nota: "Presenza di detriti/ghiaia nell'area di misura del sensore",
        id: "(7)",
        checked: false,
    },
    {
        nota: "Lavori in alveo",
        id: "(8)",
        checked: false,
    },
    {
        nota: "Scala non applicabile per modifiche alla morfologia della sezione",
        id: "(9)",
        checked: false,
    },
    {
        nota: "Situazione idraulica alterata per la presenza di opere di regolazione in alveo",
        id: "(10)",
        checked: false,
    },
    {
        nota: "Scala di deflusso in fase di ricalibrazione",
        id: "(11)",
        checked: false,
    },
    {
        nota: "Situazione idraulica alterata da derivazioni a monte sezione",
        id: "(12)",
        checked: false,
    },
    {
        nota: "Dato stimato sulla base di misure e/o osservazioni dirette",
        id: "(13)",
        checked: false,
    },
    {
        nota: "Sezione con portata quasi nulla",
        id: "(14)",
        checked: false,
    },
    {
        nota: "Dati relativi al secondo sensore idrometrico",
        id: "(15)",
        checked: false,
    },
    {
        nota: "Valore non significativo per effetto delle regolazioni artificiali a monte",
        id: "(16)",
        checked: false,
    },
    {
        nota: "Dato valutato in base a calcoli teorici",
        id: "(17)",
        checked: false,
    }
])
let ready = ref(false)

watch(() => props.selectedarea, (newselection) => {
  ready.value = false
  for(const index in note.value){
    note.value[index].checked = false
    if(newselection.idnota && newselection.idnota.includes(note.value[index].id)){
      note.value[index].checked = true
    }
  }
  ready.value = true
},{ deep: true })

function changeNoteValue() {
  let idnota = ''
  let nota = ''
  for(const index in note.value){
    if(note.value[index].checked){
      idnota += note.value[index].id
      if(nota === ''){
        nota += note.value[index].id + " - " + note.value[index].nota
      }else{
        nota += ", " + note.value[index].id + " - " + note.value[index].nota
      }
    }
  }
  saveW26Data({idnota: idnota,  nota: nota}, props.selectedarea.id_w26_data,"idnota")
}

function saveW26Data(newValue,id_w26_data,campo) {
    emit('saveW26Data', newValue,id_w26_data,campo)
}
</script>