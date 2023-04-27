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

COPY public.w22verifica (id_w22verifica, id_numero_bollettino, numero_bollettino, data_emissione, data_analisi, id_w22giudizio, annotazione, situazione_evoluzione, status, last_update, username) FROM stdin;
10	27_2023	27/2023	2022-02-20	2014-06-03	1	nulla da segnalare	-Note:	1	2014-06-03 12:15:51	weboll
20	26_2023	26/2023	2023-02-19	2014-06-04	1	nulla da segnalare oggi	-Note:	1	2014-06-04 13:15:51	weboll
\.

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

COPY public.w22verifica_data (id_w22verifica, id_w22_zone, prev_crit_tot, oss_crit_tot, err_crit_tot, id_w22verifica_data) FROM stdin;
10	1	A	O	3	22
10	2	A	O	3	23
10	3	A	O	3	24
10	4	A	O	3	25
10	5	A	O	3	26
10	6	A	O	3	27
10	7	A	O	3	28
10	8	A	O	3	29
10	9	A	O	3	30
10	10	A	O	3	31
10	11	A	O	3	32
10	12	A	O	3	33
10	13	A	O	3	34
10	14	A	O	3	35
10	15	A	O	3	36
10	16	A	O	3	37
10	17	A	O	3	38
10	18	A	O	3	39
10	19	A	O	3	40
10	20	A	O	3	41
10	21	A	O	3	42
10	22	A	O	3	43
10	23	A	O	3	44
10	24	A	O	3	45
10	25	A	O	3	46
10	26	A	O	3	47
10	27	A	O	3	48
20	1	A	O	3	49
20	2	A	O	3	50
20	3	A	O	3	51
20	4	A	O	3	52
20	5	A	O	3	53
20	6	A	O	3	54
20	7	A	O	3	55
20	8	A	O	3	56
20	9	A	O	3	57
20	10	A	O	3	58
20	11	A	O	3	59
20	12	A	O	3	60
20	13	A	O	3	61
20	14	A	O	3	62
20	15	A	O	3	63
20	16	A	O	3	64
20	17	A	O	3	65
20	18	A	O	3	66
20	19	A	O	3	67
20	20	A	O	3	68
20	21	A	O	3	69
20	22	A	O	3	70
20	23	A	O	3	71
20	24	A	O	3	72
20	25	A	O	3	73
20	26	A	O	3	74
20	27	A	O	3	75
\.

--ALTER TABLE ONLY public.w22verifica_data
--    ADD CONSTRAINT w22verifica_data_pkey PRIMARY KEY (id_w22verifica_data);

ALTER TABLE ONLY public.w22verifica_data
    ADD CONSTRAINT w22verifica_data_fkey001 FOREIGN KEY (id_w22verifica) REFERENCES public.w22verifica(id_w22verifica) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE ONLY public.w22verifica_data
    ADD CONSTRAINT w22verifica_data_fkey002 FOREIGN KEY (id_w22_zone) REFERENCES public.w22_zone(id_w22_zone) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE ONLY public.w22verifica_data
    ADD CONSTRAINT w22verifica_data_fkey003 FOREIGN KEY (err_crit_tot ) REFERENCES public.w22severita(id_w22severita) ON DELETE CASCADE ON UPDATE CASCADE;

SELECT setval('public.w22verifica_data_id_w22verifica_data_seq', max(id_w22verifica_data)) FROM public.w22verifica_data;

