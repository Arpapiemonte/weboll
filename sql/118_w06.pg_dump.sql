CREATE TABLE public.w06 (
    id_w06 bigint NOT NULL,
    start_valid_time timestamp(0) without time zone NOT NULL,
    validity integer NOT NULL,
    next_blt_time timestamp(0) without time zone NOT NULL,
    status character(1) DEFAULT 0 NOT NULL,
    id_w06_parent integer,
    last_update timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(6) with time zone NOT NULL,
    username character varying(30) DEFAULT "current_user"() NOT NULL
);

COMMENT ON COLUMN public.w06.status IS '0 = Draft; 1 = Final';

CREATE SEQUENCE public.w06_id_w06_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE ONLY public.w06 ALTER COLUMN id_w06 SET DEFAULT nextval('public.w06_id_w06_seq'::regclass);

ALTER TABLE ONLY public.w06
    ADD CONSTRAINT w06_pkey PRIMARY KEY (id_w06);

CREATE TABLE public.w06_data (
    id_w06 bigint NOT NULL,
    id_w06_data serial NOT NULL,
    id_venue integer NOT NULL,
    id_time_layouts integer NOT NULL,
    sky_condition smallint,
    precipitation_class smallint,
    cumulated_snow integer,
    freezing_level integer,
    snow_level integer,
    temperature_below_zero boolean,
    risk_freezing_rain boolean
);

ALTER TABLE ONLY public.w06_data
    ADD CONSTRAINT w06_data_unique UNIQUE (id_w06, id_venue, id_time_layouts);

ALTER TABLE ONLY public.w06_data
    ADD CONSTRAINT w06_data_pkey PRIMARY KEY (id_w06_data);

ALTER TABLE ONLY public.w06_data
    ADD CONSTRAINT w06_data_fkey001 FOREIGN KEY (id_w06) REFERENCES public.w06(id_w06) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY public.w06_data
    ADD CONSTRAINT w06_data_fkey002 FOREIGN KEY (id_venue) REFERENCES public.venue(id_venue) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY public.w06_data
    ADD CONSTRAINT w06_data_fkey003 FOREIGN KEY (id_time_layouts) REFERENCES public.time_layouts(id_time_layouts) ON UPDATE CASCADE ON DELETE CASCADE;

\set command `echo "curl $DATA_LOCATION/w06.copy"`
COPY w06
  FROM PROGRAM :'command' CSV HEADER DELIMITER ',' ;
\set command `echo "curl $DATA_LOCATION/w06_data.copy"`
COPY w06_data 
  FROM PROGRAM :'command' CSV HEADER;

SELECT setval('public.w06_id_w06_seq', max(id_w06)) FROM public.w06;
SELECT setval('public.w06_data_id_w06_data_seq', max(id_w06_data)) FROM public.w06_data;