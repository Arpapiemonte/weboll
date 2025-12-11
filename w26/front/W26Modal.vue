// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt

<template>
  <div
    id="w26Modal"
    class="modal"
    tabindex="-1"
  >
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            Crea Bollettino Idrologico di Sintesi
          </h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          />
        </div>
        <div class="modal-body">
          <div class="d-flex justify-content-center">
            <div>
              <div
                class="btn-group d-flex"
                role="group"
                aria-label="Toolbar with button groups"
              >
                <div
                  class="btn-group me-2"
                  role="group"
                  aria-label="First group"
                >
                  <button 
                    v-for="(day,index) in days.slice(0, 5)" 
                    :key="day"
                    :disabled="bisavailable[index] !== 2"
                    type="button" 
                    class="btn"
                    :class="bisavailable[index] === 2 ? 'btn-outline-primary': bisavailable[index] === 1 ? 'btn-dark': 'btn-warning'"
                    data-bs-dismiss="modal"
                    @click="createW26(day)"
                  >
                    {{ day }}
                  </button>
                </div>
              </div>
              <div
                class="btn-group"
                role="group"
                aria-label="Toolbar with button groups"
              >
                <div
                  class="btn-group me-2 mt-3"
                  role="group"
                  aria-label="Second group"
                >
                  <button 
                    v-for="(day,index) in days.slice(5, 10)" 
                    :key="day"
                    :disabled="bisavailable[index + 5] !== 2" 
                    type="button" 
                    class="btn"
                    :class="bisavailable[index + 5] === 2 ? 'btn-outline-primary': bisavailable[index + 5] === 1 ? 'btn-dark': 'btn-warning'"
                    data-bs-dismiss="modal"
                    @click="createW26(day)"
                  >
                    {{ day }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button
            class="btn btn-outline-primary"
            style="pointer-events: none"
          >
            Disponibile
          </button>
          <button
            disabled
            class="btn btn-dark"
          >
            Inviato
          </button>
          <button
            disabled
            class="btn bg-warning"
          >
            Bozza
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import 'vue-toast-notification/dist/theme-default.css'

export default {
  name: 'W26Modal',
  props: {
    updatew26fetch: {
      type: Number,
      default: null
    }
  },
  emits: [`createW26`],
  data () {
    return {
      bisavailable: [],
      days: [],
    }
  },
  watch: {
    // whenever filter changes, this function will run
    updatew26fetch: {
      deep: true,
      handler() {
        const today = new Date(new Date().setDate(new Date().getDate()))
        const twentydaysbefore = new Date(new Date().setDate(new Date().getDate()-20))

        const dataValiditaToday = this.dateToString(today)
        const dataValiditatwentydaysbefore = this.dateToString(twentydaysbefore)

        this.fetchAllBis(dataValiditatwentydaysbefore, dataValiditaToday).then(responseAll => {
          if (!responseAll.ok) {
            this.$toast.open(
              {
                message: `Errore ${responseAll.status} nel recupero del bollettino`,
                type: 'error',
                position: 'top-left'
              }
            )
          }
          return responseAll.json()
        }).then(data => {
          this.bisavailable = []
          const allBis = data
          this.days.forEach(d => {
            let available = 2
            allBis.results.forEach(bis => {
              if(bis.data_validita === d){
                if(bis.status === "0" || bis.status === "2"){
                  available = 0
                }else{
                  available = 1
                }
              }
            })
            this.bisavailable.push(available)
          })
        }).catch(error => {
          this.$toast.open(
            {
              message: error,
              type: 'error',
              position: 'top-left'
            }
          )
        })          
      },
    },
  },
  mounted: function () {
    this.days = []
    this.populateBisOlimpia()
  },
  methods: {
    populateBisOlimpia(){
      const today = new Date(new Date().setDate(new Date().getDate()))
      const twentydaysbefore = new Date(new Date().setDate(new Date().getDate()-20))

      const dataValiditaToday = this.dateToString(today)
      const dataValiditatwentydaysbefore = this.dateToString(twentydaysbefore)

      this.fetchBisOlimpia(dataValiditatwentydaysbefore, dataValiditaToday).then(responseAll => {
        if (!responseAll.ok) {
          this.$toast.open(
              {
                message: `Errore ${responseAll.status} nel recupero del bollettino`,
                type: 'error',
                position: 'top-left'
              }
            )
          }
          return responseAll.json()
        }).then(data => {
          let results = data.filter(d => d.numero === 10)
          results = results.slice(0, 10)
          results.reverse()
          results.forEach(bisOlimpia => {
            let dateString = this.dateToString(new Date(bisOlimpia.data))
            this.days.push(dateString)
          })
        }).catch(error => {
          this.$toast.open(
            {
              message: error,
              type: 'error',
              position: 'top-left'
            }
          )
        })
    },
    async fetchAllBis(date_min, date_max){
      const response = await fetch(`/api/w26/bulletins/?data_min=${date_min}&data_max=${date_max}`, {
        headers: {
          accept: 'application/json'
        }
      })
      return response
    },
    async fetchBisOlimpia(date_min, date_max){
      const response = await fetch(`/api/w26/bisbulletins/?data_min=${date_min}&data_max=${date_max}`, {
        headers: {
          accept: 'application/json'
        }
      })
      return response
    },
    createW26(day){
      this.$emit('createW26', day)
    },
    dateToString(date){
      const yy = date.getFullYear()
      const mm = date.getMonth() + 1
      const dd = date.getDate()
      return [yy, (mm>9 ? '' : '0') + mm, (dd>9 ? '' : '0') + dd].join('-')
    }
  }
}

</script>