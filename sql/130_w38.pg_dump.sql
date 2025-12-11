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

--SET default_with_oids = true;

CREATE OR REPLACE FUNCTION public.w38_numero_bollettino()
 RETURNS character varying
 LANGUAGE plpgsql
AS $function$
BEGIN
  RETURN
  (SELECT COUNT(data_emissione) + 1 || '/' || date_part('year', current_date)
  FROM w38
  WHERE data_emissione >= date_trunc('year', current_date) AND data_emissione < current_date);

END;
$function$
;

--
-- Name: w38; Type: TABLE; Schema: public; Owner: weboll; Tablespace:
--

CREATE TABLE public.w38 (
    id_w38 bigint NOT NULL,
    data_emissione date DEFAULT ('now'::text)::date NOT NULL,
    numero_bollettino character varying(30) DEFAULT public.w38_numero_bollettino() NOT NULL,
    situazione_evoluzione text,
    status character(1) DEFAULT 0 NOT NULL,
    last_update timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(6) with time zone NOT NULL,
    username character varying(30) DEFAULT "current_user"() NOT NULL,
    data_validita date NOT NULL,
    note text
);


ALTER TABLE public.w38 OWNER TO weboll;

--
-- Name: COLUMN w38.status; Type: COMMENT; Schema: public; Owner: weboll
--

COMMENT ON COLUMN public.w38.status IS '0 = Draft; 1 = Final';


--
-- Name: w38_id_w38_seq; Type: SEQUENCE; Schema: public; Owner: weboll
--

CREATE SEQUENCE public.w38_id_w38_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.w38_id_w38_seq OWNER TO weboll;

--
-- Name: w38_id_w38_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: weboll
--

ALTER SEQUENCE public.w38_id_w38_seq OWNED BY public.w38.id_w38;


--
-- Name: id_w38; Type: DEFAULT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w38 ALTER COLUMN id_w38 SET DEFAULT nextval('public.w38_id_w38_seq'::regclass);


--
-- Data for Name: w38; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.w38 (id_w38, data_emissione, numero_bollettino, situazione_evoluzione, status, last_update, username, data_validita, note) FROM stdin;
502	2023-02-17	251/2021		1	2023-02-17 12:01:45	weboll	2023-02-17	-
503	2023-02-18	252/2021		1	2023-02-18 12:11:06	weboll	2023-02-18	-
504	2023-02-19	253/2021		1	2023-02-19 12:06:42	weboll	2023-02-19	-
505	2023-02-20	254/2021		1	2023-02-20 12:06:44	weboll	2023-02-20	-
506	2023-02-21	255/2021		1	2023-02-21 12:04:49	weboll	2023-02-21	-
\.


--
-- Name: w38_id_w38_seq; Type: SEQUENCE SET; Schema: public; Owner: weboll
--

SELECT pg_catalog.setval('public.w38_id_w38_seq', 506, true);

ALTER TABLE public.w38 ADD id_w38_parent INTEGER DEFAULT NULL;

--
-- Name: w38_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace:
--

ALTER TABLE ONLY public.w38
    ADD CONSTRAINT w38_pkey PRIMARY KEY (id_w38);


CREATE TABLE public.w38_dati_ivrea (
	id_w38 bigint NOT NULL,
	--id_venue character varying(6) NOT NULL,
    id_venue integer NOT NULL,
	data_emissione date NULL,
	id_time_layouts integer NOT NULL,
	numeric_value integer NULL,
	CONSTRAINT b_layout_pkey PRIMARY KEY (id_w38)
);

ALTER TABLE public.w38_dati_ivrea OWNER TO weboll;

CREATE SEQUENCE public.w38_dati_ivrea_id_w38_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.w38_dati_ivrea_id_w38_seq OWNER TO weboll;

ALTER SEQUENCE public.w38_dati_ivrea_id_w38_seq OWNED BY public.w38_dati_ivrea.id_w38;

ALTER TABLE ONLY public.w38_dati_ivrea ALTER COLUMN id_w38 SET DEFAULT nextval('public.w38_dati_ivrea_id_w38_seq'::regclass);

COPY public.w38_dati_ivrea (id_w38, id_venue, data_emissione, id_time_layouts, numeric_value) FROM stdin;
1	1	2023-02-22	48	10
2	1	2023-02-22	66	9
3	1	2023-02-22	83	8
4	9	2023-02-22	48	10
5	9	2023-02-22	66	9
6	9	2023-02-22	83	8
7	11	2023-02-22	48	10
8	11	2023-02-22	66	9
9	11	2023-02-22	83	8
10	16	2023-02-22	48	10
11	16	2023-02-22	66	9
12	16	2023-02-22	83	8
13	28	2023-02-22	48	10
14	28	2023-02-22	66	9
15	28	2023-02-22	83	8
16	33	2023-02-22	48	10
17	33	2023-02-22	66	9
18	33	2023-02-22	83	8
19	59	2023-02-22	48	10
20	59	2023-02-22	66	9
21	59	2023-02-22	83	8
22	63	2023-02-22	48	10
23	63	2023-02-22	66	9
24	63	2023-02-22	83	8
25	64	2023-02-22	48	10
26	64	2023-02-22	66	9
27	64	2023-02-22	83	8
28	87	2023-02-22	48	10
29	87	2023-02-22	66	9
30	87	2023-02-22	83	8
31	88	2023-02-22	48	10
32	88	2023-02-22	66	9
33	88	2023-02-22	83	8
34	89	2023-02-22	48	10
35	89	2023-02-22	66	9
36	89	2023-02-22	83	8
37	90	2023-02-22	48	10
38	90	2023-02-22	66	9
39	90	2023-02-22	83	8
40	91	2023-02-22	48	10
41	91	2023-02-22	66	9
42	91	2023-02-22	83	8
43	116	2023-02-22	48	10
44	116	2023-02-22	66	9
45	116	2023-02-22	83	8
46	190	2023-02-22	48	10
47	190	2023-02-22	66	9
48	190	2023-02-22	83	8
49	191	2023-02-22	48	10
50	191	2023-02-22	66	9
51	191	2023-02-22	83	8
52	192	2023-02-22	48	10
53	192	2023-02-22	66	9
54	192	2023-02-22	83	8
55	193	2023-02-22	48	10
56	193	2023-02-22	66	9
57	193	2023-02-22	83	8
58	194	2023-02-22	48	10
59	194	2023-02-22	66	9
60	194	2023-02-22	83	8
61	195	2023-02-22	48	10
62	195	2023-02-22	66	9
63	195	2023-02-22	83	8
101	1	2023-02-23	48	10
102	1	2023-02-23	66	9
103	1	2023-02-23	83	8
104	9	2023-02-23	48	10
105	9	2023-02-23	66	9
106	9	2023-02-23	83	8
107	11	2023-02-23	48	10
108	11	2023-02-23	66	9
109	11	2023-02-23	83	8
110	16	2023-02-23	48	10
111	16	2023-02-23	66	9
112	16	2023-02-23	83	8
113	28	2023-02-23	48	10
114	28	2023-02-23	66	9
115	28	2023-02-23	83	8
116	33	2023-02-23	48	10
117	33	2023-02-23	66	9
118	33	2023-02-23	83	8
119	59	2023-02-23	48	10
120	59	2023-02-23	66	9
121	59	2023-02-23	83	8
122	63	2023-02-23	48	10
123	63	2023-02-23	66	9
124	63	2023-02-23	83	8
125	64	2023-02-23	48	10
126	64	2023-02-23	66	9
127	64	2023-02-23	83	8
128	87	2023-02-23	48	10
129	87	2023-02-23	66	9
130	87	2023-02-23	83	8
131	88	2023-02-23	48	10
132	88	2023-02-23	66	9
133	88	2023-02-23	83	8
134	89	2023-02-23	48	10
135	89	2023-02-23	66	9
136	89	2023-02-23	83	8
137	90	2023-02-23	48	10
138	90	2023-02-23	66	9
139	90	2023-02-23	83	8
140	91	2023-02-23	48	10
141	91	2023-02-23	66	9
142	91	2023-02-23	83	8
143	116	2023-02-23	48	10
144	116	2023-02-23	66	9
145	116	2023-02-23	83	8
146	190	2023-02-23	48	10
147	190	2023-02-23	66	9
148	190	2023-02-23	83	8
149	191	2023-02-23	48	10
150	191	2023-02-23	66	9
151	191	2023-02-23	83	8
152	192	2023-02-23	48	10
153	192	2023-02-23	66	9
154	192	2023-02-23	83	8
155	193	2023-02-23	48	10
156	193	2023-02-23	66	9
157	193	2023-02-23	83	8
158	194	2023-02-23	48	10
159	194	2023-02-23	66	9
160	194	2023-02-23	83	8
161	195	2023-02-23	48	10
162	195	2023-02-23	66	9
163	195	2023-02-23	83	8
\.
--
-- PostgreSQL database dump complete
--
