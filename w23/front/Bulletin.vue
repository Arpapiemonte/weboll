// Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <div
    v-if="ready"
    class="container-fluid"
  >
    <div
      class="row justify-content-end sticky-top py-1"
      style="background-color: #f8f9fa;"
    >
      <div
        v-if="allerta.status === '0' && allerta.data_emissione === today"
        class="col"
      >
        <Availability
          name="psa"
          :availability="availability.psa"
        />
        <Availability
          name="vigilanza"
          :availability="availability.vigilanza"
        />
        <Availability
          name="pluvoss"
          :availability="availability.pluvoss"
        />
        <span class="badge rounded-pill text-bg-primary">risk_val
          <Availability
            name="oggi"
            :availability="availability.risk_val_oggi"
          />
          <Availability
            name="domani"
            :availability="availability.risk_val_domani"
          />
        </span>
      </div>

      <div
        class="btn-group w-auto"
        role="group"
      >
        <button
          v-if="allerta.status === '0' && allerta.data_emissione === today && state.username"
          :disabled="sending || firstguessing"
          type="button"
          class="btn btn-outline-dark"
          @click="execute('firstguess', false, 'First guess completata')"
        >
          <span v-if="firstguessing">
            <span
              class="spinner-border spinner-border-sm"
              role="status"
              aria-hidden="true"
            />
            Sto calcolando la first guess ...
          </span>
          <span v-else>
            <img
              src="~bootstrap-icons/icons/calculator.svg"
              alt="calc icon"
              width="18"
              height="18"
            > Aggiorna First Guess
          </span>
        </button>
        <a
          class="btn btn-outline-primary"
          :href="'/api/w23/xml/' + allerta.id_w23"
          target="_blank"
          role="button"
        >
          <img
            src="~bootstrap-icons/icons/filetype-xml.svg"
            alt="PDF icon"
            width="18"
            height="18"
          > XML-CAP
        </a>
        <a
          class="btn btn-outline-primary"
          :href="'/api/w23/kml36h/' + allerta.id_w23"
          target="_blank"
          role="button"
        >
          <img
            src="~bootstrap-icons/icons/filetype-xml.svg"
            alt="PDF icon"
            width="18"
            height="18"
          > KML
        </a>
        <a
          class="btn btn-outline-primary"
          :href="'/api/w23/png/' + allerta.id_w23"
          target="_blank"
          role="button"
        >
          <img
            src="~bootstrap-icons/icons/file-earmark-image.svg"
            alt="PDF icon"
            width="18"
            height="18"
          > PNG
        </a>
        <a
          class="btn btn-outline-primary"
          :href="'/api/w23/rupar_png/' + allerta.id_w23"
          target="_blank"
          role="button"
        >
          <img
            src="~bootstrap-icons/icons/file-earmark-image.svg"
            alt="PDF icon"
            width="18"
            height="18"
          > RUPAR
        </a>
        <a
          class="btn btn-outline-primary"
          :href="'/api/w23/pdf/' + allerta.id_w23"
          target="_blank"
          role="button"
        >
          <img
            src="~bootstrap-icons/icons/file-earmark-pdf-fill.svg"
            alt="PDF icon"
            width="18"
            height="18"
          > PDF
        </a>
        <button
          v-if="allerta.status === '1' && state.username && allerta.data_emissione.substring(0, 10) === today"
          type="button"
          class="btn btn-outline-warning"
          @click="execute('reopen', true, 'Bollettino riaperto')"
        >
          <span v-if="reopening">
            <span
              class="spinner-border spinner-border-sm"
              role="status"
              aria-hidden="true"
            />
            Sto riaprendo il bollettino ...
          </span>
          <span v-else>
            <img
              src="~bootstrap-icons/icons/unlock-fill.svg"
              alt="unlock icon"
              width="18"
              height="18"
            > Riapri
          </span>
        </button>
        <button
          v-if="allerta.status === '0' && allerta.data_emissione === today && state.username"
          :disabled="sending || firstguessing || allerta.fraserisknat.trim().length===0 || allerta.fraserisknat === vigilanza.sintesi_meteo" 
          type="button"
          class="btn btn-outline-success"
          @click="execute_timeout('send', false, 'Bollettino inviato')"
        >
          <span v-if="sending">
            <span
              class="spinner-border spinner-border-sm"
              role="status"
              aria-hidden="true"
            />
            Sto inviando il bollettino ...
          </span>
          <span v-else>
            <img
              src="~bootstrap-icons/icons/send-fill.svg"
              alt="envelope icon"
              width="18"
              height="18"
            > Invia
          </span>
        </button>
        <button
          v-if="allerta.status === '0' && state.username"
          type="button"
          class="btn btn-outline-danger"
          @click="remove()"
        >
          <img
            src="~bootstrap-icons/icons/trash-fill.svg"
            alt="trashbin icon"
            width="18"
            height="18"
          > Elimina
        </button>
      </div>
    </div>
    <div class="row mb-3">
      <h1>Bollettino Allerta {{ allerta.numero_bollettino }}</h1>
    </div>
    <div class="row">
      <div class="col-md-2 mb-3">
        <label for="status">Stato
          <span v-if="allerta.status == 1">
            <input
              id="stato"
              disabled
              class="form-control"
              name="stato"
              type="text"
              value="Inviato"
            >
          </span>
          <span v-else-if="allerta.status == 2">
            <input
              id="stato"
              disabled
              class="form-control"
              name="stato"
              type="text"
              value="Riaperto"
            >
          </span>
          <span v-else>
            <input
              id="stato"
              disabled
              class="form-control"
              name="stato"
              type="text"
              value="Bozza"
            >
          </span>
        </label>
      </div>
      <div class="col-md-2 mb-3">
        <label for="data_emissione">Data emissione
          <input
            id="data_emissione"
            disabled
            class="form-control"
            name="data_emissione"
            type="text"
            :value="oggi"
          >
        </label>
      </div>
      <div class="col-md-2 mb-3">
        <label for="last_update">Ultima modifica
          <input
            id="last_update"
            disabled
            class="form-control"
            name="last_update"
            type="text"
            :value="getDateFormatted(allerta.last_update)"
          >
        </label>
      </div>
      <div class="col-md-2 mb-3">
        <label for="username">Autore
          <input
            id="username"
            disabled
            class="form-control"
            name="username"
            type="text"
            :value="allerta.username"
          >
        </label>
      </div>
    </div>
    <div class="row mt-3">
      <div class="col-xl-12 col-md-12 mb-3">
        <ul
          class="nav nav-tabs nav-justified sticky-top bg-light"
          style="top: 46px;"
          role="tablist"
        >
          <li
            class="nav-item"
            role="presentation"
          >
            <button
              id="pills-base_bollettino-tab"
              class="nav-link active"
              data-bs-toggle="pill"
              data-bs-target="#pills-base_bollettino"
              type="button"
              role="tab"
              aria-controls="pills-base_bollettino"
              aria-selected="true"
            >
              Base Bollettino
            </button>
          </li>
          <li
            class="nav-item"
            role="presentation"
          >
            <button
              id="pills-bollettino_emesso-tab"
              class="nav-link"
              data-bs-toggle="pill"
              data-bs-target="#pills-bollettino_emesso"
              type="button"
              role="tab"
              aria-controls="pills-bollettino_emesso"
              aria-selected="false"
            >
              Bollettino emesso
            </button>
          </li>
          <li
            class="nav-item"
            role="presentation"
          >
            <button
              id="pills-annotazione-tab"
              class="nav-link"
              data-bs-toggle="pill"
              data-bs-target="#pills-annotazione"
              type="button"
              role="tab"
              aria-controls="pills-annotazione"
              aria-selected="false"
            >
              Annotazione
            </button>
          </li>
          <li
            class="nav-item"
            role="presentation"
          >
            <button
              id="pills-pioggia-massima-tab"
              class="nav-link"
              data-bs-toggle="pill"
              data-bs-target="#pills-pioggia-massima"
              type="button"
              role="tab"
              aria-controls="pills-pioggia-massima"
              aria-selected="false"
            >
              Pioggia massima
            </button>
          </li>
          <li
            class="nav-item"
            role="presentation"
          >
            <button
              id="pills-pioggia-media-tab"
              class="nav-link"
              data-bs-toggle="pill"
              data-bs-target="#pills-pioggia-media"
              type="button"
              role="tab"
              aria-controls="pills-pioggia-media"
              aria-selected="false"
            >
              Pioggia media
            </button>
          </li>
          <li
            class="nav-item"
            role="presentation"
          >
            <button
              id="pills-neve-tab"
              class="nav-link"
              data-bs-toggle="pill"
              data-bs-target="#pills-neve"
              type="button"
              role="tab"
              aria-controls="pills-neve"
              aria-selected="false"
            >
              Neve
            </button>
          </li>
          <li
            class="nav-item"
            role="presentation"
          >
            <button
              id="pills-frase_risknat-tab"
              class="nav-link"
              :class="{'text-danger': allerta.fraserisknat.trim().length===0 || allerta.fraserisknat === vigilanza.sintesi_meteo }"
              data-bs-toggle="pill"
              data-bs-target="#pills-frase_risknat"
              type="button"
              role="tab"
              aria-controls="pills-frase_risknat"
              aria-selected="false"
            >
              Frase sito Arpa
            </button>
          </li>
          <li
            class="nav-item"
            role="presentation"
          >
            <button
              id="pills-criteri-tab"
              class="nav-link"
              data-bs-toggle="pill"
              data-bs-target="#pills-criteri"
              type="button"
              role="tab"
              aria-controls="pills-criteri"
              aria-selected="false"
            >
              Criteri
            </button>
          </li>
        </ul>
        <div
          class="tab-content"
        >
          <div
            id="pills-base_bollettino"
            class="tab-pane fade show active"
            role="tabpanel"
            aria-labelledby="pills-base_bollettino-tab"
          >
            <div class="row">
              <div class="col-xl-8 col-md-12 mb-3">
                <nav
                  class="navbar justify-content-center sticky-top bg-light border-bottom"
                  style="top: 88px;"
                >
                  <ul class="nav">
                    <li
                      class="nav-item px-1"
                      @click="goto('oggi')"
                    >
                      <a class="nav-link"> Oggi </a>
                    </li>
                    <li
                      class="nav-item px-1"
                      @click="goto('domani')"
                    >
                      <a class="nav-link"> Domani </a>
                    </li>
                  </ul>
                </nav>
                <div
                  id="oggi"
                  class="offset"
                >
                  <h3>Oggi {{ oggi }}</h3>
                  <TabellaAllerta
                    :readonly="true"
                    :coloreriskstorm="colore_risk_storm_oggi"
                    :pericolo-massimo="pericolo_massimo_oggi_for"
                    :w23data="allerta.w23data_set"
                    :lista-parametri="lista_parametri_oggi_for"
                  />
                </div> <!-- row -->
                <div
                  id="domani"
                  class="offset"
                >
                  <h3>Domani {{ domani }}</h3>
                  <TabellaAllerta
                    :readonly="true"
                    :coloreriskstorm="colore_risk_storm_domani"
                    :pericolo-massimo="pericolo_massimo_domani_for"
                    :w23data="allerta.w23data_set"
                    :lista-parametri="lista_parametri_domani_for"
                  />
                </div> <!-- row -->
              </div>  <!--col-->
              <div class="col-xl-4 col-md-12 mb-3">
                <div
                  class="sticky-top pt-5"
                  style="z-index: 0;"
                >
                  <MapAllerta
                    v-if="Object.keys(pericolo_massimo_for).length > 0"
                    :orography="false"
                    :rivers="false"
                    :provinces="false"
                    :capitals="false"
                    :layer="true"
                    :venue-data="pericolo_massimo_for"
                  />
                </div>
              </div> <!-- col -->
            </div> <!-- row -->
          </div>

          <div
            id="pills-bollettino_emesso"
            class="tab-pane fade"
            role="tabpanel"
            aria-labelledby="pills-bollettino_emesso-tab"
          >
            <div class="row">
              <div class="col-xl-10 col-md-12 mb-3">
                <nav
                  class="navbar justify-content-center sticky-top bg-light border-bottom"
                  style="top: 88px;"
                >
                  <ul class="nav">
                    <li
                      class="nav-item px-1"
                      @click="goto('oggi1')"
                    >
                      <a class="nav-link"> Oggi </a>
                    </li>
                    <li
                      class="nav-item px-1"
                      @click="goto('domani1')"
                    >
                      <a class="nav-link"> Domani </a>
                    </li>
                    <li
                      class="nav-item px-1"
                      @click="goto('situa')"
                    >
                      <a class="nav-link"> Note </a>
                    </li>
                  </ul>
                </nav>
                <div
                  id="oggi1"
                  class="offset"
                  style="z-index: 2;"
                >
                  <h3>Oggi {{ oggi }}</h3>
                  <TabellaAllerta
                    :scenario="true"
                    :readonly="(allerta.status !== '0' || !state.username)"
                    :pericolo-massimo="pericolo_massimo_oggi"
                    :w23data="allerta.w23data_set"
                    :lista-parametri="lista_parametri_oggi"
                    :pericoli="pericoli"
                    :effetti="effetti"
                    :coloreriskstorm="colore_risk_storm_oggi"
                    @save-data="saveData"
                    @save-data-pericolo="saveDataPericolo"
                  />
                </div> <!-- row -->
                <div
                  id="domani1"
                  class="offset"
                  style="z-index: 1;"
                >
                  <h3>Domani {{ domani }}</h3>
                  <TabellaAllerta
                    :scenario="true"
                    :readonly="(allerta.status !== '0' || !state.username)"
                    :pericolo-massimo="pericolo_massimo_domani"
                    :w23data="allerta.w23data_set"
                    :lista-parametri="lista_parametri_domani"
                    :pericoli="pericoli"
                    :effetti="effetti"
                    :coloreriskstorm="colore_risk_storm_domani"
                    @save-data="saveData"
                    @save-data-pericolo="saveDataPericolo"
                  />
                </div> <!-- row -->
                <div
                  id="situa"
                >
                  <h3>Note</h3>
                  <textarea
                    id="situazione_meteo"
                    v-model="allerta.situazione_meteo"
                    :disabled="(allerta.status !== '0' || !state.username)"
                    name="situazione_meteo"
                    rows="3"
                    cols="120"
                    @change="saveField('situazione_meteo')"
                  />
                </div> <!-- row -->
              </div>  <!--col-->
              <div class="col-xl-2 col-md-12 mb-3">
                <div
                  class="sticky-top pt-5"
                  style="z-index: 0;"
                >
                  <MapAllerta
                    v-if="Object.keys(pericolo_massimo).length > 0"
                    :orography="false"
                    :rivers="false"
                    :provinces="false"
                    :capitals="false"
                    :layer="true"
                    :venue-data="pericolo_massimo"
                    :area-pericolo="area_pericolo"
                  />
                </div>
              </div> <!-- col -->
            </div> <!-- row -->
          </div>

          <div
            id="pills-annotazione"
            class="tab-pane fade"
            role="tabpanel"
            aria-labelledby="pills-annotazione-tab"
          >
            .
            <div class="col-md-12 mb-3">
              <h3>Ultima modifica annotazione</h3>
              <input
                id="last_update_annotazione"
                disabled
                class="form-control"
                name="last_update_annotazione"
                type="text"
                :value="getDateFormatted(allerta.last_update_annotazione)"
              >
              <br>
              <h3>Annotazione</h3>
              <textarea
                id="annotazione"
                v-model="allerta.annotazione"
                name="annotazione"
                rows="5"
                cols="120"
                @change="saveField('annotazione')"
              />
              <br>
              <h4>La modifica dei livelli può avvenire in base ai seguenti elementi:</h4>
              <ul>
                <li>entità dello scostamento dei valori derivanti dalle previsioni numeriche con i valori di riferimento</li>
                <li>condizioni pregresse (precipitazioni precedenti che determinano condizioni di saturazione del suolo; nevicate precedenti ancora al suolo che, sommate a quelle previste, determinano situazioni critiche; livelli idrometrici elevati; situazioni emergenziali per rischio meteo-idrogeologico e idraulico in corso, particolari vulnerabilità note o segnalate dalla SOR come incendi boschivi in grado di determinare un rischio maggiore di fenomeni erosivi e franosi)</li>
                <li>incertezza previsionale (nella localizzazione spaziale e/o nell’intensità dei fenomeni)</li>
                <li>fenomeni che interessano molto parzialmente un’area di allerta o una porzione considerata meno vulnerabile dell’area di allerta (alta montagna)</li>
                <li>fenomeni attesi alla scadenza della validità dell’allerta (tipicamente oltre le 30h) per i quali vi sia un’incertezza previsionale nota</li>
                <li>situazioni contingenti note o segnalate dalla SOR o dalle prefetture o dal DPC (eventi di rilevanza regionale che comportano una elevata esposizione -concerti, eventi culturali, sportivi, manifestazioni-; esercitazioni di protezione civile; criticità rilevanti su reticolo viario principale, ponti, autostrade; condizioni di apertura dei passi di montagna; primi eventi della stagione…)</li>
                <li>valutazioni di opportunità in relazione al grado di allerta emesso dalle Regioni confinanti, che possono essere consultate</li>
              </ul>
            </div>
          </div>
          <div
            id="pills-frase_risknat"
            class="tab-pane fade"
            role="tabpanel"
            aria-labelledby="pills-frase_risknat-tab"
          >
            <div class="col-md-12 mb-3">
              <h3>Frase sito Arpa</h3>
              <textarea
                id="frase_risknat"
                v-model="allerta.fraserisknat"
                :disabled="(allerta.status !== '0' || !state.username)"
                name="frase_risknat"
                rows="5"
                cols="120"
                @change="saveField('fraserisknat')"
              />
            </div>
            <br>
            <h4>NB: La frase deve essere diversa dalla frase proposta dal bollettino di vigilanza e non vuota.</h4>
          </div>

          <div
            id="pills-pioggia-massima"
            class="tab-pane fade"
            role="tabpanel"
            aria-labelledby="pills-pioggia-massima-tab"
          >
            <div
              class="col-md-12 mb-3"
            >
              <TabellaPioggiaMax
                :debug="debug"
                :labels="labels"
                :soglie="soglie_pluv_area_prev_massimi"
                :piogge-massime="piogge_massime"
              />
            </div>
          </div>
          <div
            id="pills-pioggia-media"
            class="tab-pane fade"
            role="tabpanel"
            aria-labelledby="pills-pioggia-media-tab"
          >
            <div
              class="col-md-12 mb-3"
            >
              <TabellaPioggiaAvg
                :debug="debug"
                :labels="labels"
                :soglie="soglie_pluv_area_prev_medie"
                :piogge-medie="piogge_medie"
                :tls="tls"
              />
            </div>
          </div>

          <div
            id="pills-neve"
            class="tab-pane fade"
            role="tabpanel"
            aria-labelledby="pills-neve-tab"
          >
            <div
              class="col-md-12 mb-3"
            >
              <TabellaNeve
                :debug="debug"
                :soglie="soglie_nivo_area_prev"
                :neve="neve"
              />
            </div>
          </div>
          <div
            id="pills-criteri"
            class="tab-pane fade"
            role="tabpanel"
            aria-labelledby="pills-criteri-tab"
          >
            <div class="col-md-12 mb-3">
              <h3>Criteri</h3>
              <div
                class="sticky-top pt-5"
                style="z-index: 0;"
              >
                <img
                  src="/images/criteri.png"
                  class="img-fluid"
                  alt="test"
                >
                <br>
                <h3>Criteri Bollettino allerta</h3>
                <li>Il superamento della soglia della singola area è riferito alla fine della scadenza e colora solo il giorno di fine scadenza</li>
                <li>Il massimo allerta è il colore massimo per la stessa area di ogni fenomeno sui due giorni</li>
                <li>Per avere un colore diverso dal verde sul fenomeno "Idrogeologico per temporali" ci deve essere superamento sia sulle piogge massime che sui temporali(Vigilanza)</li>
                <li>Per avere un colore diverso dal verde sul fenomeno Idrogeologico è necessario avere due superamenti di durate diverse sulle piogge massime</li>
                <li>Per avere un colore diverso dal verde sul fenomeno Idraulico è necessario avere due superamenti di durate diverse sulle piogge medie</li>
                <li>Per avere un colore diverso dal verde sul fenomeno neve è necessario avere un superamento sulla neve prevista (neve da vigilanza sotto i 1300m)</li>
                <li>Il colore sul fenomeno Valanghe si ottiene da una procedura che converte opportunamente i gradi di pericolo valanghe</li>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div> <!-- row -->
    <MapBase />
  </div>
</template>

<script>
import api from '@/api'
import store from '@/store'
import Availability from './Availability.vue'
import MapAllerta from './MapAllerta.vue'
import MapBase from './MapBase.vue'
import TabellaAllerta from './TabellaAllerta.vue'
import TabellaNeve from './TabellaNeve.vue'
import TabellaPioggiaMax from './TabellaPioggiaMax.vue'
import TabellaPioggiaAvg from './TabellaPioggiaAvg.vue'

const status_first_time = 'X'

export default {
  name: 'AllertaBulletin',
  components: {
    Availability,
    MapAllerta,
    MapBase,
    TabellaAllerta,
    TabellaNeve,
    TabellaPioggiaMax,
    TabellaPioggiaAvg
  },
  props: {
    id: {
      type: String,
      default: () => ''
    },
  },
  data () {
    // non reactive properties
    this.righe = ["Piem-A", "Piem-B", "Piem-C", "Piem-D", "Piem-E", "Piem-F", "Piem-G", "Piem-H", "Piem-I", "Piem-L", "Piem-M"]
    this.lista_parametri = ['idrogeologico', 'temporali', 'idraulico', 'neve', 'valanghe']
    this.lista_parametri_oggi = this.lista_parametri.map(p => p + '_oggi')
    this.lista_parametri_domani = this.lista_parametri.map(p => p + '_domani')
    this.lista_parametri_oggi_for = this.lista_parametri_oggi.map(p => p + '_for')
    this.lista_parametri_domani_for = this.lista_parametri_domani.map(p => p + '_for')
    this.lista_parametri_oggi_domani = this.lista_parametri_oggi.concat(this.lista_parametri_domani)
    this.lista_parametri_oggi_domani_for = this.lista_parametri_oggi_domani.map(p => p + '_for')
    this.lista_parametri_completa = this.lista_parametri_oggi_domani.concat(this.lista_parametri_oggi_domani_for)
    //Fenomeno idraulico
    this.lista_parametro_idraulico = ['idraulico']
    this.lista_parametri_oggi_idraulico = this.lista_parametro_idraulico.map(p => p + '_oggi')
    this.lista_parametri_domani_idraulico = this.lista_parametro_idraulico.map(p => p + '_domani')
    this.lista_parametri_oggi_domani_idraulico = this.lista_parametri_oggi_idraulico.concat(this.lista_parametri_domani_idraulico)
    this.tls = {
      900: [{id:45, role:0}, {id:46, role:0}, {id:60, role:0}, {id:61, role:0}, {id:62, role:0}, {id:63, role:0}, {id:77, role:1}, {id:78, role:1}, {id:79, role:1}, {id:80, role:1}],
      901: [
        {
          id:1009,
          role:-1,
          sources: [44, 45],
          counts: {},
        },
        {id:48, role:0},
        {id:1011, role:0},
        {id:64, role:0},
        {id:1013, role:0},
        {id:65, role:0},
        {id:1015, role:1},
        {id:81, role:1},
        {id:1017, role:1},
        {id:82, role:1}
      ],
      902: [
        {
          id:2006,
          role:-1,
          sources: [29, 43, 44, 45],
          counts: {},
        },
        {
          id:49,
          role:-1,
          sources: [43, 44, 45, 46],
          counts: {},
        },
        {
          id:2009,
          role:-1,
          sources: [44, 45, 46, 60],
          counts: {},
        },
        {id:2010, role:0},
        {id:2011, role:0},
        {id:66, role:0},
        {id:2014, role:1},
        {id:2015, role:1},
        {id:2016, role:1},
        {id:83, role:1}
      ],
      903: [
        {
          id:3003,
          role:-1,
          sources: [12, 26, 27, 28, 29, 43, 44, 45],
          counts: {},
        },
        {
          id:3004,
          role:-1,
          sources: [26, 27, 28, 29, 43, 44, 45, 46],
          counts: {},
        },
        {
          id:3005,
          role:-1,
          sources: [27, 28, 29, 43, 44, 45, 46, 60],
          counts: {},
        },
        {
          id:3006,
          role:-1,
          sources: [28, 29, 43, 44, 45, 46, 60, 61],
          counts: {},
        },
        {
          id:3007,
          role:-1,
          sources: [29, 43, 44, 45, 46, 60, 61, 62],
          counts: {},
        },
        {
          id:3008,
          role:-1,
          sources: [43, 44, 45, 46, 60, 61, 62, 63],
          counts: {},
        },
        {
          id:3009,
          role:-1,
          sources: [44, 45, 46, 60, 61, 62, 63, 77],
          counts: {},
        },
        {id:3010, role:1},
        {id:3011, role:1},
        {id:3012, role:1}
      ],
      125: [{id:45, role:0}, {id:46, role:0}, {id:60, role:0}, {id:61, role:0}, {id:62, role:0}, {id:63, role:0}, {id:77, role:1}, {id:78, role:1}, {id:79, role:1}, {id:80, role:1}],
      126: [{id:48, role:0}, {id:66, role:0}],
      127: [{id:66, role:0}],
    }
    return {
      // reactive properties
      debug: false,
      ready: false,
      sending: false,
      saving: false,
      reopening: false,
      firstguessing: false,
      state: store.state,
      allerta: {
        numero_bollettino: "aaaaaaaa",
        w23data_set: []
      },
      vigilanza: null,
      psa: null,
      pericoli: [],
      effetti: [],
      time_layouts: {},
      soglie_nivo_area_prev: [],
      soglie_pluv_area_prev_massimi: [],
      soglie_pluv_area_prev_medie: [],
      risk_val_oggi: null,
      risk_val_domani: null,
      pluvossh6: {},
      colore_risk_storm_oggi: {},
      colore_risk_storm_domani: {},
      availability: {},
      pluv: null,
      piogge_medie: {},
      piogge_massime: {},
      tls_lookup: {},
      risk_storm_oggi: {},
      risk_storm_domani: {},
      neve: {},
      labels: {},
    }
  },
  computed: {
    avverse() {
      let vd = { }
      // vero se c'è un fenomeno giallo o superiore in una qualsiasi cella di "bollettino emesso" anche in bozza
      let max = 2
      Object.keys(this.pericolo_massimo).forEach(id => max = Math.max(max, this.pericolo_massimo[id].sort_index))
      vd["pericolo_massimo"] = max
      // vero se c'è un fenomeno giallo o superiore in una qualsiasi cella del fenomeno idraulico di "bollettino emesso" anche in bozza
      let max_idraulico = 2
      Object.keys(this.pericolo_massimo_idraulico).forEach(id => max_idraulico = Math.max(max_idraulico, this.pericolo_massimo_idraulico[id].sort_index))
      vd["max_idraulico"] = max_idraulico
      //console.log('vd',vd)
      return vd
    },
    today() {
      // returns today in 2021-04-22 format
      let d = new Date()
      return d.toISOString().substring(0, 10)
    },
    pericolo_massimo () {
      let vd = { }
      this.allerta.w23data_set.forEach(area => {
        vd[area.id_w23_zone.id_w23_zone] = this.massimo(area.id_w23_zone.id_w23_zone, this.lista_parametri_oggi_domani)
      })
      return vd
    },
    pericolo_massimo_idraulico () {
      let vd = { }
      this.allerta.w23data_set.forEach(area => {
        vd[area.id_w23_zone.id_w23_zone] = this.massimo(area.id_w23_zone.id_w23_zone, this.lista_parametri_oggi_domani_idraulico)
      })
      return vd
    },
    pericolo_massimo_oggi () {
      let vd = { }
      this.allerta.w23data_set.forEach(area => {
        vd[area.id_w23_zone.id_w23_zone] = this.massimo(area.id_w23_zone.id_w23_zone, this.lista_parametri_oggi)
      })
      return vd
    },
    pericolo_massimo_domani () {
      let vd = { }
      this.allerta.w23data_set.forEach(area => {
        vd[area.id_w23_zone.id_w23_zone] = this.massimo(area.id_w23_zone.id_w23_zone, this.lista_parametri_domani)
      })
      return vd
    },
    pericolo_massimo_for () {
      let vd = { }
      this.allerta.w23data_set.forEach(area => {
        vd[area.id_w23_zone.id_w23_zone] = this.massimo_for(area, this.lista_parametri_oggi_domani_for)
      })
      return vd
    },
    pericolo_massimo_oggi_for () {
      let vd = { }
      this.allerta.w23data_set.forEach(area => {
        vd[area.id_w23_zone.id_w23_zone] = this.massimo_for(area, this.lista_parametri_oggi_for)
      })
      return vd
    },
    pericolo_massimo_domani_for () {
      let vd = { }
      this.allerta.w23data_set.forEach(area => {
        vd[area.id_w23_zone.id_w23_zone] = this.massimo_for(area, this.lista_parametri_domani_for)
      })
      return vd
    },
    pericolo_da_id () {
      let cp = { }
      this.pericoli.forEach(pericolo => {
        cp[pericolo.id_w23_pericolo] = pericolo
      })
      return cp
    },
    pericolo_da_indice () {
      let cp = { }
      this.pericoli.forEach(pericolo => {
        cp[pericolo.sort_index] = pericolo
      })
      return cp
    },
    area_pericolo () {
      let cs = { }
      this.allerta.w23data_set.forEach(area => {
        this.lista_parametri_oggi_domani.forEach(parametro => {
          if (!(parametro in cs)) {
            cs[parametro] = { }
          }
          cs[parametro][area.id_w23_zone.id_w23_zone] = this.pericolo_da_id[area[parametro].id_w23_pericolo]
        })
      })
      return cs
    },
    oggi () {
      return api.getDateFormatted(this.allerta.data_emissione, false)
    },
    domani () {
      return api.getDateFormatted(this.allerta.data_emissione, false, 1)
    },
  },
  watch: {
    avverse(new_value, old_value) {
      const frase = 'AVVISO DI CONDIZIONI METEOROLOGICHE AVVERSE per i dettagli consultare il bollettino di Vigilanza Meteorologica. '
      const frase_idraulico = 'Consultare il Bollettino di previsione delle Piene.'
      // console.log(`avverse = ${value}, allerta.situazione_meteo = ${this.allerta.situazione_meteo}`)
      // console.log('this.allerta', this.allerta, 'new_value',new_value, 'old_value',old_value)
      if (this.allerta && this.allerta.status === '0' && this.state.username) {
        if (this.allerta.situazione_meteo.includes(frase)) {
          if (new_value["pericolo_massimo"]<=2) {
            this.allerta.situazione_meteo = this.allerta.situazione_meteo.replace(frase, '')
          }
        } else {
          if (new_value["pericolo_massimo"]>2) {
            if (!(this.allerta.situazione_meteo.includes("il bollettino di Vigilanza"))) { 
              this.allerta.situazione_meteo += frase
            }
          }
        }
        if (this.allerta.situazione_meteo.includes(frase_idraulico)) {
          if (new_value["max_idraulico"]<=2) {
            this.allerta.situazione_meteo = this.allerta.situazione_meteo.replace(frase_idraulico, '')
          }
        } else {
          if (new_value["max_idraulico"]>2) {
            this.allerta.situazione_meteo += frase_idraulico
          }
        }
        this.saveField('situazione_meteo')
      }
    }
  },
  created() {
    this.getAllerta()
  },
  methods: {
    fill_labels() {
      const tls = [45, 46, 48, 49, 60, 61, 62, 63, 64, 65, 66, 77, 78, 79, 80, 81, 82, 83, 1009, 1011, 1013, 1015, 1017, 2006, 2009, 2010, 2011, 2014, 2015, 2016, 3003, 3004, 3005, 3006, 3007, 3008, 3009, 3010, 3011, 3012]
      let map = {}
      tls.forEach(tl => {
        const tlo = this.time_layouts[tl]
        if (tlo) {
          map[tl] = [
            this.getOffsetDateFormatted(this.allerta.data_emissione, tlo.start_day_offset, tlo.start_time),
            this.getOffsetDateFormatted(this.allerta.data_emissione, tlo.end_day_offset, tlo.end_time),
          ]
        } else {
          map[tl] = ["", ""]
        }
      })
      this.labels = map
    },
    fill_neve() {
      let ad = {
        SNOW_LEV: {
          45: {},
          46: {},
          60: {},
          61: {},
          62: {},
          63: {},
        },
        SNOW_LEV_MIN: {
          1009: {}, // min(45, 46, 60, 61, 62, 63)
        },
        SNOW_LEV_MAX: {
          1009: {}, // max(45, 46, 60, 61, 62, 63)
        },
        SNOW_400: {
          1009: {}, // 48 + 66
          48: {},
          66: {},
        },
        SNOW_700: {
          1009: {}, // 48 + 66
          48: {},
          66: {},
        },
        SNOW_1000: {
          1009: {}, // 48 + 66
          48: {},
          66: {},
        },
      }
      if (this.availability.vigilanza) {
        this.vigilanza.w24data_set.forEach(record => {
          if (record.id_parametro in ad) {
            if (record.id_time_layouts in ad[record.id_parametro]) {
                ad[record.id_parametro][record.id_time_layouts][record.id_allertamento] = parseFloat(record.numeric_value)
            }
          }
        })
        const clip = (value) => {
            return value < 9990 && value > 0 ? value : null
        }
        this.righe.forEach(area => {
          ad.SNOW_400[1009][area] = ad.SNOW_400[48][area] + ad.SNOW_400[66][area]
          ad.SNOW_700[1009][area] = ad.SNOW_700[48][area] + ad.SNOW_700[66][area]
          ad.SNOW_1000[1009][area] = ad.SNOW_1000[48][area] + ad.SNOW_1000[66][area]
          const levels = [
            ad.SNOW_LEV[45][area],
            ad.SNOW_LEV[46][area],
            ad.SNOW_LEV[60][area],
            ad.SNOW_LEV[61][area],
            ad.SNOW_LEV[62][area],
            ad.SNOW_LEV[63][area],
          ]
          ad.SNOW_LEV_MIN[1009][area] = clip(this.arrayMin(levels.filter(v => v > 100)))
          ad.SNOW_LEV_MAX[1009][area] = clip(this.arrayMax(levels.filter(v => v < 9990)))
        })
      }
      this.neve = ad
    },
    get_risk_storm(tl) {
      let rs = {}
      if (this.availability && this.availability.vigilanza) {
        this.vigilanza.w24data_set.forEach(record => {
          if (record.id_parametro === 'RISK_STORM' && record.id_time_layouts === tl) {
            rs[record.id_allertamento] = parseInt(record.numeric_value)
          }
        })
      }
      return rs
    },
    fill_risk_storm() {
      this.risk_storm_oggi = this.get_risk_storm(48)
      this.risk_storm_domani = this.get_risk_storm(66)
    },
    fill_tls_lookup() {
      let tls_lookup = {}
      Object.values(this.time_layouts).forEach(tl => {
        const start_time = new Date("1970-01-01T" + tl.start_time + "Z")
        const start_minutes = Math.round(tl.start_day_offset * 24 * 60 +  start_time.getTime() / 1000.0 / 60.0)
        const end_time = new Date("1970-01-01T" + tl.end_time + "Z")
        const end_minutes = Math.round(tl.end_day_offset * 24 * 60 +  end_time.getTime() / 1000.0 / 60.0)
        if (end_minutes - start_minutes == 360) {
          tls_lookup[end_minutes] = tl
        }
      })
      this.tls_lookup = tls_lookup
    },
    fill_piogge_massime() {
      let piogge_massime = {125: {}, 126: {}, 127: {}}
      let time_layouts = Object.fromEntries(Object.keys(this.tls).map(tl => [tl, this.tls[tl].map(tl => tl.id)]))
      Object.keys(piogge_massime).forEach(id_aggregazione => {
        time_layouts[id_aggregazione].forEach(id_time_layouts => {
          piogge_massime[id_aggregazione][id_time_layouts] = {}
        })
      })
      if (Object.keys(this.tls).length > 0) {
        if ((this.allerta.status !== '0' && this.allerta.status !== status_first_time) || this.allerta.data_emissione !== this.today) {
          // cerca le piogge massime sul w23_data
          // console.log("fill_piogge_massime: ((this.allerta.status !== '0' && this.allerta.status !== status_first_time) || this.allerta.data_emissione !== this.today)")
          this.allerta.w23data_set.forEach(zona => {
            const area = zona.id_w23_zone.nome_zona

            piogge_massime[125][45][area] = zona.pluvmax6h18g0
            piogge_massime[125][46][area] = zona.pluvmax6h00g1
            piogge_massime[125][60][area] = zona.pluvmax6h06g1
            piogge_massime[125][61][area] = zona.pluvmax6h12g1
            piogge_massime[125][62][area] = zona.pluvmax6h18g1
            piogge_massime[125][63][area] = zona.pluvmax6h00g2
            piogge_massime[125][77][area] = zona.pluvmax6h06g2
            piogge_massime[125][78][area] = zona.pluvmax6h12g2
            piogge_massime[125][79][area] = zona.pluvmax6h18g2
            piogge_massime[125][80][area] = zona.pluvmax6h00g3

            piogge_massime[126][48][area] = zona.pluvmax12hd0
            piogge_massime[126][66][area] = zona.pluvmax12hd1

            piogge_massime[127][66][area] = zona.pluvmax24hd1
          })
        }else{
          if (this.pluv) {
            // console.log("fill_piogge_massime: this.pluv ok")
            let id_parametro = this.rearrange(this.psa.w30data_set, "id_parametro")
            let pluv = this.rearrange(id_parametro["PLUV"], "id_time_layouts");
            let time_layouts = {
              125: [45, 46, 60, 61, 62, 63, 77, 78, 79, 80],
              126: [48, 66],
              127: [66]
            };
            Object.keys(piogge_massime).forEach(id_aggregazione => {
              // console.log('========== id_aggregazione =', id_aggregazione)
              time_layouts[id_aggregazione].forEach(id_time_layouts => {
                // console.log(`looking at id_time_layouts = ${id_time_layouts}`)
                if (id_time_layouts in pluv) {
                  // console.log(`PLUV[${id_time_layouts}] = ${JSON.stringify(pluv[id_time_layouts])}`)
                  let value_data = this.rearrange(pluv[id_time_layouts], "id_aggregazione")
                  // console.log(`value_data = ${JSON.stringify(value_data)}`)
                  if (id_aggregazione in value_data) {
                    let aaa = this.rearrange(value_data[id_aggregazione], "id_allertamento")
                    // console.log(`aaa = ${JSON.stringify(aaa)}`)
                    let bbb = Object.entries(aaa).map(item => [item[0], item[1][0].numeric_value])
                    // console.log(`bbb = ${JSON.stringify(bbb)}`)
                    piogge_massime[id_aggregazione][id_time_layouts] = Object.fromEntries(bbb)
                  } else {
                    // console.log(`${id_aggregazione} not found in PLUV[${id_time_layouts}]`)
                    piogge_massime[id_aggregazione][id_time_layouts] = {}
                  }
                } else {
                  // console.log(`${id_time_layouts} not found in PLUV`)
                  piogge_massime[id_aggregazione][id_time_layouts] = {}
                }
              })
            })
          }
        }
      }
      this.piogge_massime = piogge_massime
    },
    fill_pluv() {
      if (this.availability.psa) {
        let id_parametro = this.rearrange(this.psa.w30data_set, "id_parametro")
        this.pluv = this.rearrange(
          id_parametro["PLUV"],
          "id_time_layouts",
          data => this.rearrange(
            data,
            "id_aggregazione",
            data1 => this.rearrange(
              data1,
              "id_allertamento",
              arr => arr[0].numeric_value
            )
          )
        )
      }
    },
    fill_piogge_medie() {
      let piogge_medie = {900: {}, 901: {}, 902: {}, 903: {}};
      let time_layouts = Object.fromEntries(Object.keys(this.tls).map(tl => [tl, this.tls[tl].map(tl => tl.id)]))
      Object.keys(piogge_medie).forEach(id_aggregazione => {
        time_layouts[id_aggregazione].forEach(id_time_layouts => {
          piogge_medie[id_aggregazione][id_time_layouts] = {}
        })
      })
      if (Object.keys(this.tls).length > 0) {
        if ((this.allerta.status !== '0' && this.allerta.status !== status_first_time) || this.allerta.data_emissione !== this.today) {
          // console.log('========== status 1')
          // retrieve mixed observation/forecasts from pluvmed{12,24,48}h{00,06,12,18}g{0,1,2}_oss
          this.allerta.w23data_set.forEach(zona => {
            const area = zona.id_w23_zone.nome_zona

            piogge_medie[901][1009][area] = zona.pluvmed12h18g0_oss

            piogge_medie[902][2006][area] = zona.pluvmed24h18g0_oss
            piogge_medie[902][49][area] = zona.pluvmed24h00g1_oss
            piogge_medie[902][2009][area] = zona.pluvmed24h06g1_oss

            piogge_medie[903][3003][area] = zona.pluvmed48h18g0_oss
            piogge_medie[903][3004][area] = zona.pluvmed48h00g1_oss
            piogge_medie[903][3005][area] = zona.pluvmed48h06g1_oss
            piogge_medie[903][3006][area] = zona.pluvmed48h12g1_oss
            piogge_medie[903][3007][area] = zona.pluvmed48h18g1_oss
            piogge_medie[903][3008][area] = zona.pluvmed48h00g2_oss
            piogge_medie[903][3009][area] = zona.pluvmed48h06g2_oss

            piogge_medie[900][45][area] = zona.pluvmed6h18g0
            piogge_medie[900][46][area] = zona.pluvmed6h00g1
            piogge_medie[900][60][area] = zona.pluvmed6h06g1
            piogge_medie[900][61][area] = zona.pluvmed6h12g1
            piogge_medie[900][62][area] = zona.pluvmed6h18g1
            piogge_medie[900][63][area] = zona.pluvmed6h00g2
            piogge_medie[900][77][area] = zona.pluvmed6h06g2
            piogge_medie[900][78][area] = zona.pluvmed6h12g2
            piogge_medie[900][79][area] = zona.pluvmed6h18g2
            piogge_medie[900][80][area] = zona.pluvmed6h00g3

            piogge_medie[901][48][area] = zona.pluvmed12h00g1
            piogge_medie[901][1011][area] = zona.pluvmed12h06g1
            piogge_medie[901][64][area] = zona.pluvmed12h12g1
            piogge_medie[901][1013][area] = zona.pluvmed12h18g1
            piogge_medie[901][65][area] = zona.pluvmed12h00g2
            piogge_medie[901][1015][area] = zona.pluvmed12h06g2
            piogge_medie[901][81][area] = zona.pluvmed12h12g2
            piogge_medie[901][1017][area] = zona.pluvmed12h18g2
            piogge_medie[901][82][area] = zona.pluvmed12h00g3

            piogge_medie[902][2010][area] = zona.pluvmed24h12g1
            piogge_medie[902][2011][area] = zona.pluvmed24h18g1
            piogge_medie[902][66][area] = zona.pluvmed24h00g2
            piogge_medie[902][2014][area] = zona.pluvmed24h06g2
            piogge_medie[902][2015][area] = zona.pluvmed24h12g2
            piogge_medie[902][2016][area] = zona.pluvmed24h18g2
            piogge_medie[902][83][area] = zona.pluvmed24h00g3

            piogge_medie[903][3010][area] = zona.pluvmed48h12g2
            piogge_medie[903][3011][area] = zona.pluvmed48h18g2
            piogge_medie[903][3012][area] = zona.pluvmed48h00g3
          })
        } else {
          if (this.pluv) {
            // console.log('========== compute forecasts from pluv', piogge_medie)
            Object.keys(piogge_medie).forEach(id_aggregazione => {
              time_layouts[id_aggregazione].forEach(id_time_layouts => {
                if (id_time_layouts in this.pluv) {
                  let value_data = this.pluv[id_time_layouts]
                  if (id_aggregazione in value_data) {
                    piogge_medie[id_aggregazione][id_time_layouts] = {...value_data[id_aggregazione]}
                  }
                } else {
                  //console.log(`tls[${id_aggregazione}] = ${JSON.stringify(this.tls[id_aggregazione])}`)
                  let agg = this.tls[id_aggregazione].find(item => item.id == id_time_layouts)
                  // console.log('agg.sources',agg.sources,agg)
                  if (agg && agg.sources) {
                    // console.log("chiamo add")
                    piogge_medie[id_aggregazione][id_time_layouts] = Object.fromEntries(this.righe.map(k => [k, 0]))
                    piogge_medie[id_aggregazione][id_time_layouts]["Piem-V"] = 0
                    agg.counts = this.add(piogge_medie[id_aggregazione][id_time_layouts], agg.sources)
                  }
                }
              })
              // console.log(`piogge_medie[${id_aggregazione}] = ${JSON.stringify(piogge_medie[id_aggregazione])}`)
            })
          }
          // console.log('this.availability.pluvoss ',this.availability.pluvoss)
          if (this.availability.pluvoss) {
            //console.log('========== compute mixed observation/forecasts from pluvossh6')
            Object.keys(this.tls).forEach(key => {
              //console.log('  tls =', key)
              this.tls[key].forEach(agg => {
                //console.log('    agg =', agg.id)
                if (agg.sources) {
                  piogge_medie[key][agg.id] = Object.fromEntries(Object.keys(this.pluvossh6).map(k => [k, 0]))
                  agg.counts = this.add(piogge_medie[key][agg.id], agg.sources)
                  if (agg.counts.observations + agg.counts.forecasts === 0) {
                    piogge_medie[key][agg.id] = {}
                  }
                  //console.log(`piogge_medie[${key}][${agg.id}]: adding ${agg.counts.observations}% observations from [${agg.sources}] and ${agg.counts.forecasts}% forecasts`)
                }
              })
            })
          }
        }
      }
      this.piogge_medie = piogge_medie
    },
    fill_colore_risk_storm_oggi() {
      let rso = {
        "VdAo-A": {rischio_temporali: 'ASSENTE', colore_html: '#6EBB00'}
      }
      if (this.availability.vigilanza) {
        this.vigilanza.w24data_set.forEach(record => {
         if (record.id_parametro === 'RISK_STORM' && record.id_time_layouts === 48) {
            let data = {}
            if(parseInt(record.numeric_value)==0){
              data['rischio_temporali'] = 'ASSENTE'
              data['colore_html'] = '#6EBB00'
            }else if(parseInt(record.numeric_value)==1){
              data['rischio_temporali'] = 'ROVESCI'
              data['colore_html'] = '#6EBB00'
            }else if(parseInt(record.numeric_value)==2){
              data['rischio_temporali'] = 'TEMPORALI'
              data['colore_html'] = '#6EBB00'
            }else if(parseInt(record.numeric_value)==3){
              data['rischio_temporali'] = 'TEMPORALI FORTI'
              data['colore_html'] = '#FFFF00'
            }else if(parseInt(record.numeric_value)==4){
              data['rischio_temporali'] = 'TEMPORALI FORTI PERSISTENTI'
              data['colore_html'] = '#FFA500'
            }
            //rso[record.id_allertamento] = parseInt(record.numeric_value)
            rso[record.id_allertamento] = data
          }
        })
      }else{
        this.allerta.w23data_set.forEach(area => {
          let data = {}
          data['rischio_temporali'] = 'ASSENTE'
          data['colore_html'] = '#6EBB00'
          rso[area.id_w23_zone.nome_zona] = data
        })
      }
      this.colore_risk_storm_oggi = rso
    },
    fill_colore_risk_storm_domani() {
      let rsd = {
        "VdAo-A": {rischio_temporali: 'ASSENTE', colore_html: '#6EBB00'}
      }

      if (this.availability.vigilanza) {
        this.vigilanza.w24data_set.forEach(record => {
          if (record.id_parametro === 'RISK_STORM' && record.id_time_layouts === 66) {
            let data = {}
            if(parseInt(record.numeric_value)==0){
              data['rischio_temporali'] = 'ASSENTE'
              data['colore_html'] = '#6EBB00'
            }else if(parseInt(record.numeric_value)==1){
              data['rischio_temporali'] = 'ROVESCI'
              data['colore_html'] = '#6EBB00'
            }else if(parseInt(record.numeric_value)==2){
              data['rischio_temporali'] = 'TEMPORALI'
              data['colore_html'] = '#6EBB00'
            }else if(parseInt(record.numeric_value)==3){
              data['rischio_temporali'] = 'TEMPORALI FORTI'
              data['colore_html'] = '#FFFF00'
            }else if(parseInt(record.numeric_value)==4){
              data['rischio_temporali'] = 'TEMPORALI FORTI PERSISTENTI'
              data['colore_html'] = '#FFA500'
            }
            rsd[record.id_allertamento] = data
          }
        })
      }else{
        this.allerta.w23data_set.forEach(area => {
          let data = {}
          data['rischio_temporali'] = 'ASSENTE'
          data['colore_html'] = '#6EBB00'
          rsd[area.id_w23_zone.nome_zona] = data
        })
      }
      this.colore_risk_storm_domani = rsd
    },
    getAllerta() {
      this.allerta_id = this.id
      if (typeof this.allerta_id === 'undefined') {
        return
      }
      this.fetchData()
    },
    saveField(field) {
      // console.log("saveField")
      this.saving = true
      let stack = []
      const payload = {"id_key":"id_w23","id":this.allerta.id_w23,"value_key":field,"new_value": this.allerta[field]}
      const payloadusername = {"id_key":"id_w23","id":this.allerta.id_w23,"value_key":"username","new_value": store.state.username}
      stack.push(payloadusername)
      stack.push(payload)
      this.saveW23(stack)
    },
    saveData(value, id_w23_zone, field) {
      let myW23zone = this.allerta.w23data_set.find(w23data => {
        return w23data.id_w23_zone.id_w23_zone === id_w23_zone
      })
      let stack = []
      const payload = {"id_key":"id_w23_data","id":myW23zone.id_w23_data,"value_key":field,"new_value": value}
      const payloadusername = {"id_key":"id_w23","id":this.allerta.id_w23,"value_key":"username","new_value": store.state.username}
      stack.push(payloadusername)
      stack.push(payload)
      this.saveW23(stack)
    },
    saveDataPericolo(value, id_w23_zone, field) {
      let myW23zone = this.allerta.w23data_set.find(w23data => {
        return w23data.id_w23_zone.id_w23_zone === id_w23_zone
      })
      let stack = []
      const payload = {"id_key":"id_w23_data","id":myW23zone.id_w23_data,"value_key":field,"new_value": value}
      const payloadusername = {"id_key":"id_w23","id":this.allerta.id_w23,"value_key":"username","new_value": store.state.username}
      stack.push(payloadusername)
      stack.push(payload)
      this.saveW23(stack, () => {
        this.setPericolo(myW23zone, field, this.pericolo_da_id[value])
      })
    },
    arrayMin(arr) {
      return Math.min.apply(Math, arr)
    },
    arrayMax(arr) {
      return Math.max.apply(Math, arr)
    },
    execute_timeout(action, reroute, message){
      // console.log("inizio execute_timeout")
      if (this.saving){
        console.log("saving è true faccio partire timeout")
        setTimeout(() => {
          console.log("aspetto 1 secondo finchè non finisce il salvataggio in corso")
          this.execute_timeout(action, reroute, message)
        }, 1000);
      }else{
        console.log("saving è false lancio execute")
        this.execute(action, reroute, message)
      }
      // console.log("fine execute_timeout")
    },
    execute(action, reroute, message) {
      if (action === 'firstguess') {
        if (!confirm("Vuoi davvero aggiornare la first guess? I dati nel tab 'Base Bollettino' verranno sovrascritti!")) {
          return
        } else {
          this.fetchData(this.firstguess)
        }
      } else {
        if ((action === 'send') && 
          (!this.availability.vigilanza) && 
          !confirm("Vuoi davvero finalizzare? Manca vigilanza"))  
        {
          return
        }else if((action === 'send') && 
          (!this.availability.risk_val_oggi || !this.availability.risk_val_domani) && 
          !confirm("Vuoi davvero finalizzare? Mancano le valanghe"))
        {
          return
        }
        this.really_execute(action, reroute, message)
      }
    },
    rischio_neve(parametro, time_layout, area) {
      // parametro = SNOW_400, SNOW_700, SNOW_1000
      // time_layout = 48, 1009
      // area = Piem-A, Piem-B, ...
      // return value: 1, 2, 3, 4 or 5
      const ambito = {
        SNOW_400: "pianura",
        SNOW_700: "collina",
        SNOW_1000: "montagna ",
      }
      const factor = 1.0  // time_layout === 1009 ? 1.5 : 1.0
      const value = this.neve[parametro][time_layout][area]
      const soglia = this.soglie_nivo_area_prev[ambito[parametro]][area]
      if (soglia) {
        // console.log(`soglie_nivo_area_prev[${ambito[parametro]}][${area}] = ${soglia}`)
        // console.log(`rischio_neve(${value} ${JSON.stringify(soglia)}`)
        if (value >= soglia.soglia_cod3 * factor) {
          return 5
        } else if (value >= soglia.soglia_cod2 * factor) {
          return 4
        } else if (value >= soglia.soglia_cod1 * factor) {
          return 3
        } else {
          return 2
        }
      } else {
        return 1
      }
    },
    rischio_pioggia_max(aggregazione, time_layout, area) {
      // aggregazione = 125, 126, 127
      // time_layout = 45, 46 ...
      // area = Piem-A, Piem-B, ...
      // return value: 1, 2, 3, 4 or 5
      const h = {
        125: 'h6',
        126: 'h12',
        127: 'h24'
      }
      const factor = 1 // set this to 200 to see some colors when there is little or no precipitations
      let value = 0
      if (aggregazione in this.piogge_massime && time_layout in this.piogge_massime[aggregazione]) {
        value = this.piogge_massime[aggregazione][time_layout][area]
      }
      const soglia = this.soglie_pluv_area_prev_massimi[h[aggregazione]][area]
      if (soglia) {
        // console.log(`soglie_pluv_area_prev_massimi[${h[aggregazione]}][${area}] = ${soglia}`)
        if (value >= soglia[3] / factor) {
          return 5
        } else if (value >= soglia[2] / factor) {
          return 4
        } else if (value >= soglia[1] / factor) {
          return 3
        } else {
          return 2
        }
      } else {
        return 1
      }
    },
    rischio_pioggia_avg(aggregazione, time_layout, area) {
      // aggregazione = 900, 901, 902, 903
      // time_layout = 45, 46 ...
      // area = Piem-A, Piem-B, ...
      // return value: 1, 2, 3, 4 or 5
      const h = {
        900: 'h6',
        901: 'h12',
        902: 'h24',
        903: 'h48'
      }
      const factor = 1 // set this to 200 to see some colors when there is little or no precipitations
      let value = "ND"
      if (this.piogge_medie[aggregazione][time_layout] !== undefined){
         value = this.piogge_medie[aggregazione][time_layout][area]
      }
      const soglia = this.soglie_pluv_area_prev_medie[h[aggregazione]][area]
      if (soglia) {
        // console.log(`soglie_pluv_area_prev_medie[${h[aggregazione]}][${area}] = ${soglia}`)
        if (value >= soglia[2] / factor) {
          return 5
        } else if (value >= soglia[1] / factor) {
          return 4
        } else if (value >= soglia[0] / factor) {
          return 3
        } else {
          return 2
        }
      } else {
        return 1
      }
    },
    rischio_temporali(rs) {
      // return value: 1, 2, 3 or 4
      return {
        0: 2, // ASSENTI = verde
        1: 2, // ROVESCI = verde
        2: 2, // TEMPORALI = verde
        3: 3, // TEMPORALI FORTI => giallo
        4: 4  // TEMPORALI FORTI E PERSISTENTI = arancione
      }[rs]
    },
    rischio_valanghe(rv) {
      // return value: 1, 2, 3, 4 or 5
      // 0/assente, 1-4 -> bianco/verde/giallo/arancione/rosso
      return rv + 1
    },
    min2(arr) {
      // find the minimum risk level greater than 2 that occurs in at least 2 elements
      // of the supplied array, or else return 2
      if (arr.filter(i => i === 5).length >= 2) {
        return 5
      } else if (arr.filter(i => i >= 4).length >= 2) {
        return 4
      }if (arr.filter(i => i >= 3).length >= 2) {
        return 3
      } else {
        return 2
      }
    },
    firstguess(copy_over = false) {
      this['firstguessing'] = true
      let stack = []

      this.allerta.w23data_set.forEach(zona => {
        const area = zona.id_w23_zone.nome_zona
        // pluvoss   
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmed12h18g0_oss","new_value": this.availability.psa?this.piogge_medie[901][1009][area].toFixed(1): "ND"})

        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmed24h18g0_oss","new_value": this.availability.psa?this.piogge_medie[902][2006][area].toFixed(1): "ND"})
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmed24h00g1_oss","new_value": this.availability.psa?this.piogge_medie[902][49][area].toFixed(1): "ND"})
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmed24h06g1_oss","new_value": this.availability.psa?this.piogge_medie[902][2009][area].toFixed(1): "ND"})

        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmed48h18g0_oss","new_value": this.availability.psa?this.piogge_medie[903][3003][area].toFixed(1): "ND"})
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmed48h00g1_oss","new_value": this.availability.psa?this.piogge_medie[903][3004][area].toFixed(1): "ND"})
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmed48h06g1_oss","new_value": this.availability.psa?this.piogge_medie[903][3005][area].toFixed(1): "ND"})
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmed48h12g1_oss","new_value": this.availability.psa?this.piogge_medie[903][3006][area].toFixed(1): "ND"})
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmed48h18g1_oss","new_value": this.availability.psa?this.piogge_medie[903][3007][area].toFixed(1): "ND"})
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmed48h00g2_oss","new_value": this.availability.psa?this.piogge_medie[903][3008][area].toFixed(1): "ND"})
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmed48h06g2_oss","new_value": this.availability.psa?this.piogge_medie[903][3009][area].toFixed(1): "ND"})

        // piogge medie
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmed6h18g0","new_value": this.availability.psa?this.piogge_medie[900][45][area].toFixed(1): "ND"})
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmed6h00g1","new_value": this.availability.psa?this.piogge_medie[900][46][area].toFixed(1): "ND"})
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmed6h06g1","new_value": this.availability.psa?this.piogge_medie[900][60][area].toFixed(1): "ND"})
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmed6h12g1","new_value": this.availability.psa?this.piogge_medie[900][61][area].toFixed(1): "ND"})
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmed6h18g1","new_value": this.availability.psa?this.piogge_medie[900][62][area].toFixed(1): "ND"})
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmed6h00g2","new_value": this.availability.psa?this.piogge_medie[900][63][area].toFixed(1): "ND"})
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmed6h06g2","new_value": this.availability.psa?this.piogge_medie[900][77][area].toFixed(1): "ND"})
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmed6h12g2","new_value": this.availability.psa?this.piogge_medie[900][78][area].toFixed(1): "ND"})
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmed6h18g2","new_value": this.availability.psa?this.piogge_medie[900][79][area].toFixed(1): "ND"})
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmed6h00g3","new_value": this.availability.psa?this.piogge_medie[900][80][area].toFixed(1): "ND"})
            
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmed12h00g1","new_value": this.availability.psa?this.piogge_medie[901][48][area].toFixed(1): "ND"})
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmed12h06g1","new_value": this.availability.psa?this.piogge_medie[901][1011][area].toFixed(1): "ND"})
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmed12h12g1","new_value": this.availability.psa?this.piogge_medie[901][64][area].toFixed(1): "ND"})
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmed12h18g1","new_value": this.availability.psa?this.piogge_medie[901][1013][area].toFixed(1): "ND"})
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmed12h00g2","new_value": this.availability.psa?this.piogge_medie[901][65][area].toFixed(1): "ND"})
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmed12h06g2","new_value": this.availability.psa?this.piogge_medie[901][1015][area].toFixed(1): "ND"})
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmed12h12g2","new_value": this.availability.psa?this.piogge_medie[901][81][area].toFixed(1): "ND"})
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmed12h18g2","new_value": this.availability.psa?this.piogge_medie[901][1017][area].toFixed(1): "ND"})
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmed12h00g3","new_value": this.availability.psa?this.piogge_medie[901][82][area].toFixed(1): "ND"})

        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmed24h12g1","new_value": this.availability.psa?this.piogge_medie[902][2010][area].toFixed(1): "ND"})
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmed24h18g1","new_value": this.availability.psa?this.piogge_medie[902][2011][area].toFixed(1): "ND"})
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmed24h00g2","new_value": this.availability.psa?this.piogge_medie[902][66][area].toFixed(1): "ND"})
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmed24h06g2","new_value": this.availability.psa?this.piogge_medie[902][2014][area].toFixed(1): "ND"})
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmed24h12g2","new_value": this.availability.psa?this.piogge_medie[902][2015][area].toFixed(1): "ND"})
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmed24h18g2","new_value": this.availability.psa?this.piogge_medie[902][2016][area].toFixed(1): "ND"})
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmed24h00g3","new_value": this.availability.psa?this.piogge_medie[902][83][area].toFixed(1): "ND"})

        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmed48h12g2","new_value": this.availability.psa?this.piogge_medie[903][3010][area].toFixed(1): "ND"})
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmed48h18g2","new_value": this.availability.psa?this.piogge_medie[903][3011][area].toFixed(1): "ND"})
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmed48h00g3","new_value": this.availability.psa?this.piogge_medie[903][3012][area].toFixed(1): "ND"})

        // piogge massime
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmax6h18g0","new_value": this.availability.psa?this.piogge_massime[125][45][area].toFixed(1): "ND"})
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmax6h00g1","new_value": this.availability.psa?this.piogge_massime[125][46][area].toFixed(1): "ND"})
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmax6h06g1","new_value": this.availability.psa?this.piogge_massime[125][60][area].toFixed(1): "ND"})
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmax6h12g1","new_value": this.availability.psa?this.piogge_massime[125][61][area].toFixed(1): "ND"})
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmax6h18g1","new_value": this.availability.psa?this.piogge_massime[125][62][area].toFixed(1): "ND"})
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmax6h00g2","new_value": this.availability.psa?this.piogge_massime[125][63][area].toFixed(1): "ND"})
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmax6h06g2","new_value": this.availability.psa?this.piogge_massime[125][77][area].toFixed(1): "ND"})
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmax6h12g2","new_value": this.availability.psa?this.piogge_massime[125][78][area].toFixed(1): "ND"})
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmax6h18g2","new_value": this.availability.psa?this.piogge_massime[125][79][area].toFixed(1): "ND"})
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmax6h00g3","new_value": this.availability.psa?this.piogge_massime[125][80][area].toFixed(1): "ND"})
        
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmax12hd0","new_value": this.availability.psa?this.piogge_massime[126][48][area].toFixed(1): "ND"})
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmax12hd1","new_value": this.availability.psa?this.piogge_massime[126][66][area].toFixed(1): "ND"})
        
        stack.push({"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":"pluvmax24hd1","new_value": this.availability.psa?this.piogge_massime[127][66][area].toFixed(1): "ND"})

        // neve
        zona.neve400_oggi = this.rischio_neve('SNOW_400', 48, area)
        zona.neve700_oggi = this.rischio_neve('SNOW_700', 48, area)
        zona.neve1000_oggi = this.rischio_neve('SNOW_1000', 48, area)
        const neve_oggi = Math.max(zona.neve400_oggi, zona.neve700_oggi, zona.neve1000_oggi)
        stack = stack.concat(this.setFirstGuess(zona, 'neve_oggi', neve_oggi, copy_over))
        zona.neve400_domani = this.rischio_neve('SNOW_400', 1009, area)
        zona.neve700_domani = this.rischio_neve('SNOW_700', 1009, area)
        zona.neve1000_domani = this.rischio_neve('SNOW_1000', 1009, area)
        const neve_domani = Math.max(zona.neve400_domani, zona.neve700_domani, zona.neve1000_domani)
        stack = stack.concat(this.setFirstGuess(zona, 'neve_domani', neve_domani, copy_over))

        // idrogeologico
        // Per avere un colore diverso dal verde sul fenomeno Idrogeologico
        // è necessario avere due superamenti di durate diverse sulle piogge massime
        const superamenti_soglie_pioggia_max_oggi = [
          Math.max(
            this.rischio_pioggia_max(125, 45, area),
            this.rischio_pioggia_max(125, 46, area)
          ),
          this.rischio_pioggia_max(126, 48, area),
          this.rischio_pioggia_max(127, 66, area),
        ]
        const idrogeologico_oggi = this.min2(superamenti_soglie_pioggia_max_oggi)
        stack = stack.concat(this.setFirstGuess(zona, 'idrogeologico_oggi', idrogeologico_oggi, copy_over))
        const superamenti_soglie_pioggia_max_domani = [
          Math.max(
            this.rischio_pioggia_max(125, 60, area),
            this.rischio_pioggia_max(125, 61, area),
            this.rischio_pioggia_max(125, 62, area),
            this.rischio_pioggia_max(125, 63, area)
          ),
          this.rischio_pioggia_max(126, 66, area),
          this.rischio_pioggia_max(127, 66, area),
        ]
        const idrogeologico_domani = this.min2(superamenti_soglie_pioggia_max_domani)
        stack = stack.concat(this.setFirstGuess(zona, 'idrogeologico_domani', idrogeologico_domani, copy_over))

        // idraulico
        // Per avere un colore diverso dal verde sul fenomeno Idraulico
        // è necessario avere due superamenti di durate diverse sulle piogge medie
        const superamenti_soglie_pioggia_avg_oggi = [
          Math.max(
            this.rischio_pioggia_avg(900, 45, area),
            this.rischio_pioggia_avg(900, 46, area)
          ), // 6h
          Math.max(
            this.rischio_pioggia_avg(901, 1009, area),
            this.rischio_pioggia_avg(901, 48, area),
            this.rischio_pioggia_avg(901, 1011, area)
          ), // 12h
          Math.max(
            this.rischio_pioggia_avg(902, 2006, area),
            this.rischio_pioggia_avg(902, 49, area),
            this.rischio_pioggia_avg(902, 2009, area),
            this.rischio_pioggia_avg(902, 2010, area),
            this.rischio_pioggia_avg(902, 2011, area)
          ), // 24h
          Math.max(
            this.rischio_pioggia_avg(903, 3003, area),
            this.rischio_pioggia_avg(903, 3004, area),
            this.rischio_pioggia_avg(903, 3005, area),
            this.rischio_pioggia_avg(903, 3006, area),
            this.rischio_pioggia_avg(903, 3007, area),
            this.rischio_pioggia_avg(903, 3008, area),
            this.rischio_pioggia_avg(903, 3009, area)
          ) // 48h
        ]
        const idraulico_oggi = this.min2(superamenti_soglie_pioggia_avg_oggi)
        stack = stack.concat(this.setFirstGuess(zona, 'idraulico_oggi', idraulico_oggi, copy_over))
        const superamenti_soglie_pioggia_avg_domani = [
          Math.max(
            this.rischio_pioggia_avg(900, 60, area),
            this.rischio_pioggia_avg(900, 61, area),
            this.rischio_pioggia_avg(900, 62, area),
            this.rischio_pioggia_avg(900, 63, area)
          ), // 6h
          Math.max(
            this.rischio_pioggia_avg(901, 1011, area),
            this.rischio_pioggia_avg(901, 64, area),
            this.rischio_pioggia_avg(901, 1013, area),
            this.rischio_pioggia_avg(901, 65, area)
          ), // 12h
          Math.max(
            this.rischio_pioggia_avg(902, 2009, area),
            this.rischio_pioggia_avg(902, 2010, area),
            this.rischio_pioggia_avg(902, 2011, area),
            this.rischio_pioggia_avg(902, 66, area)
          ), // 24h
          Math.max(
            this.rischio_pioggia_avg(903, 3005, area),
            this.rischio_pioggia_avg(903, 3006, area),
            this.rischio_pioggia_avg(903, 3007, area),
            this.rischio_pioggia_avg(903, 3008, area),
            this.rischio_pioggia_avg(903, 3009, area)
          ) // 48h
        ]
        const idraulico_domani = this.min2(superamenti_soglie_pioggia_avg_domani)
        stack = stack.concat(this.setFirstGuess(zona, 'idraulico_domani', idraulico_domani, copy_over))

        // temporali
        if (area in this.risk_storm_oggi) {
          let temporali_oggi = 2 // VERDE
          if (idrogeologico_oggi > 2) {
            temporali_oggi = this.rischio_temporali(this.risk_storm_oggi[area])
          }
          stack = stack.concat(this.setFirstGuess(zona, 'temporali_oggi', temporali_oggi, copy_over))
        }
        if (area in this.risk_storm_domani) {
          let temporali_domani = 2 // VERDE
          if (idrogeologico_domani > 2) {
            temporali_domani = this.rischio_temporali(this.risk_storm_domani[area])
          }
          // console.log(`temporali_domani = ${temporali_domani}`)
          stack = stack.concat(this.setFirstGuess(zona, 'temporali_domani', temporali_domani, copy_over))
        }

        // valanghe
        // console.log(`this.risk_val_oggi = ${JSON.stringify(this.risk_val_oggi)}`)
        if (area in this.risk_val_oggi) {
          // console.log(`looking at area ${area}, valore_originale = ${this.risk_val_oggi[area].valore_originale}`)
          const valanghe_oggi = this.rischio_valanghe(Number(this.risk_val_oggi[area].valore_originale))
          stack = stack.concat(this.setFirstGuess(zona, 'valanghe_oggi', valanghe_oggi, copy_over))
        }
        // console.log(`this.risk_val_domani = ${JSON.stringify(this.risk_val_domani)}`)
        if (area in this.risk_val_domani) {
          // console.log(`looking at area ${area}, valore_originale = ${this.risk_val_domani[area].valore_originale}`)
          const valanghe_domani = this.rischio_valanghe(Number(this.risk_val_domani[area].valore_originale))
          stack = stack.concat(this.setFirstGuess(zona, 'valanghe_domani', valanghe_domani, copy_over))
        }
      })

      if (this.availability.vigilanza){
        this.allerta.fraserisknat = this.vigilanza.sintesi_meteo
        this.saveField('fraserisknat')
      }

      const payloadusername = {"id_key":"id_w23","id":this.allerta.id_w23,"value_key":"username","new_value": store.state.username}
      stack.push(payloadusername)
      const payloadstatus = {"id_key":"id_w23","id":this.allerta.id_w23,"value_key":"status","new_value": 0}
      stack.push(payloadstatus)
      this.saveW23(stack, () => {
        this['firstguessing'] = false
        this.allerta.status = '0'
        this.$toast.open(
          {
            message: "First guess completata",
            type: 'success',
            position: 'top-left'
          }
        )
      })
      return stack
    },
    async fetchAction(action) {
      const response = await api.fetch_wrapper(
        store.state.access,
        `/api/w23/bulletins/${this.allerta.id_w23}/${action}/`
      )
      return response
    },
    really_execute(action, reroute, message) {
      this[action + 'ing'] = true
      this.fetchAction(action).then(response => {
        this[action + 'ing'] = false
        if (response.ok) {
          return response.json()
        } else {
          this.$toast.open(
            {
              message: `Errore ${response.status} nell'esecuzione del comando ${action}`,
              type: 'error',
              position: 'top-left'
            }
          )
        }
      }).then(data => {
        this.$toast.open(
          {
            message: message,
            type: 'success',
            position: 'top-left'
          }
        )
        if (reroute) {
          this.$router.push({ path: `/w23/${data.id_w23}`})
          this.allerta_id = data.id_w23
          this.countfetch = 0
          this.fetchData()
        } else {
          this.fetchData()
        }
      }).catch((error) => {
        this[action + 'ing'] = false
        this.$toast.open(
          {
            message: error,
            type: 'error',
            position: 'top-left'
          }
        )
      })
    },
    remove() {
      if (
        confirm('Vuoi davvero cancellare questo bollettino?')
      ) {
        api.fetchBulletinDelete(this.allerta.id_w23, 'w23/bulletins', store).then(response => {
          if (response.ok) {
            this.$toast.open(
              {
                message: 'Bollettino cancellato',
                type: 'success',
                position: 'top-left'
              }
            )
            this.bozza_presente = false
            this.$router.push({ path: `/w23`})
          } else {
            this.$toast.open(
              {
                message: `Errore ${response.status} nella cancellazione del bollettino`,
                type: 'error',
                position: 'top-left'
              }
            )
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
    add(agg, sources) {
      // console.log('-----------------',agg, sources)
      let total = 0
      let countObservations = 0
      let countForecasts = 0
      Object.keys(agg).forEach(area => {
        total = 0
        countObservations = 0
        countForecasts = 0
        //console.log(this.pluv)
        sources.forEach(tl => {
          total += 6
          if(this.availability.pluvoss){
            if (tl in this.pluvossh6[area]) {
              //console.log("preferisco le osservazioni")
              // prefer observations
              agg[area] += Number(this.pluvossh6[area][tl])
              countObservations += 6
            } else{
              //console.log("quando le osservazionimancano preferisci le previsioni")
              if (this.pluv){
                //console.log("this.pluv")
                if (tl in this.pluv){
                  //console.log(tl, "tl in this.pluv")
                  if (900 in this.pluv[tl]) {
                    //console.log(tl, "900 è dentro", this.pluv[tl])
                    // when observations are missing, try forecasts
                    agg[area] += this.pluv[tl][900][area]
                    countForecasts += 6
                  /*}else{
                    console.log(tl, "900 non in",this.pluv[tl])*/
                  }
                }/*else{
                  console.log(tl,"non in this.pluv", this.pluv)
                }*/
              }/*else{
                console.log("this.pluv non c'è")
              }*/
            }
          }else{
            //console.log("non abbiamo pluvoss")
            if (this.pluv){
              //console.log("this.pluv")
              if (tl in this.pluv){
                //console.log(tl, "tl in this.pluv")
                if (900 in this.pluv[tl]) {
                  //console.log(tl, "900 è dentro", this.pluv[tl])
                  // when observations are missing, try forecasts
                  agg[area] += this.pluv[tl][900][area]
                  countForecasts += 6
                }/*else{
                  //console.log(tl, "900 non in",this.pluv[tl])
                }*/
              }else{
                //console.log(tl,"non in this.pluv", this.pluv)
                countForecasts += 6
              }
            }/*else{
              console.log("this.pluv non c'è")
            }*/
          }
          //console.log(tl, countObservations, countForecasts)
        })
      })
      return {
        observations: 100.0 * countObservations / total,
        forecasts: 100.0 * countForecasts / total
      }
    },
    subtractHours(date, hours) {
      date.setHours(date.getHours() - hours)
      return date
    },
    pluvoss(pfdb) {
      const reference = new Date(this.allerta.data_emissione + " 00:00:00")
      const tl_map = {
        "-30": 12,
        "-24": 26,
        "-18": 27,
        "-12": 28,
        "-6": 29,
        "0": 43,
        "6": 44,
        "12": 45,
        "18": 46,
      } // maps from number of hours in the future to the time layouts we're interested in
      return this.rearrange(
        pfdb,
        "area",
        data => {
          data.forEach(item => {
            item.start = this.subtractHours(new Date(`${item.data} ${item.ora}`), 6)
            const delta_hours = (item.start - reference) / 3600000  // number of hours in the future (positive) or past (negative)
            if (delta_hours in tl_map) {
              item.id_time_layouts = tl_map[delta_hours]
            } else {
              item.id_time_layouts = null
            }
            return item
          })
          return this.rearrange(
            data,
            "id_time_layouts",
            arr => arr[0].valore
          )
        }
      )
    },
    pluvoss_available(p) {
      return "12" in p['Piem-A'] ||
        "26" in p['Piem-A'] ||
        "27" in p['Piem-A'] ||
        "28" in p['Piem-A'] ||
        "29" in p['Piem-A'] ||
        "43" in p['Piem-A'] ||
        "44" in p['Piem-A'] || 
        "45" in p['Piem-A'] 
    },
    async fetchData (callback = null) {
      this.ready = false
      this.pericoli = await this.fetchJson("/api/w23/pericoli/", "Pericolo")
      const data = await this.fetchJson(`/api/w23/bulletins/${this.allerta_id}/`, "Bollettino di allerta")
      data.w23data_set.forEach(w23data => {
        this.lista_parametri_completa.forEach(key => {
          w23data[key] = JSON.parse(JSON.stringify(this.pericolo_da_id[w23data[key]]))
        })
        // temporale_domani: "ASSENTI"
        // temporale_oggi: "ASSENTI"
      })
      this.allerta = data
      this.effetti = await this.fetchJson('/api/w23/effetti/', "Effetti sul territorio")
      this.time_layouts = this.rearrange(
        await this.fetchJson("/api/w23/time_layouts/", "Time Layouts"),
        "id_time_layouts",
        arr => arr[0]
      )
      this.fill_tls_lookup()
      this.fill_labels()
      this.vigilanza = await this.fetchJson(`/api/w24/current/${this.allerta.data_emissione}`, "Bollettino di vigilanza")
      this.psa = await this.fetchJson(`/api/w30/current/${this.allerta.data_emissione}`, "Bollettino PSA")
      this.soglie_nivo_area_prev = this.rearrange(
        await this.fetchJson("/api/w23/soglie_nivo_area_prev/", "Soglie neve"),
        "ambito",
        data => this.rearrange(data, "idtab_allertamento", arr => arr[0])
      )
      this.soglie_pluv_area_prev_massimi = this.rearrange2(
        await this.fetchJson("/api/w23/soglie_pluv_area_prev_massimi/", "Soglie Pioggia massima"),
        ["h6", "h12", "h24"],
        "idtab_allertamento"
      )
      this.soglie_pluv_area_prev_medie = this.rearrange2(
        await this.fetchJson("/api/w23/soglie_pluv_area_prev_medie/", "Soglie Pioggia media"),
        ["h6", "h12", "h24", "h48"],
        "idtab_allertamento",
      )
      const risk_val = await this.fetchJson("/api/w24/fz/?id_parametro=RISK_VAL", "RISK_VAL da forecast zone")
      this.risk_val_oggi = this.rearrange(
        risk_val,
        "id_allertamento",
        arr => arr.filter(risk => risk.data_riferimento.substring(0, 10) == this.allerta.data_emissione)[0]
      )
      let tomorrow = new Date(this.allerta.data_emissione)
      tomorrow.setDate(tomorrow.getDate() + 1)
      const tomorrow_date = tomorrow.toISOString().substring(0, 10)
      // console.log('PRIMA this.risk_val_domani-------',this.risk_val_domani)
      this.risk_val_domani = this.rearrange(
        risk_val,
        "id_allertamento",
        arr => arr.filter(risk => risk.data_riferimento.substring(0, 10) == tomorrow_date)[0]
      )
      // console.log('DOPO this.risk_val_domani-------',this.risk_val_domani)
      // aggregate data in 6-hours groups and compute id_time_layouts
      let pluvossh6_from_db = await this.fetchJson(`/api/w23/pluvossh6/`, "Precipitazioni medie esaorarie osservate")
      // console.log("pluvossh6_from_db.length", pluvossh6_from_db.length)
      let pluvoss_availability=false
      if(pluvossh6_from_db.length>0){
        // this.pluvoss_available(this.pluvossh6)
        pluvoss_availability=true
        this.pluvossh6 = this.pluvoss(pluvossh6_from_db)
      }
      this.availability = {
        risk_val_oggi: this.risk_val_oggi && Object.keys(this.risk_val_oggi).length > 0,
        risk_val_domani: this.risk_val_domani && Object.keys(this.risk_val_domani).length > 0,
        vigilanza: this.vigilanza && 'w24data_set' in this.vigilanza,
        psa: this.psa && 'w30data_set' in this.psa,
        pluvoss: pluvoss_availability
      }

      this.fill_neve()
      this.fill_risk_storm()
      this.fill_pluv()
      this.fill_piogge_massime()
      this.fill_piogge_medie()
      this.fill_colore_risk_storm_oggi()
      this.fill_colore_risk_storm_domani()
      if (this.allerta.status === status_first_time) {
        this.firstguess(true)
      }
      if (callback) {
        callback()
      }
      this.ready = true
    },
    async fetchJson (endpoint, description) {
      try {
        const response = await fetch(endpoint, {
          headers: {
            accept: 'application/json'
          }
        })
        if (!response.ok) {
          this.$toast.open(
            {
              message: `Errore ${response.status} nel recupero di ${description}`,
              type: 'error',
              position: 'top-left'
            }
          )
          return {}
        } else {
          return response.json()
        }
      } catch(error) {
        this.$toast.open(
          {
            message: error,
            type: 'error',
            position: 'top-left'
          }
        )
        return {}
      }
    },
    getDateFormatted(rawString, time = true) {
      return api.getDateFormatted(rawString, time)
    },
    massimo(id_w23_zone, parametri) {
      let m = undefined
      parametri.forEach(parametro => {
        let area = this.area_pericolo[parametro][id_w23_zone]
        if (!m) {
          m = area
        } else {
          if (m.sort_index < area.sort_index) {
            m = area
          }
        }
      })
      return m
    },
    massimo_for(area, parametri) {
      let m = undefined
      parametri.forEach(parametro => {
        if (!m) {
          m = area[parametro]
        } else {
          if (m.sort_index < area[parametro].sort_index) {
            m = area[parametro]
          }
        }
      })
      return m
    },
    setPericolo(zona, campo, pericolo) {
      // console.log(`setPericolo(${zona}, ${campo}, ${pericolo})`)
      zona[campo].id_w23_pericolo = pericolo.id_w23_pericolo
      zona[campo].colore_html = pericolo.colore_html
      zona[campo].sort_index = pericolo.sort_index
    },
    setFirstGuess(zona, campo, indice, copy_over) {
      const pericolo = this.pericolo_da_indice[indice]
      if (copy_over) {
        this.setPericolo(zona, campo, pericolo)
        this.setPericolo(zona, `${campo}_for`, pericolo)
        return [
            {"id_key":"id_w23_data","id":zona.id_w23_data,"value_key":campo,"new_value": pericolo.id_w23_pericolo},
            {"id_key":"id_w23_data","id":zona.id_w23_data,"value_key": `${campo}_for`,"new_value": pericolo.id_w23_pericolo},
        ]
      } else {
        this.setPericolo(zona, `${campo}_for`, pericolo)
        return [
            {"id_key":"id_w23_data","id":zona.id_w23_data,"value_key": `${campo}_for`,"new_value": pericolo.id_w23_pericolo},
        ]
      }
    },
    saveW23(stack, callback=null) {
      this.bulkUpdateW23(stack).then((response) => {
        if (!response.ok) {
          this.$toast.open(
            {
              message: 'Errore nel salvataggio',
              type: 'error',
              position: 'top-left'
            }
          )
          this.saving = false
        }
        return response.json()
      }).then(data => {
        this.$toast.open(
        {
            message: 'Dato salvato',
            type: 'success',
            position: 'top-left'
        }
        )
        this.allerta.last_update = data.bulletin.last_update
        this.allerta.last_update_annotazione = data.bulletin.last_update_annotazione
        this.allerta.username = store.state.username
        this.saving = false
        if (callback) {
          callback()
        }
      }).catch((error) => {
        this.$toast.open(
          {
            message: `Errore di comunicazione: ${error}`,
            type: 'error',
            position: 'top-left'
          }
        )
        this.saving = false
      })
    },
    async bulkUpdateW23(snapshots) {
      let payload = snapshots
      const response = await api.fetch_wrapper(
        store.state.access,
        `/api/w23/bulletins/bulk_update/`,
        {
          method: 'POST',
          body: JSON.stringify(payload)
        }
      )
      return response
    },
    goto(id) {
      const element = document.getElementById(id)
      element.scrollIntoView({ behavior: "smooth" })
    },
    getOffsetDateFormatted(base, day_offset, time_offset) {
      const baseDate = new Date(base + " 00:00")
      baseDate.setDate(baseDate.getDate() + day_offset)
      let [hours_offset, minutes_offset] = time_offset.split(":").map(x => parseInt(x))
      baseDate.setHours(baseDate.getHours() + hours_offset)
      baseDate.setMinutes(baseDate.getMinutes() + minutes_offset)
      const day = baseDate.getDate()
      var hour = baseDate.getHours()
      const dow = ["Dom", "Lun", "Mar", "Mer", "Gio", "Ven", "Sab"][baseDate.getDay()]
      // console.log(hour,hour.toString().length)
      if (hour.toString().length == 1) hour = "0" + hour
      return `${dow} ${day} ore ${hour}`
    },
    rearrange(data, key, func=null) {
      // rearranges the array data in a dictionary
      // aggregating all records with the same key as an array
      // optionally transforming each array with the func function
      let value_data = {}
      data.forEach(record => {
        if (!(record[key] in value_data)) {
          value_data[record[key]] = []
        }
        // console.log('rearrange record', record)
        value_data[record[key]].push(record)
      })
      if (func) {
        Object.keys(value_data).forEach(key => value_data[key] = func(value_data[key]))
      }
      if(!Object.values(value_data).some(item => item != undefined)) value_data = {}
      return value_data
    },
    rearrange2(data, keys, key2) {
      // rearranges the array data in a two-level dictionary
      // pulling out the values of the keys as dictionaries
      // aggregating all records with the same key2 as sorted arrays
      let value_data = Object.fromEntries(keys.map(k => [k, {}]))
      data.forEach(record => {
        keys.forEach(k => {
          if (!(record[key2] in value_data[k])) {
            value_data[k][record[key2]] = []
          }
          value_data[k][record[key2]].push(record[k])
        })
      })
      keys.forEach(k => Object.keys(value_data[k]).forEach(k2 => value_data[k][k2].sort((a, b) => a - b)))
      return value_data
    },
  }
}
</script>
