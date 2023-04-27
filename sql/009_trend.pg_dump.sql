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
-- Name: trend; Type: TABLE; Schema: public; Owner: weboll; Tablespace: 
--

CREATE TABLE public.trend (
    id_trend smallint NOT NULL,
    id_web smallint NOT NULL,
    desc_ita character varying(50),
    desc_eng character varying(50),
    last_update timestamp without time zone DEFAULT ('now'::text)::timestamp(6) with time zone NOT NULL,
    username character varying(30) DEFAULT "current_user"() NOT NULL
);


ALTER TABLE public.trend OWNER TO weboll;

--
-- Data for Name: trend; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.trend (id_trend, id_web, desc_ita, desc_eng, last_update, username) FROM stdin;
0	0	Stazionario	Steady	2006-11-13 12:58:20	weboll
1	1	In Aumento	Increasing	2006-11-13 12:58:20	weboll
2	-1	In Diminuzione	Decreasing	2006-11-13 12:58:20	weboll
\.


--
-- Name: trend_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace: 
--

ALTER TABLE ONLY public.trend
    ADD CONSTRAINT trend_pkey PRIMARY KEY (id_trend);


--
-- Name: TABLE trend; Type: ACL; Schema: public; Owner: weboll
--



--
-- PostgreSQL database dump complete
--

