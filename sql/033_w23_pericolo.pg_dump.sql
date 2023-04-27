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
-- Name: w23_pericolo; Type: TABLE; Schema: public; Owner: weboll; Tablespace:
--

CREATE TABLE public.w23_pericolo (
    id_w23_pericolo character varying(10) NOT NULL,
    colore_html character varying(30) NOT NULL,
    sort_index integer NOT NULL
);


ALTER TABLE public.w23_pericolo OWNER TO weboll;

--
-- Data for Name: w23_pericolo; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.w23_pericolo (id_w23_pericolo, colore_html, sort_index) FROM stdin;
ROSSO	#FF0000	5
ARANCIONE	#FFA500	4
GIALLO	#FFFF00	3
VERDE	#6EBB00	2
BIANCO	#ffffff	1
\.


--
-- Name: w23_pericolo_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace:
--

ALTER TABLE ONLY public.w23_pericolo
    ADD CONSTRAINT w23_pericolo_pkey PRIMARY KEY (id_w23_pericolo);


--
-- Name: TABLE w23_pericolo; Type: ACL; Schema: public; Owner: weboll
--



--
-- PostgreSQL database dump complete
--
