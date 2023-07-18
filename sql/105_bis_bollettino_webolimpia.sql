create table public.bis_bollettino_webolimpia (
	data timestamp without time zone,
	codice character varying(9),
	numero integer,
	h_min numeric,
	h_max numeric,
	h_med numeric,
	q_min numeric,
	q_max numeric,
	q_med numeric,
	corso_acqua character varying(50),
	localita character varying(50),
	id_note integer,
	note text
);

ALTER TABLE public.bis_bollettino_webolimpia OWNER TO weboll;

\c
truncate public.bis_bollettino_webolimpia;
\set command `echo "curl $DATA_LOCATION/bis_bollettino_webolimpia.copy"`
COPY public.bis_bollettino_webolimpia FROM PROGRAM :'command' CSV HEADER;