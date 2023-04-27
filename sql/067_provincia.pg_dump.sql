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
-- Name: provincia; Type: TABLE; Schema: public; Owner: weboll; Tablespace: 
--

CREATE TABLE public.provincia (
    codice_istat_prov character varying(3) NOT NULL,
    sigla_auto character varying(2) NOT NULL,
    denominazione character varying(40) NOT NULL,
    codice_istat_1981 character varying(2),
    codice_istat_reg character varying(1),
    data_agg timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(6) with time zone NOT NULL
);


ALTER TABLE public.provincia OWNER TO weboll;

--
-- Name: TABLE provincia; Type: COMMENT; Schema: public; Owner: weboll
--

COMMENT ON TABLE public.provincia IS 'Elenco delle provincie italiane';


--
-- Data for Name: provincia; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.provincia (codice_istat_prov, sigla_auto, denominazione, codice_istat_1981, codice_istat_reg, data_agg) FROM stdin;
028	PD	PROVINCIA DI PADOVA	28	F	2004-07-14 10:25:21
029	RO	PROVINCIA DI ROVIGO	29	F	2004-07-14 10:25:21
030	UD	PROVINCIA DI UDINE	30	G	2004-07-14 10:25:21
031	GO	PROVINCIA DI GORIZIA	31	G	2004-07-14 10:25:21
032	TS	PROVINCIA DI TRIESTE	32	G	2004-07-14 10:25:21
033	PC	PROVINCIA DI PIACENZA	33	I	2004-07-14 10:25:21
034	PR	PROVINCIA DI PARMA	34	I	2004-07-14 10:25:21
035	RE	PROVINCIA DI REGGIO NELL'EMILIA	35	I	2004-07-14 10:25:21
036	MO	PROVINCIA DI MODENA	36	I	2004-07-14 10:25:21
037	BO	PROVINCIA DI BOLOGNA	37	I	2004-07-14 10:25:21
038	FE	PROVINCIA DI FERRARA	38	I	2004-07-14 10:25:21
039	RA	PROVINCIA DI RAVENNA	39	I	2004-07-14 10:25:21
040	FO	PROVINCIA DI FORLI'	40	I	2004-07-14 10:25:21
041	PS	PROVINCIA DI PESARO	41	L	2004-07-14 10:25:21
042	AN	PROVINCIA DI ANCONA	42	L	2004-07-14 10:25:21
043	MC	PROVINCIA DI MACERATA	43	L	2004-07-14 10:25:21
044	AP	PROVINCIA DI ASCOLI PICENO	44	Q	2004-07-14 10:25:21
045	MS	PROVINCIA DI MASSA CARRARA	45	M	2004-07-14 10:25:21
046	LU	PROVINCIA DI LUCCA	46	M	2004-07-14 10:25:21
047	PT	PROVINCIA DI PISTOIA	47	M	2004-07-14 10:25:21
048	FI	PROVINCIA DI FIRENZE	48	M	2004-07-14 10:25:21
049	LI	PROVINCIA DI LIVORNO	49	M	2004-07-14 10:25:21
050	PI	PROVINCIA DI PISA	50	M	2004-07-14 10:25:21
051	AR	PROVINCIA DI AREZZO	51	M	2004-07-14 10:25:21
052	SI	PROVINCIA DI SIENA	52	M	2004-07-14 10:25:21
053	GR	PROVINCIA DI GROSSETO	53	M	2004-07-14 10:25:21
054	PG	PROVINCIA DI PERUGIA	54	N	2004-07-14 10:25:21
055	TR	PROVINCIA DI TERNI	55	N	2004-07-14 10:25:21
056	VT	PROVINCIA DI VITERBO	56	O	2004-07-14 10:25:21
057	RI	PROVINCIA DI RIETI	57	O	2004-07-14 10:25:21
058	RM	PROVINCIA DI ROMA	58	O	2004-07-14 10:25:21
059	LT	PROVINCIA DI LATINA	59	O	2004-07-14 10:25:21
060	FR	PROVINCIA DI FROSINONE	60	O	2004-07-14 10:25:21
061	CE	PROVINCIA DI CASERTA	61	P	2004-07-14 10:25:21
062	BN	PROVINCIA DI BENEVENTO	62	P	2004-07-14 10:25:21
063	NA	PROVINCIA DI NAPOLI	63	P	2004-07-14 10:25:21
064	AV	PROVINCIA DI AVELLINO	64	P	2004-07-14 10:25:21
065	SA	PROVINCIA DI SALERNO	65	P	2004-07-14 10:25:21
066	AQ	PROVINCIA DI L'AQUILA	66	Q	2004-07-14 10:25:21
067	TE	PROVINCIA DI TERAMO	67	Q	2004-07-14 10:25:21
068	PE	PROVINCIA DI PESCARA	68	Q	2004-07-14 10:25:21
069	CH	PROVINCIA DI CHIETI	69	Q	2004-07-14 10:25:21
070	CB	PROVINCIA DI CAMPOBASSO	70	R	2004-07-14 10:25:21
071	FG	PROVINCIA DI FOGGIA	71	S	2004-07-14 10:25:21
072	BA	PROVINCIA DI BARI	72	S	2004-07-14 10:25:21
073	TA	PROVINCIA DI TARANTO	73	S	2004-07-14 10:25:21
074	BR	PROVINCIA DI BRINDISI	74	S	2004-07-14 10:25:21
075	LE	PROVINCIA DI LECCE	75	S	2004-07-14 10:25:21
076	PZ	PROVINCIA DI POTENZA	76	T	2004-07-14 10:25:21
077	MT	PROVINCIA DI MATERA	77	T	2004-07-14 10:25:21
078	CS	PROVINCIA DI COSENZA	78	U	2004-07-14 10:25:21
079	CZ	PROVINCIA DI CATANZARO	79	U	2004-07-14 10:25:21
080	RC	PROVINCIA DI REGGIO DI CALABRIA	80	U	2004-07-14 10:25:21
081	TP	PROVINCIA DI TRAPANI	81	V	2004-07-14 10:25:21
082	PA	PROVINCIA DI PALERMO	82	V	2004-07-14 10:25:21
083	ME	PROVINCIA DI MESSINA	83	V	2004-07-14 10:25:21
084	AG	PROVINCIA DI AGRIGENTO	84	V	2004-07-14 10:25:21
085	CL	PROVINCIA DI CALTANISSETTA	85	V	2004-07-14 10:25:21
086	EN	PROVINCIA DI ENNA	86	V	2004-07-14 10:25:21
087	CT	PROVINCIA DI CATANIA	87	V	2004-07-14 10:25:21
088	RG	PROVINCIA DI RAGUSA	88	V	2004-07-14 10:25:22
089	SR	PROVINCIA DI SIRACUSA	89	V	2004-07-14 10:25:22
090	SS	PROVINCIA DI SASSARI	90	Z	2004-07-14 10:25:22
091	NU	PROVINCIA DI NUORO	91	Z	2004-07-14 10:25:22
092	CA	PROVINCIA DI CAGLIARI	92	Z	2004-07-14 10:25:22
093	PN	PROVINCIA DI PORDENONE	93	G	2004-07-14 10:25:22
094	IS	PROVINCIA DI ISERNIA	94	R	2004-07-14 10:25:22
095	OR	PROVINCIA DI ORISTANO	95	Z	2004-07-14 10:25:22
096	BI	PROVINCIA DI BIELLA	\N	A	2004-07-14 10:25:22
097	LC	PROVINCIA DI LECCO	\N	D	2004-07-14 10:25:22
098	LO	PROVINCIA DI LODI	\N	D	2004-07-14 10:25:22
099	RN	PROVINCIA DI RIMINI	\N	I	2004-07-14 10:25:22
100	PO	PROVINCIA DI PRATO	\N	M	2004-07-14 10:25:22
101	KR	PROVINCIA DI CROTONE	\N	U	2004-07-14 10:25:22
102	VV	PROVINCIA DI VIBO VALENTIA	\N	U	2004-07-14 10:25:22
103	VB	PROVINCIA DEL VERBANO CUSIO OSSOLA	\N	A	2004-07-14 10:25:22
001	TO	PROVINCIA DI TORINO	01	A	2004-07-14 10:25:21
002	VC	PROVINCIA DI VERCELLI	02	A	2004-07-14 10:25:21
003	NO	PROVINCIA DI NOVARA	03	A	2004-07-14 10:25:21
004	CN	PROVINCIA DI CUNEO	04	A	2004-07-14 10:25:21
005	AT	PROVINCIA DI ASTI	05	A	2004-07-14 10:25:21
006	AL	PROVINCIA DI ALESSANDRIA	06	A	2004-07-14 10:25:21
007	AO	PROVINCIA DI AOSTA	07	B	2004-07-14 10:25:21
008	IM	PROVINCIA DI IMPERIA	08	C	2004-07-14 10:25:21
009	SV	PROVINCIA DI SAVONA	09	C	2004-07-14 10:25:21
010	GE	PROVINCIA DI GENOVA	10	C	2004-07-14 10:25:21
011	SP	PROVINCIA DI LA SPEZIA	11	C	2004-07-14 10:25:21
012	VA	PROVINCIA DI VARESE	12	D	2004-07-14 10:25:21
013	CO	PROVINCIA DI COMO	13	D	2004-07-14 10:25:21
014	SO	PROVINCIA DI SONDRIO	14	D	2004-07-14 10:25:21
015	MI	PROVINCIA DI MILANO	15	D	2004-07-14 10:25:21
016	BG	PROVINCIA DI BERGAMO	16	D	2004-07-14 10:25:21
017	BS	PROVINCIA DI BRESCIA	17	D	2004-07-14 10:25:21
018	PV	PROVINCIA DI PAVIA	18	D	2004-07-14 10:25:21
019	CR	PROVINCIA DI CREMONA	19	D	2004-07-14 10:25:21
020	MN	PROVINCIA DI MANTOVA	20	D	2004-07-14 10:25:21
021	BZ	PROVINCIA DI BOLZANO - BOZEN	21	E	2004-07-14 10:25:21
022	TN	PROVINCIA DI TRENTO	22	E	2004-07-14 10:25:21
023	VR	PROVINCIA DI VERONA	23	F	2004-07-14 10:25:21
024	VI	PROVINCIA DI VICENZA	24	F	2004-07-14 10:25:21
025	BL	PROVINCIA DI BELLUNO	25	F	2004-07-14 10:25:21
026	TV	PROVINCIA DI TREVISO	26	F	2004-07-14 10:25:21
027	VE	PROVINCIA DI VENEZIA	27	F	2004-07-14 10:25:21
999	ZZ	ZZZ	\N	\N	2014-04-03 15:11:33
---	--	---	\N	\N	2014-04-03 15:12:46
108	MB	PROVINCIA DI MONZA E DELLA BRIANZA	\N	D	2017-02-22 08:33:29
109	FM	PROVINCIA DI FERMO	\N	L	2017-02-22 08:33:29
110	BT	PROVINCIA DI BARLETTA-ANDRIA-TRANI	\N	S	2017-02-22 08:33:29
111	-	PROVINCIA DEL SUD SARDEGNA	\N	Z	2017-02-22 08:33:29
\.


--
-- Name: provincia_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace: 
--

ALTER TABLE ONLY public.provincia
    ADD CONSTRAINT provincia_pkey PRIMARY KEY (codice_istat_prov);


--
-- Name: provincia_fkey001; Type: FK CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.provincia
    ADD CONSTRAINT provincia_fkey001 FOREIGN KEY (codice_istat_reg) REFERENCES public.regione(codice_istat_reg) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: TABLE provincia; Type: ACL; Schema: public; Owner: weboll
--



--
-- PostgreSQL database dump complete
--
