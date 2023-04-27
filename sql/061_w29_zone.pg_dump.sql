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

--
-- Name: w29_zone; Type: TABLE; Schema: public; Owner: weboll; Tablespace:
--

CREATE TABLE public.w29_zone (
    id_w29_zone integer NOT NULL,
    descrizione character varying(30) NOT NULL
);


ALTER TABLE public.w29_zone OWNER TO weboll;

--
-- Data for Name: w29_zone; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.w29_zone (id_w29_zone, descrizione) FROM stdin;
1	A
2	B
3	C
4	D
5	E
6	F
7	G
8	H
9	I
10	L
11	M
\.


--
-- Name: w29_zone_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace:
--

ALTER TABLE ONLY public.w29_zone
    ADD CONSTRAINT w29_zone_pkey PRIMARY KEY (id_w29_zone);


--
-- Name: TABLE w29_zone; Type: ACL; Schema: public; Owner: weboll
--



--
-- PostgreSQL database dump complete
--
