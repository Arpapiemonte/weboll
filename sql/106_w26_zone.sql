--
-- PostgreSQL database dump
--

-- Dumped from database version 13.7 (Debian 13.7-1.pgdg110+1)
-- Dumped by pg_dump version 13.7 (Debian 13.7-1.pgdg110+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: w26_zone; Type: TABLE; Schema: public; Owner: weboll
--

CREATE TABLE public.w26_zone (
    id_w26_zone integer NOT NULL,
    codice character varying(9),
    localita character varying(100) NOT NULL,
    corsoacqua character varying(100) NOT NULL,
    numero integer NOT NULL
);


ALTER TABLE public.w26_zone OWNER TO weboll;

--
-- Data for Name: w26_zone; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.w26_zone (id_w26_zone, codice, localita, corsoacqua, numero) FROM stdin;
1	001191901	San Martino	Chisone	10
2	001300700	Villafranca	Pellice	20
3	001309900	Vinovo	Chisola	30
4	001272909	Torino	Sangone	40
5	001270904	Susa (Via Mazzini)	Dora Riparia	50
6	001272701	Torino	Dora Riparia	60
7	001128901	Lanzo	Stura di Lanzo	70
8	001272702	Torino	Stura di Lanzo	80
9	001109900	Front	Malone	90
10	001066900	Spineto	Orco	100
11	001236700	San Benigno	Orco	110
12	001179900	Parella	Chiusella	120
13	001271900	Tavagnasco	Dora Baltea	130
14	001293700	Verolengo	Dora Baltea	140
15	002032700	Carisio	Elvo	150
16	002160900	Vigliano	Cervo	160
17	002108700	Quinto Vercellese	Cervo	170
18	002016901	Borgosesia	Sesia	180
19	018107700	Palestro	Sesia	190
20	003096900	Candoglia	Toce	200
21	003100900	Momo	Agogna	210
22	004082700	Dronero	Maira	220
23	004179700	Racconigi	Maira	230
24	004197900	Rossana	Varaita	240
25	004171700	Polonghera	Varaita	250
26	004139700	Monterosso	Grana	260
27	001257900	Santena	Banna	270
28	004233901	Andonno	Gesso	280
29	004185900	Robilante	Vermenagna	290
30	004079900	Gaiola	Stura di Demonte	300
31	004089901	Fossano	Stura di Demonte	310
32	004043700	Carru'	Pesio	320
33	004130700	Mondovì	Ellero	330
34	004086900	Farigliano	Tanaro	340
35	004003900	Alba	Tanaro	350
36	006003902	Alessandria	Tanaro	360
37	006105700	Montecastello	Tanaro	370
38	005029900	Castelnuovo	Belbo	380
39	009048900	Piana Crixia	Bormida di Spigno	390
40	005064700	Mombaldone	Bormida di Spigno	400
41	004035900	Camerana	Bormida di Millesimo	410
42	006043900	Cassine	Bormida	420
43	006012700	Basaluzzo	Orba	430
44	006160900	Serravalle	Scrivia	440
45	001300900	Villafranca Piemonte	Po	450
46	001272703	Torino (C.so Regina)	Po	460
47	001253700	San Sebastiano	Po	470
48	006039901	Casale Monferrato	Po	480
49	006177900	Valenza	Po	490
50	006087700	Isola S. Antonio	Po	500
\.


--
-- Name: w26_zone w26_zone_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w26_zone
    ADD CONSTRAINT w26_zone_pkey PRIMARY KEY (id_w26_zone);


--
-- PostgreSQL database dump complete
--

