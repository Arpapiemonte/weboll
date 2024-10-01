--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;

SET default_tablespace = '';

CREATE TABLE public.w22giudizio (
	id_w22giudizio int8 NOT NULL,
	descrizione text NULL,
	colore_html varchar(30) NOT NULL
);

ALTER TABLE public.w22giudizio OWNER TO weboll;

COPY public.w22giudizio (id_w22giudizio, descrizione, colore_html) FROM stdin;
1	Ottimo	#6EBB00
2	Buono	#6EBB00
3	Sufficiente	#ffff00
4	Insufficiente	#FF0000
5	Pessimo	#8f00ff
\.

ALTER TABLE ONLY public.w22giudizio
    ADD CONSTRAINT id_w22giudizio_pkey PRIMARY KEY (id_w22giudizio);


CREATE TABLE public.w22severita (
	id_w22severita int8 NOT NULL,
	sigla varchar(3) NOT NULL,
	descrizione text NULL,
	colore_html varchar(30) NOT NULL
);

ALTER TABLE public.w22severita OWNER TO weboll;

COPY public.w22severita (id_w22severita, sigla, descrizione, colore_html) FROM stdin;
1	Ok	Assenza di errore	#6EBB00
2	Li	Errore lieve	#ffff00
3	Gr	Errore grave	#FF0000
4	MGr	Errore molto grave	#8f00ff
\.

ALTER TABLE ONLY public.w22severita
    ADD CONSTRAINT id_w22severita_pkey PRIMARY KEY (id_w22severita);


CREATE TABLE public.w22verifica (
	id_w22verifica bigserial NOT NULL,
	id_numero_bollettino varchar(30) NOT NULL,
  numero_bollettino varchar(30) NOT NULL,
	data_emissione date NOT NULL DEFAULT 'now'::text::date,
	data_analisi date NOT NULL DEFAULT 'now'::text::date,
	id_w22giudizio int8 NOT NULL,
	annotazione text NULL,
	situazione_evoluzione text NULL,
	status bpchar(1) NOT NULL DEFAULT 0,
	last_update timestamp(0) NOT NULL DEFAULT 'now'::text::timestamp(6) with time zone,
	username varchar(30) NOT NULL DEFAULT "current_user"()
);

ALTER TABLE public.w22verifica OWNER TO weboll;

ALTER TABLE ONLY public.w22verifica
    ADD CONSTRAINT w22verifica_pkey PRIMARY KEY (id_w22verifica);

ALTER TABLE ONLY public.w22verifica
    ADD CONSTRAINT w22verifica_fkey001 FOREIGN KEY (id_w22giudizio) REFERENCES public.w22giudizio(id_w22giudizio) ON DELETE CASCADE ON UPDATE CASCADE;

CREATE UNIQUE INDEX numero_bollettino_index ON public.w22 (numero_bollettino);

ALTER TABLE ONLY public.w22verifica
    ADD CONSTRAINT w22verifica_fkey002 FOREIGN KEY (numero_bollettino) REFERENCES public.w22(numero_bollettino) ON DELETE CASCADE ON UPDATE CASCADE;


CREATE TABLE public.w22verifica_data (
	id_w22verifica int8 NOT NULL,
	id_w22_zone int4 NOT NULL,
	prev_crit_tot varchar(15) NULL, 
	oss_crit_tot varchar(15) NULL,
	err_crit_tot int8 NOT NULL,
	id_w22verifica_data bigserial NOT NULL
);

ALTER TABLE public.w22verifica_data OWNER TO weboll;

--ALTER TABLE ONLY public.w22verifica_data
--    ADD CONSTRAINT w22verifica_data_pkey PRIMARY KEY (id_w22verifica_data);

ALTER TABLE ONLY public.w22verifica_data
    ADD CONSTRAINT w22verifica_data_fkey001 FOREIGN KEY (id_w22verifica) REFERENCES public.w22verifica(id_w22verifica) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE ONLY public.w22verifica_data
    ADD CONSTRAINT w22verifica_data_fkey002 FOREIGN KEY (id_w22_zone) REFERENCES public.w22_zone(id_w22_zone) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE ONLY public.w22verifica_data
    ADD CONSTRAINT w22verifica_data_fkey003 FOREIGN KEY (err_crit_tot ) REFERENCES public.w22severita(id_w22severita) ON DELETE CASCADE ON UPDATE CASCADE;

\set command `echo "curl $DATA_LOCATION/w22verifica.copy"`
COPY public.w22verifica
  FROM PROGRAM :'command' CSV HEADER;
\set command `echo "curl $DATA_LOCATION/w22verifica_data.copy"`
COPY public.w22verifica_data
  FROM PROGRAM :'command' CSV HEADER;

SELECT setval('public.w22verifica_id_w22verifica_seq', max(id_w22verifica)) FROM public.w22verifica;
SELECT setval('public.w22verifica_data_id_w22verifica_data_seq', max(id_w22verifica_data)) FROM public.w22verifica_data;