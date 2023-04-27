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
-- Name: w32_pericolombacini; Type: TABLE; Schema: public; Owner: weboll; Tablespace:
--

CREATE TABLE public.w32_pericolombacini (
    id_w32_pericolombacini character varying(2) NOT NULL,
    descrizione text
);


ALTER TABLE public.w32_pericolombacini OWNER TO weboll;

--
-- Data for Name: w32_pericolombacini; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.w32_pericolombacini (id_w32_pericolombacini, descrizione) FROM stdin;
np	Non pervenuto
-	Probabilità di innesco debris flow NO
S	Probabilità di innesco debris flow S
\.


--
-- Name: w32_pericolombacini_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace:
--

ALTER TABLE ONLY public.w32_pericolombacini
    ADD CONSTRAINT w32_pericolombacini_pkey PRIMARY KEY (id_w32_pericolombacini);
