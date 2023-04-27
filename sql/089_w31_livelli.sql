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
-- Name: w31_livelli; Type: TABLE; Schema: public; Owner: weboll
--

CREATE TABLE public.w31_livelli (
    id_w31_livelli integer NOT NULL,
    colore character varying(10) NOT NULL
);


ALTER TABLE public.w31_livelli OWNER TO weboll;

--
-- Data for Name: w31_livelli; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.w31_livelli (id_w31_livelli, colore) FROM stdin;
1	cyan
2	green
3	yellow
4	orange
5	red
\.


--
-- Name: w31_livelli w31_livelli_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll
--

ALTER TABLE ONLY public.w31_livelli
    ADD CONSTRAINT w31_livelli_pkey PRIMARY KEY (id_w31_livelli);


--
-- PostgreSQL database dump complete
--

