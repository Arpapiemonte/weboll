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
  "/w06/bulletins/": {
    /** @description API endpoint that allows W06 bulletins to be viewed or edited */
    get: operations["w06_bulletins_list"];
    /** @description API endpoint that allows W06 bulletins to be viewed or edited */
    post: operations["w06_bulletins_create"];
  };
  "/w06/bulletins/{id_w06}/": {
    /** @description API endpoint that allows W06 bulletins to be viewed or edited */
    get: operations["w06_bulletins_retrieve"];
    /** @description API endpoint that allows W06 bulletins to be viewed or edited */
    put: operations["w06_bulletins_update"];
    /** @description API endpoint that allows W06 bulletins to be viewed or edited */
    delete: operations["w06_bulletins_destroy"];
    /** @description API endpoint that allows W06 bulletins to be viewed or edited */
    patch: operations["w06_bulletins_partial_update"];
  };
  "/w06/bulletins/{id_w06}/reopen/": {
    /** @description API endpoint that allows W06 bulletins to be viewed or edited */
    get: operations["w06_bulletins_reopen_retrieve"];
  };
  "/w06/bulletins/{id_w06}/send/": {
    /** @description API endpoint that allows W06 bulletins to be viewed or edited */
    get: operations["w06_bulletins_send_retrieve"];
  };
  "/w06/bulletins/bulk_update/": {
    /** @description API endpoint that allows W06 bulletins to be viewed or edited */
    post: operations["w06_bulletins_bulk_update_create"];
  };
  "/w06/bulletins/new/": {
    /** @description API endpoint that allows W06 bulletins to be viewed or edited */
    get: operations["w06_bulletins_new_retrieve"];
  };
  "/w06/data/": {
    /** @description API endpoint that allows W06 bulletin Data to be viewed or edited */
    get: operations["w06_data_list"];
    /** @description API endpoint that allows W06 bulletin Data to be viewed or edited */
    post: operations["w06_data_create"];
  };
  "/w06/data/{id_w06_data}/": {
    /** @description API endpoint that allows W06 bulletin Data to be viewed or edited */
    get: operations["w06_data_retrieve"];
    /** @description API endpoint that allows W06 bulletin Data to be viewed or edited */
    put: operations["w06_data_update"];
    /** @description API endpoint that allows W06 bulletin Data to be viewed or edited */
    delete: operations["w06_data_destroy"];
    /** @description API endpoint that allows W06 bulletin Data to be viewed or edited */
    patch: operations["w06_data_partial_update"];
  };
  "/w07/bulletins/": {
    /** @description API endpoint that allows W07 bulletins to be viewed or edited */
    get: operations["w07_bulletins_list"];
    /** @description API endpoint that allows W07 bulletins to be viewed or edited */
    post: operations["w07_bulletins_create"];
  };
  "/w07/bulletins/{id_w07}/": {
    /** @description API endpoint that allows W07 bulletins to be viewed or edited */
    get: operations["w07_bulletins_retrieve"];
    /** @description API endpoint that allows W07 bulletins to be viewed or edited */
    put: operations["w07_bulletins_update"];
    /** @description API endpoint that allows W07 bulletins to be viewed or edited */
    delete: operations["w07_bulletins_destroy"];
    /** @description API endpoint that allows W07 bulletins to be viewed or edited */
    patch: operations["w07_bulletins_partial_update"];
  };
  "/w07/bulletins/{id_w07}/reopen/": {
    /** @description API endpoint that allows W07 bulletins to be viewed or edited */
    get: operations["w07_bulletins_reopen_retrieve"];
  };
  "/w07/bulletins/{id_w07}/send/": {
    /** @description API endpoint that allows W07 bulletins to be viewed or edited */
    get: operations["w07_bulletins_send_retrieve"];
  };
  "/w07/bulletins/bulk_update/": {
    /** @description API endpoint that allows W07 bulletins to be viewed or edited */
    post: operations["w07_bulletins_bulk_update_create"];
  };
  "/w07/bulletins/new/": {
    /** @description API endpoint that allows W07 bulletins to be viewed or edited */
    get: operations["w07_bulletins_new_retrieve"];
  };
  "/w07/data/": {
    /** @description API endpoint that allows w07 bulletin Data to be viewed or edited */
    get: operations["w07_data_list"];
    /** @description API endpoint that allows w07 bulletin Data to be viewed or edited */
    post: operations["w07_data_create"];
  };
  "/w07/data/{id_w07_data}/": {
    /** @description API endpoint that allows w07 bulletin Data to be viewed or edited */
    get: operations["w07_data_retrieve"];
    /** @description API endpoint that allows w07 bulletin Data to be viewed or edited */
    put: operations["w07_data_update"];
    /** @description API endpoint that allows w07 bulletin Data to be viewed or edited */
    delete: operations["w07_data_destroy"];
    /** @description API endpoint that allows w07 bulletin Data to be viewed or edited */
    patch: operations["w07_data_partial_update"];
  };
  "/w12/bulletins/": {
    /** @description API endpoint that allows W12 bulletins to be viewed or edited */
    get: operations["w12_bulletins_list"];
    /** @description API endpoint that allows W12 bulletins to be viewed or edited */
    post: operations["w12_bulletins_create"];
  };
  "/w12/bulletins/{id_w12}/": {
    /** @description API endpoint that allows W12 bulletins to be viewed or edited */
    get: operations["w12_bulletins_retrieve"];
    /** @description API endpoint that allows W12 bulletins to be viewed or edited */
    put: operations["w12_bulletins_update"];
    /** @description API endpoint that allows W12 bulletins to be viewed or edited */
    delete: operations["w12_bulletins_destroy"];
    /** @description API endpoint that allows W12 bulletins to be viewed or edited */
    patch: operations["w12_bulletins_partial_update"];
  };
  "/w12/bulletins/{id_w12}/reopen/": {
    /** @description API endpoint that allows W12 bulletins to be viewed or edited */
    get: operations["w12_bulletins_reopen_retrieve"];
  };
  "/w12/bulletins/{id_w12}/send/": {
    /** @description API endpoint that allows W12 bulletins to be viewed or edited */
    get: operations["w12_bulletins_send_retrieve"];
  };
  "/w12/bulletins/bulk_update/": {
    /** @description API endpoint that allows W12 bulletins to be viewed or edited */
    post: operations["w12_bulletins_bulk_update_create"];
  };
  "/w12/bulletins/new/": {
    /** @description API endpoint that allows W12 bulletins to be viewed or edited */
    get: operations["w12_bulletins_new_retrieve"];
  };
  "/w12/data/": {
    /** @description API endpoint that allows W12 bulletin Data to be viewed or edited */
    get: operations["w12_data_list"];
    /** @description API endpoint that allows W12 bulletin Data to be viewed or edited */
    post: operations["w12_data_create"];
  };
  "/w12/data/{id_w12_data}/": {
    /** @description API endpoint that allows W12 bulletin Data to be viewed or edited */
    get: operations["w12_data_retrieve"];
    /** @description API endpoint that allows W12 bulletin Data to be viewed or edited */
    put: operations["w12_data_update"];
    /** @description API endpoint that allows W12 bulletin Data to be viewed or edited */
    delete: operations["w12_data_destroy"];
    /** @description API endpoint that allows W12 bulletin Data to be viewed or edited */
    patch: operations["w12_data_partial_update"];
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
  "/w17/bulletins/": {
    /** @description API endpoint that allows W17 bulletins to be viewed or edited */
    get: operations["w17_bulletins_list"];
    /** @description API endpoint that allows W17 bulletins to be viewed or edited */
    post: operations["w17_bulletins_create"];
  };
  "/w17/bulletins/{id_w17}/": {
    /** @description API endpoint that allows W17 bulletins to be viewed or edited */
    get: operations["w17_bulletins_retrieve"];
    /** @description API endpoint that allows W17 bulletins to be viewed or edited */
    put: operations["w17_bulletins_update"];
    /** @description API endpoint that allows W17 bulletins to be viewed or edited */
    delete: operations["w17_bulletins_destroy"];
    /** @description API endpoint that allows W17 bulletins to be viewed or edited */
    patch: operations["w17_bulletins_partial_update"];
  };
  "/w17/bulletins/{id_w17}/copy/": {
    /** @description API endpoint that allows W17 bulletins to be viewed or edited */
    get: operations["w17_bulletins_copy_retrieve"];
  };
  "/w17/bulletins/{id_w17}/reopen/": {
    /** @description API endpoint that allows W17 bulletins to be viewed or edited */
    get: operations["w17_bulletins_reopen_retrieve"];
  };
  "/w17/bulletins/{id_w17}/send/": {
    /** @description API endpoint that allows W17 bulletins to be viewed or edited */
    get: operations["w17_bulletins_send_retrieve"];
  };
  "/w17/bulletins/bulk_update/": {
    /** @description API endpoint that allows W17 bulletins to be viewed or edited */
    post: operations["w17_bulletins_bulk_update_create"];
  };
  "/w17/bulletins/new/": {
    /** @description API endpoint that allows W17 bulletins to be viewed or edited */
    get: operations["w17_bulletins_new_retrieve"];
  };
  "/w17/bulletins_full/": {
    get: operations["w17_bulletins_full_list"];
    post: operations["w17_bulletins_full_create"];
  };
  "/w17/bulletins_full/{id_w17}/": {
    get: operations["w17_bulletins_full_retrieve"];
    put: operations["w17_bulletins_full_update"];
    delete: operations["w17_bulletins_full_destroy"];
    patch: operations["w17_bulletins_full_partial_update"];
  };
  "/w17/classes/": {
    /** @description API endpoint that allows W17 classes to be viewed */
    get: operations["w17_classes_list"];
    /** @description API endpoint that allows W17 classes to be viewed */
    post: operations["w17_classes_create"];
  };
  "/w17/classes/{id_w17_classes}/": {
    /** @description API endpoint that allows W17 classes to be viewed */
    get: operations["w17_classes_retrieve"];
    /** @description API endpoint that allows W17 classes to be viewed */
    put: operations["w17_classes_update"];
    /** @description API endpoint that allows W17 classes to be viewed */
    delete: operations["w17_classes_destroy"];
    /** @description API endpoint that allows W17 classes to be viewed */
    patch: operations["w17_classes_partial_update"];
  };
  "/w17/data/": {
    /** @description API endpoint that allows W17 bulletin Data to be viewed or edited */
    get: operations["w17_data_list"];
    /** @description API endpoint that allows W17 bulletin Data to be viewed or edited */
    post: operations["w17_data_create"];
  };
  "/w17/data/{id_w17_data}/": {
    /** @description API endpoint that allows W17 bulletin Data to be viewed or edited */
    get: operations["w17_data_retrieve"];
    /** @description API endpoint that allows W17 bulletin Data to be viewed or edited */
    put: operations["w17_data_update"];
    /** @description API endpoint that allows W17 bulletin Data to be viewed or edited */
    delete: operations["w17_data_destroy"];
    /** @description API endpoint that allows W17 bulletin Data to be viewed or edited */
    patch: operations["w17_data_partial_update"];
  };
  "/w17/stazioni/": {
    /** @description API endpoint that allows stations to be viewed */
    get: operations["w17_stazioni_list"];
    /** @description API endpoint that allows stations to be viewed */
    post: operations["w17_stazioni_create"];
  };
  "/w17/stazioni/{codice_istat_comune}/": {
    /** @description API endpoint that allows stations to be viewed */
    get: operations["w17_stazioni_retrieve"];
    /** @description API endpoint that allows stations to be viewed */
    put: operations["w17_stazioni_update"];
    /** @description API endpoint that allows stations to be viewed */
    delete: operations["w17_stazioni_destroy"];
    /** @description API endpoint that allows stations to be viewed */
    patch: operations["w17_stazioni_partial_update"];
  };
  "/w17/trend/": {
    /** @description API endpoint that allows trends to be viewed */
    get: operations["w17_trend_list"];
    /** @description API endpoint that allows trends to be viewed */
    post: operations["w17_trend_create"];
  };
  "/w17/trend/{id_trend}/": {
    /** @description API endpoint that allows trends to be viewed */
    get: operations["w17_trend_retrieve"];
    /** @description API endpoint that allows trends to be viewed */
    put: operations["w17_trend_update"];
    /** @description API endpoint that allows trends to be viewed */
    delete: operations["w17_trend_destroy"];
    /** @description API endpoint that allows trends to be viewed */
    patch: operations["w17_trend_partial_update"];
  };
  "/w17verifica/bulletins/": {
    /** @description API endpoint that allows W31 bulletins to be viewed or edited */
    get: operations["w17verifica_bulletins_list"];
    /** @description API endpoint that allows W31 bulletins to be viewed or edited */
    post: operations["w17verifica_bulletins_create"];
  };
  "/w17verifica/bulletins/{id_w17verifica}/": {
    /** @description API endpoint that allows W31 bulletins to be viewed or edited */
    get: operations["w17verifica_bulletins_retrieve"];
    /** @description API endpoint that allows W31 bulletins to be viewed or edited */
    put: operations["w17verifica_bulletins_update"];
    /** @description API endpoint that allows W31 bulletins to be viewed or edited */
    delete: operations["w17verifica_bulletins_destroy"];
    /** @description API endpoint that allows W31 bulletins to be viewed or edited */
    patch: operations["w17verifica_bulletins_partial_update"];
  };
  "/w17verifica/bulletins/{id_w17verifica}/copy/": {
    /** @description API endpoint that allows W31 bulletins to be viewed or edited */
    get: operations["w17verifica_bulletins_copy_retrieve"];
  };
  "/w17verifica/bulletins/{id_w17verifica}/reopen/": {
    /** @description API endpoint that allows W31 bulletins to be viewed or edited */
    get: operations["w17verifica_bulletins_reopen_retrieve"];
  };
  "/w17verifica/bulletins/{id_w17verifica}/send/": {
    /** @description API endpoint that allows W31 bulletins to be viewed or edited */
    get: operations["w17verifica_bulletins_send_retrieve"];
  };
  "/w17verifica/bulletins/bulk_update/": {
    /** @description API endpoint that allows W31 bulletins to be viewed or edited */
    post: operations["w17verifica_bulletins_bulk_update_create"];
  };
  "/w17verifica/bulletins/new/": {
    /** @description API endpoint that allows W31 bulletins to be viewed or edited */
    get: operations["w17verifica_bulletins_new_retrieve"];
  };
  "/w17verifica/data/": {
    /** @description API endpoint that allows W17verifica bulletin Data to be viewed or edited */
    get: operations["w17verifica_data_list"];
    /** @description API endpoint that allows W17verifica bulletin Data to be viewed or edited */
    post: operations["w17verifica_data_create"];
  };
  "/w17verifica/data/{id_w17_verifica_data}/": {
    /** @description API endpoint that allows W17verifica bulletin Data to be viewed or edited */
    get: operations["w17verifica_data_retrieve"];
    /** @description API endpoint that allows W17verifica bulletin Data to be viewed or edited */
    put: operations["w17verifica_data_update"];
    /** @description API endpoint that allows W17verifica bulletin Data to be viewed or edited */
    delete: operations["w17verifica_data_destroy"];
    /** @description API endpoint that allows W17verifica bulletin Data to be viewed or edited */
    patch: operations["w17verifica_data_partial_update"];
  };
  "/w17verifica/massimali/": {
    /** @description API endpoint that allows W17verificaMassimali bulletin Data to be viewed or edited */
    get: operations["w17verifica_massimali_list"];
    /** @description API endpoint that allows W17verificaMassimali bulletin Data to be viewed or edited */
    post: operations["w17verifica_massimali_create"];
  };
  "/w17verifica/massimali/{id_w17_verifica_massimali}/": {
    /** @description API endpoint that allows W17verificaMassimali bulletin Data to be viewed or edited */
    get: operations["w17verifica_massimali_retrieve"];
    /** @description API endpoint that allows W17verificaMassimali bulletin Data to be viewed or edited */
    put: operations["w17verifica_massimali_update"];
    /** @description API endpoint that allows W17verificaMassimali bulletin Data to be viewed or edited */
    delete: operations["w17verifica_massimali_destroy"];
    /** @description API endpoint that allows W17verificaMassimali bulletin Data to be viewed or edited */
    patch: operations["w17verifica_massimali_partial_update"];
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
  "/w26/bulletins/{id_w26}/reopen/": {
    /** @description API endpoint that allows W26 bulletins to be viewed or edited */
    get: operations["w26_bulletins_reopen_retrieve"];
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
  "/w28/bulletins/": {
    /** @description API endpoint that allows W28 bulletins to be viewed or edited */
    get: operations["w28_bulletins_list"];
    /** @description API endpoint that allows W28 bulletins to be viewed or edited */
    post: operations["w28_bulletins_create"];
  };
  "/w28/bulletins/{id_w28}/": {
    /** @description API endpoint that allows W28 bulletins to be viewed or edited */
    get: operations["w28_bulletins_retrieve"];
    /** @description API endpoint that allows W28 bulletins to be viewed or edited */
    put: operations["w28_bulletins_update"];
    /** @description API endpoint that allows W28 bulletins to be viewed or edited */
    delete: operations["w28_bulletins_destroy"];
    /** @description API endpoint that allows W28 bulletins to be viewed or edited */
    patch: operations["w28_bulletins_partial_update"];
  };
  "/w28/bulletins/{id_w28}/reopen/": {
    /** @description API endpoint that allows W28 bulletins to be viewed or edited */
    get: operations["w28_bulletins_reopen_retrieve"];
  };
  "/w28/bulletins/{id_w28}/send/": {
    /** @description API endpoint that allows W28 bulletins to be viewed or edited */
    get: operations["w28_bulletins_send_retrieve"];
  };
  "/w28/bulletins/bulk_update/": {
    /** @description API endpoint that allows W28 bulletins to be viewed or edited */
    post: operations["w28_bulletins_bulk_update_create"];
  };
  "/w28/bulletins/new/": {
    /** @description API endpoint that allows W28 bulletins to be viewed or edited */
    get: operations["w28_bulletins_new_retrieve"];
  };
  "/w28/data/": {
    /** @description API endpoint that allows w28 bulletin Data to be viewed or edited */
    get: operations["w28_data_list"];
    /** @description API endpoint that allows w28 bulletin Data to be viewed or edited */
    post: operations["w28_data_create"];
  };
  "/w28/data/{id_w28_data}/": {
    /** @description API endpoint that allows w28 bulletin Data to be viewed or edited */
    get: operations["w28_data_retrieve"];
    /** @description API endpoint that allows w28 bulletin Data to be viewed or edited */
    put: operations["w28_data_update"];
    /** @description API endpoint that allows w28 bulletin Data to be viewed or edited */
    delete: operations["w28_data_destroy"];
    /** @description API endpoint that allows w28 bulletin Data to be viewed or edited */
    patch: operations["w28_data_partial_update"];
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
  "/w32/bulletins/": {
    /** @description API endpoint that allows W32 bulletins to be viewed or edited */
    get: operations["w32_bulletins_list"];
    /** @description API endpoint that allows W32 bulletins to be viewed or edited */
    post: operations["w32_bulletins_create"];
  };
  "/w32/bulletins/{id_w32}/": {
    /** @description API endpoint that allows W32 bulletins to be viewed or edited */
    get: operations["w32_bulletins_retrieve"];
    /** @description API endpoint that allows W32 bulletins to be viewed or edited */
    put: operations["w32_bulletins_update"];
    /** @description API endpoint that allows W32 bulletins to be viewed or edited */
    delete: operations["w32_bulletins_destroy"];
    /** @description API endpoint that allows W32 bulletins to be viewed or edited */
    patch: operations["w32_bulletins_partial_update"];
  };
  "/w32/bulletins/{id_w32}/send/": {
    /** @description API endpoint that allows W32 bulletins to be viewed or edited */
    get: operations["w32_bulletins_send_retrieve"];
  };
  "/w32/bulletins/bulk_update/": {
    /** @description API endpoint that allows W32 bulletins to be viewed or edited */
    post: operations["w32_bulletins_bulk_update_create"];
  };
  "/w32/bulletins/new/": {
    /** @description API endpoint that allows W32 bulletins to be viewed or edited */
    get: operations["w32_bulletins_new_retrieve"];
  };
  "/w32/data/": {
    /** @description API endpoint that allows W32 bulletin Data to be viewed or edited */
    get: operations["w32_data_list"];
    /** @description API endpoint that allows W32 bulletin Data to be viewed or edited */
    post: operations["w32_data_create"];
  };
  "/w32/data/{id_w32_data}/": {
    /** @description API endpoint that allows W32 bulletin Data to be viewed or edited */
    get: operations["w32_data_retrieve"];
    /** @description API endpoint that allows W32 bulletin Data to be viewed or edited */
    put: operations["w32_data_update"];
    /** @description API endpoint that allows W32 bulletin Data to be viewed or edited */
    delete: operations["w32_data_destroy"];
    /** @description API endpoint that allows W32 bulletin Data to be viewed or edited */
    patch: operations["w32_data_partial_update"];
  };
  "/w32/datambacini/": {
    /** @description API endpoint that allows W32 bulletin MbaciniData to be viewed or edited */
    get: operations["w32_datambacini_list"];
    /** @description API endpoint that allows W32 bulletin MbaciniData to be viewed or edited */
    post: operations["w32_datambacini_create"];
  };
  "/w32/datambacini/{id_w32_mbacini_data}/": {
    /** @description API endpoint that allows W32 bulletin MbaciniData to be viewed or edited */
    get: operations["w32_datambacini_retrieve"];
    /** @description API endpoint that allows W32 bulletin MbaciniData to be viewed or edited */
    put: operations["w32_datambacini_update"];
    /** @description API endpoint that allows W32 bulletin MbaciniData to be viewed or edited */
    delete: operations["w32_datambacini_destroy"];
    /** @description API endpoint that allows W32 bulletin MbaciniData to be viewed or edited */
    patch: operations["w32_datambacini_partial_update"];
  };
  "/w32/mbacini/": {
    /** @description API endpoint that allows W32 bulletin Probabilita to be viewed or edited */
    get: operations["w32_mbacini_list"];
    /** @description API endpoint that allows W32 bulletin Probabilita to be viewed or edited */
    post: operations["w32_mbacini_create"];
  };
  "/w32/mbacini/{id_w32_mbacini}/": {
    /** @description API endpoint that allows W32 bulletin Probabilita to be viewed or edited */
    get: operations["w32_mbacini_retrieve"];
    /** @description API endpoint that allows W32 bulletin Probabilita to be viewed or edited */
    put: operations["w32_mbacini_update"];
    /** @description API endpoint that allows W32 bulletin Probabilita to be viewed or edited */
    delete: operations["w32_mbacini_destroy"];
    /** @description API endpoint that allows W32 bulletin Probabilita to be viewed or edited */
    patch: operations["w32_mbacini_partial_update"];
  };
  "/w32/pericolo/": {
    /** @description API endpoint that allows W32 bulletin Pericolo to be viewed or edited */
    get: operations["w32_pericolo_list"];
    /** @description API endpoint that allows W32 bulletin Pericolo to be viewed or edited */
    post: operations["w32_pericolo_create"];
  };
  "/w32/pericolo/{id_w32_pericolo}/": {
    /** @description API endpoint that allows W32 bulletin Pericolo to be viewed or edited */
    get: operations["w32_pericolo_retrieve"];
    /** @description API endpoint that allows W32 bulletin Pericolo to be viewed or edited */
    put: operations["w32_pericolo_update"];
    /** @description API endpoint that allows W32 bulletin Pericolo to be viewed or edited */
    delete: operations["w32_pericolo_destroy"];
    /** @description API endpoint that allows W32 bulletin Pericolo to be viewed or edited */
    patch: operations["w32_pericolo_partial_update"];
  };
  "/w32/pericolombacini/": {
    /** @description API endpoint that allows W32 bulletin Pericolombacini to be viewed or edited */
    get: operations["w32_pericolombacini_list"];
    /** @description API endpoint that allows W32 bulletin Pericolombacini to be viewed or edited */
    post: operations["w32_pericolombacini_create"];
  };
  "/w32/pericolombacini/{id_w32_pericolombacini}/": {
    /** @description API endpoint that allows W32 bulletin Pericolombacini to be viewed or edited */
    get: operations["w32_pericolombacini_retrieve"];
    /** @description API endpoint that allows W32 bulletin Pericolombacini to be viewed or edited */
    put: operations["w32_pericolombacini_update"];
    /** @description API endpoint that allows W32 bulletin Pericolombacini to be viewed or edited */
    delete: operations["w32_pericolombacini_destroy"];
    /** @description API endpoint that allows W32 bulletin Pericolombacini to be viewed or edited */
    patch: operations["w32_pericolombacini_partial_update"];
  };
  "/w32/zone/": {
    /** @description API endpoint that allows W32 bulletin Zone to be viewed or edited */
    get: operations["w32_zone_list"];
    /** @description API endpoint that allows W32 bulletin Zone to be viewed or edited */
    post: operations["w32_zone_create"];
  };
  "/w32/zone/{id_w32_zone}/": {
    /** @description API endpoint that allows W32 bulletin Zone to be viewed or edited */
    get: operations["w32_zone_retrieve"];
    /** @description API endpoint that allows W32 bulletin Zone to be viewed or edited */
    put: operations["w32_zone_update"];
    /** @description API endpoint that allows W32 bulletin Zone to be viewed or edited */
    delete: operations["w32_zone_destroy"];
    /** @description API endpoint that allows W32 bulletin Zone to be viewed or edited */
    patch: operations["w32_zone_partial_update"];
  };
  "/w33/bulletins/": {
    /** @description API endpoint that allows W33 bulletins to be viewed or edited */
    get: operations["w33_bulletins_list"];
    /** @description API endpoint that allows W33 bulletins to be viewed or edited */
    post: operations["w33_bulletins_create"];
  };
  "/w33/bulletins/{id_w33}/": {
    /** @description API endpoint that allows W33 bulletins to be viewed or edited */
    get: operations["w33_bulletins_retrieve"];
    /** @description API endpoint that allows W33 bulletins to be viewed or edited */
    put: operations["w33_bulletins_update"];
    /** @description API endpoint that allows W33 bulletins to be viewed or edited */
    delete: operations["w33_bulletins_destroy"];
    /** @description API endpoint that allows W33 bulletins to be viewed or edited */
    patch: operations["w33_bulletins_partial_update"];
  };
  "/w33/bulletins/{id_w33}/reopen/": {
    /** @description API endpoint that allows W33 bulletins to be viewed or edited */
    get: operations["w33_bulletins_reopen_retrieve"];
  };
  "/w33/bulletins/{id_w33}/send/": {
    /** @description API endpoint that allows W33 bulletins to be viewed or edited */
    get: operations["w33_bulletins_send_retrieve"];
  };
  "/w33/bulletins/bulk_update/": {
    /** @description API endpoint that allows W33 bulletins to be viewed or edited */
    post: operations["w33_bulletins_bulk_update_create"];
  };
  "/w33/bulletins/new/": {
    /** @description API endpoint that allows W33 bulletins to be viewed or edited */
    get: operations["w33_bulletins_new_retrieve"];
  };
  "/w33/data/": {
    /** @description API endpoint that allows W33 bulletin Data to be viewed or edited */
    get: operations["w33_data_list"];
    /** @description API endpoint that allows W33 bulletin Data to be viewed or edited */
    post: operations["w33_data_create"];
  };
  "/w33/data/{id_w33_data}/": {
    /** @description API endpoint that allows W33 bulletin Data to be viewed or edited */
    get: operations["w33_data_retrieve"];
    /** @description API endpoint that allows W33 bulletin Data to be viewed or edited */
    put: operations["w33_data_update"];
    /** @description API endpoint that allows W33 bulletin Data to be viewed or edited */
    delete: operations["w33_data_destroy"];
    /** @description API endpoint that allows W33 bulletin Data to be viewed or edited */
    patch: operations["w33_data_partial_update"];
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
    PaginatedW06List: {
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
      results?: (components["schemas"]["W06"])[];
    };
    PaginatedW07List: {
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
      results?: (components["schemas"]["W07"])[];
    };
    PaginatedW12List: {
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
      results?: (components["schemas"]["W12"])[];
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
    PaginatedW17List: {
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
      results?: (components["schemas"]["W17"])[];
    };
    PaginatedW17SerializerFullList: {
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
      results?: (components["schemas"]["W17SerializerFull"])[];
    };
    PaginatedW17verificaList: {
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
      results?: (components["schemas"]["W17verifica"])[];
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
    PaginatedW28List: {
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
      results?: (components["schemas"]["W28"])[];
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
    PaginatedW32List: {
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
      results?: (components["schemas"]["W32"])[];
    };
    PaginatedW33List: {
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
      results?: (components["schemas"]["W33"])[];
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
    PatchedStazioneMisura: {
      codice_istat_comune?: string;
      progr_punto_com?: number;
      codice_stazione?: string | null;
      nazione?: string | null;
      indirizzo_localita?: string | null;
      denominazione?: string;
      /** Format: decimal */
      latitudine_n?: string | null;
      /** Format: decimal */
      longitudine_e?: string | null;
      /** Format: decimal */
      latitudine_mm?: string | null;
      /** Format: decimal */
      longitudine_mm?: string | null;
      utm_x?: number | null;
      utm_y?: number | null;
      /** Format: decimal */
      quota_stazione?: string | null;
      /** Format: decimal */
      quota_sito?: string | null;
      cod_staz_meteo?: string | null;
      proprietario?: string | null;
      idtab_allertamento_2?: string | null;
      /** Format: date-time */
      data_agg?: string;
      autore_agg?: string;
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
    PatchedTrend: {
      id_trend?: number;
      id_web?: number;
      desc_ita?: string | null;
      desc_eng?: string | null;
      /** Format: date-time */
      last_update?: string;
      username?: string;
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
    PatchedW06: {
      id_w06?: number;
      /** Format: date-time */
      start_valid_time?: string;
      validity?: number;
      /** Format: date-time */
      next_blt_time?: string;
      status?: string;
      id_w06_parent?: number | null;
      /** Format: date-time */
      last_update?: string;
      username?: string;
    };
    PatchedW06Data: {
      id_w06_data?: number;
      sky_condition?: number | null;
      precipitation_class?: number | null;
      cumulated_snow?: number | null;
      freezing_level?: number | null;
      snow_level?: number | null;
      temperature_below_zero?: boolean | null;
      risk_freezing_rain?: boolean | null;
      id_w06?: number;
      id_venue?: number;
      id_time_layouts?: number;
    };
    PatchedW07: {
      id_w07?: number;
      id_w07_parent?: number | null;
      /** Format: date-time */
      start_valid_time?: string;
      validity?: number;
      /** Format: date-time */
      next_blt_time?: string;
      status?: string;
      /** Format: date-time */
      last_update?: string;
      username?: string;
    };
    PatchedW07Data: {
      id_w07_data?: number;
      precipitation_class?: number | null;
      cumulated_snow?: number | null;
      freezing_level?: number | null;
      snow_level?: number | null;
      temperature_below_zero?: boolean | null;
      air_temperature?: number | null;
      wind_class?: number | null;
      id_w07?: number;
      id_venue?: number;
      id_time_layouts?: number;
      sky_condition?: number;
    };
    PatchedW12: {
      id_w12?: number;
      id_w12_parent?: number | null;
      /** Format: date-time */
      start_valid_time?: string;
      validity?: number;
      /** Format: date-time */
      next_blt_time?: string;
      status?: string;
      /** Format: date-time */
      last_update?: string;
      username?: string;
    };
    PatchedW12Data: {
      id_w12_data?: number;
      cloud_amount?: number | null;
      precipitation_class?: number | null;
      cumulated_snow?: number | null;
      freezing_level?: number | null;
      snow_level?: number | null;
      temperature_below_zero?: boolean;
      risk_freezing_rain?: boolean;
      vis_inf_1000?: boolean;
      vis_inf_1000_reason?: number | null;
      wind_class?: number | null;
      id_w12?: number;
      id_venue?: number;
      id_time_layouts?: number;
      sky_condition?: number;
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
    PatchedW17: {
      id_w17?: number;
      /** Format: date */
      data_analysis?: string;
      /** Format: date */
      data_emissione?: string;
      /** Format: date */
      next_blt_time?: string;
      situation?: string | null;
      cloudiness?: string | null;
      weather_code?: string | null;
      /** Format: date-time */
      last_update?: string;
      username?: string;
      status?: string | null;
      numero_bollettino?: string;
      id_w17_parent?: number | null;
    };
    PatchedW17Classes: {
      id_w17_classes?: number;
      id_w17?: number;
      id_parametro?: string;
      id_classes_value?: number;
      id_classes?: number;
      id_time_layouts?: number;
    };
    PatchedW17Data: {
      id_w17_data?: number;
      /** Format: decimal */
      numeric_value?: string | null;
      id_trend?: number | null;
      text_value?: string | null;
      cod_staz_meteo?: string | null;
      id_w17?: number;
      id_venue?: number;
      id_time_layouts?: number;
      id_parametro?: string;
      id_aggregazione?: number;
    };
    PatchedW17SerializerFull: {
      id_w17?: number;
      w17data_set?: readonly (components["schemas"]["W17Data"])[];
      w17classes_set?: readonly (components["schemas"]["W17Classes"])[];
      w17blob_set?: readonly (components["schemas"]["W17Blob"])[];
      /** Format: date */
      data_analysis?: string;
      /** Format: date */
      data_emissione?: string;
      /** Format: date */
      next_blt_time?: string;
      situation?: string | null;
      cloudiness?: string | null;
      weather_code?: string | null;
      /** Format: date-time */
      last_update?: string;
      username?: string;
      status?: string | null;
      numero_bollettino?: string;
      id_w17_parent?: number | null;
    };
    PatchedW17verifica: {
      id_w17verifica?: number;
      /** Format: date */
      data_analysis?: string;
      /** Format: date */
      data_emissione?: string;
      /** Format: date */
      next_blt_time?: string;
      /** Format: date-time */
      last_update?: string;
      username?: string;
      status?: string | null;
    };
    PatchedW17verificaData: {
      id_w17_verifica_data?: number;
      /** Format: date */
      data_forecast?: string;
      forecast_id?: number | null;
      punteggio_relativo?: number | null;
      punteggio_nubi?: number | null;
      punteggio_pioggia?: number | null;
      punteggio_vento?: number | null;
      punteggio_temperatura?: number | null;
      punteggio_zero_quota_neve?: number | null;
      coerenza_mattino_nubi?: number | null;
      coerenza_pomeriggio_nubi?: number | null;
      coerenza_mattino_pioggia?: number | null;
      coerenza_pomeriggio_pioggia?: number | null;
      id_w17verifica?: number;
      id_w05?: number;
    };
    PatchedW17verificaMassimali: {
      id_w17_verifica_massimali?: number;
      id_aggregazione?: number | null;
      categoria?: number | null;
      punti_max?: number | null;
      /** Format: date-time */
      last_update?: string;
      username?: string;
      id_parametro?: string;
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
      id_w26_parent?: number | null;
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
    PatchedW28: {
      id_w28?: number;
      /** Format: date-time */
      start_valid_time?: string;
      validity?: number;
      /** Format: date-time */
      next_blt_time?: string;
      status?: string;
      id_w28_parent?: number | null;
      /** Format: date-time */
      last_update?: string;
      username?: string;
    };
    PatchedW28Data: {
      id_w28_data?: number;
      precipitation_class?: number | null;
      cumulated_snow?: number | null;
      freezing_level?: number | null;
      snow_level?: number | null;
      temperature_below_zero?: boolean | null;
      risk_freezing_rain?: boolean | null;
      id_w28?: number;
      id_venue?: number;
      id_time_layouts?: number;
      sky_condition?: number;
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
      wind?: string;
      id_w31?: number;
      id_w31_livelli?: number;
      id_time_layouts?: number;
    };
    PatchedW31Livelli: {
      id_w31_livelli?: number;
      colore?: string;
    };
    PatchedW32: {
      id_w32?: number;
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
    PatchedW32Data: {
      id_w32_data?: number;
      id_w32_zone?: components["schemas"]["W32Zone"];
      livello_criticita_oss?: string;
      livello_criticita_prev_oggi?: string;
      livello_criticita_prev_domani?: string;
      id_w32?: number;
    };
    PatchedW32Mbacini: {
      id_w32_mbacini?: number;
      area?: string;
      descrizione?: string;
      ordinamento?: number;
    };
    PatchedW32MbaciniData: {
      id_w32_mbacini_data?: number;
      id_w32_mbacini?: components["schemas"]["W32Mbacini"];
      livello_criticita_oss?: string;
      livello_criticita_prev_oggi?: string;
      livello_criticita_prev_domani?: string;
      id_w32?: number;
    };
    PatchedW32Pericolo: {
      id_w32_pericolo?: string;
      descrizione?: string | null;
    };
    PatchedW32Pericolombacini: {
      id_w32_pericolombacini?: string;
      descrizione?: string | null;
    };
    PatchedW32Zone: {
      id_w32_zone?: number;
      descrizione?: string;
    };
    PatchedW33: {
      id_w33?: number;
      id_w33_parent?: number | null;
      /** Format: date */
      data_emissione?: string;
      seq_num?: number;
      status?: string;
      /** Format: date-time */
      last_update?: string;
      username?: string;
    };
    PatchedW33Data: {
      id_w33_data?: number;
      cumulated_snow?: number | null;
      snow_level?: number | null;
      id_w33?: number;
      id_venue?: number;
      id_time_layouts?: number;
      id_sky_condition?: number;
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
    StazioneMisura: {
      codice_istat_comune: string;
      progr_punto_com: number;
      codice_stazione?: string | null;
      nazione?: string | null;
      indirizzo_localita?: string | null;
      denominazione: string;
      /** Format: decimal */
      latitudine_n?: string | null;
      /** Format: decimal */
      longitudine_e?: string | null;
      /** Format: decimal */
      latitudine_mm?: string | null;
      /** Format: decimal */
      longitudine_mm?: string | null;
      utm_x?: number | null;
      utm_y?: number | null;
      /** Format: decimal */
      quota_stazione?: string | null;
      /** Format: decimal */
      quota_sito?: string | null;
      cod_staz_meteo?: string | null;
      proprietario?: string | null;
      idtab_allertamento_2?: string | null;
      /** Format: date-time */
      data_agg: string;
      autore_agg: string;
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
    Trend: {
      id_trend: number;
      id_web: number;
      desc_ita?: string | null;
      desc_eng?: string | null;
      /** Format: date-time */
      last_update: string;
      username: string;
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
    W06: {
      id_w06: number;
      /** Format: date-time */
      start_valid_time: string;
      validity: number;
      /** Format: date-time */
      next_blt_time: string;
      status: string;
      id_w06_parent?: number | null;
      /** Format: date-time */
      last_update: string;
      username: string;
    };
    W06Data: {
      id_w06_data: number;
      sky_condition?: number | null;
      precipitation_class?: number | null;
      cumulated_snow?: number | null;
      freezing_level?: number | null;
      snow_level?: number | null;
      temperature_below_zero?: boolean | null;
      risk_freezing_rain?: boolean | null;
      id_w06: number;
      id_venue: number;
      id_time_layouts: number;
    };
    W07: {
      id_w07: number;
      id_w07_parent?: number | null;
      /** Format: date-time */
      start_valid_time: string;
      validity: number;
      /** Format: date-time */
      next_blt_time: string;
      status: string;
      /** Format: date-time */
      last_update: string;
      username: string;
    };
    W07Data: {
      id_w07_data: number;
      precipitation_class?: number | null;
      cumulated_snow?: number | null;
      freezing_level?: number | null;
      snow_level?: number | null;
      temperature_below_zero?: boolean | null;
      air_temperature?: number | null;
      wind_class?: number | null;
      id_w07: number;
      id_venue: number;
      id_time_layouts: number;
      sky_condition: number;
    };
    W12: {
      id_w12: number;
      id_w12_parent?: number | null;
      /** Format: date-time */
      start_valid_time: string;
      validity: number;
      /** Format: date-time */
      next_blt_time: string;
      status: string;
      /** Format: date-time */
      last_update: string;
      username: string;
    };
    W12Data: {
      id_w12_data: number;
      cloud_amount?: number | null;
      precipitation_class?: number | null;
      cumulated_snow?: number | null;
      freezing_level?: number | null;
      snow_level?: number | null;
      temperature_below_zero: boolean;
      risk_freezing_rain: boolean;
      vis_inf_1000: boolean;
      vis_inf_1000_reason?: number | null;
      wind_class?: number | null;
      id_w12: number;
      id_venue: number;
      id_time_layouts: number;
      sky_condition: number;
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
    W17: {
      id_w17: number;
      /** Format: date */
      data_analysis: string;
      /** Format: date */
      data_emissione: string;
      /** Format: date */
      next_blt_time: string;
      situation?: string | null;
      cloudiness?: string | null;
      weather_code?: string | null;
      /** Format: date-time */
      last_update: string;
      username: string;
      status?: string | null;
      numero_bollettino: string;
      id_w17_parent?: number | null;
    };
    W17Blob: {
      id_w17: number;
      /** Format: byte */
      situation_image: string | null;
      /** Format: byte */
      cloudiness_image: string | null;
      /** Format: byte */
      prec_mattino_image: string | null;
      /** Format: byte */
      prec_pomeriggio_image: string | null;
      /** Format: byte */
      temp_minime_image: string | null;
      /** Format: byte */
      temp_massime_image: string | null;
    };
    W17Classes: {
      id_w17_classes: number;
      id_w17: number;
      id_parametro: string;
      id_classes_value: number;
      id_classes: number;
      id_time_layouts: number;
    };
    W17Data: {
      id_w17_data: number;
      /** Format: decimal */
      numeric_value?: string | null;
      id_trend?: number | null;
      text_value?: string | null;
      cod_staz_meteo?: string | null;
      id_w17: number;
      id_venue: number;
      id_time_layouts: number;
      id_parametro: string;
      id_aggregazione: number;
    };
    W17SerializerFull: {
      id_w17: number;
      w17data_set: readonly (components["schemas"]["W17Data"])[];
      w17classes_set: readonly (components["schemas"]["W17Classes"])[];
      w17blob_set: readonly (components["schemas"]["W17Blob"])[];
      /** Format: date */
      data_analysis: string;
      /** Format: date */
      data_emissione: string;
      /** Format: date */
      next_blt_time: string;
      situation?: string | null;
      cloudiness?: string | null;
      weather_code?: string | null;
      /** Format: date-time */
      last_update: string;
      username: string;
      status?: string | null;
      numero_bollettino: string;
      id_w17_parent?: number | null;
    };
    W17verifica: {
      id_w17verifica: number;
      /** Format: date */
      data_analysis: string;
      /** Format: date */
      data_emissione: string;
      /** Format: date */
      next_blt_time: string;
      /** Format: date-time */
      last_update: string;
      username: string;
      status?: string | null;
    };
    W17verificaData: {
      id_w17_verifica_data: number;
      /** Format: date */
      data_forecast: string;
      forecast_id?: number | null;
      punteggio_relativo?: number | null;
      punteggio_nubi?: number | null;
      punteggio_pioggia?: number | null;
      punteggio_vento?: number | null;
      punteggio_temperatura?: number | null;
      punteggio_zero_quota_neve?: number | null;
      coerenza_mattino_nubi?: number | null;
      coerenza_pomeriggio_nubi?: number | null;
      coerenza_mattino_pioggia?: number | null;
      coerenza_pomeriggio_pioggia?: number | null;
      id_w17verifica: number;
      id_w05: number;
    };
    W17verificaMassimali: {
      id_w17_verifica_massimali: number;
      id_aggregazione?: number | null;
      categoria?: number | null;
      punti_max?: number | null;
      /** Format: date-time */
      last_update: string;
      username: string;
      id_parametro: string;
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
      id_w26_parent?: number | null;
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
    W28: {
      id_w28: number;
      /** Format: date-time */
      start_valid_time: string;
      validity: number;
      /** Format: date-time */
      next_blt_time: string;
      status: string;
      id_w28_parent?: number | null;
      /** Format: date-time */
      last_update: string;
      username: string;
    };
    W28Data: {
      id_w28_data: number;
      precipitation_class?: number | null;
      cumulated_snow?: number | null;
      freezing_level?: number | null;
      snow_level?: number | null;
      temperature_below_zero?: boolean | null;
      risk_freezing_rain?: boolean | null;
      id_w28: number;
      id_venue: number;
      id_time_layouts: number;
      sky_condition: number;
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
      wind: string;
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
      ordine_bollettino: number;
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
    W32: {
      id_w32: number;
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
    W32Data: {
      id_w32_data: number;
      id_w32_zone: components["schemas"]["W32Zone"];
      livello_criticita_oss: string;
      livello_criticita_prev_oggi: string;
      livello_criticita_prev_domani: string;
      id_w32: number;
    };
    W32Mbacini: {
      id_w32_mbacini: number;
      area: string;
      descrizione: string;
      ordinamento: number;
    };
    W32MbaciniData: {
      id_w32_mbacini_data: number;
      id_w32_mbacini: components["schemas"]["W32Mbacini"];
      livello_criticita_oss: string;
      livello_criticita_prev_oggi: string;
      livello_criticita_prev_domani: string;
      id_w32: number;
    };
    W32Pericolo: {
      id_w32_pericolo: string;
      descrizione?: string | null;
    };
    W32Pericolombacini: {
      id_w32_pericolombacini: string;
      descrizione?: string | null;
    };
    W32Zone: {
      id_w32_zone: number;
      descrizione: string;
    };
    W33: {
      id_w33: number;
      id_w33_parent?: number | null;
      /** Format: date */
      data_emissione: string;
      seq_num: number;
      status: string;
      /** Format: date-time */
      last_update: string;
      username: string;
    };
    W33Data: {
      id_w33_data: number;
      cumulated_snow?: number | null;
      snow_level?: number | null;
      id_w33: number;
      id_venue: number;
      id_time_layouts: number;
      id_sky_condition: number;
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

  /**
   * @description Takes a set of user credentials and returns an access and refresh JSON web
   * token pair to prove the authentication of those credentials.
   */
  token_create: {
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
  /**
   * @description Takes a refresh type JSON web token and returns an access type JSON web
   * token if the refresh token is valid.
   */
  token_refresh_create: {
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
  /**
   * @description Takes a token and indicates if it is valid.  This view provides no
   * information about a token's fitness for a particular use.
   */
  token_verify_create: {
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
  /** @description API endpoint that allows W05 bulletins to be viewed or edited */
  w05_bulletins_list: {
    parameters: {
      query?: {
        /** @description A page number within the paginated result set. */
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
  /** @description API endpoint that allows W05 bulletins to be viewed or edited */
  w05_bulletins_create: {
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
  /** @description API endpoint that allows W05 bulletins to be viewed or edited */
  w05_bulletins_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w05. */
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
  /** @description API endpoint that allows W05 bulletins to be viewed or edited */
  w05_bulletins_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w05. */
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
  /** @description API endpoint that allows W05 bulletins to be viewed or edited */
  w05_bulletins_destroy: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w05. */
        id_w05: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W05 bulletins to be viewed or edited */
  w05_bulletins_partial_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w05. */
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
  /** @description API endpoint that allows W05 bulletins to be viewed or edited */
  w05_bulletins_classes_json_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w05. */
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
  /** @description API endpoint that allows W05 bulletins to be viewed or edited */
  w05_bulletins_data_json_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w05. */
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
  /** @description API endpoint that allows W05 bulletins to be viewed or edited */
  w05_bulletins_json_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w05. */
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
  /** @description API endpoint that allows W05 bulletins to be viewed or edited */
  w05_bulletins_reload_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w05. */
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
  /** @description API endpoint that allows W05 bulletins to be viewed or edited */
  w05_bulletins_reopen_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w05. */
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
  /** @description API endpoint that allows W05 bulletins to be viewed or edited */
  w05_bulletins_resend_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w05. */
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
  /** @description API endpoint that allows W05 bulletins to be viewed or edited */
  w05_bulletins_send_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w05. */
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
  /** @description API endpoint that allows W05 bulletins to be viewed or edited */
  w05_bulletins_xml_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w05. */
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
  /** @description API endpoint that allows W05 bulletins to be viewed or edited */
  w05_bulletins_bulk_update_create: {
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
  /** @description API endpoint that allows W05 bulletins to be viewed or edited */
  w05_bulletins_new_retrieve: {
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W05"];
        };
      };
    };
  };
  /** @description API endpoint that allows Classes to be viewed */
  w05_classes_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["Classes"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows Classes to be viewed */
  w05_classes_create: {
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
  /** @description API endpoint that allows Classes to be viewed */
  w05_classes_retrieve: {
    parameters: {
      path: {
        /** @description A unique value identifying this classes. */
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
  /** @description API endpoint that allows Classes to be viewed */
  w05_classes_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this classes. */
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
  /** @description API endpoint that allows Classes to be viewed */
  w05_classes_destroy: {
    parameters: {
      path: {
        /** @description A unique value identifying this classes. */
        id_classes: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows Classes to be viewed */
  w05_classes_partial_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this classes. */
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
  /** @description API endpoint that allows W05 bulletin Data to be viewed or edited */
  w05_data_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W05Data"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows W05 bulletin Data to be viewed or edited */
  w05_data_create: {
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
  /** @description API endpoint that allows W05 bulletin Data to be viewed or edited */
  w05_data_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w05 data. */
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
  /** @description API endpoint that allows W05 bulletin Data to be viewed or edited */
  w05_data_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w05 data. */
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
  /** @description API endpoint that allows W05 bulletin Data to be viewed or edited */
  w05_data_destroy: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w05 data. */
        id_w05_data: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W05 bulletin Data to be viewed or edited */
  w05_data_partial_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w05 data. */
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
  /** @description API endpoint that allows W05 bulletin Classes to be viewed or edited */
  w05_meteo_classes_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W05Classes"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows W05 bulletin Classes to be viewed or edited */
  w05_meteo_classes_create: {
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
  /** @description API endpoint that allows W05 bulletin Classes to be viewed or edited */
  w05_meteo_classes_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w05 classes. */
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
  /** @description API endpoint that allows W05 bulletin Classes to be viewed or edited */
  w05_meteo_classes_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w05 classes. */
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
  /** @description API endpoint that allows W05 bulletin Classes to be viewed or edited */
  w05_meteo_classes_destroy: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w05 classes. */
        id_w05_classes: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W05 bulletin Classes to be viewed or edited */
  w05_meteo_classes_partial_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w05 classes. */
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
  /** @description API endpoint that allows W16 bulletins to be viewed or edited */
  w05_sky_conditions_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["SkyCondition"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows W16 bulletins to be viewed or edited */
  w05_sky_conditions_create: {
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
  /** @description API endpoint that allows W16 bulletins to be viewed or edited */
  w05_sky_conditions_retrieve: {
    parameters: {
      path: {
        /** @description A unique value identifying this sky condition. */
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
  /** @description API endpoint that allows W16 bulletins to be viewed or edited */
  w05_sky_conditions_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this sky condition. */
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
  /** @description API endpoint that allows W16 bulletins to be viewed or edited */
  w05_sky_conditions_destroy: {
    parameters: {
      path: {
        /** @description A unique value identifying this sky condition. */
        id_sky_condition: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W16 bulletins to be viewed or edited */
  w05_sky_conditions_partial_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this sky condition. */
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
  /** @description API endpoint that shows city names */
  w05_venue_names_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["Venue"])[];
        };
      };
    };
  };
  /** @description API endpoint that shows city names */
  w05_venue_names_create: {
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
  /** @description API endpoint that shows city names */
  w05_venue_names_retrieve: {
    parameters: {
      path: {
        /** @description A unique value identifying this venue. */
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
  /** @description API endpoint that shows city names */
  w05_venue_names_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this venue. */
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
  /** @description API endpoint that shows city names */
  w05_venue_names_destroy: {
    parameters: {
      path: {
        /** @description A unique value identifying this venue. */
        id_venue: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that shows city names */
  w05_venue_names_partial_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this venue. */
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
  /** @description API endpoint that allows W06 bulletins to be viewed or edited */
  w06_bulletins_list: {
    parameters: {
      query?: {
        /** @description A page number within the paginated result set. */
        page?: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["PaginatedW06List"];
        };
      };
    };
  };
  /** @description API endpoint that allows W06 bulletins to be viewed or edited */
  w06_bulletins_create: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["W06"];
        "application/x-www-form-urlencoded": components["schemas"]["W06"];
        "multipart/form-data": components["schemas"]["W06"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W06"];
        };
      };
    };
  };
  /** @description API endpoint that allows W06 bulletins to be viewed or edited */
  w06_bulletins_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w06. */
        id_w06: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W06"];
        };
      };
    };
  };
  /** @description API endpoint that allows W06 bulletins to be viewed or edited */
  w06_bulletins_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w06. */
        id_w06: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W06"];
        "application/x-www-form-urlencoded": components["schemas"]["W06"];
        "multipart/form-data": components["schemas"]["W06"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W06"];
        };
      };
    };
  };
  /** @description API endpoint that allows W06 bulletins to be viewed or edited */
  w06_bulletins_destroy: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w06. */
        id_w06: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W06 bulletins to be viewed or edited */
  w06_bulletins_partial_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w06. */
        id_w06: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW06"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW06"];
        "multipart/form-data": components["schemas"]["PatchedW06"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W06"];
        };
      };
    };
  };
  /** @description API endpoint that allows W06 bulletins to be viewed or edited */
  w06_bulletins_reopen_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w06. */
        id_w06: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W06"];
        };
      };
    };
  };
  /** @description API endpoint that allows W06 bulletins to be viewed or edited */
  w06_bulletins_send_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w06. */
        id_w06: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W06"];
        };
      };
    };
  };
  /** @description API endpoint that allows W06 bulletins to be viewed or edited */
  w06_bulletins_bulk_update_create: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["W06"];
        "application/x-www-form-urlencoded": components["schemas"]["W06"];
        "multipart/form-data": components["schemas"]["W06"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W06"];
        };
      };
    };
  };
  /** @description API endpoint that allows W06 bulletins to be viewed or edited */
  w06_bulletins_new_retrieve: {
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W06"];
        };
      };
    };
  };
  /** @description API endpoint that allows W06 bulletin Data to be viewed or edited */
  w06_data_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W06Data"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows W06 bulletin Data to be viewed or edited */
  w06_data_create: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["W06Data"];
        "application/x-www-form-urlencoded": components["schemas"]["W06Data"];
        "multipart/form-data": components["schemas"]["W06Data"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W06Data"];
        };
      };
    };
  };
  /** @description API endpoint that allows W06 bulletin Data to be viewed or edited */
  w06_data_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w06 data. */
        id_w06_data: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W06Data"];
        };
      };
    };
  };
  /** @description API endpoint that allows W06 bulletin Data to be viewed or edited */
  w06_data_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w06 data. */
        id_w06_data: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W06Data"];
        "application/x-www-form-urlencoded": components["schemas"]["W06Data"];
        "multipart/form-data": components["schemas"]["W06Data"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W06Data"];
        };
      };
    };
  };
  /** @description API endpoint that allows W06 bulletin Data to be viewed or edited */
  w06_data_destroy: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w06 data. */
        id_w06_data: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W06 bulletin Data to be viewed or edited */
  w06_data_partial_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w06 data. */
        id_w06_data: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW06Data"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW06Data"];
        "multipart/form-data": components["schemas"]["PatchedW06Data"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W06Data"];
        };
      };
    };
  };
  /** @description API endpoint that allows W07 bulletins to be viewed or edited */
  w07_bulletins_list: {
    parameters: {
      query?: {
        /** @description A page number within the paginated result set. */
        page?: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["PaginatedW07List"];
        };
      };
    };
  };
  /** @description API endpoint that allows W07 bulletins to be viewed or edited */
  w07_bulletins_create: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["W07"];
        "application/x-www-form-urlencoded": components["schemas"]["W07"];
        "multipart/form-data": components["schemas"]["W07"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W07"];
        };
      };
    };
  };
  /** @description API endpoint that allows W07 bulletins to be viewed or edited */
  w07_bulletins_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w07. */
        id_w07: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W07"];
        };
      };
    };
  };
  /** @description API endpoint that allows W07 bulletins to be viewed or edited */
  w07_bulletins_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w07. */
        id_w07: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W07"];
        "application/x-www-form-urlencoded": components["schemas"]["W07"];
        "multipart/form-data": components["schemas"]["W07"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W07"];
        };
      };
    };
  };
  /** @description API endpoint that allows W07 bulletins to be viewed or edited */
  w07_bulletins_destroy: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w07. */
        id_w07: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W07 bulletins to be viewed or edited */
  w07_bulletins_partial_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w07. */
        id_w07: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW07"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW07"];
        "multipart/form-data": components["schemas"]["PatchedW07"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W07"];
        };
      };
    };
  };
  /** @description API endpoint that allows W07 bulletins to be viewed or edited */
  w07_bulletins_reopen_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w07. */
        id_w07: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W07"];
        };
      };
    };
  };
  /** @description API endpoint that allows W07 bulletins to be viewed or edited */
  w07_bulletins_send_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w07. */
        id_w07: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W07"];
        };
      };
    };
  };
  /** @description API endpoint that allows W07 bulletins to be viewed or edited */
  w07_bulletins_bulk_update_create: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["W07"];
        "application/x-www-form-urlencoded": components["schemas"]["W07"];
        "multipart/form-data": components["schemas"]["W07"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W07"];
        };
      };
    };
  };
  /** @description API endpoint that allows W07 bulletins to be viewed or edited */
  w07_bulletins_new_retrieve: {
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W07"];
        };
      };
    };
  };
  /** @description API endpoint that allows w07 bulletin Data to be viewed or edited */
  w07_data_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W07Data"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows w07 bulletin Data to be viewed or edited */
  w07_data_create: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["W07Data"];
        "application/x-www-form-urlencoded": components["schemas"]["W07Data"];
        "multipart/form-data": components["schemas"]["W07Data"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W07Data"];
        };
      };
    };
  };
  /** @description API endpoint that allows w07 bulletin Data to be viewed or edited */
  w07_data_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w07 data. */
        id_w07_data: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W07Data"];
        };
      };
    };
  };
  /** @description API endpoint that allows w07 bulletin Data to be viewed or edited */
  w07_data_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w07 data. */
        id_w07_data: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W07Data"];
        "application/x-www-form-urlencoded": components["schemas"]["W07Data"];
        "multipart/form-data": components["schemas"]["W07Data"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W07Data"];
        };
      };
    };
  };
  /** @description API endpoint that allows w07 bulletin Data to be viewed or edited */
  w07_data_destroy: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w07 data. */
        id_w07_data: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows w07 bulletin Data to be viewed or edited */
  w07_data_partial_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w07 data. */
        id_w07_data: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW07Data"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW07Data"];
        "multipart/form-data": components["schemas"]["PatchedW07Data"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W07Data"];
        };
      };
    };
  };
  /** @description API endpoint that allows W12 bulletins to be viewed or edited */
  w12_bulletins_list: {
    parameters: {
      query?: {
        /** @description A page number within the paginated result set. */
        page?: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["PaginatedW12List"];
        };
      };
    };
  };
  /** @description API endpoint that allows W12 bulletins to be viewed or edited */
  w12_bulletins_create: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["W12"];
        "application/x-www-form-urlencoded": components["schemas"]["W12"];
        "multipart/form-data": components["schemas"]["W12"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W12"];
        };
      };
    };
  };
  /** @description API endpoint that allows W12 bulletins to be viewed or edited */
  w12_bulletins_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w12. */
        id_w12: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W12"];
        };
      };
    };
  };
  /** @description API endpoint that allows W12 bulletins to be viewed or edited */
  w12_bulletins_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w12. */
        id_w12: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W12"];
        "application/x-www-form-urlencoded": components["schemas"]["W12"];
        "multipart/form-data": components["schemas"]["W12"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W12"];
        };
      };
    };
  };
  /** @description API endpoint that allows W12 bulletins to be viewed or edited */
  w12_bulletins_destroy: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w12. */
        id_w12: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W12 bulletins to be viewed or edited */
  w12_bulletins_partial_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w12. */
        id_w12: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW12"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW12"];
        "multipart/form-data": components["schemas"]["PatchedW12"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W12"];
        };
      };
    };
  };
  /** @description API endpoint that allows W12 bulletins to be viewed or edited */
  w12_bulletins_reopen_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w12. */
        id_w12: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W12"];
        };
      };
    };
  };
  /** @description API endpoint that allows W12 bulletins to be viewed or edited */
  w12_bulletins_send_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w12. */
        id_w12: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W12"];
        };
      };
    };
  };
  /** @description API endpoint that allows W12 bulletins to be viewed or edited */
  w12_bulletins_bulk_update_create: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["W12"];
        "application/x-www-form-urlencoded": components["schemas"]["W12"];
        "multipart/form-data": components["schemas"]["W12"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W12"];
        };
      };
    };
  };
  /** @description API endpoint that allows W12 bulletins to be viewed or edited */
  w12_bulletins_new_retrieve: {
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W12"];
        };
      };
    };
  };
  /** @description API endpoint that allows W12 bulletin Data to be viewed or edited */
  w12_data_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W12Data"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows W12 bulletin Data to be viewed or edited */
  w12_data_create: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["W12Data"];
        "application/x-www-form-urlencoded": components["schemas"]["W12Data"];
        "multipart/form-data": components["schemas"]["W12Data"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W12Data"];
        };
      };
    };
  };
  /** @description API endpoint that allows W12 bulletin Data to be viewed or edited */
  w12_data_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w12 data. */
        id_w12_data: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W12Data"];
        };
      };
    };
  };
  /** @description API endpoint that allows W12 bulletin Data to be viewed or edited */
  w12_data_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w12 data. */
        id_w12_data: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W12Data"];
        "application/x-www-form-urlencoded": components["schemas"]["W12Data"];
        "multipart/form-data": components["schemas"]["W12Data"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W12Data"];
        };
      };
    };
  };
  /** @description API endpoint that allows W12 bulletin Data to be viewed or edited */
  w12_data_destroy: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w12 data. */
        id_w12_data: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W12 bulletin Data to be viewed or edited */
  w12_data_partial_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w12 data. */
        id_w12_data: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW12Data"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW12Data"];
        "multipart/form-data": components["schemas"]["PatchedW12Data"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W12Data"];
        };
      };
    };
  };
  /** @description API endpoint that allows W16 bulletins to be viewed or edited */
  w16_bulletins_list: {
    parameters: {
      query?: {
        /** @description A page number within the paginated result set. */
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
  /** @description API endpoint that allows W16 bulletins to be viewed or edited */
  w16_bulletins_create: {
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
  /** @description API endpoint that allows W16 bulletins to be viewed or edited */
  w16_bulletins_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w16. */
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
  /** @description API endpoint that allows W16 bulletins to be viewed or edited */
  w16_bulletins_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w16. */
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
  /** @description API endpoint that allows W16 bulletins to be viewed or edited */
  w16_bulletins_destroy: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w16. */
        id_w16: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W16 bulletins to be viewed or edited */
  w16_bulletins_partial_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w16. */
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
  /** @description API endpoint that allows W16 bulletins to be viewed or edited */
  w16_bulletins_copy_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w16. */
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
  /** @description API endpoint that allows W16 bulletins to be viewed or edited */
  w16_bulletins_reopen_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w16. */
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
  /** @description API endpoint that allows W16 bulletins to be viewed or edited */
  w16_bulletins_send_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w16. */
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
  /** @description API endpoint that allows W16 bulletins to be viewed or edited */
  w16_bulletins_new_retrieve: {
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W16"];
        };
      };
    };
  };
  /** @description API endpoint that allows W16Conf records to be viewed */
  w16_conf_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W16Conf"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows W16Conf records to be viewed */
  w16_conf_create: {
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
  /** @description API endpoint that allows W16Conf records to be viewed */
  w16_conf_retrieve: {
    parameters: {
      path: {
        /** @description A unique value identifying this w16 conf. */
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
  /** @description API endpoint that allows W16Conf records to be viewed */
  w16_conf_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this w16 conf. */
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
  /** @description API endpoint that allows W16Conf records to be viewed */
  w16_conf_destroy: {
    parameters: {
      path: {
        /** @description A unique value identifying this w16 conf. */
        id_w16_conf: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W16Conf records to be viewed */
  w16_conf_partial_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this w16 conf. */
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
  /** @description API endpoint that allows W16 bulletin Data to be viewed or updated */
  w16_data_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W16Data"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows W16 bulletin Data to be viewed or updated */
  w16_data_create: {
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
  /** @description API endpoint that allows W16 bulletin Data to be viewed or updated */
  w16_data_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w16 data. */
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
  /** @description API endpoint that allows W16 bulletin Data to be viewed or updated */
  w16_data_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w16 data. */
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
  /** @description API endpoint that allows W16 bulletin Data to be viewed or updated */
  w16_data_destroy: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w16 data. */
        id_w16_data: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W16 bulletin Data to be viewed or updated */
  w16_data_partial_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w16 data. */
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
  /** @description API endpoint that allows W16 bulletin Data to be viewed or updated */
  w16_data_bulk_update_create: {
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
  /** @description API endpoint that allows OzonoLivelli records to be viewed */
  w16_levels_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["OzonoLivelli"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows OzonoLivelli records to be viewed */
  w16_levels_create: {
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
  /** @description API endpoint that allows OzonoLivelli records to be viewed */
  w16_levels_retrieve: {
    parameters: {
      path: {
        /** @description A unique value identifying this ozono livelli. */
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
  /** @description API endpoint that allows OzonoLivelli records to be viewed */
  w16_levels_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this ozono livelli. */
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
  /** @description API endpoint that allows OzonoLivelli records to be viewed */
  w16_levels_destroy: {
    parameters: {
      path: {
        /** @description A unique value identifying this ozono livelli. */
        id_ozono_livelli: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows OzonoLivelli records to be viewed */
  w16_levels_partial_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this ozono livelli. */
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
  /** @description API endpoint that allows W17 bulletins to be viewed or edited */
  w17_bulletins_list: {
    parameters: {
      query?: {
        /** @description A page number within the paginated result set. */
        page?: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["PaginatedW17List"];
        };
      };
    };
  };
  /** @description API endpoint that allows W17 bulletins to be viewed or edited */
  w17_bulletins_create: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["W17"];
        "application/x-www-form-urlencoded": components["schemas"]["W17"];
        "multipart/form-data": components["schemas"]["W17"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W17"];
        };
      };
    };
  };
  /** @description API endpoint that allows W17 bulletins to be viewed or edited */
  w17_bulletins_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w17. */
        id_w17: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W17"];
        };
      };
    };
  };
  /** @description API endpoint that allows W17 bulletins to be viewed or edited */
  w17_bulletins_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w17. */
        id_w17: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W17"];
        "application/x-www-form-urlencoded": components["schemas"]["W17"];
        "multipart/form-data": components["schemas"]["W17"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W17"];
        };
      };
    };
  };
  /** @description API endpoint that allows W17 bulletins to be viewed or edited */
  w17_bulletins_destroy: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w17. */
        id_w17: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W17 bulletins to be viewed or edited */
  w17_bulletins_partial_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w17. */
        id_w17: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW17"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW17"];
        "multipart/form-data": components["schemas"]["PatchedW17"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W17"];
        };
      };
    };
  };
  /** @description API endpoint that allows W17 bulletins to be viewed or edited */
  w17_bulletins_copy_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w17. */
        id_w17: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W17"];
        };
      };
    };
  };
  /** @description API endpoint that allows W17 bulletins to be viewed or edited */
  w17_bulletins_reopen_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w17. */
        id_w17: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W17"];
        };
      };
    };
  };
  /** @description API endpoint that allows W17 bulletins to be viewed or edited */
  w17_bulletins_send_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w17. */
        id_w17: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W17"];
        };
      };
    };
  };
  /** @description API endpoint that allows W17 bulletins to be viewed or edited */
  w17_bulletins_bulk_update_create: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["W17"];
        "application/x-www-form-urlencoded": components["schemas"]["W17"];
        "multipart/form-data": components["schemas"]["W17"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W17"];
        };
      };
    };
  };
  /** @description API endpoint that allows W17 bulletins to be viewed or edited */
  w17_bulletins_new_retrieve: {
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W17"];
        };
      };
    };
  };
  w17_bulletins_full_list: {
    parameters: {
      query?: {
        data?: string;
        /** @description A page number within the paginated result set. */
        page?: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["PaginatedW17SerializerFullList"];
        };
      };
    };
  };
  w17_bulletins_full_create: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["W17SerializerFull"];
        "application/x-www-form-urlencoded": components["schemas"]["W17SerializerFull"];
        "multipart/form-data": components["schemas"]["W17SerializerFull"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W17SerializerFull"];
        };
      };
    };
  };
  w17_bulletins_full_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w17. */
        id_w17: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W17SerializerFull"];
        };
      };
    };
  };
  w17_bulletins_full_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w17. */
        id_w17: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W17SerializerFull"];
        "application/x-www-form-urlencoded": components["schemas"]["W17SerializerFull"];
        "multipart/form-data": components["schemas"]["W17SerializerFull"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W17SerializerFull"];
        };
      };
    };
  };
  w17_bulletins_full_destroy: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w17. */
        id_w17: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  w17_bulletins_full_partial_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w17. */
        id_w17: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW17SerializerFull"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW17SerializerFull"];
        "multipart/form-data": components["schemas"]["PatchedW17SerializerFull"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W17SerializerFull"];
        };
      };
    };
  };
  /** @description API endpoint that allows W17 classes to be viewed */
  w17_classes_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W17Classes"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows W17 classes to be viewed */
  w17_classes_create: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["W17Classes"];
        "application/x-www-form-urlencoded": components["schemas"]["W17Classes"];
        "multipart/form-data": components["schemas"]["W17Classes"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W17Classes"];
        };
      };
    };
  };
  /** @description API endpoint that allows W17 classes to be viewed */
  w17_classes_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w17 classes. */
        id_w17_classes: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W17Classes"];
        };
      };
    };
  };
  /** @description API endpoint that allows W17 classes to be viewed */
  w17_classes_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w17 classes. */
        id_w17_classes: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W17Classes"];
        "application/x-www-form-urlencoded": components["schemas"]["W17Classes"];
        "multipart/form-data": components["schemas"]["W17Classes"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W17Classes"];
        };
      };
    };
  };
  /** @description API endpoint that allows W17 classes to be viewed */
  w17_classes_destroy: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w17 classes. */
        id_w17_classes: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W17 classes to be viewed */
  w17_classes_partial_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w17 classes. */
        id_w17_classes: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW17Classes"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW17Classes"];
        "multipart/form-data": components["schemas"]["PatchedW17Classes"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W17Classes"];
        };
      };
    };
  };
  /** @description API endpoint that allows W17 bulletin Data to be viewed or edited */
  w17_data_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W17Data"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows W17 bulletin Data to be viewed or edited */
  w17_data_create: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["W17Data"];
        "application/x-www-form-urlencoded": components["schemas"]["W17Data"];
        "multipart/form-data": components["schemas"]["W17Data"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W17Data"];
        };
      };
    };
  };
  /** @description API endpoint that allows W17 bulletin Data to be viewed or edited */
  w17_data_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w17 data. */
        id_w17_data: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W17Data"];
        };
      };
    };
  };
  /** @description API endpoint that allows W17 bulletin Data to be viewed or edited */
  w17_data_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w17 data. */
        id_w17_data: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W17Data"];
        "application/x-www-form-urlencoded": components["schemas"]["W17Data"];
        "multipart/form-data": components["schemas"]["W17Data"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W17Data"];
        };
      };
    };
  };
  /** @description API endpoint that allows W17 bulletin Data to be viewed or edited */
  w17_data_destroy: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w17 data. */
        id_w17_data: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W17 bulletin Data to be viewed or edited */
  w17_data_partial_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w17 data. */
        id_w17_data: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW17Data"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW17Data"];
        "multipart/form-data": components["schemas"]["PatchedW17Data"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W17Data"];
        };
      };
    };
  };
  /** @description API endpoint that allows stations to be viewed */
  w17_stazioni_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["StazioneMisura"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows stations to be viewed */
  w17_stazioni_create: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["StazioneMisura"];
        "application/x-www-form-urlencoded": components["schemas"]["StazioneMisura"];
        "multipart/form-data": components["schemas"]["StazioneMisura"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["StazioneMisura"];
        };
      };
    };
  };
  /** @description API endpoint that allows stations to be viewed */
  w17_stazioni_retrieve: {
    parameters: {
      path: {
        /** @description A unique value identifying this stazione misura. */
        codice_istat_comune: string;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["StazioneMisura"];
        };
      };
    };
  };
  /** @description API endpoint that allows stations to be viewed */
  w17_stazioni_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this stazione misura. */
        codice_istat_comune: string;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["StazioneMisura"];
        "application/x-www-form-urlencoded": components["schemas"]["StazioneMisura"];
        "multipart/form-data": components["schemas"]["StazioneMisura"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["StazioneMisura"];
        };
      };
    };
  };
  /** @description API endpoint that allows stations to be viewed */
  w17_stazioni_destroy: {
    parameters: {
      path: {
        /** @description A unique value identifying this stazione misura. */
        codice_istat_comune: string;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows stations to be viewed */
  w17_stazioni_partial_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this stazione misura. */
        codice_istat_comune: string;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedStazioneMisura"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedStazioneMisura"];
        "multipart/form-data": components["schemas"]["PatchedStazioneMisura"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["StazioneMisura"];
        };
      };
    };
  };
  /** @description API endpoint that allows trends to be viewed */
  w17_trend_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["Trend"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows trends to be viewed */
  w17_trend_create: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["Trend"];
        "application/x-www-form-urlencoded": components["schemas"]["Trend"];
        "multipart/form-data": components["schemas"]["Trend"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["Trend"];
        };
      };
    };
  };
  /** @description API endpoint that allows trends to be viewed */
  w17_trend_retrieve: {
    parameters: {
      path: {
        /** @description A unique value identifying this trend. */
        id_trend: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["Trend"];
        };
      };
    };
  };
  /** @description API endpoint that allows trends to be viewed */
  w17_trend_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this trend. */
        id_trend: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["Trend"];
        "application/x-www-form-urlencoded": components["schemas"]["Trend"];
        "multipart/form-data": components["schemas"]["Trend"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["Trend"];
        };
      };
    };
  };
  /** @description API endpoint that allows trends to be viewed */
  w17_trend_destroy: {
    parameters: {
      path: {
        /** @description A unique value identifying this trend. */
        id_trend: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows trends to be viewed */
  w17_trend_partial_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this trend. */
        id_trend: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedTrend"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedTrend"];
        "multipart/form-data": components["schemas"]["PatchedTrend"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["Trend"];
        };
      };
    };
  };
  /** @description API endpoint that allows W31 bulletins to be viewed or edited */
  w17verifica_bulletins_list: {
    parameters: {
      query?: {
        /** @description A page number within the paginated result set. */
        page?: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["PaginatedW17verificaList"];
        };
      };
    };
  };
  /** @description API endpoint that allows W31 bulletins to be viewed or edited */
  w17verifica_bulletins_create: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["W17verifica"];
        "application/x-www-form-urlencoded": components["schemas"]["W17verifica"];
        "multipart/form-data": components["schemas"]["W17verifica"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W17verifica"];
        };
      };
    };
  };
  /** @description API endpoint that allows W31 bulletins to be viewed or edited */
  w17verifica_bulletins_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w17_verifica. */
        id_w17verifica: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W17verifica"];
        };
      };
    };
  };
  /** @description API endpoint that allows W31 bulletins to be viewed or edited */
  w17verifica_bulletins_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w17_verifica. */
        id_w17verifica: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W17verifica"];
        "application/x-www-form-urlencoded": components["schemas"]["W17verifica"];
        "multipart/form-data": components["schemas"]["W17verifica"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W17verifica"];
        };
      };
    };
  };
  /** @description API endpoint that allows W31 bulletins to be viewed or edited */
  w17verifica_bulletins_destroy: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w17_verifica. */
        id_w17verifica: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W31 bulletins to be viewed or edited */
  w17verifica_bulletins_partial_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w17_verifica. */
        id_w17verifica: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW17verifica"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW17verifica"];
        "multipart/form-data": components["schemas"]["PatchedW17verifica"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W17verifica"];
        };
      };
    };
  };
  /** @description API endpoint that allows W31 bulletins to be viewed or edited */
  w17verifica_bulletins_copy_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w17_verifica. */
        id_w17verifica: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W17verifica"];
        };
      };
    };
  };
  /** @description API endpoint that allows W31 bulletins to be viewed or edited */
  w17verifica_bulletins_reopen_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w17_verifica. */
        id_w17verifica: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W17verifica"];
        };
      };
    };
  };
  /** @description API endpoint that allows W31 bulletins to be viewed or edited */
  w17verifica_bulletins_send_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w17_verifica. */
        id_w17verifica: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W17verifica"];
        };
      };
    };
  };
  /** @description API endpoint that allows W31 bulletins to be viewed or edited */
  w17verifica_bulletins_bulk_update_create: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["W17verifica"];
        "application/x-www-form-urlencoded": components["schemas"]["W17verifica"];
        "multipart/form-data": components["schemas"]["W17verifica"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W17verifica"];
        };
      };
    };
  };
  /** @description API endpoint that allows W31 bulletins to be viewed or edited */
  w17verifica_bulletins_new_retrieve: {
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W17verifica"];
        };
      };
    };
  };
  /** @description API endpoint that allows W17verifica bulletin Data to be viewed or edited */
  w17verifica_data_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W17verificaData"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows W17verifica bulletin Data to be viewed or edited */
  w17verifica_data_create: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["W17verificaData"];
        "application/x-www-form-urlencoded": components["schemas"]["W17verificaData"];
        "multipart/form-data": components["schemas"]["W17verificaData"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W17verificaData"];
        };
      };
    };
  };
  /** @description API endpoint that allows W17verifica bulletin Data to be viewed or edited */
  w17verifica_data_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w17_verifica_data. */
        id_w17_verifica_data: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W17verificaData"];
        };
      };
    };
  };
  /** @description API endpoint that allows W17verifica bulletin Data to be viewed or edited */
  w17verifica_data_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w17_verifica_data. */
        id_w17_verifica_data: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W17verificaData"];
        "application/x-www-form-urlencoded": components["schemas"]["W17verificaData"];
        "multipart/form-data": components["schemas"]["W17verificaData"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W17verificaData"];
        };
      };
    };
  };
  /** @description API endpoint that allows W17verifica bulletin Data to be viewed or edited */
  w17verifica_data_destroy: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w17_verifica_data. */
        id_w17_verifica_data: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W17verifica bulletin Data to be viewed or edited */
  w17verifica_data_partial_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w17_verifica_data. */
        id_w17_verifica_data: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW17verificaData"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW17verificaData"];
        "multipart/form-data": components["schemas"]["PatchedW17verificaData"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W17verificaData"];
        };
      };
    };
  };
  /** @description API endpoint that allows W17verificaMassimali bulletin Data to be viewed or edited */
  w17verifica_massimali_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W17verificaMassimali"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows W17verificaMassimali bulletin Data to be viewed or edited */
  w17verifica_massimali_create: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["W17verificaMassimali"];
        "application/x-www-form-urlencoded": components["schemas"]["W17verificaMassimali"];
        "multipart/form-data": components["schemas"]["W17verificaMassimali"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W17verificaMassimali"];
        };
      };
    };
  };
  /** @description API endpoint that allows W17verificaMassimali bulletin Data to be viewed or edited */
  w17verifica_massimali_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w17_verifica_massimali. */
        id_w17_verifica_massimali: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W17verificaMassimali"];
        };
      };
    };
  };
  /** @description API endpoint that allows W17verificaMassimali bulletin Data to be viewed or edited */
  w17verifica_massimali_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w17_verifica_massimali. */
        id_w17_verifica_massimali: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W17verificaMassimali"];
        "application/x-www-form-urlencoded": components["schemas"]["W17verificaMassimali"];
        "multipart/form-data": components["schemas"]["W17verificaMassimali"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W17verificaMassimali"];
        };
      };
    };
  };
  /** @description API endpoint that allows W17verificaMassimali bulletin Data to be viewed or edited */
  w17verifica_massimali_destroy: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w17_verifica_massimali. */
        id_w17_verifica_massimali: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W17verificaMassimali bulletin Data to be viewed or edited */
  w17verifica_massimali_partial_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w17_verifica_massimali. */
        id_w17_verifica_massimali: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW17verificaMassimali"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW17verificaMassimali"];
        "multipart/form-data": components["schemas"]["PatchedW17verificaMassimali"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W17verificaMassimali"];
        };
      };
    };
  };
  /** @description API endpoint that allows W22 bulletins to be viewed or edited */
  w22_bulletins_list: {
    parameters: {
      query?: {
        /** @description A page number within the paginated result set. */
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
  /** @description API endpoint that allows W22 bulletins to be viewed or edited */
  w22_bulletins_create: {
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
  /** @description API endpoint that allows W22 bulletins to be viewed or edited */
  w22_bulletins_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w22. */
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
  /** @description API endpoint that allows W22 bulletins to be viewed or edited */
  w22_bulletins_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w22. */
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
  /** @description API endpoint that allows W22 bulletins to be viewed or edited */
  w22_bulletins_destroy: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w22. */
        id_w22: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W22 bulletins to be viewed or edited */
  w22_bulletins_partial_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w22. */
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
  /** @description API endpoint that allows W22 bulletins to be viewed or edited */
  w22_bulletins_send_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w22. */
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
  /** @description API endpoint that allows W22 bulletins to be viewed or edited */
  w22_bulletins_bulk_update_create: {
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
  /** @description API endpoint that allows W22 bulletins to be viewed or edited */
  w22_bulletins_new_retrieve: {
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W22"];
        };
      };
    };
  };
  /** @description API endpoint that allows W22 bulletin Criticità to be viewed */
  w22_criticita_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W22Criticita"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows W22 bulletin Criticità to be viewed */
  w22_criticita_create: {
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
  /** @description API endpoint that allows W22 bulletin Criticità to be viewed */
  w22_criticita_retrieve: {
    parameters: {
      path: {
        /** @description A unique value identifying this w22 criticita. */
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
  /** @description API endpoint that allows W22 bulletin Criticità to be viewed */
  w22_criticita_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this w22 criticita. */
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
  /** @description API endpoint that allows W22 bulletin Criticità to be viewed */
  w22_criticita_destroy: {
    parameters: {
      path: {
        /** @description A unique value identifying this w22 criticita. */
        id_w22_criticita: string;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W22 bulletin Criticità to be viewed */
  w22_criticita_partial_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this w22 criticita. */
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
  /** @description API endpoint that allows W22 bulletin Data to be viewed or edited */
  w22_data_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W22Data"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows W22 bulletin Data to be viewed or edited */
  w22_data_create: {
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
  /** @description API endpoint that allows W22 bulletin Data to be viewed or edited */
  w22_data_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w22 data. */
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
  /** @description API endpoint that allows W22 bulletin Data to be viewed or edited */
  w22_data_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w22 data. */
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
  /** @description API endpoint that allows W22 bulletin Data to be viewed or edited */
  w22_data_destroy: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w22 data. */
        id_w22_data: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W22 bulletin Data to be viewed or edited */
  w22_data_partial_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w22 data. */
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
  /** @description API endpoint that allows W22 bulletin Tendenza to be viewed */
  w22_tendenza_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W22Tendenza"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows W22 bulletin Tendenza to be viewed */
  w22_tendenza_create: {
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
  /** @description API endpoint that allows W22 bulletin Tendenza to be viewed */
  w22_tendenza_retrieve: {
    parameters: {
      path: {
        /** @description A unique value identifying this w22 tendenza. */
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
  /** @description API endpoint that allows W22 bulletin Tendenza to be viewed */
  w22_tendenza_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this w22 tendenza. */
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
  /** @description API endpoint that allows W22 bulletin Tendenza to be viewed */
  w22_tendenza_destroy: {
    parameters: {
      path: {
        /** @description A unique value identifying this w22 tendenza. */
        id_w22_tendenza: string;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W22 bulletin Tendenza to be viewed */
  w22_tendenza_partial_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this w22 tendenza. */
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
  /** @description API endpoint that allows W22 bulletin Zone to be viewed or edited */
  w22_zone_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W22Zone"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows W22 bulletin Zone to be viewed or edited */
  w22_zone_create: {
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
  /** @description API endpoint that allows W22 bulletin Zone to be viewed or edited */
  w22_zone_retrieve: {
    parameters: {
      path: {
        /** @description A unique value identifying this w22 zone. */
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
  /** @description API endpoint that allows W22 bulletin Zone to be viewed or edited */
  w22_zone_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this w22 zone. */
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
  /** @description API endpoint that allows W22 bulletin Zone to be viewed or edited */
  w22_zone_destroy: {
    parameters: {
      path: {
        /** @description A unique value identifying this w22 zone. */
        id_w22_zone: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W22 bulletin Zone to be viewed or edited */
  w22_zone_partial_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this w22 zone. */
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
  /** @description API endpoint that allows W22 bulletins to be viewed or edited */
  w22verifica_bulletins_list: {
    parameters: {
      query?: {
        /** @description A page number within the paginated result set. */
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
  /** @description API endpoint that allows W22 bulletins to be viewed or edited */
  w22verifica_bulletins_create: {
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
  /** @description API endpoint that allows W22 bulletins to be viewed or edited */
  w22verifica_bulletins_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w22 verifica. */
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
  /** @description API endpoint that allows W22 bulletins to be viewed or edited */
  w22verifica_bulletins_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w22 verifica. */
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
  /** @description API endpoint that allows W22 bulletins to be viewed or edited */
  w22verifica_bulletins_destroy: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w22 verifica. */
        id_w22verifica: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W22 bulletins to be viewed or edited */
  w22verifica_bulletins_partial_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w22 verifica. */
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
  /** @description API endpoint that allows W22 bulletins to be viewed or edited */
  w22verifica_bulletins_send_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w22 verifica. */
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
  /** @description API endpoint that allows W22 bulletins to be viewed or edited */
  w22verifica_bulletins_bulk_update_create: {
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
  /** @description API endpoint that allows W22 bulletins to be viewed or edited */
  w22verifica_bulletins_new_retrieve: {
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
  /** @description API endpoint that allows W22 bulletin Data to be viewed or edited */
  w22verifica_data_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W22VerificaData"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows W22 bulletin Data to be viewed or edited */
  w22verifica_data_create: {
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
  /** @description API endpoint that allows W22 bulletin Data to be viewed or edited */
  w22verifica_data_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w22 verifica data. */
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
  /** @description API endpoint that allows W22 bulletin Data to be viewed or edited */
  w22verifica_data_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w22 verifica data. */
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
  /** @description API endpoint that allows W22 bulletin Data to be viewed or edited */
  w22verifica_data_destroy: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w22 verifica data. */
        id_w22verifica_data: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W22 bulletin Data to be viewed or edited */
  w22verifica_data_partial_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w22 verifica data. */
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
  /** @description API endpoint that allows W22 bulletin Tendenza to be viewed */
  w22verifica_giudizio_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W22Giudizio"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows W22 bulletin Tendenza to be viewed */
  w22verifica_giudizio_create: {
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
  /** @description API endpoint that allows W22 bulletin Tendenza to be viewed */
  w22verifica_giudizio_retrieve: {
    parameters: {
      path: {
        /** @description A unique value identifying this w22 giudizio. */
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
  /** @description API endpoint that allows W22 bulletin Tendenza to be viewed */
  w22verifica_giudizio_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this w22 giudizio. */
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
  /** @description API endpoint that allows W22 bulletin Tendenza to be viewed */
  w22verifica_giudizio_destroy: {
    parameters: {
      path: {
        /** @description A unique value identifying this w22 giudizio. */
        id_w22giudizio: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W22 bulletin Tendenza to be viewed */
  w22verifica_giudizio_partial_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this w22 giudizio. */
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
  /** @description API endpoint that allows W22 bulletin Criticità to be viewed */
  w22verifica_severita_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W22Severita"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows W22 bulletin Criticità to be viewed */
  w22verifica_severita_create: {
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
  /** @description API endpoint that allows W22 bulletin Criticità to be viewed */
  w22verifica_severita_retrieve: {
    parameters: {
      path: {
        /** @description A unique value identifying this w22 severita. */
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
  /** @description API endpoint that allows W22 bulletin Criticità to be viewed */
  w22verifica_severita_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this w22 severita. */
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
  /** @description API endpoint that allows W22 bulletin Criticità to be viewed */
  w22verifica_severita_destroy: {
    parameters: {
      path: {
        /** @description A unique value identifying this w22 severita. */
        id_w22severita: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W22 bulletin Criticità to be viewed */
  w22verifica_severita_partial_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this w22 severita. */
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
  /** @description API endpoint that allows W22 bulletin Zone to be viewed or edited */
  w22verifica_zone_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W22Zone"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows W22 bulletin Zone to be viewed or edited */
  w22verifica_zone_create: {
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
  /** @description API endpoint that allows W22 bulletin Zone to be viewed or edited */
  w22verifica_zone_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w22 zone. */
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
  /** @description API endpoint that allows W22 bulletin Zone to be viewed or edited */
  w22verifica_zone_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w22 zone. */
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
  /** @description API endpoint that allows W22 bulletin Zone to be viewed or edited */
  w22verifica_zone_destroy: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w22 zone. */
        id_w22_zone: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W22 bulletin Zone to be viewed or edited */
  w22verifica_zone_partial_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w22 zone. */
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
  /** @description API endpoint that allows W23 bulletins to be viewed or edited */
  w23_bulletins_list: {
    parameters: {
      query?: {
        /** @description A page number within the paginated result set. */
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
  /** @description API endpoint that allows W23 bulletins to be viewed or edited */
  w23_bulletins_create: {
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
  /** @description API endpoint that allows W23 bulletins to be viewed or edited */
  w23_bulletins_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w23. */
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
  /** @description API endpoint that allows W23 bulletins to be viewed or edited */
  w23_bulletins_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w23. */
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
  /** @description API endpoint that allows W23 bulletins to be viewed or edited */
  w23_bulletins_destroy: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w23. */
        id_w23: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W23 bulletins to be viewed or edited */
  w23_bulletins_partial_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w23. */
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
  /** @description API endpoint that allows W23 bulletins to be viewed or edited */
  w23_bulletins_reopen_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w23. */
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
  /** @description API endpoint that allows W23 bulletins to be viewed or edited */
  w23_bulletins_send_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w23. */
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
  /** @description API endpoint that allows W23 bulletins to be viewed or edited */
  w23_bulletins_bulk_update_create: {
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
  /** @description API endpoint that allows W23 bulletins to be viewed or edited */
  w23_bulletins_new_retrieve: {
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W23"];
        };
      };
    };
  };
  /** @description View the latest W23 bulletin sent for a certain day */
  w23_current_retrieve: {
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
  /** @description API endpoint that allows W23 bulletin Data to be viewed or edited */
  w23_data_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W23Data"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows W23 bulletin Data to be viewed or edited */
  w23_data_create: {
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
  /** @description API endpoint that allows W23 bulletin Data to be viewed or edited */
  w23_data_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w23 data. */
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
  /** @description API endpoint that allows W23 bulletin Data to be viewed or edited */
  w23_data_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w23 data. */
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
  /** @description API endpoint that allows W23 bulletin Data to be viewed or edited */
  w23_data_destroy: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w23 data. */
        id_w23_data: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W23 bulletin Data to be viewed or edited */
  w23_data_partial_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w23 data. */
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
  /** @description API endpoint that allows W23 bulletin Effetti sul territorio to be viewed */
  w23_effetti_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W23Effettiterritorio"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows W23 bulletin Effetti sul territorio to be viewed */
  w23_effetti_create: {
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
  /** @description API endpoint that allows W23 bulletin Effetti sul territorio to be viewed */
  w23_effetti_retrieve: {
    parameters: {
      path: {
        /** @description A unique value identifying this w23 effettiterritorio. */
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
  /** @description API endpoint that allows W23 bulletin Effetti sul territorio to be viewed */
  w23_effetti_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this w23 effettiterritorio. */
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
  /** @description API endpoint that allows W23 bulletin Effetti sul territorio to be viewed */
  w23_effetti_destroy: {
    parameters: {
      path: {
        /** @description A unique value identifying this w23 effettiterritorio. */
        id_w23_effettiterritorio: string;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W23 bulletin Effetti sul territorio to be viewed */
  w23_effetti_partial_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this w23 effettiterritorio. */
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
  /** @description API endpoint that allows W23 bulletin Pericolo to be viewed */
  w23_pericoli_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W23Pericolo"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows W23 bulletin Pericolo to be viewed */
  w23_pericoli_create: {
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
  /** @description API endpoint that allows W23 bulletin Pericolo to be viewed */
  w23_pericoli_retrieve: {
    parameters: {
      path: {
        /** @description A unique value identifying this w23 pericolo. */
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
  /** @description API endpoint that allows W23 bulletin Pericolo to be viewed */
  w23_pericoli_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this w23 pericolo. */
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
  /** @description API endpoint that allows W23 bulletin Pericolo to be viewed */
  w23_pericoli_destroy: {
    parameters: {
      path: {
        /** @description A unique value identifying this w23 pericolo. */
        id_w23_pericolo: string;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W23 bulletin Pericolo to be viewed */
  w23_pericoli_partial_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this w23 pericolo. */
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
    parameters: {
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
      path: {
        /** @description A unique integer value identifying this w23 pluvossh6. */
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
      path: {
        /** @description A unique integer value identifying this w23 pluvossh6. */
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
      path: {
        /** @description A unique integer value identifying this w23 pluvossh6. */
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
      path: {
        /** @description A unique integer value identifying this w23 pluvossh6. */
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
      path: {
        /** @description A unique value identifying this soglie nivo area prev. */
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
      path: {
        /** @description A unique value identifying this soglie nivo area prev. */
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
      path: {
        /** @description A unique value identifying this soglie nivo area prev. */
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
      path: {
        /** @description A unique value identifying this soglie nivo area prev. */
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
      path: {
        /** @description A unique value identifying this soglie pluv area prev massimi. */
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
      path: {
        /** @description A unique value identifying this soglie pluv area prev massimi. */
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
      path: {
        /** @description A unique value identifying this soglie pluv area prev massimi. */
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
      path: {
        /** @description A unique value identifying this soglie pluv area prev massimi. */
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
      path: {
        /** @description A unique value identifying this soglie pluv area prev medie. */
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
      path: {
        /** @description A unique value identifying this soglie pluv area prev medie. */
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
      path: {
        /** @description A unique value identifying this soglie pluv area prev medie. */
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
      path: {
        /** @description A unique value identifying this soglie pluv area prev medie. */
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
      path: {
        /** @description A unique value identifying this time layouts. */
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
      path: {
        /** @description A unique value identifying this time layouts. */
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
      path: {
        /** @description A unique value identifying this time layouts. */
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
      path: {
        /** @description A unique value identifying this time layouts. */
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
  /** @description API endpoint that allows W23 bulletin Zone to be viewed */
  w23_zone_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W23Zone"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows W23 bulletin Zone to be viewed */
  w23_zone_create: {
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
  /** @description API endpoint that allows W23 bulletin Zone to be viewed */
  w23_zone_retrieve: {
    parameters: {
      path: {
        /** @description A unique value identifying this w23 zone. */
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
  /** @description API endpoint that allows W23 bulletin Zone to be viewed */
  w23_zone_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this w23 zone. */
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
  /** @description API endpoint that allows W23 bulletin Zone to be viewed */
  w23_zone_destroy: {
    parameters: {
      path: {
        /** @description A unique value identifying this w23 zone. */
        id_w23_zone: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W23 bulletin Zone to be viewed */
  w23_zone_partial_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this w23 zone. */
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
  /** @description API endpoint that allows W24 bulletins to be viewed or edited */
  w24_bulletins_list: {
    parameters: {
      query?: {
        /** @description A page number within the paginated result set. */
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
  /** @description API endpoint that allows W24 bulletins to be viewed or edited */
  w24_bulletins_create: {
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
  /** @description API endpoint that allows W24 bulletins to be viewed or edited */
  w24_bulletins_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w24. */
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
  /** @description API endpoint that allows W24 bulletins to be viewed or edited */
  w24_bulletins_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w24. */
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
  /** @description API endpoint that allows W24 bulletins to be viewed or edited */
  w24_bulletins_destroy: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w24. */
        id_w24: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W24 bulletins to be viewed or edited */
  w24_bulletins_partial_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w24. */
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
  /** @description API endpoint that allows W24 bulletins to be viewed or edited */
  w24_bulletins_reopen_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w24. */
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
  /** @description API endpoint that allows W24 bulletins to be viewed or edited */
  w24_bulletins_send_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w24. */
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
  /** @description API endpoint that allows W24 bulletins to be viewed or edited */
  w24_bulletins_bulk_update_create: {
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
  /** @description API endpoint that allows W24 bulletins to be viewed or edited */
  w24_bulletins_new_retrieve: {
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W24"];
        };
      };
    };
  };
  /** @description View the latest W24 bulletin sent for a certain day */
  w24_current_retrieve: {
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
  /** @description API endpoint that allows W24 bulletin Data to be viewed or edited */
  w24_data_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W24Data"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows W24 bulletin Data to be viewed or edited */
  w24_data_create: {
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
  /** @description API endpoint that allows W24 bulletin Data to be viewed or edited */
  w24_data_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w24 data. */
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
  /** @description API endpoint that allows W24 bulletin Data to be viewed or edited */
  w24_data_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w24 data. */
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
  /** @description API endpoint that allows W24 bulletin Data to be viewed or edited */
  w24_data_destroy: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w24 data. */
        id_w24_data: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W24 bulletin Data to be viewed or edited */
  w24_data_partial_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w24 data. */
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
    parameters: {
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
      path: {
        /** @description A unique integer value identifying this forecast zone. */
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
      path: {
        /** @description A unique integer value identifying this forecast zone. */
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
      path: {
        /** @description A unique integer value identifying this forecast zone. */
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
      path: {
        /** @description A unique integer value identifying this forecast zone. */
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
  /** @description API endpoint that allows W24 bulletin Data to be viewed or edited */
  w24_soglie_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W24Soglie"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows W24 bulletin Data to be viewed or edited */
  w24_soglie_create: {
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
  /** @description API endpoint that allows W24 bulletin Data to be viewed or edited */
  w24_soglie_retrieve: {
    parameters: {
      path: {
        /** @description A unique value identifying this w24 soglie. */
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
  /** @description API endpoint that allows W24 bulletin Data to be viewed or edited */
  w24_soglie_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this w24 soglie. */
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
  /** @description API endpoint that allows W24 bulletin Data to be viewed or edited */
  w24_soglie_destroy: {
    parameters: {
      path: {
        /** @description A unique value identifying this w24 soglie. */
        id_allertamento: string;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W24 bulletin Data to be viewed or edited */
  w24_soglie_partial_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this w24 soglie. */
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
  /** @description API endpoint that allows W26 bulletins to be viewed or edited */
  w26_bisbulletins_list: {
    parameters: {
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
  /** @description API endpoint that allows W26 bulletins to be viewed or edited */
  w26_bisbulletins_create: {
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
  /** @description API endpoint that allows W26 bulletins to be viewed or edited */
  w26_bisbulletins_retrieve: {
    parameters: {
      path: {
        /** @description A unique value identifying this bis bollettino webolimpia. */
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
  /** @description API endpoint that allows W26 bulletins to be viewed or edited */
  w26_bisbulletins_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this bis bollettino webolimpia. */
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
  /** @description API endpoint that allows W26 bulletins to be viewed or edited */
  w26_bisbulletins_destroy: {
    parameters: {
      path: {
        /** @description A unique value identifying this bis bollettino webolimpia. */
        codice: string;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W26 bulletins to be viewed or edited */
  w26_bisbulletins_partial_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this bis bollettino webolimpia. */
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
  /** @description API endpoint that allows W26 bulletins to be viewed or edited */
  w26_bulletins_list: {
    parameters: {
      query?: {
        data_max?: string;
        data_min?: string;
        id_w26?: number;
        /** @description A page number within the paginated result set. */
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
  /** @description API endpoint that allows W26 bulletins to be viewed or edited */
  w26_bulletins_create: {
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
  /** @description API endpoint that allows W26 bulletins to be viewed or edited */
  w26_bulletins_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w26. */
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
  /** @description API endpoint that allows W26 bulletins to be viewed or edited */
  w26_bulletins_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w26. */
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
  /** @description API endpoint that allows W26 bulletins to be viewed or edited */
  w26_bulletins_destroy: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w26. */
        id_w26: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W26 bulletins to be viewed or edited */
  w26_bulletins_partial_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w26. */
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
  /** @description API endpoint that allows W26 bulletins to be viewed or edited */
  w26_bulletins_reopen_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w26. */
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
  /** @description API endpoint that allows W26 bulletins to be viewed or edited */
  w26_bulletins_send_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w26. */
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
  /** @description API endpoint that allows W26 bulletins to be viewed or edited */
  w26_bulletins_bulk_update_create: {
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
  /** @description API endpoint that allows W26 bulletins to be viewed or edited */
  w26_bulletins_new_retrieve: {
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
  /** @description API endpoint that allows W26 bulletin Data to be viewed or edited */
  w26_data_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W26Data"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows W26 bulletin Data to be viewed or edited */
  w26_data_create: {
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
  /** @description API endpoint that allows W26 bulletin Data to be viewed or edited */
  w26_data_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w26 data. */
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
  /** @description API endpoint that allows W26 bulletin Data to be viewed or edited */
  w26_data_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w26 data. */
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
  /** @description API endpoint that allows W26 bulletin Data to be viewed or edited */
  w26_data_destroy: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w26 data. */
        id_w26_data: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W26 bulletin Data to be viewed or edited */
  w26_data_partial_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w26 data. */
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
  /** @description API endpoint that allows W26 bulletin Zone to be viewed or edited */
  w26_zone_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W26Zone"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows W26 bulletin Zone to be viewed or edited */
  w26_zone_create: {
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
  /** @description API endpoint that allows W26 bulletin Zone to be viewed or edited */
  w26_zone_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w26 zone. */
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
  /** @description API endpoint that allows W26 bulletin Zone to be viewed or edited */
  w26_zone_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w26 zone. */
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
  /** @description API endpoint that allows W26 bulletin Zone to be viewed or edited */
  w26_zone_destroy: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w26 zone. */
        id_w26_zone: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W26 bulletin Zone to be viewed or edited */
  w26_zone_partial_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w26 zone. */
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
  /** @description API endpoint that allows W28 bulletins to be viewed or edited */
  w28_bulletins_list: {
    parameters: {
      query?: {
        /** @description A page number within the paginated result set. */
        page?: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["PaginatedW28List"];
        };
      };
    };
  };
  /** @description API endpoint that allows W28 bulletins to be viewed or edited */
  w28_bulletins_create: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["W28"];
        "application/x-www-form-urlencoded": components["schemas"]["W28"];
        "multipart/form-data": components["schemas"]["W28"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W28"];
        };
      };
    };
  };
  /** @description API endpoint that allows W28 bulletins to be viewed or edited */
  w28_bulletins_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w28. */
        id_w28: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W28"];
        };
      };
    };
  };
  /** @description API endpoint that allows W28 bulletins to be viewed or edited */
  w28_bulletins_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w28. */
        id_w28: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W28"];
        "application/x-www-form-urlencoded": components["schemas"]["W28"];
        "multipart/form-data": components["schemas"]["W28"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W28"];
        };
      };
    };
  };
  /** @description API endpoint that allows W28 bulletins to be viewed or edited */
  w28_bulletins_destroy: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w28. */
        id_w28: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W28 bulletins to be viewed or edited */
  w28_bulletins_partial_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w28. */
        id_w28: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW28"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW28"];
        "multipart/form-data": components["schemas"]["PatchedW28"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W28"];
        };
      };
    };
  };
  /** @description API endpoint that allows W28 bulletins to be viewed or edited */
  w28_bulletins_reopen_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w28. */
        id_w28: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W28"];
        };
      };
    };
  };
  /** @description API endpoint that allows W28 bulletins to be viewed or edited */
  w28_bulletins_send_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w28. */
        id_w28: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W28"];
        };
      };
    };
  };
  /** @description API endpoint that allows W28 bulletins to be viewed or edited */
  w28_bulletins_bulk_update_create: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["W28"];
        "application/x-www-form-urlencoded": components["schemas"]["W28"];
        "multipart/form-data": components["schemas"]["W28"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W28"];
        };
      };
    };
  };
  /** @description API endpoint that allows W28 bulletins to be viewed or edited */
  w28_bulletins_new_retrieve: {
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W28"];
        };
      };
    };
  };
  /** @description API endpoint that allows w28 bulletin Data to be viewed or edited */
  w28_data_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W28Data"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows w28 bulletin Data to be viewed or edited */
  w28_data_create: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["W28Data"];
        "application/x-www-form-urlencoded": components["schemas"]["W28Data"];
        "multipart/form-data": components["schemas"]["W28Data"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W28Data"];
        };
      };
    };
  };
  /** @description API endpoint that allows w28 bulletin Data to be viewed or edited */
  w28_data_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w28 data. */
        id_w28_data: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W28Data"];
        };
      };
    };
  };
  /** @description API endpoint that allows w28 bulletin Data to be viewed or edited */
  w28_data_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w28 data. */
        id_w28_data: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W28Data"];
        "application/x-www-form-urlencoded": components["schemas"]["W28Data"];
        "multipart/form-data": components["schemas"]["W28Data"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W28Data"];
        };
      };
    };
  };
  /** @description API endpoint that allows w28 bulletin Data to be viewed or edited */
  w28_data_destroy: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w28 data. */
        id_w28_data: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows w28 bulletin Data to be viewed or edited */
  w28_data_partial_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w28 data. */
        id_w28_data: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW28Data"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW28Data"];
        "multipart/form-data": components["schemas"]["PatchedW28Data"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W28Data"];
        };
      };
    };
  };
  /** @description API endpoint that allows W29 bulletins to be viewed or edited */
  w29_bulletins_list: {
    parameters: {
      query?: {
        /** @description A page number within the paginated result set. */
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
  /** @description API endpoint that allows W29 bulletins to be viewed or edited */
  w29_bulletins_create: {
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
  /** @description API endpoint that allows W29 bulletins to be viewed or edited */
  w29_bulletins_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w29. */
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
  /** @description API endpoint that allows W29 bulletins to be viewed or edited */
  w29_bulletins_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w29. */
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
  /** @description API endpoint that allows W29 bulletins to be viewed or edited */
  w29_bulletins_destroy: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w29. */
        id_w29: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W29 bulletins to be viewed or edited */
  w29_bulletins_partial_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w29. */
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
  /** @description API endpoint that allows W29 bulletins to be viewed or edited */
  w29_bulletins_send_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w29. */
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
  /** @description API endpoint that allows W29 bulletins to be viewed or edited */
  w29_bulletins_bulk_update_create: {
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
  /** @description API endpoint that allows W29 bulletins to be viewed or edited */
  w29_bulletins_new_retrieve: {
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W29"];
        };
      };
    };
  };
  /** @description API endpoint that allows W29 bulletin Data to be viewed or edited */
  w29_data_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W29Data"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows W29 bulletin Data to be viewed or edited */
  w29_data_create: {
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
  /** @description API endpoint that allows W29 bulletin Data to be viewed or edited */
  w29_data_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w29 data. */
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
  /** @description API endpoint that allows W29 bulletin Data to be viewed or edited */
  w29_data_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w29 data. */
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
  /** @description API endpoint that allows W29 bulletin Data to be viewed or edited */
  w29_data_destroy: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w29 data. */
        id_w29_data: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W29 bulletin Data to be viewed or edited */
  w29_data_partial_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w29 data. */
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
  /** @description API endpoint that allows W29 bulletin Pericolo to be viewed or edited */
  w29_pericolo_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W29Pericolo"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows W29 bulletin Pericolo to be viewed or edited */
  w29_pericolo_create: {
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
  /** @description API endpoint that allows W29 bulletin Pericolo to be viewed or edited */
  w29_pericolo_retrieve: {
    parameters: {
      path: {
        /** @description A unique value identifying this w29 pericolo. */
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
  /** @description API endpoint that allows W29 bulletin Pericolo to be viewed or edited */
  w29_pericolo_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this w29 pericolo. */
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
  /** @description API endpoint that allows W29 bulletin Pericolo to be viewed or edited */
  w29_pericolo_destroy: {
    parameters: {
      path: {
        /** @description A unique value identifying this w29 pericolo. */
        id_w29_pericolo: string;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W29 bulletin Pericolo to be viewed or edited */
  w29_pericolo_partial_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this w29 pericolo. */
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
  /** @description API endpoint that allows W29 bulletin Probabilita to be viewed or edited */
  w29_probabilita_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W29Probabilita"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows W29 bulletin Probabilita to be viewed or edited */
  w29_probabilita_create: {
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
  /** @description API endpoint that allows W29 bulletin Probabilita to be viewed or edited */
  w29_probabilita_retrieve: {
    parameters: {
      path: {
        /** @description A unique value identifying this w29 probabilita. */
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
  /** @description API endpoint that allows W29 bulletin Probabilita to be viewed or edited */
  w29_probabilita_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this w29 probabilita. */
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
  /** @description API endpoint that allows W29 bulletin Probabilita to be viewed or edited */
  w29_probabilita_destroy: {
    parameters: {
      path: {
        /** @description A unique value identifying this w29 probabilita. */
        id_w29_probabilita: string;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W29 bulletin Probabilita to be viewed or edited */
  w29_probabilita_partial_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this w29 probabilita. */
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
  /** @description API endpoint that allows W29 bulletin Zone to be viewed or edited */
  w29_zone_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W29Zone"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows W29 bulletin Zone to be viewed or edited */
  w29_zone_create: {
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
  /** @description API endpoint that allows W29 bulletin Zone to be viewed or edited */
  w29_zone_retrieve: {
    parameters: {
      path: {
        /** @description A unique value identifying this w29 zone. */
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
  /** @description API endpoint that allows W29 bulletin Zone to be viewed or edited */
  w29_zone_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this w29 zone. */
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
  /** @description API endpoint that allows W29 bulletin Zone to be viewed or edited */
  w29_zone_destroy: {
    parameters: {
      path: {
        /** @description A unique value identifying this w29 zone. */
        id_w29_zone: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W29 bulletin Zone to be viewed or edited */
  w29_zone_partial_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this w29 zone. */
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
  /** @description API endpoint that allows W30 bulletins to be viewed or edited */
  w30_bulletins_list: {
    parameters: {
      query?: {
        /** @description A page number within the paginated result set. */
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
  /** @description API endpoint that allows W30 bulletins to be viewed or edited */
  w30_bulletins_create: {
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
  /** @description API endpoint that allows W30 bulletins to be viewed or edited */
  w30_bulletins_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w30. */
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
  /** @description API endpoint that allows W30 bulletins to be viewed or edited */
  w30_bulletins_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w30. */
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
  /** @description API endpoint that allows W30 bulletins to be viewed or edited */
  w30_bulletins_destroy: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w30. */
        id_w30: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W30 bulletins to be viewed or edited */
  w30_bulletins_partial_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w30. */
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
  /** @description API endpoint that allows W30 bulletins to be viewed or edited */
  w30_bulletins_reopen_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w30. */
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
  /** @description API endpoint that allows W30 bulletins to be viewed or edited */
  w30_bulletins_send_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w30. */
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
  /** @description API endpoint that allows W30 bulletins to be viewed or edited */
  w30_bulletins_new_retrieve: {
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W30"];
        };
      };
    };
  };
  /** @description View the latest W30 bulletin sent for a certain day */
  w30_current_retrieve: {
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
  /** @description View the aggregated bulletin Data for the last 4 bulletins from the supplied date backwards */
  w30_currentdata_list: {
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
  /** @description API endpoint that allows W30 bulletin Data to be viewed or edited */
  w30_data_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W30Data"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows W30 bulletin Data to be viewed or edited */
  w30_data_create: {
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
  /** @description API endpoint that allows W30 bulletin Data to be viewed or edited */
  w30_data_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w30 data. */
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
  /** @description API endpoint that allows W30 bulletin Data to be viewed or edited */
  w30_data_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w30 data. */
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
  /** @description API endpoint that allows W30 bulletin Data to be viewed or edited */
  w30_data_destroy: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w30 data. */
        id_w30_data: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W30 bulletin Data to be viewed or edited */
  w30_data_partial_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w30 data. */
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
  /** @description API endpoint that allows W30 bulletin Data to be viewed or edited */
  w30_data_bulk_update_create: {
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
  /** @description API endpoint that allows W31 bulletins to be viewed or edited */
  w31_bulletins_list: {
    parameters: {
      query?: {
        /** @description A page number within the paginated result set. */
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
  /** @description API endpoint that allows W31 bulletins to be viewed or edited */
  w31_bulletins_create: {
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
  /** @description API endpoint that allows W31 bulletins to be viewed or edited */
  w31_bulletins_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w31. */
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
  /** @description API endpoint that allows W31 bulletins to be viewed or edited */
  w31_bulletins_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w31. */
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
  /** @description API endpoint that allows W31 bulletins to be viewed or edited */
  w31_bulletins_destroy: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w31. */
        id_w31: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W31 bulletins to be viewed or edited */
  w31_bulletins_partial_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w31. */
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
  /** @description API endpoint that allows W31 bulletins to be viewed or edited */
  w31_bulletins_copy_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w31. */
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
  /** @description API endpoint that allows W31 bulletins to be viewed or edited */
  w31_bulletins_reopen_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w31. */
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
  /** @description API endpoint that allows W31 bulletins to be viewed or edited */
  w31_bulletins_send_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w31. */
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
  /** @description API endpoint that allows W31 bulletins to be viewed or edited */
  w31_bulletins_bulk_update_create: {
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
  /** @description API endpoint that allows W31 bulletins to be viewed or edited */
  w31_bulletins_new_retrieve: {
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W31"];
        };
      };
    };
  };
  /** @description View the latest W31 bulletin sent */
  w31_current_retrieve: {
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
  /** @description API endpoint that allows W31 bulletin Data to be viewed or updated */
  w31_data_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W31DataMacroareeLivelli"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows W31 bulletin Data to be viewed or updated */
  w31_data_create: {
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
  /** @description API endpoint that allows W31 bulletin Data to be viewed or updated */
  w31_data_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w31 data macroaree livelli. */
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
  /** @description API endpoint that allows W31 bulletin Data to be viewed or updated */
  w31_data_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w31 data macroaree livelli. */
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
  /** @description API endpoint that allows W31 bulletin Data to be viewed or updated */
  w31_data_destroy: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w31 data macroaree livelli. */
        id_w31_data_macroaree_livelli: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W31 bulletin Data to be viewed or updated */
  w31_data_partial_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w31 data macroaree livelli. */
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
  /** @description API endpoint that allows W31 levels to be viewed */
  w31_levels_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W31Livelli"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows W31 levels to be viewed */
  w31_levels_create: {
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
  /** @description API endpoint that allows W31 levels to be viewed */
  w31_levels_retrieve: {
    parameters: {
      path: {
        /** @description A unique value identifying this w31 livelli. */
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
  /** @description API endpoint that allows W31 levels to be viewed */
  w31_levels_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this w31 livelli. */
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
  /** @description API endpoint that allows W31 levels to be viewed */
  w31_levels_destroy: {
    parameters: {
      path: {
        /** @description A unique value identifying this w31 livelli. */
        id_w31_livelli: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W31 levels to be viewed */
  w31_levels_partial_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this w31 livelli. */
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
  /** @description API endpoint that allows W32 bulletins to be viewed or edited */
  w32_bulletins_list: {
    parameters: {
      query?: {
        /** @description A page number within the paginated result set. */
        page?: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["PaginatedW32List"];
        };
      };
    };
  };
  /** @description API endpoint that allows W32 bulletins to be viewed or edited */
  w32_bulletins_create: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["W32"];
        "application/x-www-form-urlencoded": components["schemas"]["W32"];
        "multipart/form-data": components["schemas"]["W32"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W32"];
        };
      };
    };
  };
  /** @description API endpoint that allows W32 bulletins to be viewed or edited */
  w32_bulletins_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w32. */
        id_w32: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W32"];
        };
      };
    };
  };
  /** @description API endpoint that allows W32 bulletins to be viewed or edited */
  w32_bulletins_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w32. */
        id_w32: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W32"];
        "application/x-www-form-urlencoded": components["schemas"]["W32"];
        "multipart/form-data": components["schemas"]["W32"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W32"];
        };
      };
    };
  };
  /** @description API endpoint that allows W32 bulletins to be viewed or edited */
  w32_bulletins_destroy: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w32. */
        id_w32: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W32 bulletins to be viewed or edited */
  w32_bulletins_partial_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w32. */
        id_w32: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW32"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW32"];
        "multipart/form-data": components["schemas"]["PatchedW32"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W32"];
        };
      };
    };
  };
  /** @description API endpoint that allows W32 bulletins to be viewed or edited */
  w32_bulletins_send_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w32. */
        id_w32: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W32"];
        };
      };
    };
  };
  /** @description API endpoint that allows W32 bulletins to be viewed or edited */
  w32_bulletins_bulk_update_create: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["W32"];
        "application/x-www-form-urlencoded": components["schemas"]["W32"];
        "multipart/form-data": components["schemas"]["W32"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W32"];
        };
      };
    };
  };
  /** @description API endpoint that allows W32 bulletins to be viewed or edited */
  w32_bulletins_new_retrieve: {
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W32"];
        };
      };
    };
  };
  /** @description API endpoint that allows W32 bulletin Data to be viewed or edited */
  w32_data_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W32Data"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows W32 bulletin Data to be viewed or edited */
  w32_data_create: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["W32Data"];
        "application/x-www-form-urlencoded": components["schemas"]["W32Data"];
        "multipart/form-data": components["schemas"]["W32Data"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W32Data"];
        };
      };
    };
  };
  /** @description API endpoint that allows W32 bulletin Data to be viewed or edited */
  w32_data_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w32 data. */
        id_w32_data: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W32Data"];
        };
      };
    };
  };
  /** @description API endpoint that allows W32 bulletin Data to be viewed or edited */
  w32_data_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w32 data. */
        id_w32_data: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W32Data"];
        "application/x-www-form-urlencoded": components["schemas"]["W32Data"];
        "multipart/form-data": components["schemas"]["W32Data"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W32Data"];
        };
      };
    };
  };
  /** @description API endpoint that allows W32 bulletin Data to be viewed or edited */
  w32_data_destroy: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w32 data. */
        id_w32_data: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W32 bulletin Data to be viewed or edited */
  w32_data_partial_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w32 data. */
        id_w32_data: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW32Data"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW32Data"];
        "multipart/form-data": components["schemas"]["PatchedW32Data"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W32Data"];
        };
      };
    };
  };
  /** @description API endpoint that allows W32 bulletin MbaciniData to be viewed or edited */
  w32_datambacini_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W32MbaciniData"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows W32 bulletin MbaciniData to be viewed or edited */
  w32_datambacini_create: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["W32MbaciniData"];
        "application/x-www-form-urlencoded": components["schemas"]["W32MbaciniData"];
        "multipart/form-data": components["schemas"]["W32MbaciniData"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W32MbaciniData"];
        };
      };
    };
  };
  /** @description API endpoint that allows W32 bulletin MbaciniData to be viewed or edited */
  w32_datambacini_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w32 mbacini data. */
        id_w32_mbacini_data: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W32MbaciniData"];
        };
      };
    };
  };
  /** @description API endpoint that allows W32 bulletin MbaciniData to be viewed or edited */
  w32_datambacini_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w32 mbacini data. */
        id_w32_mbacini_data: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W32MbaciniData"];
        "application/x-www-form-urlencoded": components["schemas"]["W32MbaciniData"];
        "multipart/form-data": components["schemas"]["W32MbaciniData"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W32MbaciniData"];
        };
      };
    };
  };
  /** @description API endpoint that allows W32 bulletin MbaciniData to be viewed or edited */
  w32_datambacini_destroy: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w32 mbacini data. */
        id_w32_mbacini_data: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W32 bulletin MbaciniData to be viewed or edited */
  w32_datambacini_partial_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w32 mbacini data. */
        id_w32_mbacini_data: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW32MbaciniData"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW32MbaciniData"];
        "multipart/form-data": components["schemas"]["PatchedW32MbaciniData"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W32MbaciniData"];
        };
      };
    };
  };
  /** @description API endpoint that allows W32 bulletin Probabilita to be viewed or edited */
  w32_mbacini_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W32Mbacini"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows W32 bulletin Probabilita to be viewed or edited */
  w32_mbacini_create: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["W32Mbacini"];
        "application/x-www-form-urlencoded": components["schemas"]["W32Mbacini"];
        "multipart/form-data": components["schemas"]["W32Mbacini"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W32Mbacini"];
        };
      };
    };
  };
  /** @description API endpoint that allows W32 bulletin Probabilita to be viewed or edited */
  w32_mbacini_retrieve: {
    parameters: {
      path: {
        /** @description A unique value identifying this w32 mbacini. */
        id_w32_mbacini: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W32Mbacini"];
        };
      };
    };
  };
  /** @description API endpoint that allows W32 bulletin Probabilita to be viewed or edited */
  w32_mbacini_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this w32 mbacini. */
        id_w32_mbacini: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W32Mbacini"];
        "application/x-www-form-urlencoded": components["schemas"]["W32Mbacini"];
        "multipart/form-data": components["schemas"]["W32Mbacini"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W32Mbacini"];
        };
      };
    };
  };
  /** @description API endpoint that allows W32 bulletin Probabilita to be viewed or edited */
  w32_mbacini_destroy: {
    parameters: {
      path: {
        /** @description A unique value identifying this w32 mbacini. */
        id_w32_mbacini: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W32 bulletin Probabilita to be viewed or edited */
  w32_mbacini_partial_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this w32 mbacini. */
        id_w32_mbacini: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW32Mbacini"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW32Mbacini"];
        "multipart/form-data": components["schemas"]["PatchedW32Mbacini"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W32Mbacini"];
        };
      };
    };
  };
  /** @description API endpoint that allows W32 bulletin Pericolo to be viewed or edited */
  w32_pericolo_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W32Pericolo"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows W32 bulletin Pericolo to be viewed or edited */
  w32_pericolo_create: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["W32Pericolo"];
        "application/x-www-form-urlencoded": components["schemas"]["W32Pericolo"];
        "multipart/form-data": components["schemas"]["W32Pericolo"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W32Pericolo"];
        };
      };
    };
  };
  /** @description API endpoint that allows W32 bulletin Pericolo to be viewed or edited */
  w32_pericolo_retrieve: {
    parameters: {
      path: {
        /** @description A unique value identifying this w32 pericolo. */
        id_w32_pericolo: string;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W32Pericolo"];
        };
      };
    };
  };
  /** @description API endpoint that allows W32 bulletin Pericolo to be viewed or edited */
  w32_pericolo_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this w32 pericolo. */
        id_w32_pericolo: string;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W32Pericolo"];
        "application/x-www-form-urlencoded": components["schemas"]["W32Pericolo"];
        "multipart/form-data": components["schemas"]["W32Pericolo"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W32Pericolo"];
        };
      };
    };
  };
  /** @description API endpoint that allows W32 bulletin Pericolo to be viewed or edited */
  w32_pericolo_destroy: {
    parameters: {
      path: {
        /** @description A unique value identifying this w32 pericolo. */
        id_w32_pericolo: string;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W32 bulletin Pericolo to be viewed or edited */
  w32_pericolo_partial_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this w32 pericolo. */
        id_w32_pericolo: string;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW32Pericolo"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW32Pericolo"];
        "multipart/form-data": components["schemas"]["PatchedW32Pericolo"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W32Pericolo"];
        };
      };
    };
  };
  /** @description API endpoint that allows W32 bulletin Pericolombacini to be viewed or edited */
  w32_pericolombacini_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W32Pericolombacini"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows W32 bulletin Pericolombacini to be viewed or edited */
  w32_pericolombacini_create: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["W32Pericolombacini"];
        "application/x-www-form-urlencoded": components["schemas"]["W32Pericolombacini"];
        "multipart/form-data": components["schemas"]["W32Pericolombacini"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W32Pericolombacini"];
        };
      };
    };
  };
  /** @description API endpoint that allows W32 bulletin Pericolombacini to be viewed or edited */
  w32_pericolombacini_retrieve: {
    parameters: {
      path: {
        /** @description A unique value identifying this w32 pericolombacini. */
        id_w32_pericolombacini: string;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W32Pericolombacini"];
        };
      };
    };
  };
  /** @description API endpoint that allows W32 bulletin Pericolombacini to be viewed or edited */
  w32_pericolombacini_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this w32 pericolombacini. */
        id_w32_pericolombacini: string;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W32Pericolombacini"];
        "application/x-www-form-urlencoded": components["schemas"]["W32Pericolombacini"];
        "multipart/form-data": components["schemas"]["W32Pericolombacini"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W32Pericolombacini"];
        };
      };
    };
  };
  /** @description API endpoint that allows W32 bulletin Pericolombacini to be viewed or edited */
  w32_pericolombacini_destroy: {
    parameters: {
      path: {
        /** @description A unique value identifying this w32 pericolombacini. */
        id_w32_pericolombacini: string;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W32 bulletin Pericolombacini to be viewed or edited */
  w32_pericolombacini_partial_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this w32 pericolombacini. */
        id_w32_pericolombacini: string;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW32Pericolombacini"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW32Pericolombacini"];
        "multipart/form-data": components["schemas"]["PatchedW32Pericolombacini"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W32Pericolombacini"];
        };
      };
    };
  };
  /** @description API endpoint that allows W32 bulletin Zone to be viewed or edited */
  w32_zone_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W32Zone"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows W32 bulletin Zone to be viewed or edited */
  w32_zone_create: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["W32Zone"];
        "application/x-www-form-urlencoded": components["schemas"]["W32Zone"];
        "multipart/form-data": components["schemas"]["W32Zone"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W32Zone"];
        };
      };
    };
  };
  /** @description API endpoint that allows W32 bulletin Zone to be viewed or edited */
  w32_zone_retrieve: {
    parameters: {
      path: {
        /** @description A unique value identifying this w32 zone. */
        id_w32_zone: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W32Zone"];
        };
      };
    };
  };
  /** @description API endpoint that allows W32 bulletin Zone to be viewed or edited */
  w32_zone_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this w32 zone. */
        id_w32_zone: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W32Zone"];
        "application/x-www-form-urlencoded": components["schemas"]["W32Zone"];
        "multipart/form-data": components["schemas"]["W32Zone"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W32Zone"];
        };
      };
    };
  };
  /** @description API endpoint that allows W32 bulletin Zone to be viewed or edited */
  w32_zone_destroy: {
    parameters: {
      path: {
        /** @description A unique value identifying this w32 zone. */
        id_w32_zone: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W32 bulletin Zone to be viewed or edited */
  w32_zone_partial_update: {
    parameters: {
      path: {
        /** @description A unique value identifying this w32 zone. */
        id_w32_zone: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW32Zone"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW32Zone"];
        "multipart/form-data": components["schemas"]["PatchedW32Zone"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W32Zone"];
        };
      };
    };
  };
  /** @description API endpoint that allows W33 bulletins to be viewed or edited */
  w33_bulletins_list: {
    parameters: {
      query?: {
        /** @description A page number within the paginated result set. */
        page?: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["PaginatedW33List"];
        };
      };
    };
  };
  /** @description API endpoint that allows W33 bulletins to be viewed or edited */
  w33_bulletins_create: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["W33"];
        "application/x-www-form-urlencoded": components["schemas"]["W33"];
        "multipart/form-data": components["schemas"]["W33"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W33"];
        };
      };
    };
  };
  /** @description API endpoint that allows W33 bulletins to be viewed or edited */
  w33_bulletins_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w33. */
        id_w33: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W33"];
        };
      };
    };
  };
  /** @description API endpoint that allows W33 bulletins to be viewed or edited */
  w33_bulletins_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w33. */
        id_w33: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W33"];
        "application/x-www-form-urlencoded": components["schemas"]["W33"];
        "multipart/form-data": components["schemas"]["W33"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W33"];
        };
      };
    };
  };
  /** @description API endpoint that allows W33 bulletins to be viewed or edited */
  w33_bulletins_destroy: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w33. */
        id_w33: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W33 bulletins to be viewed or edited */
  w33_bulletins_partial_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w33. */
        id_w33: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW33"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW33"];
        "multipart/form-data": components["schemas"]["PatchedW33"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W33"];
        };
      };
    };
  };
  /** @description API endpoint that allows W33 bulletins to be viewed or edited */
  w33_bulletins_reopen_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w33. */
        id_w33: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W33"];
        };
      };
    };
  };
  /** @description API endpoint that allows W33 bulletins to be viewed or edited */
  w33_bulletins_send_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w33. */
        id_w33: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W33"];
        };
      };
    };
  };
  /** @description API endpoint that allows W33 bulletins to be viewed or edited */
  w33_bulletins_bulk_update_create: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["W33"];
        "application/x-www-form-urlencoded": components["schemas"]["W33"];
        "multipart/form-data": components["schemas"]["W33"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W33"];
        };
      };
    };
  };
  /** @description API endpoint that allows W33 bulletins to be viewed or edited */
  w33_bulletins_new_retrieve: {
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W33"];
        };
      };
    };
  };
  /** @description API endpoint that allows W33 bulletin Data to be viewed or edited */
  w33_data_list: {
    responses: {
      200: {
        content: {
          "application/json": (components["schemas"]["W33Data"])[];
        };
      };
    };
  };
  /** @description API endpoint that allows W33 bulletin Data to be viewed or edited */
  w33_data_create: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["W33Data"];
        "application/x-www-form-urlencoded": components["schemas"]["W33Data"];
        "multipart/form-data": components["schemas"]["W33Data"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["W33Data"];
        };
      };
    };
  };
  /** @description API endpoint that allows W33 bulletin Data to be viewed or edited */
  w33_data_retrieve: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w33 data. */
        id_w33_data: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W33Data"];
        };
      };
    };
  };
  /** @description API endpoint that allows W33 bulletin Data to be viewed or edited */
  w33_data_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w33 data. */
        id_w33_data: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["W33Data"];
        "application/x-www-form-urlencoded": components["schemas"]["W33Data"];
        "multipart/form-data": components["schemas"]["W33Data"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W33Data"];
        };
      };
    };
  };
  /** @description API endpoint that allows W33 bulletin Data to be viewed or edited */
  w33_data_destroy: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w33 data. */
        id_w33_data: number;
      };
    };
    responses: {
      /** @description No response body */
      204: never;
    };
  };
  /** @description API endpoint that allows W33 bulletin Data to be viewed or edited */
  w33_data_partial_update: {
    parameters: {
      path: {
        /** @description A unique integer value identifying this w33 data. */
        id_w33_data: number;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["PatchedW33Data"];
        "application/x-www-form-urlencoded": components["schemas"]["PatchedW33Data"];
        "multipart/form-data": components["schemas"]["PatchedW33Data"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["W33Data"];
        };
      };
    };
  };
}
