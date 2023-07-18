\c
\set command `echo "curl $DATA_LOCATION/w30_last_5_days.copy"`
COPY w30 FROM PROGRAM :'command' CSV HEADER DELIMITER ',' ;
\set command `echo "curl $DATA_LOCATION/w30_data_last_5_days.copy"`
COPY w30_data FROM PROGRAM :'command' CSV HEADER;
