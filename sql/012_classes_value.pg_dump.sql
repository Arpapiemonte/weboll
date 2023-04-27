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
-- Name: classes_value; Type: TABLE; Schema: public; Owner: weboll; Tablespace: 
--

CREATE TABLE public.classes_value (
    id_classes_value smallint DEFAULT nextval('public.classes_value_id_classes_value_seq'::regclass) NOT NULL,
    id_classes smallint NOT NULL,
    description character varying(50) NOT NULL,
    last_update timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(6) with time zone NOT NULL,
    username character varying(30) DEFAULT "current_user"() NOT NULL
);


ALTER TABLE public.classes_value OWNER TO weboll;

--
-- Data for Name: classes_value; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.classes_value (id_classes_value, id_classes, description, last_update, username) FROM stdin;
1	1	Sereno	2010-03-23 09:00:00	weboll
2	1	Poco Nuvoloso	2010-03-23 09:00:00	weboll
3	1	Parzialmente - Irregolarmente Nuvoloso	2010-03-23 09:00:00	weboll
4	1	Nuvoloso	2010-03-23 09:00:00	weboll
5	1	Molto Nuvoloso	2010-03-23 09:00:00	weboll
6	1	Coperto	2010-03-23 09:00:00	weboll
7	2	Intensificazione	2010-03-23 09:00:00	weboll
8	2	Mancante - Stazionario	2010-03-23 09:00:00	weboll
9	2	Attenuazione	2010-03-23 09:00:00	weboll
10	3	Si	2010-03-23 09:00:00	weboll
11	3	No	2010-03-23 09:00:00	weboll
14	4	Nebbia	2010-03-23 09:00:00	weboll
16	5	Assente	2010-03-23 09:00:00	weboll
17	5	Debole	2010-03-23 09:00:00	weboll
18	5	Moderata	2010-03-23 09:00:00	weboll
19	5	Forte	2010-03-23 09:00:00	weboll
20	5	Molto Forte	2010-03-23 09:00:00	weboll
21	6	Assente	2010-03-23 09:00:00	weboll
22	6	Debole	2010-03-23 09:00:00	weboll
23	6	Moderata	2010-03-23 09:00:00	weboll
24	6	Forte	2010-03-23 09:00:00	weboll
25	6	Molto Forte	2010-03-23 09:00:00	weboll
26	7	Assente	2010-03-23 09:00:00	weboll
27	7	Debole	2010-03-23 09:00:00	weboll
28	7	Moderata	2010-03-23 09:00:00	weboll
29	7	Forte	2010-03-23 09:00:00	weboll
30	7	Molto Forte	2010-03-23 09:00:00	weboll
31	8	Intensificazione	2010-03-23 09:00:00	weboll
32	8	Costante	2010-03-23 09:00:00	weboll
33	8	Attenuazione - Esaurimento	2010-03-23 09:00:00	weboll
34	9	In Aumento	2010-03-23 09:00:00	weboll
35	9	Stazionaria	2010-03-23 09:00:00	weboll
36	9	In Diminuzione	2010-03-23 09:00:00	weboll
37	10	In Aumento	2010-03-23 09:00:00	weboll
38	10	Stazionario	2010-03-23 09:00:00	weboll
39	10	in Diminuzione	2010-03-23 09:00:00	weboll
40	11	In Aumento	2010-03-23 09:00:00	weboll
41	11	Stazionario	2010-03-23 09:00:00	weboll
42	11	In Diminuzione	2010-03-23 09:00:00	weboll
43	12	In Aumento	2010-03-23 09:00:00	weboll
44	12	Stazionario	2010-03-23 09:00:00	weboll
45	12	In Diminuzione	2010-03-23 09:00:00	weboll
46	13	In Aumento	2010-03-23 09:00:00	weboll
47	13	Stazionario	2010-03-23 09:00:00	weboll
48	13	In Diminuzione	2010-03-23 09:00:00	weboll
49	14	Non Definito	2010-03-23 09:00:00	weboll
50	14	In Aumento	2010-03-23 09:00:00	weboll
51	14	Stazionario	2010-03-23 09:00:00	weboll
52	14	In Diminuzione	2010-03-23 09:00:00	weboll
53	15	Non Definito	2010-03-23 09:00:00	weboll
54	15	In Aumento	2010-03-23 09:00:00	weboll
55	15	Stazionario	2010-03-23 09:00:00	weboll
56	15	In Diminuzione	2010-03-23 09:00:00	weboll
57	16	Calmo	2010-03-23 09:00:00	weboll
58	16	Debole	2010-03-23 09:00:00	weboll
59	16	Moderato	2010-03-23 09:00:00	weboll
60	16	Forte	2010-03-23 09:00:00	weboll
61	16	Molto Forte	2010-03-23 09:00:00	weboll
62	16	Burrasca	2010-03-23 09:00:00	weboll
63	17	In Aumento	2010-03-23 09:00:00	weboll
64	17	Costante	2010-03-23 09:00:00	weboll
65	17	In Calo	2010-03-23 09:00:00	weboll
66	18	Calmo	2010-03-23 09:00:00	weboll
67	18	Debole	2010-03-23 09:00:00	weboll
68	18	Moderato	2010-03-23 09:00:00	weboll
69	18	Forte	2010-03-23 09:00:00	weboll
70	18	Molto Forte	2010-03-23 09:00:00	weboll
71	18	Burrasca	2010-03-23 09:00:00	weboll
72	19	In Aumento	2010-03-23 09:00:00	weboll
73	19	Costante	2010-03-23 09:00:00	weboll
74	19	In Calo	2010-03-23 09:00:00	weboll
75	20	Si	2010-03-23 09:00:00	weboll
76	20	No	2010-03-23 09:00:00	weboll
77	20	Forti	2010-03-23 09:00:00	weboll
78	21	Esteso	2010-03-23 09:00:00	weboll
79	21	Locale	2010-03-23 09:00:00	weboll
80	21	Assente	2010-03-23 09:00:00	weboll
12	4	Buona/Ottima	2010-03-23 09:00:00	weboll
15	4	Foschia/Banchi di nebbia	2010-03-23 09:00:00	weboll
81	1	-	2021-04-12 15:00:00	weboll
82	2	-	2021-04-12 15:00:00	weboll
83	3	-	2021-04-12 15:00:00	weboll
84	4	-	2021-04-12 15:00:00	weboll
85	5	-	2021-04-12 15:00:00	weboll
86	6	-	2021-04-12 15:00:00	weboll
87	7	-	2021-04-12 15:00:00	weboll
88	8	-	2021-04-12 15:00:00	weboll
89	9	-	2021-04-12 15:00:00	weboll
90	10	-	2021-04-12 15:00:00	weboll
91	11	-	2021-04-12 15:00:00	weboll
92	12	-	2021-04-12 15:00:00	weboll
93	13	-	2021-04-12 15:00:00	weboll
94	14	-	2021-04-12 15:00:00	weboll
95	15	-	2021-04-12 15:00:00	weboll
96	16	-	2021-04-12 15:00:00	weboll
97	17	-	2021-04-12 15:00:00	weboll
98	18	-	2021-04-12 15:00:00	weboll
99	19	-	2021-04-12 15:00:00	weboll
100	20	-	2021-04-12 15:00:00	weboll
101	21	-	2021-04-12 15:00:00	weboll
\.


--
-- Name: classes_value_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace: 
--

ALTER TABLE ONLY public.classes_value
    ADD CONSTRAINT classes_value_pkey PRIMARY KEY (id_classes_value);


--
-- Name: classes_value_fkey001; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.classes_value
    ADD CONSTRAINT classes_value_fkey001 FOREIGN KEY (id_classes) REFERENCES public.classes(id_classes) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: TABLE classes_value; Type: ACL; Schema: public; Owner: weboll
--



--
-- PostgreSQL database dump complete
--

