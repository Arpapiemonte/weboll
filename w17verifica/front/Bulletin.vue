// Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <div class="container-fluid">
    <div
      class="row justify-content-end sticky-top py-1"
      style="background-color: #f8f9fa;"
    >
      <!-- https://getbootstrap.com/docs/5.1/components/button-group/ -->
      <div
        class="btn-group w-auto"
        role="group"
        aria-label="Basic outlined example"
      >
        <a
          class="btn btn-outline-primary"
          :href="'/api/w17verifica/pdf/' + verifica.id_w17verifica"
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
          v-if="verifica.status === '0' && state.username"
          :disabled="actions.sending"
          type="button"
          class="btn btn-outline-success"
          @click="execute('send', false, 'Bollettino inviato')"
        >
          <span v-if="actions.sending">
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
              alt="unlock icon"
              width="18"
              height="18"
            > Invia
          </span>
        </button>
        <button
          v-if="state.username && verifica.data_emissione.substring(0, 10) === today"
          type="button"
          class="btn btn-outline-danger"
          @click="remove()"
        >
          <img
            src="~bootstrap-icons/icons/trash-fill.svg"
            alt="unlock icon"
            width="18"
            height="18"
          > Elimina
        </button>
      </div>
    </div>

    <div class="row mb-3">
      <h1>Bollettino Verifica Meteo {{ verifica.id_w17verifica }}</h1>
      <!--
      <div
        class="alert alert-danger"
      >
        Ci sono dei campi incompleti
      </div>-->
    </div>
    <div class="row">
      <div class="col-md-2 mb-3">
        <label for="status">Stato
          <span v-if="verifica.status === '1'">
            <input
              id="stato"
              disabled
              class="form-control"
              name="stato"
              type="text"
              value="Inviato"
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
            :value="getDateFormatted(verifica.data_emissione, false)"
          >
        </label>
      </div>
      <div class="col-md-2 mb-3">
        <label for="data_analisi">Data analisi
          <input
            id="data_analisi"
            disabled
            class="form-control"
            name="data_analisi"
            type="text"
            :value="getDateFormatted(verifica.data_analysis, false)"
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
            :value="getDateFormatted(verifica.last_update)"
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
            :value="verifica.username"
          >
        </label>
      </div>
      <div v-if="ready">
        <div class="d-flex justify-content-center">
          <div class="col-md-11 mb-3">
            <div class="row">
              <div class="col-md-12 mb-3">
                <ul
                  id="pills-tab"
                  class="nav nav-pills mb-3"
                  role="tablist"
                >
                  <li
                    class="nav-item"
                    role="presentation"
                  >
                    <button
                      id="pills-verifica12-tab"
                      class="nav-link active"
                      data-bs-toggle="pill"
                      data-bs-target="#pills-verifica12"
                      type="button"
                      role="tab"
                      aria-controls="pills-verifica12"
                      aria-selected="true"
                    >
                      Verifica +12
                    </button>
                  </li>
                  <li
                    class="nav-item"
                    role="presentation"
                  >
                    <button
                      id="pills-verifica24-tab"
                      class="nav-link"
                      data-bs-toggle="pill"
                      data-bs-target="#pills-verifica24"
                      type="button"
                      role="tab"
                      aria-controls="pills-verifica24"
                      aria-selected="false"
                    >
                      Verifica +24
                    </button>
                  </li>
                  <li
                    class="nav-item"
                    role="presentation"
                  >
                    <button
                      id="pills-verifica48-tab"
                      class="nav-link"
                      data-bs-toggle="pill"
                      data-bs-target="#pills-verifica48"
                      type="button"
                      role="tab"
                      aria-controls="pills-verifica48"
                      aria-selected="false"
                    >
                      Verifica +48
                    </button>
                  </li>
                  <li
                    class="nav-item"
                    role="presentation"
                  >
                    <button
                      id="pills-statistica-tab"
                      class="nav-link"
                      data-bs-toggle="pill"
                      data-bs-target="#pills-statistica"
                      type="button"
                      role="tab"
                      aria-controls="pills-statistica"
                      aria-selected="false"
                    >
                      Statistica
                    </button>
                  </li>
                </ul>
                <div
                  id="pills-tabContent"
                  class="tab-content"
                >
                  <div
                    id="pills-verifica12"
                    class="tab-pane fade show active"
                    role="tabpanel"
                    aria-labelledby="pills-verifica12-tab"
                  >
                    <div class="row">
                      <div class="col-sm">
                        <table class="table">
                          <thead>
                            <tr>
                              <th
                                class="text-left"
                              />
                              <th
                                class="text-left"
                              >
                                Osservata 
                              </th>
                              <th
                                class="text-left"
                              >
                                Prevista 
                              </th>
                              <th
                                class="text-center"
                              >
                                Punti 
                              </th>
                              <th
                                class="text-center"
                              >
                                Max 
                              </th>
                            </tr>
                            <tr>
                              <th
                                class="text-left"
                                colspan="5"
                              >
                                Nuvolosità Mattino
                              </th>
                            </tr>
                          </thead>
                          <!--<tbody>-->
                          <tr>
                            <td
                              class="text-left"
                              scope="row"
                            >
                              Classe nubi
                            </td>
                            <td
                              style="line-height:2em;background:rgb(220, 218, 218)"
                              class="text-left"
                              scope="row"
                            >
                              <TableCell
                                style="background:rgb(220, 218, 218)"
                                :meteoclasses="meteoclasses['COP_TOT']['1'].classes_values"
                                :value="analisibulletin.w17_classes['COP_TOT']['30']['1'].id_classes_value"
                              />
                            </td>
                            <td
                              style="background:rgb(220, 218, 218)"
                              class="text-left"
                              scope="row"
                            >
                              Non disponibile
                            </td>
                            <td
                              style="background:rgb(220, 218, 218)"
                              class="text-center"
                              scope="row"
                            >
                              0
                            </td>
                            <td
                              style="background:rgb(220, 218, 218)"
                              class="text-center"
                              scope="row"
                            >
                              2
                            </td>
                          </tr>
                          <tr>
                            <td
                              class="text-left"
                              scope="row"
                            >
                              Evoluzione
                            </td>
                            <td
                              style="line-height:2em;background:rgb(220, 218, 218)"
                              class="text-left"
                              scope="row"
                            >
                              <TableCell
                                style="background:rgb(220, 218, 218)"
                                :meteoclasses="meteoclasses['COP_TOT']['2'].classes_values"
                                :value="analisibulletin.w17_classes['COP_TOT']['30']['2'].id_classes_value"
                              />
                            </td>
                            <td
                              style="background:rgb(220, 218, 218)"
                              class="text-left"
                              scope="row"
                            >
                              Non disponibile
                            </td>
                            <td
                              style="background:rgb(220, 218, 218)"
                              class="text-center"
                              scope="row"
                            >
                              0
                            </td>
                            <td
                              style="background:rgb(220, 218, 218)"
                              class="text-center"
                              scope="row"
                            >
                              2
                            </td>
                          </tr>
                          <tr>
                            <td
                              class="text-left"
                              scope="row"
                            >
                              Visibilità
                            </td>
                            <td
                              style="line-height:2em;background:rgb(220, 218, 218)"
                              class="text-left"
                              scope="row"
                            >
                              <TableCell
                                style="background:rgb(220, 218, 218)"
                                :meteoclasses="meteoclasses['COP_TOT']['4'].classes_values"
                                :value="analisibulletin.w17_classes['COP_TOT']['30']['4'].id_classes_value"
                              />
                            </td>
                            <td
                              style="background:rgb(220, 218, 218)"
                              class="text-left"
                              scope="row"
                            >
                              Non disponibile
                            </td>
                            <td
                              style="background:rgb(220, 218, 218)"
                              class="text-center"
                              scope="row"
                            >
                              0
                            </td>
                            <td
                              style="background:rgb(220, 218, 218)"
                              class="text-center"
                              scope="row"
                            >
                              0
                            </td>
                          </tr>
                          <tr>
                            <td
                              class="text-left"
                              scope="row"
                            >
                              Localizzazione/Coerenza
                            </td>
                            <td
                              class="text-left"
                              scope="row"
                            />
                            <td
                              class="text-left"
                              scope="row"
                            />
                            <td
                              class="text-center"
                              scope="row"
                              style="background:rgb(220, 218, 218)"
                            >
                              <input
                                id="coerenza_mattino_nubi12"
                                style="width: 4em;background:rgb(220, 218, 218)"
                                type="number"
                                min="0"
                                max="2"
                                :readonly="true"
                                class="form-control text-center"
                                name="coerenza_mattino_nubi12"
                                :value="Number(verifica.w17_verifica_data_set[0].coerenza_mattino_nubi)"
                                @change="saveCoerenza($event.target.value, verifica.w17_verifica_data_set[0].id_w17_verifica_data, 'coerenza_mattino_nubi')"
                              >
                            </td>
                            <td
                              class="text-center"
                              scope="row"
                              style="background:rgb(220, 218, 218)"
                            >
                              2
                            </td>
                          </tr>
                          <!--</tbody>
                        </table>
                        <table class="table">
                          <thead>-->
                          <tr>
                            <th
                              class="text-left"
                              colspan="5"
                            >
                              Precipitazioni Mattino
                            </th>
                          </tr>
                          <!--</thead>
                          <tbody>-->
                          <tr>
                            <td
                              class="text-left"
                              scope="row"
                            >
                              Classe su Regione
                            </td>
                            <td
                              style="line-height:2em;background:rgb(220, 218, 218)"
                              class="text-left"
                              scope="row"
                            >
                              <TableCell
                                style="background:rgb(220, 218, 218)"
                                :meteoclasses="meteoclasses['PLUV']['5'].classes_values"
                                :value="analisibulletin.w17_classes['PLUV']['30']['5'].id_classes_value"
                              />
                            </td>
                            <td
                              style="background:rgb(220, 218, 218)"
                              class="text-left"
                              scope="row"
                            >
                              Non disponibile
                            </td>
                            <td
                              style="background:rgb(220, 218, 218)"
                              class="text-center"
                              scope="row"
                            >
                              0
                            </td>
                            <td
                              style="background:rgb(220, 218, 218)"
                              class="text-center"
                              scope="row"
                            >
                              2
                            </td>
                          </tr>
                          <tr>
                            <td
                              class="text-left"
                              scope="row"
                            >
                              Classe su Area
                            </td>
                            <td
                              style="line-height:2em;background:rgb(220, 218, 218)"
                              class="text-left"
                              scope="row"
                            > 
                              <TableCell
                                style="background:rgb(220, 218, 218)"
                                :meteoclasses="meteoclasses['PLUV']['6'].classes_values"
                                :value="analisibulletin.w17_classes['PLUV']['30']['6'].id_classes_value"
                              />
                            </td>
                            <td
                              style="background:rgb(220, 218, 218)"
                              class="text-left"
                              scope="row"
                            >
                              Non disponibile
                            </td>
                            <td
                              style="background:rgb(220, 218, 218)"
                              class="text-center"
                              scope="row"
                            >
                              0
                            </td>
                            <td
                              style="background:rgb(220, 218, 218)"
                              class="text-center"
                              scope="row"
                            >
                              2
                            </td>
                          </tr>
                          <tr>
                            <td
                              class="text-left"
                              scope="row"
                            >
                              Classe massimo
                            </td>
                            <td
                              style="line-height:2em;background:rgb(220, 218, 218)"
                              class="text-left"
                              scope="row"
                            > 
                              <TableCell
                                style="background:rgb(220, 218, 218)"
                                :meteoclasses="meteoclasses['PLUV']['7'].classes_values"
                                :value="analisibulletin.w17_classes['PLUV']['30']['7'].id_classes_value"
                              />
                            </td>
                            <td
                              style="background:rgb(220, 218, 218)"
                              class="text-left"
                              scope="row"
                            >
                              Non disponibile
                            </td>
                            <td
                              style="background:rgb(220, 218, 218)"
                              class="text-center"
                              scope="row"
                            >
                              0
                            </td>
                            <td
                              style="background:rgb(220, 218, 218)"
                              class="text-center"
                              scope="row"
                            >
                              2
                            </td>
                          </tr>
                          <tr>
                            <td
                              class="text-left"
                              scope="row"
                            >
                              Nuvolosità
                            </td>
                            <td
                              style="line-height:2em;background:rgb(220, 218, 218)"
                              class="text-left"
                              scope="row"
                            > 
                              <TableCell
                                style="background:rgb(220, 218, 218)"
                                :meteoclasses="meteoclasses['PLUV']['8'].classes_values"
                                :value="analisibulletin.w17_classes['PLUV']['30']['8'].id_classes_value"
                              />
                            </td>
                            <td
                              style="background:rgb(220, 218, 218)"
                              class="text-left"
                              scope="row"
                            >
                              Non disponibile
                            </td>
                            <td
                              style="background:rgb(220, 218, 218)"
                              class="text-center"
                              scope="row"
                            >
                              0
                            </td>
                            <td
                              style="background:rgb(220, 218, 218)"
                              class="text-center"
                              scope="row"
                            >
                              2
                            </td>
                          </tr>
                          <tr>
                            <td
                              class="text-left"
                              scope="row"
                            >
                              Localizzazione/Coerenza
                            </td>
                            <td
                              class="text-left"
                              scope="row"
                            />
                            <td
                              class="text-left"
                              scope="row"
                            />
                            <td
                              class="text-center"
                              scope="row"
                              style="background-color:rgb(220, 218, 218)"
                            >
                              <input
                                id="coerenza_mattino_pioggia12"
                                style="width: 5em;background:rgb(220, 218, 218)"
                                type="number"
                                min="0"
                                max="2"
                                :readonly="true"
                                class="form-control"
                                name="coerenza_mattino_pioggia12"
                                :value="Number(verifica.w17_verifica_data_set[0].coerenza_mattino_pioggia)"
                                @change="saveCoerenza($event.target.value, verifica.w17_verifica_data_set[0].id_w17_verifica_data, 'coerenza_mattino_pioggia')"
                              >
                            </td>
                            <td
                              style="background:rgb(220, 218, 218)"
                              class="text-center"
                              scope="row"
                            >
                              2
                            </td>
                          </tr>
                          <!--</tbody>
                        </table>
                        <table class="table">
                          <thead>-->
                          <tr>
                            <th
                              class="text-left"
                              colspan="5"
                            >
                              Zero Termico
                            </th>
                          </tr>
                          <!--</thead>-->
                          <tbody>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Valore 12-24
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.w17_data['FRZLVL']['31']['0'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[0].w05_data['FRZLVL']['48']['0'].numeric_value) }}
                              </td>
                              <td
                                class="text-center"
                                scope="row"
                              >
                                {{ punti['FRZLVL'][0]['48']['data'] }}
                              </td>
                              <td
                                class="text-center"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Andamento 12-24
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['FRZLVL']['12'].classes_values"
                                  :value="analisibulletin.w17_classes['FRZLVL']['31']['12'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['FRZLVL']['12'].classes_values"
                                  :value="meteobulletins[0].w05_classes['FRZLVL']['48']['12'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-center"
                                scope="row"
                              >
                                {{ punti['FRZLVL'][0]['48']['12'] }}
                              </td>
                              <td
                                class="text-center"
                                scope="row"
                              >
                                1
                              </td>
                            </tr>
                            <!--</tbody>
                        </table>
                        <table class="table">
                          <thead>-->
                            <tr>
                              <th
                                class="text-left"
                                colspan="5"
                              >
                                Temperatura
                              </th>
                            </tr>
                            <!--</thead>
                          <tbody>-->
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Scarto minima
                              </td>
                              <td
                                style="background:rgb(220, 218, 218)"
                                class="text-left"
                                scope="row"
                                colspan="2"
                              />
                              <td
                                style="background:rgb(220, 218, 218)"
                                class="text-center"
                                scope="row"
                              />
                              <td
                                style="background:rgb(220, 218, 218)"
                                class="text-center"
                                scope="row"
                              />
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Scarto massima
                              </td>
                              <td
                                style="background:rgb(220, 218, 218)"
                                class="text-left"
                                scope="row"
                                colspan="2"
                              />
                              <td
                                style="background:rgb(220, 218, 218)"
                                class="text-center"
                                scope="row"
                              />
                              <td
                                style="background:rgb(220, 218, 218)"
                                class="text-center"
                                scope="row"
                              />
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                andam.minima
                              </td>
                              <td
                                style="line-height:2em;background:rgb(220, 218, 218)"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['TERMA']['9'].classes_values"
                                  :value="analisibulletin.w17_classes['TERMA']['34']['9'].id_classes_value"
                                />
                              </td>
                              <td
                                style="background:rgb(220, 218, 218)"
                                class="text-left"
                                scope="row"
                              >
                                Non disponibile
                              </td>
                              <td
                                style="background:rgb(220, 218, 218)"
                                class="text-center"
                                scope="row"
                              />
                              <td
                                style="background:rgb(220, 218, 218)"
                                class="text-center"
                                scope="row"
                              />
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                andam.massima
                              </td>
                              <td
                                style="line-height:2em;background:rgb(220, 218, 218)"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  style="background:rgb(220, 218, 218)"
                                  :meteoclasses="meteoclasses['TERMA']['10'].classes_values"
                                  :value="analisibulletin.w17_classes['TERMA']['33']['10'].id_classes_value"
                                />
                              </td>
                              <td
                                style="background:rgb(220, 218, 218)"
                                class="text-left"
                                scope="row"
                              >
                                Non disponibile
                              </td>
                              <td
                                style="background:rgb(220, 218, 218)"
                                class="text-center"
                                scope="row"
                              />
                              <td
                                style="background:rgb(220, 218, 218)"
                                class="text-center"
                                scope="row"
                              />
                            </tr>
                          </tbody>
                        </table>
                        <table class="table">
                          <tbody>
                            <tr>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                MIN
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                AL
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                AT
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                BI
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                CN
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                NO
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                TO
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                VB
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                VC
                              </th>	
                            </tr>
                            <tr>
                              <th
                                style="background:rgb(220, 218, 218)"
                                class="text-left"
                                scope="row"
                              >
                                OSS
                              </th>
                              <td
                                style="background:rgb(220, 218, 218)"
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['34']['9'].numeric_value) }}
                              </td>
                              <td
                                style="background:rgb(220, 218, 218)"
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['34']['11'].numeric_value) }}
                              </td>
                              <td
                                style="background:rgb(220, 218, 218)"
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['34']['1'].numeric_value) }}
                              </td>
                              <td
                                style="background:rgb(220, 218, 218)"
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['34']['28'].numeric_value) }}
                              </td>
                              <td
                                style="background:rgb(220, 218, 218)"
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['34']['33'].numeric_value) }}
                              </td>
                              <td
                                style="background:rgb(220, 218, 218)"
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['34']['59'].numeric_value) }}
                              </td>
                              <td
                                style="background:rgb(220, 218, 218)"
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['34']['63'].numeric_value) }}
                              </td>
                              <td
                                style="background:rgb(220, 218, 218)"
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['34']['64'].numeric_value) }}
                              </td>
                            </tr>
                            <tr>
                              <th
                                style="background:rgb(220, 218, 218)"
                                class="text-left"
                                scope="row"
                              >
                                FOR
                              </th>
                              <td
                                style="background:rgb(220, 218, 218)"
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[0].rearrangemeteoterma['TERMA']['51']['9'].numeric_value) }}
                              </td>
                              <td
                                style="background:rgb(220, 218, 218)"
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[0].rearrangemeteoterma['TERMA']['51']['11'].numeric_value) }}
                              </td>
                              <td
                                style="background:rgb(220, 218, 218)"
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[0].rearrangemeteoterma['TERMA']['51']['1'].numeric_value) }}
                              </td>
                              <td
                                style="background:rgb(220, 218, 218)"
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[0].rearrangemeteoterma['TERMA']['51']['28'].numeric_value) }}
                              </td>
                              <td
                                style="background:rgb(220, 218, 218)"
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[0].rearrangemeteoterma['TERMA']['51']['33'].numeric_value) }}
                              </td>
                              <td
                                style="background:rgb(220, 218, 218)"
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[0].rearrangemeteoterma['TERMA']['51']['59'].numeric_value) }}
                              </td>
                              <td
                                style="background:rgb(220, 218, 218)"
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[0].rearrangemeteoterma['TERMA']['51']['63'].numeric_value) }}
                              </td>
                              <td
                                style="background:rgb(220, 218, 218)"
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[0].rearrangemeteoterma['TERMA']['51']['64'].numeric_value) }}
                              </td>
                            </tr>
                          </tbody>
                        </table>                       
                        <table class="table">
                          <tbody>
                            <tr>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                MAX
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                AL
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                AT
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                BI
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                CN
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                NO
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                TO
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                VB
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                VC
                              </th>	
                            </tr>
                            <tr>
                              <th
                                style="background:rgb(220, 218, 218)"
                                class="text-left"
                                scope="row"
                              >
                                OSS
                              </th>
                              <td
                                style="background:rgb(220, 218, 218)"
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['33']['9'].numeric_value) }}
                              </td>
                              <td
                                style="background:rgb(220, 218, 218)"
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['33']['11'].numeric_value) }}
                              </td>
                              <td
                                style="background:rgb(220, 218, 218)"
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['33']['1'].numeric_value) }}
                              </td>
                              <td
                                style="background:rgb(220, 218, 218)"
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['33']['28'].numeric_value) }}
                              </td>
                              <td
                                style="background:rgb(220, 218, 218)"
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['33']['33'].numeric_value) }}
                              </td>
                              <td
                                style="background:rgb(220, 218, 218)"
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['33']['59'].numeric_value) }}
                              </td>
                              <td
                                style="background:rgb(220, 218, 218)"
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['33']['63'].numeric_value) }}
                              </td>
                              <td
                                style="background:rgb(220, 218, 218)"
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['33']['64'].numeric_value) }}
                              </td>
                            </tr>
                            <tr>
                              <th
                                style="background:rgb(220, 218, 218)"
                                class="text-left"
                                scope="row"
                              >
                                FOR
                              </th>
                              <td
                                style="background:rgb(220, 218, 218)"
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[0].rearrangemeteoterma['TERMA']['50']['9'].numeric_value) }}
                              </td>
                              <td
                                style="background:rgb(220, 218, 218)"
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[0].rearrangemeteoterma['TERMA']['50']['11'].numeric_value) }}
                              </td>
                              <td
                                style="background:rgb(220, 218, 218)"
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[0].rearrangemeteoterma['TERMA']['50']['1'].numeric_value) }}
                              </td>
                              <td
                                style="background:rgb(220, 218, 218)"
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[0].rearrangemeteoterma['TERMA']['50']['28'].numeric_value) }}
                              </td>
                              <td
                                style="background:rgb(220, 218, 218)"
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[0].rearrangemeteoterma['TERMA']['50']['33'].numeric_value) }}
                              </td>
                              <td
                                style="background:rgb(220, 218, 218)"
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[0].rearrangemeteoterma['TERMA']['50']['59'].numeric_value) }}
                              </td>
                              <td
                                style="background:rgb(220, 218, 218)"
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[0].rearrangemeteoterma['TERMA']['50']['63'].numeric_value) }}
                              </td>
                              <td
                                style="background:rgb(220, 218, 218)"
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[0].rearrangemeteoterma['TERMA']['50']['64'].numeric_value) }}
                              </td>
                            </tr>
                          </tbody>
                        </table>
                      </div>                    
                      <div class="col-sm">
                        <table class="table">
                          <thead>
                            <tr>
                              <th
                                class="text-left"
                              />
                              <th
                                class="text-left"
                              >
                                Osservata 
                              </th>
                              <th
                                class="text-left"
                              >
                                Prevista 
                              </th>
                              <th
                                class="text-left"
                              >
                                Punti 
                              </th>
                              <th
                                class="text-left"
                              >
                                Max 
                              </th>
                            </tr>
                            <tr>
                              <th
                                class="text-left"
                                colspan="5"
                              >
                                Nuvolosità Pomeriggio
                              </th>
                            </tr>
                          </thead>
                          <!--<tbody>-->
                          <tr>
                            <td
                              class="text-left"
                              scope="row"
                            >
                              Classe nubi
                            </td>
                            <td
                              style="line-height:2em;"
                              class="text-left"
                              scope="row"
                            >
                              <TableCell
                                :meteoclasses="meteoclasses['COP_TOT']['1'].classes_values"
                                :value="analisibulletin.w17_classes['COP_TOT']['31']['1'].id_classes_value"
                              />
                            </td>
                            <td
                              style="line-height:2em;"
                              class="text-left"
                              scope="row"
                            >
                              <TableCell
                                :meteoclasses="meteoclasses['COP_TOT']['1'].classes_values"
                                :value="meteobulletins[0].w05_classes['COP_TOT']['48']['1'].id_classes_value"
                              />
                            </td>
                            <td
                              class="text-center"
                              scope="row"
                            >
                              {{ punti['COP_TOT'][0]['48']['1'] }}
                            </td>
                            <td
                              class="text-center"
                              scope="row"
                            >
                              2
                            </td>
                          </tr>
                          <tr>
                            <td
                              class="text-left"
                              scope="row"
                            >
                              Evoluzione
                            </td>
                            <td
                              style="line-height:2em;"
                              class="text-left"
                              scope="row"
                            >
                              <TableCell
                                :meteoclasses="meteoclasses['COP_TOT']['2'].classes_values"
                                :value="analisibulletin.w17_classes['COP_TOT']['31']['2'].id_classes_value"
                              />
                            </td>
                            <td
                              style="line-height:2em;"
                              class="text-left"
                              scope="row"
                            >
                              <TableCell
                                :meteoclasses="meteoclasses['COP_TOT']['2'].classes_values"
                                :value="meteobulletins[0].w05_classes['COP_TOT']['48']['2'].id_classes_value"
                              />
                            </td>
                            <td
                              class="text-center"
                              scope="row"
                            >
                              {{ punti['COP_TOT'][0]['48']['2'] }}
                            </td>
                            <td
                              class="text-center"
                              scope="row"
                            >
                              2
                            </td>
                          </tr>
                          <tr>
                            <td
                              class="text-left"
                              scope="row"
                            >
                              Visibilità
                            </td>
                            <td
                              style="line-height:2em;"
                              class="text-left"
                              scope="row"
                            >
                              <TableCell
                                :meteoclasses="meteoclasses['COP_TOT']['4'].classes_values"
                                :value="analisibulletin.w17_classes['COP_TOT']['31']['4'].id_classes_value"
                              />
                            </td>
                            <td
                              style="line-height:2em;"
                              class="text-left"
                              scope="row"
                            >
                              <TableCell
                                :meteoclasses="meteoclasses['COP_TOT']['4'].classes_values"
                                :value="meteobulletins[0].w05_classes['COP_TOT']['48']['4'].id_classes_value"
                              />
                            </td>
                            <td
                              class="text-center"
                              scope="row"
                            >
                              {{ punti['COP_TOT'][0]['48']['4'] }}
                            </td>
                            <td
                              class="text-center"
                              scope="row"
                            >
                              2
                            </td>
                          </tr>
                          <tr>
                            <td
                              class="text-left"
                              scope="row"
                            >
                              Localizzazione/Coerenza
                            </td>
                            <td
                              class="text-left"
                              scope="row"
                            />
                            <td
                              class="text-left"
                              scope="row"
                            />
                            <td
                              class="text-left"
                              scope="row"
                            >
                              <input
                                id="coerenza_pomeriggio_nubi12"
                                style="width: 5em;background-color: #eecbda;"
                                :readonly="readonly"
                                type="number"
                                min="0"
                                max="2"
                                class="form-control"
                                name="coerenza_pomeriggio_nubi12"
                                :value="Number(verifica.w17_verifica_data_set[0].coerenza_pomeriggio_nubi)"
                                @change="saveCoerenza($event.target.value, verifica.w17_verifica_data_set[0].id_w17_verifica_data, 'coerenza_pomeriggio_nubi')"
                              >
                            </td>
                            <td
                              class="text-center"
                              scope="row"
                            >
                              2
                            </td>
                          </tr>
                          <!-- </tbody>
                        </table>
                        <table class="table">
                          <thead>-->
                          <tr>
                            <th
                              class="text-left"
                              colspan="5"
                            >
                              Precipitazioni Pomeriggio
                            </th>
                          </tr>
                          <!--</thead>-->
                          <tbody>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Classe su Regione
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              > 
                                <TableCell
                                  :meteoclasses="meteoclasses['PLUV']['5'].classes_values"
                                  :value="analisibulletin.w17_classes['PLUV']['31']['5'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['PLUV']['5'].classes_values"
                                  :value="meteobulletins[0].w05_classes['PLUV']['48']['5'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-center"
                                scope="row"
                              >
                                {{ punti['PLUV'][0]['48']['5'] }}
                              </td>
                              <td
                                class="text-center"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Classe su Area
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['PLUV']['6'].classes_values"
                                  :value="analisibulletin.w17_classes['PLUV']['30']['6'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['PLUV']['6'].classes_values"
                                  :value="meteobulletins[0].w05_classes['PLUV']['48']['6'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-center"
                                scope="row"
                              >
                                {{ punti['PLUV'][0]['48']['6'] }}
                              </td>
                              <td
                                class="text-center"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Classe massimo
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['PLUV']['7'].classes_values"
                                  :value="analisibulletin.w17_classes['PLUV']['30']['7'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['PLUV']['7'].classes_values"
                                  :value="meteobulletins[0].w05_classes['PLUV']['48']['7'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-center"
                                scope="row"
                              >
                                {{ punti['PLUV'][0]['48']['7'] }}
                              </td>
                              <td
                                class="text-center"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Nuvolosità
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['PLUV']['8'].classes_values"
                                  :value="analisibulletin.w17_classes['PLUV']['30']['8'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['PLUV']['8'].classes_values"
                                  :value="meteobulletins[0].w05_classes['PLUV']['48']['8'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-center"
                                scope="row"
                              >
                                {{ punti['PLUV'][0]['48']['8'] }}
                              </td>
                              <td
                                class="text-center"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Localizzazione/Coerenza
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              />
                              <td
                                class="text-left"
                                scope="row"
                              />
                              <td
                                class="text-left"
                                scope="row"
                              >
                                <input
                                  id="coerenza_pomeriggio_pioggia12"
                                  style="width: 5em;background-color: #eecbda;"
                                  :readonly="readonly"
                                  type="number"
                                  min="0"
                                  max="2"
                                  class="form-control"
                                  name="coerenza_pomeriggio_pioggia12"
                                  :value="Number(verifica.w17_verifica_data_set[0].coerenza_pomeriggio_pioggia)"
                                  @change="saveCoerenza($event.target.value, verifica.w17_verifica_data_set[0].id_w17_verifica_data, 'coerenza_pomeriggio_pioggia')"
                                >
                              </td>
                              <td
                                class="text-center"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                          </tbody>
                          <!--</table>
                        <table class="table">
                          <thead>-->
                          <tr>
                            <th
                              class="text-left"
                              colspan="5"
                            >
                              Quota Neve
                            </th>
                          </tr>
                          <!--</thead>
                          <tbody>-->
                          <tr>
                            <td
                              class="text-left"
                              scope="row"
                            >
                              Quota neve min
                            </td>
                            <td
                              class="text-left"
                              scope="row"
                            >
                              {{ Math.round(analisibulletin.w17_data['SNOW_LEV']['32']['1'].numeric_value) }}
                            </td>
                            <td
                              class="text-left"
                              scope="row"
                            >
                              {{ Math.round(meteobulletins[0].w05_data['SNOW_LEV']['48']['1'].numeric_value) }}
                            </td>
                            <td
                              class="text-center"
                              scope="row"
                            >
                              {{ punti['SNOW_LEV'][0]['48']['min'] }}
                            </td>
                            <td
                              class="text-center"
                              scope="row"
                            >
                              1
                            </td>
                          </tr>
                          <tr>
                            <td
                              class="text-left"
                              scope="row"
                            >
                              quota neve max
                            </td>
                            <td
                              class="text-left"
                              scope="row"
                            >
                              {{ Math.round(analisibulletin.w17_data['SNOW_LEV']['32']['0'].numeric_value) }}
                            </td>
                            <td
                              class="text-left"
                              scope="row"
                            >
                              {{ Math.round(meteobulletins[0].w05_data['SNOW_LEV']['48']['0'].numeric_value) }}
                            </td>
                            <td
                              class="text-center"
                              scope="row"
                            >
                              {{ punti['SNOW_LEV'][0]['48']['max'] }}
                            </td>
                            <td
                              class="text-center"
                              scope="row"
                            >
                              1
                            </td>
                          </tr>
                          <!--</tbody>
                        </table>
                        <table class="table">
                          <thead>-->
                          <tr>
                            <th
                              class="text-left"
                              colspan="5"
                            >
                              Venti
                            </th>
                          </tr>
                          <!--</thead>-->
                          <tbody>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Intensità pianura
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['VELV']['16'].classes_values"
                                  :value="analisibulletin.w17_classes['VELV']['32']['16'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['VELV']['16'].classes_values"
                                  :value="meteobulletins[0].w05_classes['VELV']['48']['16'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-center"
                                scope="row"
                              >
                                {{ punti['VELV'][0]['48']['16'] }}
                              </td>
                              <td
                                class="text-center"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Intensità montagna
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['VELV']['18'].classes_values"
                                  :value="analisibulletin.w17_classes['VELV']['32']['18'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['VELV']['18'].classes_values"
                                  :value="meteobulletins[0].w05_classes['VELV']['48']['18'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-center"
                                scope="row"
                              >
                                {{ punti['VELV'][0]['48']['18'] }}
                              </td>
                              <td
                                class="text-center"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Andam. pianura
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['VELV']['17'].classes_values"
                                  :value="analisibulletin.w17_classes['VELV']['32']['17'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['VELV']['17'].classes_values"
                                  :value="meteobulletins[0].w05_classes['VELV']['48']['17'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-center"
                                scope="row"
                              >
                                {{ punti['VELV'][0]['48']['17'] }}
                              </td>
                              <td
                                class="text-center"
                                scope="row"
                              >
                                1
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Andam. Montagna
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['VELV']['19'].classes_values"
                                  :value="analisibulletin.w17_classes['VELV']['32']['19'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['VELV']['19'].classes_values"
                                  :value="meteobulletins[0].w05_classes['VELV']['48']['19'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-center"
                                scope="row"
                              >
                                {{ punti['VELV'][0]['48']['19'] }}
                              </td>
                              <td
                                class="text-center"
                                scope="row"
                              >
                                1
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Rinforzi
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['VELV']['20'].classes_values"
                                  :value="analisibulletin.w17_classes['VELV']['32']['20'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['VELV']['20'].classes_values"
                                  :value="meteobulletins[0].w05_classes['VELV']['48']['20'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-center"
                                scope="row"
                              >
                                {{ punti['VELV'][0]['48']['20'] }}
                              </td>
                              <td
                                class="text-center"
                                scope="row"
                              >
                                1
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Venti di foehn
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['VELV']['21'].classes_values"
                                  :value="analisibulletin.w17_classes['VELV']['32']['21'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['VELV']['21'].classes_values"
                                  :value="meteobulletins[0].w05_classes['VELV']['48']['21'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-center"
                                scope="row"
                              >
                                {{ punti['VELV'][0]['48']['21'] }}
                              </td>
                              <td
                                class="text-center"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                          </tbody>
                        </table>
                        <table class="table">
                          <thead>
                            <tr>
                              <th
                                class="text-center"
                                colspan="3"
                              >
                                PUNTEGGIO TOTALE
                              </th>
                            </tr>
                            <tr>
                              <th
                                class="text-center"
                                colspan="1"
                              >
                                Ottenuti
                              </th>
                              <th
                                class="text-center"
                                colspan="1"
                              >
                                Totali
                              </th>
                              <th
                                class="text-center"
                                colspan="1"
                              >
                                Relativo %
                              </th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td
                                class="text-center"
                                scope="row"
                              >
                                {{ parziali[0] }}
                              </td>
                              <td
                                class="text-center"
                                scope="row"
                              >
                                56
                              </td>
                              <th
                                class="text-center"
                                scope="row"
                                style="background-color: #05e173;"
                              >
                                {{ verifica.w17_verifica_data_set[0].punteggio_relativo }}
                              </th>
                            </tr>
                          </tbody>
                        </table>
                      </div>
                    </div>
                    <div class="col-xl-5 col-md-12 mb-3">
                      <div
                        class="sticky-top pt-5"
                        style="z-index: 0;"
                      />
                    </div> <!-- col -->
                  </div>

                  <div
                    id="pills-verifica24"
                    class="tab-pane fade"
                    role="tabpanel"
                    aria-labelledby="pills-verifica24-tab"
                  >
                    <div class="row">
                      <div class="col-sm">
                        <table class="table">
                          <thead>
                            <tr>
                              <th
                                class="text-left"
                              />
                              <th
                                class="text-left"
                              >
                                Osservata 
                              </th>
                              <th
                                class="text-left"
                              >
                                Prevista 
                              </th>
                              <th
                                class="text-left"
                              >
                                Punti 
                              </th>
                              <th
                                class="text-left"
                              >
                                Max 
                              </th>
                            </tr>
                            <tr>
                              <th
                                class="text-left"
                                colspan="5"
                              >
                                Nuvolosità Mattino
                              </th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Classe nubi
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['COP_TOT']['1'].classes_values"
                                  :value="analisibulletin.w17_classes['COP_TOT']['30']['1'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['COP_TOT']['1'].classes_values"
                                  :value="meteobulletins[1].w05_classes['COP_TOT']['64']['1'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['COP_TOT'][1]['64']['1'] }} 
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Evoluzione
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['COP_TOT']['2'].classes_values"
                                  :value="analisibulletin.w17_classes['COP_TOT']['30']['2'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['COP_TOT']['2'].classes_values"
                                  :value="meteobulletins[1].w05_classes['COP_TOT']['64']['2'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['COP_TOT'][1]['64']['2'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Visibilità
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['COP_TOT']['4'].classes_values"
                                  :value="analisibulletin.w17_classes['COP_TOT']['30']['4'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['COP_TOT']['4'].classes_values"
                                  :value="meteobulletins[1].w05_classes['COP_TOT']['64']['4'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['COP_TOT'][1]['64']['4'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Localizzazione/Coerenza
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              />
                              <td
                                class="text-left"
                                scope="row"
                              />
                              <td
                                class="text-left"
                                scope="row"
                              >
                                <input
                                  id="coerenza_mattino_nubi24"
                                  style="width: 5em;background-color: #eecbda;"
                                  :readonly="readonly"
                                  type="number"
                                  min="0"
                                  max="2"
                                  class="form-control"
                                  name="coerenza_mattino_nubi24"
                                  :value="Number(verifica.w17_verifica_data_set[1].coerenza_mattino_nubi)"
                                  @change="saveCoerenza($event.target.value, verifica.w17_verifica_data_set[1].id_w17_verifica_data, 'coerenza_mattino_nubi')"
                                >
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                          </tbody>
                        </table>
                        <table class="table">
                          <thead>
                            <tr>
                              <th
                                class="text-left"
                                colspan="5"
                              >
                                Precipitazioni Mattino
                              </th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Classe su Regione
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['PLUV']['5'].classes_values"
                                  :value="analisibulletin.w17_classes['PLUV']['30']['5'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['PLUV']['5'].classes_values"
                                  :value="meteobulletins[1].w05_classes['PLUV']['64']['5'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['PLUV'][1]['64']['5'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Classe su Area
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['PLUV']['6'].classes_values"
                                  :value="analisibulletin.w17_classes['PLUV']['30']['6'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['PLUV']['6'].classes_values"
                                  :value="meteobulletins[1].w05_classes['PLUV']['64']['6'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['PLUV'][1]['64']['6'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Classe massimo
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['PLUV']['7'].classes_values"
                                  :value="analisibulletin.w17_classes['PLUV']['30']['7'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['PLUV']['7'].classes_values"
                                  :value="meteobulletins[1].w05_classes['PLUV']['64']['7'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['PLUV'][1]['64']['7'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Nuvolosità
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['PLUV']['8'].classes_values"
                                  :value="analisibulletin.w17_classes['PLUV']['30']['8'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['PLUV']['8'].classes_values"
                                  :value="meteobulletins[1].w05_classes['PLUV']['64']['8'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['PLUV'][1]['64']['8'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Localizzazione/Coerenza
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              />
                              <td
                                class="text-left"
                                scope="row"
                              />
                              <td
                                class="text-left"
                                scope="row"
                              >
                                <input
                                  id="coerenza_pomeriggio_pioggia24"
                                  style="width: 5em;background-color: #eecbda;"
                                  :readonly="readonly"
                                  type="number"
                                  min="0"
                                  max="2"
                                  class="form-control"
                                  name="coerenza_pomeriggio_pioggia24"
                                  :value="Number(verifica.w17_verifica_data_set[1].coerenza_mattino_pioggia)"
                                  @change="saveCoerenza($event.target.value, verifica.w17_verifica_data_set[1].id_w17_verifica_data, 'coerenza_mattino_pioggia')"
                                >
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                          </tbody>
                        </table>
                        <table class="table">
                          <thead>
                            <tr>
                              <th
                                class="text-left"
                                colspan="5"
                              >
                                Zero Termico
                              </th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Valore 00-24
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.w17_data['FRZLVL']['32']['0'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[1].w05_data['FRZLVL']['66']['0'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['FRZLVL'][1]['66']['data'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Andamento 00-24
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['FRZLVL']['13'].classes_values"
                                  :value="analisibulletin.w17_classes['FRZLVL']['32']['13'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['FRZLVL']['13'].classes_values"
                                  :value="meteobulletins[1].w05_classes['FRZLVL']['66']['13'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['FRZLVL'][1]['66']['13'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                1
                              </td>
                            </tr>
                          </tbody>
                        </table>
                        <table class="table">
                          <thead>
                            <tr>
                              <th
                                class="text-left"
                                colspan="5"
                              >
                                Temperatura
                              </th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Scarto minima
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                                colspan="2"
                              >
                                {{ scarto_temp['TERMA'][1]['67']['scarto'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['TERMA'][1]['67']['data67'] }}  
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Scarto massima
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                                colspan="2"
                              >
                                {{ scarto_temp['TERMA'][1]['68']['scarto'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['TERMA'][1]['68']['data68'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                andam.minima
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['TERMA']['9'].classes_values"
                                  :value="analisibulletin.w17_classes['TERMA']['34']['9'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['TERMA']['9'].classes_values"
                                  :value="meteobulletins[1].w05_classes['TERMA']['68']['9'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['TERMA'][1]['68']['9'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                andam.massima
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['TERMA']['10'].classes_values"
                                  :value="analisibulletin.w17_classes['TERMA']['33']['10'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['TERMA']['10'].classes_values"
                                  :value="meteobulletins[1].w05_classes['TERMA']['67']['10'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['TERMA'][1]['67']['10'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                          </tbody>
                        </table>
                        <table class="table">
                          <tbody>
                            <tr>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                MIN
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                AL
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                AT
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                BI
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                CN
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                NO
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                TO
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                VB
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                VC
                              </th>	
                            </tr>
                            <tr>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                OSS
                              </th>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['34']['9'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['34']['11'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['34']['1'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['34']['28'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['34']['33'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['34']['59'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['34']['63'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['34']['64'].numeric_value) }}
                              </td>
                            </tr>
                            <tr>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                FOR
                              </th>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[1].rearrangemeteoterma['TERMA']['68']['9'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[1].rearrangemeteoterma['TERMA']['68']['11'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[1].rearrangemeteoterma['TERMA']['68']['1'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[1].rearrangemeteoterma['TERMA']['68']['28'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[1].rearrangemeteoterma['TERMA']['68']['33'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[1].rearrangemeteoterma['TERMA']['68']['59'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[1].rearrangemeteoterma['TERMA']['68']['63'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[1].rearrangemeteoterma['TERMA']['68']['64'].numeric_value) }}
                              </td>
                            </tr>
                          </tbody>
                        </table>                       
                        <table class="table">
                          <tbody>
                            <tr>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                MAX
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                AL
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                AT
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                BI
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                CN
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                NO
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                TO
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                VB
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                VC
                              </th>	
                            </tr>
                            <tr>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                OSS
                              </th>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['33']['9'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['33']['11'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['33']['1'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['33']['28'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['33']['33'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['33']['59'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['33']['63'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['33']['64'].numeric_value) }}
                              </td>
                            </tr>
                            <tr>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                FOR
                              </th>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[1].rearrangemeteoterma['TERMA']['67']['9'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[1].rearrangemeteoterma['TERMA']['67']['11'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[1].rearrangemeteoterma['TERMA']['67']['1'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[1].rearrangemeteoterma['TERMA']['67']['28'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[1].rearrangemeteoterma['TERMA']['67']['33'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[1].rearrangemeteoterma['TERMA']['67']['59'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[1].rearrangemeteoterma['TERMA']['67']['63'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[1].rearrangemeteoterma['TERMA']['67']['64'].numeric_value) }}
                              </td>
                            </tr>
                          </tbody>
                        </table>
                      </div>                    
                      <div class="col-sm">
                        <table class="table">
                          <thead>
                            <tr>
                              <th
                                class="text-left"
                              />
                              <th
                                class="text-left"
                              >
                                Osservata 
                              </th>
                              <th
                                class="text-left"
                              >
                                Prevista 
                              </th>
                              <th
                                class="text-left"
                              >
                                Punti 
                              </th>
                              <th
                                class="text-left"
                              >
                                Max 
                              </th>
                            </tr>
                            <tr>
                              <th
                                class="text-left"
                                colspan="5"
                              >
                                Nuvolosità Pomeriggio
                              </th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Classe nubi
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['COP_TOT']['1'].classes_values"
                                  :value="analisibulletin.w17_classes['COP_TOT']['31']['1'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['COP_TOT']['1'].classes_values"
                                  :value="meteobulletins[1].w05_classes['COP_TOT']['65']['1'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['COP_TOT'][1]['65']['1'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Evoluzione
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['COP_TOT']['2'].classes_values"
                                  :value="analisibulletin.w17_classes['COP_TOT']['31']['2'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['COP_TOT']['2'].classes_values"
                                  :value="meteobulletins[1].w05_classes['COP_TOT']['65']['2'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['COP_TOT'][1]['65']['2'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Visibilità
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['COP_TOT']['4'].classes_values"
                                  :value="analisibulletin.w17_classes['COP_TOT']['31']['4'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['COP_TOT']['4'].classes_values"
                                  :value="meteobulletins[1].w05_classes['COP_TOT']['65']['4'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['COP_TOT'][1]['65']['4'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Localizzazione/Coerenza
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              />
                              <td
                                class="text-left"
                                scope="row"
                              />
                              <td
                                class="text-left"
                                scope="row"
                              >
                                <input
                                  id="coerenza_pomeriggio_nubi24"
                                  style="width: 5em;background-color: #eecbda;"
                                  :readonly="readonly"
                                  type="number"
                                  min="0"
                                  max="2"
                                  class="form-control"
                                  name="coerenza_pomeriggio_nubi24"
                                  :value="Number(verifica.w17_verifica_data_set[1].coerenza_pomeriggio_nubi)"
                                  @change="saveCoerenza($event.target.value, verifica.w17_verifica_data_set[1].id_w17_verifica_data, 'coerenza_pomeriggio_nubi')"
                                >
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                          </tbody>
                        </table>
                        <table class="table">
                          <thead>
                            <tr>
                              <th
                                class="text-left"
                                colspan="5"
                              >
                                Precipitazioni Pomeriggio
                              </th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Classe su Regione
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['PLUV']['5'].classes_values"
                                  :value="analisibulletin.w17_classes['PLUV']['30']['5'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['PLUV']['5'].classes_values"
                                  :value="meteobulletins[1].w05_classes['PLUV']['65']['5'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['PLUV'][1]['65']['5'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Classe su Area
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['PLUV']['6'].classes_values"
                                  :value="analisibulletin.w17_classes['PLUV']['30']['6'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['PLUV']['6'].classes_values"
                                  :value="meteobulletins[1].w05_classes['PLUV']['65']['6'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['PLUV'][1]['65']['6'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Classe massimo
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['PLUV']['7'].classes_values"
                                  :value="analisibulletin.w17_classes['PLUV']['30']['7'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['PLUV']['7'].classes_values"
                                  :value="meteobulletins[1].w05_classes['PLUV']['65']['7'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['PLUV'][1]['65']['7'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Nuvolosità
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['PLUV']['8'].classes_values"
                                  :value="analisibulletin.w17_classes['PLUV']['30']['8'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['PLUV']['8'].classes_values"
                                  :value="meteobulletins[1].w05_classes['PLUV']['65']['8'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['PLUV'][1]['65']['8'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Localizzazione/Coerenza
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              />
                              <td
                                class="text-left"
                                scope="row"
                              />
                              <td
                                class="text-left"
                                scope="row"
                              >
                                <input
                                  id="coerenza_pomeriggio_pioggia24"
                                  style="width: 5em;background-color: #eecbda;"
                                  :readonly="readonly"
                                  type="number"
                                  min="0"
                                  max="2"
                                  class="form-control"
                                  name="coerenza_pomeriggio_pioggia24"
                                  :value="Number(verifica.w17_verifica_data_set[1].coerenza_pomeriggio_pioggia)"
                                  @change="saveCoerenza($event.target.value, verifica.w17_verifica_data_set[1].id_w17_verifica_data, 'coerenza_pomeriggio_pioggia')"
                                >
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                          </tbody>
                        </table>
                        <table class="table">
                          <thead>
                            <tr>
                              <th
                                class="text-left"
                                colspan="5"
                              >
                                Quota Neve
                              </th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Quota neve min
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.w17_data['SNOW_LEV']['32']['1'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[1].w05_data['SNOW_LEV']['66']['0'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['SNOW_LEV'][1]['66']['min'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                1
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                quota neve max
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.w17_data['SNOW_LEV']['32']['0'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[1].w05_data['SNOW_LEV']['66']['0'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['SNOW_LEV'][1]['66']['max'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                1
                              </td>
                            </tr>
                          </tbody>
                        </table>
                        <table class="table">
                          <thead>
                            <tr>
                              <th
                                class="text-left"
                                colspan="5"
                              >
                                Venti
                              </th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Intensità pianura
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['VELV']['16'].classes_values"
                                  :value="analisibulletin.w17_classes['VELV']['32']['16'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['VELV']['16'].classes_values"
                                  :value="meteobulletins[1].w05_classes['VELV']['66']['16'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['VELV'][1]['66']['16'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Intensità montagna
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['VELV']['18'].classes_values"
                                  :value="analisibulletin.w17_classes['VELV']['32']['18'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['VELV']['18'].classes_values"
                                  :value="meteobulletins[1].w05_classes['VELV']['66']['18'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['VELV'][1]['66']['18'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Andam. pianura
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['VELV']['17'].classes_values"
                                  :value="analisibulletin.w17_classes['VELV']['32']['17'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['VELV']['17'].classes_values"
                                  :value="meteobulletins[1].w05_classes['VELV']['66']['17'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['VELV'][1]['66']['17'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                1
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Andam. Montagna
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['VELV']['19'].classes_values"
                                  :value="analisibulletin.w17_classes['VELV']['32']['19'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['VELV']['19'].classes_values"
                                  :value="meteobulletins[1].w05_classes['VELV']['66']['19'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['VELV'][1]['66']['19'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                1
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Rinforzi
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['VELV']['20'].classes_values"
                                  :value="analisibulletin.w17_classes['VELV']['32']['20'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['VELV']['20'].classes_values"
                                  :value="meteobulletins[1].w05_classes['VELV']['66']['20'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['VELV'][1]['66']['20'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                1
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Venti di foehn
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['VELV']['21'].classes_values"
                                  :value="analisibulletin.w17_classes['VELV']['32']['21'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['VELV']['21'].classes_values"
                                  :value="meteobulletins[1].w05_classes['VELV']['66']['21'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['VELV'][1]['66']['21'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                          </tbody>
                        </table>
                        <table class="table">
                          <thead>
                            <tr>
                              <th
                                class="text-center"
                                colspan="3"
                              >
                                PUNTEGGIO TOTALE
                              </th>
                            </tr>
                            <tr>
                              <th
                                class="text-center"
                                colspan="1"
                              >
                                Ottenuti
                              </th>
                              <th
                                class="text-center"
                                colspan="1"
                              >
                                Totali
                              </th>
                              <th
                                class="text-center"
                                colspan="1"
                              >
                                Relativo %
                              </th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td
                                class="text-center"
                                scope="row"
                              >
                                {{ parziali[1] }}
                              </td>
                              <td
                                class="text-center"
                                scope="row"
                              >
                                56
                              </td>
                              <th
                                class="text-center"
                                scope="row"
                                style="background-color: #05e173;"
                              >
                                {{ verifica.w17_verifica_data_set[1].punteggio_relativo }}
                              </th>
                            </tr>
                          </tbody>
                        </table>
                      </div>
                    </div>
                    <div class="col-xl-5 col-md-12 mb-3">
                      <div
                        class="sticky-top pt-5"
                        style="z-index: 0;"
                      />
                    </div> <!-- col -->
                  </div>
                  <div
                    id="pills-verifica48"
                    class="tab-pane fade"
                    role="tabpanel"
                    aria-labelledby="pills-verifica48-tab"
                  >
                    <div class="row">
                      <div class="col-sm">
                        <table class="table">
                          <thead>
                            <tr>
                              <th
                                class="text-left"
                              />
                              <th
                                class="text-left"
                              >
                                Osservata 
                              </th>
                              <th
                                class="text-left"
                              >
                                Prevista 
                              </th>
                              <th
                                class="text-left"
                              >
                                Punti 
                              </th>
                              <th
                                class="text-left"
                              >
                                Max 
                              </th>
                            </tr>
                            <tr>
                              <th
                                class="text-left"
                                colspan="5"
                              >
                                Nuvolosità Mattino
                              </th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Classe nubi
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['COP_TOT']['1'].classes_values"
                                  :value="analisibulletin.w17_classes['COP_TOT']['30']['1'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['COP_TOT']['1'].classes_values"
                                  :value="meteobulletins[2].w05_classes['COP_TOT']['81']['1'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['COP_TOT'][2]['81']['1'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Evoluzione
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['COP_TOT']['2'].classes_values"
                                  :value="analisibulletin.w17_classes['COP_TOT']['30']['2'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['COP_TOT']['2'].classes_values"
                                  :value="meteobulletins[2].w05_classes['COP_TOT']['81']['2'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['COP_TOT'][2]['81']['2'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Visibilità
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['COP_TOT']['4'].classes_values"
                                  :value="analisibulletin.w17_classes['COP_TOT']['30']['4'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['COP_TOT']['4'].classes_values"
                                  :value="meteobulletins[2].w05_classes['COP_TOT']['81']['4'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['COP_TOT'][2]['81']['4'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Localizzazione/Coerenza
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              />
                              <td
                                class="text-left"
                                scope="row"
                              />
                              <td
                                class="text-left"
                                scope="row"
                              >
                                <input
                                  id="coerenza_mattino_nubi48"
                                  style="width: 5em;background-color: #eecbda;"
                                  :readonly="readonly"
                                  type="number"
                                  min="0"
                                  max="2"
                                  class="form-control"
                                  name="coerenza_mattino_nubi48"
                                  :value="Number(verifica.w17_verifica_data_set[2].coerenza_mattino_nubi)"
                                  @change="saveCoerenza($event.target.value, verifica.w17_verifica_data_set[2].id_w17_verifica_data, 'coerenza_mattino_nubi')"
                                >
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                          </tbody>
                        </table>
                        <table class="table">
                          <thead>
                            <tr>
                              <th
                                class="text-left"
                                colspan="5"
                              >
                                Precipitazioni Mattino
                              </th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Classe su Regione
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['PLUV']['5'].classes_values"
                                  :value="analisibulletin.w17_classes['PLUV']['30']['5'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['PLUV']['5'].classes_values"
                                  :value="meteobulletins[2].w05_classes['PLUV']['81']['5'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['PLUV'][2]['81']['5'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Classe su Area
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['PLUV']['6'].classes_values"
                                  :value="analisibulletin.w17_classes['PLUV']['30']['6'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['PLUV']['6'].classes_values"
                                  :value="meteobulletins[2].w05_classes['PLUV']['81']['6'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['PLUV'][2]['81']['6'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Classe massimo
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['PLUV']['7'].classes_values"
                                  :value="analisibulletin.w17_classes['PLUV']['30']['7'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['PLUV']['7'].classes_values"
                                  :value="meteobulletins[2].w05_classes['PLUV']['81']['7'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['PLUV'][2]['81']['7'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Nuvolosità
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['PLUV']['8'].classes_values"
                                  :value="analisibulletin.w17_classes['PLUV']['30']['8'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['PLUV']['8'].classes_values"
                                  :value="meteobulletins[2].w05_classes['PLUV']['81']['8'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['PLUV'][2]['81']['8'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Localizzazione/Coerenza
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              />
                              <td
                                class="text-left"
                                scope="row"
                              />
                              <td
                                class="text-left"
                                scope="row"
                              >
                                <input
                                  id="coerenza_mattino_pioggia48"
                                  style="width: 5em;background-color: #eecbda;"
                                  :readonly="readonly"
                                  type="number"
                                  min="0"
                                  max="2"
                                  class="form-control"
                                  name="coerenza_mattino_pioggia48"
                                  :value="Number(verifica.w17_verifica_data_set[2].coerenza_mattino_nubi)"
                                  @change="saveCoerenza($event.target.value, verifica.w17_verifica_data_set[2].id_w17_verifica_data, 'coerenza_mattino_pioggia')"
                                >
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                          </tbody>
                        </table>
                        <table class="table">
                          <thead>
                            <tr>
                              <th
                                class="text-left"
                                colspan="5"
                              >
                                Zero Termico
                              </th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Valore 00-24
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.w17_data['FRZLVL']['32']['0'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[2].w05_data['FRZLVL']['83']['0'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['FRZLVL'][2]['83']['data'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Andamento 00-24
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['FRZLVL']['13'].classes_values"
                                  :value="analisibulletin.w17_classes['FRZLVL']['32']['13'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['FRZLVL']['13'].classes_values"
                                  :value="meteobulletins[2].w05_classes['FRZLVL']['83']['13'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['FRZLVL'][2]['83']['13'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                1
                              </td>
                            </tr>
                          </tbody>
                        </table>
                        <table class="table">
                          <thead>
                            <tr>
                              <th
                                class="text-left"
                                colspan="5"
                              >
                                Temperatura
                              </th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Scarto minima
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                                colspan="2"
                              >
                                {{ scarto_temp['TERMA'][2]['85']['scarto'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['TERMA'][2]['85']['data85'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Scarto massima
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                                colspan="2"
                              >
                                {{ scarto_temp['TERMA'][2]['84']['scarto'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['TERMA'][2]['84']['data84'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                andam.minima
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['TERMA']['9'].classes_values"
                                  :value="analisibulletin.w17_classes['TERMA']['34']['9'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['TERMA']['9'].classes_values"
                                  :value="meteobulletins[2].w05_classes['TERMA']['85']['9'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['TERMA'][2]['85']['9'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                andam.massima
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['TERMA']['10'].classes_values"
                                  :value="analisibulletin.w17_classes['TERMA']['33']['10'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['TERMA']['10'].classes_values"
                                  :value="meteobulletins[2].w05_classes['TERMA']['84']['10'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['TERMA'][2]['84']['10'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                          </tbody>
                        </table>
                        <table class="table">
                          <tbody>
                            <tr>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                MIN
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                AL
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                AT
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                BI
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                CN
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                NO
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                TO
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                VB
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                VC
                              </th>	
                            </tr>
                            <tr>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                OSS
                              </th>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['34']['9'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['34']['11'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['34']['1'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['34']['28'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['34']['33'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['34']['59'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['34']['63'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['34']['64'].numeric_value) }}
                              </td>
                            </tr>
                            <tr>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                FOR
                              </th>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[2].rearrangemeteoterma['TERMA']['85']['9'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[2].rearrangemeteoterma['TERMA']['85']['11'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[2].rearrangemeteoterma['TERMA']['85']['1'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[2].rearrangemeteoterma['TERMA']['85']['28'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[2].rearrangemeteoterma['TERMA']['85']['33'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[2].rearrangemeteoterma['TERMA']['85']['59'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[2].rearrangemeteoterma['TERMA']['85']['63'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[2].rearrangemeteoterma['TERMA']['85']['64'].numeric_value) }}
                              </td>
                            </tr>
                          </tbody>
                        </table>                       
                        <table class="table">
                          <tbody>
                            <tr>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                MAX
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                AL
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                AT
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                BI
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                CN
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                NO
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                TO
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                VB
                              </th>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                VC
                              </th>	
                            </tr>
                            <tr>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                OSS
                              </th>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['33']['9'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['33']['11'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['33']['1'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['33']['28'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['33']['33'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['33']['59'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['33']['63'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.rearrangeanalisiterma['TERMA']['33']['64'].numeric_value) }}
                              </td>
                            </tr>
                            <tr>
                              <th
                                class="text-left"
                                scope="row"
                              >
                                FOR
                              </th>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[2].rearrangemeteoterma['TERMA']['84']['9'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[2].rearrangemeteoterma['TERMA']['84']['11'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[2].rearrangemeteoterma['TERMA']['84']['1'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[2].rearrangemeteoterma['TERMA']['84']['28'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[2].rearrangemeteoterma['TERMA']['84']['33'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[2].rearrangemeteoterma['TERMA']['84']['59'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[2].rearrangemeteoterma['TERMA']['84']['63'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[2].rearrangemeteoterma['TERMA']['84']['64'].numeric_value) }}
                              </td>
                            </tr>
                          </tbody>
                        </table>
                      </div>                    
                      <div class="col-sm">
                        <table class="table">
                          <thead>
                            <tr>
                              <th
                                class="text-left"
                              />
                              <th
                                class="text-left"
                              >
                                Osservata 
                              </th>
                              <th
                                class="text-left"
                              >
                                Prevista 
                              </th>
                              <th
                                class="text-left"
                              >
                                Punti 
                              </th>
                              <th
                                class="text-left"
                              >
                                Max 
                              </th>
                            </tr>
                            <tr>
                              <th
                                class="text-left"
                                colspan="5"
                              >
                                Nuvolosità Pomeriggio
                              </th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Classe nubi
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              > 
                                <TableCell
                                  :meteoclasses="meteoclasses['COP_TOT']['1'].classes_values"
                                  :value="analisibulletin.w17_classes['COP_TOT']['31']['1'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['COP_TOT']['1'].classes_values"
                                  :value="meteobulletins[2].w05_classes['COP_TOT']['82']['1'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['COP_TOT'][2]['82']['1'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Evoluzione
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['COP_TOT']['2'].classes_values"
                                  :value="analisibulletin.w17_classes['COP_TOT']['31']['2'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['COP_TOT']['2'].classes_values"
                                  :value="meteobulletins[2].w05_classes['COP_TOT']['82']['2'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['COP_TOT'][2]['82']['2'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Visibilità
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['COP_TOT']['4'].classes_values"
                                  :value="analisibulletin.w17_classes['COP_TOT']['31']['4'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['COP_TOT']['4'].classes_values"
                                  :value="meteobulletins[2].w05_classes['COP_TOT']['82']['4'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['COP_TOT'][2]['82']['4'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Localizzazione/Coerenza
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              />
                              <td
                                class="text-left"
                                scope="row"
                              />
                              <td
                                class="text-left"
                                scope="row"
                              >
                                <input
                                  id="coerenza_pomeriggio_nubi48"
                                  style="width: 5em;background-color: #eecbda;"
                                  :readonly="readonly"
                                  type="number"
                                  min="0"
                                  max="2"
                                  class="form-control"
                                  name="coerenza_pomeriggio_nubi48"
                                  :value="Number(verifica.w17_verifica_data_set[2].coerenza_pomeriggio_nubi)"
                                  @change="saveCoerenza($event.target.value, verifica.w17_verifica_data_set[2].id_w17_verifica_data, 'coerenza_pomeriggio_nubi')"
                                >
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                          </tbody>
                        </table>
                        <table class="table">
                          <thead>
                            <tr>
                              <th
                                class="text-left"
                                colspan="5"
                              >
                                Precipitazioni Pomeriggio
                              </th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Classe su Regione
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['PLUV']['5'].classes_values"
                                  :value="analisibulletin.w17_classes['PLUV']['30']['5'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['PLUV']['5'].classes_values"
                                  :value="meteobulletins[2].w05_classes['PLUV']['82']['5'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['PLUV'][2]['82']['5'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Classe su Area
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['PLUV']['6'].classes_values"
                                  :value="analisibulletin.w17_classes['PLUV']['30']['6'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['PLUV']['6'].classes_values"
                                  :value="meteobulletins[2].w05_classes['PLUV']['82']['6'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['PLUV'][2]['82']['6'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Classe massimo
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['PLUV']['7'].classes_values"
                                  :value="analisibulletin.w17_classes['PLUV']['30']['7'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['PLUV']['7'].classes_values"
                                  :value="meteobulletins[2].w05_classes['PLUV']['82']['7'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['PLUV'][2]['82']['7'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Nuvolosità
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['PLUV']['8'].classes_values"
                                  :value="analisibulletin.w17_classes['PLUV']['30']['8'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['PLUV']['8'].classes_values"
                                  :value="meteobulletins[2].w05_classes['PLUV']['82']['8'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['PLUV'][2]['82']['8'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Localizzazione/Coerenza
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              />
                              <td
                                class="text-left"
                                scope="row"
                              />
                              <td
                                class="text-left"
                                scope="row"
                              >
                                <input
                                  id="coerenza_pomeriggio_pioggia48"
                                  style="width: 5em;background-color: #eecbda;"
                                  :readonly="readonly"
                                  type="number"
                                  min="0"
                                  max="2"
                                  class="form-control"
                                  name="coerenza_pomeriggio_pioggia48"
                                  :value="Number(verifica.w17_verifica_data_set[2].coerenza_pomeriggio_pioggia)"
                                  @change="saveCoerenza($event.target.value, verifica.w17_verifica_data_set[2].id_w17_verifica_data, 'coerenza_pomeriggio_pioggia')"
                                >
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                          </tbody>
                        </table>
                        <table class="table">
                          <thead>
                            <tr>
                              <th
                                class="text-left"
                                colspan="5"
                              >
                                Quota Neve
                              </th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Quota neve min
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.w17_data['SNOW_LEV']['32']['1'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[2].w05_data['SNOW_LEV']['83']['1'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['SNOW_LEV'][2]['83']['min'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                1
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                quota neve max
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(analisibulletin.w17_data['SNOW_LEV']['32']['0'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ Math.round(meteobulletins[2].w05_data['SNOW_LEV']['83']['0'].numeric_value) }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['SNOW_LEV'][2]['83']['max'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                1
                              </td>
                            </tr>
                          </tbody>
                        </table>
                        <table class="table">
                          <thead>
                            <tr>
                              <th
                                class="text-left"
                                colspan="5"
                              >
                                Venti
                              </th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Intensità pianura
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['VELV']['16'].classes_values"
                                  :value="analisibulletin.w17_classes['VELV']['32']['16'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['VELV']['16'].classes_values"
                                  :value="meteobulletins[2].w05_classes['VELV']['83']['16'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['VELV'][2]['83']['16'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Intensità montagna
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['VELV']['18'].classes_values"
                                  :value="analisibulletin.w17_classes['VELV']['32']['18'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['VELV']['18'].classes_values"
                                  :value="meteobulletins[2].w05_classes['VELV']['83']['18'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['VELV'][2]['83']['18'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Andam. pianura
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['VELV']['17'].classes_values"
                                  :value="analisibulletin.w17_classes['VELV']['32']['17'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['VELV']['17'].classes_values"
                                  :value="meteobulletins[2].w05_classes['VELV']['83']['17'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['VELV'][2]['83']['17'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                1
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Andam. Montagna
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['VELV']['19'].classes_values"
                                  :value="analisibulletin.w17_classes['VELV']['32']['19'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['VELV']['19'].classes_values"
                                  :value="meteobulletins[2].w05_classes['VELV']['83']['19'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['VELV'][2]['83']['19'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                1
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Rinforzi
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['VELV']['20'].classes_values"
                                  :value="analisibulletin.w17_classes['VELV']['32']['20'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['VELV']['20'].classes_values"
                                  :value="meteobulletins[2].w05_classes['VELV']['83']['20'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['VELV'][2]['83']['20'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                1
                              </td>
                            </tr>
                            <tr>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                Venti di foehn
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['VELV']['21'].classes_values"
                                  :value="analisibulletin.w17_classes['VELV']['32']['21'].id_classes_value"
                                />
                              </td>
                              <td
                                style="line-height:2em;"
                                class="text-left"
                                scope="row"
                              >
                                <TableCell
                                  :meteoclasses="meteoclasses['VELV']['21'].classes_values"
                                  :value="meteobulletins[2].w05_classes['VELV']['83']['21'].id_classes_value"
                                />
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                {{ punti['VELV'][2]['83']['21'] }}
                              </td>
                              <td
                                class="text-left"
                                scope="row"
                              >
                                2
                              </td>
                            </tr>
                          </tbody>
                        </table>
                        <table class="table">
                          <thead>
                            <tr>
                              <th
                                class="text-center"
                                colspan="3"
                              >
                                PUNTEGGIO TOTALE
                              </th>
                            </tr>
                            <tr>
                              <th
                                class="text-center"
                                colspan="1"
                              >
                                Ottenuti
                              </th>
                              <th
                                class="text-center"
                                colspan="1"
                              >
                                Totali
                              </th>
                              <th
                                class="text-center"
                                colspan="1"
                              >
                                Relativo %
                              </th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td
                                class="text-center"
                                scope="row"
                              >
                                {{ parziali[2] }}
                              </td>
                              <td
                                class="text-center"
                                scope="row"
                              >
                                56
                              </td>
                              <th
                                class="text-center"
                                scope="row"
                                style="background-color: #05e173;"
                              >
                                {{ verifica.w17_verifica_data_set[2].punteggio_relativo }}
                              </th>
                            </tr>
                          </tbody>
                        </table>
                      </div>
                    </div>
                    <div class="col-xl-5 col-md-12 mb-3">
                      <div
                        class="sticky-top pt-5"
                        style="z-index: 0;"
                      />
                    </div> <!-- col -->
                  </div>
                  <div
                    id="pills-statistica"
                    class="tab-pane fade"
                    role="tabpanel"
                    aria-labelledby="pills-statistica-tab"
                  >
                    <div class="col-md-12 mb-3">
                      <table class="table">
                        <thead>
                          <tr>
                            <th
                              class="text-center"
                              colspan="1"
                            />
                            <th
                              class="text-left"
                              colspan="1"
                            >
                              Nuvolosità
                            </th>
                            <th
                              class="text-left"
                              colspan="1"
                            >
                              Precipitazione
                            </th>
                            <th
                              class="text-left"
                              colspan="1"
                            >
                              Zero termico/Quota Neve
                            </th>
                            <th
                              class="text-left"
                              colspan="1"
                            >
                              Temperatura
                            </th>
                            <th
                              class="text-left"
                              colspan="1"
                            >
                              Venti
                            </th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr
                            v-for="area in verifica.w17_verifica_data_set"
                            :key="area.id_w17_verifica_data"
                          >
                            <th scope="row">
                              Verifica + {{ area.forecast_id }}
                            </th>
                            <th scope="row">
                              {{ area.punteggio_nubi }}
                            </th>
                            <th scope="row">
                              {{ area.punteggio_pioggia }}
                            </th>
                            <th scope="row">
                              {{ area.punteggio_zero_quota_neve }}
                            </th>
                            <th scope="row">
                              {{ area.punteggio_temperatura }}
                            </th>
                            <th scope="row">
                              {{ area.punteggio_vento }}
                            </th>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                    <div class="col-xl-5 col-md-12 mb-3">
                      <div
                        class="sticky-top pt-5"
                        style="z-index: 0;"
                      />
                    </div> <!-- col -->
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
export default {
  name: 'VerificaBulletin',
}
</script>

<script setup lang="ts">
import { Ref, ref, onMounted, computed, nextTick, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useToast } from 'vue-toast-notification'

import api from '../../src/api'
import store from '../../src/store'

import { components } from '../../src/types/weboll'

import TableCell from "./TableCell.vue"

const router = useRouter()
const route = useRoute()
const toast = useToast()

type W17verificaFull = components['schemas']['W17verifica'] & { w17_verifica_data_set: components['schemas']['W17verificaData'][] }
type W05Full = components['schemas']['W05'] &  
  { w05data_set: W05Data[] } & 
  { w05classes_set: W05Classes[] }

type W05Classes = components['schemas']['W05Classes']
type W05Data = components['schemas']['W05Data']

type W05ClassesExt = W05Classes & {classes_values: {} }
type MeteoClasses = {
    "COP_TOT": {[index: number]: W05ClassesExt},
    "FRZLVL":{[index: number]: W05ClassesExt},
    "PLUV":{[index: number]: W05ClassesExt},
    "TERMA":{[index: number]: W05ClassesExt},
    "VELV":{[index: number]: W05ClassesExt}
}


type W05FullRearranged = W05Full & {w05_classes?: any, w05_data?: any, rearrangemeteoterma?: any}
type ArrayTransformer = (arr: Array<any>) => any

// reactive properties
let verifica_id = ref(NaN)
let verifica: Ref<W17verificaFull> = ref({"id_w17verifica":2,"w17_verifica_data_set":[{"id_w17_verifica_data":25,"id_w05":4955,"data_forecast":"2023-06-07","forecast_id":12,"punteggio_relativo":0,"punteggio_nubi":0,"punteggio_pioggia":0,"punteggio_vento":0,"punteggio_temperatura":0,"punteggio_zero_quota_neve":0,"coerenza_mattino_nubi":0,"coerenza_pomeriggio_nubi":0,"coerenza_mattino_pioggia":0,"coerenza_pomeriggio_pioggia":0,"id_w17verifica":2},{"id_w17_verifica_data":26,"id_w05":4955,"data_forecast":"2023-06-06","forecast_id":24,"punteggio_relativo":0,"punteggio_nubi":0,"punteggio_pioggia":0,"punteggio_vento":0,"punteggio_temperatura":0,"punteggio_zero_quota_neve":0,"coerenza_mattino_nubi":0,"coerenza_pomeriggio_nubi":0,"coerenza_mattino_pioggia":0,"coerenza_pomeriggio_pioggia":0,"id_w17verifica":2},{"id_w17_verifica_data":27,"id_w05":4955,"data_forecast":"2023-06-05","forecast_id":48,"punteggio_relativo":0,"punteggio_nubi":0,"punteggio_pioggia":0,"punteggio_vento":0,"punteggio_temperatura":0,"punteggio_zero_quota_neve":0,"coerenza_mattino_nubi":0,"coerenza_pomeriggio_nubi":0,"coerenza_mattino_pioggia":0,"coerenza_pomeriggio_pioggia":0,"id_w17verifica":2}],"data_analysis":"2023-06-07","data_emissione":"2023-06-08","next_blt_time":"2023-06-09","last_update":"2023-06-08T09:21:59","username":"aliccoop","status":"0"})
let state = ref(store.state)
let ready = ref(false)
let readonly = ref(true)
let meteobulletins: Ref<Array<W05FullRearranged>> = ref([])
let analisibulletin = ref({
  "id_w17":3384,
  "w17data_set":[],
  "data_analysis":"2023-06-05",
  "data_emissione":"2023-06-06",
  "next_blt_time":"2023-06-07",
  "situation":"Un'area di bassa...",
  "cloudiness":"...",
  "weather_code":"20",
  "last_update":"2023-06-06T09:14:06",
  "username":"",
  "status":"1",
  "numero_bollettino":"157/2023",
  "id_w17_parent":null,
  "w17_classes":{},
  "w17_data":{},
  "rearrangeanalisiterma":{}
  })
//let meteoclasses: Ref<MeteoClasses> = ref()
let meteoclasses: Ref<MeteoClasses> = ref({
    "COP_TOT": {},
    "FRZLVL":{},
    "PLUV":{},
    "TERMA":{},
    "VELV":{}
})
let today = ref('')

let countfetch = ref(0)
let actions = ref({
  sending:false,
})
//tl del meteo da filtrare
const meteo_time_layouts = [[48,50,51],[64,65,66,67,68],[81,82,83,84,85]]
//tl del analisi da filtrare
const analisi_time_layouts = [30,31,32,33,34]
//corrispondenze tra tl meteo e analisi generiche
const corrispondenzegenerale = {
  '48':'31',
  '50':'33',
  '51':'34',
  '64':'30',
  '65':'31',
  '66':'32',
  '67':'33',
  '68':'34',
  '81':'30',
  '82':'31',
  '83':'32',
  '84':'33',
  '85':'34'
}

//corrispondenze tra tl meteo e analisi dello zero termico
const corrispondenzezerotermico = {
  '48':'31',
  '66':'32',
  '83':'32',
}

//corrispondenze tra tl meteo e analisi dei venti
const corrispondenzeventi = {
  '48':'32',
  '66':'32',
  '83':'32',
}

//aspetto che l'evento si verifichi per iniziare
watch(() => countfetch, async (new_value) => {
  //trovo i dati dei bollettini meteo
  if(new_value.value > 2){
    // metodo per ordinarli dal più nuovo al più vecchio
    meteobulletins.value.sort((a,b) => a.id_w05 > b.id_w05 ? -1 : 1)
    let index = 0
    meteobulletins.value.forEach(meteobulletin => {
      //console.log(meteobulletin.id_w05)
      // codice per filtrare meteo dati
      meteobulletin.w05data_set=meteobulletin.w05data_set.filter((e: { id_time_layouts: number })=>meteo_time_layouts[index].includes(e.id_time_layouts))
      meteobulletin.w05data_set=meteobulletin.w05data_set.filter((e: { id_parametro: string })=> e.id_parametro === 'TERMA' || e.id_parametro === 'SNOW_LEV' || e.id_parametro === 'FRZLVL')
      // codice per filtrare meteo classes
      meteobulletin.w05classes_set=meteobulletin.w05classes_set.filter((e: { id_time_layouts: number })=>meteo_time_layouts[index].includes(e.id_time_layouts))
      meteobulletin.w05classes_set=meteobulletin.w05classes_set.filter((e: { id_parametro: string })=> e.id_parametro !== 'SNOW_LEV')
      // codice per riarranggiare meteo classes
      let rearrangemeteoclasses = rearrange(
      meteobulletin.w05classes_set,
        "id_parametro",
        pippo=>rearrange(pippo, "id_time_layouts", 
        pippo2=>rearrange(pippo2, "id_classes", (arr: any[]) => arr[0] ))
      )
      // codice per riarranggiare meteo dati
      let rearrangemeteodata = rearrange(
      meteobulletin.w05data_set,
        "id_parametro",
        pippo=>rearrange(pippo, "id_time_layouts", (arr: any[]) => arr)
      )
      // Assegnazione del riarrangiamento
      meteobulletin['w05_classes']=rearrangemeteoclasses
      meteobulletin['w05_data']=rearrangemeteodata
      // codice per riarranggiare meteo terma per id_venue
      let rearrangemeteoterma = rearrange(
        meteobulletin.w05data_set,
        "id_parametro",
        pippo=>rearrange(pippo, "id_time_layouts", 
        pippo2=>rearrange(pippo2, "id_venue", (arr: any[]) => arr[0] ))
      )
      // Assegnazione del riarrangiamento
      meteobulletin['rearrangemeteoterma']=rearrangemeteoterma
      // delete meteobulletin.w05classes_set
      // delete meteobulletin.w05data_set
      index += 1
    })
    // se è la prima volta che creo "X" aggiorno i punteggi che altrimenti non conosco e metto staus =0
    if(verifica.value.status === "X"){
      await nextTick()
      checkPunteggi()
      let payload = {}
      payload['status'] = "0"
      payload['id_w17verifica'] = verifica.value.id_w17verifica
      bulkUpdateW17verifica(payload).then((response) => {
        if (!response.ok) {
          toast.open(
            {
              message: 'Errore nel salvataggio',
              type: 'error',
              position: 'top-left'
            }
          )
        }
        return response.json()
      }).then(data => {
        toast.open(
          {
            message: 'Dato salvato',
            type: 'success',
            position: 'top-left'
          }
        )
        verifica.value.status = "0"
        verifica.value.last_update = data.last_update
        verifica.value.username = (store.state.username || "")
        ready.value = true
      }).catch((error) => {
        toast.open(
          {
            message: `Errore di comunicazione: ${error}`,
            type: 'error',
            position: 'top-left'
          }
        )
      })
    }else{
      ready.value = true
    }  
  }
},{ deep: true })

// variabile computed per calcolare lo scarto delle temperature
const scarto_temp = computed(() => {
  let tmp = {}
  for(const param in meteoclasses.value){
    tmp[param] = {}
    for(let tab = 0; tab < 3; tab ++){
      tmp[param][tab] = {}
      for( const tl in meteobulletins.value[tab].w05_classes[param]){
        tmp[param][tab][tl] = {}
      }
    }
  }

  for(let tab = 0; tab < 3; tab ++){
    for(const param in meteobulletins.value[tab].w05_data){
      for(const tl in meteobulletins.value[tab].w05_data[param]){
        if(param === 'TERMA'){
          if(meteobulletins.value[tab].w05_data[param][tl] && analisibulletin.value.w17_data[param][corrispondenzegenerale[tl]]){
            let scartopr = 0
            for(let i = 0; i<meteobulletins.value[tab].w05_data[param][tl].length; i++){
              if(meteobulletins.value[tab].w05_data[param][tl][i].id_venue !== 67){
                let meteo = meteobulletins.value[tab].w05_data[param][tl][i]
                let analisi = analisibulletin.value.w17_data[param][corrispondenzegenerale[tl]].find(e => e.id_venue === meteo.id_venue)
                scartopr += Math.abs(parseInt(meteo.numeric_value) - parseInt(analisi.numeric_value))                
              }
            }
            
            let scarto = Math.round(scartopr/8)
            tmp[param][tab][tl]['scarto'] = tab === 0 ? 0 : scarto
          }
        }
      }
    }
  }
  return tmp
})

// metodo per calcolare i punteggi delle singole classi e dei dati 
const punti = computed(() => {
  let tmp = {}
  for(const param in meteoclasses.value){
    tmp[param] = {}
    tmp['SNOW_LEV'] = {}
    for(let tab = 0; tab < 3; tab ++){
      tmp[param][tab] = {}
      tmp['SNOW_LEV'][tab] = {}
      for( const tl in meteobulletins.value[tab].w05_classes[param]){
        tmp[param][tab][tl] = {}
        tmp['SNOW_LEV'][tab][tl] = {}
        for(const classe in meteoclasses.value[param]){
          let value = 0
          if(param === 'COP_TOT' || param === 'PLUV' || param ==='TERMA'){
            if(analisibulletin.value.w17_classes[param][corrispondenzegenerale[tl]] && meteobulletins.value[tab].w05_classes[param][tl][classe]){
              let meteovalue = meteobulletins.value[tab].w05_classes[param][tl][classe].id_classes_value
              let analisivalue = analisibulletin.value.w17_classes[param][corrispondenzegenerale[tl]][classe].id_classes_value
              let abs = Math.abs(meteovalue - analisivalue)
              if(abs === 0){
                value = 2
              }else if(abs === 1) {
                value = 1
              }
              tmp[param][tab][tl][classe] = tab === 0 && param === 'TERMA' ? 0 : value 
            }
          }else if (param ==='FRZLVL'){
            if(analisibulletin.value.w17_classes[param][corrispondenzezerotermico[tl]] && meteobulletins.value[tab].w05_classes[param][tl][classe]){
              let meteovalue = meteobulletins.value[tab].w05_classes[param][tl][classe].id_classes_value
              let analisivalue = analisibulletin.value.w17_classes[param][corrispondenzezerotermico[tl]][classe].id_classes_value
              let abs = Math.abs(meteovalue - analisivalue)
              if(abs === 0){
                value = 1
              }
              tmp[param][tab][tl][classe] = value
            }

          }if(param === 'VELV'){
            if(analisibulletin.value.w17_classes[param][corrispondenzeventi[tl]] && meteobulletins.value[tab].w05_classes[param][tl][classe]){
              let meteovalue = meteobulletins.value[tab].w05_classes[param][tl][classe].id_classes_value
              let analisivalue = analisibulletin.value.w17_classes[param][corrispondenzeventi[tl]][classe].id_classes_value
              let abs = Math.abs(meteovalue - analisivalue)
              if(['17','19','20'].includes(classe)){
                if(abs === 0){
                  value = 1
                }
              }else{
                if(abs === 0){
                  value = 2
                }else if(abs === 1) {
                  value = 1
                }
              }
              tmp[param][tab][tl][classe] = value
            }
          }  
        }
      }
    }
  }

  
  for(let tab = 0; tab < 3; tab ++){
    for(const param in meteobulletins.value[tab].w05_data){
      for(const tl in meteobulletins.value[tab].w05_data[param]){
        let value = 0
        if(param === 'FRZLVL'){
          if(meteobulletins.value[tab].w05_data[param][tl] && analisibulletin.value.w17_data[param][corrispondenzezerotermico[tl]]){
            let meteovalue = parseInt(meteobulletins.value[tab].w05_data[param][tl][0].numeric_value)
            let analisivalue = parseInt(analisibulletin.value.w17_data[param][corrispondenzezerotermico[tl]][0].numeric_value)
            let abs = Math.abs(meteovalue - analisivalue)
            if(abs <= 100){
              value = 2
            }else if(abs <= 200) {
              value = 1
            }
            tmp[param][tab][tl]['data'] = value
          }
        }
        if(param === 'TERMA'){
          if(meteobulletins.value[tab].w05_data[param][tl] && analisibulletin.value.w17_data[param][corrispondenzegenerale[tl]]){
            let scartopr = 0
            for(let i = 0; i<meteobulletins.value[tab].w05_data[param][tl].length; i++){
              if(meteobulletins.value[tab].w05_data[param][tl][i].id_venue !== 67){
                let meteo = meteobulletins.value[tab].w05_data[param][tl][i]
                let analisi = analisibulletin.value.w17_data[param][corrispondenzegenerale[tl]].find(e => e.id_venue === meteo.id_venue)
                scartopr += Math.abs(parseInt(meteo.numeric_value) - parseInt(analisi.numeric_value))                
              }
            }
            
            let scarto = Math.round(scartopr/8)
            if(scarto <= 1){
              value = 2
            }else if (scarto <= 2){
              value = 1
            }
            tmp[param][tab][tl]['data' + tl] = tab === 0 ? 0 : value
          }
        }
        if(param === 'SNOW_LEV'){
          if(meteobulletins.value[tab].w05_data[param][tl] && analisibulletin.value.w17_data[param][corrispondenzeventi[tl]]){
            let meteomin = meteobulletins.value[tab].w05_data[param][tl].find(e => e.id_aggregazione = 910).numeric_value
            let analisimin= analisibulletin.value.w17_data[param][corrispondenzeventi[tl]].find(e => e.id_aggregazione = 324).numeric_value
            let meteomax = meteobulletins.value[tab].w05_data[param][tl].find(e => e.id_aggregazione = 909).numeric_value
            let analisimax= analisibulletin.value.w17_data[param][corrispondenzeventi[tl]].find(e => e.id_aggregazione = 323).numeric_value
            let absmin = Math.abs(meteomin - analisimin)
            let absmax = Math.abs(meteomax - analisimax)
            //console.log(absmin, absmax)
            if(absmin <= 300){
              value = 1
            }
            tmp[param][tab][tl]['min'] = value
            value = 0
            if(absmax <= 300){
              value = 1
            }
            tmp[param][tab][tl]['max'] = value
          }
        }
      }
    }
  }
  return tmp
})

//Inizio punteggio classe nubi
// punteggio parziale nubi totale
const punteggio_nubi = computed(() => {
  let punteggio_nubi = [0, 0, 0]

  for(const tab in punti.value['COP_TOT']){
    let sum = 0
    for(const tl in punti.value['COP_TOT'][tab]){
      for(const classe in punti.value['COP_TOT'][tab][tl]){
        if(['1', '2', '4'].includes(classe)){
          sum += punti.value['COP_TOT'][tab][tl][classe]
        }
      }
    }
    sum += verifica.value.w17_verifica_data_set[tab].coerenza_mattino_nubi + verifica.value.w17_verifica_data_set[tab].coerenza_pomeriggio_nubi
    punteggio_nubi[tab] = sum
  }

  return punteggio_nubi
})

// punteggio parziale nubi Classe nubi
const punteggio_classe_nubi = computed(() => {
  let punteggio_classe_nubi = [0, 0, 0]

  for(const tab in punti.value['COP_TOT']){
    let sum = 0
    for(const tl in punti.value['COP_TOT'][tab]){
      sum += punti.value['COP_TOT'][tab][tl]['1']
    }
    punteggio_classe_nubi[tab] = sum
  }

  return punteggio_classe_nubi
})

// punteggio parziale nubi evoluzione
const punteggio_evoluzione = computed(() => {
  let punteggio_evoluzione = [0, 0, 0]

  for(const tab in punti.value['COP_TOT']){
    let sum = 0
    for(const tl in punti.value['COP_TOT'][tab]){
      sum += punti.value['COP_TOT'][tab][tl]['2']
    }
    punteggio_evoluzione[tab] = sum
  }

  return punteggio_evoluzione
})

// punteggio parziale nubi Visibilità
const punteggio_visibilita = computed(() => {
  let punteggio_visibilita = [0, 0, 0]

  for(const tab in punti.value['COP_TOT']){
    let sum = 0
    for(const tl in punti.value['COP_TOT'][tab]){
      sum += punti.value['COP_TOT'][tab][tl]['4']
    }
    punteggio_visibilita[tab] = sum
  }

  return punteggio_visibilita
})
//fine punteggio classe nubi

//Inizio punteggio classe Pioggia
// punteggio parziale pioggia totale
const punteggio_pioggia = computed(() => {
  let punteggio_pioggia = [0, 0, 0]

  for(const tab in punti.value['PLUV']){
    let sum = 0
    for(const tl in punti.value['PLUV'][tab]){
      for(const classe in punti.value['PLUV'][tab][tl]){
        sum += punti.value['PLUV'][tab][tl][classe]
      }
    }
    sum += verifica.value.w17_verifica_data_set[tab].coerenza_mattino_pioggia + verifica.value.w17_verifica_data_set[tab].coerenza_pomeriggio_pioggia
    punteggio_pioggia[tab] = sum
  }
  return punteggio_pioggia
})
//Fine punteggio classe Pioggia

//Inizio punteggio classe Temperatura
// punteggio parziale temperatura
const punteggio_temperatura = computed(() => {
  let punteggio_temperatura = [0, 0, 0]

  for(const tab in punti.value['TERMA']){
    let sum = 0
    for(const tl in punti.value['TERMA'][tab]){
      for(const classe in punti.value['TERMA'][tab][tl]){
        sum += punti.value['TERMA'][tab][tl][classe]
      }
    }
    punteggio_temperatura[tab] = sum
  }
  
  return punteggio_temperatura
})
//fine punteggio classe Temperatura

//Inizio punteggio classe quota neve
// punteggio parziale quota neve
const punteggio_zero_quota_neve = computed(() => {
  let punteggio_zero_quota_neve = [0, 0, 0]

  for(const tab in punti.value['FRZLVL']){
    let sum = 0
    for(const tl in punti.value['FRZLVL'][tab]){
      if(['48', '66', '83'].includes(tl)){
        for(const classe in punti.value['FRZLVL'][tab][tl]){
          sum += punti.value['FRZLVL'][tab][tl][classe]
        }
      }
    }
    punteggio_zero_quota_neve[tab] = sum
  }

  for(const tab in punti.value['SNOW_LEV']){
    let sum = punteggio_zero_quota_neve[tab]
    for(const tl in punti.value['SNOW_LEV'][tab]){
      if(['48', '66', '83'].includes(tl)){
        for(const classe in punti.value['SNOW_LEV'][tab][tl]){
          sum += punti.value['SNOW_LEV'][tab][tl][classe]
        }
      }
    }
    punteggio_zero_quota_neve[tab] = sum
  }

  return punteggio_zero_quota_neve

})
//Fine punteggio classe quota neve
// Inizio punteggio classe Venti
// punteggio parziale venti
const punteggio_vento = computed(() => {
  let punteggio_vento = [0, 0, 0]

  for(const tab in punti.value['VELV']){
    let sum = 0
    for(const tl in punti.value['VELV'][tab]){
      for(const classe in punti.value['VELV'][tab][tl]){
        sum += punti.value['VELV'][tab][tl][classe]
      }
    }
    punteggio_vento[tab] = sum
  }

  return punteggio_vento
})
// punteggio parziale vento foehn
const punteggio_foehn = computed(() => {
  let punteggio_foehn = [0, 0, 0]

  for(const tab in punti.value['VELV']){
    let sum = 0
    for(const tl in punti.value['VELV'][tab]){
      sum += punti.value['VELV'][tab][tl]['21']
    }
    punteggio_foehn[tab] = sum
  }
  console.log('punteggio_foehn',punteggio_foehn)
  return punteggio_foehn
})
// Fine punteggio classe Venti
/*
TAB 0
    3*(classeNubiMax + evolNubiMax) +
    localizzazioneNubiNubiMax + //è sempre 0 
    2*(visibilitaMax + precRegioneMax + precAreaMax + precMassimoMax + precEvolMax + coerenzaNubiMax + coerenzaPioggiaMax)+
    intensitaPianuraMax +
    andamVentoPianuraMax +
    intensitaMontagnaMax +
    andamVentoMontagnaMax +
    rinforziVentoMax + 
    2*(foehnMax) +
    zeroTPomeriggioMax +
    snowLevMinMax +
    snowLevMaxMax +
    andamZeroTPomeriggioMax
		
TAB 1 - 2
    2*(classeNubiPuntiMattino[1]+evolNubiPuntiMattino[1]) +
    locNubiPuntiMattino[1]+visibilitaPuntiMattino[1]+
		2*(classeNubiPuntiPomeriggio[1]+evolNubiPuntiPomeriggio[1])+
    locNubiPuntiPomeriggio[1]+
    visibilitaPuntiPomeriggio[1]+
				precRegionePuntiMattino[1]+ 
        precAreaPuntiMattino[1]+ 
        precMassimoPuntiMattino[1]+ 
        precEvolPuntiMattino[1]+
				precRegionePuntiPomeriggio[1]+
        precAreaPuntiPomeriggio[1]+
        precMassimoPuntiPomeriggio[1]+
        precEvolPuntiPomeriggio[1]+
				coerenzaMattinoNubi[1]+
        coerenzaMattinoPioggia[1]+
        coerenzaPomeriggioNubi[1]+
        coerenzaPomeriggioPioggia[1]+
				andamZeroTPuntiGiorno[1]+
        valoreZeroTPuntiGiorno[1]+
				valoreQuotaNeveMinPunti[1]+
        valoreQuotaNeveMaxPunti[1]+
				valoreTminPunti[1]+ 
        valoreTmaxPunti[1]+ 
        andamTminPunti[1]+
        andamTmaxPunti[1]+
				intensitaPianuraPunti[1]+
        intensitaMontagnaPunti[1]+
        andamVentoPianuraPunti[1]+
				andamVentoMontagnaPunti[1]+
        rinforziVentoPunti[1]+
        2*(foehnPunti[1])
*/
const parziali = computed(() => {
  let parziali = [0, 0, 0]

  for(let tab=0; tab<3; tab++){
    if(tab === 0){
      parziali[tab] = Math.round(
      3 * (punteggio_classe_nubi.value[tab] + punteggio_evoluzione.value[tab])
      + 2 * (punteggio_visibilita.value[tab] + punteggio_pioggia.value[tab] + verifica.value.w17_verifica_data_set[tab].coerenza_pomeriggio_nubi)
      + (punteggio_vento.value[tab] - punteggio_foehn.value[tab])
      + 2 * punteggio_foehn.value[tab]
      + punteggio_zero_quota_neve.value[tab]
      + punteggio_temperatura.value[tab])
    }else{
      parziali[tab] = Math.round(
      2 * (punteggio_classe_nubi.value[tab] + punteggio_evoluzione.value[tab])
      + (punteggio_visibilita.value[tab] + punteggio_pioggia.value[tab] + verifica.value.w17_verifica_data_set[tab].coerenza_mattino_nubi + verifica.value.w17_verifica_data_set[tab].coerenza_pomeriggio_nubi)
      + (punteggio_vento.value[tab] - punteggio_foehn.value[tab])
      + 2 * punteggio_foehn.value[tab]
      + punteggio_zero_quota_neve.value[tab]
      + punteggio_temperatura.value[tab])
    }
  }

  return parziali
})

const statistica_nubi = computed(() => {
  let statistica_nubi = [0,0,0]
  
  for(let tab=0; tab<3; tab++){
    const max_nubi = tab === 0 ? 8 : 16
    let value = Math.round((punteggio_nubi.value[tab]/max_nubi)*100)
    statistica_nubi[tab] = value
  }

  return statistica_nubi
})

const statistica_pioggia = computed(() => {
  let statistica_pioggia = [0,0,0]
  
  for(let tab=0; tab<3; tab++){
    const max_pioggia = tab === 0 ? 10 : 20
    let value = Math.round((punteggio_pioggia.value[tab]/max_pioggia)*100)
    statistica_pioggia[tab] = value
  }

  return statistica_pioggia
})

const statistica_zero = computed(() => {
  let statistica_zero = [0,0,0]
  
  for(let tab=0; tab<3; tab++){
    const max_zero = 5
    let value = Math.round((punteggio_zero_quota_neve.value[tab]/max_zero)*100)
    statistica_zero[tab] = value
  }

  return statistica_zero

})

const statistica_terma = computed(() => {
  let statistica_terma = [0,0,0]
  
  for(let tab=0; tab<3; tab++){
    const max_terma = 8
    let value = Math.round((punteggio_temperatura.value[tab]/max_terma)*100)
    statistica_terma[tab] = value
  }

  return statistica_terma
})


const statistica_vento = computed(() => {
  let statistica_vento = [0,0,0]
  
  for(let tab=0; tab<3; tab++){
    const max_wind = 9
    let value = Math.round((punteggio_vento.value[tab]/max_wind)*100)
    statistica_vento[tab] = value
  }

  return statistica_vento
})

const punteggio_percentuale = computed(() => {
  let punteggio_percentuale = [0,0,0]
  let max = [56, 68, 68]
  
  for(let tab=0; tab<3; tab++){
    
    punteggio_percentuale[tab] = Math.round(parziali.value[tab]/max[tab] * 100)
  }

  return punteggio_percentuale
})

const punteggio = computed(() => {
  return {
    punteggio_nubi: statistica_nubi.value,
    punteggio_pioggia: statistica_pioggia.value,
    punteggio_zero_quota_neve: statistica_zero.value,
    punteggio_temperatura: statistica_terma.value,
    punteggio_vento: statistica_vento.value,
    punteggio_relativo: punteggio_percentuale.value,
  }
})

//console.log('nuvolosita+++++++++',nuvolosita)

/* 
OSSERVATO CLASSI
Nuvolosità 
classe nubi id_classes=1 id_parametro=cop_tot mattino=30 pomeriggio=31
evoluzione id_classes=2 id_parametro=cop_tot mattino=30 pomeriggio=31
visibilità id_classes=4 id_parametro=cop_tot mattino=30 pomeriggio=31

precipitazione
id_classes=5 id_parametro=PLUV mattino=30 pomeriggio=31
id_classes=6 id_parametro=PLUV mattino=30 pomeriggio=31
id_classes=7 id_parametro=PLUV mattino=30 pomeriggio=31
id_classes=8 id_parametro=PLUV mattino=30 pomeriggio=31

zero termico
id_classes=12 id_parametro=FRZLVL pomeriggio=31 (bollettino 0)
id_classes=13 id_parametro=FRZLVL pomeriggio=32 (bollettino 1,2)

venti
id_classes=16 id_parametro=VELV pomeriggio=32
id_classes=17 id_parametro=VELV pomeriggio=32
id_classes=18 id_parametro=VELV pomeriggio=32
id_classes=19 id_parametro=VELV pomeriggio=32
id_classes=20 id_parametro=VELV pomeriggio=32
id_classes=21 id_parametro=VELV pomeriggio=32

andamento.min
id_classes=9 id_parametro=TERMA id_time_layouts=34
andamento max
id_classes=10 id_parametro=TERMA id_time_layouts=33
*/

onMounted(() => {
  if (typeof route.params.id === 'string') {
    verifica_id.value = parseInt(route.params.id)
  }
  fetchData()
})

async function fetchData() {
  today.value = dateToString(new Date())
  ready.value = false
  // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions
  fetchVerifica(verifica_id.value).then(response => {
    if (!response.ok) {
      toast.open(
        {
          message: `Errore ${response.status} nel recupero del bollettino`,
          type: 'error',
          position: 'top-left'
        }
      )
    }
    return response.json()
  }).then(async data => {
    verifica.value = data
    verifica.value.w17_verifica_data_set.sort((a,b) => a.id_w05 > b.id_w05 ? -1 : 1)
    readonly.value = (verifica.value.status === '1' || !state.value.username)
    const response=await fetchMeteoClasses()
    //meteoclasses.value=await response.json()
    let dataclasses=await response.json()
    dataclasses=dataclasses.filter(d => d.id_parametro !== 'SNOW_LEV')
    let classes = dataclasses.reduce((accumulator, currentValue) => {
      accumulator[currentValue.id_parametro][currentValue.id_classes] = currentValue;
      return accumulator
    }, { COP_TOT: {}, FRZLVL: {}, PLUV: {}, TERMA: {}, VELV: {} })  
    Object.keys(classes).forEach(id_parametro => {
      let cl = classes[id_parametro]
      Object.keys(cl).forEach(index => {
        // get class descriptor array
        let classes_value = cl[index].classes_value
        
        let tmp = {}
        classes_value.forEach(e => {
          tmp[e.id_classes_value] = e
        })

        classes[id_parametro][index]["classes_values"] = tmp
        delete classes[id_parametro][index]["classes_value"]
      })
    })
    meteoclasses.value=classes
    const response1=await fetchAnalisi(verifica.value.data_analysis)
    let analisi=(await response1.json()).results[0]

    //analisibulletin.value=(await response1.json()).results[0]
    // codice per filtrare analisi classes 
    analisi['w17classes_set']=analisi['w17classes_set'].filter((e: { id_time_layouts: number })=>analisi_time_layouts.includes(e.id_time_layouts))
    analisi['w17data_set']=analisi['w17data_set'].filter((e: { id_time_layouts: number })=>analisi_time_layouts.includes(e.id_time_layouts))
    analisi['w17data_set']=analisi['w17data_set'].filter((e: { id_parametro: number })=>['TERMA', 'FRZLVL', 'SNOW_LEV'].includes(e.id_parametro.toString()))
    
    // codice per riarranggiare analisi classes
    let rearrangeanalisiclasses = rearrange(
          analisi['w17classes_set'],
          "id_parametro",
          pippo=>rearrange(pippo, "id_time_layouts", 
          pippo2=>rearrange(pippo2, "id_classes", (arr: any[]) => arr[0] ))
          )
    let rearrangeanalisidata = rearrange(
          analisi['w17data_set'],
          "id_parametro",
          pippo=>rearrange(pippo, "id_time_layouts", (arr: any[]) => arr)
          )
    //console.log('---------analisi ----',analisi)
    analisi['w17_classes']= rearrangeanalisiclasses
    analisi['w17_data'] = rearrangeanalisidata
    let rearrangeanalisiterma = rearrange(
          analisi['w17data_set'],
          "id_parametro",
          pippo=>rearrange(pippo, "id_time_layouts", 
          pippo2=>rearrange(pippo2, "id_venue", (arr: any[]) => arr[0] ))
          )
    delete analisi.w17classes_set
    delete analisi.w17data_set
    analisibulletin.value=analisi
    /**/
    analisi['rearrangeanalisiterma'] = rearrangeanalisiterma
    if (meteobulletins.value.length === 0){
      verifica.value.w17_verifica_data_set.forEach(async (dataset: { id_w05: any })=>{
        try{
          let response=await fetchMeteo(dataset.id_w05)
          const meteobulletin=await response.json()
          meteobulletins.value.push(meteobulletin)
          countfetch.value += 1
        }catch(error)  {
          toast.open(
            {
              message: error,
              type: 'error',
              position: 'top-left'
            }
          )
        }
      })
    }else{
      countfetch.value += 1
    }
  }).catch(error => {
    toast.open(
      {
        message: error,
        type: 'error',
        position: 'top-left'
      }
    )
  })
}

async function fetchVerifica(id: string | number) {
  const response = await fetch('/api/w17verifica/bulletins/' + id + '/', {
    headers: {
      accept: 'application/json'
    }
  })
  return response
}

async function fetchMeteo (meteo_id: string) {
  const response = await fetch('/api/w05/bulletins/' + meteo_id + '/', {
    headers: {
      accept: 'application/json'
    }
  })
  return response
}

async function fetchMeteoClasses () {
  const response = await fetch('/api/w05/classes/', {
    headers: {
      accept: 'application/json'
    }
  })
  return response
}

async function fetchAnalisi (analisi_data: string) {
  const response = await fetch('/api/w17/bulletins_full/?data=' + analisi_data , {
    headers: {
      accept: 'application/json'
    }
  })
  return response
}

function getDateFormatted(rawString: string, time = true) {
  return api.getDateFormatted(rawString, time)
}

function saveW17verifica(newValue: null, id_w17verifica: any, campo: null) {
  const payload = { }
  payload['id_w17verifica'] = id_w17verifica
  payload['username'] = store.state.username
  bulkUpdateW17verifica(payload).then((response) => {
    if (!response.ok) {
      toast.open(
        {
          message: 'Errore nel salvataggio',
          type: 'error',
          position: 'top-left'
        }
      )
    }
    return response.json()
  }).then(data => {
    toast.open(
      {
        message: 'Dato salvato',
        type: 'success',
        position: 'top-left'
      }
    )
    verifica.value.last_update = data.last_update
    verifica.value.username = (store.state.username || "")
  }).catch((error) => {
    toast.open(
      {
        message: `Errore di comunicazione: ${error}`,
        type: 'error',
        position: 'top-left'
      }
    )
  })
}

function checkPunteggi(){
  for(let tab=0; tab<3; tab++){
    for(const p in punteggio.value){
      if(verifica.value.w17_verifica_data_set[tab][p] !== punteggio.value[p][tab]){
        //console.log(punteggio.value[p][tab],verifica.value.w17_verifica_data_set[tab].id_w17_verifica_data, p)
        saveW17verificaData(punteggio.value[p][tab],verifica.value.w17_verifica_data_set[tab].id_w17_verifica_data, p) 
      }
    }
  }
}

function saveCoerenza(newValue: any,id_w17_verifica_data: any,campo: string){
  saveW17verificaData(newValue, id_w17_verifica_data, campo)
  checkPunteggi()
}

function saveW17verificaData(newValue: any,id_w17_verifica_data: any,campo: string) {
  let myIdW17verifica = verifica.value.w17_verifica_data_set.find((w17verificadata: { id_w17_verifica_data: any }) => {
    return w17verificadata.id_w17_verifica_data === id_w17_verifica_data
  })

  if(myIdW17verifica){
    const payload = { }
    myIdW17verifica[campo] = parseInt(newValue)
    payload[campo] = newValue

    fetchPatch(myIdW17verifica.id_w17_verifica_data, 'data', payload).then((response) => {
      if (!response.ok) {
        toast.open(
          {
            message: 'Errore nel salvataggio',
            type: 'error',
            position: 'top-left'
          }
        )
      } else {
        saveW17verifica(null, verifica.value.id_w17verifica, null)
      }
    }).catch((error) => {
      toast.open(
        {
          message: `Errore di comunicazione: ${error}`,
          type: 'error',
          position: 'top-left'
        }
      )
    })
  }
}

function remove() {
  if (
    confirm('Vuoi davvero cancellare questo bollettino?')
  ) {
    api.fetchBulletinDelete(verifica_id.value, 'w17verifica/bulletins', store).then(response => {
      if (response.ok) {
        toast.open(
          {
            message: 'Bollettino cancellato',
            type: 'success',
            position: 'top-left'
          }
        )
        router.back()
      } else {
        toast.open(
          {
            message: `Errore ${response.status} nella cancellazione del bollettino`,
            type: 'error',
            position: 'top-left'
          }
        )
      }
    }).catch(error => {
      toast.open(
        {
          message: error,
          type: 'error',
          position: 'top-left'
        }
      )
    })
  }
}

async function fetchVerificaAction(action: any) {
  const response = await api.fetch_wrapper(
    store.state.access,
    `/api/w17verifica/bulletins/${verifica_id.value}/${action}/`
  )
  return response
}

function execute(action: string, reroute: any, message: any) {
  actions.value[action + 'ing'] = true
  fetchVerificaAction(action).then(response => {
    actions.value[action + 'ing'] = false
    if (response.ok) {
      return response.json()
    } else {
      toast.open(
        {
          message: `Errore ${response.status} nell'esecuzione del comando ${action}`,
          type: 'error',
          position: 'top-left'
        }
      )
    }
  }).then(data => {
    toast.open(
      {
        message: message,
        type: 'success',
        position: 'top-left'
      }
    )
    if (reroute) {
      router.push({ path: `/w17verifica/${data.id_w17verifica}` })
      verifica_id.value = data.id_w17verifica
      fetchData()
    } else {
      fetchData()
    }
  }).catch((error) => {
    this[action + 'ing'] = false
    toast.open(
      {
        message: error,
        type: 'error',
        position: 'top-left'
      }
    )
  })
}

async function fetchPatch(id: any, endpoint: string, payload: {}) {
  const response = await api.fetch_wrapper(
    store.state.access,
    `/api/w17verifica/${endpoint}/${id}/`,
    {
      method: 'PATCH',
      body: JSON.stringify(payload)
    }
  )
  return response
}

async function bulkUpdateW17verifica(payload: {}) {
  const response = await api.fetch_wrapper(
    store.state.access,
    `/api/w17verifica/bulletins/bulk_update/`,
    {
      method: 'POST',
      body: JSON.stringify(payload)
    }
  )
  return response
}

function rearrange(data: any[], key: string, func: ArrayTransformer | null = null) {
//function rearrange(data: any[], key: string, func=null) {
  // rearranges the array data in a dictionary
  // aggregating all records with the same key as an array
  // optionally transforming each array with the func function
  let value_data = {}
  data.forEach((record: { [x: string]: string | number }) => {
    if (!(record[key] in value_data)) {
      value_data[record[key]] = []
    }
    // console.log('rearrange record', record)
    value_data[record[key]].push(record)
  })
  if (func) {
    Object.keys(value_data).forEach(key => value_data[key] = func(value_data[key]))
  }
  if (!Object.values(value_data).some(item => item != undefined)) value_data = {}
  return value_data
}

function dateToString(date){
  const yy = date.getFullYear()
  const mm = date.getMonth() + 1
  const dd = date.getDate()
  return [yy, (mm>9 ? '' : '0') + mm, (dd>9 ? '' : '0') + dd].join('-')
}

</script>
<style scoped>

  table {border: 1px solid;}

  th {max-width: 10px; text-align: left;border: 1px dotted;background-color: rgb(213, 222, 227);}

  td {max-width: 10px; text-align: left;border: 1px dotted;}

</style>