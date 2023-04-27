\c
\set command `echo "curl $DATA_LOCATION/w23_last_5_days.copy"`
COPY w23(
    id_w23,
    data_emissione,
    numero_bollettino,
    situazione_meteo,
    status,
    last_update,
    username,
    fraserisknat,
    annotazione,
    last_update_annotazione
  ) FROM PROGRAM :'command' CSV HEADER;
\set command `echo "curl $DATA_LOCATION/w23_data_last_5_days.copy"`
COPY w23_data FROM PROGRAM :'command' CSV HEADER;
truncate w23_pluvossh6;
\set command `echo "curl $DATA_LOCATION/w23_pluvossh6.copy"`
COPY w23_pluvossh6 FROM PROGRAM :'command' CSV HEADER;
ALTER TABLE w23_data ADD COLUMN id_w23_data BIGSERIAL PRIMARY KEY;
alter table w23_pluvossh6 drop CONSTRAINT w23_pluvossh6_pkey;
ALTER TABLE w23_pluvossh6 ADD COLUMN id_w23_pluvossh6 BIGSERIAL PRIMARY KEY;
