\c
truncate w05 cascade;
truncate weather_values;
\set command `echo "curl $DATA_LOCATION/w05_last_5_days.copy"`
COPY w05 FROM PROGRAM :'command' CSV HEADER;
\set command `echo "curl $DATA_LOCATION/w05_data_last_5_days.copy"`
COPY w05_data(id_w05,
  id_venue ,
  id_parametro ,
  id_aggregazione ,
  numeric_value ,
  id_trend ,
  text_value ,
  id_time_layouts,
  start_valid_time,
  end_valid_time) FROM PROGRAM :'command' CSV HEADER;
\set command `echo "curl $DATA_LOCATION/w05_classes_last_5_days.copy"`
COPY w05_classes(id_w05,
  id_venue,
  id_parametro,
  id_aggregazione,
  id_classes_value,
  id_classes,
  id_time_layouts,
  start_valid_time,
  end_valid_time) FROM PROGRAM :'command' CSV HEADER;
\set command `echo "curl $DATA_LOCATION/weather_values.copy"`
COPY weather_values(id_venue,
  start_time,
  end_time,
  id_time_layouts,
  id_parametro,
  id_aggregazione,
  original_numeric_values,
  validated_numeric_values,
  original_text_values,
  validated_text_values,
  original_trend,
  validated_trend,
  id_query_numeric,
  id_query_text,
  cod_staz_meteo,
  last_update,
  username,
  id_weather_values) FROM PROGRAM :'command' CSV HEADER;
SELECT setval('w05_id_seq', max(id_w05)) FROM w05;
SELECT setval('w05_data_id_w05_data_seq', max(id_w05_data)) FROM w05_data;
SELECT setval('w05_classes_id_w05_classes_seq', max(id_w05_classes)) FROM w05_classes;
