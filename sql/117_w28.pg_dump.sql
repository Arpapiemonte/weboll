CREATE TABLE public.w28 (
    id_w28 bigint NOT NULL,
    start_valid_time timestamp(0) without time zone NOT NULL,
    validity integer NOT NULL,
    next_blt_time timestamp(0) without time zone NOT NULL,
    status character(1) DEFAULT 0 NOT NULL,
    id_w28_parent integer,
    last_update timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(6) with time zone NOT NULL,
    username character varying(30) DEFAULT "current_user"() NOT NULL
);

COMMENT ON COLUMN public.w28.status IS '0 = Draft; 1 = Final';

CREATE SEQUENCE public.w28_id_w28_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE ONLY public.w28 ALTER COLUMN id_w28 SET DEFAULT nextval('public.w28_id_w28_seq'::regclass);

ALTER TABLE ONLY public.w28
    ADD CONSTRAINT w28_pkey PRIMARY KEY (id_w28);

CREATE TABLE public.w28_data (
    id_w28 bigint NOT NULL,
    id_w28_data serial NOT NULL,
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

ALTER TABLE ONLY public.w28_data
    ADD CONSTRAINT w28_data_unique UNIQUE (id_w28, id_venue, id_time_layouts);

ALTER TABLE ONLY public.w28_data
    ADD CONSTRAINT w28_data_pkey PRIMARY KEY (id_w28_data);

ALTER TABLE ONLY public.w28_data
    ADD CONSTRAINT w28_data_fkey001 FOREIGN KEY (id_w28) REFERENCES public.w28(id_w28) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY public.w28_data
    ADD CONSTRAINT w28_data_fkey002 FOREIGN KEY (id_venue) REFERENCES public.venue(id_venue) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY public.w28_data
    ADD CONSTRAINT w28_data_fkey003 FOREIGN KEY (id_time_layouts) REFERENCES public.time_layouts(id_time_layouts) ON UPDATE CASCADE ON DELETE CASCADE;

\set command `echo "curl $DATA_LOCATION/w28.copy"`
COPY w28(id_w28,start_valid_time,validity,next_blt_time,status,last_update,username) 
  FROM PROGRAM :'command' CSV HEADER DELIMITER ',' ;
\set command `echo "curl $DATA_LOCATION/w28_data.copy"`
COPY w28_data(id_w28,id_venue,id_time_layouts,sky_condition,precipitation_class,cumulated_snow,freezing_level,snow_level,temperature_below_zero,risk_freezing_rain) 
  FROM PROGRAM :'command' CSV HEADER;
