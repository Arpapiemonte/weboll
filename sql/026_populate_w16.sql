-- author    = "weboll"
-- credits   = ""
-- copyright = "Copyright (C) 2024 Arpa Piemonte - Dipartimento Rischi Naturali e Ambientali"
-- date      = "2021-07-28"
-- manteiner = "weboll"
-- email     = "noreply@arpa.piemonte.it"
-- license   = "Licensed under the European Union Public License 1.2 (EUPL-1.2) as per linee guida per l’Acquisizione e il riuso di software per la Pubblica Amministrazione."
\c
truncate w16 cascade;
\set command `echo "curl $DATA_LOCATION/w16_last_5_days.value"`
COPY w16(
        id_w16
        ,start_valid_time
        ,validity
        ,next_blt_time
        ,made_by
        ,note
        ,status
        ,last_update
        ,username
        ,seq_num
        ,version
        ,id_w16_parent
  ) FROM PROGRAM :'command' CSV DELIMITER ',' ;
-- truncate w16_data cascade;
\set command `echo "curl $DATA_LOCATION/w16_data_last_5_days.value"`
COPY w16_data(
        id_w16_data
        ,id_w16
	,id_ozono_zone
        ,data_emissione
	,data_scadenza
        ,id_scadenza
        ,id_ozono_livelli
  ) FROM PROGRAM :'command' CSV DELIMITER ',' ;
-- truncate w16_data1 cascade;
\set command `echo "curl $DATA_LOCATION/w16_data1_last_5_days.value"`
COPY w16_data1(
        id_w16_data
        ,id_qa_parametro
	,id_ozono_aggregazione
        ,valore_num
	,valore_classe
        ,id_w16_data1
        ,id_strumentazione
  ) FROM PROGRAM :'command' CSV DELIMITER ',' ;
