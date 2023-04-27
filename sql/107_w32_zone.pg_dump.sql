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
-- Name: w32_zone; Type: TABLE; Schema: public; Owner: weboll; Tablespace:
--

CREATE TABLE public.w32_zone (
    id_w32_zone integer NOT NULL,
    descrizione character varying(30) NOT NULL
);


ALTER TABLE public.w32_zone OWNER TO weboll;

--
-- Data for Name: w32_zone; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.w32_zone (id_w32_zone, descrizione) FROM stdin;
1	A
2	B
3	C
4	D
5	E
6	F
\.


--
-- Name: w32_zone_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace:
--

ALTER TABLE ONLY public.w32_zone
    ADD CONSTRAINT w32_zone_pkey PRIMARY KEY (id_w32_zone);
--
