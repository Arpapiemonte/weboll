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

SET default_with_oids = false;

--
-- Name: regione; Type: TABLE; Schema: public; Owner: weboll; Tablespace: 
--

CREATE TABLE public.regione (
    codice_istat_reg character varying(1) NOT NULL,
    denominazione character varying(40) NOT NULL,
    superficie integer,
    data_agg timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(6) with time zone NOT NULL
);


ALTER TABLE public.regione OWNER TO weboll;

--
-- Name: TABLE regione; Type: COMMENT; Schema: public; Owner: weboll
--

COMMENT ON TABLE public.regione IS 'Elenco delle regioni italiane';


--
-- Data for Name: regione; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.regione (codice_istat_reg, denominazione, superficie, data_agg) FROM stdin;
A	PIEMONTE	\N	2004-07-14 10:29:39
B	VALLE D'AOSTA	\N	2004-07-14 10:29:39
C	LIGURIA	\N	2004-07-14 10:29:39
D	LOMBARDIA	\N	2004-07-14 10:29:39
E	TRENTINO ALTO ADIGE	\N	2004-07-14 10:29:39
F	VENETO	\N	2004-07-14 10:29:39
G	FRIULI VENEZIA GIULIA	\N	2004-07-14 10:29:39
I	EMILIA ROMAGNA	\N	2004-07-14 10:29:39
L	MARCHE	\N	2004-07-14 10:29:39
M	TOSCANA	\N	2004-07-14 10:29:39
N	UMBRIA	\N	2004-07-14 10:29:39
O	LAZIO	\N	2004-07-14 10:29:39
P	CAMPANIA	\N	2004-07-14 10:29:39
Q	ABRUZZI	\N	2004-07-14 10:29:39
R	MOLISE	\N	2004-07-14 10:29:39
S	PUGLIA	\N	2004-07-14 10:29:39
T	BASILICATA	\N	2004-07-14 10:29:39
U	CALABRIA	\N	2004-07-14 10:29:39
V	SICILIA	\N	2004-07-14 10:29:39
Z	SARDEGNA	\N	2004-07-14 10:29:39
\.


--
-- Name: regione_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace: 
--

ALTER TABLE ONLY public.regione
    ADD CONSTRAINT regione_pkey PRIMARY KEY (codice_istat_reg);


--
-- Name: TABLE regione; Type: ACL; Schema: public; Owner: weboll
--



--
-- PostgreSQL database dump complete
--

