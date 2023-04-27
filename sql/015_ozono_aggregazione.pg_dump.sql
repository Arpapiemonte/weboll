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
-- Name: ozono_aggregazione; Type: TABLE; Schema: public; Owner: weboll; Tablespace: 
--

CREATE TABLE public.ozono_aggregazione (
    id_ozono_aggregazione smallint NOT NULL,
    aggregazione character varying(20) NOT NULL,
    desc_aggregazione_spaziale character varying(30) NOT NULL,
    desc_aggregazione_temporale character varying(60) NOT NULL,
    last_update timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(6) with time zone NOT NULL,
    username character varying(30) DEFAULT "current_user"() NOT NULL
);


ALTER TABLE public.ozono_aggregazione OWNER TO weboll;

--
-- Data for Name: ozono_aggregazione; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.ozono_aggregazione (id_ozono_aggregazione, aggregazione, desc_aggregazione_spaziale, desc_aggregazione_temporale, last_update, username) FROM stdin;
1	mx8_90p	90 percentile	massimo giornaliero della media mobile su otto ore	2010-05-21 16:23:43	weboll
2	mx8_75p	75 percentile	massimo giornaliero della media mobile su otto ore	2010-05-21 16:23:43	weboll
3	mx8_50p	50 percentile	massimo giornaliero della media mobile su otto ore	2010-05-21 16:23:43	weboll
4	mx8_med	media	massimo giornaliero della media mobile su otto ore	2010-05-21 16:23:43	weboll
5	mx8_max	massimo	massimo giornaliero della media mobile su otto ore	2010-05-21 16:23:43	weboll
6	mxd_90p	90 percentile	massimo giornaliero	2010-05-21 16:23:43	weboll
7	mxd_75p	75 percentile	massimo giornaliero	2010-05-21 16:23:43	weboll
8	mxd_50p	50 percentile	massimo giornaliero	2010-05-21 16:23:43	weboll
9	mxd_med	media	massimo giornaliero	2010-06-10 09:32:13	weboll
10	mxd_max	massimo	massimo giornaliero	2010-05-21 16:23:43	weboll
11	90p	90 percentile		2010-06-10 09:41:14	weboll
12	75p	75 percentile		2010-06-10 09:42:50	weboll
13	50p	50 percentile		2010-06-10 09:44:14	weboll
14	media	media		2010-06-16 14:08:28	weboll
15	massimo	massimo		2010-06-16 14:09:50	weboll
\.


--
-- Name: ozono_aggregazione_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace: 
--

ALTER TABLE ONLY public.ozono_aggregazione
    ADD CONSTRAINT ozono_aggregazione_pkey PRIMARY KEY (id_ozono_aggregazione);


--
-- Name: TABLE ozono_aggregazione; Type: ACL; Schema: public; Owner: weboll
--



--
-- PostgreSQL database dump complete
--

