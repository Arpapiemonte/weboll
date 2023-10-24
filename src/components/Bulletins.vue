// Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <LoginModal ref="login" />
  <div class="container-fluid">
    <div class="row">
      <ColMenu />
      <main
        role="main"
        class="col-md-9 ms-sm-auto col-lg-10 pt-3 px-4"
      >
        <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-3 border-bottom">
          <h2>Bollettini {{ name }}</h2>
          <div class="btn-toolbar mb-2 mb-md-0">
            <div class="input-group mb-3">
              <div class="btn-group me-2">
                <button
                  v-if="!oggi_presente && state.username"
                  :disabled="creating"
                  class="btn btn-sm btn-outline-primary"
                  type="button"
                  @click="create()"
                >
                  <span v-if="creating">
                    <span
                      class="spinner-border spinner-border-sm"
                      role="status"
                      aria-hidden="true"
                    />
                    Sto creando il bollettino ...
                  </span>
                  <span v-else>Crea bollettino</span>
                </button>
                <legend>
                  <span v-if="!verifica && state.username">
                    <span style="font-size: small;">
                      Inserire Numero boll piene
                    </span>
                  </span>
                </legend>
                <input
                  v-if="!verifica && state.username"
                  id="num_bollettino"
                  v-model="num_bollettino"
                  :readonly="readonly"
                  class="form-control"
                  name="num_bollettino"
                  type="text"
                  @change="createVerifica(num_bollettino)"
                >
                <!--<legend>
                  <span v-if="!w26 && state.username">
                    <font size="2">
                      Inserire validità
                    </font>
                  </span>
                </legend>
                 <input
                  v-if="!w26 && state.username"
                  id="validita"
                  v-model="validita"
                  :readonly="readonly"
                  class="form-control"
                  name="validita"
                  type="text"
                  @change="createW26(validita)"
                > -->
                <slot
                  name="openW26modal"
                />
                <!--<Datepicker
                  v-if="!verifica && state.username"
                  v-model="data_oggi"
                  :disabled="readonly"
                  :style="readonly ? '--dp-disabled-color: #e9ecef' : '--dp-background-color: white'"
                  format="dd/MM/yyyy"
                  auto-apply
                  @update:modelValue="create()"
                />-->
              </div>
              <label
                class="input-group-text"
                for="inputGroupSelect01"
              >Mese </label>
              <select
                id="inputGroupSelect01"
                v-model="filter.month"
                class="form-select"
              >
                <option
                  disabled
                  value=""
                >
                  Scegli il mese
                </option>
                <option value="all">
                  Tutti
                </option>
                <option value="1">
                  Gennaio
                </option>
                <option value="2">
                  Febbraio
                </option>
                <option value="3">
                  Marzo
                </option>
                <option value="4">
                  Aprile
                </option>
                <option value="5">
                  Maggio
                </option>
                <option value="6">
                  Giugno
                </option>
                <option value="7">
                  Luglio
                </option>
                <option value="8">
                  Agosto
                </option>
                <option value="9">
                  Settembre
                </option>
                <option value="10">
                  Ottobre
                </option>
                <option value="11">
                  Novembre
                </option>
                <option value="12">
                  Dicembre
                </option>
              </select>
              <label
                class="input-group-text"
                for="inputGroupSelect02"
              >Anno </label>
              <select
                id="inputGroupSelect02"
                v-model="filter.year"
                class="form-select"
              >
                <option disabled>
                  Scegli l'anno
                </option>
                <option
                  v-for="year in year_list"
                  :key="year"
                >
                  {{ year }}
                </option>
              </select>
            </div>
          </div>
        </div>
        <div class="table-responsive">
          <table class="table table-striped table-sm">
            <thead class="thead-dark">
              <tr v-if="bulletins.length > 0">
                <th
                  scope="col"
                  style="width:100px;"
                  class="cursor-pointer align-middle"
                  @click="sort(primaryKeyName)"
                >
                  Id {{ currentSort === primaryKeyName ? currentSortDir === 'asc' ? '▲' : '▼' : ' ' }}
                </th>
                <slot
                  name="th1"
                  :current-sort="currentSort"
                  :current-sort-dir="currentSortDir"
                  :sort="sort"
                />
                <th
                  scope="col"
                  style="width:300px;"
                  class="cursor-pointer align-middle"
                  @click="sort('last_update')"
                >
                  Data ultima modifica {{ currentSort === 'last_update' ? currentSortDir === 'asc' ? '▲' : '▼' : ' ' }}
                </th>
                <slot
                  name="th2"
                  :current-sort="currentSort"
                  :current-sort-dir="currentSortDir"
                  :sort="sort"
                />
                <th
                  scope="col"
                  style="width:150px;"
                  class="cursor-pointer align-middle"
                  @click="sort('username')"
                >
                  Autore {{ currentSort === 'username' ? currentSortDir === 'asc' ? '▲' : '▼' : ' ' }}
                </th>
                <th 
                  scope="col"
                  class="align-middle"
                >
                  Stato
                </th>
                <th 
                  scope="col"
                  class="align-middle"
                >
                  Visualizza<br>Modifica
                </th>
                <th 
                  scope="col"
                  class="align-middle"
                >
                  PDF
                </th>
                <th 
                  scope="col"
                  class="align-middle"
                >
                  Elimina
                </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="bulletin in sortedBulletins"
                :key="bulletin[primaryKeyName]"
              >
                <td>
                  {{ bulletin[primaryKeyName] }}
                </td>
                <slot
                  :bulletin="bulletin"
                  name="td1"
                />
                <td>
                  {{ getDateFormatted(bulletin.last_update) }}
                </td>
                <slot
                  :bulletin="bulletin"
                  name="td2"
                />
                <td>{{ bulletin.username }}</td>
                <td>
                  <span v-if="bulletin.status === '1'">Inviato</span>
                  <span v-else-if="bulletin.status === '0'">Bozza</span>
                  <span v-else-if="bulletin.status === 'X'">Bozza</span>
                  <span v-else>Riaperto</span>
                </td>
                <td>
                  <router-link
                    v-slot="{ navigate }"
                    custom
                    :to="`/${detailPage}/${bulletin[primaryKeyName]}`"
                  >
                    <button
                      class="btn btn-outline-secondary btn-sm"
                      role="button"
                      @click="navigate"
                    >
                      <img
                        src="~bootstrap-icons/icons/eye-fill.svg"
                        alt="view icon"
                        width="18"
                        height="18"
                      >
                    </button>
                  </router-link>
                </td>
                <td>
                  <a
                    class="btn btn-outline-primary btn-sm"
                    :href="`/api/${pdfEndpoint}/${bulletin[primaryKeyName]}`"
                    target="_blank"
                    role="button"
                  >
                    <img
                      src="~bootstrap-icons/icons/file-earmark-pdf-fill.svg"
                      alt="PDF icon"
                      width="18"
                      height="18"
                    >
                  </a>
                </td>
                <td>
                  <button
                    :disabled="(bulletin.status !== '0' || !username) && 
                      !(bulletin['id_w17verifica'] !== undefined && 
                        getDateFormatted(bulletin.data_emissione, false) === getDateFormatted(new Date(), false))"
                    type="button"
                    class="btn btn-outline-danger btn-sm"
                    @click="remove(bulletin[primaryKeyName])"
                  >
                    <img
                      src="~bootstrap-icons/icons/trash-fill.svg"
                      alt="delete icon"
                      width="18"
                      height="18"
                    >
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
          <div
            class="fixed-table-pagination"
            style=""
          >
            <div class="float-right pagination">
              <ul class="pagination">
                <li
                  class="page-item page-pre"
                  :class="{disabled: current_page === 0}"
                >
                  <a
                    class="page-link"
                    aria-label="previous page"
                    href="javascript:void(0)"
                    @click="goto(current_page - 1)"
                  >‹</a>
                </li>
                <li
                  v-for="page in pages"
                  :key="page"
                  class="page-item"
                  :class="{ active: current_page === page}"
                >
                  <a
                    class="page-link"
                    :aria-label="'vai alla pagina ' + (page + 1)"
                    href="javascript:void(0)"
                    @click="goto(page)"
                  >{{ page + 1 }}</a>
                </li>
                <li
                  class="page-item page-next"
                  :class="{disabled: current_page === total_pages - 1}"
                >
                  <a
                    class="page-link"
                    aria-label="next page"
                    href="javascript:void(0)"
                    @click="goto(current_page + 1)"
                  >›</a>
                </li>
              </ul>
            </div>
            <span style="font-size: small;">
              Azienda Certificata UNI EN ISO 9001:2015 certificato GCERTI ITALY n° GITI-820-QC
            </span>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
import 'vue-toast-notification/dist/theme-default.css'
import api from '@/api'
import store from '../store'
import ColMenu from '@/components/ColMenu.vue'
import LoginModal from '@/components/LoginModal.vue'

export default {
  name: 'GeneralBulletins',
  components: {
    ColMenu,
    LoginModal,
  },
  props: {
    // name of the primary key
    primaryKeyName: {
      type: String,
      default: "id_w05"
    },
    // back-end endpoint to get the list of bulletins
    endpoint: {
      type: String,
      default: "w05/bulletins"
    },
    // bulletin name to appear in title
    name: {
      type: String,
      default: "Meteo"
    },
    // path slug to bulletin detail page
    detailPage: {
      type: String,
      default: "w05"
    },
    // back-end endpoint to get the bulletin PDF
    pdfEndpoint: {
      type: String,
      default: "w05/pdf"
    },
    dateField: {
      type: String,
      default: "start_valid_time"
    },
  },
  data: function() {
    // non reactive properties
    // this should be the same as the one set in StandardResultsSetPagination class in website/common/views.py:
    this.page_size = 31
    this.username = store.state.username
    return {
      // reactive properties
      state: store.state,
      bulletins: [],
      currentSort: null,
      currentSortDir: 'desc',
      count: 0,
      current_page: 0,
      creating: false,
      deleting_primary_key: 0,
      oggi_presente: true,
      verifica: true,
      w26: true,
      updatew26fetch: 0,
      year_list: [],
      num_bollettino: "num_yyyy",
      validita: "yyyy-mm-dd",
      //data_oggi: "2022-02-10",
      filter: {
        year: (new Date()).getFullYear(),
        month: "all",
      },
    }
  },
  computed: {
    pages () {
      return [...Array(this.total_pages).keys()]
    },
    total_pages() {
      return Math.ceil(this.count / this.page_size)
    },
    sortedBulletins() {
      var sortedBull = this.bulletins
      return sortedBull.sort((a,b) => {
        let modifier = 1;
        if(this.currentSortDir === 'desc') modifier = -1;
        if(a[this.currentSort] < b[this.currentSort]) return -1 * modifier;
        if(a[this.currentSort] > b[this.currentSort]) return 1 * modifier;
        return 0;
      });
    }
  },
  watch: {
    // whenever filter changes, this function will run
    filter: {
      deep: true,
      handler(newValue) {
        this.filter.year = newValue.year
        this.filter.month = newValue.month
        this.goto(0)
      },
    },
  },
  mounted() {
    this.currentSort = this.primaryKeyName
    this.goto(0)
    //this.data_oggi = new Date()
    //this.num_bollettino = "172_2022"
    let year_now = new Date().getFullYear()
    for (var x = year_now; x >= 2010; x--) {
      this.year_list.push(x)
    }
  },
  methods: {
    goto(page) {
      let d = new Date()
      let today = d.toISOString().substring(0, 10)
      this.current_page = page
      this.oggi_presente = true
      this.verifica = true
      this.w26 = true
      api.fetchBulletinsFilter(this.endpoint, {
        page: page,
        year: this.filter.year,
        month: this.filter.month,
      })
      .then(response => {
        if (!response.ok) {
          this.$toast.open(
            {
              message: `Errore ${response.status} nel recupero della lista`,
              type: 'error',
              position: 'top-left'
            }
          )
        }
        return response.json()
      }).then(data => {
        this.bulletins = data.results
        this.count = data.count
      }).catch((error) => {
        this.$toast.open(
          {
            message: error,
            type: 'error',
            position: 'top-left'
          }
        )
      })
      // separately fetch unfiltered page 0 to retrieve the latest bulletins and check whether today's bulletin is present
      api.fetchBulletins(this.endpoint, 0).then(response => {
        if (!response.ok) {
          this.$toast.open(
            {
              message: `Errore ${response.status} nella verifica del bollettino di oggi già presente`,
              type: 'error',
              position: 'top-left'
            }
          )
        }
        return response.json()
      }).then(data => {
        //lista dei bollettino che si possono fare più volte al giorno (w29,w22,w32)
        if (this.endpoint === 'w29/bulletins' || this.endpoint === 'w32/bulletins' || this.endpoint === 'w22/bulletins'){
          this.oggi_presente = false
        }else if(this.endpoint === 'w22verifica/bulletins'){
          this.verifica = false
        }else if(this.endpoint === 'w26/bulletins'){
          this.w26 = false
        }
        else{
          this.oggi_presente = data.results.some(bulletin => bulletin[this.dateField].substring(0, 10) == today)
        }
      }).catch((error) => {
        this.$toast.open(
          {
            message: error,
            type: 'error',
            position: 'top-left'
          }
        )
      })
    },
    remove(id) {
      this.deleting_primary_key = this.bulletins.find(bulletin => bulletin[`id_${this.detailPage}`] === id)[this.primaryKeyName]
      if (
        confirm(`Vuoi davvero cancellare il bollettino ${this.deleting_primary_key}?`)
      ) {
        api.fetchBulletinDelete(id, this.endpoint, store).then(response => {
          if (response.ok) {
            this.$toast.open(
              {
                message: 'Bollettino cancellato',
                type: 'success',
                position: 'top-left'
              }
            )
            this.goto(0)
          } else {
            this.$toast.open(
              {
                message: `Errore ${response.status} nella cancellazione del bollettino`,
                type: 'error',
                position: 'top-left'
              }
            )
            if (response.status === 401 || response.status === 403) {
              this.$refs.login.show()
              return null
            }
          }
        }).catch((error) => {
          this.$toast.open(
            {
              message: error,
              type: 'error',
              position: 'top-left'
            }
          )
        })
      }
    },
    async fetchBulletinNew () {
      const response = await api.fetch_wrapper(
        store.state.access,
        `/api/${this.endpoint}/new/`
      )
      return response
    },
    async fetchBulletinNewVerifica (num_bollettino) {
      const response = await api.fetch_wrapper(
        store.state.access,
        `/api/${this.endpoint}/new/${num_bollettino}/`
      )
      return response
    },
    createVerifica(num_bollettino) {
      this.creating = true
      this.fetchBulletinNewVerifica(num_bollettino).then(async response => {
        this.creating = false
        if (response.ok) {
          this.$toast.open(
            {
              message: 'Bollettino creato',
              type: 'success',
              position: 'top-left'
            }
          )
          var tmp = await response.json()
          this.$router.push({ path: `/${this.detailPage}/${tmp[this.primaryKeyName]}`})
        } else {
          this.$toast.open(
            {
              message: `Errore ${response.status} nella creazione del bollettino`,
              type: 'error',
              position: 'top-left'
            }
          )
          this.creating = false
          if (response.status === 401 || response.status === 403) {
            this.$refs.login.show()
            return null
          }
        }
      }).catch((error) => {
        this.creating = false
        this.$toast.open(
          {
            message: error,
            type: 'error',
            position: 'top-left'
          }
        )
      })
    },    
    create() {
      this.creating = true
      this.fetchBulletinNew().then(async response => {
        this.creating = false
        if (response.ok) {
          this.$toast.open(
            {
              message: 'Bollettino creato',
              type: 'success',
              position: 'top-left'
            }
          )
          var tmp = await response.json()
          this.$router.push({ path: `/${this.detailPage}/${tmp[this.primaryKeyName]}`})
        } else {
          if (response.status === 555) {
            tmp = await response.json()
            this.$toast.open(
              {
                message: `Errore ${tmp.error} nella creazione del bollettino`,
                type: 'error',
                position: 'top-left'
              }
            )
          }else{
            this.$toast.open(
              {
                message: `Errore ${response.status} nella creazione del bollettino`,
                type: 'error',
                position: 'top-left'
              }
            )
            this.creating = false
            if (response.status === 401 || response.status === 403) {
              this.$refs.login.show()
              return null
            }
          }
        }
      }).catch((error) => {
        this.creating = false
        this.$toast.open(
          {
            message: error,
            type: 'error',
            position: 'top-left'
          }
        )
      })
    },
    sort(s) {
      if(s === this.currentSort) {
        this.currentSortDir = this.currentSortDir==='asc'?'desc':'asc';
      }
      this.currentSort = s;
    },
    getDateFormatted(rawString, time = true) {
      return api.getDateFormatted(rawString, time)
    }
  }
}
</script>
