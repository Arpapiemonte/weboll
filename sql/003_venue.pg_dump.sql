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
-- Name: venue; Type: TABLE; Schema: public; Owner: weboll; Tablespace: 
--

CREATE TABLE public.venue (
    id_venue integer NOT NULL,
    description character varying(50) NOT NULL,
    altitude numeric(6,2),
    last_update timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(6) with time zone NOT NULL,
    username character varying(30) DEFAULT "current_user"() NOT NULL
);


ALTER TABLE public.venue OWNER TO weboll;

--
-- Data for Name: venue; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.venue (id_venue, description, altitude, last_update, username) FROM stdin;
120	TO.2	\N	2012-05-25 13:00:00	weboll
121	TO.3	\N	2012-05-25 13:00:00	weboll
122	TO.4	\N	2012-05-25 13:00:00	weboll
123	TO.5	\N	2012-05-25 13:00:00	weboll
124	TO.6	\N	2012-05-25 13:00:00	weboll
125	TO.7	\N	2012-05-25 13:00:00	weboll
126	TO.8	\N	2012-05-25 13:00:00	weboll
127	TO.9	\N	2012-05-25 13:00:00	weboll
101	A26 Ovada - Dir. Predosa-Bettole - A7 Tortona	\N	2010-11-02 15:00:00	weboll
104	A26 Romagnano Sesia - A8/A26 Castelletto Ticino	\N	2010-11-02 15:00:00	weboll
105	A26 Dir. Gallarate-Gattico - Gravellona Toce	\N	2010-11-02 15:00:00	weboll
96	A6 Ceva - Altare	\N	2010-11-02 15:00:00	weboll
97	A6 Altare - Savona	\N	2010-11-02 15:00:00	weboll
99	A7 Confine Liguria-Piemonte - Serravalle Scrivia	\N	2010-11-02 15:00:00	weboll
100	A26 Confine Liguria-Piemonte - Ovada	\N	2010-11-02 15:00:00	weboll
102	A26 Dir. Predosa-Bettole - Casale Monferrato	\N	2010-11-02 15:00:00	weboll
107	A21 Tanaro - Alessandria Est	\N	2010-12-06 11:20:00	weboll
108	A21 Broni-Stradella - Piacenza	\N	2010-12-06 11:20:00	weboll
24	A21 Alessandria Est - Broni-Stradella	\N	2010-12-06 11:20:00	weboll
49	A21 Asti Est - Tanaro	\N	2010-12-06 11:20:00	weboll
66	A21 Torino - Villanova d'Asti	\N	2010-12-06 11:20:00	weboll
41	A4 Biandrate - Rho	\N	2010-12-06 11:20:00	weboll
19	A4 Cigliano - Biandrate	\N	2010-12-06 11:20:00	weboll
25	A4 Settimo Torinese - Cigliano	\N	2010-12-06 11:20:00	weboll
47	A4 Torino - Settimo Torinese	\N	2010-12-06 11:20:00	weboll
87	Alpi Cozie	2000.00	2010-09-06 14:15:00	weboll
88	Alpi Graie	2000.00	2010-09-06 14:15:00	weboll
89	Alpi Lepontine	2000.00	2010-09-06 14:15:00	weboll
90	Alpi Marittime	2000.00	2010-09-06 14:15:00	weboll
91	Appennino	1500.00	2010-09-06 14:15:00	weboll
92	Pianure Occidentali	400.00	2010-09-06 14:15:00	weboll
93	Pianure Orientali	400.00	2010-09-06 14:15:00	weboll
73	Piem-A	\N	2010-05-31 10:20:00	weboll
74	Piem-B	\N	2010-05-31 10:20:00	weboll
75	Piem-C	\N	2010-05-31 10:20:00	weboll
76	Piem-D	\N	2010-05-31 10:20:00	weboll
77	Piem-E	\N	2010-05-31 10:20:00	weboll
78	Piem-F	\N	2010-05-31 10:20:00	weboll
79	Piem-G	\N	2010-05-31 10:20:00	weboll
80	Piem-H	\N	2010-05-31 10:20:00	weboll
81	Piem-I	\N	2010-05-31 10:20:00	weboll
82	Piem-L	\N	2010-05-31 10:20:00	weboll
83	Piem-M	\N	2010-05-31 10:20:00	weboll
84	Piem-T	\N	2010-05-31 10:20:00	weboll
85	VdAo-A	\N	2010-05-31 10:20:00	weboll
86	Z	\N	2010-05-31 10:20:00	weboll
67	Regione Piemonte	\N	2010-02-08 14:39:00	weboll
106	A21 Villanova d'Asti - Asti Est	\N	2010-12-06 11:20:00	weboll
63	Verbania	202.00	2010-12-13 23:10:00	weboll
1	Biella	405.00	2010-12-13 23:10:00	weboll
2	Oropa	1162.00	2010-12-13 23:10:00	weboll
3	Sestriere	2020.00	2010-12-13 23:10:00	weboll
4	Bardonecchia	1312.00	2010-12-13 23:10:00	weboll
5	Claviere	1760.00	2010-12-13 23:10:00	weboll
8	Oulx	1100.00	2010-12-13 23:10:00	weboll
43	Salbertrand	1032.00	2010-12-13 23:10:00	weboll
6	Sauze d'Oulx	1510.00	2010-12-13 23:10:00	weboll
45	Sauze di Cesana	1560.00	2010-12-13 23:10:00	weboll
7	San Sicario	2087.00	2010-12-13 23:10:00	weboll
32	Monte Fraiteve	2701.00	2010-12-13 23:10:00	weboll
28	Cuneo	575.00	2010-12-13 23:10:00	weboll
9	Alessandria	90.00	2010-12-13 23:10:00	weboll
72	Capanne di Cosola	1550.00	2010-12-13 23:10:00	weboll
11	Asti	117.00	2010-12-13 23:10:00	weboll
33	Novara	178.00	2010-12-13 23:10:00	weboll
59	Torino	239.00	2010-12-13 23:10:00	weboll
64	Vercelli	132.00	2010-12-13 23:10:00	weboll
14	Sestriere Banchetta	2480.00	2010-12-13 23:10:00	weboll
10	Sestriere Alpette	2250.00	2010-12-13 23:10:00	weboll
12	Domodossola	252.00	2010-12-13 23:10:00	weboll
13	Arona	332.00	2010-12-13 23:10:00	weboll
15	Varallo	470.00	2010-12-13 23:10:00	weboll
16	Ivrea	337.00	2010-12-13 23:10:00	weboll
18	Susa	520.00	2010-12-13 23:10:00	weboll
20	Chiomonte	750.00	2010-12-13 23:10:00	weboll
21	Meana	730.00	2010-12-13 23:10:00	weboll
22	Gravere	750.00	2010-12-13 23:10:00	weboll
23	Giaglione	520.00	2010-12-13 23:10:00	weboll
26	Exilles	870.00	2010-12-13 23:10:00	weboll
27	Cesana	1354.00	2010-12-13 23:10:00	weboll
30	Moncenisio	1461.00	2010-12-13 23:10:00	weboll
31	Colle Barant	2294.00	2010-12-13 23:10:00	weboll
34	Bobbio Pellice	1312.00	2010-12-13 23:10:00	weboll
35	Saluzzo	395.00	2010-12-13 23:10:00	weboll
36	Luserna San Giovanni	478.00	2010-12-13 23:10:00	weboll
37	Entracque	950.00	2010-12-13 23:10:00	weboll
38	Fossano	403.00	2010-12-13 23:10:00	weboll
40	Chiusa Pesio	575.00	2010-12-13 23:10:00	weboll
42	Alba	172.00	2010-12-13 23:10:00	weboll
44	San Damiano	154.00	2010-12-13 23:10:00	weboll
70	Casale Monferrato	136.00	2010-12-13 23:10:00	weboll
46	Crea	385.00	2010-12-13 23:10:00	weboll
60	Tortona	122.00	2010-12-13 23:10:00	weboll
61	Acqui Terme	215.00	2010-12-13 23:10:00	weboll
62	Nizza Monferrato	138.00	2010-12-13 23:10:00	weboll
65	Arquata Scrivia	325.00	2010-12-13 23:10:00	weboll
68	Alpe Cheggio	1505.00	2010-12-14 10:20:00	weboll
69	Piamprato	1550.00	2010-12-14 10:20:00	weboll
71	Valdieri	1390.00	2010-12-14 10:20:00	weboll
58	Montechiaro d'Asti	200.00	2010-12-13 23:10:00	weboll
57	Villanova d'Asti	238.00	2010-12-14 10:20:00	weboll
50	Borgomanero	300.00	2010-12-17 15:30:00	weboll
51	Mottarone	1502.00	2010-12-17 15:30:00	weboll
52	Omegna	292.00	2010-12-17 15:30:00	weboll
53	Macugnaga	1360.00	2010-12-17 15:30:00	weboll
54	Formazza	1226.00	2010-12-17 15:30:00	weboll
94	A6 Torino - Mondovì	\N	2010-11-02 15:00:00	weboll
95	A6 Mondovì - Ceva	\N	2010-11-02 15:00:00	weboll
103	A26 Casale Monf. - Romagnano + Stroppiana-Santhià	\N	2010-11-02 15:00:00	weboll
39	Mondovì	422.00	2010-12-13 23:10:00	weboll
48	Isola di Sant'Antonio	77.00	2010-12-13 23:10:00	weboll
55	Caselle Torinese	300.00	2011-06-14 09:30:00	weboll
17	Alpi Lepontine Nord	2000.00	2011-06-14 10:15:01	weboll
29	Alpi Lepontine Sud	2000.00	2011-06-14 10:15:02	weboll
56	Alpi Pennine Nord	2000.00	2011-06-14 10:15:03	weboll
111	Alpi Cozie Nord	2000.00	2011-06-14 10:15:07	weboll
113	Alpi Cozie Sud	2000.00	2011-06-14 10:15:09	weboll
112	Alpi Cozie zone di confine	2000.00	2011-06-14 10:15:08	weboll
110	Alpi Graie zone di confine	2000.00	2011-06-14 10:15:06	weboll
114	Alpi Marittime Occidentali	2000.00	2011-06-14 10:15:10	weboll
115	Alpi Marittime Orientali	2000.00	2011-06-14 10:15:11	weboll
118	Appennino e Preappennino Alessandrino	1500.00	2011-06-14 10:15:14	weboll
117	Langhe e Roero	700.00	2011-06-14 10:15:13	weboll
109	Alpi Pennine Sud	2000.00	2011-06-14 10:15:04	weboll
119	Collina Torinese e Astigiano	700.00	2011-06-14 10:15:15	weboll
116	Alpi Liguri	1500.00	2011-06-14 10:15:12	weboll
187	A33 Tratta1 Cuneo-Carru	\N	2016-12-07 10:02:24.0	weboll
188	A33 Tratta2 Marene-Cherasco	\N	2016-12-07 10:02:47.0	weboll
189	A33 Tratta3 Alba-Asti	\N	2016-12-07 10:03:44.0	weboll
190	Alpi Pennine	\N	2016-12-07 10:03:44.0	weboll
191	Lago d'Orta	\N	2016-12-07 10:03:44.0	weboll
192	Laghi di avigliana	\N	2016-12-07 10:03:44.0	weboll
193	Pianura	400.00	2010-09-06 14:15:00	weboll
194	Bassa Montagna	1500.00	2010-09-06 14:15:00	weboll
195	Alta Montagna	2000.00	2010-09-06 14:15:00	weboll
\.


--
-- Name: venue_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace: 
--

ALTER TABLE ONLY public.venue
    ADD CONSTRAINT venue_pkey PRIMARY KEY (id_venue);


--
-- Name: TABLE venue; Type: ACL; Schema: public; Owner: weboll
--

ALTER TABLE public.venue OWNER TO weboll;

--
-- PostgreSQL database dump complete
--

INSERT INTO public.venue
(id_venue, description, altitude, last_update, username)
VALUES(171, 'Provincia di Alessandria', NULL, '2013-07-12 14:20:00.000', 'weboll');
INSERT INTO public.venue
(id_venue, description, altitude, last_update, username)
VALUES(172, 'Provincia di Asti', NULL, '2013-07-12 14:20:00.000', 'weboll');
INSERT INTO public.venue
(id_venue, description, altitude, last_update, username)
VALUES(173, 'Provincia di Biella', NULL, '2013-07-12 14:20:00.000', 'weboll');
INSERT INTO public.venue
(id_venue, description, altitude, last_update, username)
VALUES(174, 'Provincia di Cuneo', NULL, '2013-07-12 14:20:00.000', 'weboll');
INSERT INTO public.venue
(id_venue, description, altitude, last_update, username)
VALUES(175, 'Provincia di Novara', NULL, '2013-07-12 14:20:00.000', 'weboll');
INSERT INTO public.venue
(id_venue, description, altitude, last_update, username)
VALUES(176, 'Provincia di Torino', NULL, '2013-07-12 14:20:00.000', 'weboll');
INSERT INTO public.venue
(id_venue, description, altitude, last_update, username)
VALUES(177, 'Provincia di Verbania', NULL, '2013-07-12 14:20:00.000', 'weboll');
INSERT INTO public.venue
(id_venue, description, altitude, last_update, username)
VALUES(178, 'Provincia di Vercelli', NULL, '2013-07-12 14:20:00.000', 'weboll');
INSERT INTO public.venue
(id_venue, description, altitude, last_update, username)
VALUES(179, 'Pray Sessera', 409.00, '2013-07-12 14:20:00.000', 'weboll');
INSERT INTO public.venue
(id_venue, description, altitude, last_update, username)
VALUES(180, 'Pettinengo', 725.00, '2013-11-29 13:00:00.000', 'weboll');
INSERT INTO public.venue
(id_venue, description, altitude, last_update, username)
VALUES(181, 'Piedicavallo', 1040.00, '2013-11-29 13:00:00.000', 'weboll');
INSERT INTO public.venue
(id_venue, description, altitude, last_update, username)
VALUES(182, 'Masserano', 243.00, '2013-11-29 13:00:00.000', 'weboll');
INSERT INTO public.venue
(id_venue, description, altitude, last_update, username)
VALUES(183, 'Massazza', 226.00, '2013-11-29 13:00:00.000', 'weboll');
