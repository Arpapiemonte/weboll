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
-- Name: aree_allertamento; Type: TABLE; Schema: public; Owner: weboll; Tablespace:
--

CREATE TABLE public.aree_allertamento (
    id_allertamento character varying(6) NOT NULL,
    id_area integer NOT NULL,
    descrizione character varying(50),
    codice_istat_reg character varying(1) NOT NULL
);


ALTER TABLE public.aree_allertamento OWNER TO weboll;

--
-- Data for Name: aree_allertamento; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.aree_allertamento (id_allertamento, id_area, descrizione, codice_istat_reg) FROM stdin;
Abru-A	1	Bacini Tordino Vomano	Q
Abru-B	2	Bacino Alto del Pescara	Q
Abru-C	3	Bacino Basso del Pescara	Q
Abru-D	4	Bacino del Sangro	Q
Abru-E	5	Marsica	Q
Basi-A	6	Bacino dell'Ofanto	T
Basi-B	7	Bacini Basento Bradano	T
Basi-C	8	Bacini Agri Sinni	T
Bolz-A	9	Venosta	E
Bolz-B	10	Alto Adige	E
Bolz-C	11	Isarco	E
Cala-1	12	Ver. Tirrenico Set. Calabrese	U
Cala-2	13	Ver. Tirrenico Cen. Calabrese	U
Cala-3	14	Ver. Tirrenico Mer. Calabrese	U
Cala-4	15	Ver. Ionico Set. Calabrese	U
Cala-5	16	Ver. Ionico Cen. Calabrese	U
Cala-6	17	Ver. Ionico Mer. Calabrese	U
Camp-A	18	Bacino Alto del Volturno	P
Camp-B	19	Pianura di Napoli	P
Camp-C	20	Bacino Alto del Calore	P
Camp-D	21	Salernitano	P
Camp-E	22	Bacino Alto del Sele	P
Camp-F	23	Bacino Basso del Sele	P
Emil-A	24	Bacino Alto del Lamone Savio	I
Emil-B	25	Pianura di Forli' Ravenna	I
Emil-C	26	Bacino del Reno	I
Emil-D	27	Pianura di Bologna e Ferrara	I
Emil-E	28	Bacini Secchia Panaro	I
Emil-F	29	Pianura di Modena Reggio Emilia	I
Emil-G	30	Bacini Trebbia Taro	I
Emil-H	31	Pianura di Parma Piacenza	I
Friu-A	32	Bacino del Livenza	G
Friu-B	33	Bacino del Tagliamento	G
Friu-C	34	Pianura di Udine Gorizia Trieste	G
Lazi-A	35	Laghi Bolsena e Bracciano	O
Lazi-B	36	Bacino Basso del Tevere	O
Lazi-C	37	Appennino di Rieti	O
Lazi-D	38	Bacino del Sisto	O
Lazi-E	39	Marsica e Ciociaria	O
Ligu-A	40	Bacini Liguri Marittimi di Ponente	C
Ligu-B	41	Bacini Liguri Marittimi di Centro	C
Ligu-C	42	Bacini Liguri Padani di Ponente	C
Ligu-D	43	Bacini Liguri Padani di Levante	C
Ligu-E	44	Bacini Liguri Marittimi di Levante	C
Lomb-A	45	Valtellina	D
Lomb-B	46	Bacini Brembo Ticino	D
Lomb-C	47	Milano Brianza	D
Lomb-D	48	Pianura Occidentale Lombarda	D
Lomb-E	49	Oltrepo' Pavese	D
Lomb-F	50	Pianura Orientale Lombarda	D
Lomb-G	51	Garda Valcamonica	D
Lomb-H	52	Alpi e Prealpi Bergamasche	D
Marc-A	53	Appennino Marchigiano Settentrionale	L
Marc-B	54	Pianura Marchigiana Settentrionale	L
Marc-C	55	Appennino Marchigiano Meridionale	L
Marc-D	56	Pianura Marchigiana Meridionale	L
Moli-A	57	Bacini Biferno Trigno Fortore	R
Piem-A	58	Toce	A
Piem-B	59	Dora Baltea Sesia	A
Piem-C	60	Orco Bassa Dora Riparia Sangone	A
Piem-D	61	Alta Dora Riparia Po	A
Piem-E	62	Varaita Stura	A
Piem-F	63	Alto Tanaro	A
Piem-G	64	Belbo Bormida	A
Piem-H	65	Scrivia	A
Piem-I	66	Pianura settentrionale	A
Piem-L	67	Pianura Torinese Colline	A
Piem-M	68	Pianura Cuneese	A
Piem-T	69	Ticino	A
Piem-V	70	Dora Baltea	A
Pugl-A	71	Gargano	S
Pugl-B	72	Capitanata	S
Pugl-C	73	Terra di Bari	S
Pugl-D	74	Penisola Salentina	S
Pugl-E	75	Bacini Lato Lama di Lenne	S
Pugl-F	76	Bacino Basso dell'Ofanto	S
Sard-A	77	Iglesiente	Z
Sard-B	78	Campidano	Z
Sard-C	79	Bacini Montevecchio Pischilappiu	Z
Sard-D	80	Bacini Flumendosa Flumineddu	Z
Sard-E	81	Bacino del Tirso	Z
Sard-F	82	Gallura	Z
Sard-G	83	Logudoro	Z
Sici-A	84	Monti Peloritani	V
Sici-B	85	Bacino del Simeto	V
Sici-C	86	Val di Noto	V
Sici-D	87	Bacini Gela Platani Salso	V
Sici-E	88	Versante Tirrenico Siciliano	V
Sici-F	89	Val di Mazara	V
Tosc-A	90	Versilia Apuane	M
Tosc-B	91	Valdarno Medio e Inferiore	M
Tosc-C	92	Costa Maremmana	M
Tosc-D	93	Chianti Amiata	M
Tosc-E	94	Valdarno Superiore	M
Tosc-F	95	Dorsale Appenninica Toscana	M
Tren-A	96	Bacino Basso dell'Adige Trentino	E
Tren-B	97	Bacini Noce Sarca	E
Umbr-A	98	Bacino Alto del Tevere	N
Umbr-B	99	Appennino di Foligno	N
Umbr-C	100	Bacino Medio Tevere	N
VdAo-A	70	Dora Baltea	B
VdAo-B	59	Dora Baltea Sesia	B
VdAo-C	60	Orco Bassa Dora Riparia Sangone	B
Vene-A	101	Bacino del Piave	F
Vene-B	102	Bacino del Brenta	F
Vene-C	103	Monti Lessini	F
Vene-D	104	Bacini Po di Venezia Tartaro	F
Vene-E	105	Pianura di Padova e Vicenza	F
Vene-F	106	Bacino del Sile	F
Vene-G	107	Bacino Veneto del Livenza	F
\.


--
-- Name: aree_allertamento_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace:
--

ALTER TABLE ONLY public.aree_allertamento
    ADD CONSTRAINT aree_allertamento_pkey PRIMARY KEY (id_allertamento);


--
-- Name: TABLE aree_allertamento; Type: ACL; Schema: public; Owner: weboll
--



--
-- PostgreSQL database dump complete
--

