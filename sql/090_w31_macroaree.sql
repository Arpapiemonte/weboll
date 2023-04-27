--
-- PostgreSQL database dump
--

-- Dumped from database version 13.7 (Debian 13.7-1.pgdg110+1)
-- Dumped by pg_dump version 13.7 (Debian 13.7-1.pgdg110+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: w31_macroaree; Type: TABLE; Schema: public; Owner: weboll
--

CREATE TABLE public.w31_macroaree (
    id_w31_macroaree integer NOT NULL,
    nome character varying(100) NOT NULL,
    ordine_bollettino integer NOT NULL
);


ALTER TABLE public.w31_macroaree OWNER TO weboll;

--
-- Data for Name: w31_macroaree; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.w31_macroaree (id_w31_macroaree, nome, ordine_bollettino) FROM stdin;
1	Cuneo SO	4
2	Nord	1
3	Torino Nord	2
4	Torino Ovest	3
5	SudEst	6
6	Cuneo SE	5
\.


--
-- Name: w31_macroaree w31_macroaree_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w31_macroaree
    ADD CONSTRAINT w31_macroaree_pkey PRIMARY KEY (id_w31_macroaree);


--
-- PostgreSQL database dump complete
--

