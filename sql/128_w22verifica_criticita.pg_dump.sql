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
-- Name: w22verifica_criticita; Type: TABLE; Schema: public; Owner: weboll; Tablespace:
--

CREATE TABLE public.w22verifica_criticita (
    id_w22_criticita character varying(2) NOT NULL,
    descrizione text,
    colore_html character varying(30) NOT NULL
);


ALTER TABLE public.w22verifica_criticita OWNER TO weboll;

--
-- Data for Name: w22verifica_criticita; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.w22verifica_criticita (id_w22_criticita, descrizione, colore_html) FROM stdin;
-	N.D	#FFFFFF
A	Assente	#6EBB00
O	Ordinaria	#FFFF00
M	Moderata	#FFA500
E	Elevata	#FF0000
\.


--
-- Name: w22_criticita_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace:
--

ALTER TABLE ONLY public.w22verifica_criticita
    ADD CONSTRAINT w22verifica_criticita_pkey PRIMARY KEY (id_w22_criticita);


--
-- Name: TABLE w22verifica_criticita; Type: ACL; Schema: public; Owner: weboll
--

