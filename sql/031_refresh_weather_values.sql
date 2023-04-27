/* serve per copiare la weather_values di db2006_new sul database weboll tramite la vista weather_values_remote */
CREATE OR REPLACE FUNCTION public.refresh_weather_values() RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN

/* è legato al file 14_weather_values_pg_dump.sql riga 3670
ALTER TABLE "public"."weather_values" DISABLE TRIGGER "weather_values_tr"; */


DELETE FROM weather_values
WHERE (id_venue, start_time, end_time, id_parametro, id_aggregazione) NOT IN
(SELECT id_venue, start_time, end_time, id_parametro, id_aggregazione
FROM weather_values_remote);


DELETE FROM weather_values
WHERE (id_venue, start_time, end_time, id_parametro, id_aggregazione) IN
   (SELECT id_venue, start_time, end_time, id_parametro, id_aggregazione
   FROM weather_values
   WHERE (id_venue, start_time, end_time, id_parametro, id_aggregazione) IN
      (SELECT id_venue, start_time, end_time, id_parametro, id_aggregazione
      FROM weather_values_remote)
   GROUP BY id_venue, start_time, end_time, id_parametro, id_aggregazione
   HAVING COUNT(*) > 1);


UPDATE weather_values
SET id_time_layouts = weather_values_remote.id_time_layouts,
 original_numeric_values = weather_values_remote.original_numeric_values,
 validated_numeric_values = weather_values_remote.validated_numeric_values,
 original_text_values = weather_values_remote.original_text_values,
 validated_text_values = weather_values_remote.validated_text_values,
 original_trend = weather_values_remote.original_trend,
 validated_trend = weather_values_remote.validated_trend,
 id_query_numeric = weather_values_remote.id_query_numeric,
 id_query_text = weather_values_remote.id_query_text,
 cod_staz_meteo = weather_values_remote.cod_staz_meteo,
 last_update = weather_values_remote.last_update,
 username = weather_values_remote.username
FROM weather_values_remote
WHERE
(weather_values.id_venue, weather_values.start_time, weather_values.end_time, weather_values.id_parametro, weather_values.id_aggregazione) =
(weather_values_remote.id_venue, weather_values_remote.start_time, weather_values_remote.end_time, weather_values_remote.id_parametro, weather_values_remote.id_aggregazione);

INSERT INTO weather_values (
  id_venue,
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
  username
)
SELECT id_venue, start_time, end_time, id_time_layouts, id_parametro,
id_aggregazione, original_numeric_values, validated_numeric_values,
original_text_values, validated_text_values, original_trend, validated_trend,
id_query_numeric, id_query_text, cod_staz_meteo, last_update, username FROM weather_values_remote
WHERE (id_venue, start_time, end_time, id_parametro, id_aggregazione) NOT IN
(SELECT id_venue, start_time, end_time, id_parametro, id_aggregazione
FROM weather_values);

/* è legato al file 14_weather_values_pg_dump.sql riga 3670
ALTER TABLE "public"."weather_values" ENABLE TRIGGER "weather_values_tr"; */

RETURN;
END
$$;


/* ALTER FUNCTION public.refresh_weather_values() OWNER TO weboll; */
