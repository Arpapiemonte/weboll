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
-- Name: w22_tendenza; Type: TABLE; Schema: public; Owner: weboll; Tablespace:
--

CREATE TABLE public.w22_tendenza (
    id_w22_tendenza character varying(2) NOT NULL,
    descrizione text
);


ALTER TABLE public.w22_tendenza OWNER TO weboll;

--
-- Data for Name: w22_tendenza; Type: TABLE DATA; Schema: public; Owner: weboll
--

COPY public.w22_tendenza (id_w22_tendenza, descrizione) FROM stdin;
1	stazionario
2	diminuzione
3	crescita
\.


--
-- Name: w22_tendenza_pkey; Type: CONSTRAINT; Schema: public; Owner: weboll; Tablespace:
--

ALTER TABLE ONLY public.w22_tendenza
    ADD CONSTRAINT w22_tendenza_pkey PRIMARY KEY (id_w22_tendenza);

CREATE UNIQUE INDEX w22_tendenza_unique ON public.w22_tendenza (descrizione);


--
-- Name: TABLE w22_tendenza; Type: ACL; Schema: public; Owner: weboll
--


