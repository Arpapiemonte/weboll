-- author    = "weboll"
-- credits   = ""
-- copyright = "Copyright (C) 2025 Arpa Piemonte - Dipartimento Rischi Naturali e Ambientali"
-- date      = "2021-05-17"
-- manteiner = "weboll"
-- email     = "noreply@arpa.piemonte.it"
-- license   = "Licensed under the European Union Public License 1.2 (EUPL-1.2) as per linee guida per l’Acquisizione e il riuso di software per la Pubblica Amministrazione."
\c
truncate qa_misure cascade;
\set command `echo "curl $DATA_LOCATION/qa_misure_last_5_days.value"`
COPY qa_misure(
        id_venue
        ,data_emissione
        ,data_scadenza
        ,id_scadenza
        ,id_strumentazione
        ,id_qa_aggregazione
        ,id_qa_parametro
        ,valore_originale_num
        ,valore_validato_num
        ,valore_originale_classe
        ,valore_validato_classe
        ,valore_originale_txt
        ,valore_validato_txt
	,last_update
        ,username
  ) FROM PROGRAM :'command' CSV DELIMITER ',' HEADER;
