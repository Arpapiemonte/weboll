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
-- Name: soglie_nivo_area_prev; Type: TABLE; Schema: public; Owner: weboll; Tablespace: 
--

CREATE TABLE public.soglie_nivo_area_prev (
    idtab_allertamento character varying(6) NOT NULL,
    ambito character varying(10) NOT NULL,
    soglia_cod1 numeric(5,1),
    soglia_cod2 numeric(5,1),
    soglia_cod3 numeric(5,1),
    data_agg date NOT NULL,
    autore_agg character varying(30)
);


ALTER TABLE public.soglie_nivo_area_prev OWNER TO weboll;

--
-- Data for Name: soglie_nivo_area_prev; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.soglie_nivo_area_prev (idtab_allertamento, ambito, soglia_cod1, soglia_cod2, soglia_cod3, data_agg, autore_agg) FROM stdin;
Piem-A	pianura	10.0	20.0	40.0	2014-06-18	weboll
Piem-A	collina	20.0	40.0	60.0	2014-06-18	weboll
Piem-A	montagna 	40.0	70.0	100.0	2014-06-18	weboll
Piem-B	pianura	999.0	999.0	999.0	2014-06-18	weboll
Piem-B	collina	20.0	40.0	60.0	2014-06-18	weboll
Piem-B	montagna 	40.0	70.0	100.0	2014-06-18	weboll
Piem-C	pianura	999.0	999.0	999.0	2014-06-18	weboll
Piem-C	collina	20.0	40.0	60.0	2014-06-18	weboll
Piem-C	montagna 	40.0	70.0	100.0	2014-06-18	weboll
Piem-D	pianura	999.0	999.0	999.0	2014-06-18	weboll
Piem-D	collina	20.0	40.0	60.0	2014-06-18	weboll
Piem-D	montagna 	40.0	70.0	100.0	2014-06-18	weboll
Piem-E	pianura	999.0	999.0	999.0	2014-06-18	weboll
Piem-E	collina	20.0	40.0	60.0	2014-06-18	weboll
Piem-E	montagna 	40.0	70.0	100.0	2014-06-18	weboll
Piem-F	pianura	10.0	20.0	40.0	2014-06-18	weboll
Piem-F	collina	20.0	40.0	60.0	2014-06-18	weboll
Piem-F	montagna 	40.0	70.0	100.0	2014-06-18	weboll
Piem-G	pianura	10.0	20.0	40.0	2014-06-18	weboll
Piem-G	collina	20.0	40.0	60.0	2014-06-18	weboll
Piem-G	montagna 	999.0	999.0	999.0	2014-06-18	weboll
Piem-H	pianura	10.0	20.0	40.0	2014-06-18	weboll
Piem-H	collina	20.0	40.0	60.0	2014-06-18	weboll
Piem-H	montagna 	999.0	999.0	999.0	2014-06-18	weboll
Piem-I	pianura	10.0	20.0	40.0	2014-06-18	weboll
Piem-I	collina	999.0	999.0	999.0	2014-06-18	weboll
Piem-I	montagna 	999.0	999.0	999.0	2014-06-18	weboll
Piem-L	pianura	10.0	20.0	40.0	2014-06-18	weboll
Piem-L	collina	999.0	999.0	999.0	2014-06-18	weboll
Piem-L	montagna 	999.0	999.0	999.0	2014-06-18	weboll
Piem-M	pianura	10.0	20.0	40.0	2014-06-18	weboll
Piem-M	collina	20.0	40.0	60.0	2014-06-18	weboll
Piem-M	montagna 	999.0	999.0	999.0	2014-06-18	weboll
\.


--
-- Name: soglie_nivo_area_prev_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace: 
--

ALTER TABLE ONLY public.soglie_nivo_area_prev
    ADD CONSTRAINT soglie_nivo_area_prev_pkey PRIMARY KEY (idtab_allertamento, ambito);


--
-- Name: TABLE soglie_nivo_area_prev; Type: ACL; Schema: public; Owner: weboll
--



--
-- PostgreSQL database dump complete
--

