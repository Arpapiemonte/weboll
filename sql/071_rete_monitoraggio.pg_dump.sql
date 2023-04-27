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
-- Name: rete_monitoraggio; Type: TABLE; Schema: public; Owner: weboll; Tablespace: 
--

CREATE TABLE public.rete_monitoraggio (
    id_rete_monit character varying(2) NOT NULL,
    denominazione character varying(100) NOT NULL,
    data_validita date DEFAULT ('now'::text)::date NOT NULL,
    data_agg date DEFAULT ('now'::text)::date NOT NULL,
    autore_agg character varying(30) DEFAULT "current_user"() NOT NULL,
    sigla_rete character varying(10),
    ente_gestore character varying(100)
);


ALTER TABLE public.rete_monitoraggio OWNER TO weboll;

--
-- Name: COLUMN rete_monitoraggio.id_rete_monit; Type: COMMENT; Schema: public; Owner: weboll
--

COMMENT ON COLUMN public.rete_monitoraggio.id_rete_monit IS 'Caratteristiche generali delle reti di monitoraggio';


--
-- Name: COLUMN rete_monitoraggio.denominazione; Type: COMMENT; Schema: public; Owner: weboll
--

COMMENT ON COLUMN public.rete_monitoraggio.denominazione IS 'Denominazione della rete di monitoraggio';


--
-- Name: COLUMN rete_monitoraggio.data_validita; Type: COMMENT; Schema: public; Owner: weboll
--

COMMENT ON COLUMN public.rete_monitoraggio.data_validita IS 'Data inizio validita'' rete monitoraggio';


--
-- Name: COLUMN rete_monitoraggio.data_agg; Type: COMMENT; Schema: public; Owner: weboll
--

COMMENT ON COLUMN public.rete_monitoraggio.data_agg IS 'Data di ultimo aggiornamento dei dati';


--
-- Name: COLUMN rete_monitoraggio.autore_agg; Type: COMMENT; Schema: public; Owner: weboll
--

COMMENT ON COLUMN public.rete_monitoraggio.autore_agg IS 'Autore dell''ultimo aggiornamento dei dati';


--
-- Name: COLUMN rete_monitoraggio.sigla_rete; Type: COMMENT; Schema: public; Owner: weboll
--

COMMENT ON COLUMN public.rete_monitoraggio.sigla_rete IS 'Sigla della rete di monitoraggio';


--
-- Name: COLUMN rete_monitoraggio.ente_gestore; Type: COMMENT; Schema: public; Owner: weboll
--

COMMENT ON COLUMN public.rete_monitoraggio.ente_gestore IS 'Ente gestore della rete di monitoraggio';


--
-- Data for Name: rete_monitoraggio; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.rete_monitoraggio (id_rete_monit, denominazione, data_validita, data_agg, autore_agg, sigla_rete, ente_gestore) FROM stdin;
FR	FRENCH BROADBAND SEISMOLOGICAL NETWORK	2008-05-13	2011-03-29	weboll	FBSN	RENASS-EOST, BUREAU CENTRAL SISMOLOGIQUE FRANCAIS/CNRS, INSTITUT NATIONAL DES SCIENCES DE L'UNIVERS
IG	REGIONAL SEISMIC NETWORK OF NORTH WESTERN ITALY	1967-01-01	2011-03-29	weboll	RSNI	UNIVERSITA' DEGLI STUDI DI GENOVA, DIPTERIS, SETTORE GEOFISICA
UF	UFFICIO FEDERALE DELL'AMBIENTE UFAM - SVIZZERA	2016-09-01	2016-08-26	weboll	\N	\N
EF	RETE FRANCIA (EDF)	2013-01-21	2013-01-21	weboll	\N	\N
MF	RETE FRANCIA (METEO FRANCE)	2011-11-03	2011-11-03	weboll	\N	\N
FV	FRIULI-VENEZIA GIULIA SEISMOMETRIC NETWORK	1977-05-06	2008-05-13	weboll	FVGSN	ISTITUTO NAZIONALE DI OCEANOGRAFIA E DI GEOFISICA SPERIMENTALE, CENTRO DI RICERCHE SISMOLOGICHE
IV	ITALIAN NATIONAL SEISMIC NETWORK	1988-01-01	2008-05-13	weboll	INSN	ISTITUTO NAZIONALE DI GEOFISICA E VULCANOLOGIA, CENTRO NAZIONALE TERREMOTI
MN	MEDITERRANEAN VERY BROADBAND SEISMOGRAPHIC NETWORK	1988-04-29	2008-05-13	weboll	MEDNET	ISTITUTO NAZIONALE DI GEOFISICA E VULCANOLOGIA, CENTRO NAZIONALE TERREMOTI
RA	RESEAU LARGE BANDE DES ALPES	2008-05-13	2008-05-13	weboll	ROSALP	UNIVERSITE' JOSEPH FOURIER, LGIT, OBSERVATOIRE DES SCIENCES DE L'UNIVERS DE GRENOBLE
SE	SWISS DIGITAL SEISMIC NETWORK	1997-01-01	2008-05-13	weboll	SDSNET	EIDGENOSSISCHE TECHNISCHE HOCHSCHULE ZURICH, INSTITUT FUR GEOPHYSIK, SCHWEIZERISCHER ERDBEBENDIENST
TG	RESEAU TRES GRANDE RESOLUTION SISMIQUE	2008-05-13	2008-05-13	weboll	TGRS	UNIVERSITE' DE NICE - SOPHIA ANTIPOLIS, UMR GEOSCIENCES AZUR, LABORATOIRE DES SCIENCES DE LA TERRE
AE	RETE DELL'AEM AZIENDA ENERGETICA MUNICIPALE DI TORINO	1945-01-01	2012-07-02	weboll	\N	\N
CN	RETE DEL CNR ISTITUTO PER LO STUDIO DEGLI ECOSISTEMI	1981-01-01	2012-07-02	weboll	\N	\N
EE	RETE DELL'ENEL ENTE NAZIONALE PER L'ENERGIA ELETTRICA	1928-01-01	2012-07-02	weboll	\N	\N
IN	RETE DEGLI INVASI	1929-01-01	2012-07-02	weboll	\N	\N
CT	ASSOCIAZIONE IRRIGAZIONE EST SESIA - RETE DEL CONSORZIO TICINO	2012-01-01	2015-02-03	weboll	\N	\N
17	RETE METEOIDROGRAFICA DI ARPA PIEMONTE	2003-03-01	2007-01-15	weboll	\N	\N
AG	RETE AGROMETEOROLOGIA	1997-01-01	2007-01-15	weboll	\N	\N
CH	RETE DELLA SVIZZERA ITALIANA	1800-01-01	2007-01-15	weboll	\N	\N
DG	RETE DIGHE	2007-01-01	2007-02-28	weboll	\N	\N
EM	RETE EMILIA ROMAGNA	2003-01-01	2007-01-15	weboll	\N	\N
LO	RETE LOMBARDIA	2003-01-01	2007-01-15	weboll	\N	\N
MP	RETE DEL MINISTERO DEI LAVORI PUBBLICI - MAGISTRATO DEL PO	1997-10-30	2007-01-15	weboll	\N	\N
RI	REGIONE PIEMONTE DIREZIONE AMBIENTE	1990-06-15	2007-11-07	weboll	\N	\N
RL	RETE DELLA REGIONE LIGURIA	2001-05-29	2007-01-15	weboll	\N	\N
SC	RETE SERIE CLIMATICHE ULTRACENTENARIE	1753-01-31	2007-01-15	weboll	\N	\N
SY	RETE SYNOP	1951-01-01	2007-01-15	weboll	\N	\N
UI	RETE STORICA UFFICIO IDROGRAFICO (BANCA DATI STORICA CLIMATOLOGICA)	1913-01-01	2007-01-15	weboll	\N	\N
VA	RETE DELLA REGIONE VALLE D'AOSTA	1800-01-01	2007-01-15	weboll	\N	\N
TA	SERVIZIO METEOMONT - TRUPPE ALPINE	2020-01-01	2020-02-17	weboll	\N	\N
\.


--
-- Name: rete_monitoraggio_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace: 
--

ALTER TABLE ONLY public.rete_monitoraggio
    ADD CONSTRAINT rete_monitoraggio_pkey PRIMARY KEY (id_rete_monit);


--
-- Name: rete_monitoraggio_idx001; Type: INDEX; Schema: public; Owner: weboll; Tablespace: 
--

CREATE UNIQUE INDEX rete_monitoraggio_idx001 ON public.rete_monitoraggio USING btree (denominazione);


--
-- Name: TABLE rete_monitoraggio; Type: ACL; Schema: public; Owner: weboll
--



--
-- PostgreSQL database dump complete
--

