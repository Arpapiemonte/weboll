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

CREATE TABLE public.unita_misura (
    id_unita_misura character varying(2) NOT NULL,
    descrizione character varying(60),
    data_agg timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(6) with time zone NOT NULL,
    autore_agg character varying(30) DEFAULT "current_user"() NOT NULL
);

ALTER TABLE public.unita_misura OWNER TO weboll;

--

COPY public.unita_misura (id_unita_misura, descrizione, data_agg, autore_agg) FROM stdin;
34	Parti per milione	2006-11-17 00:00:00	weboll
35	Metri elevato a -1	2006-11-17 00:00:00	weboll
36	Milligrami al metro quadro per mese	2006-11-17 00:00:00	weboll
37	Alfanumerico	2006-11-17 00:00:00	weboll
38	Decibel	2006-11-17 00:00:00	weboll
39	MilliVolt	2006-11-17 00:00:00	weboll
41	Veicoli/unita' di tempo	2006-11-17 00:00:00	weboll
44	Joule al metro quadro al giorno	2008-05-26 00:00:00	weboll
45	Numero di particelle al metro cubo	2009-07-17 00:00:00	weboll
01	Millimetri	2006-11-17 00:00:00	weboll
02	Gradi Celsius	2007-07-17 00:00:00	weboll
03	Gradi	2006-11-17 00:00:00	weboll
04	Chilometri all'ora	2006-11-17 00:00:00	weboll
05	Percentuale	2006-11-17 00:00:00	weboll
06	Centimetri	2006-11-17 00:00:00	weboll
07	Hettopascal	2006-11-17 00:00:00	weboll
08	Megajoule al metro quadro	2006-11-17 00:00:00	weboll
09	Watt al metro quadro	2006-11-17 00:00:00	weboll
10	Volt	2006-11-17 00:00:00	weboll
11	Ampere	2006-11-17 00:00:00	weboll
12	Chilometri	2006-11-17 00:00:00	weboll
13	Metri	2006-11-17 00:00:00	weboll
14	Metri cubi al secondo	2006-11-17 00:00:00	weboll
15	Microsiemens al centimetro	2006-11-17 00:00:00	weboll
16	Milligrammi al litro	2006-11-17 00:00:00	weboll
17	Unita' nefelometriche di torbidita'	2006-12-01 00:00:00	weboll
18	Estinzione al metro	2006-11-17 00:00:00	weboll
19	Ottavi con valore 9 per cielo invisibile	2006-11-17 00:00:00	weboll
20	Minuti	2006-11-17 00:00:00	weboll
21	Sedicesimi (rosa venti) con valore 17 per calma vento	2006-11-17 00:00:00	weboll
22	Metri al secondo	2006-11-17 00:00:00	weboll
23	Microgrammi al metro cubo	2006-11-17 00:00:00	weboll
24	Milligrammi al metro cubo	2006-11-17 00:00:00	weboll
25	Nanogrammi al metro cubo	2006-11-17 00:00:00	weboll
26	Secondi	2006-11-17 00:00:00	weboll
27	Ampere ora	2006-11-17 00:00:00	weboll
28	Calorie al centimetro quadro al minuto	2006-11-17 00:00:00	weboll
29	Parti di impurita' per mille parti di acqua	2006-12-01 00:00:00	weboll
30	Decametri	2006-11-17 00:00:00	weboll
31	Parti per bilione (miliardo)	2006-11-17 00:00:00	weboll
32	Litri al secondo per km quadro	2006-11-17 00:00:00	weboll
33	°C*d	2005-12-21 00:00:00	weboll
40	NanoSievert per ora	2006-11-17 00:00:00	weboll
42	MilliSievert per ora	2007-05-17 00:00:00	weboll
43	Chilogrammo al metro quadro	2008-05-20 00:00:00	weboll
98	Numero (adimensionale)	2006-11-17 00:00:00	weboll
99	ALTRA UNITA' DI MISURA	2006-11-17 00:00:00	weboll
\.





ALTER TABLE ONLY public.unita_misura
    ADD CONSTRAINT unita_misura_pkey PRIMARY KEY (id_unita_misura);


--
-- Name: TABLE unita_misura; Type: ACL; Schema: public; Owner: weboll
--

ALTER TABLE public.unita_misura OWNER TO weboll;

--
-- PostgreSQL database dump complete
--
