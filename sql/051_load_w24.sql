\c
\set command `echo "curl $DATA_LOCATION/w24_last_5_days.copy"`
COPY w24(
    id_w24,
    numero_bollettino,
    data_emissione,
    next_blt_time,
    sintesi_meteo,
    status,
    last_update,
    username,
    tipo_anomalia_termica,
    forzante_0,
    forzante_1,
    forzante_2
  ) FROM PROGRAM :'command' CSV HEADER DELIMITER ',' ;
\set command `echo "curl $DATA_LOCATION/w24_data_last_5_days.copy"`
COPY w24_data FROM PROGRAM :'command' CSV HEADER;
truncate forecast_zone;
\set command `echo "curl $DATA_LOCATION/forecast_zone.copy"`
COPY forecast_zone FROM PROGRAM :'command' CSV HEADER;
ALTER TABLE w24_data ADD COLUMN id_w24_data BIGSERIAL PRIMARY KEY;
