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
-- Name: soglie_pluv_area_prev_massimi; Type: TABLE; Schema: public; Owner: weboll; Tablespace: 
--

CREATE TABLE public.soglie_pluv_area_prev_massimi (
    idtab_allertamento character varying(6) NOT NULL,
    codice_allertamento character varying(1) NOT NULL,
    h1 numeric(5,1),
    h3 numeric(5,1),
    h6 numeric(5,1),
    h12 numeric(5,1),
    h24 numeric(5,1),
    data_agg date NOT NULL,
    autore_agg character varying(30)
);


ALTER TABLE public.soglie_pluv_area_prev_massimi OWNER TO weboll;

--
-- Name: TABLE soglie_pluv_area_prev_massimi; Type: COMMENT; Schema: public; Owner: weboll
--

COMMENT ON TABLE public.soglie_pluv_area_prev_massimi IS 'La tavola contiene le soglie di pioggia per area di allertamento, da 1 a 24 ore da usare come valore massimo sull''area';


--
-- Data for Name: soglie_pluv_area_prev_massimi; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.soglie_pluv_area_prev_massimi (idtab_allertamento, codice_allertamento, h1, h3, h6, h12, h24, data_agg, autore_agg) FROM stdin;
Piem-A	3	\N	\N	125.0	180.0	255.0	2018-10-22	weboll
Piem-B	3	\N	\N	120.0	170.0	240.0	2018-10-22	weboll
Piem-C	3	\N	\N	100.0	140.0	200.0	2018-10-22	weboll
Piem-D	3	\N	\N	80.0	115.0	165.0	2018-10-22	weboll
Piem-E	3	\N	\N	80.0	105.0	150.0	2018-10-22	weboll
Piem-F	3	\N	\N	90.0	120.0	160.0	2018-10-22	weboll
Piem-F	1	32.0	47.0	50.0	65.0	85.0	2018-10-22	weboll
Piem-F	2	44.0	65.0	65.0	85.0	120.0	2018-10-22	weboll
Piem-G	3	\N	\N	110.0	140.0	175.0	2018-10-22	weboll
Piem-G	1	39.0	51.0	55.0	70.0	90.0	2018-10-22	weboll
Piem-G	2	55.0	75.0	75.0	100.0	125.0	2018-10-22	weboll
Piem-H	3	\N	\N	110.0	140.0	180.0	2018-10-22	weboll
Piem-H	1	40.0	52.0	55.0	70.0	90.0	2018-10-22	weboll
Piem-H	2	57.0	77.0	80.0	100.0	130.0	2018-10-22	weboll
Piem-I	3	\N	\N	90.0	110.0	135.0	2018-10-22	weboll
Piem-I	1	40.0	49.0	50.0	60.0	75.0	2018-10-22	weboll
Piem-I	2	53.0	67.0	70.0	85.0	100.0	2018-10-22	weboll
Piem-L	3	\N	\N	85.0	105.0	125.0	2018-10-22	weboll
Piem-L	1	37.0	45.0	45.0	55.0	70.0	2018-10-22	weboll
Piem-L	2	50.0	62.0	65.0	80.0	95.0	2018-10-22	weboll
Piem-M	3	\N	\N	80.0	100.0	125.0	2018-10-22	weboll
Piem-M	1	33.0	43.0	45.0	55.0	70.0	2018-10-22	weboll
Piem-M	2	45.0	60.0	60.0	75.0	95.0	2018-10-22	weboll
Piem-A	4	72.0	126.0	180.0	280.0	365.0	2021-06-08	weboll
Piem-B	4	68.0	118.0	165.0	240.0	335.0	2021-06-08	weboll
Piem-C	4	57.0	100.0	145.0	205.0	290.0	2021-06-08	weboll
Piem-D	4	49.0	85.0	120.0	170.0	240.0	2021-06-08	weboll
Piem-E	4	45.0	77.0	105.0	150.0	210.0	2021-06-08	weboll
Piem-F	4	63.0	99.0	130.0	175.0	230.0	2021-06-08	weboll
Piem-G	4	81.0	120.0	155.0	200.0	255.0	2021-06-08	weboll
Piem-H	4	83.0	123.0	160.0	205.0	260.0	2021-06-08	weboll
Piem-I	4	75.0	103.0	125.0	155.0	190.0	2021-06-08	weboll
Piem-L	4	70.0	97.0	120.0	145.0	175.0	2021-06-08	weboll
Piem-M	4	64.0	92.0	115.0	145.0	180.0	2021-06-08	weboll
Piem-A	1	37.0	65.0	65.0	95.0	135.0	2018-10-22	weboll
Piem-A	2	50.0	89.0	90.0	130.0	190.0	2018-10-22	weboll
Piem-B	1	35.0	61.0	65.0	90.0	130.0	2018-10-22	weboll
Piem-B	2	48.0	83.0	85.0	125.0	175.0	2018-10-22	weboll
Piem-C	1	29.0	51.0	55.0	75.0	105.0	2018-10-22	weboll
Piem-C	2	40.0	70.0	75.0	105.0	145.0	2018-10-22	weboll
Piem-D	1	24.0	42.0	45.0	60.0	85.0	2018-10-22	weboll
Piem-D	2	34.0	59.0	60.0	85.0	120.0	2018-10-22	weboll
Piem-E	1	24.0	40.0	40.0	60.0	80.0	2018-10-22	weboll
Piem-E	2	32.0	54.0	60.0	80.0	110.0	2018-10-22	weboll
\.


--
-- Name: soglie_pluv_area_prev_massimi_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace: 
--

ALTER TABLE ONLY public.soglie_pluv_area_prev_massimi
    ADD CONSTRAINT soglie_pluv_area_prev_massimi_pkey PRIMARY KEY (idtab_allertamento, codice_allertamento);


--
-- Name: TABLE soglie_pluv_area_prev_massimi; Type: ACL; Schema: public; Owner: weboll
--



--
-- PostgreSQL database dump complete
--

