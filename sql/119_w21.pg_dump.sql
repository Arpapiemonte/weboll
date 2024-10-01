CREATE TABLE public.w21 (
	id_w21 bigserial NOT NULL,
	data_emissione date NOT NULL DEFAULT 'now'::text::date,
	id_w21_parent integer,
	status bpchar(1) NOT NULL DEFAULT 0,
	last_update timestamp(0) NOT NULL DEFAULT 'now'::text::timestamp(6) with time zone,
	username varchar(30) NOT NULL DEFAULT "current_user"(),
	CONSTRAINT w21_pkey PRIMARY KEY (id_w21)
);
COMMENT ON COLUMN public.w21.status IS '0 = Draft; 1 = Final; 2 = Reopen';

CREATE TABLE public.w21_data (
	id_w21_data bigserial NOT NULL,
	id_w21 bigint NOT NULL,
	id_venue integer NOT NULL,
	id_time_layouts integer NOT NULL,
	id_parametro varchar(10) NOT NULL,
	id_aggregazione integer NOT NULL,
	numeric_value numeric(7, 2) NULL,
	id_trend integer NULL,
	CONSTRAINT w21_data_pkey PRIMARY KEY (id_w21_data)
);

ALTER TABLE ONLY public.w21_data
    ADD CONSTRAINT w21_data_unique UNIQUE (id_w21, id_venue, id_time_layouts, id_parametro, id_aggregazione);

ALTER TABLE public.w21_data ADD CONSTRAINT w21_data_fkey001 FOREIGN KEY (id_w21) REFERENCES public.w21(id_w21) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE public.w21_data ADD CONSTRAINT w21_data_fkey002 FOREIGN KEY (id_venue) REFERENCES public.venue(id_venue) ON DELETE SET NULL ON UPDATE CASCADE;
ALTER TABLE public.w21_data ADD CONSTRAINT w21_data_fkey003 FOREIGN KEY (id_time_layouts) REFERENCES public.time_layouts(id_time_layouts) ON DELETE SET NULL ON UPDATE CASCADE;
ALTER TABLE public.w21_data ADD CONSTRAINT w21_data_fkey004 FOREIGN KEY (id_parametro) REFERENCES public.parametro(id_parametro) ON DELETE SET NULL ON UPDATE CASCADE;
ALTER TABLE public.w21_data ADD CONSTRAINT w21_data_fkey005 FOREIGN KEY (id_aggregazione) REFERENCES public.aggregazione(id_aggregazione) ON DELETE SET NULL ON UPDATE CASCADE;

\set command `echo "curl $DATA_LOCATION/w21.copy"`
COPY w21
  FROM PROGRAM :'command' CSV HEADER DELIMITER ',' ;
\set command `echo "curl $DATA_LOCATION/w21_data.copy"`
COPY w21_data
  FROM PROGRAM :'command' CSV HEADER;

SELECT setval('public.w21_id_w21_seq', max(id_w21)) FROM public.w21;
SELECT setval('public.w21_data_id_w21_data_seq', max(id_w21_data)) FROM public.w21_data;