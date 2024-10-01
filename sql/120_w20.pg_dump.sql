CREATE TABLE public.traps_comuni (
    data date,
    comune character varying(80),
    frane_tot smallint,
    frane_sup1 smallint,
    frane_sup2 smallint,
    stato smallint DEFAULT 0,
    codice integer,
    gid integer NOT NULL
);

COMMENT ON TABLE public.traps_comuni IS 'Comuni TRAPS: scivolamenti';

CREATE SEQUENCE public.traps_comuni_gid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE ONLY public.traps_comuni ALTER COLUMN gid SET DEFAULT nextval('public.traps_comuni_gid_seq'::regclass);

COPY public.traps_comuni (data, comune, frane_tot, frane_sup1, frane_sup2, stato, codice, gid) FROM stdin;
2023-05-31	Bene_Vagienna	4	2	0	2	80	82765
2023-05-31	Alba	16	9	0	2	71	82759
2023-05-31	Albaretto_della_Torre	8	1	0	2	72	82760
2023-05-31	Bagnasco	2	2	0	2	74	82761
2023-05-31	Bastia_Mondovi	7	7	0	2	77	82762
2023-05-31	Battifollo	2	2	0	2	78	82763
2023-05-31	Belvedere_Langhe	6	6	0	2	79	82764
2023-05-31	Benevello	4	4	0	2	81	82766
2023-05-31	Bonvicino	13	3	0	2	83	82767
2023-05-31	Borgomale	3	3	0	2	84	82768
2023-05-31	Briaglia	17	17	0	2	87	82769
2023-05-31	Castellino_Tanaro	4	4	0	2	93	82770
2023-05-31	Castelnuovo_di_Ceva	1	1	0	2	94	82771
2023-05-31	Cerretto_Langhe	13	2	0	2	98	82772
2023-05-31	Ceva	30	30	0	2	99	82773
2023-05-31	Ciglie	1	1	0	2	101	82774
2023-05-31	Clavesana	10	5	0	2	103	82775
2023-05-31	Diano_Alba	8	1	0	2	107	82776
2023-05-31	Dogliani	28	7	0	2	108	82777
2023-05-31	Farigliano	11	5	0	2	109	82778
2023-05-31	Grinzane_Cavour	5	1	0	2	114	82779
2023-05-31	Igliano	5	5	0	2	116	82780
2023-05-31	Lequio_Berria	6	6	0	2	118	82781
2023-05-31	Lesegno	4	4	0	2	120	82782
2023-05-31	Marsaglia	8	7	0	2	124	82783
2023-05-31	Mombasiglio	19	19	0	2	126	82784
2023-05-31	Monastero_di_Vasco	5	5	5	3	127	82785
2023-05-31	Mondovi	21	21	7	3	129	82786
2023-05-31	Montezemolo	11	1	0	2	133	82787
2023-05-31	Murazzano	29	17	0	2	134	82788
2023-05-31	Neviglie	5	1	0	2	137	82789
2023-05-31	Niella_Tanaro	6	6	0	2	139	82790
2023-05-31	Paroldo	6	1	0	2	141	82791
2023-05-31	Priero	9	9	0	2	146	82792
2023-05-31	Roascio	5	5	0	2	149	82793
2023-05-31	Rocca_Ciglie	6	6	0	2	150	82794
2023-05-31	Roddi	9	1	0	2	152	82795
2023-05-31	Roddino	12	1	0	2	153	82796
2023-05-31	Rodello	7	3	0	2	154	82797
2023-05-31	Sale_delle_Langhe	27	20	0	2	155	82798
2023-05-31	Sale_San_Giovanni	5	4	0	2	156	82799
2023-05-31	San_Michele_Mondovi	12	12	0	2	159	82800
2023-05-31	Scagnello	5	5	0	2	161	82801
2023-05-31	Torresina	3	3	0	2	167	82802
2023-05-31	Treiso	11	10	0	2	168	82803
2023-05-31	Trezzo_Tinella	9	8	0	2	169	82804
2023-05-31	Vicoforte	43	43	32	3	172	82805
\.

SELECT pg_catalog.setval('public.traps_comuni_gid_seq', 82805, true);

ALTER TABLE ONLY public.traps_comuni
    ADD CONSTRAINT traps_comuni_data_key UNIQUE (data, comune);

ALTER TABLE ONLY public.traps_comuni
    ADD CONSTRAINT traps_comuni_pkey PRIMARY KEY (gid);

CREATE OR REPLACE FUNCTION public.w20_numero_bollettino()
 RETURNS character varying
 LANGUAGE plpgsql
AS $function$
BEGIN
  RETURN
  (SELECT COUNT(data_emissione) + 1 || '/' || date_part('year', current_date)
  FROM w20
  WHERE data_emissione >= date_trunc('year', current_date) AND data_emissione < current_date);

END;
$function$
;

CREATE TABLE public.w20 (
    id_w20 bigint NOT NULL,
	data_emissione date NOT NULL DEFAULT 'now'::text::date,
	numero_bollettino varchar(30) NOT NULL DEFAULT w20_numero_bollettino(),
    status character(1) DEFAULT 0 NOT NULL,
    last_update timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(6) with time zone NOT NULL,
    username character varying(30) DEFAULT "current_user"() NOT NULL,
	pioggia_infiltrata bytea NULL,
	neve_equivalente bytea NULL
);

COMMENT ON COLUMN public.w20.status IS '0 = Draft; 1 = Final';

CREATE SEQUENCE public.w20_id_w20_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE ONLY public.w20 ALTER COLUMN id_w20 SET DEFAULT nextval('public.w20_id_w20_seq'::regclass);

ALTER TABLE ONLY public.w20
    ADD CONSTRAINT w20_pkey PRIMARY KEY (id_w20);


CREATE TABLE public.w20_data (
	id_w20 bigint NOT NULL,
    id_w20_zone integer NOT NULL,
    id_w20_data serial NOT NULL,
	provincia varchar(100) NOT NULL,
	comune varchar(100) NOT NULL,
	if_perc varchar(100) NOT NULL,
	prob_innesco varchar(100) NOT NULL
);

ALTER TABLE ONLY public.w20_data
    ADD CONSTRAINT w20_data_unique UNIQUE (id_w20, provincia, comune);

ALTER TABLE ONLY public.w20_data
    ADD CONSTRAINT w20_data_pkey PRIMARY KEY (id_w20_data);

ALTER TABLE ONLY public.w20_data
    ADD CONSTRAINT w20_data_fkey001 FOREIGN KEY (id_w20) REFERENCES public.w20(id_w20) ON UPDATE CASCADE ON DELETE CASCADE;

CREATE TABLE public.w20_pericolo (
    id_w20_pericolo character varying(10) NOT NULL,
    descrizione text
);

CREATE TABLE public.w20_zone (
    id_w20_zone integer NOT NULL,
    comune varchar(30) NOT NULL,
    provincia varchar(20) NOT NULL,
	if_perc varchar(10) NULL
);

ALTER TABLE ONLY public.w20_zone
    ADD CONSTRAINT w20_zone_pkey PRIMARY KEY (id_w20_zone);


COPY public.w20_zone (id_w20_zone, comune, provincia, if_perc) FROM stdin;
0	Acqui Terme	AL	4.01
1	Alice Bel Colle	AL	3.40
2	Bistagno	AL	5.55
3	Cartosio	AL	0.80
4	Cassine	AL	4.80
5	Castelletto d'Erro	AL	22.55
6	Cavatore	AL	4.01
7	Cremolino	AL	4.03
8	Denice	AL	2.36
9	Grognardo	AL	4.01
10	Melazzo	AL	4.01
11	Merana	AL	1.48
12	Montechiaro d'Acqui	AL	22.55
13	Orsara Bormida	AL	0.27
14	Ovada	AL	4.03
15	Ponti	AL	6.80
16	Ponzone	AL	0.80
17	Prasco	AL	4.03
18	Ricaldone	AL	0.27
19	Spigno Monferrato	AL	2.36
20	Strevi	AL	0.27
21	Terzo	AL	4.01
22	Visone	AL	4.01
23	Agliano	AT	0.16
24	Antignano	AT	0.20
25	ASTI	AT	0.58
26	Azzano d'Asti	AT	0.58
27	Bruno	AT	1.18
28	Bubbio	AT	2.68
29	Calamandrana	AT	2.97
30	Calosso	AT	1.13
31	Canelli	AT	1.13
32	Cassinasco	AT	2.97
33	Castagnole delle Lanze	AT	0.17
34	Castel Boglione	AT	4.37
35	Castel Rocchero	AT	4.37
36	Castelletto Molina	AT	3.26
37	Castelnuovo Belbo	AT	1.18
38	Castelnuovo Calcea	AT	0.16
39	Cessole	AT	2.36
40	Coazzolo	AT	4.27
41	Cortiglione	AT	1.78
42	Costigliole d'Asti	AT	1.19
43	Fontanile	AT	16.29
44	Incisa Scapaccino	AT	1.73
45	Isola d'Asti	AT	0.58
46	Loazzolo	AT	0.54
47	Maranzana	AT	4.80
48	Moasca	AT	0.29
49	Mombaldone	AT	2.36
50	Mombaruzzo	AT	7.00
51	Mombercelli	AT	0.09
52	Monastero Bormida	AT	2.36
53	Montabone	AT	4.01
54	Montaldo Scarampi	AT	0.16
55	Montegrosso d'Asti	AT	1.19
56	Nizza Monferrato	AT	16.29
57	Olmo Gentile	AT	2.36
58	Quaranti	AT	3.26
59	Revigliasco d'Asti	AT	0.58
60	Roccaverano	AT	2.36
61	Rocchetta Palafea	AT	23.75
62	Rocchetta Tanaro	AT	0.18
63	San Giorgio Scarampi	AT	2.36
64	San Martino Alfieri	AT	1.32
65	San Marzano Oliveto	AT	0.23
66	Serole	AT	2.36
67	Sessame	AT	1.84
68	Vaglio Serra	AT	3.20
69	Vesime	AT	0.42
70	Vinchio	AT	7.00
71	Alba	CN	3.88
72	Albaretto della Torre	CN	7.69
73	Arguello	CN	38.36
74	Bagnasco	CN	1.08
75	Barbaresco	CN	0.85
76	Barolo	CN	12.76
77	Bastia Mondovi'	CN	4.05
78	Battifollo	CN	1.08
79	Belvedere Langhe	CN	3.42
80	Bene Vagienna	CN	11.42
81	Benevello	CN	3.88
82	Bergolo	CN	0.98
83	Bonvicino	CN	3.42
84	Borgomale	CN	3.88
85	Bosia	CN	0.98
86	Bossolasco	CN	4.78
87	Briaglia	CN	2.39
88	Camerana	CN	5.25
89	Camo	CN	4.27
90	Castagnito	CN	0.85
91	Castelletto Uzzone	CN	3.76
92	Castellinaldo	CN	0.33
93	Castellino Tanaro	CN	3.14
94	Castelnuovo di Ceva	CN	17.38
95	Castiglione Falletto	CN	0.87
96	Castiglione Tinella	CN	0.17
97	Castino	CN	0.98
98	Cerretto Langhe	CN	38.36
99	Ceva	CN	2.06
100	Cherasco	CN	19.32
101	Ciglie'	CN	4.05
102	Cissone	CN	10.61
103	Clavesana	CN	3.14
104	Cortemilia	CN	0.98
105	Cossano Belbo	CN	0.42
106	Cravanzana	CN	3.97
107	Diano d'Alba	CN	3.88
108	Dogliani	CN	3.42
109	Farigliano	CN	2.73
110	Feisoglio	CN	4.78
111	Gorzegno	CN	4.78
112	Gottasecca	CN	3.76
113	Govone	CN	1.32
114	Grinzane Cavour	CN	5.50
115	Guarene	CN	1.20
116	Igliano	CN	2.78
117	La Morra	CN	0.87
118	Lequio Berria	CN	7.69
119	Lequio Tanaro	CN	1.42
120	Lesegno	CN	2.78
121	Levice	CN	2.48
122	Magliano Alfieri	CN	0.85
123	Mango	CN	1.07
124	Marsaglia	CN	3.14
125	Mombarcaro	CN	4.20
126	Mombasiglio	CN	3.67
127	Monastero di Vasco	CN	18.63
128	Monchiero	CN	3.58
129	Mondovi'	CN	4.05
130	Monesiglio	CN	3.76
131	Monforte d'Alba	CN	3.58
132	Montelupo Albese	CN	2.16
133	Montezemolo	CN	5.25
134	Murazzano	CN	2.73
135	Narzole	CN	19.32
136	Neive	CN	4.27
137	Neviglie	CN	4.37
138	Niella Belbo	CN	4.78
139	Niella Tanaro	CN	4.05
140	Novello	CN	3.88
141	Paroldo	CN	2.06
142	Perletto	CN	0.98
143	Pezzolo valle Uzzone	CN	0.98
144	Piobesi d'Alba	CN	12.36
145	Piozzo	CN	1.42
146	Priero	CN	17.38
147	Priocca	CN	0.86
148	Prunetto	CN	2.48
149	Roascio	CN	2.06
150	Rocca Ciglie'	CN	4.05
151	Rocchetta Belbo	CN	1.07
152	Roddi	CN	0.87
153	Roddino	CN	3.58
154	Rodello	CN	5.15
155	Sale delle Langhe	CN	1.34
156	Sale San Giovanni	CN	1.34
157	Saliceto	CN	5.25
158	San Benedetto Belbo	CN	3.48
159	San Michele Mondovi'	CN	5.92
160	Santo Stefano Belbo	CN	2.68
161	Scagnello	CN	3.67
162	Serralunga d'Alba	CN	2.16
163	Serravalle Langhe	CN	4.78
164	Sinio	CN	6.08
165	Somano	CN	3.58
166	Torre Bormida	CN	0.98
167	Torresina	CN	2.06
168	Treiso	CN	4.37
169	Trezzo Tinella	CN	2.04
170	Verduno	CN	19.32
171	Vezza d'Alba	CN	2.82
172	Vicoforte	CN	5.70
\.


COPY public.w20_pericolo (id_w20_pericolo, descrizione) FROM stdin;
A	Probabilita' di attivazione assente
B	Probabilita' di attivazione bassa - possibili  movimenti registrati dalle rete di monitoraggio (ove presente) senza espressioni morfologiche superficiali; attivazioni allo stadio incipiente (comparsa di evidenze morfologiche superficiali: rigonfiamenti, avvallamenti, trincee e fratture sui versanti); peggioramento di stadi incipienti pregressi
E	Probabilita' di attivazione elevata - possibili attivazioni parossistiche con scivolamento di porzioni di versante; attivazioni allo stadio incipiente (comparsa di evidenze morfologiche superficiali: rigonfiamenti, avvallamenti, trincee e fratture sui versanti); peggioramento di stadi incipienti pregressi
\.

\set command `echo "curl $DATA_LOCATION/w20.copy"`
COPY w20(id_w20,data_emissione,numero_bollettino,status,last_update,username,pioggia_infiltrata,neve_equivalente) 
  FROM PROGRAM :'command' CSV HEADER DELIMITER ',' ;
\set command `echo "curl $DATA_LOCATION/w20_data.copy"`
COPY w20_data(id_w20,id_w20_zone,id_w20_data,provincia,comune,if_perc,prob_innesco) 
  FROM PROGRAM :'command' CSV HEADER;
