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
-- Name: soglie_pluv_area_prev_medie; Type: TABLE; Schema: public; Owner: weboll; Tablespace: 
--

CREATE TABLE public.soglie_pluv_area_prev_medie (
    idtab_allertamento character varying(6) NOT NULL,
    codice_allertamento character varying(1) NOT NULL,
    h6 numeric(5,1),
    h12 numeric(5,1),
    h24 numeric(5,1),
    h48 numeric(5,1),
    h72 numeric(5,1),
    data_agg date NOT NULL,
    autore_agg character varying(30)
);


ALTER TABLE public.soglie_pluv_area_prev_medie OWNER TO weboll;

--
-- Name: TABLE soglie_pluv_area_prev_medie; Type: COMMENT; Schema: public; Owner: weboll
--

COMMENT ON TABLE public.soglie_pluv_area_prev_medie IS 'La tavola contiene le soglie di pioggia per area di allertamento, da 6 a 72 ore da usare come valore medio sull''area';


--
-- Data for Name: soglie_pluv_area_prev_medie; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.soglie_pluv_area_prev_medie (idtab_allertamento, codice_allertamento, h6, h12, h24, h48, h72, data_agg, autore_agg) FROM stdin;
Piem-A	2	75.0	110.0	160.0	235.0	300.0	2018-11-14	weboll
Piem-E	1	35.0	45.0	65.0	95.0	120.0	2018-11-14	weboll
Piem-E	2	45.0	65.0	95.0	130.0	165.0	2018-10-22	weboll
Piem-E	3	60.0	85.0	125.0	180.0	225.0	2018-10-22	weboll
Piem-F	1	40.0	50.0	70.0	95.0	115.0	2018-10-22	weboll
Piem-F	2	55.0	75.0	100.0	135.0	165.0	2018-10-22	weboll
Piem-F	3	75.0	100.0	140.0	185.0	225.0	2018-10-22	weboll
Piem-G	1	40.0	55.0	70.0	95.0	110.0	2018-10-22	weboll
Piem-G	2	60.0	80.0	105.0	140.0	165.0	2018-10-22	weboll
Piem-G	3	80.0	110.0	150.0	195.0	230.0	2018-10-22	weboll
Piem-H	1	45.0	55.0	75.0	100.0	120.0	2018-10-22	weboll
Piem-H	2	65.0	85.0	110.0	145.0	170.0	2018-10-22	weboll
Piem-H	3	90.0	120.0	155.0	205.0	245.0	2018-10-22	weboll
Piem-I	1	40.0	50.0	65.0	80.0	90.0	2018-10-22	weboll
Piem-I	2	50.0	65.0	85.0	105.0	125.0	2018-10-22	weboll
Piem-I	3	70.0	90.0	115.0	145.0	165.0	2018-10-22	weboll
Piem-L	1	35.0	45.0	60.0	70.0	85.0	2018-10-22	weboll
Piem-L	2	50.0	60.0	80.0	100.0	115.0	2018-10-22	weboll
Piem-L	3	65.0	85.0	110.0	135.0	155.0	2018-10-22	weboll
Piem-M	1	35.0	45.0	60.0	75.0	90.0	2018-10-22	weboll
Piem-M	2	50.0	65.0	80.0	105.0	125.0	2018-10-22	weboll
Piem-M	3	65.0	85.0	110.0	145.0	170.0	2018-10-22	weboll
Piem-A	1	55.0	80.0	115.0	170.0	215.0	2018-10-22	weboll
Piem-A	3	100.0	150.0	220.0	320.0	410.0	2018-10-22	weboll
Piem-B	1	50.0	75.0	110.0	155.0	200.0	2018-10-22	weboll
Piem-B	2	70.0	100.0	150.0	215.0	275.0	2018-10-22	weboll
Piem-B	3	95.0	140.0	205.0	295.0	375.0	2018-10-22	weboll
Piem-C	1	40.0	60.0	88.0	130.0	165.0	2018-10-22	weboll
Piem-C	2	55.0	85.0	125.0	180.0	230.0	2018-10-22	weboll
Piem-C	3	80.0	115.0	170.0	250.0	320.0	2018-10-22	weboll
Piem-D	1	35.0	50.0	75.0	105.0	135.0	2018-10-22	weboll
Piem-D	2	50.0	70.0	105.0	150.0	190.0	2018-10-22	weboll
Piem-D	3	70.0	100.0	145.0	210.0	265.0	2018-10-22	weboll
\.


--
-- Name: soglie_pluv_area_prev_medie_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace: 
--

ALTER TABLE ONLY public.soglie_pluv_area_prev_medie
    ADD CONSTRAINT soglie_pluv_area_prev_medie_pkey PRIMARY KEY (idtab_allertamento, codice_allertamento);


--
-- Name: TABLE soglie_pluv_area_prev_medie; Type: ACL; Schema: public; Owner: weboll
--



--
-- PostgreSQL database dump complete
--

