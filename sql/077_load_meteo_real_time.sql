\c
\set command `echo "curl $DATA_LOCATION/meteo_real_time.copy"`
COPY meteo_real_time_idro FROM PROGRAM :'command' CSV HEADER;
