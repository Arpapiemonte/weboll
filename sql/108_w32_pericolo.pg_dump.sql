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
-- Name: w32_pericolo; Type: TABLE; Schema: public; Owner: weboll; Tablespace:
--

CREATE TABLE public.w32_pericolo (
    id_w32_pericolo character varying(2) NOT NULL,
    descrizione text
);


ALTER TABLE public.w32_pericolo OWNER TO weboll;

--
-- Data for Name: w32_pericolo; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.w32_pericolo (id_w32_pericolo, descrizione) FROM stdin;
np	Non pervenuto
A	Nulla da segnalare
I	Possibili inneschi isolati che interessano limitati settori delle valli alpine principali
P	Possibili inneschi poco diffusi che interessano discreti settori delle valli alpine principali
D	Possibili inneschi  diffusi che interessano estesi settori delle valli alpine principali
\.


--
-- Name: w32_pericolo_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace:
--

ALTER TABLE ONLY public.w32_pericolo
    ADD CONSTRAINT w32_pericolo_pkey PRIMARY KEY (id_w32_pericolo);
