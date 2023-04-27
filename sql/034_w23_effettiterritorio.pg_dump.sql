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

--
-- Name: w23_effettiterritorio; Type: TABLE; Schema: public; Owner: weboll; Tablespace:
--

CREATE TABLE public.w23_effettiterritorio (
    id_w23_effettiterritorio character varying(2) NOT NULL,
    descrizione character varying(100)
);


ALTER TABLE public.w23_effettiterritorio OWNER TO weboll;

--
-- Data for Name: w23_effettiterritorio; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.w23_effettiterritorio (id_w23_effettiterritorio, descrizione) FROM stdin;
0	-
11	L'attività valanghiva potrà localmente interessare la viabilità
01	Locali allagamenti ed isolati fenomeni di versante
02	Locali allagamenti, caduta alberi, fulminazioni e isolati fenomeni di versante
03	Allagamenti per transito piene e frane causate dalla pioggia antecedente
04	Possibili disagi alla viabilità
05	Limitate esondazioni dei corsi d'acqua e attivazione fenomeni di versante
06	Allagamenti per transito piene e frane causate dalla pioggia antecedente
07	Disagi alla viabilità e possibili interruzioni nelle forniture dei servizi
08	Estese esondazioni dei corsi d'acqua e diffusi fenomeni di versante
09	Allagamenti per transito piene e frane causate dalla pioggia antecedente
10	Interruzione viabilità, forniture dei servizi e possibili crolli di coperture
\.


--
-- Name: w23_effettiterritorio_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace:
--

ALTER TABLE ONLY public.w23_effettiterritorio
    ADD CONSTRAINT w23_effettiterritorio_pkey PRIMARY KEY (id_w23_effettiterritorio);


--
-- Name: TABLE w23_effettiterritorio; Type: ACL; Schema: public; Owner: weboll
--



--
-- PostgreSQL database dump complete
--

