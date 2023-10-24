-- public.w17 definition

-- Drop table

-- DROP TABLE public.w17;

CREATE OR REPLACE FUNCTION public.w17_numero_bollettino()
 RETURNS character varying
 LANGUAGE plpgsql
AS $function$
BEGIN
  RETURN
  (SELECT COUNT(DISTINCT data_emissione) + 1 || '/' || date_part('year', current_date)
  FROM w17
  WHERE data_emissione >= date_trunc('year', current_date) AND data_emissione < current_date);

END;
$function$
;


CREATE TABLE public.w17 (
	id_w17 bigserial NOT NULL,
	data_analysis date NOT NULL,
	data_emissione date NOT NULL DEFAULT 'now'::text::date,
	next_blt_time date NOT NULL,
	situation text NULL,
	cloudiness text NULL,
	weather_code text NULL,
	last_update timestamp(0) NOT NULL DEFAULT 'now'::text::timestamp(6) with time zone,
	username varchar(30) NOT NULL DEFAULT "current_user"(),
	status bpchar(1) NULL,
	numero_bollettino varchar(30) NOT NULL DEFAULT w17_numero_bollettino(),
	CONSTRAINT w17_pkey PRIMARY KEY (id_w17)
);


-- public.w17_blob definition

-- Drop table

-- DROP TABLE public.w17_blob;

CREATE TABLE public.w17_blob (
	id_w17 int8 NOT NULL,
	situation_image bytea NULL,
	cloudiness_image bytea NULL,
	prec_mattino_image bytea NULL,
	prec_pomeriggio_image bytea NULL,
	temp_minime_image bytea NULL,
	temp_massime_image bytea NULL,
	CONSTRAINT w17_blob_pkey PRIMARY KEY (id_w17),
	CONSTRAINT w17_blob_fkey001 FOREIGN KEY (id_w17) REFERENCES public.w17(id_w17) ON DELETE CASCADE ON UPDATE CASCADE
);


-- public.w17_classes definition

-- Drop table

-- DROP TABLE public.w17_classes;

CREATE TABLE public.w17_classes (
	id_w17 int4 NOT NULL,
	id_w17_classes bigserial NOT NULL,
	id_parametro varchar(10) NOT NULL,
	id_classes_value int2 NOT NULL,
	id_classes int2 NOT NULL,
	id_time_layouts int4 NOT NULL,
	CONSTRAINT w17_classes_pkey PRIMARY KEY (id_w17_classes),
	CONSTRAINT w17_classes_unique UNIQUE (id_w17, id_classes_value, id_classes, id_time_layouts),
	CONSTRAINT w17_classes_fkey001 FOREIGN KEY (id_w17) REFERENCES public.w17(id_w17) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT w17_classes_fkey002 FOREIGN KEY (id_parametro) REFERENCES public.parametro(id_parametro) ON UPDATE CASCADE,
	CONSTRAINT w17_classes_fkey003 FOREIGN KEY (id_classes_value) REFERENCES public.classes_value(id_classes_value) ON UPDATE CASCADE,
	CONSTRAINT w17_classes_fkey004 FOREIGN KEY (id_classes) REFERENCES public.classes(id_classes) ON UPDATE CASCADE,
	CONSTRAINT w17_classes_fkey005 FOREIGN KEY (id_time_layouts) REFERENCES public.time_layouts(id_time_layouts) ON UPDATE CASCADE
);


-- public.w17_data definition

-- Drop table

-- DROP TABLE public.w17_data;

CREATE TABLE public.w17_data (
	id_w17 int8 NOT NULL,
	id_w17_data bigserial NOT NULL,
	id_venue int4 NOT NULL,
	id_time_layouts int4 NOT NULL,
	id_parametro varchar(10) NOT NULL,
	id_aggregazione int4 NOT NULL,
	numeric_value numeric(7, 2) NULL,
	id_trend int2 NULL,
	text_value text NULL,
	cod_staz_meteo varchar(5) NULL,
	CONSTRAINT w17_data_pkey PRIMARY KEY (id_w17_data),
	CONSTRAINT w17_data_unique UNIQUE (id_w17, id_venue, id_time_layouts, id_parametro, id_aggregazione),
	CONSTRAINT w17_data_fkey001 FOREIGN KEY (id_w17) REFERENCES public.w17(id_w17) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT w17_data_fkey002 FOREIGN KEY (id_venue) REFERENCES public.venue(id_venue) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT w17_data_fkey003 FOREIGN KEY (id_time_layouts) REFERENCES public.time_layouts(id_time_layouts) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT w17_data_fkey004 FOREIGN KEY (id_parametro) REFERENCES public.parametro(id_parametro) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT w17_data_fkey005 FOREIGN KEY (id_aggregazione) REFERENCES public.aggregazione(id_aggregazione) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT w17_data_fkey006 FOREIGN KEY (cod_staz_meteo) REFERENCES public.stazione_misura(cod_staz_meteo) ON DELETE CASCADE ON UPDATE CASCADE
);


ALTER TABLE public.w17 OWNER TO weboll;
ALTER TABLE public.w17_blob OWNER TO weboll;
ALTER TABLE public.w17_classes OWNER TO weboll;
ALTER TABLE public.w17_classes_id_w17_classes_seq OWNER TO weboll;
ALTER TABLE public.w17_data OWNER TO weboll;
ALTER TABLE public.w17_data_id_w17_data_seq OWNER TO weboll;
ALTER TABLE public.w17_id_w17_seq OWNER TO weboll;


\set command `echo "curl $DATA_LOCATION/w17_last_days.copy"`
COPY w17 FROM PROGRAM :'command' CSV HEADER;

\set command `echo "curl $DATA_LOCATION/w17_blob_last_days.copy"`
COPY w17_blob FROM PROGRAM :'command' CSV HEADER;

\set command `echo "curl $DATA_LOCATION/w17_classes_last_days.copy"`
COPY w17_classes(id_w17,
	id_parametro,
	id_classes_value,
	id_classes,
	id_time_layouts) FROM PROGRAM :'command' CSV HEADER;

\set command `echo "curl $DATA_LOCATION/w17_data_last_days.copy"`
COPY w17_data(id_w17,
	id_venue,
	id_time_layouts,
	id_parametro,
	id_aggregazione,
	numeric_value,
	id_trend,
	text_value,
	cod_staz_meteo) FROM PROGRAM :'command' CSV HEADER;

ALTER TABLE public.w17 ADD id_w17_parent INTEGER DEFAULT NULL;