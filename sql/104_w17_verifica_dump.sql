-- public.w17_verifica definition

-- Drop table

-- DROP TABLE public.w17_verifica;

CREATE TABLE public.w17_verifica (
	id_w17verifica  bigserial NOT NULL,
	data_analysis date NULL,
	data_emissione date NOT NULL DEFAULT 'now'::text::date,
	next_blt_time date NOT NULL,
	status bpchar(1) NULL,
	last_update timestamp(0) NOT NULL DEFAULT 'now'::text::timestamp(6) with time zone,
	username varchar(30) NOT NULL DEFAULT "current_user"(),
	CONSTRAINT w17_verifica_pkey PRIMARY KEY (id_w17verifica),
	CONSTRAINT w17_verifica_fkey001 FOREIGN KEY (id_w17verifica) REFERENCES public.w17_verifica(id_w17verifica) ON DELETE CASCADE ON UPDATE CASCADE
);


-- public.w17_verifica_data definition

-- Drop table

-- DROP TABLE public.w17_verifica_data;

CREATE TABLE public.w17_verifica_data (
	id_w17verifica int8 NOT NULL,
	id_w05 int8 NOT NULL,
	id_w17_verifica_data bigserial NOT NULL,
	data_forecast date NULL,
	forecast_id int2 NOT NULL,
	punteggio_relativo int4 NOT NULL,
	punteggio_nubi int4 NOT NULL,
	punteggio_pioggia int4 NOT NULL,
	punteggio_vento int4 NOT NULL,
	punteggio_temperatura int4 NOT NULL,
	punteggio_zero_quota_neve int4 NOT NULL,
	coerenza_mattino_nubi int4 NOT NULL,
	coerenza_pomeriggio_nubi int4 NOT NULL,
	coerenza_mattino_pioggia int4 NOT NULL,
	coerenza_pomeriggio_pioggia int4 NOT NULL,
	CONSTRAINT w17_verifica_data_pkey PRIMARY KEY (id_w17_verifica_data),
	CONSTRAINT w17_verifica_data_unique UNIQUE (id_w17verifica, forecast_id),
	CONSTRAINT w17_verifica_data_fkey001 FOREIGN KEY (id_w17verifica) REFERENCES public.w17_verifica(id_w17verifica) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT w17_verifica_data_fkey002 FOREIGN KEY (id_w05) REFERENCES public.w05(id_w05) ON UPDATE CASCADE
);

-- public.w17_verifica_massimali definition

-- Drop table

-- DROP TABLE public.w17_verifica_massimali;

CREATE TABLE public.w17_verifica_massimali (
	id_w17_verifica_massimali bigserial NOT NULL,
	id_parametro varchar(10) NOT NULL,
	id_aggregazione int4 NOT NULL,
	categoria int2 NOT NULL,
	punti_max int2 NULL,
	last_update timestamp(0) NOT NULL DEFAULT 'now'::text::timestamp(6) with time zone,
	username varchar(30) NOT NULL DEFAULT "current_user"(),
	CONSTRAINT w17_verifica_massimali_pkey PRIMARY KEY (id_w17_verifica_massimali),
	CONSTRAINT w17_verifica_massimali_unique UNIQUE (id_parametro, id_aggregazione, categoria),
	CONSTRAINT w17_verifica_massimali_fkey001 FOREIGN KEY (id_aggregazione) REFERENCES public.aggregazione(id_aggregazione) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT w17_verifica_massimali_fkey002 FOREIGN KEY (id_parametro) REFERENCES public.parametro(id_parametro) ON DELETE CASCADE ON UPDATE CASCADE
);

SELECT setval('public.w17_verifica_data_id_w17_verifica_data_seq', max(id_w17_verifica_data)) FROM public.w17_verifica_data;

ALTER TABLE public.w17_verifica OWNER TO weboll;
ALTER TABLE public.w17_verifica_data OWNER TO weboll;
ALTER TABLE public.w17_verifica_massimali OWNER TO weboll;

COPY public.w17_verifica_massimali (id_parametro, id_aggregazione, categoria, punti_max, last_update, username) FROM stdin;
COP_TOT	0	1	2	2014-07-11 15:21:41	weboll
TERMA	909	10	2	2014-07-11 15:22:56	weboll
COP_TOT	0	3	0	2014-07-11 15:23:23	weboll
COP_TOT	0	4	2	2014-07-11 15:23:29	weboll
PLUV	0	5	2	2014-07-11 15:23:35	weboll
PLUV	0	6	2	2014-07-11 15:23:41	weboll
PLUV	0	7	2	2014-07-11 15:23:47	weboll
PLUV	0	8	2	2014-07-11 15:23:56	weboll
FRZLVL	914	12	2	2014-07-11 15:24:00	weboll
FRZLVL	912	13	2	2014-07-11 15:24:04	weboll
TERMA	910	9	2	2014-07-11 15:24:08	weboll
SNOW_LEV	323	15	1	2014-07-11 15:24:22	weboll
SNOW_LEV	324	14	1	2014-07-11 15:24:30	weboll
SNOW_LEV	0	14	0	2014-07-11 15:24:38	weboll
SNOW_LEV	0	15	0	2014-07-11 15:24:41	weboll
TERMA	0	9	2	2014-07-11 15:24:45	weboll
TERMA	0	10	2	2014-07-11 15:24:48	weboll
FRZLVL	0	12	1	2014-07-11 15:24:55	weboll
FRZLVL	0	13	1	2014-07-11 15:25:00	weboll
COP_TOT	0	2	2	2014-07-11 15:25:05	weboll
VELV	0	16	2	2014-07-11 15:25:10	weboll
VELV	0	17	1	2014-07-11 15:25:16	weboll
VELV	0	18	2	2014-07-11 15:25:22	weboll
VELV	0	19	1	2014-07-11 15:25:26	weboll
VELV	0	20	1	2014-07-11 15:25:32	weboll
VELV	0	21	2	2014-07-11 15:25:36	weboll
COP_TOT	0	99	2	2014-10-15 15:28:14	weboll
PLUV	0	99	2	2014-10-15 15:28:30	weboll
\.


\set command `echo "curl $DATA_LOCATION/w17_verifica_last_days.copy"`
COPY w17_verifica FROM PROGRAM :'command' CSV HEADER;


\set command `echo "curl $DATA_LOCATION/w17_verifica_data_last_days.copy"`
COPY w17_verifica_data(
    id_w17verifica,
	id_w05,
	data_forecast,
	forecast_id,
	punteggio_relativo,
	punteggio_nubi,
	punteggio_pioggia,
	punteggio_vento,
	punteggio_temperatura,
	punteggio_zero_quota_neve,
	coerenza_mattino_nubi,
	coerenza_pomeriggio_nubi,
	coerenza_mattino_pioggia,
	coerenza_pomeriggio_pioggia) FROM PROGRAM :'command' CSV HEADER;
