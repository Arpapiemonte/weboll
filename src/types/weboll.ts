// Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
// This file is part of weboll (the bulletin back-office for ARPA Piemonte).
// weboll is licensed under the AGPL-3.0-or-later License.
// License text available at https://www.gnu.org/licenses/agpl.txt



export interface paths {
  "/token/": {
    /**
     * @description Takes a set of user credentials and returns an access and refresh JSON web
     * token pair to prove the authentication of those credentials.
     */
    post: operations["token_create"];
  };
  "/token/refresh/": {
    /**
     * @description Takes a refresh type JSON web token and returns an access type JSON web
     * token if the refresh token is valid.
     */
    post: operations["token_refresh_create"];
  };
  "/token/verify/": {
    /**
     * @description Takes a token and indicates if it is valid.  This view provides no
     * information about a token's fitness for a particular use.
     */
    post: operations["token_verify_create"];
  };
  "/w05/bulletins/": {
    /** @description API endpoint that allows W05 bulletins to be viewed or edited */
    get: operations["w05_bulletins_list"];
    /** @description API endpoint that allows W05 bulletins to be viewed or edited */
    post: operations["w05_bulletins_create"];
  };
  "/w05/bulletins/{id_w05}/": {
    /** @description API endpoint that allows W05 bulletins to be viewed or edited */
    get: operations["w05_bulletins_retrieve"];
    /** @description API endpoint that allows W05 bulletins to be viewed or edited */
    put: operations["w05_bulletins_update"];
    /** @description API endpoint that allows W05 bulletins to be viewed or edited */
    delete: operations["w05_bulletins_destroy"];
    /** @description API endpoint that allows W05 bulletins to be viewed or edited */
    patch: operations["w05_bulletins_partial_update"];
  };
  "/w05/bulletins/{id_w05}/classes_json/": {
    /** @description API endpoint that allows W05 bulletins to be viewed or edited */
    get: operations["w05_bulletins_classes_json_retrieve"];
  };
  "/w05/bulletins/{id_w05}/data_json/": {
    /** @description API endpoint that allows W05 bulletins to be viewed or edited */
    get: operations["w05_bulletins_data_json_retrieve"];
  };
  "/w05/bulletins/{id_w05}/json/": {
    /** @description API endpoint that allows W05 bulletins to be viewed or edited */
    get: operations["w05_bulletins_json_retrieve"];
  };
  "/w05/bulletins/{id_w05}/reload/": {
    /** @description API endpoint that allows W05 bulletins to be viewed or edited */
    get: operations["w05_bulletins_reload_retrieve"];
  };
  "/w05/bulletins/{id_w05}/reopen/": {
    /** @description API endpoint that allows W05 bulletins to be viewed or edited */
    get: operations["w05_bulletins_reopen_retrieve"];
  };
  "/w05/bulletins/{id_w05}/resend/": {
    /** @description API endpoint that allows W05 bulletins to be viewed or edited */
    get: operations["w05_bulletins_resend_retrieve"];
  };
  "/w05/bulletins/{id_w05}/send/": {
    /** @description API endpoint that allows W05 bulletins to be viewed or edited */
    get: operations["w05_bulletins_send_retrieve"];
  };
  "/w05/bulletins/{id_w05}/xml/": {
    /** @description API endpoint that allows W05 bulletins to be viewed or edited */
    get: operations["w05_bulletins_xml_retrieve"];
  };
  "/w05/bulletins/bulk_update/": {
    /** @description API endpoint that allows W05 bulletins to be viewed or edited */
    post: operations["w05_bulletins_bulk_update_create"];
  };
  "/w05/bulletins/new/": {
    /** @description API endpoint that allows W05 bulletins to be viewed or edited */
    get: operations["w05_bulletins_new_retrieve"];
  };
  "/w05/classes/": {
    /** @description API endpoint that allows Classes to be viewed */
    get: operations["w05_classes_list"];
    /** @description API endpoint that allows Classes to be viewed */
    post: operations["w05_classes_create"];
  };
  "/w05/classes/{id_classes}/": {
    /** @description API endpoint that allows Classes to be viewed */
    get: operations["w05_classes_retrieve"];
    /** @description API endpoint that allows Classes to be viewed */
    put: operations["w05_classes_update"];
    /** @description API endpoint that allows Classes to be viewed */
    delete: operations["w05_classes_destroy"];
    /** @description API endpoint that allows Classes to be viewed */
    patch: operations["w05_classes_partial_update"];
  };
  "/w05/data/": {
    /** @description API endpoint that allows W05 bulletin Data to be viewed or edited */
    get: operations["w05_data_list"];
    /** @description API endpoint that allows W05 bulletin Data to be viewed or edited */
    post: operations["w05_data_create"];
  };
  "/w05/data/{id_w05_data}/": {
    /** @description API endpoint that allows W05 bulletin Data to be viewed or edited */
    get: operations["w05_data_retrieve"];
    /** @description API endpoint that allows W05 bulletin Data to be viewed or edited */
    put: operations["w05_data_update"];
    /** @description API endpoint that allows W05 bulletin Data to be viewed or edited */
    delete: operations["w05_data_destroy"];
    /** @description API endpoint that allows W05 bulletin Data to be viewed or edited */
    patch: operations["w05_data_partial_update"];
  };
  "/w05/meteo_classes/": {
    /** @description API endpoint that allows W05 bulletin Classes to be viewed or edited */
    get: operations["w05_meteo_classes_list"];
    /** @description API endpoint that allows W05 bulletin Classes to be viewed or edited */
    post: operations["w05_meteo_classes_create"];
  };
  "/w05/meteo_classes/{id_w05_classes}/": {
    /** @description API endpoint that allows W05 bulletin Classes to be viewed or edited */
    get: operations["w05_meteo_classes_retrieve"];
    /** @description API endpoint that allows W05 bulletin Classes to be viewed or edited */
    put: operations["w05_meteo_classes_update"];
    /** @description API endpoint that allows W05 bulletin Classes to be viewed or edited */
    delete: operations["w05_meteo_classes_destroy"];
    /** @description API endpoint that allows W05 bulletin Classes to be viewed or edited */
    patch: operations["w05_meteo_classes_partial_update"];
  };
  "/w05/sky_conditions/": {
    /** @description API endpoint that allows W16 bulletins to be viewed or edited */
    get: operations["w05_sky_conditions_list"];
    /** @description API endpoint that allows W16 bulletins to be viewed or edited */
    post: operations["w05_sky_conditions_create"];
  };
  "/w05/sky_conditions/{id_sky_condition}/": {
    /** @description API endpoint that allows W16 bulletins to be viewed or edited */
    get: operations["w05_sky_conditions_retrieve"];
    /** @description API endpoint that allows W16 bulletins to be viewed or edited */
    put: operations["w05_sky_conditions_update"];
    /** @description API endpoint that allows W16 bulletins to be viewed or edited */
    delete: operations["w05_sky_conditions_destroy"];
    /** @description API endpoint that allows W16 bulletins to be viewed or edited */
    patch: operations["w05_sky_conditions_partial_update"];
  };
  "/w05/venue_names/": {
    /** @description API endpoint that shows city names */
    get: operations["w05_venue_names_list"];
    /** @description API endpoint that shows city names */
    post: operations["w05_venue_names_create"];
  };
  "/w05/venue_names/{id_venue}/": {
    /** @description API endpoint that shows city names */
    get: operations["w05_venue_names_retrieve"];
    /** @description API endpoint that shows city names */
    put: operations["w05_venue_names_update"];
    /** @description API endpoint that shows city names */
    delete: operations["w05_venue_names_destroy"];
    /** @description API endpoint that shows city names */
    patch: operations["w05_venue_names_partial_update"];
  };
  "/w16/bulletins/": {
    /** @description API endpoint that allows W16 bulletins to be viewed or edited */
    get: operations["w16_bulletins_list"];
    /** @description API endpoint that allows W16 bulletins to be viewed or edited */
    post: operations["w16_bulletins_create"];
  };
  "/w16/bulletins/{id_w16}/": {
    /** @description API endpoint that allows W16 bulletins to be viewed or edited */
    get: operations["w16_bulletins_retrieve"];
    /** @description API endpoint that allows W16 bulletins to be viewed or edited */
    put: operations["w16_bulletins_update"];
    /** @description API endpoint that allows W16 bulletins to be viewed or edited */
    delete: operations["w16_bulletins_destroy"];
    /** @description API endpoint that allows W16 bulletins to be viewed or edited */
    patch: operations["w16_bulletins_partial_update"];
  };
  "/w16/bulletins/{id_w16}/copy/": {
    /** @description API endpoint that allows W16 bulletins to be viewed or edited */
    get: operations["w16_bulletins_copy_retrieve"];
  };
  "/w16/bulletins/{id_w16}/reopen/": {
    /** @description API endpoint that allows W16 bulletins to be viewed or edited */
    get: operations["w16_bulletins_reopen_retrieve"];
  };
  "/w16/bulletins/{id_w16}/send/": {
    /** @description API endpoint that allows W16 bulletins to be viewed or edited */
    get: operations["w16_bulletins_send_retrieve"];
  };
  "/w16/bulletins/new/": {
    /** @description API endpoint that allows W16 bulletins to be viewed or edited */
    get: operations["w16_bulletins_new_retrieve"];
  };
  "/w16/conf/": {
    /** @description API endpoint that allows W16Conf records to be viewed */
    get: operations["w16_conf_list"];
    /** @description API endpoint that allows W16Conf records to be viewed */
    post: operations["w16_conf_create"];
  };
  "/w16/conf/{id_w16_conf}/": {
    /** @description API endpoint that allows W16Conf records to be viewed */
    get: operations["w16_conf_retrieve"];
    /** @description API endpoint that allows W16Conf records to be viewed */
    put: operations["w16_conf_update"];
    /** @description API endpoint that allows W16Conf records to be viewed */
    delete: operations["w16_conf_destroy"];
    /** @description API endpoint that allows W16Conf records to be viewed */
    patch: operations["w16_conf_partial_update"];
  };
  "/w16/data/": {
    /** @description API endpoint that allows W16 bulletin Data to be viewed or updated */
    get: operations["w16_data_list"];
    /** @description API endpoint that allows W16 bulletin Data to be viewed or updated */
    post: operations["w16_data_create"];
  };
  "/w16/data/{id_w16_data}/": {
    /** @description API endpoint that allows W16 bulletin Data to be viewed or updated */
    get: operations["w16_data_retrieve"];
    /** @description API endpoint that allows W16 bulletin Data to be viewed or updated */
    put: operations["w16_data_update"];
    /** @description API endpoint that allows W16 bulletin Data to be viewed or updated */
    delete: operations["w16_data_destroy"];
    /** @description API endpoint that allows W16 bulletin Data to be viewed or updated */
    patch: operations["w16_data_partial_update"];
  };
  "/w16/data/bulk_update/": {
    /** @description API endpoint that allows W16 bulletin Data to be viewed or updated */
    post: operations["w16_data_bulk_update_create"];
  };
  "/w16/levels/": {
    /** @description API endpoint that allows OzonoLivelli records to be viewed */
    get: operations["w16_levels_list"];
    /** @description API endpoint that allows OzonoLivelli records to be viewed */
    post: operations["w16_levels_create"];
  };
  "/w16/levels/{id_ozono_livelli}/": {
    /** @description API endpoint that allows OzonoLivelli records to be viewed */
    get: operations["w16_levels_retrieve"];
    /** @description API endpoint that allows OzonoLivelli records to be viewed */
    put: operations["w16_levels_update"];
    /** @description API endpoint that allows OzonoLivelli records to be viewed */
    delete: operations["w16_levels_destroy"];
    /** @description API endpoint that allows OzonoLivelli records to be viewed */
    patch: operations["w16_levels_partial_update"];
  };
  "/w22/bulletins/": {
    /** @description API endpoint that allows W22 bulletins to be viewed or edited */
    get: operations["w22_bulletins_list"];
    /** @description API endpoint that allows W22 bulletins to be viewed or edited */
    post: operations["w22_bulletins_create"];
  };
  "/w22/bulletins/{id_w22}/": {
    /** @description API endpoint that allows W22 bulletins to be viewed or edited */
    get: operations["w22_bulletins_retrieve"];
    /** @description API endpoint that allows W22 bulletins to be viewed or edited */
    put: operations["w22_bulletins_update"];
    /** @description API endpoint that allows W22 bulletins to be viewed or edited */
    delete: operations["w22_bulletins_destroy"];
    /** @description API endpoint that allows W22 bulletins to be viewed or edited */
    patch: operations["w22_bulletins_partial_update"];
  };
  "/w22/bulletins/{id_w22}/send/": {
    /** @description API endpoint that allows W22 bulletins to be viewed or edited */
    get: operations["w22_bulletins_send_retrieve"];
  };
  "/w22/bulletins/bulk_update/": {
    /** @description API endpoint that allows W22 bulletins to be viewed or edited */
    post: operations["w22_bulletins_bulk_update_create"];
  };
  "/w22/bulletins/new/": {
    /** @description API endpoint that allows W22 bulletins to be viewed or edited */
    get: operations["w22_bulletins_new_retrieve"];
  };
  "/w22/criticita/": {
    /** @description API endpoint that allows W22 bulletin Criticità to be viewed */
    get: operations["w22_criticita_list"];
    /** @description API endpoint that allows W22 bulletin Criticità to be viewed */
    post: operations["w22_criticita_create"];
  };
  "/w22/criticita/{id_w22_criticita}/": {
    /** @description API endpoint that allows W22 bulletin Criticità to be viewed */
    get: operations["w22_criticita_retrieve"];
    /** @description API endpoint that allows W22 bulletin Criticità to be viewed */
    put: operations["w22_criticita_update"];
    /** @description API endpoint that allows W22 bulletin Criticità to be viewed */
    delete: operations["w22_criticita_destroy"];
    /** @description API endpoint that allows W22 bulletin Criticità to be viewed */
    patch: operations["w22_criticita_partial_update"];
  };
  "/w22/data/": {
    /** @description API endpoint that allows W22 bulletin Data to be viewed or edited */
    get: operations["w22_data_list"];
    /** @description API endpoint that allows W22 bulletin Data to be viewed or edited */
    post: operations["w22_data_create"];
  };
  "/w22/data/{id_w22_data}/": {
    /** @description API endpoint that allows W22 bulletin Data to be viewed or edited */
    get: operations["w22_data_retrieve"];
    /** @description API endpoint that allows W22 bulletin Data to be viewed or edited */
    put: operations["w22_data_update"];
    /** @description API endpoint that allows W22 bulletin Data to be viewed or edited */
    delete: operations["w22_data_destroy"];
    /** @description API endpoint that allows W22 bulletin Data to be viewed or edited */
    patch: operations["w22_data_partial_update"];
  };
  "/w22/tendenza/": {
    /** @description API endpoint that allows W22 bulletin Tendenza to be viewed */
    get: operations["w22_tendenza_list"];
    /** @description API endpoint that allows W22 bulletin Tendenza to be viewed */
    post: operations["w22_tendenza_create"];
  };
  "/w22/tendenza/{id_w22_tendenza}/": {
    /** @description API endpoint that allows W22 bulletin Tendenza to be viewed */
    get: operations["w22_tendenza_retrieve"];
    /** @description API endpoint that allows W22 bulletin Tendenza to be viewed */
    put: operations["w22_tendenza_update"];
    /** @description API endpoint that allows W22 bulletin Tendenza to be viewed */
    delete: operations["w22_tendenza_destroy"];
    /** @description API endpoint that allows W22 bulletin Tendenza to be viewed */
    patch: operations["w22_tendenza_partial_update"];
  };
  "/w22/zone/": {
    /** @description API endpoint that allows W22 bulletin Zone to be viewed or edited */
    get: operations["w22_zone_list"];
    /** @description API endpoint that allows W22 bulletin Zone to be viewed or edited */
    post: operations["w22_zone_create"];
  };
  "/w22/zone/{id_w22_zone}/": {
    /** @description API endpoint that allows W22 bulletin Zone to be viewed or edited */
    get: operations["w22_zone_retrieve"];
    /** @description API endpoint that allows W22 bulletin Zone to be viewed or edited */
    put: operations["w22_zone_update"];
    /** @description API endpoint that allows W22 bulletin Zone to be viewed or edited */
    delete: operations["w22_zone_destroy"];
    /** @description API endpoint that allows W22 bulletin Zone to be viewed or edited */
    patch: operations["w22_zone_partial_update"];
  };
  "/w22verifica/bulletins/": {
    /** @description API endpoint that allows W22 bulletins to be viewed or edited */
    get: operations["w22verifica_bulletins_list"];
    /** @description API endpoint that allows W22 bulletins to be viewed or edited */
    post: operations["w22verifica_bulletins_create"];
  };
  "/w22verifica/bulletins/{id_w22verifica}/": {
    /** @description API endpoint that allows W22 bulletins to be viewed or edited */
    get: operations["w22verifica_bulletins_retrieve"];
    /** @description API endpoint that allows W22 bulletins to be viewed or edited */
    put: operations["w22verifica_bulletins_update"];
    /** @description API endpoint that allows W22 bulletins to be viewed or edited */
    delete: operations["w22verifica_bulletins_destroy"];
    /** @description API endpoint that allows W22 bulletins to be viewed or edited */
    patch: operations["w22verifica_bulletins_partial_update"];
  };
  "/w22verifica/bulletins/{id_w22verifica}/send/": {
    /** @description API endpoint that allows W22 bulletins to be viewed or edited */
    get: operations["w22verifica_bulletins_send_retrieve"];
  };
  "/w22verifica/bulletins/bulk_update/": {
    /** @description API endpoint that allows W22 bulletins to be viewed or edited */
    post: operations["w22verifica_bulletins_bulk_update_create"];
  };
  "/w22verifica/bulletins/new/{num_bollettino}/": {
    /** @description API endpoint that allows W22 bulletins to be viewed or edited */
    get: operations["w22verifica_bulletins_new_retrieve"];
  };
  "/w22verifica/data/": {
    /** @description API endpoint that allows W22 bulletin Data to be viewed or edited */
    get: operations["w22verifica_data_list"];
    /** @description API endpoint that allows W22 bulletin Data to be viewed or edited */
    post: operations["w22verifica_data_create"];
  };
  "/w22verifica/data/{id_w22verifica_data}/": {
    /** @description API endpoint that allows W22 bulletin Data to be viewed or edited */
    get: operations["w22verifica_data_retrieve"];
    /** @description API endpoint that allows W22 bulletin Data to be viewed or edited */
    put: operations["w22verifica_data_update"];
    /** @description API endpoint that allows W22 bulletin Data to be viewed or edited */
    delete: operations["w22verifica_data_destroy"];
    /** @description API endpoint that allows W22 bulletin Data to be viewed or edited */
    patch: operations["w22verifica_data_partial_update"];
  };
  "/w22verifica/giudizio/": {
    /** @description API endpoint that allows W22 bulletin Tendenza to be viewed */
    get: operations["w22verifica_giudizio_list"];
    /** @description API endpoint that allows W22 bulletin Tendenza to be viewed */
    post: operations["w22verifica_giudizio_create"];
  };
  "/w22verifica/giudizio/{id_w22giudizio}/": {
    /** @description API endpoint that allows W22 bulletin Tendenza to be viewed */
    get: operations["w22verifica_giudizio_retrieve"];
    /** @description API endpoint that allows W22 bulletin Tendenza to be viewed */
    put: operations["w22verifica_giudizio_update"];
    /** @description API endpoint that allows W22 bulletin Tendenza to be viewed */
    delete: operations["w22verifica_giudizio_destroy"];
    /** @description API endpoint that allows W22 bulletin Tendenza to be viewed */
    patch: operations["w22verifica_giudizio_partial_update"];
  };
  "/w22verifica/severita/": {
    /** @description API endpoint that allows W22 bulletin Criticità to be viewed */
    get: operations["w22verifica_severita_list"];
    /** @description API endpoint that allows W22 bulletin Criticità to be viewed */
    post: operations["w22verifica_severita_create"];
  };
  "/w22verifica/severita/{id_w22severita}/": {
    /** @description API endpoint that allows W22 bulletin Criticità to be viewed */
    get: operations["w22verifica_severita_retrieve"];
    /** @description API endpoint that allows W22 bulletin Criticità to be viewed */
    put: operations["w22verifica_severita_update"];
    /** @description API endpoint that allows W22 bulletin Criticità to be viewed */
    delete: operations["w22verifica_severita_destroy"];
    /** @description API endpoint that allows W22 bulletin Criticità to be viewed */
    patch: operations["w22verifica_severita_partial_update"];
  };
  "/w22verifica/zone/": {
    /** @description API endpoint that allows W22 bulletin Zone to be viewed or edited */
    get: operations["w22verifica_zone_list"];
    /** @description API endpoint that allows W22 bulletin Zone to be viewed or edited */
    post: operations["w22verifica_zone_create"];
  };
  "/w22verifica/zone/{id_w22_zone}/": {
    /** @description API endpoint that allows W22 bulletin Zone to be viewed or edited */
    get: operations["w22verifica_zone_retrieve"];
    /** @description API endpoint that allows W22 bulletin Zone to be viewed or edited */
    put: operations["w22verifica_zone_update"];
    /** @description API endpoint that allows W22 bulletin Zone to be viewed or edited */
    delete: operations["w22verifica_zone_destroy"];
    /** @description API endpoint that allows W22 bulletin Zone to be viewed or edited */
    patch: operations["w22verifica_zone_partial_update"];
  };
  "/w23/bulletins/": {
    /** @description API endpoint that allows W23 bulletins to be viewed or edited */
    get: operations["w23_bulletins_list"];
    /** @description API endpoint that allows W23 bulletins to be viewed or edited */
    post: operations["w23_bulletins_create"];
  };
  "/w23/bulletins/{id_w23}/": {
    /** @description API endpoint that allows W23 bulletins to be viewed or edited */
    get: operations["w23_bulletins_retrieve"];
    /** @description API endpoint that allows W23 bulletins to be viewed or edited */
    put: operations["w23_bulletins_update"];
    /** @description API endpoint that allows W23 bulletins to be viewed or edited */
    delete: operations["w23_bulletins_destroy"];
    /** @description API endpoint that allows W23 bulletins to be viewed or edited */
    patch: operations["w23_bulletins_partial_update"];
  };
  "/w23/bulletins/{id_w23}/reopen/": {
    /** @description API endpoint that allows W23 bulletins to be viewed or edited */
    get: operations["w23_bulletins_reopen_retrieve"];
  };
  "/w23/bulletins/{id_w23}/send/": {
    /** @description API endpoint that allows W23 bulletins to be viewed or edited */
    get: operations["w23_bulletins_send_retrieve"];
  };
  "/w23/bulletins/bulk_update/": {
    /** @description API endpoint that allows W23 bulletins to be viewed or edited */
    post: operations["w23_bulletins_bulk_update_create"];
  };
  "/w23/bulletins/new/": {
    /** @description API endpoint that allows W23 bulletins to be viewed or edited */
    get: operations["w23_bulletins_new_retrieve"];
  };
  "/w23/current/{data_emissione}": {
    /** @description View the latest W23 bulletin sent for a certain day */
    get: operations["w23_current_retrieve"];
  };
  "/w23/data/": {
    /** @description API endpoint that allows W23 bulletin Data to be viewed or edited */
    get: operations["w23_data_list"];
    /** @description API endpoint that allows W23 bulletin Data to be viewed or edited */
    post: operations["w23_data_create"];
  };
  "/w23/data/{id_w23_data}/": {
    /** @description API endpoint that allows W23 bulletin Data to be viewed or edited */
    get: operations["w23_data_retrieve"];
    /** @description API endpoint that allows W23 bulletin Data to be viewed or edited */
    put: operations["w23_data_update"];
    /** @description API endpoint that allows W23 bulletin Data to be viewed or edited */
    delete: operations["w23_data_destroy"];
    /** @description API endpoint that allows W23 bulletin Data to be viewed or edited */
    patch: operations["w23_data_partial_update"];
  };
  "/w23/effetti/": {
    /** @description API endpoint that allows W23 bulletin Effetti sul territorio to be viewed */
    get: operations["w23_effetti_list"];
    /** @description API endpoint that allows W23 bulletin Effetti sul territorio to be viewed */
    post: operations["w23_effetti_create"];
  };
  "/w23/effetti/{id_w23_effettiterritorio}/": {
    /** @description API endpoint that allows W23 bulletin Effetti sul territorio to be viewed */
    get: operations["w23_effetti_retrieve"];
    /** @description API endpoint that allows W23 bulletin Effetti sul territorio to be viewed */
    put: operations["w23_effetti_update"];
    /** @description API endpoint that allows W23 bulletin Effetti sul territorio to be viewed */
    delete: operations["w23_effetti_destroy"];
    /** @description API endpoint that allows W23 bulletin Effetti sul territorio to be viewed */
    patch: operations["w23_effetti_partial_update"];
  };
  "/w23/pericoli/": {
    /** @description API endpoint that allows W23 bulletin Pericolo to be viewed */
    get: operations["w23_pericoli_list"];
    /** @description API endpoint that allows W23 bulletin Pericolo to be viewed */
    post: operations["w23_pericoli_create"];
  };
  "/w23/pericoli/{id_w23_pericolo}/": {
    /** @description API endpoint that allows W23 bulletin Pericolo to be viewed */
    get: operations["w23_pericoli_retrieve"];
    /** @description API endpoint that allows W23 bulletin Pericolo to be viewed */
    put: operations["w23_pericoli_update"];
    /** @description API endpoint that allows W23 bulletin Pericolo to be viewed */
    delete: operations["w23_pericoli_destroy"];
    /** @description API endpoint that allows W23 bulletin Pericolo to be viewed */
    patch: operations["w23_pericoli_partial_update"];
  };
  "/w23/pluvossh6/": {
    get: operations["w23_pluvossh6_list"];
    post: operations["w23_pluvossh6_create"];
  };
  "/w23/pluvossh6/{id_w23_pluvossh6}/": {
    get: operations["w23_pluvossh6_retrieve"];
    put: operations["w23_pluvossh6_update"];
    delete: operations["w23_pluvossh6_destroy"];
    patch: operations["w23_pluvossh6_partial_update"];
  };
  "/w23/soglie_nivo_area_prev/": {
    get: operations["w23_soglie_nivo_area_prev_list"];
    post: operations["w23_soglie_nivo_area_prev_create"];
  };
  "/w23/soglie_nivo_area_prev/{idtab_allertamento}/": {
    get: operations["w23_soglie_nivo_area_prev_retrieve"];
    put: operations["w23_soglie_nivo_area_prev_update"];
    delete: operations["w23_soglie_nivo_area_prev_destroy"];
    patch: operations["w23_soglie_nivo_area_prev_partial_update"];
  };
  "/w23/soglie_pluv_area_prev_massimi/": {
    get: operations["w23_soglie_pluv_area_prev_massimi_list"];
    post: operations["w23_soglie_pluv_area_prev_massimi_create"];
  };
  "/w23/soglie_pluv_area_prev_massimi/{idtab_allertamento}/": {
    get: operations["w23_soglie_pluv_area_prev_massimi_retrieve"];
    put: operations["w23_soglie_pluv_area_prev_massimi_update"];
    delete: operations["w23_soglie_pluv_area_prev_massimi_destroy"];
    patch: operations["w23_soglie_pluv_area_prev_massimi_partial_update"];
  };
  "/w23/soglie_pluv_area_prev_medie/": {
    get: operations["w23_soglie_pluv_area_prev_medie_list"];
    post: operations["w23_soglie_pluv_area_prev_medie_create"];
  };
  "/w23/soglie_pluv_area_prev_medie/{idtab_allertamento}/": {
    get: operations["w23_soglie_pluv_area_prev_medie_retrieve"];
    put: operations["w23_soglie_pluv_area_prev_medie_update"];
    delete: operations["w23_soglie_pluv_area_prev_medie_destroy"];
    patch: operations["w23_soglie_pluv_area_prev_medie_partial_update"];
  };
  "/w23/time_layouts/": {
    get: operations["w23_time_layouts_list"];
    post: operations["w23_time_layouts_create"];
  };
  "/w23/time_layouts/{id_time_layouts}/": {
    get: operations["w23_time_layouts_retrieve"];
    put: operations["w23_time_layouts_update"];
    delete: operations["w23_time_layouts_destroy"];
    patch: operations["w23_time_layouts_partial_update"];
  };
  "/w23/zone/": {
    /** @description API endpoint that allows W23 bulletin Zone to be viewed */
    get: operations["w23_zone_list"];
    /** @description API endpoint that allows W23 bulletin Zone to be viewed */
    post: operations["w23_zone_create"];
  };
  "/w23/zone/{id_w23_zone}/": {
    /** @description API endpoint that allows W23 bulletin Zone to be viewed */
    get: operations["w23_zone_retrieve"];
    /** @description API endpoint that allows W23 bulletin Zone to be viewed */
    put: operations["w23_zone_update"];
    /** @description API endpoint that allows W23 bulletin Zone to be viewed */
    delete: operations["w23_zone_destroy"];
    /** @description API endpoint that allows W23 bulletin Zone to be viewed */
    patch: operations["w23_zone_partial_update"];
  };
  "/w24/bulletins/": {
    /** @description API endpoint that allows W24 bulletins to be viewed or edited */
    get: operations["w24_bulletins_list"];
    /** @description API endpoint that allows W24 bulletins to be viewed or edited */
    post: operations["w24_bulletins_create"];
  };
  "/w24/bulletins/{id_w24}/": {
    /** @description API endpoint that allows W24 bulletins to be viewed or edited */
    get: operations["w24_bulletins_retrieve"];
    /** @description API endpoint that allows W24 bulletins to be viewed or edited */
    put: operations["w24_bulletins_update"];
    /** @description API endpoint that allows W24 bulletins to be viewed or edited */
    delete: operations["w24_bulletins_destroy"];
    /** @description API endpoint that allows W24 bulletins to be viewed or edited */
    patch: operations["w24_bulletins_partial_update"];
  };
  "/w24/bulletins/{id_w24}/reopen/": {
    /** @description API endpoint that allows W24 bulletins to be viewed or edited */
    get: operations["w24_bulletins_reopen_retrieve"];
  };
  "/w24/bulletins/{id_w24}/send/": {
    /** @description API endpoint that allows W24 bulletins to be viewed or edited */
    get: operations["w24_bulletins_send_retrieve"];
  };
  "/w24/bulletins/bulk_update/": {
    /** @description API endpoint that allows W24 bulletins to be viewed or edited */
    post: operations["w24_bulletins_bulk_update_create"];
  };
  "/w24/bulletins/new/": {
    /** @description API endpoint that allows W24 bulletins to be viewed or edited */
    get: operations["w24_bulletins_new_retrieve"];
  };
  "/w24/current/{data_emissione}": {
    /** @description View the latest W24 bulletin sent for a certain day */
    get: operations["w24_current_retrieve"];
  };
  "/w24/data/": {
    /** @description API endpoint that allows W24 bulletin Data to be viewed or edited */
    get: operations["w24_data_list"];
    /** @description API endpoint that allows W24 bulletin Data to be viewed or edited */
    post: operations["w24_data_create"];
  };
  "/w24/data/{id_w24_data}/": {
    /** @description API endpoint that allows W24 bulletin Data to be viewed or edited */
    get: operations["w24_data_retrieve"];
    /** @description API endpoint that allows W24 bulletin Data to be viewed or edited */
    put: operations["w24_data_update"];
    /** @description API endpoint that allows W24 bulletin Data to be viewed or edited */
    delete: operations["w24_data_destroy"];
    /** @description API endpoint that allows W24 bulletin Data to be viewed or edited */
    patch: operations["w24_data_partial_update"];
  };
  "/w24/fz/": {
    get: operations["w24_fz_list"];
    post: operations["w24_fz_create"];
  };
  "/w24/fz/{id_forecast_zone}/": {
    get: operations["w24_fz_retrieve"];
    put: operations["w24_fz_update"];
    delete: operations["w24_fz_destroy"];
    patch: operations["w24_fz_partial_update"];
  };
  "/w24/soglie/": {
    /** @description API endpoint that allows W24 bulletin Data to be viewed or edited */
    get: operations["w24_soglie_list"];
    /** @description API endpoint that allows W24 bulletin Data to be viewed or edited */
    post: operations["w24_soglie_create"];
  };
  "/w24/soglie/{id_allertamento}/": {
    /** @description API endpoint that allows W24 bulletin Data to be viewed or edited */
    get: operations["w24_soglie_retrieve"];
    /** @description API endpoint that allows W24 bulletin Data to be viewed or edited */
    put: operations["w24_soglie_update"];
    /** @description API endpoint that allows W24 bulletin Data to be viewed or edited */
    delete: operations["w24_soglie_destroy"];
    /** @description API endpoint that allows W24 bulletin Data to be viewed or edited */
    patch: operations["w24_soglie_partial_update"];
  };
  "/w26/bisbulletins/": {
    /** @description API endpoint that allows W26 bulletins to be viewed or edited */
    get: operations["w26_bisbulletins_list"];
    /** @description API endpoint that allows W26 bulletins to be viewed or edited */
    post: operations["w26_bisbulletins_create"];
  };
  "/w26/bisbulletins/{codice}/": {
    /** @description API endpoint that allows W26 bulletins to be viewed or edited */
    get: operations["w26_bisbulletins_retrieve"];
    /** @description API endpoint that allows W26 bulletins to be viewed or edited */
    put: operations["w26_bisbulletins_update"];
    /** @description API endpoint that allows W26 bulletins to be viewed or edited */
    delete: operations["w26_bisbulletins_destroy"];
    /** @description API endpoint that allows W26 bulletins to be viewed or edited */
    patch: operations["w26_bisbulletins_partial_update"];
  };
  "/w26/bulletins/": {
    /** @description API endpoint that allows W26 bulletins to be viewed or edited */
    get: operations["w26_bulletins_list"];
    /** @description API endpoint that allows W26 bulletins to be viewed or edited */
    post: operations["w26_bulletins_create"];
  };
  "/w26/bulletins/{id_w26}/": {
    /** @description API endpoint that allows W26 bulletins to be viewed or edited */
    get: operations["w26_bulletins_retrieve"];
    /** @description API endpoint that allows W26 bulletins to be viewed or edited */
    put: operations["w26_bulletins_update"];
    /** @description API endpoint that allows W26 bulletins to be viewed or edited */
    delete: operations["w26_bulletins_destroy"];
    /** @description API endpoint that allows W26 bulletins to be viewed or edited */
    patch: operations["w26_bulletins_partial_update"];
  };
  "/w26/bulletins/{id_w26}/send/": {
    /** @description API endpoint that allows W26 bulletins to be viewed or edited */
    get: operations["w26_bulletins_send_retrieve"];
  };
  "/w26/bulletins/bulk_update/": {
    /** @description API endpoint that allows W26 bulletins to be viewed or edited */
    post: operations["w26_bulletins_bulk_update_create"];
  };
  "/w26/bulletins/new/{validita}/": {
    /** @description API endpoint that allows W26 bulletins to be viewed or edited */
    get: operations["w26_bulletins_new_retrieve"];
  };
  "/w26/data/": {
    /** @description API endpoint that allows W26 bulletin Data to be viewed or edited */
    get: operations["w26_data_list"];
    /** @description API endpoint that allows W26 bulletin Data to be viewed or edited */
    post: operations["w26_data_create"];
  };
  "/w26/data/{id_w26_data}/": {
    /** @description API endpoint that allows W26 bulletin Data to be viewed or edited */
    get: operations["w26_data_retrieve"];
    /** @description API endpoint that allows W26 bulletin Data to be viewed or edited */
    put: operations["w26_data_update"];
    /** @description API endpoint that allows W26 bulletin Data to be viewed or edited */
    delete: operations["w26_data_destroy"];
    /** @description API endpoint that allows W26 bulletin Data to be viewed or edited */
    patch: operations["w26_data_partial_update"];
  };
  "/w26/zone/": {
    /** @description API endpoint that allows W26 bulletin Zone to be viewed or edited */
    get: operations["w26_zone_list"];
    /** @description API endpoint that allows W26 bulletin Zone to be viewed or edited */
    post: operations["w26_zone_create"];
  };
  "/w26/zone/{id_w26_zone}/": {
    /** @description API endpoint that allows W26 bulletin Zone to be viewed or edited */
    get: operations["w26_zone_retrieve"];
    /** @description API endpoint that allows W26 bulletin Zone to be viewed or edited */
    put: operations["w26_zone_update"];
    /** @description API endpoint that allows W26 bulletin Zone to be viewed or edited */
    delete: operations["w26_zone_destroy"];
    /** @description API endpoint that allows W26 bulletin Zone to be viewed or edited */
    patch: operations["w26_zone_partial_update"];
  };
  "/w29/bulletins/": {
    /** @description API endpoint that allows W29 bulletins to be viewed or edited */
    get: operations["w29_bulletins_list"];
    /** @description API endpoint that allows W29 bulletins to be viewed or edited */
    post: operations["w29_bulletins_create"];
  };
  "/w29/bulletins/{id_w29}/": {
    /** @description API endpoint that allows W29 bulletins to be viewed or edited */
    get: operations["w29_bulletins_retrieve"];
    /** @description API endpoint that allows W29 bulletins to be viewed or edited */
    put: operations["w29_bulletins_update"];
    /** @description API endpoint that allows W29 bulletins to be viewed or edited */
    delete: operations["w29_bulletins_destroy"];
    /** @description API endpoint that allows W29 bulletins to be viewed or edited */
    patch: operations["w29_bulletins_partial_update"];
  };
  "/w29/bulletins/{id_w29}/send/": {
    /** @description API endpoint that allows W29 bulletins to be viewed or edited */
    get: operations["w29_bulletins_send_retrieve"];
  };
  "/w29/bulletins/bulk_update/": {
    /** @description API endpoint that allows W29 bulletins to be viewed or edited */
    post: operations["w29_bulletins_bulk_update_create"];
  };
  "/w29/bulletins/new/": {
    /** @description API endpoint that allows W29 bulletins to be viewed or edited */
    get: operations["w29_bulletins_new_retrieve"];
  };
  "/w29/data/": {
    /** @description API endpoint that allows W29 bulletin Data to be viewed or edited */
    get: operations["w29_data_list"];
    /** @description API endpoint that allows W29 bulletin Data to be viewed or edited */
    post: operations["w29_data_create"];
  };
  "/w29/data/{id_w29_data}/": {
    /** @description API endpoint that allows W29 bulletin Data to be viewed or edited */
    get: operations["w29_data_retrieve"];
    /** @description API endpoint that allows W29 bulletin Data to be viewed or edited */
    put: operations["w29_data_update"];
    /** @description API endpoint that allows W29 bulletin Data to be viewed or edited */
    delete: operations["w29_data_destroy"];
    /** @description API endpoint that allows W29 bulletin Data to be viewed or edited */
    patch: operations["w29_data_partial_update"];
  };
  "/w29/pericolo/": {
    /** @description API endpoint that allows W29 bulletin Pericolo to be viewed or edited */
    get: operations["w29_pericolo_list"];
    /** @description API endpoint that allows W29 bulletin Pericolo to be viewed or edited */
    post: operations["w29_pericolo_create"];
  };
  "/w29/pericolo/{id_w29_pericolo}/": {
    /** @description API endpoint that allows W29 bulletin Pericolo to be viewed or edited */
    get: operations["w29_pericolo_retrieve"];
    /** @description API endpoint that allows W29 bulletin Pericolo to be viewed or edited */
    put: operations["w29_pericolo_update"];
    /** @description API endpoint that allows W29 bulletin Pericolo to be viewed or edited */
    delete: operations["w29_pericolo_destroy"];
    /** @description API endpoint that allows W29 bulletin Pericolo to be viewed or edited */
    patch: operations["w29_pericolo_partial_update"];
  };
  "/w29/probabilita/": {
    /** @description API endpoint that allows W29 bulletin Probabilita to be viewed or edited */
    get: operations["w29_probabilita_list"];
    /** @description API endpoint that allows W29 bulletin Probabilita to be viewed or edited */
    post: operations["w29_probabilita_create"];
  };
  "/w29/probabilita/{id_w29_probabilita}/": {
    /** @description API endpoint that allows W29 bulletin Probabilita to be viewed or edited */
    get: operations["w29_probabilita_retrieve"];
    /** @description API endpoint that allows W29 bulletin Probabilita to be viewed or edited */
    put: operations["w29_probabilita_update"];
    /** @description API endpoint that allows W29 bulletin Probabilita to be viewed or edited */
    delete: operations["w29_probabilita_destroy"];
    /** @description API endpoint that allows W29 bulletin Probabilita to be viewed or edited */
    patch: operations["w29_probabilita_partial_update"];
  };
  "/w29/zone/": {
    /** @description API endpoint that allows W29 bulletin Zone to be viewed or edited */
    get: operations["w29_zone_list"];
    /** @description API endpoint that allows W29 bulletin Zone to be viewed or edited */
    post: operations["w29_zone_create"];
  };
  "/w29/zone/{id_w29_zone}/": {
    /** @description API endpoint that allows W29 bulletin Zone to be viewed or edited */
    get: operations["w29_zone_retrieve"];
    /** @description API endpoint that allows W29 bulletin Zone to be viewed or edited */
    put: operations["w29_zone_update"];
    /** @description API endpoint that allows W29 bulletin Zone to be viewed or edited */
    delete: operations["w29_zone_destroy"];
    /** @description API endpoint that allows W29 bulletin Zone to be viewed or edited */
    patch: operations["w29_zone_partial_update"];
  };
  "/w30/bulletins/": {
    /** @description API endpoint that allows W30 bulletins to be viewed or edited */
    get: operations["w30_bulletins_list"];
    /** @description API endpoint that allows W30 bulletins to be viewed or edited */
    post: operations["w30_bulletins_create"];
  };
  "/w30/bulletins/{id_w30}/": {
    /** @description API endpoint that allows W30 bulletins to be viewed or edited */
    get: operations["w30_bulletins_retrieve"];
    /** @description API endpoint that allows W30 bulletins to be viewed or edited */
    put: operations["w30_bulletins_update"];
    /** @description API endpoint that allows W30 bulletins to be viewed or edited */
    delete: operations["w30_bulletins_destroy"];
    /** @description API endpoint that allows W30 bulletins to be viewed or edited */
    patch: operations["w30_bulletins_partial_update"];
  };
  "/w30/bulletins/{id_w30}/reopen/": {
    /** @description API endpoint that allows W30 bulletins to be viewed or edited */
    get: operations["w30_bulletins_reopen_retrieve"];
  };
  "/w30/bulletins/{id_w30}/send/": {
    /** @description API endpoint that allows W30 bulletins to be viewed or edited */
    get: operations["w30_bulletins_send_retrieve"];
  };
  "/w30/bulletins/new/": {
    /** @description API endpoint that allows W30 bulletins to be viewed or edited */
    get: operations["w30_bulletins_new_retrieve"];
  };
  "/w30/current/{data_emissione}": {
    /** @description View the latest W30 bulletin sent for a certain day */
    get: operations["w30_current_retrieve"];
  };
  "/w30/currentdata/{data_emissione}": {
    /** @description View the aggregated bulletin Data for the last 4 bulletins from the supplied date backwards */
    get: operations["w30_currentdata_list"];
  };
  "/w30/data/": {
    /** @description API endpoint that allows W30 bulletin Data to be viewed or edited */
    get: operations["w30_data_list"];
    /** @description API endpoint that allows W30 bulletin Data to be viewed or edited */
    post: operations["w30_data_create"];
  };
  "/w30/data/{id_w30_data}/": {
    /** @description API endpoint that allows W30 bulletin Data to be viewed or edited */
    get: operations["w30_data_retrieve"];
    /** @description API endpoint that allows W30 bulletin Data to be viewed or edited */
    put: operations["w30_data_update"];
    /** @description API endpoint that allows W30 bulletin Data to be viewed or edited */
    delete: operations["w30_data_destroy"];
    /** @description API endpoint that allows W30 bulletin Data to be viewed or edited */
    patch: operations["w30_data_partial_update"];
  };
  "/w30/data/bulk_update/": {
    /** @description API endpoint that allows W30 bulletin Data to be viewed or edited */
    post: operations["w30_data_bulk_update_create"];
  };
  "/w31/bulletins/": {
    /** @description API endpoint that allows W31 bulletins to be viewed or edited */
    get: operations["w31_bulletins_list"];
    /** @description API endpoint that allows W31 bulletins to be viewed or edited */
    post: operations["w31_bulletins_create"];
  };
  "/w31/bulletins/{id_w31}/": {
    /** @description API endpoint that allows W31 bulletins to be viewed or edited */
    get: operations["w31_bulletins_retrieve"];
    /** @description API endpoint that allows W31 bulletins to be viewed or edited */
    put: operations["w31_bulletins_update"];
    /** @description API endpoint that allows W31 bulletins to be viewed or edited */
    delete: operations["w31_bulletins_destroy"];
    /** @description API endpoint that allows W31 bulletins to be viewed or edited */
    patch: operations["w31_bulletins_partial_update"];
  };
  "/w31/bulletins/{id_w31}/copy/": {
    /** @description API endpoint that allows W31 bulletins to be viewed or edited */
    get: operations["w31_bulletins_copy_retrieve"];
  };
  "/w31/bulletins/{id_w31}/reopen/": {
    /** @description API endpoint that allows W31 bulletins to be viewed or edited */
    get: operations["w31_bulletins_reopen_retrieve"];
  };
  "/w31/bulletins/{id_w31}/send/": {
    /** @description API endpoint that allows W31 bulletins to be viewed or edited */
    get: operations["w31_bulletins_send_retrieve"];
  };
  "/w31/bulletins/bulk_update/": {
    /** @description API endpoint that allows W31 bulletins to be viewed or edited */
    post: operations["w31_bulletins_bulk_update_create"];
  };
  "/w31/bulletins/new/": {
    /** @description API endpoint that allows W31 bulletins to be viewed or edited */
    get: operations["w31_bulletins_new_retrieve"];
  };
  "/w31/current/{emissione}": {
    /** @description View the latest W31 bulletin sent */
    get: operations["w31_current_retrieve"];
  };
  "/w31/data/": {
    /** @description API endpoint that allows W31 bulletin Data to be viewed or updated */
    get: operations["w31_data_list"];
    /** @description API endpoint that allows W31 bulletin Data to be viewed or updated */
    post: operations["w31_data_create"];
  };
  "/w31/data/{id_w31_data_macroaree_livelli}/": {
    /** @description API endpoint that allows W31 bulletin Data to be viewed or updated */
    get: operations["w31_data_retrieve"];
    /** @description API endpoint that allows W31 bulletin Data to be viewed or updated */
    put: operations["w31_data_update"];
    /** @description API endpoint that allows W31 bulletin Data to be viewed or updated */
    delete: operations["w31_data_destroy"];
    /** @description API endpoint that allows W31 bulletin Data to be viewed or updated */
    patch: operations["w31_data_partial_update"];
  };
  "/w31/levels/": {
    /** @description API endpoint that allows W31 levels to be viewed */
    get: operations["w31_levels_list"];
    /** @description API endpoint that allows W31 levels to be viewed */
    post: operations["w31_levels_create"];
  };
  "/w31/levels/{id_w31_livelli}/": {
    /** @description API endpoint that allows W31 levels to be viewed */
    get: operations["w31_levels_retrieve"];
    /** @description API endpoint that allows W31 levels to be viewed */
    put: operations["w31_levels_update"];
    /** @description API endpoint that allows W31 levels to be viewed */
    delete: operations["w31_levels_destroy"];
    /** @description API endpoint that allows W31 levels to be viewed */
    patch: operations["w31_levels_partial_update"];
  };
}

export type webhooks = Record<string, never>;

export interface components {
  schemas: {
    BisBollettinoWebolimpia: {
      codice?: string;
      /** Format: date-time */
      data?: string | null;
      numero?: number | null;
      /** Format: double */
      h_min?: number | null;
      /** Format: double */
      h_max?: number | null;
      /** Format: double */
      h_med?: number | null;
      /** Format: double */
      q_min?: number | null;
      /** Format: double */
      q_max?: number | null;
      /** Format: double */
      q_med?: number | null;
      corso_acqua?: string | null;
      localita?: string | null;
      id_note?: number;
      note?: string | null;
    };
    Classes: {
      id_classes: number;
      id_parametro: string;
      description?: string | null;
      classes_value: readonly (components["schemas"]["ClassesValue"])[];
    };
    ClassesValue: {
      id_classes_value: number;
      description: string;
    };
    ForecastZone: {
      id_forecast_zone: number;
      model_name: string;
      model_type: string;
      /** Format: date-time */
      data_emissione: string;
      /** Format: date-time */
      data_riferimento: string;
      /** Format: decimal */
      valore_originale?: string | null;
      /** Format: decimal */
      valore_validato?: string | null;
      /** Format: date-time */
      last_update: string;
      username: string;
      id_allertamento: string;
      id_parametro: string;
      id_aggregazione: number;
    };
    MyTokenObtainPair: {
      username: string;
      password: string;
    };
    OzonoLivelli: {
      id_ozono_livelli: number;
      livelli: number;
      rgb: string;
      soglia_inferiore_mxd: number;
      soglia_inferiore_mx8: number;
      sintesi_raccomandazioni?: string | null;
      descrizione?: string | null;
      raccomandazione?: string | null;
    };
    PaginatedW05List: {
      /** @example 123 */
      count?: number;
      /**
       * Format: uri 
       * @example http://api.example.org/accounts/?page=4
       */
      next?: string | null;
      /**
       * Format: uri 
       * @example http://api.example.org/accounts/?page=2
       */
      previous?: string | null;
      results?: (components["schemas"]["W05"])[];
    };
    PaginatedW16List: {
      /** @example 123 */
      count?: number;
      /**
       * Format: uri 
       * @example http://api.example.org/accounts/?page=4
       */
      next?: string | null;
      /**
       * Format: uri 
       * @example http://api.example.org/accounts/?page=2
       */
      previous?: string | null;
      results?: (components["schemas"]["W16"])[];
    };
    PaginatedW22List: {
      /** @example 123 */
      count?: number;
      /**
       * Format: uri 
       * @example http://api.example.org/accounts/?page=4
       */
      next?: string | null;
      /**
       * Format: uri 
       * @example http://api.example.org/accounts/?page=2
       */
      previous?: string | null;
      results?: (components["schemas"]["W22"])[];
    };
    PaginatedW22VerificaList: {
      /** @example 123 */
      count?: number;
      /**
       * Format: uri 
       * @example http://api.example.org/accounts/?page=4
       */
      next?: string | null;
      /**
       * Format: uri 
       * @example http://api.example.org/accounts/?page=2
       */
      previous?: string | null;
      results?: (components["schemas"]["W22Verifica"])[];
    };
    PaginatedW23List: {
      /** @example 123 */
      count?: number;
      /**
       * Format: uri 
       * @example http://api.example.org/accounts/?page=4
       */
      next?: string | null;
      /**
       * Format: uri 
       * @example http://api.example.org/accounts/?page=2
       */
      previous?: string | null;
      results?: (components["schemas"]["W23"])[];
    };
    PaginatedW24List: {
      /** @example 123 */
      count?: number;
      /**
       * Format: uri 
       * @example http://api.example.org/accounts/?page=4
       */
      next?: string | null;
      /**
       * Format: uri 
       * @example http://api.example.org/accounts/?page=2
       */
      previous?: string | null;
      results?: (components["schemas"]["W24"])[];
    };
    PaginatedW26List: {
      /** @example 123 */
      count?: number;
      /**
       * Format: uri 
       * @example http://api.example.org/accounts/?page=4
       */
      next?: string | null;
      /**
       * Format: uri 
       * @example http://api.example.org/accounts/?page=2
       */
      previous?: string | null;
      results?: (components["schemas"]["W26"])[];
    };
    PaginatedW29List: {
      /** @example 123 */
      count?: number;
      /**
       * Format: uri 
       * @example http://api.example.org/accounts/?page=4
       */
      next?: string | null;
      /**
       * Format: uri 
       * @example http://api.example.org/accounts/?page=2
       */
      previous?: string | null;
      results?: (components["schemas"]["W29"])[];
    };
    PaginatedW30List: {
      /** @example 123 */
      count?: number;
      /**
       * Format: uri 
       * @example http://api.example.org/accounts/?page=4
       */
      next?: string | null;
      /**
       * Format: uri 
       * @example http://api.example.org/accounts/?page=2
       */
      previous?: string | null;
      results?: (components["schemas"]["W30"])[];
    };
    PaginatedW31List: {
      /** @example 123 */
      count?: number;
      /**
       * Format: uri 
       * @example http://api.example.org/accounts/?page=4
       */
      next?: string | null;
      /**
       * Format: uri 
       * @example http://api.example.org/accounts/?page=2
       */
      previous?: string | null;
      results?: (components["schemas"]["W31"])[];
    };
    PatchedBisBollettinoWebolimpia: {
      codice?: string;
      /** Format: date-time */
      data?: string | null;
      numero?: number | null;
      /** Format: double */
      h_min?: number | null;
      /** Format: double */
      h_max?: number | null;
      /** Format: double */
      h_med?: number | null;
      /** Format: double */
      q_min?: number | null;
      /** Format: double */
      q_max?: number | null;
      /** Format: double */
      q_med?: number | null;
      corso_acqua?: string | null;
      localita?: string | null;
      id_note?: number;
      note?: string | null;
    };
    PatchedClasses: {
      id_classes?: number;
      id_parametro?: string;
      description?: string | null;
      classes_value?: readonly (components["schemas"]["ClassesValue"])[];
    };
    PatchedForecastZone: {
      id_forecast_zone?: number;
      model_name?: string;
      model_type?: string;
      /** Format: date-time */
      data_emissione?: string;
      /** Format: date-time */
      data_riferimento?: string;
      /** Format: decimal */
      valore_originale?: string | null;
      /** Format: decimal */
      valore_validato?: string | null;
      /** Format: date-time */
      last_update?: string;
      username?: string;
      id_allertamento?: string;
      id_parametro?: string;
      id_aggregazione?: number;
    };
    PatchedOzonoLivelli: {
      id_ozono_livelli?: number;
      livelli?: number;
      rgb?: string;
      soglia_inferiore_mxd?: number;
      soglia_inferiore_mx8?: number;
      sintesi_raccomandazioni?: string | null;
      descrizione?: string | null;
      raccomandazione?: string | null;
    };
    PatchedSkyCondition: {
      id_sky_condition?: number;
      sky_condition?: string;
      description?: string;
      description_ita?: string;
      classes?: (components["schemas"]["SkyConditionClasses"])[];
    };
    PatchedSoglieNivoAreaPrev: {
      idtab_allertamento?: string;
      ambito?: string;
      /** Format: decimal */
      soglia_cod1?: string | null;
      /** Format: decimal */
      soglia_cod2?: string | null;
      /** Format: decimal */
      soglia_cod3?: string | null;
    };
    PatchedSogliePluvAreaPrevMassimi: {
      idtab_allertamento?: string;
      codice_allertamento?: string;
      /** Format: decimal */
      h6?: string | null;
      /** Format: decimal */
      h12?: string | null;
      /** Format: decimal */
      h24?: string | null;
    };
    PatchedSogliePluvAreaPrevMedie: {
      idtab_allertamento?: string;
      codice_allertamento?: string;
      /** Format: decimal */
      h6?: string | null;
      /** Format: decimal */
      h12?: string | null;
      /** Format: decimal */
      h24?: string | null;
      /** Format: decimal */
      h48?: string | null;
    };
    PatchedTimeLayouts: {
      id_time_layouts?: number;
      start_day_offset?: number;
      end_day_offset?: number | null;
      /** Format: time */
      start_time?: string;
      /** Format: time */
      end_time?: string;
    };
    PatchedVenue: {
      id_venue?: number;
      description?: string;
      /** Format: decimal */
      altitude?: string | null;
      /** Format: date-time */
      last_update?: string;
      username?: string;
    };
    PatchedW05: {
      id_w05?: number;
      /** Format: date-time */
      start_valid_time?: string;
      validity?: number;
      /** Format: date-time */
      next_blt_time?: string;
      situation?: string | null;
      status?: string;
      /** Format: date-time */
      last_update?: string;
      username?: string;
      /** Format: int64 */
      seq_num?: number | null;
      /** Format: int64 */
      version?: number | null;
      id_w05_parent?: number | null;
      /** Format: byte */
      situation_image?: string | null;
    };
    PatchedW05Classes: {
      id_w05_classes?: number;
      /** Format: date-time */
      start_valid_time?: string;
      /** Format: date-time */
      end_valid_time?: string;
      id_w05?: number;
      id_venue?: number;
      id_parametro?: string;
      id_aggregazione?: number;
      id_classes_value?: number;
      id_classes?: number;
      id_time_layouts?: number;
    };
    PatchedW05Data: {
      id_w05_data?: number;
      /** Format: decimal */
      numeric_value?: string | null;
      text_value?: string | null;
      /** Format: date-time */
      start_valid_time?: string;
      /** Format: date-time */
      end_valid_time?: string;
      id_w05?: number;
      id_venue?: number;
      id_parametro?: string;
      id_aggregazione?: number;
      id_trend?: number | null;
      id_time_layouts?: number;
    };
    PatchedW16: {
      id_w16?: number;
      /** Format: date-time */
      start_valid_time?: string;
      validity?: number;
      /** Format: date-time */
      next_blt_time?: string;
      made_by?: string;
      note?: string;
      status?: string;
      /** Format: date-time */
      last_update?: string;
      username?: string;
      /** Format: int64 */
      seq_num?: number | null;
      /** Format: int64 */
      version?: number | null;
      id_w16_parent?: number | null;
    };
    PatchedW16Conf: {
      id_w16_conf?: number;
      /** Format: date-time */
      last_update?: string;
      username?: string;
      id_ozono_aggregazione?: number;
    };
    PatchedW16Data: {
      id_w16_data?: number;
      w16data1_set?: readonly (components["schemas"]["W16Data1"])[];
      /** Format: date-time */
      data_emissione?: string;
      /** Format: date-time */
      data_scadenza?: string;
      id_scadenza?: number;
      id_w16?: number;
      id_ozono_zone?: number;
      id_ozono_livelli?: number;
    };
    PatchedW22: {
      id_w22?: number;
      /** Format: date */
      data_emissione?: string;
      ora_emissione?: string;
      /** Format: date */
      data_validita?: string;
      numero_bollettino?: string;
      annotazione?: string | null;
      situazione_evoluzione?: string | null;
      status?: string;
      pdf_ordinario?: string;
      /** Format: date-time */
      last_update?: string;
      username?: string;
      validita?: string | null;
    };
    PatchedW22Criticita: {
      id_w22_criticita?: string;
      descrizione?: string | null;
      colore_html?: string;
    };
    PatchedW22Data: {
      id_w22_data?: number;
      id_w22_zone?: components["schemas"]["W22Zone"];
      codice1?: string | null;
      codice2?: string | null;
      codice3?: string | null;
      tendenza6hprecedenti?: string | null;
      portata_attesa?: string | null;
      criticita_attesa?: string | null;
      prev_crit12h?: string | null;
      prev_crit24h?: string | null;
      prev_crit36h?: string | null;
      tend48h?: string | null;
      massimo_previsione?: string | null;
      data_massimo_storico?: string | null;
      valore_massimo_storico?: string | null;
      id_w22?: number;
    };
    PatchedW22Giudizio: {
      /** Format: int64 */
      id_w22giudizio?: number;
      descrizione?: string | null;
      colore_html?: string;
    };
    PatchedW22Severita: {
      /** Format: int64 */
      id_w22severita?: number;
      sigla?: string;
      descrizione?: string | null;
      colore_html?: string;
    };
    PatchedW22Tendenza: {
      id_w22_tendenza?: string;
      descrizione?: string | null;
    };
    PatchedW22Verifica: {
      id_w22verifica?: number;
      id_numero_bollettino?: string;
      numero_bollettino?: string;
      /** Format: date */
      data_emissione?: string;
      /** Format: date */
      data_analisi?: string;
      /** Format: int64 */
      id_w22giudizio?: number;
      annotazione?: string | null;
      situazione_evoluzione?: string | null;
      status?: string;
      /** Format: date-time */
      last_update?: string;
      username?: string;
    };
    PatchedW22VerificaData: {
      id_w22verifica_data?: number;
      id_w22_zone?: components["schemas"]["W22Zone"];
      prev_crit_tot?: string | null;
      oss_crit_tot?: string | null;
      err_crit_tot?: string | null;
      id_w22verifica?: number;
    };
    PatchedW22Zone: {
      id_w22_zone?: number;
      codice_istat_comune?: string;
      progr_punto_com?: number;
      denominazione_stazione?: string;
      corso_acqua?: string;
      id_parametro?: string | null;
    };
    PatchedW23: {
      id_w23?: number;
      /** Format: date */
      data_emissione?: string;
      numero_bollettino?: string;
      situazione_meteo?: string | null;
      status?: string;
      /** Format: date-time */
      last_update?: string;
      username?: string;
      fraserisknat?: string | null;
      annotazione?: string | null;
      /** Format: date-time */
      last_update_annotazione?: string;
      id_w23_parent?: number | null;
    };
    PatchedW23Data: {
      id_w23_data?: number;
      id_w23_zone?: components["schemas"]["W23Zone"];
      scenario_atteso?: string | null;
      scenario_atteso_for?: string | null;
      pluvmax12hd0?: string | null;
      pluvmax12hd1?: string | null;
      pluvmax24hd1?: string | null;
      pluvmax6h18g0?: string | null;
      pluvmax6h00g1?: string | null;
      pluvmax6h06g1?: string | null;
      pluvmax6h12g1?: string | null;
      pluvmax6h18g1?: string | null;
      pluvmax6h00g2?: string | null;
      pluvmax6h06g2?: string | null;
      pluvmax6h12g2?: string | null;
      pluvmax6h18g2?: string | null;
      pluvmax6h00g3?: string | null;
      pluvmed6h18g0?: string | null;
      pluvmed6h00g1?: string | null;
      pluvmed6h06g1?: string | null;
      pluvmed6h12g1?: string | null;
      pluvmed6h18g1?: string | null;
      pluvmed6h00g2?: string | null;
      pluvmed6h06g2?: string | null;
      pluvmed6h12g2?: string | null;
      pluvmed6h18g2?: string | null;
      pluvmed6h00g3?: string | null;
      pluvmed12h18g0_oss?: string | null;
      pluvmed12h00g1?: string | null;
      pluvmed12h06g1?: string | null;
      pluvmed12h12g1?: string | null;
      pluvmed12h18g1?: string | null;
      pluvmed12h00g2?: string | null;
      pluvmed12h06g2?: string | null;
      pluvmed12h12g2?: string | null;
      pluvmed12h18g2?: string | null;
      pluvmed12h00g3?: string | null;
      pluvmed24h18g0_oss?: string | null;
      pluvmed24h00g1_oss?: string | null;
      pluvmed24h06g1_oss?: string | null;
      pluvmed24h12g1?: string | null;
      pluvmed24h18g1?: string | null;
      pluvmed24h00g2?: string | null;
      pluvmed24h06g2?: string | null;
      pluvmed24h12g2?: string | null;
      pluvmed24h18g2?: string | null;
      pluvmed24h00g3?: string | null;
      pluvmed48h18g0_oss?: string | null;
      pluvmed48h00g1_oss?: string | null;
      pluvmed48h06g1_oss?: string | null;
      pluvmed48h12g1_oss?: string | null;
      pluvmed48h18g1_oss?: string | null;
      pluvmed48h00g2_oss?: string | null;
      pluvmed48h06g2_oss?: string | null;
      pluvmed48h12g2?: string | null;
      pluvmed48h18g2?: string | null;
      pluvmed48h00g3?: string | null;
      neveqmin?: string | null;
      neveqmax?: string | null;
      neve400_oggi?: string | null;
      neve400_domani?: string | null;
      neve400_totale?: string | null;
      neve700_oggi?: string | null;
      neve700_domani?: string | null;
      neve700_totale?: string | null;
      neve1000_oggi?: string | null;
      neve1000_domani?: string | null;
      neve1000_totale?: string | null;
      temporale_oggi?: string | null;
      temporale_domani?: string | null;
      neveqd01?: string | null;
      neveqd02?: string | null;
      neveqd11?: string | null;
      neveqd12?: string | null;
      neveqd13?: string | null;
      neveqd14?: string | null;
      id_w23?: number;
      idrogeologico_oggi?: string;
      idrogeologico_domani?: string;
      temporali_oggi?: string;
      temporali_domani?: string;
      idraulico_oggi?: string;
      idraulico_domani?: string;
      neve_oggi?: string;
      neve_domani?: string;
      valanghe_oggi?: string;
      valanghe_domani?: string;
      idrogeologico_oggi_for?: string | null;
      idrogeologico_domani_for?: string | null;
      temporali_oggi_for?: string | null;
      temporali_domani_for?: string | null;
      idraulico_oggi_for?: string | null;
      idraulico_domani_for?: string | null;
      neve_oggi_for?: string | null;
      neve_domani_for?: string | null;
      valanghe_oggi_for?: string | null;
      valanghe_domani_for?: string | null;
    };
    PatchedW23Effettiterritorio: {
      id_w23_effettiterritorio?: string;
      descrizione?: string | null;
    };
    PatchedW23Pericolo: {
      id_w23_pericolo?: string;
      colore_html?: string;
      sort_index?: number;
    };
    PatchedW23Pluvossh6: {
      id_w23_pluvossh6?: number;
      /** Format: date */
      data?: string;
      /** Format: time */
      ora?: string;
      area?: string;
      valore?: string | null;
    };
    PatchedW23Zone: {
      id_w23_zone?: number;
      zona_allerta?: string;
      bacino?: string;
      provincia?: string;
      nome_zona?: string | null;
    };
    PatchedW24: {
      id_w24?: number;
      numero_bollettino?: string;
      /** Format: date */
      data_emissione?: string;
      /** Format: date */
      next_blt_time?: string;
      sintesi_meteo?: string | null;
      status?: string;
      /** Format: date-time */
      last_update?: string;
      username?: string;
      tipo_anomalia_termica?: string | null;
      forzante_0?: string;
      forzante_1?: string;
      forzante_2?: string;
      id_w24_parent?: number | null;
    };
    PatchedW24Data: {
      id_w24_data?: number;
      /** Format: decimal */
      numeric_value?: string;
      id_w24?: number;
      id_allertamento?: string;
      id_time_layouts?: number;
      id_parametro?: string;
    };
    PatchedW24Soglie: {
      id_allertamento?: string;
      /** Format: decimal */
      soglia1?: string;
      /** Format: decimal */
      soglia2?: string;
      classe_intensita?: number;
      /** Format: date-time */
      last_update?: string;
      username?: string;
      id_parametro?: string;
      id_aggregazione?: number;
    };
    PatchedW26: {
      id_w26?: number;
      /** Format: date */
      data_emissione?: string;
      numero_bollettino?: string;
      status?: string;
      /** Format: date-time */
      last_update?: string;
      username?: string;
      /** Format: date */
      data_validita?: string;
    };
    PatchedW26Data: {
      id_w26_data?: number;
      id_w26_zone?: components["schemas"]["W26Zone"];
      hmin?: string | null;
      hmax?: string | null;
      hmed?: string | null;
      qmin?: string | null;
      qmax?: string | null;
      qmed?: string | null;
      nota?: string | null;
      idnota?: string | null;
      id_w26?: number;
    };
    PatchedW26Zone: {
      id_w26_zone?: number;
      codice?: string;
      localita?: string;
      corsoacqua?: string;
      numero?: number;
    };
    PatchedW29: {
      id_w29?: number;
      /** Format: date */
      data_emissione?: string;
      ora_emissione?: string;
      ora_simulazione?: string;
      numero_bollettino?: string;
      situazione_evoluzione?: string | null;
      status?: string;
      /** Format: date-time */
      last_update?: string;
      username?: string;
      /** Format: date */
      data_validita?: string;
      ora_osservazione?: string | null;
      data_osservazione?: string | null;
      data_simulazione?: string | null;
      note?: string | null;
    };
    PatchedW29Data: {
      id_w29_data?: number;
      id_w29_zone?: components["schemas"]["W29Zone"];
      livello_criticita_oss?: string;
      probabilita_criticita_oss?: string;
      livello_criticita_prev_oggi?: string;
      probabilita_criticita_prev_oggi?: string;
      livello_criticita_prev_domani?: string;
      probabilita_criticita_prev_domani?: string;
      id_w29?: number;
    };
    PatchedW29Pericolo: {
      id_w29_pericolo?: string;
      descrizione?: string | null;
    };
    PatchedW29Probabilita: {
      id_w29_probabilita?: string;
      descrizione?: string | null;
    };
    PatchedW29Zone: {
      id_w29_zone?: number;
      descrizione?: string;
    };
    PatchedW30: {
      id_w30?: number;
      /** Format: int64 */
      seq_num?: number | null;
      /** Format: date-time */
      data_emissione?: string;
      /** Format: date-time */
      data_prossimo_aggiornamento?: string;
      status?: string;
      /** Format: date-time */
      last_update?: string;
      username?: string;
      id_w30_parent?: number | null;
      firstguess?: string;
    };
    PatchedW30Data: {
      id_w30_data?: number;
      numeric_value?: number | null;
      id_w30?: number;
      id_allertamento?: string;
      id_time_layouts?: number;
      id_parametro?: string;
      id_aggregazione?: number;
    };
    PatchedW31: {
      id_w31?: number;
      /** Format: date-time */
      start_valid_time?: string;
      validity?: number;
      /** Format: date-time */
      next_blt_time?: string;
      status?: string;
      /** Format: date-time */
      last_update?: string;
      username?: string;
      /** Format: int64 */
      seq_num?: number | null;
      /** Format: int64 */
      version?: number | null;
      algoritmo?: string;
      id_w31_parent?: number | null;
      annotazione?: string | null;
    };
    PatchedW31DataMacroareeLivelli: {
      id_w31_data_macroaree_livelli?: number;
      id_w31_macroaree?: components["schemas"]["W31Macroaree"];
      id_w31?: number;
      id_w31_livelli?: number;
      id_time_layouts?: number;
    };
    PatchedW31Livelli: {
      id_w31_livelli?: number;
      colore?: string;
    };
    SkyCondition: {
      id_sky_condition: number;
      sky_condition: string;
      description: string;
      description_ita: string;
      classes: (components["schemas"]["SkyConditionClasses"])[];
    };
    SkyConditionClasses: {
      id_parametro: string;
      ordinamento: number;
    };
    SoglieNivoAreaPrev: {
      idtab_allertamento: string;
      ambito: string;
      /** Format: decimal */
      soglia_cod1?: string | null;
      /** Format: decimal */
      soglia_cod2?: string | null;
      /** Format: decimal */
      soglia_cod3?: string | null;
    };
    SogliePluvAreaPrevMassimi: {
      idtab_allertamento: string;
      codice_allertamento: string;
      /** Format: decimal */
      h6?: string | null;
      /** Format: decimal */
      h12?: string | null;
      /** Format: decimal */
      h24?: string | null;
    };
    SogliePluvAreaPrevMedie: {
      idtab_allertamento: string;
      codice_allertamento: string;
      /** Format: decimal */
      h6?: string | null;
      /** Format: decimal */
      h12?: string | null;
      /** Format: decimal */
      h24?: string | null;
      /** Format: decimal */
      h48?: string | null;
    };
    TimeLayouts: {
      id_time_layouts: number;
      start_day_offset: number;
      end_day_offset?: number | null;
      /** Format: time */
      start_time: string;
      /** Format: time */
      end_time: string;
    };
    TokenRefresh: {
      access: string;
      refresh: string;
    };
    TokenVerify: {
      token: string;
    };
    Venue: {
      id_venue: number;
      description: string;
      /** Format: decimal */
      altitude?: string | null;
      /** Format: date-time */
      last_update: string;
      username: string;
    };
    W05: {
      id_w05: number;
      /** Format: date-time */
      start_valid_time: string;
      validity: number;
      /** Format: date-time */
      next_blt_time: string;
      situation?: string | null;
      status: string;
      /** Format: date-time */
      last_update: string;
      username: string;
      /** Format: int64 */
      seq_num?: number | null;
      /** Format: int64 */
      version?: number | null;
      id_w05_parent?: number | null;
      /** Format: byte */
      situation_image: string | null;
    };
    W05Classes: {
      id_w05_classes: number;
      /** Format: date-time */
      start_valid_time: string;
      /** Format: date-time */
      end_valid_time: string;
      id_w05: number;
      id_venue: number;
      id_parametro: string;
      id_aggregazione: number;
      id_classes_value: number;
      id_classes: number;
      id_time_layouts: number;
    };
    W05Data: {
      id_w05_data: number;
      /** Format: decimal */
      numeric_value?: string | null;
      text_value?: string | null;
      /** Format: date-time */
      start_valid_time: string;
      /** Format: date-time */
      end_valid_time: string;
      id_w05: number;
      id_venue: number;
      id_parametro: string;
      id_aggregazione: number;
      id_trend?: number | null;
      id_time_layouts: number;
    };
    W16: {
      id_w16: number;
      /** Format: date-time */
      start_valid_time: string;
      validity: number;
      /** Format: date-time */
      next_blt_time: string;
      made_by: string;
      note: string;
      status: string;
      /** Format: date-time */
      last_update: string;
      username: string;
      /** Format: int64 */
      seq_num?: number | null;
      /** Format: int64 */
      version?: number | null;
      id_w16_parent?: number | null;
    };
    W16Conf: {
      id_w16_conf: number;
      /** Format: date-time */
      last_update: string;
      username: string;
      id_ozono_aggregazione: number;
    };
    W16Data: {
      id_w16_data: number;
      w16data1_set: readonly (components["schemas"]["W16Data1"])[];
      /** Format: date-time */
      data_emissione: string;
      /** Format: date-time */
      data_scadenza: string;
      id_scadenza: number;
      id_w16: number;
      id_ozono_zone: number;
      id_ozono_livelli: number;
    };
    W16Data1: {
      id_w16_data1: number;
      id_qa_parametro: string;
      /** Format: decimal */
      valore_num?: string | null;
      valore_classe?: number | null;
      id_strumentazione?: number | null;
      id_w16_data: number;
      id_ozono_aggregazione: number;
    };
    W22: {
      id_w22: number;
      /** Format: date */
      data_emissione: string;
      ora_emissione: string;
      /** Format: date */
      data_validita: string;
      numero_bollettino: string;
      annotazione?: string | null;
      situazione_evoluzione?: string | null;
      status: string;
      pdf_ordinario: string;
      /** Format: date-time */
      last_update: string;
      username: string;
      validita?: string | null;
    };
    W22Criticita: {
      id_w22_criticita: string;
      descrizione?: string | null;
      colore_html: string;
    };
    W22Data: {
      id_w22_data: number;
      id_w22_zone: components["schemas"]["W22Zone"];
      codice1?: string | null;
      codice2?: string | null;
      codice3?: string | null;
      tendenza6hprecedenti?: string | null;
      portata_attesa?: string | null;
      criticita_attesa?: string | null;
      prev_crit12h?: string | null;
      prev_crit24h?: string | null;
      prev_crit36h?: string | null;
      tend48h?: string | null;
      massimo_previsione?: string | null;
      data_massimo_storico?: string | null;
      valore_massimo_storico?: string | null;
      id_w22: number;
    };
    W22Giudizio: {
      /** Format: int64 */
      id_w22giudizio: number;
      descrizione?: string | null;
      colore_html: string;
    };
    W22Severita: {
      /** Format: int64 */
      id_w22severita: number;
      sigla: string;
      descrizione?: string | null;
      colore_html: string;
    };
    W22Tendenza: {
      id_w22_tendenza: string;
      descrizione?: string | null;
    };
    W22Verifica: {
      id_w22verifica: number;
      id_numero_bollettino: string;
      numero_bollettino: string;
      /** Format: date */
      data_emissione: string;
      /** Format: date */
      data_analisi: string;
      /** Format: int64 */
      id_w22giudizio: number;
      annotazione?: string | null;
      situazione_evoluzione?: string | null;
      status: string;
      /** Format: date-time */
      last_update: string;
      username: string;
    };
    W22VerificaData: {
      id_w22verifica_data: number;
      id_w22_zone: components["schemas"]["W22Zone"];
      prev_crit_tot?: string | null;
      oss_crit_tot?: string | null;
      err_crit_tot?: string | null;
      id_w22verifica: number;
    };
    W22Zone: {
      id_w22_zone: number;
      codice_istat_comune: string;
      progr_punto_com: number;
      denominazione_stazione: string;
      corso_acqua: string;
      id_parametro?: string | null;
    };
    W23: {
      id_w23: number;
      /** Format: date */
      data_emissione: string;
      numero_bollettino: string;
      situazione_meteo?: string | null;
      status: string;
      /** Format: date-time */
      last_update: string;
      username: string;
      fraserisknat?: string | null;
      annotazione?: string | null;
      /** Format: date-time */
      last_update_annotazione: string;
      id_w23_parent?: number | null;
    };
    W23Data: {
      id_w23_data: number;
      id_w23_zone: components["schemas"]["W23Zone"];
      scenario_atteso?: string | null;
      scenario_atteso_for?: string | null;
      pluvmax12hd0?: string | null;
      pluvmax12hd1?: string | null;
      pluvmax24hd1?: string | null;
      pluvmax6h18g0?: string | null;
      pluvmax6h00g1?: string | null;
      pluvmax6h06g1?: string | null;
      pluvmax6h12g1?: string | null;
      pluvmax6h18g1?: string | null;
      pluvmax6h00g2?: string | null;
      pluvmax6h06g2?: string | null;
      pluvmax6h12g2?: string | null;
      pluvmax6h18g2?: string | null;
      pluvmax6h00g3?: string | null;
      pluvmed6h18g0?: string | null;
      pluvmed6h00g1?: string | null;
      pluvmed6h06g1?: string | null;
      pluvmed6h12g1?: string | null;
      pluvmed6h18g1?: string | null;
      pluvmed6h00g2?: string | null;
      pluvmed6h06g2?: string | null;
      pluvmed6h12g2?: string | null;
      pluvmed6h18g2?: string | null;
      pluvmed6h00g3?: string | null;
      pluvmed12h18g0_oss?: string | null;
      pluvmed12h00g1?: string | null;
      pluvmed12h06g1?: string | null;
      pluvmed12h12g1?: string | null;
      pluvmed12h18g1?: string | null;
      pluvmed12h00g2?: string | null;
      pluvmed12h06g2?: string | null;
      pluvmed12h12g2?: string | null;
      pluvmed12h18g2?: string | null;
      pluvmed12h00g3?: string | null;
      pluvmed24h18g0_oss?: string | null;
      pluvmed24h00g1_oss?: string | null;
      pluvmed24h06g1_oss?: string | null;
      pluvmed24h12g1?: string | null;
      pluvmed24h18g1?: string | null;
      pluvmed24h00g2?: string | null;
      pluvmed24h06g2?: string | null;
      pluvmed24h12g2?: string | null;
      pluvmed24h18g2?: string | null;
      pluvmed24h00g3?: string | null;
      pluvmed48h18g0_oss?: string | null;
      pluvmed48h00g1_oss?: string | null;
      pluvmed48h06g1_oss?: string | null;
      pluvmed48h12g1_oss?: string | null;
      pluvmed48h18g1_oss?: string | null;
      pluvmed48h00g2_oss?: string | null;
      pluvmed48h06g2_oss?: string | null;
      pluvmed48h12g2?: string | null;
      pluvmed48h18g2?: string | null;
      pluvmed48h00g3?: string | null;
      neveqmin?: string | null;
      neveqmax?: string | null;
      neve400_oggi?: string | null;
      neve400_domani?: string | null;
      neve400_totale?: string | null;
      neve700_oggi?: string | null;
      neve700_domani?: string | null;
      neve700_totale?: string | null;
      neve1000_oggi?: string | null;
      neve1000_domani?: string | null;
      neve1000_totale?: string | null;
      temporale_oggi?: string | null;
      temporale_domani?: string | null;
      neveqd01?: string | null;
      neveqd02?: string | null;
      neveqd11?: string | null;
      neveqd12?: string | null;
      neveqd13?: string | null;
      neveqd14?: string | null;
      id_w23: number;
      idrogeologico_oggi: string;
      idrogeologico_domani: string;
      temporali_oggi: string;
      temporali_domani: string;
      idraulico_oggi: string;
      idraulico_domani: string;
      neve_oggi: string;
      neve_domani: string;
      valanghe_oggi: string;
      valanghe_domani: string;
      idrogeologico_oggi_for?: string | null;
      idrogeologico_domani_for?: string | null;
      temporali_oggi_for?: string | null;
      temporali_domani_for?: string | null;
      idraulico_oggi_for?: string | null;
      idraulico_domani_for?: string | null;
      neve_oggi_for?: string | null;
      neve_domani_for?: string | null;
      valanghe_oggi_for?: string | null;
      valanghe_domani_for?: string | null;
    };
    W23Effettiterritorio: {
      id_w23_effettiterritorio: string;
      descrizione?: string | null;
    };
    W23Pericolo: {
      id_w23_pericolo: string;
      colore_html: string;
      sort_index: number;
    };
    W23Pluvossh6: {
      id_w23_pluvossh6: number;
      /** Format: date */
      data: string;
      /** Format: time */
      ora: string;
      area: string;
      valore?: string | null;
    };
    W23SerializerFull: {
      id_w23: number;
      w23data_set: string;
      /** Format: date */
      data_emissione: string;
      numero_bollettino: string;
      situazione_meteo?: string | null;
      status: string;
      /** Format: date-time */
      last_update: string;
      username: string;
      fraserisknat?: string | null;
      annotazione?: string | null;
      /** Format: date-time */
      last_update_annotazione: string;
      id_w23_parent?: number | null;
    };
    W23Zone: {
      id_w23_zone: number;
      zona_allerta: string;
      bacino: string;
      provincia: string;
      nome_zona?: string | null;
    };
    W24: {
      id_w24: number;
      numero_bollettino: string;
      /** Format: date */
      data_emissione: string;
      /** Format: date */
      next_blt_time: string;
      sintesi_meteo?: string | null;
      status: string;
      /** Format: date-time */
      last_update: string;
      username: string;
      tipo_anomalia_termica?: string | null;
      forzante_0: string;
      forzante_1: string;
      forzante_2: string;
      id_w24_parent?: number | null;
    };
    W24Data: {
      id_w24_data: number;
      /** Format: decimal */
      numeric_value: string;
      id_w24: number;
      id_allertamento: string;
      id_time_layouts: number;
      id_parametro: string;
    };
    W24SerializerFull: {
      id_w24: number;
      w24data_set: readonly (components["schemas"]["W24Data"])[];
      numero_bollettino: string;
      /** Format: date */
      data_emissione: string;
      /** Format: date */
      next_blt_time: string;
      sintesi_meteo?: string | null;
      status: string;
      /** Format: date-time */
      last_update: string;
      username: string;
      tipo_anomalia_termica?: string | null;
      forzante_0: string;
      forzante_1: string;
      forzante_2: string;
      id_w24_parent?: number | null;
    };
    W24Soglie: {
      id_allertamento: string;
      /** Format: decimal */
      soglia1: string;
      /** Format: decimal */
      soglia2: string;
      classe_intensita: number;
      /** Format: date-time */
      last_update: string;
      username: string;
      id_parametro: string;
      id_aggregazione: number;
    };
    W26: {
      id_w26: number;
      /** Format: date */
      data_emissione: string;
      numero_bollettino: string;
      status: string;
      /** Format: date-time */
      last_update: string;
      username: string;
      /** Format: date */
      data_validita: string;
    };
    W26Data: {
      id_w26_data: number;
      id_w26_zone: components["schemas"]["W26Zone"];
      hmin?: string | null;
      hmax?: string | null;
      hmed?: string | null;
      qmin?: string | null;
      qmax?: string | null;
      qmed?: string | null;
      nota?: string | null;
      idnota?: string | null;
      id_w26: number;
    };
    W26Zone: {
      id_w26_zone: number;
      codice?: string;
      localita: string;
      corsoacqua: string;
      numero: number;
    };
    W29: {
      id_w29: number;
      /** Format: date */
      data_emissione: string;
      ora_emissione: string;
      ora_simulazione: string;
      numero_bollettino: string;
      situazione_evoluzione?: string | null;
      status: string;
      /** Format: date-time */
      last_update: string;
      username: string;
      /** Format: date */
      data_validita: string;
      ora_osservazione?: string | null;
      data_osservazione?: string | null;
      data_simulazione?: string | null;
      note?: string | null;
    };
    W29Data: {
      id_w29_data: number;
      id_w29_zone: components["schemas"]["W29Zone"];
      livello_criticita_oss: string;
      probabilita_criticita_oss: string;
      livello_criticita_prev_oggi: string;
      probabilita_criticita_prev_oggi: string;
      livello_criticita_prev_domani: string;
      probabilita_criticita_prev_domani: string;
      id_w29: number;
    };
    W29Pericolo: {
      id_w29_pericolo: string;
      descrizione?: string | null;
    };
    W29Probabilita: {
      id_w29_probabilita: string;
      descrizione?: string | null;
    };
    W29Zone: {
      id_w29_zone: number;
      descrizione: string;
    };
    W30: {
      id_w30: number;
      /** Format: int64 */
      seq_num?: number | null;
      /** Format: date-time */
      data_emissione: string;
      /** Format: date-time */
      data_prossimo_aggiornamento: string;
      status: string;
      /** Format: date-time */
      last_update: string;
      username: string;
      id_w30_parent?: number | null;
      firstguess: string;
    };
    W30CurrentDataView: {
      id_w30_data: number;
      id_time_layouts_corrected: string;
      numeric_value?: number | null;
      id_w30: number;
      id_allertamento: string;
      id_time_layouts: number;
      id_parametro: string;
      id_aggregazione: number;
    };
    W30Data: {
      id_w30_data: number;
      numeric_value?: number | null;
      id_w30: number;
      id_allertamento: string;
      id_time_layouts: number;
      id_parametro: string;
      id_aggregazione: number;
    };
    W30SerializerFull: {
      id_w30: number;
      w30data_set: readonly (components["schemas"]["W30Data"])[];
      /** Format: int64 */
      seq_num?: number | null;
      /** Format: date-time */
      data_emissione: string;
      /** Format: date-time */
      data_prossimo_aggiornamento: string;
      status: string;
      /** Format: date-time */
      last_update: string;
      username: string;
      id_w30_parent?: number | null;
      firstguess: string;
    };
    W31: {
      id_w31: number;
      /** Format: date-time */
      start_valid_time: string;
      validity: number;
      /** Format: date-time */
      next_blt_time: string;
      status: string;
      /** Format: date-time */
      last_update: string;
      username: string;
      /** Format: int64 */
      seq_num?: number | null;
      /** Format: int64 */
      version?: number | null;
      algoritmo: string;
      id_w31_parent?: number | null;
      annotazione?: string | null;
    };
    W31DataMacroareeLivelli: {
      id_w31_data_macroaree_livelli: number;
      id_w31_macroaree: components["schemas"]["W31Macroaree"];
      id_w31: number;
      id_w31_livelli: number;
      id_time_layouts: number;
    };
    W31Livelli: {
      id_w31_livelli: number;
      colore: string;
    };
    W31Macroaree: {
      id_w31_macroaree: number;
      nome: string;
    };
    W31SerializerFull: {
      id_w31: number;
      w31datamicroareelivelli_set: string;
      w31datamacroareelivelli_set: string;
      /** Format: date-time */
      start_valid_time: string;
      validity: number;
      /** Format: date-time */
      next_blt_time: string;
      status: string;
      /** Format: date-time */
      last_update: string;
      username: string;
      /** Format: int64 */
      seq_num?: number | null;
      /** Format: int64 */
      version?: number | null;
      algoritmo: string;
      id_w31_parent?: number | null;
      annotazione?: string | null;
    };
  };
  responses: never;
  parameters: never;
  requestBodies: never;
  headers: never;
  pathItems: never;
}

export type external = Record<string, never>;

export interface operations {

  token_create: {
    /**
     * @description Takes a set of user credentials and returns an access and refresh JSON web
     * token pair to prove the authentication of those credentials.
     */
    requestBody: {
      content: {
        "application/json": components["schemas"]["MyTokenObtainPair"];
        "application/x-www-form-urlencoded": components["schemas"]["MyTokenObtainPair"];
        "multipart/form-data": components["schemas"]["MyTokenObtainPair"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["MyTokenObtainPair"];
        };
      };
    };
  };
  token_refresh_create: {
    /**
     * @description Takes a refresh type JSON web token and returns an access type JSON web
     * token if the refresh token is valid.
     */
    requestBody: {
      content: {
        "application/json": components["schemas"]["TokenRefresh"];
        "application/x-www-form-urlencoded": components["schemas"]["TokenRefresh"];
        "multipart/form-data": components["schemas"]["TokenRefresh"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["TokenRefresh"];
        };
      };
    };
  };
  token_verify_create: {
    /**
     * @description Takes a token and indicates if it is valid.  This view provides no
     * information about a token's fitness for a particular use.
     */
    requestBody: {
      content: {
        "application/json": components["schemas"]["TokenVerify"];
        "application/x-www-form-urlencoded": components["schemas"]["TokenVerify"];
        "multipart/form-data": components["schemas"]["TokenVerify"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["TokenVerify"];
        };
      };
    };
  };
  w05_bulletins_list: {
    /** @description API endpoint that allows W05 bulletins to be viewed or edited */
    parameters?: {
        /** @description A page number within the paginated result set. */
      query?: {
        page?: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["PaginatedW05List"];
        };
      };
    };
  };
  w05_bulletins_create: {
    /** @description API endpoint that allows W05 bulletins to be viewed or edited */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W05"];
        "application/x-www-form-urlencoded": components["schemas"]["W05"];
        "multipart/form-data": components["schemas"]["W05"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W05"];
        };
      };
    };
  };
  w05_bulletins_retrieve: {
    /** @description API endpoint that allows W05 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w05. */
      path: {
        id_w05: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W05"];
        };
      };
    };
  };
  w05_bulletins_update: {
    /** @description API endpoint that allows W05 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w05. */
      path: {
        id_w05: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W05"];
        "application/x-www-form-urlencoded": components["schemas"]["W05"];
        "multipart/form-data": components["schemas"]["W05"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W05"];
        };
      };
    };
  };
  w05_bulletins_destroy: {
    /** @description API endpoint that allows W05 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w05. */
      path: {
        id_w05: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w05_bulletins_partial_update: {
    /** @description API endpoint that allows W05 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w05. */
      path: {
        id_w05: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW05"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW05"];
        "multipart/form-data": components["schemas"]["PatchedW05"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W05"];
        };
      };
    };
  };
  w05_bulletins_classes_json_retrieve: {
    /** @description API endpoint that allows W05 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w05. */
      path: {
        id_w05: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W05"];
        };
      };
    };
  };
  w05_bulletins_data_json_retrieve: {
    /** @description API endpoint that allows W05 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w05. */
      path: {
        id_w05: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W05"];
        };
      };
    };
  };
  w05_bulletins_json_retrieve: {
    /** @description API endpoint that allows W05 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w05. */
      path: {
        id_w05: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W05"];
        };
      };
    };
  };
  w05_bulletins_reload_retrieve: {
    /** @description API endpoint that allows W05 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w05. */
      path: {
        id_w05: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W05"];
        };
      };
    };
  };
  w05_bulletins_reopen_retrieve: {
    /** @description API endpoint that allows W05 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w05. */
      path: {
        id_w05: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W05"];
        };
      };
    };
  };
  w05_bulletins_resend_retrieve: {
    /** @description API endpoint that allows W05 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w05. */
      path: {
        id_w05: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W05"];
        };
      };
    };
  };
  w05_bulletins_send_retrieve: {
    /** @description API endpoint that allows W05 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w05. */
      path: {
        id_w05: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W05"];
        };
      };
    };
  };
  w05_bulletins_xml_retrieve: {
    /** @description API endpoint that allows W05 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w05. */
      path: {
        id_w05: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/xml": components["schemas"]["W05"];
        };
      };
    };
  };
  w05_bulletins_bulk_update_create: {
    /** @description API endpoint that allows W05 bulletins to be viewed or edited */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W05"];
        "application/x-www-form-urlencoded": components["schemas"]["W05"];
        "multipart/form-data": components["schemas"]["W05"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W05"];
        };
      };
    };
  };
  w05_bulletins_new_retrieve: {
    /** @description API endpoint that allows W05 bulletins to be viewed or edited */
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W05"];
        };
      };
    };
  };
  w05_classes_list: {
    /** @description API endpoint that allows Classes to be viewed */
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["Classes"])[];
        };
      };
    };
  };
  w05_classes_create: {
    /** @description API endpoint that allows Classes to be viewed */
    requestBody: {
      content: {
        "application/json": components["schemas"]["Classes"];
        "application/x-www-form-urlencoded": components["schemas"]["Classes"];
        "multipart/form-data": components["schemas"]["Classes"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["Classes"];
        };
      };
    };
  };
  w05_classes_retrieve: {
    /** @description API endpoint that allows Classes to be viewed */
    parameters: {
        /** @description A unique value identifying this classes. */
      path: {
        id_classes: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["Classes"];
        };
      };
    };
  };
  w05_classes_update: {
    /** @description API endpoint that allows Classes to be viewed */
    parameters: {
        /** @description A unique value identifying this classes. */
      path: {
        id_classes: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["Classes"];
        "application/x-www-form-urlencoded": components["schemas"]["Classes"];
        "multipart/form-data": components["schemas"]["Classes"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["Classes"];
        };
      };
    };
  };
  w05_classes_destroy: {
    /** @description API endpoint that allows Classes to be viewed */
    parameters: {
        /** @description A unique value identifying this classes. */
      path: {
        id_classes: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w05_classes_partial_update: {
    /** @description API endpoint that allows Classes to be viewed */
    parameters: {
        /** @description A unique value identifying this classes. */
      path: {
        id_classes: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedClasses"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedClasses"];
        "multipart/form-data": components["schemas"]["PatchedClasses"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["Classes"];
        };
      };
    };
  };
  w05_data_list: {
    /** @description API endpoint that allows W05 bulletin Data to be viewed or edited */
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W05Data"])[];
        };
      };
    };
  };
  w05_data_create: {
    /** @description API endpoint that allows W05 bulletin Data to be viewed or edited */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W05Data"];
        "application/x-www-form-urlencoded": components["schemas"]["W05Data"];
        "multipart/form-data": components["schemas"]["W05Data"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W05Data"];
        };
      };
    };
  };
  w05_data_retrieve: {
    /** @description API endpoint that allows W05 bulletin Data to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w05 data. */
      path: {
        id_w05_data: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W05Data"];
        };
      };
    };
  };
  w05_data_update: {
    /** @description API endpoint that allows W05 bulletin Data to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w05 data. */
      path: {
        id_w05_data: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W05Data"];
        "application/x-www-form-urlencoded": components["schemas"]["W05Data"];
        "multipart/form-data": components["schemas"]["W05Data"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W05Data"];
        };
      };
    };
  };
  w05_data_destroy: {
    /** @description API endpoint that allows W05 bulletin Data to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w05 data. */
      path: {
        id_w05_data: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w05_data_partial_update: {
    /** @description API endpoint that allows W05 bulletin Data to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w05 data. */
      path: {
        id_w05_data: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW05Data"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW05Data"];
        "multipart/form-data": components["schemas"]["PatchedW05Data"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W05Data"];
        };
      };
    };
  };
  w05_meteo_classes_list: {
    /** @description API endpoint that allows W05 bulletin Classes to be viewed or edited */
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W05Classes"])[];
        };
      };
    };
  };
  w05_meteo_classes_create: {
    /** @description API endpoint that allows W05 bulletin Classes to be viewed or edited */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W05Classes"];
        "application/x-www-form-urlencoded": components["schemas"]["W05Classes"];
        "multipart/form-data": components["schemas"]["W05Classes"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W05Classes"];
        };
      };
    };
  };
  w05_meteo_classes_retrieve: {
    /** @description API endpoint that allows W05 bulletin Classes to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w05 classes. */
      path: {
        id_w05_classes: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W05Classes"];
        };
      };
    };
  };
  w05_meteo_classes_update: {
    /** @description API endpoint that allows W05 bulletin Classes to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w05 classes. */
      path: {
        id_w05_classes: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W05Classes"];
        "application/x-www-form-urlencoded": components["schemas"]["W05Classes"];
        "multipart/form-data": components["schemas"]["W05Classes"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W05Classes"];
        };
      };
    };
  };
  w05_meteo_classes_destroy: {
    /** @description API endpoint that allows W05 bulletin Classes to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w05 classes. */
      path: {
        id_w05_classes: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w05_meteo_classes_partial_update: {
    /** @description API endpoint that allows W05 bulletin Classes to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w05 classes. */
      path: {
        id_w05_classes: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW05Classes"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW05Classes"];
        "multipart/form-data": components["schemas"]["PatchedW05Classes"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W05Classes"];
        };
      };
    };
  };
  w05_sky_conditions_list: {
    /** @description API endpoint that allows W16 bulletins to be viewed or edited */
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["SkyCondition"])[];
        };
      };
    };
  };
  w05_sky_conditions_create: {
    /** @description API endpoint that allows W16 bulletins to be viewed or edited */
    requestBody: {
      content: {
        "application/json": components["schemas"]["SkyCondition"];
        "application/x-www-form-urlencoded": components["schemas"]["SkyCondition"];
        "multipart/form-data": components["schemas"]["SkyCondition"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["SkyCondition"];
        };
      };
    };
  };
  w05_sky_conditions_retrieve: {
    /** @description API endpoint that allows W16 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique value identifying this sky condition. */
      path: {
        id_sky_condition: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["SkyCondition"];
        };
      };
    };
  };
  w05_sky_conditions_update: {
    /** @description API endpoint that allows W16 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique value identifying this sky condition. */
      path: {
        id_sky_condition: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["SkyCondition"];
        "application/x-www-form-urlencoded": components["schemas"]["SkyCondition"];
        "multipart/form-data": components["schemas"]["SkyCondition"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["SkyCondition"];
        };
      };
    };
  };
  w05_sky_conditions_destroy: {
    /** @description API endpoint that allows W16 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique value identifying this sky condition. */
      path: {
        id_sky_condition: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w05_sky_conditions_partial_update: {
    /** @description API endpoint that allows W16 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique value identifying this sky condition. */
      path: {
        id_sky_condition: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedSkyCondition"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedSkyCondition"];
        "multipart/form-data": components["schemas"]["PatchedSkyCondition"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["SkyCondition"];
        };
      };
    };
  };
  w05_venue_names_list: {
    /** @description API endpoint that shows city names */
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["Venue"])[];
        };
      };
    };
  };
  w05_venue_names_create: {
    /** @description API endpoint that shows city names */
    requestBody: {
      content: {
        "application/json": components["schemas"]["Venue"];
        "application/x-www-form-urlencoded": components["schemas"]["Venue"];
        "multipart/form-data": components["schemas"]["Venue"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["Venue"];
        };
      };
    };
  };
  w05_venue_names_retrieve: {
    /** @description API endpoint that shows city names */
    parameters: {
        /** @description A unique value identifying this venue. */
      path: {
        id_venue: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["Venue"];
        };
      };
    };
  };
  w05_venue_names_update: {
    /** @description API endpoint that shows city names */
    parameters: {
        /** @description A unique value identifying this venue. */
      path: {
        id_venue: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["Venue"];
        "application/x-www-form-urlencoded": components["schemas"]["Venue"];
        "multipart/form-data": components["schemas"]["Venue"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["Venue"];
        };
      };
    };
  };
  w05_venue_names_destroy: {
    /** @description API endpoint that shows city names */
    parameters: {
        /** @description A unique value identifying this venue. */
      path: {
        id_venue: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w05_venue_names_partial_update: {
    /** @description API endpoint that shows city names */
    parameters: {
        /** @description A unique value identifying this venue. */
      path: {
        id_venue: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedVenue"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedVenue"];
        "multipart/form-data": components["schemas"]["PatchedVenue"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["Venue"];
        };
      };
    };
  };
  w16_bulletins_list: {
    /** @description API endpoint that allows W16 bulletins to be viewed or edited */
    parameters?: {
        /** @description A page number within the paginated result set. */
      query?: {
        page?: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["PaginatedW16List"];
        };
      };
    };
  };
  w16_bulletins_create: {
    /** @description API endpoint that allows W16 bulletins to be viewed or edited */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W16"];
        "application/x-www-form-urlencoded": components["schemas"]["W16"];
        "multipart/form-data": components["schemas"]["W16"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W16"];
        };
      };
    };
  };
  w16_bulletins_retrieve: {
    /** @description API endpoint that allows W16 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w16. */
      path: {
        id_w16: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W16"];
        };
      };
    };
  };
  w16_bulletins_update: {
    /** @description API endpoint that allows W16 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w16. */
      path: {
        id_w16: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W16"];
        "application/x-www-form-urlencoded": components["schemas"]["W16"];
        "multipart/form-data": components["schemas"]["W16"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W16"];
        };
      };
    };
  };
  w16_bulletins_destroy: {
    /** @description API endpoint that allows W16 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w16. */
      path: {
        id_w16: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w16_bulletins_partial_update: {
    /** @description API endpoint that allows W16 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w16. */
      path: {
        id_w16: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW16"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW16"];
        "multipart/form-data": components["schemas"]["PatchedW16"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W16"];
        };
      };
    };
  };
  w16_bulletins_copy_retrieve: {
    /** @description API endpoint that allows W16 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w16. */
      path: {
        id_w16: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W16"];
        };
      };
    };
  };
  w16_bulletins_reopen_retrieve: {
    /** @description API endpoint that allows W16 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w16. */
      path: {
        id_w16: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W16"];
        };
      };
    };
  };
  w16_bulletins_send_retrieve: {
    /** @description API endpoint that allows W16 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w16. */
      path: {
        id_w16: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W16"];
        };
      };
    };
  };
  w16_bulletins_new_retrieve: {
    /** @description API endpoint that allows W16 bulletins to be viewed or edited */
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W16"];
        };
      };
    };
  };
  w16_conf_list: {
    /** @description API endpoint that allows W16Conf records to be viewed */
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W16Conf"])[];
        };
      };
    };
  };
  w16_conf_create: {
    /** @description API endpoint that allows W16Conf records to be viewed */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W16Conf"];
        "application/x-www-form-urlencoded": components["schemas"]["W16Conf"];
        "multipart/form-data": components["schemas"]["W16Conf"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W16Conf"];
        };
      };
    };
  };
  w16_conf_retrieve: {
    /** @description API endpoint that allows W16Conf records to be viewed */
    parameters: {
        /** @description A unique value identifying this w16 conf. */
      path: {
        id_w16_conf: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W16Conf"];
        };
      };
    };
  };
  w16_conf_update: {
    /** @description API endpoint that allows W16Conf records to be viewed */
    parameters: {
        /** @description A unique value identifying this w16 conf. */
      path: {
        id_w16_conf: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W16Conf"];
        "application/x-www-form-urlencoded": components["schemas"]["W16Conf"];
        "multipart/form-data": components["schemas"]["W16Conf"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W16Conf"];
        };
      };
    };
  };
  w16_conf_destroy: {
    /** @description API endpoint that allows W16Conf records to be viewed */
    parameters: {
        /** @description A unique value identifying this w16 conf. */
      path: {
        id_w16_conf: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w16_conf_partial_update: {
    /** @description API endpoint that allows W16Conf records to be viewed */
    parameters: {
        /** @description A unique value identifying this w16 conf. */
      path: {
        id_w16_conf: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW16Conf"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW16Conf"];
        "multipart/form-data": components["schemas"]["PatchedW16Conf"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W16Conf"];
        };
      };
    };
  };
  w16_data_list: {
    /** @description API endpoint that allows W16 bulletin Data to be viewed or updated */
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W16Data"])[];
        };
      };
    };
  };
  w16_data_create: {
    /** @description API endpoint that allows W16 bulletin Data to be viewed or updated */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W16Data"];
        "application/x-www-form-urlencoded": components["schemas"]["W16Data"];
        "multipart/form-data": components["schemas"]["W16Data"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W16Data"];
        };
      };
    };
  };
  w16_data_retrieve: {
    /** @description API endpoint that allows W16 bulletin Data to be viewed or updated */
    parameters: {
        /** @description A unique integer value identifying this w16 data. */
      path: {
        id_w16_data: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W16Data"];
        };
      };
    };
  };
  w16_data_update: {
    /** @description API endpoint that allows W16 bulletin Data to be viewed or updated */
    parameters: {
        /** @description A unique integer value identifying this w16 data. */
      path: {
        id_w16_data: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W16Data"];
        "application/x-www-form-urlencoded": components["schemas"]["W16Data"];
        "multipart/form-data": components["schemas"]["W16Data"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W16Data"];
        };
      };
    };
  };
  w16_data_destroy: {
    /** @description API endpoint that allows W16 bulletin Data to be viewed or updated */
    parameters: {
        /** @description A unique integer value identifying this w16 data. */
      path: {
        id_w16_data: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w16_data_partial_update: {
    /** @description API endpoint that allows W16 bulletin Data to be viewed or updated */
    parameters: {
        /** @description A unique integer value identifying this w16 data. */
      path: {
        id_w16_data: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW16Data"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW16Data"];
        "multipart/form-data": components["schemas"]["PatchedW16Data"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W16Data"];
        };
      };
    };
  };
  w16_data_bulk_update_create: {
    /** @description API endpoint that allows W16 bulletin Data to be viewed or updated */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W16Data"];
        "application/x-www-form-urlencoded": components["schemas"]["W16Data"];
        "multipart/form-data": components["schemas"]["W16Data"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W16Data"];
        };
      };
    };
  };
  w16_levels_list: {
    /** @description API endpoint that allows OzonoLivelli records to be viewed */
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["OzonoLivelli"])[];
        };
      };
    };
  };
  w16_levels_create: {
    /** @description API endpoint that allows OzonoLivelli records to be viewed */
    requestBody: {
      content: {
        "application/json": components["schemas"]["OzonoLivelli"];
        "application/x-www-form-urlencoded": components["schemas"]["OzonoLivelli"];
        "multipart/form-data": components["schemas"]["OzonoLivelli"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["OzonoLivelli"];
        };
      };
    };
  };
  w16_levels_retrieve: {
    /** @description API endpoint that allows OzonoLivelli records to be viewed */
    parameters: {
        /** @description A unique value identifying this ozono livelli. */
      path: {
        id_ozono_livelli: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["OzonoLivelli"];
        };
      };
    };
  };
  w16_levels_update: {
    /** @description API endpoint that allows OzonoLivelli records to be viewed */
    parameters: {
        /** @description A unique value identifying this ozono livelli. */
      path: {
        id_ozono_livelli: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["OzonoLivelli"];
        "application/x-www-form-urlencoded": components["schemas"]["OzonoLivelli"];
        "multipart/form-data": components["schemas"]["OzonoLivelli"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["OzonoLivelli"];
        };
      };
    };
  };
  w16_levels_destroy: {
    /** @description API endpoint that allows OzonoLivelli records to be viewed */
    parameters: {
        /** @description A unique value identifying this ozono livelli. */
      path: {
        id_ozono_livelli: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w16_levels_partial_update: {
    /** @description API endpoint that allows OzonoLivelli records to be viewed */
    parameters: {
        /** @description A unique value identifying this ozono livelli. */
      path: {
        id_ozono_livelli: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedOzonoLivelli"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedOzonoLivelli"];
        "multipart/form-data": components["schemas"]["PatchedOzonoLivelli"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["OzonoLivelli"];
        };
      };
    };
  };
  w22_bulletins_list: {
    /** @description API endpoint that allows W22 bulletins to be viewed or edited */
    parameters?: {
        /** @description A page number within the paginated result set. */
      query?: {
        page?: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["PaginatedW22List"];
        };
      };
    };
  };
  w22_bulletins_create: {
    /** @description API endpoint that allows W22 bulletins to be viewed or edited */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W22"];
        "application/x-www-form-urlencoded": components["schemas"]["W22"];
        "multipart/form-data": components["schemas"]["W22"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W22"];
        };
      };
    };
  };
  w22_bulletins_retrieve: {
    /** @description API endpoint that allows W22 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w22. */
      path: {
        id_w22: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W22"];
        };
      };
    };
  };
  w22_bulletins_update: {
    /** @description API endpoint that allows W22 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w22. */
      path: {
        id_w22: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W22"];
        "application/x-www-form-urlencoded": components["schemas"]["W22"];
        "multipart/form-data": components["schemas"]["W22"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W22"];
        };
      };
    };
  };
  w22_bulletins_destroy: {
    /** @description API endpoint that allows W22 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w22. */
      path: {
        id_w22: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w22_bulletins_partial_update: {
    /** @description API endpoint that allows W22 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w22. */
      path: {
        id_w22: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW22"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW22"];
        "multipart/form-data": components["schemas"]["PatchedW22"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W22"];
        };
      };
    };
  };
  w22_bulletins_send_retrieve: {
    /** @description API endpoint that allows W22 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w22. */
      path: {
        id_w22: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W22"];
        };
      };
    };
  };
  w22_bulletins_bulk_update_create: {
    /** @description API endpoint that allows W22 bulletins to be viewed or edited */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W22"];
        "application/x-www-form-urlencoded": components["schemas"]["W22"];
        "multipart/form-data": components["schemas"]["W22"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W22"];
        };
      };
    };
  };
  w22_bulletins_new_retrieve: {
    /** @description API endpoint that allows W22 bulletins to be viewed or edited */
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W22"];
        };
      };
    };
  };
  w22_criticita_list: {
    /** @description API endpoint that allows W22 bulletin Criticità to be viewed */
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W22Criticita"])[];
        };
      };
    };
  };
  w22_criticita_create: {
    /** @description API endpoint that allows W22 bulletin Criticità to be viewed */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W22Criticita"];
        "application/x-www-form-urlencoded": components["schemas"]["W22Criticita"];
        "multipart/form-data": components["schemas"]["W22Criticita"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W22Criticita"];
        };
      };
    };
  };
  w22_criticita_retrieve: {
    /** @description API endpoint that allows W22 bulletin Criticità to be viewed */
    parameters: {
        /** @description A unique value identifying this w22 criticita. */
      path: {
        id_w22_criticita: string;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W22Criticita"];
        };
      };
    };
  };
  w22_criticita_update: {
    /** @description API endpoint that allows W22 bulletin Criticità to be viewed */
    parameters: {
        /** @description A unique value identifying this w22 criticita. */
      path: {
        id_w22_criticita: string;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W22Criticita"];
        "application/x-www-form-urlencoded": components["schemas"]["W22Criticita"];
        "multipart/form-data": components["schemas"]["W22Criticita"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W22Criticita"];
        };
      };
    };
  };
  w22_criticita_destroy: {
    /** @description API endpoint that allows W22 bulletin Criticità to be viewed */
    parameters: {
        /** @description A unique value identifying this w22 criticita. */
      path: {
        id_w22_criticita: string;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w22_criticita_partial_update: {
    /** @description API endpoint that allows W22 bulletin Criticità to be viewed */
    parameters: {
        /** @description A unique value identifying this w22 criticita. */
      path: {
        id_w22_criticita: string;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW22Criticita"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW22Criticita"];
        "multipart/form-data": components["schemas"]["PatchedW22Criticita"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W22Criticita"];
        };
      };
    };
  };
  w22_data_list: {
    /** @description API endpoint that allows W22 bulletin Data to be viewed or edited */
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W22Data"])[];
        };
      };
    };
  };
  w22_data_create: {
    /** @description API endpoint that allows W22 bulletin Data to be viewed or edited */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W22Data"];
        "application/x-www-form-urlencoded": components["schemas"]["W22Data"];
        "multipart/form-data": components["schemas"]["W22Data"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W22Data"];
        };
      };
    };
  };
  w22_data_retrieve: {
    /** @description API endpoint that allows W22 bulletin Data to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w22 data. */
      path: {
        id_w22_data: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W22Data"];
        };
      };
    };
  };
  w22_data_update: {
    /** @description API endpoint that allows W22 bulletin Data to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w22 data. */
      path: {
        id_w22_data: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W22Data"];
        "application/x-www-form-urlencoded": components["schemas"]["W22Data"];
        "multipart/form-data": components["schemas"]["W22Data"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W22Data"];
        };
      };
    };
  };
  w22_data_destroy: {
    /** @description API endpoint that allows W22 bulletin Data to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w22 data. */
      path: {
        id_w22_data: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w22_data_partial_update: {
    /** @description API endpoint that allows W22 bulletin Data to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w22 data. */
      path: {
        id_w22_data: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW22Data"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW22Data"];
        "multipart/form-data": components["schemas"]["PatchedW22Data"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W22Data"];
        };
      };
    };
  };
  w22_tendenza_list: {
    /** @description API endpoint that allows W22 bulletin Tendenza to be viewed */
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W22Tendenza"])[];
        };
      };
    };
  };
  w22_tendenza_create: {
    /** @description API endpoint that allows W22 bulletin Tendenza to be viewed */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W22Tendenza"];
        "application/x-www-form-urlencoded": components["schemas"]["W22Tendenza"];
        "multipart/form-data": components["schemas"]["W22Tendenza"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W22Tendenza"];
        };
      };
    };
  };
  w22_tendenza_retrieve: {
    /** @description API endpoint that allows W22 bulletin Tendenza to be viewed */
    parameters: {
        /** @description A unique value identifying this w22 tendenza. */
      path: {
        id_w22_tendenza: string;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W22Tendenza"];
        };
      };
    };
  };
  w22_tendenza_update: {
    /** @description API endpoint that allows W22 bulletin Tendenza to be viewed */
    parameters: {
        /** @description A unique value identifying this w22 tendenza. */
      path: {
        id_w22_tendenza: string;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W22Tendenza"];
        "application/x-www-form-urlencoded": components["schemas"]["W22Tendenza"];
        "multipart/form-data": components["schemas"]["W22Tendenza"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W22Tendenza"];
        };
      };
    };
  };
  w22_tendenza_destroy: {
    /** @description API endpoint that allows W22 bulletin Tendenza to be viewed */
    parameters: {
        /** @description A unique value identifying this w22 tendenza. */
      path: {
        id_w22_tendenza: string;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w22_tendenza_partial_update: {
    /** @description API endpoint that allows W22 bulletin Tendenza to be viewed */
    parameters: {
        /** @description A unique value identifying this w22 tendenza. */
      path: {
        id_w22_tendenza: string;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW22Tendenza"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW22Tendenza"];
        "multipart/form-data": components["schemas"]["PatchedW22Tendenza"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W22Tendenza"];
        };
      };
    };
  };
  w22_zone_list: {
    /** @description API endpoint that allows W22 bulletin Zone to be viewed or edited */
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W22Zone"])[];
        };
      };
    };
  };
  w22_zone_create: {
    /** @description API endpoint that allows W22 bulletin Zone to be viewed or edited */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W22Zone"];
        "application/x-www-form-urlencoded": components["schemas"]["W22Zone"];
        "multipart/form-data": components["schemas"]["W22Zone"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W22Zone"];
        };
      };
    };
  };
  w22_zone_retrieve: {
    /** @description API endpoint that allows W22 bulletin Zone to be viewed or edited */
    parameters: {
        /** @description A unique value identifying this w22 zone. */
      path: {
        id_w22_zone: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W22Zone"];
        };
      };
    };
  };
  w22_zone_update: {
    /** @description API endpoint that allows W22 bulletin Zone to be viewed or edited */
    parameters: {
        /** @description A unique value identifying this w22 zone. */
      path: {
        id_w22_zone: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W22Zone"];
        "application/x-www-form-urlencoded": components["schemas"]["W22Zone"];
        "multipart/form-data": components["schemas"]["W22Zone"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W22Zone"];
        };
      };
    };
  };
  w22_zone_destroy: {
    /** @description API endpoint that allows W22 bulletin Zone to be viewed or edited */
    parameters: {
        /** @description A unique value identifying this w22 zone. */
      path: {
        id_w22_zone: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w22_zone_partial_update: {
    /** @description API endpoint that allows W22 bulletin Zone to be viewed or edited */
    parameters: {
        /** @description A unique value identifying this w22 zone. */
      path: {
        id_w22_zone: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW22Zone"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW22Zone"];
        "multipart/form-data": components["schemas"]["PatchedW22Zone"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W22Zone"];
        };
      };
    };
  };
  w22verifica_bulletins_list: {
    /** @description API endpoint that allows W22 bulletins to be viewed or edited */
    parameters?: {
        /** @description A page number within the paginated result set. */
      query?: {
        page?: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["PaginatedW22VerificaList"];
        };
      };
    };
  };
  w22verifica_bulletins_create: {
    /** @description API endpoint that allows W22 bulletins to be viewed or edited */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W22Verifica"];
        "application/x-www-form-urlencoded": components["schemas"]["W22Verifica"];
        "multipart/form-data": components["schemas"]["W22Verifica"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W22Verifica"];
        };
      };
    };
  };
  w22verifica_bulletins_retrieve: {
    /** @description API endpoint that allows W22 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w22 verifica. */
      path: {
        id_w22verifica: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W22Verifica"];
        };
      };
    };
  };
  w22verifica_bulletins_update: {
    /** @description API endpoint that allows W22 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w22 verifica. */
      path: {
        id_w22verifica: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W22Verifica"];
        "application/x-www-form-urlencoded": components["schemas"]["W22Verifica"];
        "multipart/form-data": components["schemas"]["W22Verifica"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W22Verifica"];
        };
      };
    };
  };
  w22verifica_bulletins_destroy: {
    /** @description API endpoint that allows W22 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w22 verifica. */
      path: {
        id_w22verifica: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w22verifica_bulletins_partial_update: {
    /** @description API endpoint that allows W22 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w22 verifica. */
      path: {
        id_w22verifica: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW22Verifica"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW22Verifica"];
        "multipart/form-data": components["schemas"]["PatchedW22Verifica"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W22Verifica"];
        };
      };
    };
  };
  w22verifica_bulletins_send_retrieve: {
    /** @description API endpoint that allows W22 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w22 verifica. */
      path: {
        id_w22verifica: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W22Verifica"];
        };
      };
    };
  };
  w22verifica_bulletins_bulk_update_create: {
    /** @description API endpoint that allows W22 bulletins to be viewed or edited */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W22Verifica"];
        "application/x-www-form-urlencoded": components["schemas"]["W22Verifica"];
        "multipart/form-data": components["schemas"]["W22Verifica"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W22Verifica"];
        };
      };
    };
  };
  w22verifica_bulletins_new_retrieve: {
    /** @description API endpoint that allows W22 bulletins to be viewed or edited */
    parameters: {
      path: {
        num_bollettino: string;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W22Verifica"];
        };
      };
    };
  };
  w22verifica_data_list: {
    /** @description API endpoint that allows W22 bulletin Data to be viewed or edited */
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W22VerificaData"])[];
        };
      };
    };
  };
  w22verifica_data_create: {
    /** @description API endpoint that allows W22 bulletin Data to be viewed or edited */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W22VerificaData"];
        "application/x-www-form-urlencoded": components["schemas"]["W22VerificaData"];
        "multipart/form-data": components["schemas"]["W22VerificaData"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W22VerificaData"];
        };
      };
    };
  };
  w22verifica_data_retrieve: {
    /** @description API endpoint that allows W22 bulletin Data to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w22 verifica data. */
      path: {
        id_w22verifica_data: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W22VerificaData"];
        };
      };
    };
  };
  w22verifica_data_update: {
    /** @description API endpoint that allows W22 bulletin Data to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w22 verifica data. */
      path: {
        id_w22verifica_data: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W22VerificaData"];
        "application/x-www-form-urlencoded": components["schemas"]["W22VerificaData"];
        "multipart/form-data": components["schemas"]["W22VerificaData"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W22VerificaData"];
        };
      };
    };
  };
  w22verifica_data_destroy: {
    /** @description API endpoint that allows W22 bulletin Data to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w22 verifica data. */
      path: {
        id_w22verifica_data: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w22verifica_data_partial_update: {
    /** @description API endpoint that allows W22 bulletin Data to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w22 verifica data. */
      path: {
        id_w22verifica_data: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW22VerificaData"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW22VerificaData"];
        "multipart/form-data": components["schemas"]["PatchedW22VerificaData"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W22VerificaData"];
        };
      };
    };
  };
  w22verifica_giudizio_list: {
    /** @description API endpoint that allows W22 bulletin Tendenza to be viewed */
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W22Giudizio"])[];
        };
      };
    };
  };
  w22verifica_giudizio_create: {
    /** @description API endpoint that allows W22 bulletin Tendenza to be viewed */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W22Giudizio"];
        "application/x-www-form-urlencoded": components["schemas"]["W22Giudizio"];
        "multipart/form-data": components["schemas"]["W22Giudizio"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W22Giudizio"];
        };
      };
    };
  };
  w22verifica_giudizio_retrieve: {
    /** @description API endpoint that allows W22 bulletin Tendenza to be viewed */
    parameters: {
        /** @description A unique value identifying this w22 giudizio. */
      path: {
        id_w22giudizio: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W22Giudizio"];
        };
      };
    };
  };
  w22verifica_giudizio_update: {
    /** @description API endpoint that allows W22 bulletin Tendenza to be viewed */
    parameters: {
        /** @description A unique value identifying this w22 giudizio. */
      path: {
        id_w22giudizio: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W22Giudizio"];
        "application/x-www-form-urlencoded": components["schemas"]["W22Giudizio"];
        "multipart/form-data": components["schemas"]["W22Giudizio"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W22Giudizio"];
        };
      };
    };
  };
  w22verifica_giudizio_destroy: {
    /** @description API endpoint that allows W22 bulletin Tendenza to be viewed */
    parameters: {
        /** @description A unique value identifying this w22 giudizio. */
      path: {
        id_w22giudizio: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w22verifica_giudizio_partial_update: {
    /** @description API endpoint that allows W22 bulletin Tendenza to be viewed */
    parameters: {
        /** @description A unique value identifying this w22 giudizio. */
      path: {
        id_w22giudizio: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW22Giudizio"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW22Giudizio"];
        "multipart/form-data": components["schemas"]["PatchedW22Giudizio"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W22Giudizio"];
        };
      };
    };
  };
  w22verifica_severita_list: {
    /** @description API endpoint that allows W22 bulletin Criticità to be viewed */
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W22Severita"])[];
        };
      };
    };
  };
  w22verifica_severita_create: {
    /** @description API endpoint that allows W22 bulletin Criticità to be viewed */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W22Severita"];
        "application/x-www-form-urlencoded": components["schemas"]["W22Severita"];
        "multipart/form-data": components["schemas"]["W22Severita"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W22Severita"];
        };
      };
    };
  };
  w22verifica_severita_retrieve: {
    /** @description API endpoint that allows W22 bulletin Criticità to be viewed */
    parameters: {
        /** @description A unique value identifying this w22 severita. */
      path: {
        id_w22severita: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W22Severita"];
        };
      };
    };
  };
  w22verifica_severita_update: {
    /** @description API endpoint that allows W22 bulletin Criticità to be viewed */
    parameters: {
        /** @description A unique value identifying this w22 severita. */
      path: {
        id_w22severita: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W22Severita"];
        "application/x-www-form-urlencoded": components["schemas"]["W22Severita"];
        "multipart/form-data": components["schemas"]["W22Severita"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W22Severita"];
        };
      };
    };
  };
  w22verifica_severita_destroy: {
    /** @description API endpoint that allows W22 bulletin Criticità to be viewed */
    parameters: {
        /** @description A unique value identifying this w22 severita. */
      path: {
        id_w22severita: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w22verifica_severita_partial_update: {
    /** @description API endpoint that allows W22 bulletin Criticità to be viewed */
    parameters: {
        /** @description A unique value identifying this w22 severita. */
      path: {
        id_w22severita: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW22Severita"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW22Severita"];
        "multipart/form-data": components["schemas"]["PatchedW22Severita"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W22Severita"];
        };
      };
    };
  };
  w22verifica_zone_list: {
    /** @description API endpoint that allows W22 bulletin Zone to be viewed or edited */
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W22Zone"])[];
        };
      };
    };
  };
  w22verifica_zone_create: {
    /** @description API endpoint that allows W22 bulletin Zone to be viewed or edited */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W22Zone"];
        "application/x-www-form-urlencoded": components["schemas"]["W22Zone"];
        "multipart/form-data": components["schemas"]["W22Zone"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W22Zone"];
        };
      };
    };
  };
  w22verifica_zone_retrieve: {
    /** @description API endpoint that allows W22 bulletin Zone to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w22 zone. */
      path: {
        id_w22_zone: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W22Zone"];
        };
      };
    };
  };
  w22verifica_zone_update: {
    /** @description API endpoint that allows W22 bulletin Zone to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w22 zone. */
      path: {
        id_w22_zone: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W22Zone"];
        "application/x-www-form-urlencoded": components["schemas"]["W22Zone"];
        "multipart/form-data": components["schemas"]["W22Zone"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W22Zone"];
        };
      };
    };
  };
  w22verifica_zone_destroy: {
    /** @description API endpoint that allows W22 bulletin Zone to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w22 zone. */
      path: {
        id_w22_zone: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w22verifica_zone_partial_update: {
    /** @description API endpoint that allows W22 bulletin Zone to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w22 zone. */
      path: {
        id_w22_zone: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW22Zone"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW22Zone"];
        "multipart/form-data": components["schemas"]["PatchedW22Zone"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W22Zone"];
        };
      };
    };
  };
  w23_bulletins_list: {
    /** @description API endpoint that allows W23 bulletins to be viewed or edited */
    parameters?: {
        /** @description A page number within the paginated result set. */
      query?: {
        page?: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["PaginatedW23List"];
        };
      };
    };
  };
  w23_bulletins_create: {
    /** @description API endpoint that allows W23 bulletins to be viewed or edited */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W23"];
        "application/x-www-form-urlencoded": components["schemas"]["W23"];
        "multipart/form-data": components["schemas"]["W23"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W23"];
        };
      };
    };
  };
  w23_bulletins_retrieve: {
    /** @description API endpoint that allows W23 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w23. */
      path: {
        id_w23: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W23"];
        };
      };
    };
  };
  w23_bulletins_update: {
    /** @description API endpoint that allows W23 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w23. */
      path: {
        id_w23: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W23"];
        "application/x-www-form-urlencoded": components["schemas"]["W23"];
        "multipart/form-data": components["schemas"]["W23"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W23"];
        };
      };
    };
  };
  w23_bulletins_destroy: {
    /** @description API endpoint that allows W23 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w23. */
      path: {
        id_w23: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w23_bulletins_partial_update: {
    /** @description API endpoint that allows W23 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w23. */
      path: {
        id_w23: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW23"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW23"];
        "multipart/form-data": components["schemas"]["PatchedW23"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W23"];
        };
      };
    };
  };
  w23_bulletins_reopen_retrieve: {
    /** @description API endpoint that allows W23 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w23. */
      path: {
        id_w23: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W23"];
        };
      };
    };
  };
  w23_bulletins_send_retrieve: {
    /** @description API endpoint that allows W23 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w23. */
      path: {
        id_w23: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W23"];
        };
      };
    };
  };
  w23_bulletins_bulk_update_create: {
    /** @description API endpoint that allows W23 bulletins to be viewed or edited */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W23"];
        "application/x-www-form-urlencoded": components["schemas"]["W23"];
        "multipart/form-data": components["schemas"]["W23"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W23"];
        };
      };
    };
  };
  w23_bulletins_new_retrieve: {
    /** @description API endpoint that allows W23 bulletins to be viewed or edited */
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W23"];
        };
      };
    };
  };
  w23_current_retrieve: {
    /** @description View the latest W23 bulletin sent for a certain day */
    parameters: {
      path: {
        data_emissione: string;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W23SerializerFull"];
        };
      };
    };
  };
  w23_data_list: {
    /** @description API endpoint that allows W23 bulletin Data to be viewed or edited */
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W23Data"])[];
        };
      };
    };
  };
  w23_data_create: {
    /** @description API endpoint that allows W23 bulletin Data to be viewed or edited */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W23Data"];
        "application/x-www-form-urlencoded": components["schemas"]["W23Data"];
        "multipart/form-data": components["schemas"]["W23Data"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W23Data"];
        };
      };
    };
  };
  w23_data_retrieve: {
    /** @description API endpoint that allows W23 bulletin Data to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w23 data. */
      path: {
        id_w23_data: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W23Data"];
        };
      };
    };
  };
  w23_data_update: {
    /** @description API endpoint that allows W23 bulletin Data to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w23 data. */
      path: {
        id_w23_data: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W23Data"];
        "application/x-www-form-urlencoded": components["schemas"]["W23Data"];
        "multipart/form-data": components["schemas"]["W23Data"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W23Data"];
        };
      };
    };
  };
  w23_data_destroy: {
    /** @description API endpoint that allows W23 bulletin Data to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w23 data. */
      path: {
        id_w23_data: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w23_data_partial_update: {
    /** @description API endpoint that allows W23 bulletin Data to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w23 data. */
      path: {
        id_w23_data: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW23Data"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW23Data"];
        "multipart/form-data": components["schemas"]["PatchedW23Data"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W23Data"];
        };
      };
    };
  };
  w23_effetti_list: {
    /** @description API endpoint that allows W23 bulletin Effetti sul territorio to be viewed */
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W23Effettiterritorio"])[];
        };
      };
    };
  };
  w23_effetti_create: {
    /** @description API endpoint that allows W23 bulletin Effetti sul territorio to be viewed */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W23Effettiterritorio"];
        "application/x-www-form-urlencoded": components["schemas"]["W23Effettiterritorio"];
        "multipart/form-data": components["schemas"]["W23Effettiterritorio"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W23Effettiterritorio"];
        };
      };
    };
  };
  w23_effetti_retrieve: {
    /** @description API endpoint that allows W23 bulletin Effetti sul territorio to be viewed */
    parameters: {
        /** @description A unique value identifying this w23 effettiterritorio. */
      path: {
        id_w23_effettiterritorio: string;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W23Effettiterritorio"];
        };
      };
    };
  };
  w23_effetti_update: {
    /** @description API endpoint that allows W23 bulletin Effetti sul territorio to be viewed */
    parameters: {
        /** @description A unique value identifying this w23 effettiterritorio. */
      path: {
        id_w23_effettiterritorio: string;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W23Effettiterritorio"];
        "application/x-www-form-urlencoded": components["schemas"]["W23Effettiterritorio"];
        "multipart/form-data": components["schemas"]["W23Effettiterritorio"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W23Effettiterritorio"];
        };
      };
    };
  };
  w23_effetti_destroy: {
    /** @description API endpoint that allows W23 bulletin Effetti sul territorio to be viewed */
    parameters: {
        /** @description A unique value identifying this w23 effettiterritorio. */
      path: {
        id_w23_effettiterritorio: string;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w23_effetti_partial_update: {
    /** @description API endpoint that allows W23 bulletin Effetti sul territorio to be viewed */
    parameters: {
        /** @description A unique value identifying this w23 effettiterritorio. */
      path: {
        id_w23_effettiterritorio: string;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW23Effettiterritorio"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW23Effettiterritorio"];
        "multipart/form-data": components["schemas"]["PatchedW23Effettiterritorio"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W23Effettiterritorio"];
        };
      };
    };
  };
  w23_pericoli_list: {
    /** @description API endpoint that allows W23 bulletin Pericolo to be viewed */
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W23Pericolo"])[];
        };
      };
    };
  };
  w23_pericoli_create: {
    /** @description API endpoint that allows W23 bulletin Pericolo to be viewed */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W23Pericolo"];
        "application/x-www-form-urlencoded": components["schemas"]["W23Pericolo"];
        "multipart/form-data": components["schemas"]["W23Pericolo"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W23Pericolo"];
        };
      };
    };
  };
  w23_pericoli_retrieve: {
    /** @description API endpoint that allows W23 bulletin Pericolo to be viewed */
    parameters: {
        /** @description A unique value identifying this w23 pericolo. */
      path: {
        id_w23_pericolo: string;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W23Pericolo"];
        };
      };
    };
  };
  w23_pericoli_update: {
    /** @description API endpoint that allows W23 bulletin Pericolo to be viewed */
    parameters: {
        /** @description A unique value identifying this w23 pericolo. */
      path: {
        id_w23_pericolo: string;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W23Pericolo"];
        "application/x-www-form-urlencoded": components["schemas"]["W23Pericolo"];
        "multipart/form-data": components["schemas"]["W23Pericolo"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W23Pericolo"];
        };
      };
    };
  };
  w23_pericoli_destroy: {
    /** @description API endpoint that allows W23 bulletin Pericolo to be viewed */
    parameters: {
        /** @description A unique value identifying this w23 pericolo. */
      path: {
        id_w23_pericolo: string;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w23_pericoli_partial_update: {
    /** @description API endpoint that allows W23 bulletin Pericolo to be viewed */
    parameters: {
        /** @description A unique value identifying this w23 pericolo. */
      path: {
        id_w23_pericolo: string;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW23Pericolo"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW23Pericolo"];
        "multipart/form-data": components["schemas"]["PatchedW23Pericolo"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W23Pericolo"];
        };
      };
    };
  };
  w23_pluvossh6_list: {
    parameters?: {
      query?: {
        area?: string;
        data?: string;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W23Pluvossh6"])[];
        };
      };
    };
  };
  w23_pluvossh6_create: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["W23Pluvossh6"];
        "application/x-www-form-urlencoded": components["schemas"]["W23Pluvossh6"];
        "multipart/form-data": components["schemas"]["W23Pluvossh6"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W23Pluvossh6"];
        };
      };
    };
  };
  w23_pluvossh6_retrieve: {
    parameters: {
        /** @description A unique integer value identifying this w23 pluvossh6. */
      path: {
        id_w23_pluvossh6: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W23Pluvossh6"];
        };
      };
    };
  };
  w23_pluvossh6_update: {
    parameters: {
        /** @description A unique integer value identifying this w23 pluvossh6. */
      path: {
        id_w23_pluvossh6: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W23Pluvossh6"];
        "application/x-www-form-urlencoded": components["schemas"]["W23Pluvossh6"];
        "multipart/form-data": components["schemas"]["W23Pluvossh6"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W23Pluvossh6"];
        };
      };
    };
  };
  w23_pluvossh6_destroy: {
    parameters: {
        /** @description A unique integer value identifying this w23 pluvossh6. */
      path: {
        id_w23_pluvossh6: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w23_pluvossh6_partial_update: {
    parameters: {
        /** @description A unique integer value identifying this w23 pluvossh6. */
      path: {
        id_w23_pluvossh6: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW23Pluvossh6"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW23Pluvossh6"];
        "multipart/form-data": components["schemas"]["PatchedW23Pluvossh6"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W23Pluvossh6"];
        };
      };
    };
  };
  w23_soglie_nivo_area_prev_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["SoglieNivoAreaPrev"])[];
        };
      };
    };
  };
  w23_soglie_nivo_area_prev_create: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["SoglieNivoAreaPrev"];
        "application/x-www-form-urlencoded": components["schemas"]["SoglieNivoAreaPrev"];
        "multipart/form-data": components["schemas"]["SoglieNivoAreaPrev"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["SoglieNivoAreaPrev"];
        };
      };
    };
  };
  w23_soglie_nivo_area_prev_retrieve: {
    parameters: {
        /** @description A unique value identifying this soglie nivo area prev. */
      path: {
        idtab_allertamento: string;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["SoglieNivoAreaPrev"];
        };
      };
    };
  };
  w23_soglie_nivo_area_prev_update: {
    parameters: {
        /** @description A unique value identifying this soglie nivo area prev. */
      path: {
        idtab_allertamento: string;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["SoglieNivoAreaPrev"];
        "application/x-www-form-urlencoded": components["schemas"]["SoglieNivoAreaPrev"];
        "multipart/form-data": components["schemas"]["SoglieNivoAreaPrev"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["SoglieNivoAreaPrev"];
        };
      };
    };
  };
  w23_soglie_nivo_area_prev_destroy: {
    parameters: {
        /** @description A unique value identifying this soglie nivo area prev. */
      path: {
        idtab_allertamento: string;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w23_soglie_nivo_area_prev_partial_update: {
    parameters: {
        /** @description A unique value identifying this soglie nivo area prev. */
      path: {
        idtab_allertamento: string;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedSoglieNivoAreaPrev"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedSoglieNivoAreaPrev"];
        "multipart/form-data": components["schemas"]["PatchedSoglieNivoAreaPrev"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["SoglieNivoAreaPrev"];
        };
      };
    };
  };
  w23_soglie_pluv_area_prev_massimi_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["SogliePluvAreaPrevMassimi"])[];
        };
      };
    };
  };
  w23_soglie_pluv_area_prev_massimi_create: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["SogliePluvAreaPrevMassimi"];
        "application/x-www-form-urlencoded": components["schemas"]["SogliePluvAreaPrevMassimi"];
        "multipart/form-data": components["schemas"]["SogliePluvAreaPrevMassimi"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["SogliePluvAreaPrevMassimi"];
        };
      };
    };
  };
  w23_soglie_pluv_area_prev_massimi_retrieve: {
    parameters: {
        /** @description A unique value identifying this soglie pluv area prev massimi. */
      path: {
        idtab_allertamento: string;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["SogliePluvAreaPrevMassimi"];
        };
      };
    };
  };
  w23_soglie_pluv_area_prev_massimi_update: {
    parameters: {
        /** @description A unique value identifying this soglie pluv area prev massimi. */
      path: {
        idtab_allertamento: string;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["SogliePluvAreaPrevMassimi"];
        "application/x-www-form-urlencoded": components["schemas"]["SogliePluvAreaPrevMassimi"];
        "multipart/form-data": components["schemas"]["SogliePluvAreaPrevMassimi"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["SogliePluvAreaPrevMassimi"];
        };
      };
    };
  };
  w23_soglie_pluv_area_prev_massimi_destroy: {
    parameters: {
        /** @description A unique value identifying this soglie pluv area prev massimi. */
      path: {
        idtab_allertamento: string;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w23_soglie_pluv_area_prev_massimi_partial_update: {
    parameters: {
        /** @description A unique value identifying this soglie pluv area prev massimi. */
      path: {
        idtab_allertamento: string;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedSogliePluvAreaPrevMassimi"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedSogliePluvAreaPrevMassimi"];
        "multipart/form-data": components["schemas"]["PatchedSogliePluvAreaPrevMassimi"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["SogliePluvAreaPrevMassimi"];
        };
      };
    };
  };
  w23_soglie_pluv_area_prev_medie_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["SogliePluvAreaPrevMedie"])[];
        };
      };
    };
  };
  w23_soglie_pluv_area_prev_medie_create: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["SogliePluvAreaPrevMedie"];
        "application/x-www-form-urlencoded": components["schemas"]["SogliePluvAreaPrevMedie"];
        "multipart/form-data": components["schemas"]["SogliePluvAreaPrevMedie"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["SogliePluvAreaPrevMedie"];
        };
      };
    };
  };
  w23_soglie_pluv_area_prev_medie_retrieve: {
    parameters: {
        /** @description A unique value identifying this soglie pluv area prev medie. */
      path: {
        idtab_allertamento: string;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["SogliePluvAreaPrevMedie"];
        };
      };
    };
  };
  w23_soglie_pluv_area_prev_medie_update: {
    parameters: {
        /** @description A unique value identifying this soglie pluv area prev medie. */
      path: {
        idtab_allertamento: string;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["SogliePluvAreaPrevMedie"];
        "application/x-www-form-urlencoded": components["schemas"]["SogliePluvAreaPrevMedie"];
        "multipart/form-data": components["schemas"]["SogliePluvAreaPrevMedie"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["SogliePluvAreaPrevMedie"];
        };
      };
    };
  };
  w23_soglie_pluv_area_prev_medie_destroy: {
    parameters: {
        /** @description A unique value identifying this soglie pluv area prev medie. */
      path: {
        idtab_allertamento: string;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w23_soglie_pluv_area_prev_medie_partial_update: {
    parameters: {
        /** @description A unique value identifying this soglie pluv area prev medie. */
      path: {
        idtab_allertamento: string;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedSogliePluvAreaPrevMedie"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedSogliePluvAreaPrevMedie"];
        "multipart/form-data": components["schemas"]["PatchedSogliePluvAreaPrevMedie"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["SogliePluvAreaPrevMedie"];
        };
      };
    };
  };
  w23_time_layouts_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["TimeLayouts"])[];
        };
      };
    };
  };
  w23_time_layouts_create: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["TimeLayouts"];
        "application/x-www-form-urlencoded": components["schemas"]["TimeLayouts"];
        "multipart/form-data": components["schemas"]["TimeLayouts"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["TimeLayouts"];
        };
      };
    };
  };
  w23_time_layouts_retrieve: {
    parameters: {
        /** @description A unique value identifying this time layouts. */
      path: {
        id_time_layouts: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["TimeLayouts"];
        };
      };
    };
  };
  w23_time_layouts_update: {
    parameters: {
        /** @description A unique value identifying this time layouts. */
      path: {
        id_time_layouts: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["TimeLayouts"];
        "application/x-www-form-urlencoded": components["schemas"]["TimeLayouts"];
        "multipart/form-data": components["schemas"]["TimeLayouts"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["TimeLayouts"];
        };
      };
    };
  };
  w23_time_layouts_destroy: {
    parameters: {
        /** @description A unique value identifying this time layouts. */
      path: {
        id_time_layouts: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w23_time_layouts_partial_update: {
    parameters: {
        /** @description A unique value identifying this time layouts. */
      path: {
        id_time_layouts: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedTimeLayouts"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedTimeLayouts"];
        "multipart/form-data": components["schemas"]["PatchedTimeLayouts"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["TimeLayouts"];
        };
      };
    };
  };
  w23_zone_list: {
    /** @description API endpoint that allows W23 bulletin Zone to be viewed */
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W23Zone"])[];
        };
      };
    };
  };
  w23_zone_create: {
    /** @description API endpoint that allows W23 bulletin Zone to be viewed */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W23Zone"];
        "application/x-www-form-urlencoded": components["schemas"]["W23Zone"];
        "multipart/form-data": components["schemas"]["W23Zone"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W23Zone"];
        };
      };
    };
  };
  w23_zone_retrieve: {
    /** @description API endpoint that allows W23 bulletin Zone to be viewed */
    parameters: {
        /** @description A unique value identifying this w23 zone. */
      path: {
        id_w23_zone: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W23Zone"];
        };
      };
    };
  };
  w23_zone_update: {
    /** @description API endpoint that allows W23 bulletin Zone to be viewed */
    parameters: {
        /** @description A unique value identifying this w23 zone. */
      path: {
        id_w23_zone: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W23Zone"];
        "application/x-www-form-urlencoded": components["schemas"]["W23Zone"];
        "multipart/form-data": components["schemas"]["W23Zone"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W23Zone"];
        };
      };
    };
  };
  w23_zone_destroy: {
    /** @description API endpoint that allows W23 bulletin Zone to be viewed */
    parameters: {
        /** @description A unique value identifying this w23 zone. */
      path: {
        id_w23_zone: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w23_zone_partial_update: {
    /** @description API endpoint that allows W23 bulletin Zone to be viewed */
    parameters: {
        /** @description A unique value identifying this w23 zone. */
      path: {
        id_w23_zone: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW23Zone"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW23Zone"];
        "multipart/form-data": components["schemas"]["PatchedW23Zone"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W23Zone"];
        };
      };
    };
  };
  w24_bulletins_list: {
    /** @description API endpoint that allows W24 bulletins to be viewed or edited */
    parameters?: {
        /** @description A page number within the paginated result set. */
      query?: {
        page?: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["PaginatedW24List"];
        };
      };
    };
  };
  w24_bulletins_create: {
    /** @description API endpoint that allows W24 bulletins to be viewed or edited */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W24"];
        "application/x-www-form-urlencoded": components["schemas"]["W24"];
        "multipart/form-data": components["schemas"]["W24"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W24"];
        };
      };
    };
  };
  w24_bulletins_retrieve: {
    /** @description API endpoint that allows W24 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w24. */
      path: {
        id_w24: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W24"];
        };
      };
    };
  };
  w24_bulletins_update: {
    /** @description API endpoint that allows W24 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w24. */
      path: {
        id_w24: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W24"];
        "application/x-www-form-urlencoded": components["schemas"]["W24"];
        "multipart/form-data": components["schemas"]["W24"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W24"];
        };
      };
    };
  };
  w24_bulletins_destroy: {
    /** @description API endpoint that allows W24 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w24. */
      path: {
        id_w24: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w24_bulletins_partial_update: {
    /** @description API endpoint that allows W24 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w24. */
      path: {
        id_w24: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW24"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW24"];
        "multipart/form-data": components["schemas"]["PatchedW24"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W24"];
        };
      };
    };
  };
  w24_bulletins_reopen_retrieve: {
    /** @description API endpoint that allows W24 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w24. */
      path: {
        id_w24: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W24"];
        };
      };
    };
  };
  w24_bulletins_send_retrieve: {
    /** @description API endpoint that allows W24 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w24. */
      path: {
        id_w24: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W24"];
        };
      };
    };
  };
  w24_bulletins_bulk_update_create: {
    /** @description API endpoint that allows W24 bulletins to be viewed or edited */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W24"];
        "application/x-www-form-urlencoded": components["schemas"]["W24"];
        "multipart/form-data": components["schemas"]["W24"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W24"];
        };
      };
    };
  };
  w24_bulletins_new_retrieve: {
    /** @description API endpoint that allows W24 bulletins to be viewed or edited */
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W24"];
        };
      };
    };
  };
  w24_current_retrieve: {
    /** @description View the latest W24 bulletin sent for a certain day */
    parameters: {
      path: {
        data_emissione: string;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W24SerializerFull"];
        };
      };
    };
  };
  w24_data_list: {
    /** @description API endpoint that allows W24 bulletin Data to be viewed or edited */
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W24Data"])[];
        };
      };
    };
  };
  w24_data_create: {
    /** @description API endpoint that allows W24 bulletin Data to be viewed or edited */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W24Data"];
        "application/x-www-form-urlencoded": components["schemas"]["W24Data"];
        "multipart/form-data": components["schemas"]["W24Data"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W24Data"];
        };
      };
    };
  };
  w24_data_retrieve: {
    /** @description API endpoint that allows W24 bulletin Data to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w24 data. */
      path: {
        id_w24_data: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W24Data"];
        };
      };
    };
  };
  w24_data_update: {
    /** @description API endpoint that allows W24 bulletin Data to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w24 data. */
      path: {
        id_w24_data: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W24Data"];
        "application/x-www-form-urlencoded": components["schemas"]["W24Data"];
        "multipart/form-data": components["schemas"]["W24Data"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W24Data"];
        };
      };
    };
  };
  w24_data_destroy: {
    /** @description API endpoint that allows W24 bulletin Data to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w24 data. */
      path: {
        id_w24_data: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w24_data_partial_update: {
    /** @description API endpoint that allows W24 bulletin Data to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w24 data. */
      path: {
        id_w24_data: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW24Data"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW24Data"];
        "multipart/form-data": components["schemas"]["PatchedW24Data"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W24Data"];
        };
      };
    };
  };
  w24_fz_list: {
    parameters?: {
      query?: {
        id_parametro?: string;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["ForecastZone"])[];
        };
      };
    };
  };
  w24_fz_create: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["ForecastZone"];
        "application/x-www-form-urlencoded": components["schemas"]["ForecastZone"];
        "multipart/form-data": components["schemas"]["ForecastZone"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["ForecastZone"];
        };
      };
    };
  };
  w24_fz_retrieve: {
    parameters: {
        /** @description A unique integer value identifying this forecast zone. */
      path: {
        id_forecast_zone: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["ForecastZone"];
        };
      };
    };
  };
  w24_fz_update: {
    parameters: {
        /** @description A unique integer value identifying this forecast zone. */
      path: {
        id_forecast_zone: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["ForecastZone"];
        "application/x-www-form-urlencoded": components["schemas"]["ForecastZone"];
        "multipart/form-data": components["schemas"]["ForecastZone"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["ForecastZone"];
        };
      };
    };
  };
  w24_fz_destroy: {
    parameters: {
        /** @description A unique integer value identifying this forecast zone. */
      path: {
        id_forecast_zone: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w24_fz_partial_update: {
    parameters: {
        /** @description A unique integer value identifying this forecast zone. */
      path: {
        id_forecast_zone: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedForecastZone"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedForecastZone"];
        "multipart/form-data": components["schemas"]["PatchedForecastZone"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["ForecastZone"];
        };
      };
    };
  };
  w24_soglie_list: {
    /** @description API endpoint that allows W24 bulletin Data to be viewed or edited */
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W24Soglie"])[];
        };
      };
    };
  };
  w24_soglie_create: {
    /** @description API endpoint that allows W24 bulletin Data to be viewed or edited */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W24Soglie"];
        "application/x-www-form-urlencoded": components["schemas"]["W24Soglie"];
        "multipart/form-data": components["schemas"]["W24Soglie"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W24Soglie"];
        };
      };
    };
  };
  w24_soglie_retrieve: {
    /** @description API endpoint that allows W24 bulletin Data to be viewed or edited */
    parameters: {
        /** @description A unique value identifying this w24 soglie. */
      path: {
        id_allertamento: string;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W24Soglie"];
        };
      };
    };
  };
  w24_soglie_update: {
    /** @description API endpoint that allows W24 bulletin Data to be viewed or edited */
    parameters: {
        /** @description A unique value identifying this w24 soglie. */
      path: {
        id_allertamento: string;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W24Soglie"];
        "application/x-www-form-urlencoded": components["schemas"]["W24Soglie"];
        "multipart/form-data": components["schemas"]["W24Soglie"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W24Soglie"];
        };
      };
    };
  };
  w24_soglie_destroy: {
    /** @description API endpoint that allows W24 bulletin Data to be viewed or edited */
    parameters: {
        /** @description A unique value identifying this w24 soglie. */
      path: {
        id_allertamento: string;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w24_soglie_partial_update: {
    /** @description API endpoint that allows W24 bulletin Data to be viewed or edited */
    parameters: {
        /** @description A unique value identifying this w24 soglie. */
      path: {
        id_allertamento: string;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW24Soglie"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW24Soglie"];
        "multipart/form-data": components["schemas"]["PatchedW24Soglie"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W24Soglie"];
        };
      };
    };
  };
  w26_bisbulletins_list: {
    /** @description API endpoint that allows W26 bulletins to be viewed or edited */
    parameters?: {
      query?: {
        codice?: string;
        data_max?: string;
        data_min?: string;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["BisBollettinoWebolimpia"])[];
        };
      };
    };
  };
  w26_bisbulletins_create: {
    /** @description API endpoint that allows W26 bulletins to be viewed or edited */
    requestBody?: {
      content: {
        "application/json": components["schemas"]["BisBollettinoWebolimpia"];
        "application/x-www-form-urlencoded": components["schemas"]["BisBollettinoWebolimpia"];
        "multipart/form-data": components["schemas"]["BisBollettinoWebolimpia"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["BisBollettinoWebolimpia"];
        };
      };
    };
  };
  w26_bisbulletins_retrieve: {
    /** @description API endpoint that allows W26 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique value identifying this bis bollettino webolimpia. */
      path: {
        codice: string;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["BisBollettinoWebolimpia"];
        };
      };
    };
  };
  w26_bisbulletins_update: {
    /** @description API endpoint that allows W26 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique value identifying this bis bollettino webolimpia. */
      path: {
        codice: string;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["BisBollettinoWebolimpia"];
        "application/x-www-form-urlencoded": components["schemas"]["BisBollettinoWebolimpia"];
        "multipart/form-data": components["schemas"]["BisBollettinoWebolimpia"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["BisBollettinoWebolimpia"];
        };
      };
    };
  };
  w26_bisbulletins_destroy: {
    /** @description API endpoint that allows W26 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique value identifying this bis bollettino webolimpia. */
      path: {
        codice: string;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w26_bisbulletins_partial_update: {
    /** @description API endpoint that allows W26 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique value identifying this bis bollettino webolimpia. */
      path: {
        codice: string;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedBisBollettinoWebolimpia"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedBisBollettinoWebolimpia"];
        "multipart/form-data": components["schemas"]["PatchedBisBollettinoWebolimpia"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["BisBollettinoWebolimpia"];
        };
      };
    };
  };
  w26_bulletins_list: {
    /** @description API endpoint that allows W26 bulletins to be viewed or edited */
    parameters?: {
        /** @description A page number within the paginated result set. */
      query?: {
        data_max?: string;
        data_min?: string;
        id_w26?: number;
        page?: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["PaginatedW26List"];
        };
      };
    };
  };
  w26_bulletins_create: {
    /** @description API endpoint that allows W26 bulletins to be viewed or edited */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W26"];
        "application/x-www-form-urlencoded": components["schemas"]["W26"];
        "multipart/form-data": components["schemas"]["W26"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W26"];
        };
      };
    };
  };
  w26_bulletins_retrieve: {
    /** @description API endpoint that allows W26 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w26. */
      path: {
        id_w26: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W26"];
        };
      };
    };
  };
  w26_bulletins_update: {
    /** @description API endpoint that allows W26 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w26. */
      path: {
        id_w26: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W26"];
        "application/x-www-form-urlencoded": components["schemas"]["W26"];
        "multipart/form-data": components["schemas"]["W26"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W26"];
        };
      };
    };
  };
  w26_bulletins_destroy: {
    /** @description API endpoint that allows W26 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w26. */
      path: {
        id_w26: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w26_bulletins_partial_update: {
    /** @description API endpoint that allows W26 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w26. */
      path: {
        id_w26: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW26"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW26"];
        "multipart/form-data": components["schemas"]["PatchedW26"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W26"];
        };
      };
    };
  };
  w26_bulletins_send_retrieve: {
    /** @description API endpoint that allows W26 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w26. */
      path: {
        id_w26: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W26"];
        };
      };
    };
  };
  w26_bulletins_bulk_update_create: {
    /** @description API endpoint that allows W26 bulletins to be viewed or edited */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W26"];
        "application/x-www-form-urlencoded": components["schemas"]["W26"];
        "multipart/form-data": components["schemas"]["W26"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W26"];
        };
      };
    };
  };
  w26_bulletins_new_retrieve: {
    /** @description API endpoint that allows W26 bulletins to be viewed or edited */
    parameters: {
      path: {
        validita: string;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W26"];
        };
      };
    };
  };
  w26_data_list: {
    /** @description API endpoint that allows W26 bulletin Data to be viewed or edited */
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W26Data"])[];
        };
      };
    };
  };
  w26_data_create: {
    /** @description API endpoint that allows W26 bulletin Data to be viewed or edited */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W26Data"];
        "application/x-www-form-urlencoded": components["schemas"]["W26Data"];
        "multipart/form-data": components["schemas"]["W26Data"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W26Data"];
        };
      };
    };
  };
  w26_data_retrieve: {
    /** @description API endpoint that allows W26 bulletin Data to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w26 data. */
      path: {
        id_w26_data: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W26Data"];
        };
      };
    };
  };
  w26_data_update: {
    /** @description API endpoint that allows W26 bulletin Data to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w26 data. */
      path: {
        id_w26_data: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W26Data"];
        "application/x-www-form-urlencoded": components["schemas"]["W26Data"];
        "multipart/form-data": components["schemas"]["W26Data"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W26Data"];
        };
      };
    };
  };
  w26_data_destroy: {
    /** @description API endpoint that allows W26 bulletin Data to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w26 data. */
      path: {
        id_w26_data: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w26_data_partial_update: {
    /** @description API endpoint that allows W26 bulletin Data to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w26 data. */
      path: {
        id_w26_data: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW26Data"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW26Data"];
        "multipart/form-data": components["schemas"]["PatchedW26Data"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W26Data"];
        };
      };
    };
  };
  w26_zone_list: {
    /** @description API endpoint that allows W26 bulletin Zone to be viewed or edited */
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W26Zone"])[];
        };
      };
    };
  };
  w26_zone_create: {
    /** @description API endpoint that allows W26 bulletin Zone to be viewed or edited */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W26Zone"];
        "application/x-www-form-urlencoded": components["schemas"]["W26Zone"];
        "multipart/form-data": components["schemas"]["W26Zone"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W26Zone"];
        };
      };
    };
  };
  w26_zone_retrieve: {
    /** @description API endpoint that allows W26 bulletin Zone to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w26 zone. */
      path: {
        id_w26_zone: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W26Zone"];
        };
      };
    };
  };
  w26_zone_update: {
    /** @description API endpoint that allows W26 bulletin Zone to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w26 zone. */
      path: {
        id_w26_zone: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W26Zone"];
        "application/x-www-form-urlencoded": components["schemas"]["W26Zone"];
        "multipart/form-data": components["schemas"]["W26Zone"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W26Zone"];
        };
      };
    };
  };
  w26_zone_destroy: {
    /** @description API endpoint that allows W26 bulletin Zone to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w26 zone. */
      path: {
        id_w26_zone: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w26_zone_partial_update: {
    /** @description API endpoint that allows W26 bulletin Zone to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w26 zone. */
      path: {
        id_w26_zone: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW26Zone"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW26Zone"];
        "multipart/form-data": components["schemas"]["PatchedW26Zone"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W26Zone"];
        };
      };
    };
  };
  w29_bulletins_list: {
    /** @description API endpoint that allows W29 bulletins to be viewed or edited */
    parameters?: {
        /** @description A page number within the paginated result set. */
      query?: {
        page?: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["PaginatedW29List"];
        };
      };
    };
  };
  w29_bulletins_create: {
    /** @description API endpoint that allows W29 bulletins to be viewed or edited */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W29"];
        "application/x-www-form-urlencoded": components["schemas"]["W29"];
        "multipart/form-data": components["schemas"]["W29"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W29"];
        };
      };
    };
  };
  w29_bulletins_retrieve: {
    /** @description API endpoint that allows W29 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w29. */
      path: {
        id_w29: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W29"];
        };
      };
    };
  };
  w29_bulletins_update: {
    /** @description API endpoint that allows W29 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w29. */
      path: {
        id_w29: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W29"];
        "application/x-www-form-urlencoded": components["schemas"]["W29"];
        "multipart/form-data": components["schemas"]["W29"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W29"];
        };
      };
    };
  };
  w29_bulletins_destroy: {
    /** @description API endpoint that allows W29 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w29. */
      path: {
        id_w29: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w29_bulletins_partial_update: {
    /** @description API endpoint that allows W29 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w29. */
      path: {
        id_w29: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW29"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW29"];
        "multipart/form-data": components["schemas"]["PatchedW29"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W29"];
        };
      };
    };
  };
  w29_bulletins_send_retrieve: {
    /** @description API endpoint that allows W29 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w29. */
      path: {
        id_w29: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W29"];
        };
      };
    };
  };
  w29_bulletins_bulk_update_create: {
    /** @description API endpoint that allows W29 bulletins to be viewed or edited */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W29"];
        "application/x-www-form-urlencoded": components["schemas"]["W29"];
        "multipart/form-data": components["schemas"]["W29"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W29"];
        };
      };
    };
  };
  w29_bulletins_new_retrieve: {
    /** @description API endpoint that allows W29 bulletins to be viewed or edited */
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W29"];
        };
      };
    };
  };
  w29_data_list: {
    /** @description API endpoint that allows W29 bulletin Data to be viewed or edited */
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W29Data"])[];
        };
      };
    };
  };
  w29_data_create: {
    /** @description API endpoint that allows W29 bulletin Data to be viewed or edited */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W29Data"];
        "application/x-www-form-urlencoded": components["schemas"]["W29Data"];
        "multipart/form-data": components["schemas"]["W29Data"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W29Data"];
        };
      };
    };
  };
  w29_data_retrieve: {
    /** @description API endpoint that allows W29 bulletin Data to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w29 data. */
      path: {
        id_w29_data: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W29Data"];
        };
      };
    };
  };
  w29_data_update: {
    /** @description API endpoint that allows W29 bulletin Data to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w29 data. */
      path: {
        id_w29_data: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W29Data"];
        "application/x-www-form-urlencoded": components["schemas"]["W29Data"];
        "multipart/form-data": components["schemas"]["W29Data"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W29Data"];
        };
      };
    };
  };
  w29_data_destroy: {
    /** @description API endpoint that allows W29 bulletin Data to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w29 data. */
      path: {
        id_w29_data: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w29_data_partial_update: {
    /** @description API endpoint that allows W29 bulletin Data to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w29 data. */
      path: {
        id_w29_data: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW29Data"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW29Data"];
        "multipart/form-data": components["schemas"]["PatchedW29Data"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W29Data"];
        };
      };
    };
  };
  w29_pericolo_list: {
    /** @description API endpoint that allows W29 bulletin Pericolo to be viewed or edited */
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W29Pericolo"])[];
        };
      };
    };
  };
  w29_pericolo_create: {
    /** @description API endpoint that allows W29 bulletin Pericolo to be viewed or edited */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W29Pericolo"];
        "application/x-www-form-urlencoded": components["schemas"]["W29Pericolo"];
        "multipart/form-data": components["schemas"]["W29Pericolo"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W29Pericolo"];
        };
      };
    };
  };
  w29_pericolo_retrieve: {
    /** @description API endpoint that allows W29 bulletin Pericolo to be viewed or edited */
    parameters: {
        /** @description A unique value identifying this w29 pericolo. */
      path: {
        id_w29_pericolo: string;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W29Pericolo"];
        };
      };
    };
  };
  w29_pericolo_update: {
    /** @description API endpoint that allows W29 bulletin Pericolo to be viewed or edited */
    parameters: {
        /** @description A unique value identifying this w29 pericolo. */
      path: {
        id_w29_pericolo: string;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W29Pericolo"];
        "application/x-www-form-urlencoded": components["schemas"]["W29Pericolo"];
        "multipart/form-data": components["schemas"]["W29Pericolo"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W29Pericolo"];
        };
      };
    };
  };
  w29_pericolo_destroy: {
    /** @description API endpoint that allows W29 bulletin Pericolo to be viewed or edited */
    parameters: {
        /** @description A unique value identifying this w29 pericolo. */
      path: {
        id_w29_pericolo: string;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w29_pericolo_partial_update: {
    /** @description API endpoint that allows W29 bulletin Pericolo to be viewed or edited */
    parameters: {
        /** @description A unique value identifying this w29 pericolo. */
      path: {
        id_w29_pericolo: string;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW29Pericolo"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW29Pericolo"];
        "multipart/form-data": components["schemas"]["PatchedW29Pericolo"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W29Pericolo"];
        };
      };
    };
  };
  w29_probabilita_list: {
    /** @description API endpoint that allows W29 bulletin Probabilita to be viewed or edited */
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W29Probabilita"])[];
        };
      };
    };
  };
  w29_probabilita_create: {
    /** @description API endpoint that allows W29 bulletin Probabilita to be viewed or edited */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W29Probabilita"];
        "application/x-www-form-urlencoded": components["schemas"]["W29Probabilita"];
        "multipart/form-data": components["schemas"]["W29Probabilita"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W29Probabilita"];
        };
      };
    };
  };
  w29_probabilita_retrieve: {
    /** @description API endpoint that allows W29 bulletin Probabilita to be viewed or edited */
    parameters: {
        /** @description A unique value identifying this w29 probabilita. */
      path: {
        id_w29_probabilita: string;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W29Probabilita"];
        };
      };
    };
  };
  w29_probabilita_update: {
    /** @description API endpoint that allows W29 bulletin Probabilita to be viewed or edited */
    parameters: {
        /** @description A unique value identifying this w29 probabilita. */
      path: {
        id_w29_probabilita: string;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W29Probabilita"];
        "application/x-www-form-urlencoded": components["schemas"]["W29Probabilita"];
        "multipart/form-data": components["schemas"]["W29Probabilita"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W29Probabilita"];
        };
      };
    };
  };
  w29_probabilita_destroy: {
    /** @description API endpoint that allows W29 bulletin Probabilita to be viewed or edited */
    parameters: {
        /** @description A unique value identifying this w29 probabilita. */
      path: {
        id_w29_probabilita: string;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w29_probabilita_partial_update: {
    /** @description API endpoint that allows W29 bulletin Probabilita to be viewed or edited */
    parameters: {
        /** @description A unique value identifying this w29 probabilita. */
      path: {
        id_w29_probabilita: string;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW29Probabilita"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW29Probabilita"];
        "multipart/form-data": components["schemas"]["PatchedW29Probabilita"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W29Probabilita"];
        };
      };
    };
  };
  w29_zone_list: {
    /** @description API endpoint that allows W29 bulletin Zone to be viewed or edited */
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W29Zone"])[];
        };
      };
    };
  };
  w29_zone_create: {
    /** @description API endpoint that allows W29 bulletin Zone to be viewed or edited */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W29Zone"];
        "application/x-www-form-urlencoded": components["schemas"]["W29Zone"];
        "multipart/form-data": components["schemas"]["W29Zone"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W29Zone"];
        };
      };
    };
  };
  w29_zone_retrieve: {
    /** @description API endpoint that allows W29 bulletin Zone to be viewed or edited */
    parameters: {
        /** @description A unique value identifying this w29 zone. */
      path: {
        id_w29_zone: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W29Zone"];
        };
      };
    };
  };
  w29_zone_update: {
    /** @description API endpoint that allows W29 bulletin Zone to be viewed or edited */
    parameters: {
        /** @description A unique value identifying this w29 zone. */
      path: {
        id_w29_zone: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W29Zone"];
        "application/x-www-form-urlencoded": components["schemas"]["W29Zone"];
        "multipart/form-data": components["schemas"]["W29Zone"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W29Zone"];
        };
      };
    };
  };
  w29_zone_destroy: {
    /** @description API endpoint that allows W29 bulletin Zone to be viewed or edited */
    parameters: {
        /** @description A unique value identifying this w29 zone. */
      path: {
        id_w29_zone: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w29_zone_partial_update: {
    /** @description API endpoint that allows W29 bulletin Zone to be viewed or edited */
    parameters: {
        /** @description A unique value identifying this w29 zone. */
      path: {
        id_w29_zone: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW29Zone"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW29Zone"];
        "multipart/form-data": components["schemas"]["PatchedW29Zone"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W29Zone"];
        };
      };
    };
  };
  w30_bulletins_list: {
    /** @description API endpoint that allows W30 bulletins to be viewed or edited */
    parameters?: {
        /** @description A page number within the paginated result set. */
      query?: {
        page?: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["PaginatedW30List"];
        };
      };
    };
  };
  w30_bulletins_create: {
    /** @description API endpoint that allows W30 bulletins to be viewed or edited */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W30"];
        "application/x-www-form-urlencoded": components["schemas"]["W30"];
        "multipart/form-data": components["schemas"]["W30"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W30"];
        };
      };
    };
  };
  w30_bulletins_retrieve: {
    /** @description API endpoint that allows W30 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w30. */
      path: {
        id_w30: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W30"];
        };
      };
    };
  };
  w30_bulletins_update: {
    /** @description API endpoint that allows W30 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w30. */
      path: {
        id_w30: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W30"];
        "application/x-www-form-urlencoded": components["schemas"]["W30"];
        "multipart/form-data": components["schemas"]["W30"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W30"];
        };
      };
    };
  };
  w30_bulletins_destroy: {
    /** @description API endpoint that allows W30 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w30. */
      path: {
        id_w30: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w30_bulletins_partial_update: {
    /** @description API endpoint that allows W30 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w30. */
      path: {
        id_w30: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW30"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW30"];
        "multipart/form-data": components["schemas"]["PatchedW30"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W30"];
        };
      };
    };
  };
  w30_bulletins_reopen_retrieve: {
    /** @description API endpoint that allows W30 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w30. */
      path: {
        id_w30: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W30"];
        };
      };
    };
  };
  w30_bulletins_send_retrieve: {
    /** @description API endpoint that allows W30 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w30. */
      path: {
        id_w30: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W30"];
        };
      };
    };
  };
  w30_bulletins_new_retrieve: {
    /** @description API endpoint that allows W30 bulletins to be viewed or edited */
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W30"];
        };
      };
    };
  };
  w30_current_retrieve: {
    /** @description View the latest W30 bulletin sent for a certain day */
    parameters: {
      path: {
        data_emissione: string;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W30SerializerFull"];
        };
      };
    };
  };
  w30_currentdata_list: {
    /** @description View the aggregated bulletin Data for the last 4 bulletins from the supplied date backwards */
    parameters: {
      path: {
        data_emissione: string;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W30CurrentDataView"])[];
        };
      };
    };
  };
  w30_data_list: {
    /** @description API endpoint that allows W30 bulletin Data to be viewed or edited */
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W30Data"])[];
        };
      };
    };
  };
  w30_data_create: {
    /** @description API endpoint that allows W30 bulletin Data to be viewed or edited */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W30Data"];
        "application/x-www-form-urlencoded": components["schemas"]["W30Data"];
        "multipart/form-data": components["schemas"]["W30Data"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W30Data"];
        };
      };
    };
  };
  w30_data_retrieve: {
    /** @description API endpoint that allows W30 bulletin Data to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w30 data. */
      path: {
        id_w30_data: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W30Data"];
        };
      };
    };
  };
  w30_data_update: {
    /** @description API endpoint that allows W30 bulletin Data to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w30 data. */
      path: {
        id_w30_data: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W30Data"];
        "application/x-www-form-urlencoded": components["schemas"]["W30Data"];
        "multipart/form-data": components["schemas"]["W30Data"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W30Data"];
        };
      };
    };
  };
  w30_data_destroy: {
    /** @description API endpoint that allows W30 bulletin Data to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w30 data. */
      path: {
        id_w30_data: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w30_data_partial_update: {
    /** @description API endpoint that allows W30 bulletin Data to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w30 data. */
      path: {
        id_w30_data: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW30Data"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW30Data"];
        "multipart/form-data": components["schemas"]["PatchedW30Data"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W30Data"];
        };
      };
    };
  };
  w30_data_bulk_update_create: {
    /** @description API endpoint that allows W30 bulletin Data to be viewed or edited */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W30Data"];
        "application/x-www-form-urlencoded": components["schemas"]["W30Data"];
        "multipart/form-data": components["schemas"]["W30Data"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W30Data"];
        };
      };
    };
  };
  w31_bulletins_list: {
    /** @description API endpoint that allows W31 bulletins to be viewed or edited */
    parameters?: {
        /** @description A page number within the paginated result set. */
      query?: {
        page?: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["PaginatedW31List"];
        };
      };
    };
  };
  w31_bulletins_create: {
    /** @description API endpoint that allows W31 bulletins to be viewed or edited */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W31"];
        "application/x-www-form-urlencoded": components["schemas"]["W31"];
        "multipart/form-data": components["schemas"]["W31"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W31"];
        };
      };
    };
  };
  w31_bulletins_retrieve: {
    /** @description API endpoint that allows W31 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w31. */
      path: {
        id_w31: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W31"];
        };
      };
    };
  };
  w31_bulletins_update: {
    /** @description API endpoint that allows W31 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w31. */
      path: {
        id_w31: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W31"];
        "application/x-www-form-urlencoded": components["schemas"]["W31"];
        "multipart/form-data": components["schemas"]["W31"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W31"];
        };
      };
    };
  };
  w31_bulletins_destroy: {
    /** @description API endpoint that allows W31 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w31. */
      path: {
        id_w31: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w31_bulletins_partial_update: {
    /** @description API endpoint that allows W31 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w31. */
      path: {
        id_w31: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW31"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW31"];
        "multipart/form-data": components["schemas"]["PatchedW31"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W31"];
        };
      };
    };
  };
  w31_bulletins_copy_retrieve: {
    /** @description API endpoint that allows W31 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w31. */
      path: {
        id_w31: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W31"];
        };
      };
    };
  };
  w31_bulletins_reopen_retrieve: {
    /** @description API endpoint that allows W31 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w31. */
      path: {
        id_w31: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W31"];
        };
      };
    };
  };
  w31_bulletins_send_retrieve: {
    /** @description API endpoint that allows W31 bulletins to be viewed or edited */
    parameters: {
        /** @description A unique integer value identifying this w31. */
      path: {
        id_w31: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W31"];
        };
      };
    };
  };
  w31_bulletins_bulk_update_create: {
    /** @description API endpoint that allows W31 bulletins to be viewed or edited */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W31"];
        "application/x-www-form-urlencoded": components["schemas"]["W31"];
        "multipart/form-data": components["schemas"]["W31"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W31"];
        };
      };
    };
  };
  w31_bulletins_new_retrieve: {
    /** @description API endpoint that allows W31 bulletins to be viewed or edited */
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W31"];
        };
      };
    };
  };
  w31_current_retrieve: {
    /** @description View the latest W31 bulletin sent */
    parameters: {
      path: {
        emissione: string;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W31SerializerFull"];
        };
      };
    };
  };
  w31_data_list: {
    /** @description API endpoint that allows W31 bulletin Data to be viewed or updated */
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W31DataMacroareeLivelli"])[];
        };
      };
    };
  };
  w31_data_create: {
    /** @description API endpoint that allows W31 bulletin Data to be viewed or updated */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W31DataMacroareeLivelli"];
        "application/x-www-form-urlencoded": components["schemas"]["W31DataMacroareeLivelli"];
        "multipart/form-data": components["schemas"]["W31DataMacroareeLivelli"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W31DataMacroareeLivelli"];
        };
      };
    };
  };
  w31_data_retrieve: {
    /** @description API endpoint that allows W31 bulletin Data to be viewed or updated */
    parameters: {
        /** @description A unique integer value identifying this w31 data macroaree livelli. */
      path: {
        id_w31_data_macroaree_livelli: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W31DataMacroareeLivelli"];
        };
      };
    };
  };
  w31_data_update: {
    /** @description API endpoint that allows W31 bulletin Data to be viewed or updated */
    parameters: {
        /** @description A unique integer value identifying this w31 data macroaree livelli. */
      path: {
        id_w31_data_macroaree_livelli: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W31DataMacroareeLivelli"];
        "application/x-www-form-urlencoded": components["schemas"]["W31DataMacroareeLivelli"];
        "multipart/form-data": components["schemas"]["W31DataMacroareeLivelli"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W31DataMacroareeLivelli"];
        };
      };
    };
  };
  w31_data_destroy: {
    /** @description API endpoint that allows W31 bulletin Data to be viewed or updated */
    parameters: {
        /** @description A unique integer value identifying this w31 data macroaree livelli. */
      path: {
        id_w31_data_macroaree_livelli: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w31_data_partial_update: {
    /** @description API endpoint that allows W31 bulletin Data to be viewed or updated */
    parameters: {
        /** @description A unique integer value identifying this w31 data macroaree livelli. */
      path: {
        id_w31_data_macroaree_livelli: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW31DataMacroareeLivelli"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW31DataMacroareeLivelli"];
        "multipart/form-data": components["schemas"]["PatchedW31DataMacroareeLivelli"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W31DataMacroareeLivelli"];
        };
      };
    };
  };
  w31_levels_list: {
    /** @description API endpoint that allows W31 levels to be viewed */
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W31Livelli"])[];
        };
      };
    };
  };
  w31_levels_create: {
    /** @description API endpoint that allows W31 levels to be viewed */
    requestBody: {
      content: {
        "application/json": components["schemas"]["W31Livelli"];
        "application/x-www-form-urlencoded": components["schemas"]["W31Livelli"];
        "multipart/form-data": components["schemas"]["W31Livelli"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W31Livelli"];
        };
      };
    };
  };
  w31_levels_retrieve: {
    /** @description API endpoint that allows W31 levels to be viewed */
    parameters: {
        /** @description A unique value identifying this w31 livelli. */
      path: {
        id_w31_livelli: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W31Livelli"];
        };
      };
    };
  };
  w31_levels_update: {
    /** @description API endpoint that allows W31 levels to be viewed */
    parameters: {
        /** @description A unique value identifying this w31 livelli. */
      path: {
        id_w31_livelli: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W31Livelli"];
        "application/x-www-form-urlencoded": components["schemas"]["W31Livelli"];
        "multipart/form-data": components["schemas"]["W31Livelli"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W31Livelli"];
        };
      };
    };
  };
  w31_levels_destroy: {
    /** @description API endpoint that allows W31 levels to be viewed */
    parameters: {
        /** @description A unique value identifying this w31 livelli. */
      path: {
        id_w31_livelli: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w31_levels_partial_update: {
    /** @description API endpoint that allows W31 levels to be viewed */
    parameters: {
        /** @description A unique value identifying this w31 livelli. */
      path: {
        id_w31_livelli: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW31Livelli"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW31Livelli"];
        "multipart/form-data": components["schemas"]["PatchedW31Livelli"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W31Livelli"];
        };
      };
    };
  };
}
