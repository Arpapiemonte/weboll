// Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt
<template>
  <div class="container-fluid">
    <div class="row justify-content-end sticky-top py-1" style="background-color: #f8f9fa;">
      <!-- https://getbootstrap.com/docs/5.1/components/button-group/ -->
      <div class="btn-group w-auto" role="group" aria-label="Basic outlined example">

        <button v-if="verificaallerta.status === '0' && state.username"
          :disabled="sending || verificaallerta.id_numero_bollettino === '0_0'" type="button"
          class="btn btn-outline-success" @click="execute_timeout('send', false, 'Bollettino inviato')">
          <span v-if="sending">
            <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true" />
            Sto inviando il bollettino ...
          </span>
          <span v-else>
            <img src="~bootstrap-icons/icons/send-fill.svg" alt="unlock icon" width="18" height="18"> Invia
          </span>
        </button>
        <button v-if="verificaallerta.status === '0' && state.username" type="button" class="btn btn-outline-danger"
          @click="remove()">
          <img src="~bootstrap-icons/icons/trash-fill.svg" alt="unlock icon" width="18" height="18"> Elimina
        </button>
      </div>
    </div>

    <div class="row mb-3">
      <h1>Bollettino Verifica Allerta {{ verificaallerta.id_w23verifica }}</h1>
      <div v-if="verificaallerta.id_numero_bollettino == '0_0'" class="alert alert-danger">
        <h1>Manca il First guess del Allerta numero {{
          verificaallerta.numero_bollettino.split("/")[0] + '_' + verificaallerta.numero_bollettino.split("/")[1] }}
        </h1>
      </div>
    </div>
    <div class="row">
      <div class="col-md-2 mb-3">
        <label for="status">Stato</label>
        <span v-if="verificaallerta.status == 1">
          <input id="stato" disabled class="form-control" name="stato" type="text" value="Inviato">
        </span>
        <span v-else>
          <input id="stato" disabled class="form-control" name="stato" type="text" value="Bozza">
        </span>
      </div>
      <div class="col-md-2 mb-3">
        <label for="data_emissione">Data emissione Allerta</label>
        <input id="data_emissione" disabled class="form-control" name="data_emissione" type="text"
          :value="getDateFormatted(verificaallerta.data_emissione, time = false)">
      </div>
      <div class="col-md-2 mb-3">
        <label for="data_analisi">Data emissione Verifica Allerta</label>
        <input id="data_analisi" disabled class="form-control" name="data_analisi" type="text"
          :value="getDateFormatted(verificaallerta.data_analisi, time = false)">
      </div>
      <div class="col-md-2 mb-3">
        <label for="ora_emissione">Num bollettino Allerta</label>
        <input id="id_numero_bollettino" :readonly="readonly" class="form-control" name="id_numero_bollettino"
          type="text" :value="verificaallerta.id_numero_bollettino"
          @change="saveW23verifica($event.target.value, verificaallerta.id_w23verifica, 'id_numero_bollettino')">
      </div>

      <div class="col-md-2 mb-3">
        <label for="last_update">Ultima modifica</label>
        <input id="last_update" disabled class="form-control" name="last_update" type="text"
          :value="getDateFormatted(verificaallerta.last_update)">
      </div>
      <div class="col-md-2 mb-3">
        <label for="username">Autore</label>
        <input id="username" disabled class="form-control" name="username" type="text"
          :value="verificaallerta.username">
      </div>
      <div class="row mt-3">
        
        <div class="col-xl-12 col-md-12 mb-3">
          <a href="https://webgis.arpa.piemonte.it/radar/common/webgis_central.php?TYPE=demotime " target="_blank">Osservazioni su IRIS</a>
        </div>
        <div class="col-xl-12 col-md-12 mb-3">
          <ul id="pills-tab" class="nav nav-pills mb-3" role="tablist">
            <li class="nav-item" role="presentation">
              <button id="pills-bollettino_emesso-tab" class="nav-link active" data-bs-toggle="pill"
                data-bs-target="#pills-bollettino_emesso" type="button" role="tab"
                aria-controls="pills-bollettino_emesso" aria-selected="true">
                Massimi Bollettino emesso
              </button>
            </li>
            <li class="nav-item" role="presentation">
              <button id="pills-idrogeologico-tab" class="nav-link" data-bs-toggle="pill"
                data-bs-target="#pills-idrogeologico" type="button" role="tab" aria-controls="pills-idrogeologico"
                aria-selected="false">
                Idrogeologico
              </button>
            </li>
            <li class="nav-item" role="presentation">
              <button id="pills-idraulico-tab" class="nav-link" data-bs-toggle="pill" data-bs-target="#pills-idraulico"
                type="button" role="tab" aria-controls="pills-idraulico" aria-selected="false">
                Idraulico
              </button>
            </li>
            <li class="nav-item" role="presentation">
              <button id="pills-temporali-tab" class="nav-link" data-bs-toggle="pill" data-bs-target="#pills-temporali"
                type="button" role="tab" aria-controls="pills-temporali" aria-selected="false">
                Temporali
              </button>
            </li>
            <li class="nav-item" role="presentation">
              <button id="pills-neve-tab" class="nav-link" data-bs-toggle="pill" data-bs-target="#pills-neve"
                type="button" role="tab" aria-controls="pills-neve" aria-selected="false">
                Neve
              </button>
            </li>
            <li class="nav-item" role="presentation">
              <button id="pills-valanghe-tab" class="nav-link" data-bs-toggle="pill" data-bs-target="#pills-valanghe"
                type="button" role="tab" aria-controls="pills-valanghe" aria-selected="false">
                Valanghe
              </button>
            </li>
            <li class="nav-item" role="presentation">
              <button id="pills-annotazione-tab" class="nav-link" data-bs-toggle="pill"
                data-bs-target="#pills-annotazione" type="button" role="tab" aria-controls="pills-annotazione"
                aria-selected="false">
                Annotazione
              </button>
            </li>
            <li class="nav-item" role="presentation">
              <button id="pills-criteri-tab" class="nav-link" data-bs-toggle="pill" data-bs-target="#pills-criteri"
                type="button" role="tab" aria-controls="pills-criteri" aria-selected="false">
                Criteri
              </button>
            </li>
          </ul>
          <div id="pills-tabContent" class="tab-content">
            <div id="pills-bollettino_emesso" class="tab-pane fade show active" role="tabpanel"
              aria-labelledby="pills-bollettino_emesso-tab">
              <div class="col-xl-12 col-md-12 mb-3">
                <div class="row">
                  <div class="col-md-12 mb-3">
                    <table>
                      <tbody>
                        <tr>
                          <td>
                            <label for="situazione_evoluzione">Situazione ed evoluzione</label><br>
                            <textarea id="situazione_evoluzione" v-model="verificaallerta.situazione_evoluzione"
                              class="form-control" name="situazione_evoluzione" rows="2" cols="200" :readonly="readonly"
                              @change="saveW23verifica(verificaallerta.situazione_evoluzione, verificaallerta.id_w23verifica, 'situazione_evoluzione')" />
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>


                <table class="table table-striped">
                  <thead>
                    <tr>
                      <th class="text-left" colspan="1">
                        ANAGRAFICA
                      </th>
                      <th class="text-left" colspan="1">
                        Criticità Prevista Oggi
                      </th>
                      <th class="text-left" colspan="1">
                        Criticità Osservata Oggi
                      </th>
                      <th class="text-left" colspan="1">
                        Criticità Prevista Domani
                      </th>
                      <th class="text-left" colspan="1">
                        Criticità Osservata Domani
                      </th>
                      <th class="text-left" colspan="1">
                        Criticità Prevista Totale </th>
                      <th class="text-left" colspan="1">
                        Criticità Osservata Totale
                      </th>
                      <th class="text-left" colspan="1">
                        Severità
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="area in verificaallerta.w23verificadata_set" :key="area.id_w23verifica_data">
                      <td>
                        {{ area.id_w23_zone.nome_zona }}
                      </td>
                      <td>
                        <CellCriticita :area="area" :campo="'prev_crit_oggi'" :criticita="criticita" :readonly=true
                          @changeCriticita="saveW23verificaDataSelect" />
                      </td>
                      <td>
                        <CellCriticita :area="area" :campo="'oss_crit_oggi'" :criticita="criticita" :readonly="readonly"
                          @changeCriticita="saveW23verificaDataSelect" />
                      </td>
                      <td>
                        <CellCriticita :area="area" :campo="'prev_crit_domani'" :criticita="criticita" :readonly=true
                          @changeCriticita="saveW23verificaDataSelect" />
                      </td>
                      <td>
                        <CellCriticita :area="area" :campo="'oss_crit_domani'" :criticita="criticita"
                          :readonly="readonly" @changeCriticita="saveW23verificaDataSelect" />
                      </td>
                      <td>
                        <CellCriticita :area="area" :campo="'prev_crit_tot'" :criticita="criticita" :readonly=true
                          @changeCriticita="saveW23verificaDataSelect" />
                      </td>
                      <td>
                        <CellCriticita :area="area" :campo="'oss_crit_tot'" :criticita="criticita" :readonly=true
                          @changeCriticita="saveW23verificaDataSelect" />
                      </td>
                      <td>
                        <CellSeverita :area="area" :campo="'err_crit_tot'" :severita="severita" :readonly=true
                          @changeSeverita="saveW23verificaDataSelect" />
                      </td>
                    </tr>
                  </tbody>
                </table>
                <div class="row">
                  <div class="col-md-12 mb-3">

                    <table>
                      <tbody>
                        <tr>
                          <td>
                            <label for="id_w23giudizio">Giudizio</label><br>
                          </td>
                        </tr>
                        <tr>
                          <CellGiudizio :w23verifica="verificaallerta" :area="verificaallerta" :campo="'id_w23giudizio'"
                            :giudizio="giudizio" :readonly="readonly" @changeGiudizio="saveW23verifica" />
                        </tr>
                      </tbody>
                    </table>
                    <table class="table table-striped">
                      <tbody>
                        <tr>
                          <th style="text-align:center;">
                            Numero Li
                          </th>
                          <th style="text-align:center;">
                            Numero Gr o MGr
                          </th>
                        </tr>
                        <tr>
                          <td style="text-align:center;">
                            {{ gr.num_li }}
                          </td>
                          <td style="text-align:center;">
                            {{ gr.num_mgr_gr }}
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-12 mb-3">
                    <label>Legenda Giudizio</label>
                    <table border=1>
                      <tbody>
                        <tr>
                          <th>
                            Giudizio
                          </th>
                          <th>
                            Valore
                          </th>
                        </tr>
                        <tr>
                          <td bgcolor="#6EBB00">
                            Ottimo
                          </td>
                          <td bgcolor="#6EBB00">
                            1
                          </td>
                        </tr>
                        <tr>
                          <td bgcolor="#6EBB00">
                            Buono
                          </td>
                          <td bgcolor="#6EBB00">
                            2
                          </td>
                        </tr>
                        <tr>
                          <td bgcolor="#ffff00">
                            Sufficiente
                          </td>
                          <td bgcolor="#ffff00">
                            3
                          </td>
                        </tr>
                        <tr>
                          <td bgcolor="#FF0000">
                            Insufficiente
                          </td>
                          <td bgcolor="#FF0000">
                            4
                          </td>
                        </tr>
                        <tr>
                          <td bgcolor="#8f00ff">
                            Pessimo
                          </td>
                          <td bgcolor="#8f00ff">
                            5
                          </td>
                        </tr>
                      </tbody>
                    </table>
                    <label>Legenda Severità</label>
                    <table border=1>
                      <tbody>
                        <tr>
                          <th>
                            Severità
                          </th>
                          <th>
                            Sigla
                          </th>
                          <th>
                            Valore
                          </th>
                        </tr>
                        <tr>
                          <td bgcolor="#6EBB00">
                            1
                          </td>
                          <td bgcolor="#6EBB00">
                            Ok
                          </td>
                          <td bgcolor="#6EBB00">
                            Assenza di errore
                          </td>
                        </tr>
                        <tr>
                          <td bgcolor="#ffff00">
                            2
                          </td>
                          <td bgcolor="#ffff00">
                            Li
                          </td>
                          <td bgcolor="#ffff00">
                            Errore lieve
                          </td>
                        </tr>
                        <tr>
                          <td bgcolor="#FF0000">
                            3
                          </td>
                          <td bgcolor="#FF0000">
                            Gr
                          </td>
                          <td bgcolor="#FF0000">
                            Errore grave
                          </td>
                        </tr>
                        <tr>
                          <td bgcolor="#8f00ff">
                            4
                          </td>
                          <td bgcolor="#8f00ff">
                            MGr
                          </td>
                          <td bgcolor="#8f00ff">
                            Errore molto grave
                          </td>
                        </tr>

                      </tbody>
                    </table>
                  </div>
                </div>
                <div class="col-xl-9 col-md-14 mb-3">
                  <div class="sticky-top pt-5" style="z-index: 0;" />
                </div> <!-- col -->
              </div> <!--col-->
            </div>

            <div id="pills-idrogeologico" class="tab-pane fade" role="tabpanel"
              aria-labelledby="pills-idrogeologico-tab">
              <div class="col-md-12 mb-3">
                <div class="row">
                  <div class="col-md-12 mb-3">
                    <table class="table table-striped">
                      <thead>
                        <tr>
                          <th class="text-left" colspan="1">
                            ANAGRAFICA
                          </th>
                          <th class="text-left" colspan="1">
                            Criticità Prevista Oggi
                          </th>
                          <th class="text-left" colspan="1">
                            Criticità Osservata Oggi
                          </th>
                          <th class="text-left" colspan="1">
                            Criticità Prevista Domani
                          </th>
                          <th class="text-left" colspan="1">
                            Criticità Osservata Domani
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="area in verificaallerta.w23verificadata_set" :key="area.id_w23verifica_data">
                          <td>
                            {{ area.id_w23_zone.nome_zona }}
                          </td>
                          <td>
                            <CellCriticita :area="area" :campo="'prev_crit_idrogeologico_oggi'" :criticita="criticita"
                              :readonly=true @changeCriticita="saveW23verificaDataSelect" />
                          </td>
                          <td>
                            <CellCriticita :area="area" :campo="'oss_crit_idrogeologico_oggi'" :criticita="criticita"
                              :readonly="readonly" @changeCriticita="saveW23verificaDataSelect" />
                          </td>
                          <td>
                            <CellCriticita :area="area" :campo="'prev_crit_idrogeologico_domani'" :criticita="criticita"
                              :readonly=true @changeCriticita="saveW23verificaDataSelect" />
                          </td>
                          <td>
                            <CellCriticita :area="area" :campo="'oss_crit_idrogeologico_domani'" :criticita="criticita"
                              :readonly="readonly" @changeCriticita="saveW23verificaDataSelect" />
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>

            <div id="pills-idraulico" class="tab-pane fade" role="tabpanel" aria-labelledby="pills-idraulico-tab">
              <div class="col-md-12 mb-3">
                <div class="row">
                  <div class="col-md-12 mb-3">
                    <table class="table table-striped">
                      <thead>
                        <tr>
                          <th class="text-left" colspan="1">
                            ANAGRAFICA
                          </th>
                          <th class="text-left" colspan="1">
                            Criticità Prevista Oggi
                          </th>
                          <th class="text-left" colspan="1">
                            Criticità Osservata Oggi
                          </th>
                          <th class="text-left" colspan="1">
                            Criticità Prevista Domani
                          </th>
                          <th class="text-left" colspan="1">
                            Criticità Osservata Domani
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="area in verificaallerta.w23verificadata_set" :key="area.id_w23verifica_data">
                          <td>
                            {{ area.id_w23_zone.nome_zona }}
                          </td>
                          <td>
                            <CellCriticita :area="area" :campo="'prev_crit_idraulico_oggi'" :criticita="criticita"
                              :readonly=true @changeCriticita="saveW23verificaDataSelect" />
                          </td>
                          <td>
                            <CellCriticita :area="area" :campo="'oss_crit_idraulico_oggi'" :criticita="criticita"
                              :readonly="readonly" @changeCriticita="saveW23verificaDataSelect" />
                          </td>
                          <td>
                            <CellCriticita :area="area" :campo="'prev_crit_idraulico_domani'" :criticita="criticita"
                              :readonly=true @changeCriticita="saveW23verificaDataSelect" />
                          </td>
                          <td>
                            <CellCriticita :area="area" :campo="'oss_crit_idraulico_domani'" :criticita="criticita"
                              :readonly="readonly" @changeCriticita="saveW23verificaDataSelect" />
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>

            <div id="pills-temporali" class="tab-pane fade" role="tabpanel" aria-labelledby="pills-temporali-tab">
              <div class="col-md-12 mb-3">
                <div class="row">
                  <div class="col-md-12 mb-3">
                    <table class="table table-striped">
                      <thead>
                        <tr>
                          <th class="text-left" colspan="1">
                            ANAGRAFICA
                          </th>
                          <th class="text-left" colspan="1">
                            Criticità Prevista Oggi
                          </th>
                          <th class="text-left" colspan="1">
                            Criticità Osservata Oggi
                          </th>
                          <th class="text-left" colspan="1">
                            Criticità Prevista Domani
                          </th>
                          <th class="text-left" colspan="1">
                            Criticità Osservata Domani
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="area in verificaallerta.w23verificadata_set" :key="area.id_w23verifica_data">
                          <td>
                            {{ area.id_w23_zone.nome_zona }}
                          </td>
                          <td>
                            <CellCriticita :area="area" :campo="'prev_crit_temporali_oggi'" :criticita="criticita"
                              :readonly=true @changeCriticita="saveW23verificaDataSelect" />
                          </td>
                          <td>
                            <CellCriticita :area="area" :campo="'oss_crit_temporali_oggi'" :criticita="criticita"
                              :readonly="readonly" @changeCriticita="saveW23verificaDataSelect" />
                          </td>
                          <td>
                            <CellCriticita :area="area" :campo="'prev_crit_temporali_domani'" :criticita="criticita"
                              :readonly=true @changeCriticita="saveW23verificaDataSelect" />
                          </td>
                          <td>
                            <CellCriticita :area="area" :campo="'oss_crit_temporali_domani'" :criticita="criticita"
                              :readonly="readonly" @changeCriticita="saveW23verificaDataSelect" />
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>



            <div id="pills-neve" class="tab-pane fade" role="tabpanel" aria-labelledby="pills-neve-tab">
              <div class="col-md-12 mb-3">
                <div class="row">
                  <div class="col-md-12 mb-3">
                    <table class="table table-striped">
                      <thead>
                        <tr>
                          <th class="text-left" colspan="1">
                            ANAGRAFICA
                          </th>
                          <th class="text-left" colspan="1">
                            Criticità Prevista Oggi
                          </th>
                          <th class="text-left" colspan="1">
                            Criticità Osservata Oggi
                          </th>
                          <th class="text-left" colspan="1">
                            Criticità Prevista Domani
                          </th>
                          <th class="text-left" colspan="1">
                            Criticità Osservata Domani
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="area in verificaallerta.w23verificadata_set" :key="area.id_w23verifica_data">
                          <td>
                            {{ area.id_w23_zone.nome_zona }}
                          </td>
                          <td>
                            <CellCriticita :area="area" :campo="'prev_crit_neve_oggi'" :criticita="criticita"
                              :readonly=true @changeCriticita="saveW23verificaDataSelect" />
                          </td>
                          <td>
                            <CellCriticita :area="area" :campo="'oss_crit_neve_oggi'" :criticita="criticita"
                              :readonly="readonly" @changeCriticita="saveW23verificaDataSelect" />
                          </td>
                          <td>
                            <CellCriticita :area="area" :campo="'prev_crit_neve_domani'" :criticita="criticita"
                              :readonly=true @changeCriticita="saveW23verificaDataSelect" />
                          </td>
                          <td>
                            <CellCriticita :area="area" :campo="'oss_crit_neve_domani'" :criticita="criticita"
                              :readonly="readonly" @changeCriticita="saveW23verificaDataSelect" />
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>


            <div id="pills-valanghe" class="tab-pane fade" role="tabpanel" aria-labelledby="pills-valanghe-tab">
              <div class="col-md-12 mb-3">
                <div class="row">
                  <div class="col-md-12 mb-3">
                    <table class="table table-striped">
                      <thead>
                        <tr>
                          <th class="text-left" colspan="1">
                            ANAGRAFICA
                          </th>
                          <th class="text-left" colspan="1">
                            Criticità Prevista Oggi
                          </th>
                          <th class="text-left" colspan="1">
                            Criticità Osservata Oggi
                          </th>
                          <th class="text-left" colspan="1">
                            Criticità Prevista Domani
                          </th>
                          <th class="text-left" colspan="1">
                            Criticità Osservata Domani
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="area in verificaallerta.w23verificadata_set" :key="area.id_w23verifica_data">
                          <td>
                            {{ area.id_w23_zone.nome_zona }}
                          </td>
                          <td>
                            <CellCriticita :area="area" :campo="'prev_crit_valanghe_oggi'" :criticita="criticita"
                              :readonly=true @changeCriticita="saveW23verificaDataSelect" />
                          </td>
                          <td>
                            <CellCriticita :area="area" :campo="'oss_crit_valanghe_oggi'" :criticita="criticita"
                              :readonly="readonly" @changeCriticita="saveW23verificaDataSelect" />
                          </td>
                          <td>
                            <CellCriticita :area="area" :campo="'prev_crit_valanghe_domani'" :criticita="criticita"
                              :readonly=true @changeCriticita="saveW23verificaDataSelect" />
                          </td>
                          <td>
                            <CellCriticita :area="area" :campo="'oss_crit_valanghe_domani'" :criticita="criticita"
                              :readonly="readonly" @changeCriticita="saveW23verificaDataSelect" />
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>


            <div id="pills-annotazione" class="tab-pane fade" role="tabpanel" aria-labelledby="pills-annotazione-tab">
              <div class="col-md-12 mb-3">
                <div class="row">
                  <div class="col-md-12 mb-3">
                    <table>
                      <tbody>
                        <tr>
                          <td>
                            <label for="annotazione">Annotazione</label><br>
                            <textarea id="annotazione" v-model="verificaallerta.annotazione" class="form-control"
                              name="annotazione" rows="2" cols="200" :readonly="readonly"
                              @change="saveW23verifica(verificaallerta.annotazione, verificaallerta.id_w23verifica, 'annotazione')" />
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>

            <div id="pills-criteri" class="tab-pane fade" role="tabpanel" aria-labelledby="pills-criteri-tab">
              <div class="col-md-12 mb-3">
                <div class="row">
                  <div class="col-md-12 mb-3">
                    <table>
                    <thead>
                      <tr>
                        <th style="text-align:center;" colspan=5>Severità</th>
                      </tr>
                      <tr>
                        <th colspan=5>Valutazione gravità Errore</th>
                      </tr>
                    </thead>
                      <tbody>
                      <tr>
                        <td style="background-color: #D6EEEE;"></td>
                        <td style="background-color: #D6EEEE;">Voss</td>
                        <td style="background-color: #D6EEEE;">Goss</td>
                        <td style="background-color: #D6EEEE;">Aoss</td>
                        <td style="background-color: #D6EEEE;">Ross</td>
                      </tr>
                      <tr>
                        <td style="background-color: #D6EEEE;">Vprev</td>
                        <td bgcolor="#6EBB00">Ok</td>
                        <td bgcolor="#ffff00">Li</td>
                        <td bgcolor="#8f00ff">MGr</td>
                        <td bgcolor="#8f00ff">MGr</td>
                      </tr>
                      <tr>
                        <td style="background-color: #D6EEEE;">Gprev</td>
                        <td bgcolor="#ffff00">Li</td>
                        <td bgcolor="#6EBB00">Ok</td>
                        <td bgcolor="#FF0000">Gr</td>
                        <td bgcolor="#8f00ff">MGr</td>
                      </tr>
                      <tr>
                        <td style="background-color: #D6EEEE;">Aprev</td>
                        <td bgcolor="#FF0000">Gr</td>
                        <td bgcolor="#ffff00">Li</td>
                        <td bgcolor="#6EBB00">Ok</td>
                        <td bgcolor="#FF0000">Gr</td>
                      </tr>
                      <tr>
                        <td style="background-color: #D6EEEE;">Rprev</td>
                        <td bgcolor="#8f00ff">MGr</td>
                        <td bgcolor="#8f00ff">MGr</td>
                        <td bgcolor="#FF0000">Gr</td>
                        <td bgcolor="#6EBB00">Ok</td>
                      </tr>
                    </tbody>
                    </table>
                    <table>
                    <thead>
                      <tr>
                        <th style="text-align:center;" colspan=7>Giudizio</th>
                      </tr>
                      <tr>
                        <th></th>
                        <th></th>
                        <th colspan=5>Numero di errori gravi (Gr-MGr)</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td></td>
                        <td></td>
                        <td style="background-color: #D6EEEE; text-align:center;">0</td>
                        <td style="background-color: #D6EEEE; text-align:center;">1</td>
                        <td style="background-color: #D6EEEE; text-align:center;">2-3</td>
                        <td style="background-color: #D6EEEE; text-align:center;">4-6</td>
                        <td style="background-color: #D6EEEE; text-align:center;">7-11</td>
                      </tr>
                      <tr>
                        <td rowspan=4 style="writing-mode: vertical-lr;width: 23px;"><b>Numero di errori lievi (Li)</b>
                        </td>
                        <td style="background-color: #D6EEEE; text-align:center;">0</td>
                        <td style="background-color: #6EBB00; text-align:center;">Ottimo</td>
                        <td style="background-color: #6EBB00; text-align:center;">Buono</td>
                        <td style="background-color: #ffff00; text-align:center;">Sufficiente</td>
                        <td style="background-color: #FF0000; text-align:center;">Insufficiente</td>
                        <td style="background-color: #8f00ff; text-align:center;">Pessimo</td>
                      </tr>
                      <tr>
                        <td style="background-color: #D6EEEE; text-align:center;">1-3</td>
                        <td style="background-color: #6EBB00; text-align:center;">Buono</td>
                        <td style="background-color: #6EBB00; text-align:center;">Buono</td>
                        <td style="background-color: #FF0000; text-align:center;">Insufficiente</td>
                        <td style="background-color: #FF0000; text-align:center;">Insufficiente</td>
                        <td style="background-color: #8f00ff; text-align:center;">Pessimo</td>
                      </tr>
                      <tr>
                        <td style="background-color: #D6EEEE; text-align:center;">4-6</td>
                        <td style="background-color: #ffff00; text-align:center;">Sufficiente</td>
                        <td style="background-color: #ffff00; text-align:center;">Sufficiente</td>
                        <td style="background-color: #FF0000; text-align:center;">Insufficiente</td>
                        <td style="background-color: #8f00ff; text-align:center;">Pessimo</td>
                        <td style="background-color: #8f00ff; text-align:center;">Pessimo</td>
                      </tr>
                      <tr>
                        <td style="background-color: #D6EEEE; text-align:center;">7-11</td>
                        <td style="background-color: #FF0000; text-align:center;">Insufficiente</td>
                        <td style="background-color: #FF0000; text-align:center;">Insufficiente</td>
                        <td style="background-color: #8f00ff; text-align:center;">Pessimo</td>
                        <td style="background-color: #8f00ff; text-align:center;">Pessimo</td>
                        <td style="background-color: #8f00ff; text-align:center;">Pessimo</td>
                      </tr>
                    </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>

          </div>
        </div>
      </div> <!-- row -->
    </div> <!-- end row -->
  </div>
</template>

<script>
import api from '@/api'
import store from '@/store'
import CellGiudizio from './CellGiudizio.vue'
import CellSeverita from './CellSeverita.vue'
import CellCriticita from './CellCriticita.vue'

export default {
  name: 'VerificaAllertaBulletin',
  components: {
    CellGiudizio,
    CellSeverita,
    CellCriticita,
  },
  props: {
    id: {
      type: String,
      default: () => ''
    },
  },
  data() {
    // non reactive properties
    return {
      // reactive properties
      verificaallerta: {
        id_w23verifica: "aaaaaaaa"
      },
      giudizio: [],
      severita: [],
      criticita: [],
      state: store.state,
      readonly: true,
      sending: false,
      saving: false,
    }
  },
  mounted() {
    console.log(`the component is now mounted.`)
  },
  computed: {
    //calcolo massimo osservato
    Verificamassimooss() {
      let vd = {}
      let criticita_dict = {}
      criticita_dict["-"] = -2
      criticita_dict["BIANCO"] = -1
      criticita_dict["VERDE"] = 0
      criticita_dict["GIALLO"] = 1
      criticita_dict["ARANCIONE"] = 2
      criticita_dict["ROSSO"] = 3

      let criticita_dict_inv = {}
      criticita_dict_inv[-2] = "-"
      criticita_dict_inv[-1] = "BIANCO"
      criticita_dict_inv[0] = "VERDE"
      criticita_dict_inv[1] = "GIALLO"
      criticita_dict_inv[2] = "ARANCIONE"
      criticita_dict_inv[3] = "ROSSO"

      if (this.verificaallerta.w23verificadata_set !== undefined) {
        this.verificaallerta.w23verificadata_set.forEach(area => {
          let massimo_domani_str = Math.max(criticita_dict[area.oss_crit_idraulico_domani], criticita_dict[area.oss_crit_idrogeologico_domani], criticita_dict[area.oss_crit_temporali_domani], criticita_dict[area.oss_crit_neve_domani], criticita_dict[area.oss_crit_neve_domani])
          let massimo_oggi_str = Math.max(criticita_dict[area.oss_crit_idraulico_oggi], criticita_dict[area.oss_crit_idrogeologico_oggi], criticita_dict[area.oss_crit_temporali_oggi], criticita_dict[area.oss_crit_neve_oggi], criticita_dict[area.oss_crit_valanghe_oggi])
          let massimo_oggidomani_str = Math.max(massimo_domani_str, massimo_oggi_str);
          let massimo_oggidomani_tot_str = Math.max(criticita_dict[area.oss_crit_oggi], criticita_dict[area.oss_crit_domani]);
          let data = {}
          data['area'] = area.id_w23_zone.id_w23_zone
          data['massimo_oggi'] = criticita_dict_inv[massimo_oggi_str]
          data['massimo_domani'] = criticita_dict_inv[massimo_domani_str]
          data['massimo_oggi_domani'] = criticita_dict_inv[massimo_oggidomani_str]
          data['massimo_oggi_domani_tot'] = criticita_dict_inv[massimo_oggidomani_tot_str]
          vd[area.id_w23_zone.id_w23_zone] = data
        })
      }
      return vd
    },
    //calcolo della severita
    Verificaseverita() {
      let vd = {}
      if (this.verificaallerta.w23verificadata_set !== undefined) {
        this.verificaallerta.w23verificadata_set.forEach(area => {
          let data = {}
          if ((area.oss_crit_tot == area.prev_crit_tot) || (area.oss_crit_tot === '-')) {
            data['severita'] = '1'
          } else if ((area.oss_crit_tot === 'VERDE' && area.prev_crit_tot === 'GIALLO') || (area.oss_crit_tot === 'GIALLO' && area.prev_crit_tot === 'VERDE') || (area.oss_crit_tot === 'GIALLO' && area.prev_crit_tot === 'ARANCIONE')) {
            data['severita'] = '2'
          } else if ((area.oss_crit_tot === 'VERDE' && area.prev_crit_tot === 'ARANCIONE') || (area.oss_crit_tot === 'ARANCIONE' && area.prev_crit_tot === 'GIALLO') || (area.oss_crit_tot === 'ARANCIONE' && area.prev_crit_tot === 'ROSSO') || (area.oss_crit_tot === 'ROSSO' && area.prev_crit_tot === 'ARANCIONE')) {
            data['severita'] = '3'
          } else {
            data['severita'] = '4'
          }
          data['area'] = area.id_w23_zone.id_w23_zone
          vd[area.id_w23_zone.id_w23_zone] = data
        })
      }
      return vd
    },
    //calcolo del giudizio
    gr() {
      let vd = {}
      let giudizio = 0
      let li = 0
      let mgr_gr = 0
      if (this.verificaallerta.w23verificadata_set !== undefined) {
        this.verificaallerta.w23verificadata_set.forEach(area => {
          vd['num_li'] = li
          vd['num_mgr_gr'] = mgr_gr
          if (area.err_crit_tot == 2) {
            li = li + 1
            vd['num_li'] = li
          } else if (area.err_crit_tot == 3) {
            mgr_gr = mgr_gr + 1
            vd['num_mgr_gr'] = mgr_gr
          } else if (area.err_crit_tot == 4) {
            mgr_gr = mgr_gr + 1
            vd['num_mgr_gr'] = mgr_gr
          }
        })
        //costruzione giudizio
        if (mgr_gr === 0 && li === 0) {
          giudizio = 1;
        }
        else if ((mgr_gr === 1 && li === 0) || (mgr_gr <= 1 && li >= 1 && li <= 3)) {
          giudizio = 2;
        }
        else if ((mgr_gr >= 2 && mgr_gr <= 3 && li === 0) || (mgr_gr <= 2 && li >= 4 && li <= 6)) {
          giudizio = 3;
        }
        else if ((mgr_gr >= 4 && mgr_gr <= 6 && li <= 3) || (mgr_gr >= 2 && mgr_gr <= 3 && li <= 6 && li >= 1) || (mgr_gr <= 2 && li >= 7)) {
          giudizio = 4;
        } else {
          //pessimo
          giudizio = 5
        }
        //fine costruzione giudizio
        vd['giudizio'] = giudizio
      }
      return vd
    },
  },
  created() {
    // https://vuejs.org/v2/guide/instance.html
    this.fetchData()
  },
  methods: {
    async fetchData() {
      this.verificaallerta_id = this.id
      this.giudizio = await this.fetchGiudizio()
      this.severita = await this.fetchSeverita()
      this.criticita = await this.fetchCriticita()

      // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions
      this.fetchVerificaAllerta().then(response => {
        if (!response.ok) {
          this.$toast.open(
            {
              message: `Errore ${response.status} nel recupero del bollettino`,
              type: 'error',
              position: 'top-left'
            }
          )
        }
        return response.json()
      }).then(data => {
        data['pippo'] = 'pluto'
        this.verificaallerta = data
        this.readonly = (this.verificaallerta.status === '1' || !this.state.username)
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
    async fetchVerificaAllerta() {
      // https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
      const response = await fetch('/api/w23verifica/bulletins/' + this.verificaallerta_id + '/', {
        headers: {
          accept: 'application/json'
        }
      })
      return response
    },
    async fetchGiudizio() {
      try {
        const response = await fetch('/api/w23verifica/giudizio/', {
          headers: {
            accept: 'application/json'
          }
        })
        if (!response.ok) {
          this.$toast.open(
            {
              message: `Errore ${response.status} nel recupero del Giudizio`,
              type: 'error',
              position: 'top-left'
            }
          )
        }
        return await response.json()
      } catch (error) {
        this.$toast.open(
          {
            message: error,
            type: 'error',
            position: 'top-left'
          }
        )
      }
    },
    async fetchSeverita() {
      try {
        const response = await fetch('/api/w23verifica/severita/', {
          headers: {
            accept: 'application/json'
          }
        })
        if (!response.ok) {
          this.$toast.open(
            {
              message: `Errore ${response.status} nel recupero del Severita`,
              type: 'error',
              position: 'top-left'
            }
          )
        }
        return await response.json()
      } catch (error) {
        this.$toast.open(
          {
            message: error,
            type: 'error',
            position: 'top-left'
          }
        )
      }
    },
    async fetchCriticita() {
      try {
        const response = await fetch('/api/w23verifica/criticita/', {
          headers: {
            accept: 'application/json'
          }
        })
        if (!response.ok) {
          this.$toast.open(
            {
              message: `Errore ${response.status} nel recupero del Criticità`,
              type: 'error',
              position: 'top-left'
            }
          )
        }
        return await response.json()
      } catch (error) {
        this.$toast.open(
          {
            message: error,
            type: 'error',
            position: 'top-left'
          }
        )
      }
    },
    async fetchPatch(id, endpoint, payload) {
      const response = await api.fetch_wrapper(
        store.state.access,
        `/api/w23verifica/${endpoint}/${id}/`,
        {
          method: 'PATCH',
          body: JSON.stringify(payload)
        }
      )
      return response
    },
    saveW23verifica(newValue, id_w23verifica, campo) {
      //se sto calcolando il giudizio in automatico
      this.saving = true
      if (campo == null) {
        campo = 'id_w23giudizio'
        newValue = this.gr.giudizio
      }
      if (campo === "id_numero_bollettino") {
        this.verificaallerta.id_numero_bollettino = newValue;
        this.verificaallerta.numero_bollettino = newValue.split("_")[0] + '/' + newValue.split("_")[1];
      }
      const payload = {}
      if (campo) {
        payload[campo] = newValue
      }
      if (campo === "id_numero_bollettino") {
        payload['numero_bollettino'] = newValue.split("_")[0] + '/' + newValue.split("_")[1];
      }
      payload['id_w23verifica'] = id_w23verifica
      payload['username'] = store.state.username
      this.bulkUpdateW23verifica(payload).then((response) => {
        if (!response.ok) {
          this.$toast.open(
            {
              message: 'Errore nel salvataggio bulk',
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
        this.verificaallerta.last_update = data.last_update
        this.verificaallerta.username = store.state.username
        if (campo === "id_w23giudizio") {
          this.verificaallerta.id_w23giudizio = newValue;
        }
        this.saving = false
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
    getDateFormatted(rawString, time = true) {
      return api.getDateFormatted(rawString, time)
    },
    // Metodo generico per salvare i dati delle select di criticita e tendenza
    saveW23verificaDataSelect(newValue, id_w23verifica_data, id_w23_zone, campo) {
      let myW23zone = this.verificaallerta.w23verificadata_set.find(w23verificadata => {
        return w23verificadata.id_w23_zone.id_w23_zone === id_w23_zone
      })
      myW23zone[campo] = newValue
      const payload = {}
      if (campo == 'oss_crit_neve_oggi' || campo == 'oss_crit_neve_domani' || campo == 'oss_crit_valanghe_oggi' || campo == 'oss_crit_valanghe_domani' || campo == 'oss_crit_temporali_oggi' || campo == 'oss_crit_temporali_domani' || campo == 'oss_crit_idraulico_oggi' || campo == 'oss_crit_idraulico_domani' || campo == 'oss_crit_idrogeologico_oggi' || campo == 'oss_crit_idrogeologico_domani') {
        //sto assegando e salvando il calcolo della criticità in automatico
        payload['oss_crit_tot'] = this.Verificamassimooss[id_w23_zone].massimo_oggi_domani
        this.verificaallerta.w23verificadata_set[id_w23_zone - 1].oss_crit_tot = this.Verificamassimooss[id_w23_zone].massimo_oggi_domani
        payload['oss_crit_oggi'] = this.Verificamassimooss[id_w23_zone].massimo_oggi
        this.verificaallerta.w23verificadata_set[id_w23_zone - 1].oss_crit_oggi = this.Verificamassimooss[id_w23_zone].massimo_oggi
        payload['oss_crit_domani'] = this.Verificamassimooss[id_w23_zone].massimo_domani
        this.verificaallerta.w23verificadata_set[id_w23_zone - 1].oss_crit_domani = this.Verificamassimooss[id_w23_zone].massimo_domani

        this.verificaallerta.w23verificadata_set[id_w23_zone - 1].err_crit_tot = this.Verificaseverita[id_w23_zone].severita
        payload['err_crit_tot'] = this.Verificaseverita[id_w23_zone].severita
        //sto salvando il calcolo del giudizio automatico
        this.saveW23verifica(this.gr.giudizio, this.verificaallerta.id_w23verifica, 'id_w23giudizio')
      }
      if (campo == 'oss_crit_oggi' || campo == 'oss_crit_domani') {
        payload['oss_crit_tot'] = this.Verificamassimooss[id_w23_zone].massimo_oggi_domani_tot
        this.verificaallerta.w23verificadata_set[id_w23_zone - 1].oss_crit_tot = this.Verificamassimooss[id_w23_zone].massimo_oggi_domani_tot
        //sto assegando e salvando il calcolo della criticità in automatico
        this.verificaallerta.w23verificadata_set[id_w23_zone - 1].err_crit_tot = this.Verificaseverita[id_w23_zone].severita
        payload['err_crit_tot'] = this.Verificaseverita[id_w23_zone].severita
        //sto salvando il calcolo del giudizio automatico
        this.saveW23verifica(this.gr.giudizio, this.verificaallerta.id_w23verifica, 'id_w23giudizio')
      }
      if (campo == 'prev_crit_tot' || campo == 'oss_crit_tot') {
        //sto assegando e salvando il calcolo della criticità in automatico
        this.verificaallerta.w23verificadata_set[id_w23_zone - 1].err_crit_tot = this.Verificaseverita[id_w23_zone].severita
        payload['err_crit_tot'] = this.Verificaseverita[id_w23_zone].severita
        //sto salvando il calcolo del giudizio automatico
        this.saveW23verifica(this.gr.giudizio, this.verificaallerta.id_w23verifica, 'id_w23giudizio')
      }
      payload[campo] = newValue

      this.fetchPatch(myW23zone.id_w23verifica_data, 'data', payload).then((response) => {
        if (!response.ok) {
          this.$toast.open(
            {
              message: 'Errore nel salvataggio',
              type: 'error',
              position: 'top-left'
            }
          )
        } else {
          this.saveW23verifica(null, this.verificaallerta.id_w23verifica, null)
        }
      }).catch((error) => {
        this.$toast.open(
          {
            message: `Errore di comunicazione: ${error}`,
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
        api.fetchBulletinDelete(this.verificaallerta_id, 'w23verifica/bulletins', store).then(response => {
          if (response.ok) {
            this.$toast.open(
              {
                message: 'Bollettino cancellato',
                type: 'success',
                position: 'top-left'
              }
            )
            this.$router.back()
          } else {
            this.$toast.open(
              {
                message: `Errore ${response.status} nella cancellazione del bollettino`,
                type: 'error',
                position: 'top-left'
              }
            )
          }
        }).catch(error => {
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
    async fetchVerificaAllertaAction(action) {
      const response = await api.fetch_wrapper(
        store.state.access,
        `/api/w23verifica/bulletins/${this.verificaallerta_id}/${action}/`
      )
      return response
    },
    execute_timeout(action, reroute, message) {
      // console.log("inizio execute_timeout")
      if (this.saving) {
        console.log("saving è true faccio partire timeout")
        setTimeout(() => {
          console.log("aspetto 1 secondo finchè non finisce il salvataggio in corso")
          this.execute_timeout(action, reroute, message)
        }, 1000);
      } else {
        console.log("saving è false lancio execute")
        this.execute(action, reroute, message)
      }
      // console.log("fine execute_timeout")
    },
    execute(action, reroute, message) {
      this[action + 'ing'] = true
      this.fetchVerificaAllertaAction(action).then(response => {
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
          this.$router.push({ path: `/w23verifica/${data.id_w23verifica}` })
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
    async bulkUpdateW23verifica(payload) {
      const response = await api.fetch_wrapper(
        store.state.access,
        `/api/w23verifica/bulletins/bulk_update/`,
        {
          method: 'POST',
          body: JSON.stringify(payload)
        }
      )
      return response
    }
  }
}
</script>
