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


CREATE TABLE public.w23verifica_criticita (
    id_w23_criticita character varying(10) NOT NULL,
    descrizione text,
    colore_html character varying(30) NOT NULL
);


ALTER TABLE public.w23verifica_criticita OWNER TO weboll;


COPY public.w23verifica_criticita (id_w23_criticita, descrizione, colore_html) FROM stdin;
-	N.D	#FFFFFF
VERDE	Assente	#6EBB00
GIALLO	Ordinaria	#FFFF00
ARANCIONE	Moderata	#FFA500
ROSSO	Elevata	#FF0000
\.


ALTER TABLE ONLY public.w23verifica_criticita
    ADD CONSTRAINT w23verifica_criticita_pkey PRIMARY KEY (id_w23_criticita);


--
-- Name: TABLE w23verifica_criticita; Type: ACL; Schema: public; Owner: weboll
--

CREATE TABLE public.w23giudizio (
	id_w23giudizio int8 NOT NULL,
	descrizione text NULL,
	colore_html varchar(30) NOT NULL
);

ALTER TABLE public.w23giudizio OWNER TO weboll;

COPY public.w23giudizio (id_w23giudizio, descrizione, colore_html) FROM stdin;
1	Ottimo	#6EBB00
2	Buono	#6EBB00
3	Sufficiente	#ffff00
4	Insufficiente	#FF0000
5	Pessimo	#8f00ff
\.

ALTER TABLE ONLY public.w23giudizio
    ADD CONSTRAINT id_w23giudizio_pkey PRIMARY KEY (id_w23giudizio);


CREATE TABLE public.w23severita (
	id_w23severita int8 NOT NULL,
	sigla varchar(3) NOT NULL,
	descrizione text NULL,
	colore_html varchar(30) NOT NULL
);

ALTER TABLE public.w23severita OWNER TO weboll;

COPY public.w23severita (id_w23severita, sigla, descrizione, colore_html) FROM stdin;
1	Ok	Assenza di errore	#6EBB00
2	Li	Errore lieve	#ffff00
3	Gr	Errore grave	#FF0000
4	MGr	Errore molto grave	#8f00ff
\.

ALTER TABLE ONLY public.w23severita
    ADD CONSTRAINT id_w23severita_pkey PRIMARY KEY (id_w23severita);


CREATE TABLE public.w23verifica (
	id_w23verifica bigserial NOT NULL,
	id_numero_bollettino varchar(30) NOT NULL,
	numero_bollettino varchar(30) NOT NULL,
	data_emissione date DEFAULT 'now'::text::date NOT NULL,
	data_analisi date DEFAULT 'now'::text::date NOT NULL,
	id_w23giudizio int8 NOT NULL,
	annotazione text NULL,
	situazione_evoluzione text NULL,
	status bpchar(1) DEFAULT 0 NOT NULL,
	last_update timestamp(0) DEFAULT 'now'::text::timestamp(6) with time zone NOT NULL,
	username varchar(30) DEFAULT "current_user"() NOT NULL
);

ALTER TABLE public.w23verifica OWNER TO weboll;

ALTER TABLE ONLY public.w23verifica
    ADD CONSTRAINT w23verifica_pkey PRIMARY KEY (id_w23verifica);

ALTER TABLE ONLY public.w23verifica
    ADD CONSTRAINT w23verifica_fkey001 FOREIGN KEY (id_w23giudizio) REFERENCES public.w23giudizio(id_w23giudizio) ON DELETE CASCADE ON UPDATE CASCADE;

-- CREATE UNIQUE INDEX numero_bollettino_index ON public.w23verifica (numero_bollettino);

-- ALTER TABLE ONLY public.w23verifica
--    ADD CONSTRAINT w23verifica_fkey002 FOREIGN KEY (numero_bollettino) REFERENCES public.w23(numero_bollettino) ON DELETE CASCADE ON UPDATE CASCADE;



CREATE TABLE public.w23verifica_data (
	id_w23verifica int8 NOT NULL,
	id_w23_zone int4 NOT NULL,
	prev_crit_idraulico_oggi varchar(15) NULL,
	oss_crit_idraulico_oggi varchar(15) NULL,
	prev_crit_idraulico_domani varchar(15) NULL,
	oss_crit_idraulico_domani varchar(15) NULL,
	prev_crit_idrogeologico_oggi varchar(15) NULL,
	oss_crit_idrogeologico_oggi varchar(15) NULL,
	prev_crit_idrogeologico_domani varchar(15) NULL,
	oss_crit_idrogeologico_domani varchar(15) NULL,
	prev_crit_temporali_oggi varchar(15) NULL,
	oss_crit_temporali_oggi varchar(15) NULL,
	prev_crit_temporali_domani varchar(15) NULL,
	oss_crit_temporali_domani varchar(15) NULL,
	prev_crit_neve_oggi varchar(15) NULL,
	oss_crit_neve_oggi varchar(15) NULL,
	prev_crit_neve_domani varchar(15) NULL,
	oss_crit_neve_domani varchar(15) NULL,
	prev_crit_valanghe_oggi varchar(15) NULL,
	oss_crit_valanghe_oggi varchar(15) NULL,
	prev_crit_valanghe_domani varchar(15) NULL,
	oss_crit_valanghe_domani varchar(15) NULL,
	prev_crit_tot varchar(15) NULL,
	oss_crit_tot varchar(15) NULL,
	err_crit_tot int8 NOT NULL,
	prev_crit_oggi varchar(15) NULL,
	oss_crit_oggi varchar(15) NULL,
	err_crit_oggi int8 NOT NULL,
	prev_crit_domani varchar(15) NULL,
	oss_crit_domani varchar(15) NULL,
	err_crit_domani int8 NOT NULL,
	id_w23verifica_data bigserial NOT NULL
);


ALTER TABLE public.w23verifica_data OWNER TO weboll;

--ALTER TABLE ONLY public.w23verifica_data
--    ADD CONSTRAINT w23verifica_data_pkey PRIMARY KEY (id_w23verifica_data);

ALTER TABLE ONLY public.w23verifica_data
    ADD CONSTRAINT w23verifica_data_fkey001 FOREIGN KEY (id_w23verifica) REFERENCES public.w23verifica(id_w23verifica) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE ONLY public.w23verifica_data
    ADD CONSTRAINT w23verifica_data_fkey002 FOREIGN KEY (id_w23_zone) REFERENCES public.w23_zone(id_w23_zone) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE ONLY public.w23verifica_data
    ADD CONSTRAINT w23verifica_data_fkey003 FOREIGN KEY (err_crit_tot) REFERENCES public.w23severita(id_w23severita) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE ONLY public.w23verifica_data
    ADD CONSTRAINT w23verifica_data_fkey004 FOREIGN KEY (err_crit_oggi) REFERENCES public.w23severita(id_w23severita) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE ONLY public.w23verifica_data
    ADD CONSTRAINT w23verifica_data_fkey005 FOREIGN KEY (err_crit_domani) REFERENCES public.w23severita(id_w23severita) ON DELETE CASCADE ON UPDATE CASCADE;

INSERT INTO public.w23verifica
(id_w23verifica, id_numero_bollettino, numero_bollettino, data_emissione, data_analisi, id_w23giudizio, annotazione, situazione_evoluzione, status, last_update, username)
VALUES(35, '336_2024', '336/2024', '2023-02-16', '2023-02-18', 1, NULL, NULL, '1', '2023-02-18 14:19:47.000', 'weboll');
INSERT INTO public.w23verifica
(id_w23verifica, id_numero_bollettino, numero_bollettino, data_emissione, data_analisi, id_w23giudizio, annotazione, situazione_evoluzione, status, last_update, username)
VALUES(36, '337_2024', '337/2024', '2023-02-17', '2023-02-21', 1, NULL, NULL, '1', '2023-02-21 10:09:17.000', 'weboll');
INSERT INTO public.w23verifica
(id_w23verifica, id_numero_bollettino, numero_bollettino, data_emissione, data_analisi, id_w23giudizio, annotazione, situazione_evoluzione, status, last_update, username)
VALUES(34, '335_2024', '335/2024', '2023-02-15', '2023-02-17', 1, NULL, NULL, '1', '2023-02-17 10:24:23.000', 'weboll');


INSERT INTO public.w23verifica_data
(id_w23verifica, id_w23_zone, prev_crit_idraulico_oggi, oss_crit_idraulico_oggi,prev_crit_idraulico_domani, oss_crit_idraulico_domani, prev_crit_neve_oggi, oss_crit_neve_oggi,prev_crit_neve_domani, oss_crit_neve_domani,prev_crit_valanghe_oggi, oss_crit_valanghe_oggi,prev_crit_valanghe_domani, oss_crit_valanghe_domani,prev_crit_idrogeologico_oggi, oss_crit_idrogeologico_oggi,prev_crit_idrogeologico_domani, oss_crit_idrogeologico_domani,prev_crit_temporali_oggi, oss_crit_temporali_oggi,prev_crit_temporali_domani, oss_crit_temporali_domani, prev_crit_tot, oss_crit_tot, err_crit_tot, prev_crit_oggi, oss_crit_oggi, err_crit_oggi, prev_crit_domani, oss_crit_domani, err_crit_domani, id_w23verifica_data)
VALUES(35, 1, '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-','VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 189);
INSERT INTO public.w23verifica_data
(id_w23verifica, id_w23_zone, prev_crit_idraulico_oggi, oss_crit_idraulico_oggi,prev_crit_idraulico_domani, oss_crit_idraulico_domani, prev_crit_neve_oggi, oss_crit_neve_oggi,prev_crit_neve_domani, oss_crit_neve_domani,prev_crit_valanghe_oggi, oss_crit_valanghe_oggi,prev_crit_valanghe_domani, oss_crit_valanghe_domani,prev_crit_idrogeologico_oggi, oss_crit_idrogeologico_oggi,prev_crit_idrogeologico_domani, oss_crit_idrogeologico_domani,prev_crit_temporali_oggi, oss_crit_temporali_oggi,prev_crit_temporali_domani, oss_crit_temporali_domani, prev_crit_tot, oss_crit_tot, err_crit_tot, prev_crit_oggi, oss_crit_oggi, err_crit_oggi, prev_crit_domani, oss_crit_domani, err_crit_domani, id_w23verifica_data)
VALUES(35, 2, '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-','VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 190);
INSERT INTO public.w23verifica_data
(id_w23verifica, id_w23_zone, prev_crit_idraulico_oggi, oss_crit_idraulico_oggi,prev_crit_idraulico_domani, oss_crit_idraulico_domani, prev_crit_neve_oggi, oss_crit_neve_oggi,prev_crit_neve_domani, oss_crit_neve_domani,prev_crit_valanghe_oggi, oss_crit_valanghe_oggi,prev_crit_valanghe_domani, oss_crit_valanghe_domani,prev_crit_idrogeologico_oggi, oss_crit_idrogeologico_oggi,prev_crit_idrogeologico_domani, oss_crit_idrogeologico_domani,prev_crit_temporali_oggi, oss_crit_temporali_oggi,prev_crit_temporali_domani, oss_crit_temporali_domani, prev_crit_tot, oss_crit_tot, err_crit_tot, prev_crit_oggi, oss_crit_oggi, err_crit_oggi, prev_crit_domani, oss_crit_domani, err_crit_domani, id_w23verifica_data)
VALUES(35, 3, '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-','VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 191);
INSERT INTO public.w23verifica_data
(id_w23verifica, id_w23_zone, prev_crit_idraulico_oggi, oss_crit_idraulico_oggi,prev_crit_idraulico_domani, oss_crit_idraulico_domani, prev_crit_neve_oggi, oss_crit_neve_oggi,prev_crit_neve_domani, oss_crit_neve_domani,prev_crit_valanghe_oggi, oss_crit_valanghe_oggi,prev_crit_valanghe_domani, oss_crit_valanghe_domani,prev_crit_idrogeologico_oggi, oss_crit_idrogeologico_oggi,prev_crit_idrogeologico_domani, oss_crit_idrogeologico_domani,prev_crit_temporali_oggi, oss_crit_temporali_oggi,prev_crit_temporali_domani, oss_crit_temporali_domani, prev_crit_tot, oss_crit_tot, err_crit_tot, prev_crit_oggi, oss_crit_oggi, err_crit_oggi, prev_crit_domani, oss_crit_domani, err_crit_domani, id_w23verifica_data)
VALUES(35, 4, '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-','VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 192);
INSERT INTO public.w23verifica_data
(id_w23verifica, id_w23_zone, prev_crit_idraulico_oggi, oss_crit_idraulico_oggi,prev_crit_idraulico_domani, oss_crit_idraulico_domani, prev_crit_neve_oggi, oss_crit_neve_oggi,prev_crit_neve_domani, oss_crit_neve_domani,prev_crit_valanghe_oggi, oss_crit_valanghe_oggi,prev_crit_valanghe_domani, oss_crit_valanghe_domani,prev_crit_idrogeologico_oggi, oss_crit_idrogeologico_oggi,prev_crit_idrogeologico_domani, oss_crit_idrogeologico_domani,prev_crit_temporali_oggi, oss_crit_temporali_oggi,prev_crit_temporali_domani, oss_crit_temporali_domani, prev_crit_tot, oss_crit_tot, err_crit_tot, prev_crit_oggi, oss_crit_oggi, err_crit_oggi, prev_crit_domani, oss_crit_domani, err_crit_domani, id_w23verifica_data)
VALUES(35, 5, '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-','VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 193);
INSERT INTO public.w23verifica_data
(id_w23verifica, id_w23_zone, prev_crit_idraulico_oggi, oss_crit_idraulico_oggi,prev_crit_idraulico_domani, oss_crit_idraulico_domani, prev_crit_neve_oggi, oss_crit_neve_oggi,prev_crit_neve_domani, oss_crit_neve_domani,prev_crit_valanghe_oggi, oss_crit_valanghe_oggi,prev_crit_valanghe_domani, oss_crit_valanghe_domani,prev_crit_idrogeologico_oggi, oss_crit_idrogeologico_oggi,prev_crit_idrogeologico_domani, oss_crit_idrogeologico_domani,prev_crit_temporali_oggi, oss_crit_temporali_oggi,prev_crit_temporali_domani, oss_crit_temporali_domani, prev_crit_tot, oss_crit_tot, err_crit_tot, prev_crit_oggi, oss_crit_oggi, err_crit_oggi, prev_crit_domani, oss_crit_domani, err_crit_domani, id_w23verifica_data)
VALUES(35, 6, '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-','VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 194);
INSERT INTO public.w23verifica_data
(id_w23verifica, id_w23_zone, prev_crit_idraulico_oggi, oss_crit_idraulico_oggi,prev_crit_idraulico_domani, oss_crit_idraulico_domani, prev_crit_neve_oggi, oss_crit_neve_oggi,prev_crit_neve_domani, oss_crit_neve_domani,prev_crit_valanghe_oggi, oss_crit_valanghe_oggi,prev_crit_valanghe_domani, oss_crit_valanghe_domani,prev_crit_idrogeologico_oggi, oss_crit_idrogeologico_oggi,prev_crit_idrogeologico_domani, oss_crit_idrogeologico_domani,prev_crit_temporali_oggi, oss_crit_temporali_oggi,prev_crit_temporali_domani, oss_crit_temporali_domani, prev_crit_tot, oss_crit_tot, err_crit_tot, prev_crit_oggi, oss_crit_oggi, err_crit_oggi, prev_crit_domani, oss_crit_domani, err_crit_domani, id_w23verifica_data)
VALUES(35, 7, '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-','VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 195);
INSERT INTO public.w23verifica_data
(id_w23verifica, id_w23_zone, prev_crit_idraulico_oggi, oss_crit_idraulico_oggi,prev_crit_idraulico_domani, oss_crit_idraulico_domani, prev_crit_neve_oggi, oss_crit_neve_oggi,prev_crit_neve_domani, oss_crit_neve_domani,prev_crit_valanghe_oggi, oss_crit_valanghe_oggi,prev_crit_valanghe_domani, oss_crit_valanghe_domani,prev_crit_idrogeologico_oggi, oss_crit_idrogeologico_oggi,prev_crit_idrogeologico_domani, oss_crit_idrogeologico_domani,prev_crit_temporali_oggi, oss_crit_temporali_oggi,prev_crit_temporali_domani, oss_crit_temporali_domani, prev_crit_tot, oss_crit_tot, err_crit_tot, prev_crit_oggi, oss_crit_oggi, err_crit_oggi, prev_crit_domani, oss_crit_domani, err_crit_domani, id_w23verifica_data)
VALUES(35, 8, '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-','VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 196);
INSERT INTO public.w23verifica_data
(id_w23verifica, id_w23_zone, prev_crit_idraulico_oggi, oss_crit_idraulico_oggi,prev_crit_idraulico_domani, oss_crit_idraulico_domani, prev_crit_neve_oggi, oss_crit_neve_oggi,prev_crit_neve_domani, oss_crit_neve_domani,prev_crit_valanghe_oggi, oss_crit_valanghe_oggi,prev_crit_valanghe_domani, oss_crit_valanghe_domani,prev_crit_idrogeologico_oggi, oss_crit_idrogeologico_oggi,prev_crit_idrogeologico_domani, oss_crit_idrogeologico_domani,prev_crit_temporali_oggi, oss_crit_temporali_oggi,prev_crit_temporali_domani, oss_crit_temporali_domani, prev_crit_tot, oss_crit_tot, err_crit_tot, prev_crit_oggi, oss_crit_oggi, err_crit_oggi, prev_crit_domani, oss_crit_domani, err_crit_domani, id_w23verifica_data)
VALUES(35, 9, '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-','VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 197);
INSERT INTO public.w23verifica_data
(id_w23verifica, id_w23_zone, prev_crit_idraulico_oggi, oss_crit_idraulico_oggi,prev_crit_idraulico_domani, oss_crit_idraulico_domani, prev_crit_neve_oggi, oss_crit_neve_oggi,prev_crit_neve_domani, oss_crit_neve_domani,prev_crit_valanghe_oggi, oss_crit_valanghe_oggi,prev_crit_valanghe_domani, oss_crit_valanghe_domani,prev_crit_idrogeologico_oggi, oss_crit_idrogeologico_oggi,prev_crit_idrogeologico_domani, oss_crit_idrogeologico_domani,prev_crit_temporali_oggi, oss_crit_temporali_oggi,prev_crit_temporali_domani, oss_crit_temporali_domani, prev_crit_tot, oss_crit_tot, err_crit_tot, prev_crit_oggi, oss_crit_oggi, err_crit_oggi, prev_crit_domani, oss_crit_domani, err_crit_domani, id_w23verifica_data)
VALUES(35, 10, '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-','VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 198);
INSERT INTO public.w23verifica_data
(id_w23verifica, id_w23_zone, prev_crit_idraulico_oggi, oss_crit_idraulico_oggi,prev_crit_idraulico_domani, oss_crit_idraulico_domani, prev_crit_neve_oggi, oss_crit_neve_oggi,prev_crit_neve_domani, oss_crit_neve_domani,prev_crit_valanghe_oggi, oss_crit_valanghe_oggi,prev_crit_valanghe_domani, oss_crit_valanghe_domani,prev_crit_idrogeologico_oggi, oss_crit_idrogeologico_oggi,prev_crit_idrogeologico_domani, oss_crit_idrogeologico_domani,prev_crit_temporali_oggi, oss_crit_temporali_oggi,prev_crit_temporali_domani, oss_crit_temporali_domani, prev_crit_tot, oss_crit_tot, err_crit_tot, prev_crit_oggi, oss_crit_oggi, err_crit_oggi, prev_crit_domani, oss_crit_domani, err_crit_domani, id_w23verifica_data)
VALUES(35, 11, '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-','VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 199);
INSERT INTO public.w23verifica_data
(id_w23verifica, id_w23_zone, prev_crit_idraulico_oggi, oss_crit_idraulico_oggi,prev_crit_idraulico_domani, oss_crit_idraulico_domani, prev_crit_neve_oggi, oss_crit_neve_oggi,prev_crit_neve_domani, oss_crit_neve_domani,prev_crit_valanghe_oggi, oss_crit_valanghe_oggi,prev_crit_valanghe_domani, oss_crit_valanghe_domani,prev_crit_idrogeologico_oggi, oss_crit_idrogeologico_oggi,prev_crit_idrogeologico_domani, oss_crit_idrogeologico_domani,prev_crit_temporali_oggi, oss_crit_temporali_oggi,prev_crit_temporali_domani, oss_crit_temporali_domani, prev_crit_tot, oss_crit_tot, err_crit_tot, prev_crit_oggi, oss_crit_oggi, err_crit_oggi, prev_crit_domani, oss_crit_domani, err_crit_domani, id_w23verifica_data)
VALUES(36, 1, '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-','VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 200);
INSERT INTO public.w23verifica_data
(id_w23verifica, id_w23_zone, prev_crit_idraulico_oggi, oss_crit_idraulico_oggi,prev_crit_idraulico_domani, oss_crit_idraulico_domani, prev_crit_neve_oggi, oss_crit_neve_oggi,prev_crit_neve_domani, oss_crit_neve_domani,prev_crit_valanghe_oggi, oss_crit_valanghe_oggi,prev_crit_valanghe_domani, oss_crit_valanghe_domani,prev_crit_idrogeologico_oggi, oss_crit_idrogeologico_oggi,prev_crit_idrogeologico_domani, oss_crit_idrogeologico_domani,prev_crit_temporali_oggi, oss_crit_temporali_oggi,prev_crit_temporali_domani, oss_crit_temporali_domani, prev_crit_tot, oss_crit_tot, err_crit_tot, prev_crit_oggi, oss_crit_oggi, err_crit_oggi, prev_crit_domani, oss_crit_domani, err_crit_domani, id_w23verifica_data)
VALUES(36, 2, '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-','VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 201);
INSERT INTO public.w23verifica_data
(id_w23verifica, id_w23_zone, prev_crit_idraulico_oggi, oss_crit_idraulico_oggi,prev_crit_idraulico_domani, oss_crit_idraulico_domani, prev_crit_neve_oggi, oss_crit_neve_oggi,prev_crit_neve_domani, oss_crit_neve_domani,prev_crit_valanghe_oggi, oss_crit_valanghe_oggi,prev_crit_valanghe_domani, oss_crit_valanghe_domani,prev_crit_idrogeologico_oggi, oss_crit_idrogeologico_oggi,prev_crit_idrogeologico_domani, oss_crit_idrogeologico_domani,prev_crit_temporali_oggi, oss_crit_temporali_oggi,prev_crit_temporali_domani, oss_crit_temporali_domani, prev_crit_tot, oss_crit_tot, err_crit_tot, prev_crit_oggi, oss_crit_oggi, err_crit_oggi, prev_crit_domani, oss_crit_domani, err_crit_domani, id_w23verifica_data)
VALUES(36, 3, '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-','VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 202);
INSERT INTO public.w23verifica_data
(id_w23verifica, id_w23_zone, prev_crit_idraulico_oggi, oss_crit_idraulico_oggi,prev_crit_idraulico_domani, oss_crit_idraulico_domani, prev_crit_neve_oggi, oss_crit_neve_oggi,prev_crit_neve_domani, oss_crit_neve_domani,prev_crit_valanghe_oggi, oss_crit_valanghe_oggi,prev_crit_valanghe_domani, oss_crit_valanghe_domani,prev_crit_idrogeologico_oggi, oss_crit_idrogeologico_oggi,prev_crit_idrogeologico_domani, oss_crit_idrogeologico_domani,prev_crit_temporali_oggi, oss_crit_temporali_oggi,prev_crit_temporali_domani, oss_crit_temporali_domani, prev_crit_tot, oss_crit_tot, err_crit_tot, prev_crit_oggi, oss_crit_oggi, err_crit_oggi, prev_crit_domani, oss_crit_domani, err_crit_domani, id_w23verifica_data)
VALUES(36, 4, '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-','VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 203);
INSERT INTO public.w23verifica_data
(id_w23verifica, id_w23_zone, prev_crit_idraulico_oggi, oss_crit_idraulico_oggi,prev_crit_idraulico_domani, oss_crit_idraulico_domani, prev_crit_neve_oggi, oss_crit_neve_oggi,prev_crit_neve_domani, oss_crit_neve_domani,prev_crit_valanghe_oggi, oss_crit_valanghe_oggi,prev_crit_valanghe_domani, oss_crit_valanghe_domani,prev_crit_idrogeologico_oggi, oss_crit_idrogeologico_oggi,prev_crit_idrogeologico_domani, oss_crit_idrogeologico_domani,prev_crit_temporali_oggi, oss_crit_temporali_oggi,prev_crit_temporali_domani, oss_crit_temporali_domani, prev_crit_tot, oss_crit_tot, err_crit_tot, prev_crit_oggi, oss_crit_oggi, err_crit_oggi, prev_crit_domani, oss_crit_domani, err_crit_domani, id_w23verifica_data)
VALUES(36, 5, '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-','VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 204);
INSERT INTO public.w23verifica_data
(id_w23verifica, id_w23_zone, prev_crit_idraulico_oggi, oss_crit_idraulico_oggi,prev_crit_idraulico_domani, oss_crit_idraulico_domani, prev_crit_neve_oggi, oss_crit_neve_oggi,prev_crit_neve_domani, oss_crit_neve_domani,prev_crit_valanghe_oggi, oss_crit_valanghe_oggi,prev_crit_valanghe_domani, oss_crit_valanghe_domani,prev_crit_idrogeologico_oggi, oss_crit_idrogeologico_oggi,prev_crit_idrogeologico_domani, oss_crit_idrogeologico_domani,prev_crit_temporali_oggi, oss_crit_temporali_oggi,prev_crit_temporali_domani, oss_crit_temporali_domani, prev_crit_tot, oss_crit_tot, err_crit_tot, prev_crit_oggi, oss_crit_oggi, err_crit_oggi, prev_crit_domani, oss_crit_domani, err_crit_domani, id_w23verifica_data)
VALUES(36, 6, '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-','VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 205);
INSERT INTO public.w23verifica_data
(id_w23verifica, id_w23_zone, prev_crit_idraulico_oggi, oss_crit_idraulico_oggi,prev_crit_idraulico_domani, oss_crit_idraulico_domani, prev_crit_neve_oggi, oss_crit_neve_oggi,prev_crit_neve_domani, oss_crit_neve_domani,prev_crit_valanghe_oggi, oss_crit_valanghe_oggi,prev_crit_valanghe_domani, oss_crit_valanghe_domani,prev_crit_idrogeologico_oggi, oss_crit_idrogeologico_oggi,prev_crit_idrogeologico_domani, oss_crit_idrogeologico_domani,prev_crit_temporali_oggi, oss_crit_temporali_oggi,prev_crit_temporali_domani, oss_crit_temporali_domani, prev_crit_tot, oss_crit_tot, err_crit_tot, prev_crit_oggi, oss_crit_oggi, err_crit_oggi, prev_crit_domani, oss_crit_domani, err_crit_domani, id_w23verifica_data)
VALUES(36, 7, '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-','VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 206);
INSERT INTO public.w23verifica_data
(id_w23verifica, id_w23_zone, prev_crit_idraulico_oggi, oss_crit_idraulico_oggi,prev_crit_idraulico_domani, oss_crit_idraulico_domani, prev_crit_neve_oggi, oss_crit_neve_oggi,prev_crit_neve_domani, oss_crit_neve_domani,prev_crit_valanghe_oggi, oss_crit_valanghe_oggi,prev_crit_valanghe_domani, oss_crit_valanghe_domani,prev_crit_idrogeologico_oggi, oss_crit_idrogeologico_oggi,prev_crit_idrogeologico_domani, oss_crit_idrogeologico_domani,prev_crit_temporali_oggi, oss_crit_temporali_oggi,prev_crit_temporali_domani, oss_crit_temporali_domani, prev_crit_tot, oss_crit_tot, err_crit_tot, prev_crit_oggi, oss_crit_oggi, err_crit_oggi, prev_crit_domani, oss_crit_domani, err_crit_domani, id_w23verifica_data)
VALUES(36, 8, '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-','VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 207);
INSERT INTO public.w23verifica_data
(id_w23verifica, id_w23_zone, prev_crit_idraulico_oggi, oss_crit_idraulico_oggi,prev_crit_idraulico_domani, oss_crit_idraulico_domani, prev_crit_neve_oggi, oss_crit_neve_oggi,prev_crit_neve_domani, oss_crit_neve_domani,prev_crit_valanghe_oggi, oss_crit_valanghe_oggi,prev_crit_valanghe_domani, oss_crit_valanghe_domani,prev_crit_idrogeologico_oggi, oss_crit_idrogeologico_oggi,prev_crit_idrogeologico_domani, oss_crit_idrogeologico_domani,prev_crit_temporali_oggi, oss_crit_temporali_oggi,prev_crit_temporali_domani, oss_crit_temporali_domani, prev_crit_tot, oss_crit_tot, err_crit_tot, prev_crit_oggi, oss_crit_oggi, err_crit_oggi, prev_crit_domani, oss_crit_domani, err_crit_domani, id_w23verifica_data)
VALUES(36, 9, '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-','VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 208);
INSERT INTO public.w23verifica_data
(id_w23verifica, id_w23_zone, prev_crit_idraulico_oggi, oss_crit_idraulico_oggi,prev_crit_idraulico_domani, oss_crit_idraulico_domani, prev_crit_neve_oggi, oss_crit_neve_oggi,prev_crit_neve_domani, oss_crit_neve_domani,prev_crit_valanghe_oggi, oss_crit_valanghe_oggi,prev_crit_valanghe_domani, oss_crit_valanghe_domani,prev_crit_idrogeologico_oggi, oss_crit_idrogeologico_oggi,prev_crit_idrogeologico_domani, oss_crit_idrogeologico_domani,prev_crit_temporali_oggi, oss_crit_temporali_oggi,prev_crit_temporali_domani, oss_crit_temporali_domani, prev_crit_tot, oss_crit_tot, err_crit_tot, prev_crit_oggi, oss_crit_oggi, err_crit_oggi, prev_crit_domani, oss_crit_domani, err_crit_domani, id_w23verifica_data)
VALUES(36, 10, '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-','VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 209);
INSERT INTO public.w23verifica_data
(id_w23verifica, id_w23_zone, prev_crit_idraulico_oggi, oss_crit_idraulico_oggi,prev_crit_idraulico_domani, oss_crit_idraulico_domani, prev_crit_neve_oggi, oss_crit_neve_oggi,prev_crit_neve_domani, oss_crit_neve_domani,prev_crit_valanghe_oggi, oss_crit_valanghe_oggi,prev_crit_valanghe_domani, oss_crit_valanghe_domani,prev_crit_idrogeologico_oggi, oss_crit_idrogeologico_oggi,prev_crit_idrogeologico_domani, oss_crit_idrogeologico_domani,prev_crit_temporali_oggi, oss_crit_temporali_oggi,prev_crit_temporali_domani, oss_crit_temporali_domani, prev_crit_tot, oss_crit_tot, err_crit_tot, prev_crit_oggi, oss_crit_oggi, err_crit_oggi, prev_crit_domani, oss_crit_domani, err_crit_domani, id_w23verifica_data)
VALUES(36, 11, '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-','VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 210);
INSERT INTO public.w23verifica_data
(id_w23verifica, id_w23_zone, prev_crit_idraulico_oggi, oss_crit_idraulico_oggi,prev_crit_idraulico_domani, oss_crit_idraulico_domani, prev_crit_neve_oggi, oss_crit_neve_oggi,prev_crit_neve_domani, oss_crit_neve_domani,prev_crit_valanghe_oggi, oss_crit_valanghe_oggi,prev_crit_valanghe_domani, oss_crit_valanghe_domani,prev_crit_idrogeologico_oggi, oss_crit_idrogeologico_oggi,prev_crit_idrogeologico_domani, oss_crit_idrogeologico_domani,prev_crit_temporali_oggi, oss_crit_temporali_oggi,prev_crit_temporali_domani, oss_crit_temporali_domani, prev_crit_tot, oss_crit_tot, err_crit_tot, prev_crit_oggi, oss_crit_oggi, err_crit_oggi, prev_crit_domani, oss_crit_domani, err_crit_domani, id_w23verifica_data)
VALUES(34, 1, '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-','VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 178);
INSERT INTO public.w23verifica_data
(id_w23verifica, id_w23_zone, prev_crit_idraulico_oggi, oss_crit_idraulico_oggi,prev_crit_idraulico_domani, oss_crit_idraulico_domani, prev_crit_neve_oggi, oss_crit_neve_oggi,prev_crit_neve_domani, oss_crit_neve_domani,prev_crit_valanghe_oggi, oss_crit_valanghe_oggi,prev_crit_valanghe_domani, oss_crit_valanghe_domani,prev_crit_idrogeologico_oggi, oss_crit_idrogeologico_oggi,prev_crit_idrogeologico_domani, oss_crit_idrogeologico_domani,prev_crit_temporali_oggi, oss_crit_temporali_oggi,prev_crit_temporali_domani, oss_crit_temporali_domani, prev_crit_tot, oss_crit_tot, err_crit_tot, prev_crit_oggi, oss_crit_oggi, err_crit_oggi, prev_crit_domani, oss_crit_domani, err_crit_domani, id_w23verifica_data)
VALUES(34, 2, '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-','VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 179);
INSERT INTO public.w23verifica_data
(id_w23verifica, id_w23_zone, prev_crit_idraulico_oggi, oss_crit_idraulico_oggi,prev_crit_idraulico_domani, oss_crit_idraulico_domani, prev_crit_neve_oggi, oss_crit_neve_oggi,prev_crit_neve_domani, oss_crit_neve_domani,prev_crit_valanghe_oggi, oss_crit_valanghe_oggi,prev_crit_valanghe_domani, oss_crit_valanghe_domani,prev_crit_idrogeologico_oggi, oss_crit_idrogeologico_oggi,prev_crit_idrogeologico_domani, oss_crit_idrogeologico_domani,prev_crit_temporali_oggi, oss_crit_temporali_oggi,prev_crit_temporali_domani, oss_crit_temporali_domani, prev_crit_tot, oss_crit_tot, err_crit_tot, prev_crit_oggi, oss_crit_oggi, err_crit_oggi, prev_crit_domani, oss_crit_domani, err_crit_domani, id_w23verifica_data)
VALUES(34, 3, '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-','VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 180);
INSERT INTO public.w23verifica_data
(id_w23verifica, id_w23_zone, prev_crit_idraulico_oggi, oss_crit_idraulico_oggi,prev_crit_idraulico_domani, oss_crit_idraulico_domani, prev_crit_neve_oggi, oss_crit_neve_oggi,prev_crit_neve_domani, oss_crit_neve_domani,prev_crit_valanghe_oggi, oss_crit_valanghe_oggi,prev_crit_valanghe_domani, oss_crit_valanghe_domani,prev_crit_idrogeologico_oggi, oss_crit_idrogeologico_oggi,prev_crit_idrogeologico_domani, oss_crit_idrogeologico_domani,prev_crit_temporali_oggi, oss_crit_temporali_oggi,prev_crit_temporali_domani, oss_crit_temporali_domani, prev_crit_tot, oss_crit_tot, err_crit_tot, prev_crit_oggi, oss_crit_oggi, err_crit_oggi, prev_crit_domani, oss_crit_domani, err_crit_domani, id_w23verifica_data)
VALUES(34, 4, '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-','VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 181);
INSERT INTO public.w23verifica_data
(id_w23verifica, id_w23_zone, prev_crit_idraulico_oggi, oss_crit_idraulico_oggi,prev_crit_idraulico_domani, oss_crit_idraulico_domani, prev_crit_neve_oggi, oss_crit_neve_oggi,prev_crit_neve_domani, oss_crit_neve_domani,prev_crit_valanghe_oggi, oss_crit_valanghe_oggi,prev_crit_valanghe_domani, oss_crit_valanghe_domani,prev_crit_idrogeologico_oggi, oss_crit_idrogeologico_oggi,prev_crit_idrogeologico_domani, oss_crit_idrogeologico_domani,prev_crit_temporali_oggi, oss_crit_temporali_oggi,prev_crit_temporali_domani, oss_crit_temporali_domani, prev_crit_tot, oss_crit_tot, err_crit_tot, prev_crit_oggi, oss_crit_oggi, err_crit_oggi, prev_crit_domani, oss_crit_domani, err_crit_domani, id_w23verifica_data)
VALUES(34, 5, '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-','VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 182);
INSERT INTO public.w23verifica_data
(id_w23verifica, id_w23_zone, prev_crit_idraulico_oggi, oss_crit_idraulico_oggi,prev_crit_idraulico_domani, oss_crit_idraulico_domani, prev_crit_neve_oggi, oss_crit_neve_oggi,prev_crit_neve_domani, oss_crit_neve_domani,prev_crit_valanghe_oggi, oss_crit_valanghe_oggi,prev_crit_valanghe_domani, oss_crit_valanghe_domani,prev_crit_idrogeologico_oggi, oss_crit_idrogeologico_oggi,prev_crit_idrogeologico_domani, oss_crit_idrogeologico_domani,prev_crit_temporali_oggi, oss_crit_temporali_oggi,prev_crit_temporali_domani, oss_crit_temporali_domani, prev_crit_tot, oss_crit_tot, err_crit_tot, prev_crit_oggi, oss_crit_oggi, err_crit_oggi, prev_crit_domani, oss_crit_domani, err_crit_domani, id_w23verifica_data)
VALUES(34, 6, '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-','VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 183);
INSERT INTO public.w23verifica_data
(id_w23verifica, id_w23_zone, prev_crit_idraulico_oggi, oss_crit_idraulico_oggi,prev_crit_idraulico_domani, oss_crit_idraulico_domani, prev_crit_neve_oggi, oss_crit_neve_oggi,prev_crit_neve_domani, oss_crit_neve_domani,prev_crit_valanghe_oggi, oss_crit_valanghe_oggi,prev_crit_valanghe_domani, oss_crit_valanghe_domani,prev_crit_idrogeologico_oggi, oss_crit_idrogeologico_oggi,prev_crit_idrogeologico_domani, oss_crit_idrogeologico_domani,prev_crit_temporali_oggi, oss_crit_temporali_oggi,prev_crit_temporali_domani, oss_crit_temporali_domani, prev_crit_tot, oss_crit_tot, err_crit_tot, prev_crit_oggi, oss_crit_oggi, err_crit_oggi, prev_crit_domani, oss_crit_domani, err_crit_domani, id_w23verifica_data)
VALUES(34, 7, '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-','VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 184);
INSERT INTO public.w23verifica_data
(id_w23verifica, id_w23_zone, prev_crit_idraulico_oggi, oss_crit_idraulico_oggi,prev_crit_idraulico_domani, oss_crit_idraulico_domani, prev_crit_neve_oggi, oss_crit_neve_oggi,prev_crit_neve_domani, oss_crit_neve_domani,prev_crit_valanghe_oggi, oss_crit_valanghe_oggi,prev_crit_valanghe_domani, oss_crit_valanghe_domani,prev_crit_idrogeologico_oggi, oss_crit_idrogeologico_oggi,prev_crit_idrogeologico_domani, oss_crit_idrogeologico_domani,prev_crit_temporali_oggi, oss_crit_temporali_oggi,prev_crit_temporali_domani, oss_crit_temporali_domani, prev_crit_tot, oss_crit_tot, err_crit_tot, prev_crit_oggi, oss_crit_oggi, err_crit_oggi, prev_crit_domani, oss_crit_domani, err_crit_domani, id_w23verifica_data)
VALUES(34, 8, '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-','VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 185);
INSERT INTO public.w23verifica_data
(id_w23verifica, id_w23_zone, prev_crit_idraulico_oggi, oss_crit_idraulico_oggi,prev_crit_idraulico_domani, oss_crit_idraulico_domani, prev_crit_neve_oggi, oss_crit_neve_oggi,prev_crit_neve_domani, oss_crit_neve_domani,prev_crit_valanghe_oggi, oss_crit_valanghe_oggi,prev_crit_valanghe_domani, oss_crit_valanghe_domani,prev_crit_idrogeologico_oggi, oss_crit_idrogeologico_oggi,prev_crit_idrogeologico_domani, oss_crit_idrogeologico_domani,prev_crit_temporali_oggi, oss_crit_temporali_oggi,prev_crit_temporali_domani, oss_crit_temporali_domani, prev_crit_tot, oss_crit_tot, err_crit_tot, prev_crit_oggi, oss_crit_oggi, err_crit_oggi, prev_crit_domani, oss_crit_domani, err_crit_domani, id_w23verifica_data)
VALUES(34, 9, '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-','VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 186);
INSERT INTO public.w23verifica_data
(id_w23verifica, id_w23_zone, prev_crit_idraulico_oggi, oss_crit_idraulico_oggi,prev_crit_idraulico_domani, oss_crit_idraulico_domani, prev_crit_neve_oggi, oss_crit_neve_oggi,prev_crit_neve_domani, oss_crit_neve_domani,prev_crit_valanghe_oggi, oss_crit_valanghe_oggi,prev_crit_valanghe_domani, oss_crit_valanghe_domani,prev_crit_idrogeologico_oggi, oss_crit_idrogeologico_oggi,prev_crit_idrogeologico_domani, oss_crit_idrogeologico_domani,prev_crit_temporali_oggi, oss_crit_temporali_oggi,prev_crit_temporali_domani, oss_crit_temporali_domani, prev_crit_tot, oss_crit_tot, err_crit_tot, prev_crit_oggi, oss_crit_oggi, err_crit_oggi, prev_crit_domani, oss_crit_domani, err_crit_domani, id_w23verifica_data)
VALUES(34, 10, '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-','VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 187);
INSERT INTO public.w23verifica_data
(id_w23verifica, id_w23_zone, prev_crit_idraulico_oggi, oss_crit_idraulico_oggi,prev_crit_idraulico_domani, oss_crit_idraulico_domani, prev_crit_neve_oggi, oss_crit_neve_oggi,prev_crit_neve_domani, oss_crit_neve_domani,prev_crit_valanghe_oggi, oss_crit_valanghe_oggi,prev_crit_valanghe_domani, oss_crit_valanghe_domani,prev_crit_idrogeologico_oggi, oss_crit_idrogeologico_oggi,prev_crit_idrogeologico_domani, oss_crit_idrogeologico_domani,prev_crit_temporali_oggi, oss_crit_temporali_oggi,prev_crit_temporali_domani, oss_crit_temporali_domani, prev_crit_tot, oss_crit_tot, err_crit_tot, prev_crit_oggi, oss_crit_oggi, err_crit_oggi, prev_crit_domani, oss_crit_domani, err_crit_domani, id_w23verifica_data)
VALUES(34, 11, '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-','VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 'VERDE', 'VERDE', 1, 188);

